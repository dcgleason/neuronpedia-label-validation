#!/usr/bin/env python3
"""Neuronpedia label checker: the full automated loop.

Stages: load labels -> generate or load prompts -> validate -> LOCK
(write <out>-prompts-locked.json + .sha256) -> score all prompts
(resumable, incremental save, disk-cached) -> run mechanism checks on
FAILs only -> write <out>-results.json and <out>-summary.md in the
scaleup-summary format, with a mechanism tag on every failure.

Labels input (--labels), any of:
  - a JSON list: [{layer, source, index, label}, ...]
  - {"tests": [...]} in pilot-prompts shape (layer/source default to
    12 / 12-gemmascope-res-16k)
  - the scaleup labels.json dict shape {"12:3473": {"label": ...}}
Or sample fresh features: --sample N --layers 6,12,18 --seed S
(labels fetched from the public feature API; features already used by
the pilot/scale-up are excluded when those files are present).

Prompt generation: --prompts-in <file> (externally generated), else the
Anthropic API when ANTHROPIC_API_KEY is available (environment or a
.env file — see envkeys.py), else a clear error.
Register-swap rewrites: --rewrites-in <file> mapping test number ->
[rewrite of sf1, rewrite of sf2]; else the Anthropic API when a key is
available; else the register check uses its template probe only.
Style probes (mechanisms v3): --style-in <file> mapping test number ->
{"probes": [s1, s2]} or a bare list of sentences. A style probe
imitates the style/register of the feature's stored positive examples
on a NEUTRAL topic; the register check scores supplied style probes in
preference to generated ones, rewrites, and the template probe.
"""
import argparse
import hashlib
import json
import os
import random
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import envkeys  # noqa: E402
import generate as gen  # noqa: E402
import mechanisms  # noqa: E402
from score import AuthError, RateLimitError, Scorer  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
ANTHRO = os.path.dirname(BASE)  # ~/workspace/anthropic-residency
DEFAULT_SOURCE = "12-gemmascope-res-16k"


def now_iso():
    return datetime.now(ZoneInfo("America/New_York")).isoformat()


def normalize_labels(data):
    """Any supported labels shape -> [{test, layer, source, index, label}]."""
    records = []
    if isinstance(data, dict) and "tests" in data:
        items = data["tests"]
        for i, t in enumerate(items, 1):
            layer = t.get("layer", 12)
            records.append({
                "test": t.get("test", i), "layer": layer,
                "source": t.get("source", f"{layer}-gemmascope-res-16k"),
                "index": t["index"], "label": t["label"],
            })
    elif isinstance(data, dict):
        for key, v in data.items():
            layer_s, index_s = key.split(":")
            layer = int(layer_s)
            records.append({
                "test": len(records) + 1, "layer": layer,
                "source": f"{layer}-gemmascope-res-16k",
                "index": int(index_s), "label": v["label"],
            })
    elif isinstance(data, list):
        for i, t in enumerate(data, 1):
            layer = t["layer"]
            records.append({
                "test": t.get("test", i), "layer": layer,
                "source": t.get("source", f"{layer}-gemmascope-res-16k"),
                "index": t["index"], "label": t["label"],
            })
    return records


def sample_labels(n, layers, seed):
    """Random fresh features per layer; labels from the public API."""
    rng = random.Random(seed)
    excluded = set()
    for rel in ("pilot-prompts.json", "scaleup/scaleup-prompts-locked.json"):
        path = os.path.join(ANTHRO, rel)
        if os.path.exists(path):
            with open(path) as f:
                for t in json.load(f)["tests"]:
                    excluded.add((t.get("layer", 12), int(t["index"])))
    per_layer = {}
    remaining = n
    for j, layer in enumerate(layers):
        take = remaining // (len(layers) - j)
        per_layer[layer] = take
        remaining -= take
    records = []
    for layer in layers:
        source = f"{layer}-gemmascope-res-16k"
        want = per_layer[layer]
        tried = set()
        got = 0
        while got < want and len(tried) < want * 30:
            index = rng.randrange(0, 16384)
            if index in tried or (layer, index) in excluded:
                continue
            tried.add(index)
            try:
                feature = mechanisms.fetch_feature(source, index)
            except Exception:
                continue
            explanations = feature.get("explanations") or []
            label = None
            for e in explanations:
                if e.get("description"):
                    label = e["description"]
                    break
            if not label:
                continue
            records.append({
                "test": len(records) + 1, "layer": layer, "source": source,
                "index": index, "label": label,
            })
            got += 1
    return records


