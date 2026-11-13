#!/usr/bin/env python3
"""Prompt generation for the Neuronpedia label checker.

Three modes:
  (a) ANTHROPIC_API_KEY available (real environment, or a .env file
      next to these scripts — see envkeys.py and .env.example) -> call
      the Anthropic Messages API directly (plain requests via urllib).
      Model from CHECKER_MODEL (default claude-sonnet-5-5),
      temperature 0.2. Fully implemented; this is the standalone
      plug-in point. Verify it end-to-end with:
          python3 generate.py --check-key
  (b) --prompts-in <file>: load externally generated prompts (e.g.
      written by Muse in-session) and validate them.
  (c) Neither -> exit with a clear message.

Output schema matches scaleup-prompts-locked.json: {"tests": [ {test,
layer, source, index, label, should_fire: [sf1, sf2], near_miss:
[nm1, nm2], predicted, basis} ]}.
"""
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import envkeys  # noqa: E402

# ---------------------------------------------------------------------------
# The generation template. Encodes the pilot's rules (Nov 12, 2026):
# plain ordinary sentences, never best-case / example-style text; each
# near-miss changes exactly one variable relative to a should-fire; a
# registered PASS/FAIL prediction and a one-line basis for every test.
# ---------------------------------------------------------------------------
TEMPLATE = """You are writing a held-out test for one auto-generated interpretability label of a sparse-autoencoder feature in the Gemma-2-2B language model.

Feature label under test: "{label}"

Write exactly four short test sentences:

1. should_fire[0] and should_fire[1]: two plain, ordinary, everyday sentences that clearly express what the label describes. Rules:
   - Plain contemporary prose, 8-20 words each, the kind of sentence that appears in ordinary writing.
   - NEVER write best-case or example-style text: no top-activation-style excerpts, no lists of related terms, no keyword-stuffed text, no document fragments.
   - The two should-fires should differ from each other in wording and context, not be near-copies.

2. near_miss[0] and near_miss[1]: two sentences that look close to the label but should NOT activate the feature if the label is accurate. Rules:
   - Each near-miss changes exactly ONE variable relative to a should-fire sentence: swap the key word for a close neighbour, use the same word in a different sense, or keep the topic but remove the labelled element.
   - A near-miss must not itself be a clear instance of what the label describes.
   - Plain ordinary prose, same length range.

3. predicted: "PASS" if you expect both should-fires to activate clearly above both near-misses under the rule min(should-fire) > max(near-miss), else "FAIL". Predict PASS only when the label names a concrete, narrow, detectable pattern; predict FAIL when the label is broad, abstract, bundles unrelated senses, or names a topic a feature is unlikely to track as such.

4. basis: one line (max ~25 words) stating why you predicted that verdict.

Respond with ONLY a JSON object, no other text:
{{"should_fire": ["...", "..."], "near_miss": ["...", "..."], "predicted": "PASS" or "FAIL", "basis": "..."}}
"""

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
# Current Sonnet as of Nov 2026 (claude-sonnet-4-5 retires 2026-11-30).
DEFAULT_MODEL = "claude-sonnet-5-5"
TEMPERATURE = 0.2


class GenerationUnavailable(RuntimeError):
    pass


class AnthropicAPIError(RuntimeError):
    """An error response from the Anthropic API.

    Carries only the HTTP status and the API's own error type/message.
    Never carries the API key or the request headers.
    """

    def __init__(self, status, message):
        if status:
            super().__init__(f"Anthropic API HTTP {status}: {message}")
        else:
            super().__init__(f"Anthropic API request failed: {message}")
        self.status = status
        self.message = message


def validate_test(test):
    """Validate one test record against the scaleup-prompts schema."""
    problems = []
    for key in ("test", "layer", "source", "index", "label",
                "should_fire", "near_miss", "predicted", "basis"):
        if key not in test:
            problems.append(f"missing key {key!r}")
    if problems:
        return problems
    sf, nm = test["should_fire"], test["near_miss"]
    if not (isinstance(sf, list) and len(sf) == 2
            and all(isinstance(s, str) and s.strip() for s in sf)):
        problems.append("should_fire must be a list of 2 non-empty strings")
    if not (isinstance(nm, list) and len(nm) == 2
            and all(isinstance(s, str) and s.strip() for s in nm)):
        problems.append("near_miss must be a list of 2 non-empty strings")
    if not problems:
        all_prompts = [s.strip() for s in sf + nm]
        if len(set(all_prompts)) != 4:
            problems.append("the 4 prompts are not all distinct")
        if set(s.strip() for s in sf) & set(s.strip() for s in nm):
            problems.append("a near-miss duplicates a should-fire")
    if test["predicted"] not in ("PASS", "FAIL"):
        problems.append("predicted must be PASS or FAIL")
    if not str(test["basis"]).strip():
        problems.append("basis is empty")
    return problems


