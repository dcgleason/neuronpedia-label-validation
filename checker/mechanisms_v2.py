#!/usr/bin/env python3
"""Failure-mechanism checks for the Neuronpedia label checker — v2.

Each failed label gets probed for WHY it failed, following the method of
the Nov 12 silent-feature failure analyses: one variable changed at a time.

Checks:
  theme_count   - what fraction of the feature's stored (positive)
                  examples are actually on the label's topic? Reads the
                  public feature API; no key, no scoring.
  keyword_test  - (i) ablation: delete the label's content words from
                  the should-fire sentences and rescore; (ii) word-alone:
                  score the label's content words on their own.
  mining        - surface-form mining (new in v2): find tokens that
                  dominate the feature's own stored positive examples
                  and probe those the label never mentions.
  register_swap - rewrite a should-fire sentence in a clearly different
                  register (via the caller's rewrite_fn) and rescore;
                  v2 adds a fixed recommendation-register template probe
                  that needs no rewrite function at all.
  length_test   - embed a should-fire sentence inside a long document
                  and rescore: (a) a long neutral document, (b) a
                  topical document built from the feature's own stored
                  examples (both new / changed in v2).

classify() maps the evidence to one of: word-form, register,
displaced-theme, document-bound, unresolved. "unresolved" is a
legitimate result: 3 of the 17 manually analyzed silent features earned it,
and in v2 it is the DEFAULT when nothing fired.

What changed in v2 (v1 is preserved verbatim in mechanisms_v1.py):
Calibration of v1 against the 17 manually analyzed silent features scored
2/17 on mechanism tags. The dominant failure was over-tagging
"displaced-theme": v1's theme_count matched label words literally, and
the stored examples almost never contain the label's own phrasing, so
nearly every feature looked "off-theme" and fell into the catch-all at
the end of the decision table. v2 therefore:
  1. TOPICAL theme count: an example counts as on-theme when it
     contains a label content word OR a morphological variant of one
     (suffix-stemmed matching, plus prefix match for stems >= 5 chars).
  2. SURFACE-FORM MINING: tokens dominating the stored positive
     examples (code tokens, 2-letter tokens, non-Latin runs included)
     are probed directly; firing on a token the label never names is
     word-form evidence the label-word probes cannot produce.
  3. LENGTH TEST v2: the topical-document variant catches features
     bound to a kind of document, not just document length.
  4. REGISTER v2: a fixed recommendation-register template probe runs
     even when no rewrite function is available.
  5. DECISION ORDER v2: displaced-theme now requires POSITIVE evidence
     (a topical-theme fraction in [0.10, 0.60) AND some probe firing on
     off-label material). Nothing firing anywhere -> unresolved.
"""
import json
import os
import re
import urllib.request
from collections import Counter

BASE_URL = "https://www.neuronpedia.org/api/feature/gemma-2-2b"
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

# --- Thresholds (named constants; tuned to the pilot failure analyses, Nov 12) ---
# A should-fire max below this counts as the feature staying silent.
SILENT_EPS = 0.5
# v2: a probe at or above this counts as CLEARLY fired. The v2 checks
# (mining, length, register) and the displaced-theme evidence test all
# use this one bar, matching the firing levels the manual failure analyses
# treated as real (weak traces of 3-8 in long documents aside).
MIN_FIRE = 4.0
# Ablation: if removing the label's content words drops the should-fire
# max to <= this fraction of the original (and the original actually
# fired), the key words themselves were carrying the activation.
ABLATION_KILL_RATIO = 0.25
MIN_FIRE_FOR_ABLATION = 2.0
# Word-alone: a bare content word scoring at least this fraction of the
# feature's stored max activation means the feature tracks the word.
WORD_ALONE_FRAC = 0.25
# Theme (v2): the label names a minority-but-present theme of the
# feature's actual examples when the topical fraction lands in
# [THEME_DISPLACED_MIN, THEME_DISPLACED_MAX). Below the band the label's
# topic is essentially absent; at or above it, the topic is the center
# of mass and something else explains the failure.
THEME_DISPLACED_MIN = 0.10
THEME_DISPLACED_MAX = 0.60
# Mining (v2): a token is "dominant" when it appears in at least this
# fraction of the stored positive examples; at most MINED_MAX_TOKENS
# dominant tokens not covered by the label get probed per feature.
MINED_DOMINANCE = 0.40
MINED_MAX_TOKENS = 3

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

