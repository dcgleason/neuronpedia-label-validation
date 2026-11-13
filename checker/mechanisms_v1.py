#!/usr/bin/env python3
"""Failure-mechanism checks for the Neuronpedia label checker.

Each failed label gets probed for WHY it failed, following the method of
the Nov 12 silent-feature autopsies: one variable changed at a time.

Checks:
  theme_count   - what fraction of the feature's stored (positive)
                  examples actually contain the label's content words?
                  Reads the public feature API; no key, no scoring.
  keyword_test  - (i) ablation: delete the label's content words from
                  the should-fire sentences and rescore; (ii) word-alone:
                  score the label's content words on their own.
  register_swap - rewrite a should-fire sentence in a clearly different
                  register (via the caller's rewrite_fn) and rescore.
  length_test   - embed a should-fire sentence inside a fixed long
                  neutral document (~450 words) and rescore.

classify() maps the evidence to one of: word-form, register,
displaced-theme, document-bound, unresolved. "unresolved" is a
legitimate result: 3 of the 17 hand-autopsied silent features earned it.
"""
import json
import os
import re
import urllib.request

BASE_URL = "https://www.neuronpedia.org/api/feature/gemma-2-2b"
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

# --- Thresholds (named constants; tuned to the pilot autopsies, Nov 12) ---
# A should-fire max below this counts as the feature staying silent.
SILENT_EPS = 0.5
# Ablation: if removing the label's content words drops the should-fire
# max to <= this fraction of the original (and the original actually
# fired), the key words themselves were carrying the activation.
ABLATION_KILL_RATIO = 0.25
MIN_FIRE_FOR_ABLATION = 2.0
# Word-alone: a bare content word scoring at least this fraction of the
# feature's stored max activation means the feature tracks the word.
WORD_ALONE_FRAC = 0.25
# Length: the sentence embedded in a long document fires at >= this
# fraction of the stored max (and at least LENGTH_MIN_ABS) while the
# bare sentence is silent -> the feature needs document context.
LENGTH_FRAC = 0.15
LENGTH_MIN_ABS = 3.0
# Register: the register-swapped sentence fires at >= REGISTER_MIN_ABS
# and at least REGISTER_RATIO x the original should-fire max (or the
# original was silent) -> the feature tracks a register, not the topic.
REGISTER_MIN_ABS = 5.0
REGISTER_RATIO = 5.0
# Theme: if fewer than this fraction of stored positive examples contain
# any label content word, the label names a minority theme of the
# feature's actual examples (displaced center of mass).
THEME_DISPLACED_MAX = 0.5

STOPWORDS = {
    "a", "an", "the", "of", "to", "in", "on", "for", "and", "or", "with",
    "without", "related", "references", "reference", "terms", "term",
    "words", "word", "phrases", "phrase", "mentions", "mention",
    "instances", "instance", "occurrences", "occurrence", "related",
    "associated", "specific", "various", "different", "certain",
    "indicating", "indicates", "describing", "describes", "containing",
    "contains", "involving", "involves", "featuring", "features",
    "elements", "element", "concepts", "concept", "topics", "topic",
    "themes", "theme", "subjects", "subject", "expressions",
    "expression", "statements", "statement", "descriptions",
}


def content_words(label):
    """The label's key content words: quoted words always count (a label
    like 'occurrences of the word "with"' names its trigger); otherwise
    lowercase alpha tokens minus stopwords, length >= 3."""
    words = []
    for m in re.findall(r'"([^"]+)"', label):
        for w in re.findall(r"[a-z']+", m.lower()):
            if w not in words:
                words.append(w)
    for w in re.findall(r"[a-z']+", label.lower()):
        if len(w) >= 3 and w not in STOPWORDS and w not in words:
            words.append(w)
    return words


