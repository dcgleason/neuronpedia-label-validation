# Llama multi-layer extension — results

Scored November 14, 2026, against the pre-registered lock (`llama-layers-predictions-locked-nov14.md`, SHA-256 `9bedd27f155ebc91dda8e21aecd86129b102a35cd2a2b3500f3f92cf6b5172f1`, published as GitHub commit f820cb5 before scoring; the locked file's hash was re-verified after the run and is unchanged). Method mirrors the November 13 Llama replication exactly: same Neuronpedia activation endpoint and Scorer, same pass rule — **min(should-fire) > max(near-miss)** — same failure classification, and the checker's mechanism sorter (plain held-out configuration, no rewrites, no style probes) run on the silent features only. Model `llama3.1-8b`; sources `8-llamascope-res-32k` (tests 1–40) and `24-llamascope-res-32k` (tests 41–80).

## Headline results

| Llama layer | Passed | Rate | Locked prediction tally |
|---|---|---|---|
| 8 (quarter depth) | 9 / 40 | 22.5% | 5 PASS / 35 FAIL |
| 16 (half depth, Nov 13 replication) | 11 / 80 | 13.8% | 23 PASS / 57 FAIL |
| 24 (three-quarter depth) | 12 / 40 | 30.0% | 6 PASS / 34 FAIL |

Combined, this run passed **21 of 80 labels (26.2%)**. Layer 16's 13.8% was not Llama's uniform level: layer 8 passed higher and layer 24 higher still.

## Prediction accuracy

- Overall: **60 / 80 (75.0%)** against the locked 11 PASS / 69 FAIL.
- Layer 8: 30 / 40 (75.0%). Layer 24: 30 / 40 (75.0%).
- Of the 11 labels predicted to pass, 6 passed (layer 8: 2 of 5; layer 24: 4 of 6). Of the 69 predicted to fail, 54 failed.
- The misses lean one way: 15 labels predicted FAIL passed (7 at layer 8, 8 at layer 24), against 5 predicted PASS that failed. The per-label calls were calibrated category-by-category on layer 16 and underestimated both new layers — the conservative bias recorded at lock time, in the direction the lock note anticipated for layer 24.

## Failure classes

Classes: **silent** = both should-fires exactly 0.00; **near-miss-beat** = a near-miss strictly outscored every should-fire (an exact tie counts as partial); **partial** = every other failure.

| Layer | Failures | Silent | Partial | Near-miss-beat |
|---|---|---|---|---|
| 8 | 31 | 24 | 6 | 1 |
| 24 | 28 | 20 | 8 | 0 |
| 16 (replication) | 69 | 51 | 16 | 2 |

One classification note: test 21 (layer 8, idx 28106) is this run's only near-miss-beat under the strict rule — near-miss max 0.79 against should-fire max 0.49, with one should-fire at 0.00. Under the replication analysis's five-shape mapping the same four numbers land in the one-sf-silent shape (mapped to partial). Both views are recorded in the raw analysis JSON; the class above follows this run's locked definition.

## Verdicts on the three locked arm-level predictions

1. **Layer 8 at or below layer 16's 13.8% — FAILED.** Layer 8 passed 9 / 40 (22.5%), well above the ~5-of-40 ceiling the prediction allowed. Early-layer Llama labels are not at least as weak as layer 16's; layer 16 is the dip, not the baseline.
2. **Layer 24 at or above 25% — SUPPORTED.** Layer 24 passed 12 / 40 (30.0%), clearing the 10-of-40 bar. The late-layer rise seen in Gemma appears in Llama as well (see the cross-model table below).
3. **Silent is the dominant failure class at every layer — SUPPORTED.** Silent failures are 24 of 31 at layer 8 and 20 of 28 at layer 24, the largest class at both layers by a wide margin, as at layer 16 (51 of 69) and throughout the Gemma work.

## Cross-model layer table

| Model | Early (~quarter depth) | Middle (~half depth) | Late (~three-quarter depth) |
|---|---|---|---|
| Gemma-2-2B (26 layers) | L6: 10/40 = 25.0% | L12: 31/120 = 25.8% | L18: 18/40 = 45.0% |
| Llama 3.1 8B (32 layers) | L8: 9/40 = 22.5% | L16: 11/80 = 13.8% | L24: 12/40 = 30.0% |

**Does the late-layer rise generalize? In direction, yes; in shape, not exactly.** In both families the three-quarter-depth cell is the best cell (Gemma 45.0%, Llama 30.0%), and in both it beats the same model's middle cell by a wide margin. That is the pattern prediction 2 bet on, and it held. The profiles differ before that point, though: Gemma is flat early (25.0%, 25.8%) and then rises, while Llama dips — layer 8 (22.5%) sits above layer 16 (13.8%) before layer 24 rises. So the shared finding is a late-layer advantage, not a common curve.

Noise check, so the dip is not over-read: at these cell sizes one standard error is roughly ±7 points at layer 8, ±4 at layer 16, ±7 at layer 24. The layer 24 vs 16 gap (16.2 points) is about 2.0 standard errors — the run's strongest signal. The layer 8 vs 16 gap (8.7 points) is about 1.1 standard errors — suggestive, not settled. Llama's absolute rates also remain below Gemma's at matched late depth (30.0% vs 45.0%).

## Mechanism sorter (silent features)

All 44 silent features were sorted (24 at layer 8, 20 at layer 24). Every one of the 44 came back **unresolved**. The sorter found no word-form, register, document-structure, or displaced-theme mechanism for any of them — a more uniform outcome than layer 16, where 1 of 51 silent features sorted as word-form. As in the calibration work, the sorter's verdicts are the weak instrument here; the pass/fail verdicts above do not depend on it.

## Notable individual features

- **Test 76 (L24, idx 3155), “mentions of specific dates in February” — predicted FAIL, passed with margin 8.62.** The prediction rested directly on layer-16 evidence that specific-date features fail; at layer 24 the same kind of label passed decisively. The clearest single reversal in the run.
- **Test 71 (L24, idx 15269), “references to charter schools and related educational systems” — the largest margin of the run, 16.62** (predicted PASS, passed).
- **Test 45 (L24, idx 18249), “elements related to cryptography and hashing processes” — predicted PASS, failed as partial.** One should-fire fired at 13.94, the other at 0.00: the feature answers half the label's plain meaning and ignores the rest.
- **Tests 69 and 56 (L24), CSS border/box-shadow terms (margin 7.88) and Python programming concepts (margin 3.42)** — both predicted FAIL on layer-16 evidence about code categories, both passed. Code labels behaved better at layer 24 than the layer-16 calibration assumed.
- **Test 21 (L8, idx 28106), “mentions of individuals involved in incidents of violence or crime” — the run's only near-miss-beat** (strict rule): the near-miss scored 0.79 against a should-fire max of 0.49.
- **Tests 25 and 37 (L8), “specific non-English characters and texts” (idx 14979) and “abbreviations or acronyms related to organizations or associations” (idx 15158)** — both predicted PASS, both completely silent on all four prompts.

## Run integrity and API accounting

- The locked file's SHA-256 was verified before scoring and again after the run: unchanged. Before any scoring call, an independent dual parse (the replication's regex parse and a separate line-based parse) agreed on all 320 prompts verbatim, none empty, and the prediction tally asserted exactly 11 PASS / 69 FAIL (layer 8: 5/35; layer 24: 6/34). The analysis pass re-asserted that every scored prompt string equals the locked prompt string.
- Scoring: 320 prompts, 320 API calls, no errors. Mechanism sorter: 382 API calls in the completed run (127 further calls served from the disk cache). One earlier sorter attempt was terminated (SIGTERM) after 4 features; its probe results were re-served from cache on the successful re-run and nothing was double-scored. All calls stayed inside the documented 1000-requests-per-60-minutes limit (the Scorer enforces a 950-call rolling window).
- Raw data: `llama-layers/llama-layers-results.json` (per-prompt activations), `llama-layers/llama-layers-analysis.json` (per-test verdicts, classes, shapes, mechanism tags and sorter detail), `llama-layers/llama-layers-prompts.json` (the verified parse of the locked file). Nothing from this run has been published to GitHub.

