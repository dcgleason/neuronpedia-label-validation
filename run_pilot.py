#!/usr/bin/env python3
"""Neuronpedia pilot harness.

Runs the 160 locked prompts from pilot-prompts.json against Neuronpedia's
POST /api/activation/new, one feature at a time, and scores each label
against the pre-registered pass rule:

    PASS if both should-fire prompts activate the feature clearly above
    both near-miss prompts, operationalized as min(should-fire max
    activations) > max(near-miss max activations). The margin
    (min SF - max NM) is reported for every test so "clearly" can be
    judged from the numbers.

The score for one prompt is the feature's max activation across tokens.

Results are saved incrementally to results-raw.json after every call, so
an interrupted run resumes where it stopped: prompts with a recorded
max_activation are skipped on the next run. results-summary.md is
rewritten after every call as well.

Rate limit: /api/activation/new allows 1000 requests per 60 minutes.
This run needs 160, far under the cap. A 0.3s pause between calls keeps
the pace gentle anyway. On HTTP 429 the harness waits 60 seconds and
retries that prompt once, then stops if still limited. On 401/403 or a
credential error it stops immediately, since every later call would fail
the same way.

Usage:
    python3 run_pilot.py            # run or resume the full pilot
"""

import json
import os
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

BASE = os.path.expanduser("~/workspace/anthropic-residency")
sys.path.insert(
    0, os.path.expanduser("~/workspace/custom-connectors/custom.neuronpedia/bin")
)
from np_activation import get_activation  # noqa: E402

PROMPTS_PATH = os.path.join(BASE, "pilot-prompts.json")
RAW_PATH = os.path.join(BASE, "results-raw.json")
SUMMARY_PATH = os.path.join(BASE, "results-summary.md")
PAUSE_SECONDS = 0.3


def load_raw():
    if os.path.exists(RAW_PATH):
        with open(RAW_PATH) as f:
            return json.load(f)
    return {
        "started_at": datetime.now(ZoneInfo("America/New_York")).isoformat(),
        "results": {},
    }


def save_raw(raw):
    raw["updated_at"] = datetime.now(ZoneInfo("America/New_York")).isoformat()
    tmp = RAW_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)
    os.replace(tmp, RAW_PATH)


def fmt(v):
    return f"{v:.2f}" if isinstance(v, (int, float)) else "—"


def write_summary(tests, raw):
    results = raw["results"]
    lines = [
        "# Pilot results — summary",
        "",
        "Pass rule (pre-registered): both should-fire prompts activate the "
        "feature clearly above both near-miss prompts. Scored as "
        "min(should-fire) > max(near-miss); the margin is min(SF) − max(NM). "
        "Each value is the feature's max activation across tokens for that prompt.",
        "",
    ]
    passed = failed = incomplete = 0
    for t in tests:
        key = lambda kind, n: f"t{t['test']:02d}-{kind}{n}"  # noqa: E731
        vals = {}
        for kind in ("sf", "nm"):
            for n in (1, 2):
                rec = results.get(key(kind, n))
                vals[f"{kind}{n}"] = rec.get("max_activation") if rec else None
        lines.append(
            f"### Test {t['test']} — idx {t['index']}, \"{t['label']}\""
        )
        lines.append("")
        lines.append(
            f"- Should-fire: {fmt(vals['sf1'])}, {fmt(vals['sf2'])}"
            f" · Near-miss: {fmt(vals['nm1'])}, {fmt(vals['nm2'])}"
        )
        if all(v is not None for v in vals.values()):
            margin = min(vals["sf1"], vals["sf2"]) - max(vals["nm1"], vals["nm2"])
            verdict = "PASS" if margin > 0 else "FAIL"
            if margin > 0:
                passed += 1
            else:
                failed += 1
            lines.append(f"- Margin: {margin:.2f} · **{verdict}**")
        else:
            incomplete += 1
            lines.append("- **INCOMPLETE** — not all four prompts have results yet.")
        lines.append("")
    lines.insert(
        3,
        f"**Scored so far: {passed} pass, {failed} fail, {incomplete} incomplete "
        f"of {len(tests)} tests.**",
    )
    lines.insert(4, "")
    with open(SUMMARY_PATH, "w") as f:
        f.write("\n".join(lines))


def main():
    with open(PROMPTS_PATH) as f:
        tests = json.load(f)["tests"]
    raw = load_raw()
    results = raw["results"]

    jobs = []
    for t in tests:
        for kind, prompts in (("sf", t["should_fire"]), ("nm", t["near_miss"])):
            for n, prompt in enumerate(prompts, start=1):
                jobs.append((f"t{t['test']:02d}-{kind}{n}", t, kind, prompt))

    done = sum(
        1
        for k, _, _, _ in jobs
        if results.get(k, {}).get("max_activation") is not None
    )
    print(f"{done}/{len(jobs)} prompts already scored. Starting.")

    for key, t, kind, prompt in jobs:
        if results.get(key, {}).get("max_activation") is not None:
            continue
        attempt = get_activation(t["index"], prompt)
        if not attempt["ok"] and attempt.get("status") == 429:
            print(f"{key}: rate limited, waiting 60s and retrying once.")
            time.sleep(60)
            attempt = get_activation(t["index"], prompt)
        rec = {
            "test": t["test"],
            "index": t["index"],
            "label": t["label"],
            "kind": kind,
            "prompt": prompt,
            "ok": attempt["ok"],
            "max_activation": attempt.get("max_activation"),
        }
        if not attempt["ok"]:
            rec["error"] = attempt.get("error")
            rec["status"] = attempt.get("status")
            rec["detail"] = attempt.get("detail", "")
        else:
            rec["response"] = attempt.get("response")
        results[key] = rec
        save_raw(raw)
        write_summary(tests, raw)

        if not attempt["ok"]:
            status = attempt.get("status")
            if status in (401, 403) or (
                status is None and "credential" in str(attempt.get("error", ""))
            ):
                print(
                    f"{key}: authorization failure ({attempt.get('error')}). "
                    "Stopping; every later call would fail the same way."
                )
                return 3
            if status == 429:
                print(f"{key}: still rate limited after retry. Stopping.")
                return 4
            print(f"{key}: call failed ({attempt.get('error')}). Continuing.")
        else:
            print(f"{key}: max activation {fmt(attempt.get('max_activation'))}")
        time.sleep(PAUSE_SECONDS)

    print("Run complete. Summary written to results-summary.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