# Mining stoplist: common English function words. A token in this list
# is never treated as a mined surface form, however dominant it is in
# the examples — function words dominate nearly all English text, so
# their dominance carries no information about the feature. (Known
# cost: a feature whose real trigger IS a function word — the pilot's
# idx 8743 fired on "or"/"nor" — cannot be caught by mining.)
FUNCTION_WORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "else", "when",
    "while", "of", "at", "by", "for", "with", "about", "against",
    "between", "into", "through", "during", "before", "after", "above",
    "below", "to", "from", "up", "down", "in", "out", "on", "off",
    "over", "under", "again", "further", "once", "here", "there",
    "all", "any", "both", "each", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not", "only", "own", "same", "so",
    "than", "too", "very", "can", "will", "just", "should", "now",
    "i", "me", "my", "we", "our", "you", "your", "he", "him", "his",
    "she", "her", "it", "its", "they", "them", "their", "this", "that",
    "these", "those", "am", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "having", "do", "does", "did",
    "doing", "would", "could", "ought", "as", "who", "whom", "what",
    "which", "where", "why", "how", "also", "one", "two", "first",
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


def _act_value(activation):
    """An example's activation value, whichever field the API used."""
    for field in ("maxActivation", "maxValue"):
        v = activation.get(field)
        if isinstance(v, (int, float)):
            return v
    return None