## All 80 tests

### Layer 8

- Test 1 (idx 27277) “references to sports organizations or events”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 2 (idx 2189) “references to global diversity and inclusiveness”: SF 0.00, 0.00 · NM 0.36, 0.00 · margin -0.36 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 3 (idx 16108) “phrases related to scientific and technical concepts”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 4 (idx 23753) “references to royal titles and their associated entities”: SF 2.02, 1.36 · NM 0.00, 0.00 · margin 1.36 · **PASS** (predicted PASS)
- Test 5 (idx 14695) “structural elements and syntax related to programming and coding conventions”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 6 (idx 19465) “code-related keywords and structures within programming syntax”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 7 (idx 18188) “references to images and photography in various contexts”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 8 (idx 22224) “specific identifiers and structured data in text”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 9 (idx 28300) “references to the concept of change”: SF 1.78, 1.40 · NM 0.71, 0.00 · margin 0.69 · **PASS** (predicted FAIL)
- Test 10 (idx 104) “terms related to measurements and adjustments of rates or effectiveness”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 11 (idx 15695) “references to fame and success in the context of individuals or groups”: SF 2.34, 0.36 · NM 0.00, 0.00 · margin 0.36 · **PASS** (predicted FAIL)
- Test 12 (idx 20596) “phrases concerning the consequences and effects of actions or decisions”: SF 1.93, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: partial
- Test 13 (idx 9110) “words related to romantic relationships and interpersonal conflicts”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 14 (idx 17737) “technical terms and concepts related to radar systems and their components”: SF 0.00, 0.67 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · class: partial
- Test 15 (idx 16835) “references to wedding photography in North Wales”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 16 (idx 29439) “references to web URLs”: SF 2.14, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: partial
- Test 17 (idx 21205) “inquiries and requests for assistance or information”: SF 0.00, 0.80 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: partial
- Test 18 (idx 7223) “UI navigation elements and commands related to closing or canceling actions”: SF 1.93, 2.05 · NM 0.49, 0.00 · margin 1.44 · **PASS** (predicted PASS)
- Test 19 (idx 23375) “items in a navigation or menu list structure”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 20 (idx 22669) “citation formats and references in the text”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 21 (idx 28106) “mentions of individuals involved in incidents of violence or crime”: SF 0.49, 0.00 · NM 0.00, 0.79 · margin -0.79 · **FAIL** (predicted FAIL) · class: near-miss-beat
- Test 22 (idx 20778) “code and programming concepts related to state management and hooks in React”: SF 0.00, 0.32 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: partial
- Test 23 (idx 6788) “concepts related to underlying issues and their consequences in various contexts”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 24 (idx 4527) “punctuations and ellipses in the text”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 25 (idx 14979) “specific non-English characters and texts”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · class: silent · mechanism: unresolved
- Test 26 (idx 22894) “terms related to nudity and body exposure”: SF 3.00, 3.67 · NM 0.49, 0.00 · margin 2.51 · **PASS** (predicted FAIL)
- Test 27 (idx 25256) “programming-related terms and structures”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 28 (idx 27400) “coding syntax and structure”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 29 (idx 31301) “terms related to coordination and organizational activities”: SF 2.33, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: partial
- Test 30 (idx 2250) “references to gun ownership and related legislative discussions”: SF 2.06, 2.02 · NM 0.00, 0.00 · margin 2.02 · **PASS** (predicted FAIL)
- Test 31 (idx 32520) “references to organizations and groups related to veterans and women's associations”: SF 1.25, 0.53 · NM 0.00, 0.00 · margin 0.53 · **PASS** (predicted FAIL)
- Test 32 (idx 29812) “elements related to instructional content and product information”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 33 (idx 3727) “references to organizational meetings and events”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 34 (idx 13137) “phrases related to investment opportunities in various locations”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 35 (idx 6127) “phrases indicating large groups or quantities”: SF 2.58, 1.67 · NM 0.00, 0.00 · margin 1.67 · **PASS** (predicted FAIL)
- Test 36 (idx 31687) “words indicating a state of being or existence”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 37 (idx 15158) “abbreviations or acronyms related to organizations or associations”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · class: silent · mechanism: unresolved
- Test 38 (idx 27446) “key terms and phrases related to significant entities and their associations”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 39 (idx 28584) “references to regulatory actions and legal settlements involving investigations”: SF 1.38, 1.36 · NM 0.48, 0.51 · margin 0.85 · **PASS** (predicted FAIL)
- Test 40 (idx 6627) “specific formatting or coding elements, often related to bibliographic references or citations”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved

