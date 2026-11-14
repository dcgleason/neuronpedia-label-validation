# Explainer swap — results (November 14, 2026)

**Headline: the Sonnet labels passed 28 of 40 (70.0%), against the GPT-4o-mini baseline of 12 of 40 (30.0%) on the same 40 features.** Swapping in a stronger explainer, shown the same kind of evidence, more than doubled the pass rate. All three locked arm-level predictions were supported, and the falsifier was not triggered.

- **Run:** scored Saturday, November 14, 2026, after the lock was public (GitHub commit `08f7b23763df74bdc7bbd4de5a123f1dff61e776`).
- **Instrument:** `checker/score.py` Scorer against the Neuronpedia activation API, source `12-gemmascope-res-16k` (Gemma-2-2B, layer 12). Pass rule: min(should-fire) > max(near-miss).
- **Calls:** 160 API calls, 0 cache hits, no rate-limit events.
- **Integrity:** locked predictions file SHA-256 verified before scoring and re-verified after, unchanged: `dad4b6e336d354e51a580563e29a4f7b75332678e54b09f7f416e44b333906f7`. Two independent parses of the locked file agreed on all 40 tests (idx, labels, 4 prompts, prediction) before any API call.
- **Raw data:** `explainer-swap/explainer-swap-results-raw.json`.

## Arm-level predictions — verdicts

1. **Sonnet labels pass at least 16 of 40 — SUPPORTED.** Actual: 28/40. The result also cleared the 22 passes the per-label calls summed to, the first arm in this study where the outcome beat the per-label sum instead of falling short of it.
2. **At least 8 of the 28 pilot failures flip to pass — SUPPORTED.** Actual: 17 of 28 flipped (18, 869, 1029, 1643, 3349, 3580, 5072, 5158, 6865, 8630, 8743, 11270, 12608, 14719, 15035, 15623, 16358). The improvement came from flips, as predicted, not from the already-passing labels.
3. **At least 9 of the 12 pilot passes hold — SUPPORTED.** Actual: 11 of 12 held. The single loss was idx 4207 ("cool"): its temperature-sense near-miss ("The cool evening air came in through the open window") fired 41.25, above both should-fires — the exact designed risk named in its locked test. The two risks the locked file named instead, idx 483 and idx 15337, both held (483 passed at +23.69 despite being predicted to fail).
4. **Falsifier (≤13/40 kills the claim) — NOT TRIGGERED.** At 28/40, the result sits far from the falsifier. On the locked file's secondary reading: the flips were not almost all word-form relabels — word-form and construction flips are there (1643, 5158, 8743, 14719, 15623), but register and fixed-formula relabels flipped too (3580, 8630, 11270), and several broader labels passed outright (869, 1029, 12608, 16358). The broader claim survives: explainer quality is a major factor in the pilot's label failures, with the design's standing caveat that the swap changed the explainer model, the example presentation, and one light instruction together, so the win belongs to the combination, not to model quality isolated.

## The three blind re-derivations

The locked draft flagged three features where Sonnet, shown only the stored examples, independently reproduced the pilot hand autopsy's findings. All three new labels PASSED:

- **idx 5158** — margin +43.00: the flagship case. The new label (Bootstrap "btn" CSS class names) scored SF 43.00 / 44.75 against NM 0.00 / 0.00, the second-largest margin in the run.
- **idx 14719** — margin +31.38: the word "color" as a token. SF 41.50 / 43.50; a near-miss with a code context but no token fired 10.12, well below both should-fires.
- **idx 8743** — margin +7.94: nor/or coordination extending a negation. SF 24.12 / 7.94 against silent near-misses; the weakest of the three margins.

## Prediction accuracy

