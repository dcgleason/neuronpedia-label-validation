#!/usr/bin/env python3
"""Scale-up harness: 160 features x 4 prompts, layers 6/12/18.

The connector helper hardcodes layer 12, so this runner implements the
same request with a per-test source, reusing the connector's credential
plumbing. Pass rule (pilot rule): min(should-fire) > max(near-miss).
Each test carries a pre-registered predicted verdict; the summary reports
prediction accuracy alongside pass rates. Results save incrementally to
scaleup-results.json; summary rewritten to scaleup-summary.md.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import (  # noqa: E402
    DynamicCredentialError,
    add_surrogate_to_request,
    read_json_response,
)

BASE = os.path.expanduser("~/workspace/anthropic-residency/scaleup")
PROMPTS = os.path.join(BASE, "scaleup-prompts-locked.json")
RAW = os.path.join(BASE, "scaleup-results.json")
SUMMARY = os.path.join(BASE, "scaleup-summary.md")
API_URL = "https://www.neuronpedia.org/api/activation/new"
HOST = "www.neuronpedia.org"
PAUSE = 0.3


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")


def extract_max(obj):
    if isinstance(obj, dict):
        vals = obj.get("values")
        if isinstance(vals, list) and vals and all(
            isinstance(v, (int, float)) for v in vals
        ):
            return max(vals)
        for v in obj.values():
            found = extract_max(v)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = extract_max(v)
            if found is not None:
                return found
    return None


def get_activation(source, index, text):
    body = {
        "feature": {"modelId": "gemma-2-2b", "source": source, "index": str(index)},
        "customText": text,
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        add_surrogate_to_request(request, "custom.neuronpedia", allowed_hosts=[HOST])
        with urllib.request.build_opener(NoRedirect()).open(
            request, timeout=60
        ) as response:
            parsed = read_json_response(response)
            return {"ok": True, "status": response.status,
                    "max_activation": extract_max(parsed), "response": parsed}
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8", "replace")[:1000]
        except Exception:
            detail = ""
        return {"ok": False, "status": e.code, "error": f"HTTP {e.code}",
                "detail": detail}
    except DynamicCredentialError as e:
        return {"ok": False, "status": None, "error": f"credential: {e}"}
    except Exception as e:
        return {"ok": False, "status": None, "error": f"{type(e).__name__}: {e}"}


def fmt(v):
    return f"{v:.2f}" if isinstance(v, (int, float)) else "—"


def write_summary(tests, results):
    lines = [
        "# Scale-up results — 160 additional labels (layers 6, 12, 18)",
        "",
        "Pass rule (pilot rule): min(should-fire) > max(near-miss). "
        "Predicted verdicts were registered in scaleup-prompts-locked.json "
        "before the run (SHA-256 in scaleup-prompts-locked.sha256).",
        "",
    ]
    stats = {}
    pred_right = pred_total = 0
    rows = []
    for t in tests:
        key = lambda kind, n: f"s{t['test']:03d}-{kind}{n}"  # noqa: E731
        vals = {}
        for kind in ("sf", "nm"):
            for n in (1, 2):
                rec = results.get(key(kind, n))
                vals[f"{kind}{n}"] = rec.get("max_activation") if rec else None
        st = stats.setdefault(t["layer"], {"pass": 0, "fail": 0, "inc": 0})
        if all(v is not None for v in vals.values()):
            margin = min(vals["sf1"], vals["sf2"]) - max(vals["nm1"], vals["nm2"])
            verdict = "PASS" if margin > 0 else "FAIL"
            st["pass" if margin > 0 else "fail"] += 1
            pred_total += 1
            if verdict == t["predicted"]:
                pred_right += 1
            rows.append(
                f"- Test {t['test']} (L{t['layer']}, idx {t['index']}) "
                f"\"{t['label']}\": SF {fmt(vals['sf1'])}, {fmt(vals['sf2'])} · "
                f"NM {fmt(vals['nm1'])}, {fmt(vals['nm2'])} · margin {margin:.2f} · "
                f"**{verdict}** (predicted {t['predicted']})"
            )
        else:
            st["inc"] += 1
            rows.append(
                f"- Test {t['test']} (L{t['layer']}, idx {t['index']}) "
                f"\"{t['label']}\": INCOMPLETE"
            )
    tot_pass = sum(s["pass"] for s in stats.values())
    tot_fail = sum(s["fail"] for s in stats.values())
    tot_inc = sum(s["inc"] for s in stats.values())
    lines.append(
        f"**Scored so far: {tot_pass} pass, {tot_fail} fail, {tot_inc} incomplete "
        f"of {len(tests)}.**"
    )
    for layer in sorted(stats):
        s = stats[layer]
        lines.append(
            f"- Layer {layer}: {s['pass']} pass, {s['fail']} fail, {s['inc']} incomplete"
        )
    if pred_total:
        lines.append(
            f"- Prediction accuracy: {pred_right}/{pred_total} "
            f"({100.0 * pred_right / pred_total:.0f}%)"
        )
    lines.append("")
    lines.extend(rows)
    with open(SUMMARY, "w") as f:
        f.write("\n".join(lines) + "\n")


def main():
    with open(PROMPTS) as f:
        tests = json.load(f)["tests"]
    raw = {"started_at": datetime.now(ZoneInfo("America/New_York")).isoformat(),
           "results": {}}
    if os.path.exists(RAW):
        with open(RAW) as f:
            raw = json.load(f)
    results = raw["results"]
    jobs = []
    for t in tests:
        for kind, prompts in (("sf", t["should_fire"]), ("nm", t["near_miss"])):
            for n, prompt in enumerate(prompts, 1):
                jobs.append((f"s{t['test']:03d}-{kind}{n}", t, prompt))
    done = sum(1 for k, _, _ in jobs
               if results.get(k, {}).get("max_activation") is not None)
    print(f"{done}/{len(jobs)} already scored. Starting.", flush=True)
    for key, t, prompt in jobs:
        if results.get(key, {}).get("max_activation") is not None:
            continue
        att = get_activation(t["source"], t["index"], prompt)
        if not att["ok"] and att.get("status") == 429:
            print(f"{key}: rate limited, waiting 60s, retrying once.", flush=True)
            time.sleep(60)
            att = get_activation(t["source"], t["index"], prompt)
        rec = {"test": t["test"], "layer": t["layer"], "index": t["index"],
               "label": t["label"], "prompt": prompt, "ok": att["ok"],
               "max_activation": att.get("max_activation")}
        if not att["ok"]:
            rec["error"] = att.get("error")
            rec["status"] = att.get("status")
        else:
            rec.pop("prompt", None)
            rec["prompt"] = prompt
        results[key] = rec
        raw["updated_at"] = datetime.now(ZoneInfo("America/New_York")).isoformat()
        with open(RAW, "w") as f:
            json.dump(raw, f, indent=2, ensure_ascii=False)
        write_summary(tests, results)
        print(f"{key}: {fmt(att.get('max_activation'))}", flush=True)
        if not att["ok"]:
            if att.get("status") in (401, 403):
                print("Authorization failure. Stopping.")
                return 3
            if att.get("status") == 429:
                print("Still rate limited. Stopping.")
                return 4
        time.sleep(PAUSE)
    print("Run complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