def validate_tests(tests):
    """Validate a list of test records; returns {test_number: [problems]}."""
    bad = {}
    for t in tests:
        problems = validate_test(t)
        if problems:
            bad[t.get("test", "?")] = problems
    return bad


def _extract_json(text):
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("no JSON object in model response")
    return json.loads(text[start:end + 1])


def _anthropic_messages(prompt_text, max_tokens, temperature=TEMPERATURE,
                        timeout=120):
    """One call to the Anthropic Messages API; returns the response text.

    THE plug-in point for standalone generation: the key is resolved
    via envkeys at call time (real environment first, then a .env file
    next to the scripts; on an interactive terminal the user is
    prompted to paste it). It is never logged, and is written to disk
    only into a .env the user explicitly approved. The model comes
    from CHECKER_MODEL (default DEFAULT_MODEL). Raises
    AnthropicAPIError on an API error response, GenerationUnavailable
    if no key is available, ValueError if the response carries no
    text. Newer Claude models reject sampling parameters; if the API
    answers 400 over `temperature`, the call is retried once without
    it.
    """
    api_key = envkeys.require_key(
        "ANTHROPIC_API_KEY",
        what_for="to generate prompts with the Anthropic API",
        where_to_get="console.anthropic.com (API Keys)",
    )
    if not api_key:
        raise GenerationUnavailable(
            "ANTHROPIC_API_KEY is not set. Set it either way: "
            'export ANTHROPIC_API_KEY="sk-ant-...", or copy '
            ".env.example to .env in this folder and paste the key there."
        )
    model = os.environ.get("CHECKER_MODEL", DEFAULT_MODEL)

    def _call(include_temperature):
        body = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt_text}],
        }
        if include_temperature and temperature is not None:
            body["temperature"] = temperature
        request = urllib.request.Request(
            ANTHROPIC_URL,
            data=json.dumps(body).encode(),
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": ANTHROPIC_VERSION,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                parsed = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                err = json.loads(e.read().decode("utf-8", "replace"))
                detail = (err.get("error") or {}).get("message", "")
            except Exception:
                detail = ""
            raise AnthropicAPIError(
                e.code, detail or f"HTTP {e.code} with no error message"
            ) from e
        except (TimeoutError, OSError) as e:
            # Connection refused/reset, DNS failure, read timeout, etc.
            raise AnthropicAPIError(
                None, f"{type(e).__name__}: {e} (is api.anthropic.com "
                "reachable from this machine?)"
            ) from e
        text = "".join(
            block.get("text", "")
            for block in parsed.get("content", [])
            if block.get("type") == "text"
        )
        if not text.strip():
            raise ValueError(
                f"Anthropic response from {model} contained no text blocks "
                f"(stop_reason={parsed.get('stop_reason')!r})"
            )
        return text

    try:
        return _call(include_temperature=True)
    except AnthropicAPIError as e:
        if e.status == 400 and "temperature" in e.message.lower():
            return _call(include_temperature=False)
        raise


def _anthropic_generate_one(label_record):
    """Generate one test for one label via the Anthropic API (mode (a)).

    Sends the generation TEMPLATE as the user prompt, parses the JSON
    reply, and returns the raw {should_fire, near_miss, predicted,
    basis} dict. Schema validation happens in generate_via_anthropic
    through the same validate_test path mode (b) uses.
    """
    text = _anthropic_messages(
        TEMPLATE.format(label=label_record["label"]), max_tokens=1024
    )
    return _extract_json(text)


def generate_via_anthropic(labels):
    """Mode (a): generate prompts for every label via the Anthropic API."""
    tests = []
    for i, rec in enumerate(labels, 1):
        last_err = None
        for _attempt in range(2):
            try:
                gen = _anthropic_generate_one(rec)
                test = {
                    "test": rec.get("test", i),
                    "layer": rec["layer"],
                    "source": rec["source"],
                    "index": rec["index"],
                    "label": rec["label"],
                    "should_fire": gen["should_fire"],
                    "near_miss": gen["near_miss"],
                    "predicted": gen["predicted"],
                    "basis": gen["basis"],
                }
                problems = validate_test(test)
                if problems:
                    raise ValueError("; ".join(problems))
                tests.append(test)
                break
            except (ValueError, KeyError, urllib.error.URLError,
                    AnthropicAPIError) as e:
                last_err = e
        else:
            raise GenerationUnavailable(
                f"Anthropic generation failed for idx {rec['index']} "
                f"({rec['label']!r}): {last_err}"
            )
    return tests


REWRITE_INSTRUCTION = """Rewrite the sentence below in a markedly different register — promotional / advertising-blurb style — while keeping the same content and the same key nouns. One sentence, plain words, similar length.

Sentence: "{text}"

Respond with ONLY the rewritten sentence, no other text."""


def anthropic_rewrite(text):
    """Rewrite one sentence in a different register via the Anthropic API.

    Used by the register_swap mechanism check when no --rewrites-in file
    is supplied. Goes through the same _anthropic_messages plug-in as
    mode (a) generation.
    """
    out = _anthropic_messages(
        REWRITE_INSTRUCTION.format(text=text), max_tokens=256
    ).strip()
    return out or None


def check_key():
    """Self-test for the Anthropic plug-in. Prints no secret material.

    Reports whether ANTHROPIC_API_KEY is available (environment or
    .env; on an interactive terminal the user may paste it when
    prompted); if it is, makes one minimal Messages API call
    (max_tokens=16) with the configured model and reports success or
    failure. Returns a process exit code.
    """
    if not envkeys.require_key(
        "ANTHROPIC_API_KEY",
        what_for="to generate prompts with the Anthropic API",
        where_to_get="console.anthropic.com (API Keys)",
    ):
        print("ANTHROPIC_API_KEY: not set")
        print("Set it either way:")
        print('  export ANTHROPIC_API_KEY="sk-ant-..."')
        print("  or copy .env.example to .env in this folder and paste "
              "the key there.")
        print("API check: skipped (nothing to test)")
        return 1
    print("ANTHROPIC_API_KEY: present")
    model = os.environ.get("CHECKER_MODEL", DEFAULT_MODEL)
    try:
        _anthropic_messages("Reply with the single word: ok", max_tokens=16,
                            timeout=30)
    except (AnthropicAPIError, GenerationUnavailable, ValueError,
            urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"API check: FAILED ({e})")
        return 1
    print(f"API check: success (model {model} responded)")
    return 0


def load_prompts_in(path, labels=None):
    """Mode (b): load externally generated prompts and validate them.

    If `labels` is given, the prompts must cover exactly those features
    (matched by index + source) and inherit layer/source/index/label from
    the labels file when absent.
    """
    with open(path) as f:
        data = json.load(f)
    tests = data["tests"] if isinstance(data, dict) else data
    if labels is not None:
        by_key = {(str(r["index"]), r["source"]): r for r in labels}
        merged = []
        for i, t in enumerate(tests, 1):
            key = (str(t["index"]), t.get("source"))
            rec = by_key.get(key)
            if rec is None and len(labels) == len(tests):
                rec = labels[i - 1]  # positional fallback
            if rec is None:
                raise GenerationUnavailable(
                    f"prompts-in test {t.get('test', i)} (idx {t.get('index')}) "
                    "does not match any label record"
                )
            t = {
                "test": t.get("test", rec.get("test", i)),
                "layer": t.get("layer", rec["layer"]),
                "source": t.get("source", rec["source"]),
                "index": rec["index"],
                "label": t.get("label", rec["label"]),
                "should_fire": t["should_fire"],
                "near_miss": t["near_miss"],
                "predicted": t["predicted"],
                "basis": t["basis"],
            }
            merged.append(t)
        tests = merged
    bad = validate_tests(tests)
    if bad:
        detail = "; ".join(f"test {k}: {', '.join(v)}" for k, v in bad.items())
        raise GenerationUnavailable(f"prompts-in failed validation: {detail}")
    return tests


def generate(labels, prompts_in=None):
    """Dispatch on the available generation mode."""
    if prompts_in:
        return load_prompts_in(prompts_in, labels)
    if envkeys.require_key(
        "ANTHROPIC_API_KEY",
        what_for="to generate prompts with the Anthropic API",
        where_to_get="console.anthropic.com (API Keys)",
    ):
        return generate_via_anthropic(labels)
    raise GenerationUnavailable(
        "No prompt-generation mode available. Either supply "
        "ANTHROPIC_API_KEY for standalone generation (export it, or "
        "copy .env.example to .env in this folder and paste the key "
        "there; + optional CHECKER_MODEL), or pass --prompts-in <file> "
        "with externally generated prompts in the scaleup-prompts schema."
    )


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Generate checker prompts for a labels file.")
    ap.add_argument("--labels", default=None, help="labels JSON: [{layer, source, index, label}]")
    ap.add_argument("--prompts-in", default=None)
    ap.add_argument("--out", default=None, help="write tests JSON here")
    ap.add_argument("--check-key", action="store_true",
                    help="report whether ANTHROPIC_API_KEY is set and, if so, "
                         "verify it with one minimal API call; prints no key material")
    args = ap.parse_args()
    if args.check_key:
        sys.exit(check_key())
    if not args.labels:
        ap.error("--labels is required unless --check-key is given")
    with open(args.labels) as f:
        labels = json.load(f)
    if isinstance(labels, dict):
        labels = labels.get("tests") or labels.get("labels")
    try:
        tests = generate(labels, args.prompts_in)
    except GenerationUnavailable as e:
        print(f"generate: {e}", file=sys.stderr)
        sys.exit(2)
    out = {"tests": tests}
    if args.out:
        with open(args.out, "w") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        print(f"wrote {len(tests)} tests to {args.out}")
    else:
        print(json.dumps(out, indent=2, ensure_ascii=False))
