#!/usr/bin/env python3
"""Run the label-rewrite test set.

Input: label-rewrite-prompts-locked.json (21 corrected labels x 4 prompts).
Pass rule (same as pilot): min(should-fire) > max(near-miss).
Every corrected label is predicted PASS. Results save incrementally to
label-rewrite-results.json; summary to label-rewrite-summary.md.
"""
import json
import os
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

BASE = os.path.expanduser("~/workspace/anthropic-residency/followup")
sys.path.insert(
    0, os.path.expanduser("~/workspace/custom-connectors/custom.neuronpedia/bin")
)
from np_activation import get_activation  # noqa: E402

PROMPTS = os.path.join(BASE, "label-rewrite-prompts-locked.json")
RAW = os.path.join(BASE, "label-rewrite-results.json")
SUMMARY = os.path.join(BASE, "label-rewrite-summary.md")
PAUSE = 0.3


def fmt(v):
    return f"{v:.2f}" if isinstance(v, (int, float)) else "—"


def write_summary(tests, results):
    lines = [
        "# Label-rewrite test — results",
        "",
        "Pass rule (pilot rule): min(should-fire) > max(near-miss). "
        "Standing prediction: every corrected label PASSes.",
        "",
    ]
    passed = failed = incomplete = 0
    for i, t in enumerate(tests, 1):
        vals = {}
        for kind in ("sf", "nm"):
            for n in (1, 2):
                rec = results.get(f"rw{i:02d}-{kind}{n}")
                vals[f"{kind}{n}"] = rec.get("max_activation") if rec else None
        lines.append(f"### idx {t['index']} — corrected: \"{t['corrected_label']}\"")
        lines.append(f"- Original: \"{t['original_label']}\"")
        lines.append(
            f"- Should-fire: {fmt(vals['sf1'])}, {fmt(vals['sf2'])} · "
            f"Near-miss: {fmt(vals['nm1'])}, {fmt(vals['nm2'])}"
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
            lines.append("- **INCOMPLETE**")
        lines.append("")
    lines.insert(3, f"**Scored: {passed} pass, {failed} fail, {incomplete} incomplete of {len(tests)}.**")
    lines.insert(4, "")
    with open(SUMMARY, "w") as f:
        f.write("\n".join(lines))


def main():
    with open(PROMPTS) as f:
        tests = json.load(f)["tests"]
    raw = {"started_at": datetime.now(ZoneInfo("America/New_York")).isoformat(), "results": {}}
    if os.path.exists(RAW):
        with open(RAW) as f:
            raw = json.load(f)
    results = raw["results"]
    for i, t in enumerate(tests, 1):
        for kind, prompts in (("sf", t["should_fire"]), ("nm", t["near_miss"])):
            for n, prompt in enumerate(prompts, 1):
                key = f"rw{i:02d}-{kind}{n}"
                if results.get(key, {}).get("max_activation") is not None:
                    continue
                att = get_activation(t["index"], prompt)
                if not att["ok"] and att.get("status") == 429:
                    print(f"{key}: rate limited, waiting 60s, retrying once.")
                    time.sleep(60)
                    att = get_activation(t["index"], prompt)
                rec = {"index": t["index"], "corrected_label": t["corrected_label"],
                       "kind": kind, "prompt": prompt, "ok": att["ok"],
                       "max_activation": att.get("max_activation")}
                if not att["ok"]:
                    rec["error"] = att.get("error")
                    rec["status"] = att.get("status")
                results[key] = rec
                raw["updated_at"] = datetime.now(ZoneInfo("America/New_York")).isoformat()
                with open(RAW, "w") as f:
                    json.dump(raw, f, indent=2, ensure_ascii=False)
                write_summary(tests, results)
                print(f"{key} idx{t['index']}: {fmt(att.get('max_activation'))}")
                if not att["ok"] and att.get("status") in (401, 403):
                    print("Authorization failure. Stopping.")
                    return 3
                if not att["ok"] and att.get("status") == 429:
                    print("Still rate limited. Stopping.")
                    return 4
                time.sleep(PAUSE)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