Per-label predictions: **28/40 correct (70.0%)** against the locked 22 PASS / 18 FAIL calls.
- Of 22 predicted passes, 19 passed. The 3 misses: idx 2580 (−3.75; a comparison-phrase near-miss beat the weaker should-fire), idx 4207 (−4.75; the lost hold above), and idx 7223 (−1.75; both should-fires fired 46.50, but the mid-sentence "overall" near-miss fired 48.25 — the label's sentence-initial position claim failed by a hair).
- Of 18 predicted fails, only 9 failed. The 9 misses were all predicted-fail labels that passed — concentrated in the register and document labels the draft expected to stay silent or unfocused (idx 1029, 3349, 5072, 6865, 8630, 15035, 15337, 15623) plus idx 483. The draft's pessimism about sentence-scale prompts for register features, calibrated on the pilot, overshot: several of these features fired strongly on two-sentence prompts.

## Failure breakdown (12 failures of the new labels)

By the study's three classes (five disjoint shapes in parentheses):

- silent: 6 (silent-all-four 6, both-sf-silent 0)
- partial: 3 (one-sf-silent 1, partial 2)
- near-miss-beat: 3

For comparison, the pilot's 28 failures on these features were 17 silent, 6 partial, 5 near-miss-beat. The swap's failures are fewer and less silent: 6 of the 12 never fired on any prompt (idx 2081, 2625, 3070, 6515, 7196, 14520 — five of them the document-boundary and no-consistent-trigger labels the locked file expected to be untestable or unfocused).

**Test 25 disclosure (idx 7623).** Per the locked file's closing notes, the two should-fire prompts contained a literal `\n` denoting a line break; the run converted both to real newlines before scoring and recorded the conversion in the raw output. With the boundary in place, should-fire 1 fired 3.33 and should-fire 2 stayed at 0.00, near-misses 0.00 — FAIL as predicted (class: partial, one-sf-silent). The boundary-shaped prompt moved the feature off zero on one prompt, but nowhere near a pass.

## Per-test results

| Test | Idx | New Sonnet label | SF1 | SF2 | NM1 | NM2 | Margin | Verdict | Predicted | Pilot |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 18 | Second or later conjuncts in multi-word proper names and category titles, after "and" or a comma | 7.38 | 23.38 | 0.00 | 0.00 | +7.38 | PASS | PASS | FAIL (silent) |
| 2 | 483 | The word "Windows" (and related XAML tokens) in Microsoft/.NET namespaces, such as System.Windows | 36.75 | 33.25 | 9.56 | 0.00 | +23.69 | PASS | FAIL | PASS |
| 3 | 869 | Names of administrative regions, especially provinces (Iran, China, Kenya, Pakistan) | 23.50 | 20.62 | 0.00 | 3.20 | +17.42 | PASS | PASS | FAIL (partial) |
| 4 | 1029 | Fragments of proper names and terms in a specific fictional context: Sanguosha AI Lua code (Three Kingdoms characters and skills like Tianxiang, Jianxiong, Yiji, Ruthless) and machine-translated Chinese web novel text (character names and cultivation terms). | 20.25 | 12.19 | 0.00 | 0.00 | +12.19 | PASS | FAIL | FAIL (silent) |
| 5 | 1302 | Mid-sentence words in e-commerce shipping, delivery, and order policy boilerplate | 7.41 | 7.66 | 0.00 | 4.81 | +2.59 | PASS | PASS | PASS |
| 6 | 1501 | Celebrations, gifts, and surprises for special occasions (birthdays, anniversaries, holidays) | 15.31 | 47.00 | 0.00 | 47.00 | -31.69 | FAIL | FAIL | FAIL (near-miss beat a should-fire) |
| 7 | 1643 | The word "light" (and its variants like "lightness" and "daylight") in its various senses, such as color shade, illumination, or low weight. | 39.75 | 41.25 | 0.00 | 0.00 | +39.75 | PASS | PASS | FAIL (near-miss beat a should-fire) |
| 8 | 1657 | The first name "Tom" (and names starting with it, like Tom Petty or Tom Mitchell) in running text | 20.25 | 21.75 | 0.00 | 0.00 | +20.25 | PASS | PASS | PASS |
| 9 | 2081 | Document-boundary <bos> tokens that start a new, unrelated text in concatenated corpus text | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | FAIL | FAIL (silent) |
| 10 | 2580 | Comparisons to other works or artists: "meets", "in the style of", "similar to", "likens to" | 40.00 | 10.44 | 14.19 | 0.00 | -3.75 | FAIL | PASS | FAIL (silent) |
| 11 | 2625 | Beginning-of-document token after a concatenated document, especially following code or technical text | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | FAIL | FAIL (silent) |
| 12 | 3070 | Scattered mid-phrase tokens inside multiword noun phrases or names, with no single clear theme. | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | FAIL | FAIL (silent) |
| 13 | 3349 | Punctuation and separators after short bullet-point headings in list-style advice text | 17.38 | 8.62 | 0.00 | 0.00 | +8.62 | PASS | FAIL | FAIL (silent) |
| 14 | 3580 | Document-boundary tokens and formulaic obituary connective phrases | 24.62 | 35.50 | 8.12 | 8.25 | +16.38 | PASS | PASS | FAIL (silent) |
| 15 | 3592 | Function words and connective tokens inside news-style music concert and ticket announcements | 28.38 | 34.00 | 7.53 | 0.00 | +20.84 | PASS | PASS | PASS |
| 16 | 4207 | The informal adjective "cool" meaning trendy or neat, along with adjacent casual words | 36.50 | 37.75 | 0.00 | 41.25 | -4.75 | FAIL | PASS | PASS |
| 17 | 4593 | Tokens in text discussing simplicity, just after or around the word "simple" | 16.88 | 31.75 | 5.69 | 13.81 | +3.06 | PASS | PASS | PASS |
| 18 | 5072 | Technical modifier words in scientific/medical noun phrases, mostly the first word or middle of a compound term (e.g. "reperfusion", "ischemia-reperfusion", "overuse") | 17.50 | 13.25 | 0.00 | 5.88 | +7.38 | PASS | FAIL | FAIL (silent) |
| 19 | 5158 | Bootstrap "btn" CSS class names in HTML button/link class attributes (e.g. "btn btn-default") | 43.00 | 44.75 | 0.00 | 0.00 | +43.00 | PASS | PASS | FAIL (silent) |
| 20 | 6515 | Spam keyword phrases ("supra shoes", "unlimited proxy for pc") inserted into SEO-spam text | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | FAIL | FAIL (silent) |
| 21 | 6865 | Function words and verb phrases in clauses describing a person's attitude, decision, or action | 5.59 | 4.66 | 0.00 | 0.00 | +4.66 | PASS | FAIL | FAIL (partial) |
| 22 | 7196 | Function words and connective phrases inside long argumentative or legal reasoning sentences | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | FAIL | FAIL (silent) |
| 23 | 7223 | The word "Overall" used as a sentence-initial summarizing or concluding transition | 46.50 | 46.50 | 0.00 | 48.25 | -1.75 | FAIL | PASS | FAIL (partial) |
| 24 | 7467 | Tokens that complete a predictable multi-word phrase, often a domain-specific term or boilerplate (e.g. "incorporated herein by reference", "dedicated ereader", "wholly executory") | 3.20 | 6.62 | 0.00 | 3.83 | -0.62 | FAIL | FAIL | FAIL (partial) |
| 25 | 7623 | Line-break or punctuation tokens at the end of a title or question line, marking the boundary before the answer or body text begins | 3.33 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | FAIL | FAIL (silent) |
| 26 | 7798 | The word "happy" (and occasionally related tokens) in greetings and expressions of willingness | 45.00 | 42.75 | 15.56 | 0.00 | +27.19 | PASS | PASS | PASS |
| 27 | 8123 | Pipes and plumbing or piping components (pipe, line, pipefitters, joints, valves) | 36.50 | 36.25 | 17.38 | 0.00 | +18.88 | PASS | PASS | PASS |
| 28 | 8630 | Connective phrases in podcast/episode blurbs describing what hosts discuss | 35.25 | 37.75 | 0.00 | 9.62 | +25.62 | PASS | FAIL | FAIL (silent) |
| 29 | 8743 | Continuation of a negated clause with "nor/or/no" coordination extending a negation | 24.12 | 7.94 | 0.00 | 0.00 | +7.94 | PASS | PASS | FAIL (silent) |
| 30 | 10276 | Head nouns of product names in e-commerce listings (shorts, bra, forks, dress, bag, camera, boots, brush) | 22.25 | 20.50 | 0.00 | 8.06 | +12.44 | PASS | PASS | PASS |
| 31 | 11270 | Words within biopharma forward-looking statement boilerplate (Amicus-style press release disclaimers) | 45.75 | 37.75 | 0.00 | 0.00 | +37.75 | PASS | PASS | FAIL (partial) |
| 32 | 12608 | The word "control" and its variants (Control, CONTROL_, control group, controlPanel), across prose, code identifiers, and tables | 48.25 | 44.00 | 0.00 | 0.00 | +44.00 | PASS | PASS | FAIL (near-miss beat a should-fire) |
| 33 | 12964 | Scattered function words and phrases in crafting/making contexts (sewing, card-making, building projects) | 3.98 | 13.88 | 0.00 | 0.00 | +3.98 | PASS | PASS | PASS |
| 34 | 13230 | Electric utility and power industry context, such as energy markets, transmission, and utility companies | 25.62 | 30.00 | 14.31 | 0.00 | +11.31 | PASS | PASS | PASS |
| 35 | 14520 | Predicate or verb-phrase tokens in the middle of a clause, where the next words are predictable from context | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | FAIL | FAIL (silent) |
| 36 | 14719 | The word "color" (or COLOR_ prefix) as a token, in any casing, in code identifiers and in prose | 41.50 | 43.50 | 10.12 | 0.00 | +31.38 | PASS | PASS | FAIL (silent) |
| 37 | 15035 | The word "short" used as an adjective meaning brief or small in length, especially at the start of a noun phrase | 43.75 | 44.75 | 20.00 | 42.25 | +1.50 | PASS | FAIL | FAIL (near-miss beat a should-fire) |
| 38 | 15337 | Repeated proper nouns or rare terms (e.g., Mercury, Kansas, Kuwait) in a document, often as the first token of a name | 12.00 | 12.12 | 6.38 | 0.00 | +5.62 | PASS | FAIL | PASS |
| 39 | 15623 | The word "yellow" and other color terms (especially yellow), including in figure captions and descriptions | 44.50 | 34.25 | 0.00 | 0.00 | +34.25 | PASS | FAIL | FAIL (near-miss beat a should-fire) |
| 40 | 16358 | First-person or conversational function words and contractions near sentence starts in informal prose | 9.62 | 16.88 | 4.53 | 0.00 | +5.09 | PASS | PASS | FAIL (partial) |

## Notes and anomalies

- No rate-limit events, no failed calls, no retries were needed; all 160 prompts were scored fresh (0 cache hits).
- Test 6 (idx 1501) failed on an exact tie at the top: should-fire 2 and near-miss 2 both fired 47.00, so min(should-fire) 15.31 lost to max(near-miss) 47.00 (margin −31.69), as predicted.
- Test 9 (idx 2081) and Test 35 (idx 14520) recorded margin +0.00 with all four prompts at 0.00 — FAIL under the strict rule (0 is not > 0), as predicted.
- The result does not change the study's standing interpretation of the pilot: GPT-4o-mini's labels, as served, failed at 70%. It shows the failure is substantially an explainer-side problem, fixable in large part by a stronger explainer writing from the same evidence — which is the premise Study 2's bake-off arms test more rigorously.