def fmt(v):
    return f"{v:.2f}" if isinstance(v, (int, float)) else "—"


def verdict_of(vals):
    if any(v is None for v in vals.values()):
        return None, None
    margin = min(vals["sf1"], vals["sf2"]) - max(vals["nm1"], vals["nm2"])
    return ("PASS" if margin > 0 else "FAIL"), margin


def write_summary(out_prefix, tests, results, mech_tags):
    lines = [
        "# Checker results",
        "",
        "Pass rule (pilot rule): min(should-fire) > max(near-miss). "
        "Prompts were locked before scoring "
        f"(SHA-256 in {os.path.basename(out_prefix)}-prompts-locked.sha256).",
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
        verdict, margin = verdict_of(vals)
        if verdict is not None:
            st["pass" if verdict == "PASS" else "fail"] += 1
            pred_total += 1
            if verdict == t["predicted"]:
                pred_right += 1
            row = (
                f"- Test {t['test']} (L{t['layer']}, idx {t['index']}) "
                f"\"{t['label']}\": SF {fmt(vals['sf1'])}, {fmt(vals['sf2'])} · "
                f"NM {fmt(vals['nm1'])}, {fmt(vals['nm2'])} · margin {margin:.2f} · "
                f"**{verdict}** (predicted {t['predicted']})"
            )
            if verdict == "FAIL" and mech_tags.get(t["test"]):
                row += f" · mechanism: {mech_tags[t['test']]}"
            rows.append(row)
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
        f"**Scored so far: {tot_pass} pass, {tot_fail} fail, {tot_inc} "
        f"incomplete of {len(tests)}.**"
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
    with open(out_prefix + "-summary.md", "w") as f:
        f.write("\n".join(lines) + "\n")


def normalize_style_probes(data):
    """--style-in JSON -> {str(test_no): [probe, ...]}.

    Values may be {"probes": [...]} (extra keys, e.g. an "index" note,
    are ignored) or a bare list of sentences. Blank/non-string entries
    are dropped.
    """
    out = {}
    for key, value in data.items():
        if isinstance(value, dict):
            probes = value.get("probes") or []
        else:
            probes = value or []
        out[str(key)] = [p for p in probes
                         if isinstance(p, str) and p.strip()]
    return out


def build_rewrite_fn(rewrites, test):
    """Per-test sentence->rewrite lookup, or the Anthropic rewriter."""
    if rewrites is not None:
        mapping = rewrites.get(str(test["test"])) or rewrites.get(test["test"])
        if not mapping:
            return None
        if isinstance(mapping, dict):
            pairs = {test["should_fire"][0]: mapping.get("sf1"),
                     test["should_fire"][1]: mapping.get("sf2")}
        else:
            pairs = {test["should_fire"][0]: mapping[0],
                     test["should_fire"][1]: mapping[1] if len(mapping) > 1 else None}
        return lambda s: pairs.get(s)
    if os.environ.get("ANTHROPIC_API_KEY") and hasattr(gen, "anthropic_rewrite"):
        return gen.anthropic_rewrite
    return None


def main():
    ap = argparse.ArgumentParser(description="Run the Neuronpedia label checker.")
    ap.add_argument("--labels", default=None, help="labels JSON file")
    ap.add_argument("--sample", type=int, default=None,
                    help="sample N fresh features instead of a labels file")
    ap.add_argument("--layers", default="6,12,18")
    ap.add_argument("--seed", type=int, default=20261113)
    ap.add_argument("--prompts-in", default=None)
    ap.add_argument("--rewrites-in", default=None)
    ap.add_argument("--style-in", default=None,
                    help="JSON: test number -> {\"probes\": [sentences]} "
                         "or [sentences]; style probes for the register "
                         "check (mechanisms v3)")
    ap.add_argument("--out", default=None, help="output prefix")
    args = ap.parse_args()

    # Pick up keys from a .env file (real environment wins) so every
    # os.environ check below and in generate.py sees them.
    envkeys.load_dotenv()

    if args.out is None:
        stamp = datetime.now(ZoneInfo("America/New_York")).strftime("%Y%m%d-%H%M%S")
        args.out = os.path.join(BASE, f"run-{stamp}")

    if args.labels:
        with open(args.labels) as f:
            labels = normalize_labels(json.load(f))
    elif args.sample:
        layers = [int(x) for x in args.layers.split(",")]
        labels = sample_labels(args.sample, layers, args.seed)
    else:
        print("run_checker: give --labels <file> or --sample N", file=sys.stderr)
        return 2
    print(f"{len(labels)} labels loaded.", flush=True)

    try:
        tests = gen.generate(labels, args.prompts_in)
    except gen.GenerationUnavailable as e:
        print(f"run_checker: {e}", file=sys.stderr)
        return 2

    # LOCK: prompts are frozen before any scoring, hash recorded.
    locked_path = args.out + "-prompts-locked.json"
    with open(locked_path, "w") as f:
        json.dump({"tests": tests}, f, indent=2, ensure_ascii=False)
    digest = hashlib.sha256(open(locked_path, "rb").read()).hexdigest()
    with open(args.out + "-prompts-locked.sha256", "w") as f:
        f.write(f"{digest}  {os.path.basename(locked_path)}\n")
    print(f"locked {len(tests)} tests -> {locked_path} (sha256 {digest[:12]}…)",
          flush=True)

    rewrites = None
    if args.rewrites_in:
        with open(args.rewrites_in) as f:
            rewrites = json.load(f)

    style_probes = None
    if args.style_in:
        with open(args.style_in) as f:
            style_probes = normalize_style_probes(json.load(f))

    raw_path = args.out + "-results.json"
    raw = {"started_at": now_iso(), "results": {}, "mechanisms": {}}
    if os.path.exists(raw_path):
        with open(raw_path) as f:
            raw = json.load(f)
    results = raw.setdefault("results", {})

    scorer = Scorer()
    jobs = []
    for t in tests:
        for kind, prompts in (("sf", t["should_fire"]), ("nm", t["near_miss"])):
            for n, prompt in enumerate(prompts, 1):
                jobs.append((f"s{t['test']:03d}-{kind}{n}", t, prompt))
    done = sum(1 for k, _, _ in jobs
               if results.get(k, {}).get("max_activation") is not None)
    print(f"{done}/{len(jobs)} already scored. Starting.", flush=True)
    try:
        for key, t, prompt in jobs:
            if results.get(key, {}).get("max_activation") is not None:
                continue
            value = scorer.get_activation(t["source"], t["index"], prompt)
            results[key] = {"test": t["test"], "layer": t["layer"],
                            "index": t["index"], "label": t["label"],
                            "prompt": prompt, "ok": True,
                            "max_activation": value}
            raw["updated_at"] = now_iso()
            with open(raw_path, "w") as f:
                json.dump(raw, f, indent=2, ensure_ascii=False)
            print(f"{key}: {value:.2f}", flush=True)
    except AuthError as e:
        print(f"run_checker: {e}", file=sys.stderr)
        return 3
    except RateLimitError as e:
        print(f"run_checker: {e}", file=sys.stderr)
        return 4
    print(f"scoring done ({scorer.n_api_calls} API calls, "
          f"{scorer.n_cache_hits} cache hits).", flush=True)

    # Mechanism checks on failures only.
    mech_tags = {}
    mech_store = raw.setdefault("mechanisms", {})
    for t in tests:
        key = lambda kind, n: f"s{t['test']:03d}-{kind}{n}"  # noqa: E731
        vals = {}
        for kind in ("sf", "nm"):
            for n in (1, 2):
                rec = results.get(key(kind, n))
                vals[f"{kind}{n}"] = rec.get("max_activation") if rec else None
        verdict, _margin = verdict_of(vals)
        if verdict != "FAIL":
            continue
        record = {"layer": t["layer"], "source": t["source"],
                  "index": t["index"], "label": t["label"]}
        rewrite_fn = build_rewrite_fn(rewrites, t)
        test_style_probes = (
            style_probes.get(str(t["test"])) if style_probes else None
        )
        mech = mechanisms.run_all(
            record, t, scorer.get_activation, rewrite_fn=rewrite_fn,
            style_probes=test_style_probes,
        )
        tag = mechanisms.classify(record, vals, mech)
        mech_tags[t["test"]] = tag
        mech_store[str(t["test"])] = {"index": t["index"], "tag": tag,
                                      "checks": mech}
        print(f"test {t['test']} (idx {t['index']}): mechanism {tag}",
              flush=True)
    raw["updated_at"] = now_iso()
    with open(raw_path, "w") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)
    write_summary(args.out, tests, results, mech_tags)
    print(f"wrote {raw_path} and {args.out}-summary.md")
    print("Run complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