def fetch_feature(source, index, cache_dir=CACHE_DIR):
    """Public GET of one feature (no key). Cached on disk."""
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, f"feature__{source}__{index}.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    url = f"{BASE_URL}/{source}/{index}"
    with urllib.request.urlopen(url, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
    with open(path, "w") as f:
        json.dump(data, f)
    return data


def _example_text(activation):
    return "".join(activation.get("tokens", [])).replace("▁", " ").lower()


def theme_count(record, feature=None):
    """Fraction of stored positive examples containing a content word."""
    if feature is None:
        feature = fetch_feature(record["source"], record["index"])
    words = content_words(record["label"])
    activations = feature.get("activations", [])
    positives = [a for a in activations if (a.get("maxValue") or 0) > 0]
    pool = positives or activations
    if not pool or not words:
        return {"status": "unavailable", "fraction": None,
                "n_examples": len(pool), "content_words": words}
    pattern = re.compile(r"\b(" + "|".join(re.escape(w) for w in words) + r")")
    hits = sum(1 for a in pool if pattern.search(_example_text(a)))
    return {"status": "ok", "fraction": hits / len(pool), "hits": hits,
            "n_examples": len(pool), "content_words": words,
            "max_act_approx": feature.get("maxActApprox")}


def _remove_words(text, words):
    out = text
    for w in words:
        out = re.sub(r"\b" + re.escape(w) + r"\b", "", out, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", out).strip(" ,;")


def keyword_test(record, test, score_fn):
    """Ablation + word-alone probes for the label's content words."""
    words = content_words(record["label"])
    sf = test["should_fire"]
    sf_max = max(
        score_fn(record["source"], record["index"], s) for s in sf
    )
    result = {"status": "ok", "content_words": words, "sf_max": sf_max}
    ablated_scores = []
    for s in sf:
        ablated = _remove_words(s, words)
        if ablated and ablated.lower() != s.lower():
            ablated_scores.append(
                score_fn(record["source"], record["index"], ablated)
            )
    result["ablated_max"] = max(ablated_scores) if ablated_scores else None
    alone = {}
    for w in words[:3]:
        alone[w] = score_fn(record["source"], record["index"], w)
    result["word_alone"] = alone
    result["word_alone_max"] = max(alone.values()) if alone else None
    return result


def register_swap(record, test, score_fn, rewrite_fn=None):
    """Rescore should-fire sentences rewritten in a different register."""
    if rewrite_fn is None:
        return {"status": "skipped",
                "reason": "no rewrite function supplied"}
    scores = []
    for s in test["should_fire"]:
        rewritten = rewrite_fn(s)
        if rewritten and rewritten != s:
            scores.append(
                score_fn(record["source"], record["index"], rewritten)
            )
    if not scores:
        return {"status": "unavailable"}
    return {"status": "ok", "swapped_max": max(scores), "scores": scores}


LONG_DOCUMENT = """The facilities committee met on Tuesday morning to review the quarterly maintenance schedule for the library building. Attendance was taken and the minutes from the previous session were approved without amendment. The first item concerned the roof inspection, which had been postponed twice because of weather. A contractor had submitted a revised estimate, and the committee agreed to compare it with the two earlier bids before making any decision. The second item was the heating system. The building manager reported that the boiler had been serviced in October and that no major faults were found, although a valve on the second floor was scheduled for replacement before the end of the year.

Attention then turned to the reading rooms. Several chairs had been sent out for repair, and the replacement fabric samples were passed around the table. One member suggested that the study carrels near the windows should be moved to reduce glare in the afternoon, and the group agreed to trial the arrangement for a month. {sentence} The discussion continued with an update on the book returns process. A new set of labels for the shelving had arrived, and staff would begin applying them the following week, starting with the reference section on the ground floor.

The treasurer presented the monthly accounts. Spending on utilities was slightly below forecast, while the cost of cleaning supplies had risen for the third month in a row. The committee noted both figures and moved on. A proposal to extend the opening hours on Saturdays was discussed at some length. Supporters argued that demand from students justified the change, while others raised concerns about staffing. No vote was taken, and the item was deferred to the next meeting so that a rota could be drafted and costed.

After a short break, the committee reviewed the events calendar for the coming season. A local history talk was confirmed for the first Thursday of next month, and a children's reading morning was planned for the school holidays. The notice boards would be updated once the dates were final. The final item was the annual review of the emergency procedures. The assembly points remain unchanged, the alarm test will continue to take place on the first Monday of each month, and new staff will receive the standard briefing during their induction week. The meeting closed with agreement on the date of the next session, and the chair thanked everyone for attending before the room was cleared and the lights were switched off."""


def length_test(record, test, score_fn):
    """Rescore should-fire sentences embedded in a long neutral document."""
    scores = []
    for s in test["should_fire"]:
        embedded = LONG_DOCUMENT.format(sentence=s)
        scores.append(score_fn(record["source"], record["index"], embedded))
    return {"status": "ok", "embedded_max": max(scores), "scores": scores,
            "doc_words": len(LONG_DOCUMENT.split())}


def classify(record, scores, mech):
    """Decision table: evidence -> mechanism tag.

    Order matters: direct firing evidence (ablation, word-alone,
    length, register) beats the indirect theme count, which beats
    giving up. `scores` is {sf1, sf2, nm1, nm2}; `mech` holds the
    check results keyed by check name.
    """
    sf_max = max(scores["sf1"], scores["sf2"])
    kw = mech.get("keyword") or {}
    if kw.get("status") == "ok":
        ablated = kw.get("ablated_max")
        if (ablated is not None and sf_max >= MIN_FIRE_FOR_ABLATION
                and ablated <= ABLATION_KILL_RATIO * sf_max):
            return "word-form"
    feature_max = (mech.get("theme") or {}).get("max_act_approx")
    if kw.get("status") == "ok" and kw.get("word_alone_max") is not None:
        alone = kw["word_alone_max"]
        if feature_max and alone >= WORD_ALONE_FRAC * feature_max and alone > SILENT_EPS:
            return "word-form"
    lt = mech.get("length") or {}
    if lt.get("status") == "ok" and sf_max <= SILENT_EPS:
        emb = lt["embedded_max"]
        if emb >= LENGTH_MIN_ABS and (
            not feature_max or emb >= LENGTH_FRAC * feature_max
        ):
            return "document-bound"
    rs = mech.get("register") or {}
    if rs.get("status") == "ok":
        swapped = rs["swapped_max"]
        if swapped >= REGISTER_MIN_ABS and (
            sf_max <= SILENT_EPS or swapped >= REGISTER_RATIO * sf_max
        ):
            return "register"
    th = mech.get("theme") or {}
    if th.get("status") == "ok" and th.get("fraction") is not None:
        if th["fraction"] < THEME_DISPLACED_MAX:
            return "displaced-theme"
    return "unresolved"


def run_all(record, test, score_fn, rewrite_fn=None):
    """Run every check for one failed test and classify it."""
    mech = {"theme": theme_count(record)}
    mech["keyword"] = keyword_test(record, test, score_fn)
    mech["length"] = length_test(record, test, score_fn)
    mech["register"] = register_swap(record, test, score_fn, rewrite_fn)
    return mech