def _positive_examples(feature):
    """The feature's stored POSITIVE examples.

    The API's example list mixes top examples with a shared
    zero-activation bin; only positives carry information. When the
    examples carry an activation value, positives are value > 0. When
    no example carries a value at all, fall back to the first portion
    of the list (top examples come first).
    """
    activations = feature.get("activations", [])
    valued = [a for a in activations if _act_value(a) is not None]
    if valued:
        return [a for a in valued if _act_value(a) > 0]
    return activations[: max(1, len(activations) // 2)]


def _example_text(activation):
    return "".join(activation.get("tokens", [])).replace("▁", " ").lower()


def _example_text_raw(activation):
    return "".join(activation.get("tokens", [])).replace("▁", " ")


# ---------------------------------------------------------------------------
# v2 topical theme counting
# ---------------------------------------------------------------------------

def _stem(word):
    """Crude suffix stemmer: -ies -> -y, then strip -ing / -ed / -es / -s.

    Deliberately simple; the >= 5-char prefix match in _token_on_theme
    covers the cases crude stemming mangles (e.g. 'running' -> 'runn').
    """
    w = word.lower()
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 5 and w.endswith("ing"):
        return w[:-3]
    if len(w) > 4 and w.endswith("ed"):
        return w[:-2]
    if len(w) > 3 and w.endswith("es"):
        return w[:-2]
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def _token_on_theme(token, words, stems):
    if token in words:
        return True
    st = _stem(token)
    if st in stems:
        return True
    # Prefix match for stems >= 5 chars: 'genetics' ~ 'genetic',
    # 'button' ~ 'buttons' beyond what the stemmer already merged.
    return any(
        len(s) >= 5 and (token.startswith(s) or st.startswith(s))
        for s in stems
    )


def theme_count(record, feature=None):
    """Fraction of stored positive examples that are on the label's topic.

    v2 (topical): an example counts when it contains a label content
    word OR a morphological variant of one (stem / prefix match), not
    only the label's literal wording as in v1.
    """
    if feature is None:
        feature = fetch_feature(record["source"], record["index"])
    words = content_words(record["label"])
    pool = _positive_examples(feature)
    if not pool or not words:
        return {"status": "unavailable", "fraction": None,
                "n_examples": len(pool), "content_words": words}
    stems = {_stem(w) for w in words}
    hits = 0
    for a in pool:
        tokens = re.findall(r"[a-z']+", _example_text(a))
        if any(_token_on_theme(t, words, stems) for t in tokens):
            hits += 1
    return {"status": "ok", "fraction": hits / len(pool), "hits": hits,
            "n_examples": len(pool), "content_words": words,
            "max_act_approx": feature.get("maxActApprox")}


# ---------------------------------------------------------------------------
# Keyword test (unchanged from v1)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# v2 surface-form mining
# ---------------------------------------------------------------------------

# Word-like tokens (letters/digits/underscore runs — catches code tokens
# like 'btn', 'utf_8', 'mp3' and 2-letter tokens) plus runs of non-Latin
# script (CJK, Cyrillic, Hebrew, Arabic), which tokenize as units here.
_MINE_TOKEN_RE = re.compile(
    r"[a-z0-9]+(?:_[a-z0-9]+)*"
    r"|[\u0590-\u05ff\u0600-\u06ff\u0400-\u04ff\u3040-\u30ff"
    r"\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]+"
)


def _mine_tokens(text):
    return _MINE_TOKEN_RE.findall(text)


def _covered_by_label(token, words, stems):
    """Is this token already named (or a variant of a word named) by
    the label? Then it is not new surface-form evidence."""
    if token in words or _stem(token) in stems:
        return True
    return any(len(s) >= 5 and token.startswith(s) for s in stems)


def _is_short_or_code(token):
    return (
        len(token) <= 4
        or "_" in token
        or any(c.isdigit() for c in token)
        or not token.isascii()
    )


def surface_mining(record, test, score_fn, feature=None):
    """Mine the feature's stored positive examples for dominant tokens
    the label never mentions, and probe them.

    A token is dominant when it appears in >= MINED_DOMINANCE of the
    positive examples. For each of up to MINED_MAX_TOKENS dominant
    tokens not covered by the label's content words, probe:
      - the token in a minimal carrier sentence, and
      - the bare token as the whole text, when it is short/code-like.
    A probe >= MIN_FIRE is word-form evidence (classify() additionally
    requires that the label-word probes did not already explain it).
    """
    if feature is None:
        feature = fetch_feature(record["source"], record["index"])
    positives = _positive_examples(feature)
    if not positives:
        return {"status": "unavailable", "reason": "no stored examples",
                "mined_max": None}
    counts = Counter()
    for a in positives:
        for tok in set(_mine_tokens(_example_text(a))):
            if tok in FUNCTION_WORDS:
                continue
            # Latin/code tokens need >= 2 chars (1-char ones are noise);
            # a non-Latin run of any length can be a real surface form.
            if len(tok) >= 2 or not tok.isascii():
                counts[tok] += 1
    words = content_words(record["label"])
    stems = {_stem(w) for w in words}
    dominant = []
    for tok, n in counts.most_common():
        if n / len(positives) < MINED_DOMINANCE:
            break
        if _covered_by_label(tok, words, stems):
            continue
        dominant.append(tok)
        if len(dominant) >= MINED_MAX_TOKENS:
            break
    probes = {}
    mined_max = None
    for tok in dominant:
        entry = {"carrier": score_fn(
            record["source"], record["index"], f"The text mentions {tok}."
        )}
        if _is_short_or_code(tok):
            entry["bare"] = score_fn(record["source"], record["index"], tok)
        probes[tok] = entry
        for v in entry.values():
            mined_max = v if mined_max is None else max(mined_max, v)
    return {"status": "ok", "n_positive_examples": len(positives),
            "dominant_tokens": dominant, "probes": probes,
            "mined_max": mined_max}


# ---------------------------------------------------------------------------
# Register check v2: supplied rewrites + fixed template probe
# ---------------------------------------------------------------------------

REGISTER_TEMPLATE = (
    "If you enjoyed {topic} before, this is the one everyone is "
    "talking about, and fans of {topic} will not want to miss it."
)


def register_swap(record, test, score_fn, rewrite_fn=None):
    """Register evidence from two probe kinds:
      - rewrite probes: should-fire sentences rewritten in a different
        register via the caller's rewrite_fn (v1 behavior; skipped
        when no function is supplied);
      - template probe (v2): a fixed recommendation-register sentence
        built from the label's top content word. Recommendation /
        promotional register is the register the manual failure analyses kept
        finding (e.g. the 'literary works' feature firing on
        'will appeal to fans of...' text), and this probe needs no
        rewrite function, so the check runs standalone.
    Result carries swapped_max (rewrites), template_max, and probe_max
    (the max over both kinds).
    """
    result = {"status": "unavailable", "scores": [], "swapped_max": None,
              "template_text": None, "template_max": None,
              "probe_max": None}
    scores = []
    if rewrite_fn is not None:
        for s in test["should_fire"]:
            rewritten = rewrite_fn(s)
            if rewritten and rewritten != s:
                scores.append(
                    score_fn(record["source"], record["index"], rewritten)
                )
    result["scores"] = scores
    result["swapped_max"] = max(scores) if scores else None
    words = content_words(record["label"])
    if words:
        template_text = REGISTER_TEMPLATE.format(topic=words[0])
        result["template_text"] = template_text
        result["template_max"] = score_fn(
            record["source"], record["index"], template_text
        )
    probes = [v for v in (result["swapped_max"], result["template_max"])
              if v is not None]
    if probes:
        result["status"] = "ok"
        result["probe_max"] = max(probes)
    return result


# ---------------------------------------------------------------------------
# Length test v2: neutral document + topical document
# ---------------------------------------------------------------------------

LONG_DOCUMENT = """The facilities committee met on Tuesday morning to review the quarterly maintenance schedule for the library building. Attendance was taken and the minutes from the previous session were approved without amendment. The first item concerned the roof inspection, which had been postponed twice because of weather. A contractor had submitted a revised estimate, and the committee agreed to compare it with the two earlier bids before making any decision. The second item was the heating system. The building manager reported that the boiler had been serviced in October and that no major faults were found, although a valve on the second floor was scheduled for replacement before the end of the year.

Attention then turned to the reading rooms. Several chairs had been sent out for repair, and the replacement fabric samples were passed around the table. One member suggested that the study carrels near the windows should be moved to reduce glare in the afternoon, and the group agreed to trial the arrangement for a month. The discussion continued with an update on the book returns process. A new set of labels for the shelving had arrived, and staff would begin applying them the following week, starting with the reference section on the ground floor.

The treasurer presented the monthly accounts. Spending on utilities was slightly below forecast, while the cost of cleaning supplies had risen for the third month in a row. The committee noted both figures and moved on. A proposal to extend the opening hours on Saturdays was discussed at some length. Supporters argued that demand from students justified the change, while others raised concerns about staffing. No vote was taken, and the item was deferred to the next meeting so that a rota could be drafted and costed.

After a short break, the committee reviewed the events calendar for the coming season. A local history talk was confirmed for the first Thursday of next month, and a children's reading morning was planned for the school holidays. The notice boards would be updated once the dates were final. The final item was the annual review of the emergency procedures. The assembly points remain unchanged, the alarm test will continue to take place on the first Monday of each month, and new staff will receive the standard briefing during their induction week. The meeting closed with agreement on the date of the next session, and the chair thanked everyone for attending before the room was cleared and the lights were switched off."""

# The v1 neutral document (~450 words) is the filler; v2 repeats it to
# reach the ~700-900 word range the manual failure analyses found necessary.
FILLER_TEXT = LONG_DOCUMENT
NEUTRAL_TARGET_WORDS = 820
TOPICAL_MAX_WORDS = 900


def _embed_in_words(words, sentence):
    mid = len(words) // 2
    return " ".join(words[:mid]) + " " + sentence + " " + " ".join(words[mid:])


def _long_neutral_document(sentence):
    filler_words = FILLER_TEXT.split()
    reps = []
    total = 0
    while total < NEUTRAL_TARGET_WORDS:
        reps.append(FILLER_TEXT)
        total += len(filler_words)
    return _embed_in_words(" ".join(reps).split(), sentence)


def _topical_document(record, sentence, feature):
    """The feature's own stored positive examples, concatenated and
    truncated to ~TOPICAL_MAX_WORDS words, with the sentence embedded
    in the middle. Word count approximates token count."""
    parts = []
    total = 0
    for a in _positive_examples(feature):
        text = _example_text_raw(a).strip()
        if not text:
            continue
        parts.append(text)
        total += len(text.split())
        if total >= TOPICAL_MAX_WORDS:
            break
    words = " ".join(parts).split()[:TOPICAL_MAX_WORDS]
    if not words:
        return None
    return _embed_in_words(words, sentence)


def length_test(record, test, score_fn, feature=None):
    """Rescore should_fire[0] embedded in long documents (v2).

    (a) neutral: a long generic document (~700-900 words of filler);
    (b) topical: a document built from the feature's own stored
    positive examples (~900 words). Firing >= MIN_FIRE on either,
    while the plain sentence did not fire, is document-bound evidence:
    the feature needs document-length context, or a document of a
    particular kind, before it responds.
    """
    if feature is None:
        feature = fetch_feature(record["source"], record["index"])
    sentence = test["should_fire"][0]
    neutral = _long_neutral_document(sentence)
    neutral_score = score_fn(record["source"], record["index"], neutral)
    result = {"status": "ok", "neutral_max": neutral_score,
              "topical_max": None, "scores": {"neutral": neutral_score},
              "neutral_doc_words": len(neutral.split())}
    topical = _topical_document(record, sentence, feature)
    if topical is not None:
        topical_score = score_fn(record["source"], record["index"], topical)
        result["topical_max"] = topical_score
        result["scores"]["topical"] = topical_score
        result["topical_doc_words"] = len(topical.split())
    result["embedded_max"] = max(
        v for v in (neutral_score, result["topical_max"]) if v is not None
    )
    return result


# ---------------------------------------------------------------------------
# Decision table v2
# ---------------------------------------------------------------------------

def classify(record, scores, mech):
    """Decision table v2: evidence -> mechanism tag.

    Order: word-form (keyword ablation / word-alone, as v1, OR mined
    surface-form evidence) -> document-bound (length v2) -> register
    (v2 probes) -> displaced-theme, ONLY with positive evidence ->
    unresolved, the default when nothing fired. `scores` is
    {sf1, sf2, nm1, nm2}; `mech` holds the check results keyed by
    check name.
    """
    sf_max = max(scores["sf1"], scores["sf2"])
    nm_max = max(scores["nm1"], scores["nm2"])
    kw = mech.get("keyword") or {}
    alone = None
    if kw.get("status") == "ok":
        alone = kw.get("word_alone_max")
        ablated = kw.get("ablated_max")
        if (ablated is not None and sf_max >= MIN_FIRE_FOR_ABLATION
                and ablated <= ABLATION_KILL_RATIO * sf_max):
            return "word-form"
    feature_max = (mech.get("theme") or {}).get("max_act_approx")
    if alone is not None and feature_max:
        if alone >= WORD_ALONE_FRAC * feature_max and alone > SILENT_EPS:
            return "word-form"
    mining = mech.get("mining") or {}
    mined_max = mining.get("mined_max")
    if (mining.get("status") == "ok" and mined_max is not None
            and mined_max >= MIN_FIRE
            and (alone is None or alone < MIN_FIRE)):
        return "word-form"
    lt = mech.get("length") or {}
    if (lt.get("status") == "ok" and lt.get("embedded_max") is not None
            and lt["embedded_max"] >= MIN_FIRE and sf_max < MIN_FIRE):
        return "document-bound"
    rs = mech.get("register") or {}
    if (rs.get("status") == "ok" and rs.get("probe_max") is not None
            and rs["probe_max"] >= MIN_FIRE and sf_max < MIN_FIRE):
        return "register"
    th = mech.get("theme") or {}
    # Positive evidence for displaced-theme: the label's topic is
    # present in the stored examples but is a minority theme, AND
    # something fired on off-label material — a near-miss (off-label
    # by construction) or any probe that matched no class above.
    probe_maxima = [mined_max, rs.get("probe_max"), lt.get("embedded_max")]
    off_label_fire = nm_max >= MIN_FIRE or any(
        v is not None and v >= MIN_FIRE for v in probe_maxima
    )
    if (th.get("status") == "ok" and th.get("fraction") is not None
            and THEME_DISPLACED_MIN <= th["fraction"] < THEME_DISPLACED_MAX
            and off_label_fire):
        return "displaced-theme"
    return "unresolved"


def _safe_score_fn(score_fn):
    """Wrap score_fn so a failed probe can never kill a run.

    The activation endpoint returned HTTP 500 on a very long text
    (Nov 13, the v2 length test's ~850-word neutral document) and the
    raw error crashed the calibration run. On any exception, retry
    once with the text halved by word count; on a second failure
    return 0.0, which reads as "no firing evidence" — the
    conservative direction for mechanism classification. Failures are
    counted on the wrapper's state for reporting.
    """
    state = {"errors": 0}

    def safe(source, index, text):
        try:
            return score_fn(source, index, text)
        except Exception:
            words = text.split()
            if len(words) > 40:
                try:
                    return score_fn(
                        source, index, " ".join(words[: len(words) // 2])
                    )
                except Exception:
                    pass
            state["errors"] += 1
            return 0.0

    safe.state = state
    return safe


def run_all(record, test, score_fn, rewrite_fn=None):
    """Run every check for one failed test and classify it."""
    safe = _safe_score_fn(score_fn)
    feature = fetch_feature(record["source"], record["index"])
    mech = {"theme": theme_count(record, feature=feature)}
    mech["keyword"] = keyword_test(record, test, safe)
    mech["mining"] = surface_mining(record, test, safe, feature=feature)
    mech["length"] = length_test(record, test, safe, feature=feature)
    mech["register"] = register_swap(record, test, safe, rewrite_fn)
    mech["probe_errors"] = safe.state["errors"]
    return mech
