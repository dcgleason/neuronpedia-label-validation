#!/usr/bin/env python3
"""Calibrate checker verdicts against human ground truth.

Compares a checker results file (<out>-results.json from run_checker.py)
against a ground-truth results file (the pilot's results-raw.json or the
scale-up's scaleup-results.json, same record shape), matched by feature
index. Verdicts on both sides use the pilot pass rule:
min(should-fire) > max(near-miss).

Writes a Markdown agreement report: overall agreement %, the confusion
counts (both-pass, both-fail, checker-pass/human-fail,
checker-fail/human-pass), and the disagreement list with both sides'
scores. Optionally also scores mechanism tags when both the checker
results carry tags and --mechanism-truth is given as JSON mapping
index (string) -> established class.
"""
import argparse
import json
import re
import sys


def verdicts_from_results(raw):
    """{index: {verdict, sf:[..], nm:[..], margin, label}} from a raw results dict."""
    groups = {}
    for key, rec in raw.get("results", {}).items():
        m = re.match(r"^[a-z]?(\d+)-(sf|nm)(\d)$", key)
        if not m or rec.get("max_activation") is None:
            continue
        test_no = int(m.group(1))
        g = groups.setdefault(test_no, {"index": rec.get("index"),
                                        "label": rec.get("label"),
                                        "sf": {}, "nm": {}})
        g[m.group(2)][int(m.group(3))] = rec["max_activation"]
    out = {}
    for _test_no, g in groups.items():
        if len(g["sf"]) == 2 and len(g["nm"]) == 2:
            sf = [g["sf"][1], g["sf"][2]]
            nm = [g["nm"][1], g["nm"][2]]
            margin = min(sf) - max(nm)
            out[g["index"]] = {
                "verdict": "PASS" if margin > 0 else "FAIL",
                "sf": sf, "nm": nm, "margin": margin, "label": g["label"],
            }
    return out


def fmt(vals):
    return ", ".join(f"{v:.2f}" for v in vals)


def main():
    ap = argparse.ArgumentParser(description="Compare checker verdicts to ground truth.")
    ap.add_argument("--checker-results", required=True)
    ap.add_argument("--ground-truth", required=True,
                    help="pilot results-raw.json or scaleup-results.json")
    ap.add_argument("--mechanism-truth", default=None,
                    help="JSON file mapping index (string) -> established mechanism class")
    ap.add_argument("--out", default=None, help="write the report here (default: stdout)")
    args = ap.parse_args()

    with open(args.checker_results) as f:
        checker_raw = json.load(f)
    with open(args.ground_truth) as f:
        truth_raw = json.load(f)
    checker = verdicts_from_results(checker_raw)
    truth = verdicts_from_results(truth_raw)

    common = sorted(set(checker) & set(truth), key=lambda i: int(i))
    if not common:
        print("calibrate: no overlapping feature indices.", file=sys.stderr)
        return 2
    both_pass = both_fail = c_pass_h_fail = c_fail_h_pass = 0
    disagreements = []
    for index in common:
        c, h = checker[index], truth[index]
        if c["verdict"] == "PASS" and h["verdict"] == "PASS":
            both_pass += 1
        elif c["verdict"] == "FAIL" and h["verdict"] == "FAIL":
            both_fail += 1
        elif c["verdict"] == "PASS":
            c_pass_h_fail += 1
            disagreements.append((index, c, h))
        else:
            c_fail_h_pass += 1
            disagreements.append((index, c, h))
    agree = both_pass + both_fail
    lines = [
        "# Calibration report",
        "",
        f"Compared {len(common)} features (matched by index) between the "
        "checker run and the human ground truth. Pass rule on both sides: "
        "min(should-fire) > max(near-miss).",
        "",
        f"**Agreement: {agree}/{len(common)} "
        f"({100.0 * agree / len(common):.1f}%)**",
        "",
        f"- Both PASS: {both_pass}",
        f"- Both FAIL: {both_fail}",
        f"- Checker PASS / human FAIL: {c_pass_h_fail}",
        f"- Checker FAIL / human PASS: {c_fail_h_pass}",
        "",
        "## Disagreements",
        "",
    ]
    if disagreements:
        for index, c, h in disagreements:
            lines.append(
                f"- idx {index} \"{c['label']}\": checker {c['verdict']} "
                f"(SF {fmt(c['sf'])} · NM {fmt(c['nm'])} · margin "
                f"{c['margin']:.2f}) vs human {h['verdict']} "
                f"(SF {fmt(h['sf'])} · NM {fmt(h['nm'])} · margin "
                f"{h['margin']:.2f})"
            )
    else:
        lines.append("- None.")

    if args.mechanism_truth:
        with open(args.mechanism_truth) as f:
            truth_tags = {int(k): v for k, v in json.load(f).items()}
        mech_store = checker_raw.get("mechanisms", {})
        tag_by_index = {}
        tests_by_no = {}
        for key, rec in checker_raw.get("results", {}).items():
            m = re.match(r"^[a-z]?(\d+)-", key)
            if m:
                tests_by_no[int(m.group(1))] = rec.get("index")
        for test_no_s, entry in mech_store.items():
            index = entry.get("index", tests_by_no.get(int(test_no_s)))
            if index is not None:
                tag_by_index[int(index)] = entry.get("tag")
        lines += ["", "## Mechanism tags vs established classes", ""]
        scored = correct = 0
        detail = []
        for index in sorted(truth_tags):
            expected = truth_tags[index]
            got = tag_by_index.get(index)
            if got is None:
                detail.append(
                    f"- idx {index}: expected {expected}, checker gave no "
                    "tag (feature did not FAIL under the checker's prompts)"
                )
                scored += 1
                continue
            scored += 1
            ok = got == expected
            correct += ok
            detail.append(
                f"- idx {index}: expected {expected}, checker {got} "
                f"({'match' if ok else 'MISS'})"
            )
        lines.append(
            f"**Mechanism accuracy on tagged ground truth: {correct}/{scored} "
            f"({100.0 * correct / scored:.1f}% of {scored} established cases; "
            "a case with no checker tag counts as a miss)**"
        )
        lines.append("")
        lines.extend(detail)

    report = "\n".join(lines) + "\n"
    if args.out:
        with open(args.out, "w") as f:
            f.write(report)
        print(f"wrote {args.out}")
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