### Layer 24

- Test 41 (idx 16917) “terms related to marine organisms and their health benefits”: SF 0.00, 11.38 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: partial
- Test 42 (idx 10092) “details about construction projects and their schedules”: SF 6.41, 1.57 · NM 0.00, 0.00 · margin 1.57 · **PASS** (predicted FAIL)
- Test 43 (idx 6962) “academic and educational qualifications”: SF 0.00, 0.00 · NM 2.94, 0.00 · margin -2.94 · **FAIL** (predicted PASS) · class: silent · mechanism: unresolved
- Test 44 (idx 3510) “numerical values and identifiers used in scientific and technical contexts”: SF 0.00, 1.90 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: partial
- Test 45 (idx 18249) “elements related to cryptography and hashing processes”: SF 13.94, 0.00 · NM 2.19, 0.00 · margin -2.19 · **FAIL** (predicted PASS) · class: partial
- Test 46 (idx 24816) “instances of dialogue or verbal expressions within the text”: SF 0.00, 0.00 · NM 5.62, 2.95 · margin -5.62 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 47 (idx 14728) “references to academic papers or publications”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 48 (idx 5588) “key issues related to economic impact and industry growth”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 49 (idx 23530) “references to published articles and sources in a document”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 50 (idx 10617) “elements related to sports events and scores”: SF 1.23, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: partial
- Test 51 (idx 19500) “online resources and services related to academic assistance and e-commerce”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 52 (idx 4680) “specific types of agreements and collective decisions”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 53 (idx 23356) “expressions of uncertainty or conditions in various contexts”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 54 (idx 29911) “details about professional achievements and background in photography and film”: SF 10.38, 2.12 · NM 0.00, 0.00 · margin 2.12 · **PASS** (predicted FAIL)
- Test 55 (idx 8994) “terms related to social sciences and their theories”: SF 8.25, 6.31 · NM 0.00, 0.00 · margin 6.31 · **PASS** (predicted FAIL)
- Test 56 (idx 29746) “elements related to Python programming concepts and functionalities”: SF 3.42, 5.03 · NM 0.00, 0.00 · margin 3.42 · **PASS** (predicted FAIL)
- Test 57 (idx 7981) “geographical or location-based terms”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 58 (idx 26744) “concepts related to eco-friendliness and nature immersion”: SF 3.08, 6.56 · NM 0.00, 0.00 · margin 3.08 · **PASS** (predicted FAIL)
- Test 59 (idx 27334) “various levels of measurement or evaluation”: SF 8.38, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: partial
- Test 60 (idx 3103) “references to the Persian Sassanians and their historical context”: SF 8.12, 11.38 · NM 0.00, 0.00 · margin 8.12 · **PASS** (predicted PASS)
- Test 61 (idx 9044) “references to individuals and organizations involved in technology and machine learning”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 62 (idx 19170) “references to companies and organizational structures”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 63 (idx 24001) “phrases related to the frequency and regularity of activities or occurrences”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 64 (idx 19832) “references to storage facilities and related concepts”: SF 11.38, 8.19 · NM 0.00, 0.00 · margin 8.19 · **PASS** (predicted PASS)
- Test 65 (idx 29452) “references to blame and criticism regarding media and political narratives”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 66 (idx 21040) “conjunctions and interrogative phrases related to inquiries or questions”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 67 (idx 20626) “references to specific locations and entities”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 68 (idx 6413) “positive descriptors and expressions of success”: SF 2.16, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: partial
- Test 69 (idx 8246) “CSS styling properties related to borders and box shadows”: SF 7.88, 9.69 · NM 0.00, 0.00 · margin 7.88 · **PASS** (predicted FAIL)
- Test 70 (idx 26702) “references to programming tasks and documentation practices”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 71 (idx 15269) “references to charter schools and related educational systems”: SF 16.62, 17.00 · NM 0.00, 0.00 · margin 16.62 · **PASS** (predicted PASS)
- Test 72 (idx 31920) “punctuation marks and related terms that emphasize arrangements or structures”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 73 (idx 12653) “information related to giveaways and contests”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 74 (idx 27839) “references to outdoor activities and sports”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 75 (idx 8622) “themes related to digital privacy and data control issues”: SF 2.45, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: partial
- Test 76 (idx 3155) “mentions of specific dates in February”: SF 9.31, 8.62 · NM 0.00, 0.00 · margin 8.62 · **PASS** (predicted FAIL)
- Test 77 (idx 12706) “terms related to DNS (Domain Name System) configurations and settings”: SF 13.44, 8.00 · NM 0.00, 0.00 · margin 8.00 · **PASS** (predicted PASS)
- Test 78 (idx 1726) “programming constructs and syntax, particularly related to setting values and property definitions”: SF 1.77, 2.11 · NM 0.00, 0.00 · margin 1.77 · **PASS** (predicted FAIL)
- Test 79 (idx 25362) “phrases indicating relationships or connections among subjects”: SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: silent · mechanism: unresolved
- Test 80 (idx 31376) “words and phrases related to cyclical or revolving concepts”: SF 0.00, 5.97 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · class: partial

