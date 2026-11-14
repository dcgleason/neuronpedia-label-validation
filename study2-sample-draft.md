# Study 2 — draft sample (NOT locked)

Built Nov 13, 2026, from the scored Study 1 data, for Danny's review. Nothing here is locked, hashed, or published. No new labels or prompts have been generated.

Design: `study2-design-labeling-bakeoff.md` — 60 Gemma layer-12 features: 40 failed (25 silent, 10 partial, 5 near-miss-beat) + 20 passed, plus an appendix of 20 failed Llama layer-16 features for the optional Arms A/C spot check.

## Method

- **Population.** The 200 Gemma features scored in Study 1: the 40-feature pilot (all layer 12) plus the 160-feature scale-up (80 layer 12, 40 layer 6, 40 layer 18). The main sample is drawn from the 120 features that are actually layer 12, per the design's one-layer rule for the main run. See the verification section for the layer-count discrepancy in the "200 layer-12 features" wording.
- **Verdicts.** Recomputed from the raw per-prompt activations in `results-raw.json` (pilot) and `scaleup/scaleup-results.json` (scale-up) under the Study 1 pass rule, min(should-fire) > max(near-miss), and checked against both summary files — agreement on all 200 features.
- **Failure-class rule (mechanical, applied uniformly).** PASS if min(SF) > max(NM). Otherwise: **silent** if all four prompts scored 0.00; **near-miss-beat** if max(near-miss) > max(should-fire), i.e. a near-miss beat every should-fire; **partial** for any other failure (one should-fire silent, or the best should-fire beat both near-misses but the weaker one did not).
- **Selection rule.** Within each stratum, features are sorted by feature index ascending and picks are taken at evenly spaced positions (position floor(i × N / k) for pick i of k from a stratum of N). Deterministic, no randomness; the sample spans each stratum instead of clustering.
- **Labels** are the Neuronpedia (gpt-4o-mini) label strings verbatim from the results JSON files; the scale-up labels were cross-checked against `scaleup/scaleup-summary.md` and agree on all 160.

## Stratum 1 — Failed, silent (25 of 49 available)

| # | Feature idx | Current label (verbatim) | Study 1 verdict | Failure class | Margin | Source |
|---|---|---|---|---|---|---|
| 1 | 18 | terms related to food and culinary subjects | FAIL | silent | 0.00 | pilot — results-summary.md / results-raw.json |
| 2 | 416 | commands or functions related to logging or alerting in programming contexts | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 3 | 1029 | references to ancient figures and mythological or legendary elements | FAIL | silent | 0.00 | pilot — results-summary.md / results-raw.json |
| 4 | 1963 | specific items, brands, and concepts related to technology or electronics, as well as people and organizations | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 5 | 2580 | references to literary works and notable authors | FAIL | silent | 0.00 | pilot — results-summary.md / results-raw.json |
| 6 | 2819 | specific numerical values or symbols associated with various metrics or measurements | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 7 | 3120 | phrases expressing preferences for sharing or communication | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 8 | 3420 | special characters and symbols used in programming or mathematical contexts | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 9 | 4116 | key terms related to genetic traits and population genetics | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 10 | 4584 | phrases related to statistical measurements and observed data frequencies | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 11 | 5158 | elements related to buttons in a UI or web interface | FAIL | silent | 0.00 | pilot — results-summary.md / results-raw.json |
| 12 | 5545 | syntax elements related to control structures in programming | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 13 | 6515 | references to a specific shoe brand | FAIL | silent | 0.00 | pilot — results-summary.md / results-raw.json |
| 14 | 6793 | terms related to programming functions, particularly those dealing with data structures and control mechanisms | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 15 | 7196 | discussions and references to issues of racism and discriminatory behaviors | FAIL | silent | 0.00 | pilot — results-summary.md / results-raw.json |
| 16 | 8630 | discussions related to music and artistic collaborations | FAIL | silent | 0.00 | pilot — results-summary.md / results-raw.json |
| 17 | 8936 | elements related to data representation and measurement in scientific contexts | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 18 | 9939 | themes related to personal struggles and emotional conflicts | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 19 | 10820 | structured data and programming constructs | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 20 | 11998 | code snippets related to programming logic and control structures | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 21 | 12314 | proper nouns, particularly place names and related identifiers | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 22 | 13961 | numerical values and sequences, indicating a focus on data or time-related information | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 23 | 14520 | terms related to governance and political processes | FAIL | silent | 0.00 | pilot — results-summary.md / results-raw.json |
| 24 | 14719 | terms related to colors and color coding | FAIL | silent | 0.00 | pilot — results-summary.md / results-raw.json |
| 25 | 15792 | mentions of specific names or terms related to financial or transactional contexts | FAIL | silent | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |

## Stratum 2 — Failed, partial (10 of 34 available)

| # | Feature idx | Current label (verbatim) | Study 1 verdict | Failure class | Margin | Source |
|---|---|---|---|---|---|---|
| 1 | 270 | comments and documentation within code | FAIL | partial | -5.03 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 2 | 1109 | terms related to technical and mechanical failures or issues | FAIL | partial | -0.31 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 3 | 1797 | terms related to affordability and financial accessibility | FAIL | partial | -3.62 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 4 | 3816 | academic institutions and their departments | FAIL | partial | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 5 | 6865 | references to personal beliefs, self-identification, and emotional experiences | FAIL | partial | -3.50 | pilot — results-summary.md / results-raw.json |
| 6 | 7223 | phrases that indicate summary or overall conclusions | FAIL | partial | 0.00 | pilot — results-summary.md / results-raw.json |
| 7 | 10243 | phrases related to capital and financial expenditures | FAIL | partial | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 8 | 12878 | code-related actions and concepts, particularly those related to database operations and backup processes | FAIL | partial | -3.59 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 9 | 14530 | mathematical formulas and symbols | FAIL | partial | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 10 | 15886 | terms related to light, rays, and optics | FAIL | partial | 0.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |

## Stratum 3 — Failed, near-miss-beat (5 of 6 available)

| # | Feature idx | Current label (verbatim) | Study 1 verdict | Failure class | Margin | Source |
|---|---|---|---|---|---|---|
| 1 | 1643 | references to light and illumination contexts | FAIL | near-miss-beat | -33.31 | pilot — results-summary.md / results-raw.json |
| 2 | 8127 | specific terms and concepts related to complex systems and interactions | FAIL | near-miss-beat | -2.95 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 3 | 12608 | terms related to control and regulation | FAIL | near-miss-beat | -37.25 | pilot — results-summary.md / results-raw.json |
| 4 | 14167 | references to supplies and equipment items | FAIL | near-miss-beat | -13.06 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 5 | 15035 | phrases that highlight the concept of “short” in various contexts | FAIL | near-miss-beat | -10.75 | pilot — results-summary.md / results-raw.json |

The one pool member not picked is idx 15623 ("references to the color yellow and its variations", pilot, margin -5.50).

## Stratum 4 — Passed (20 of 31 available)

| # | Feature idx | Current label (verbatim) | Study 1 verdict | Failure class | Margin | Source |
|---|---|---|---|---|---|---|
| 1 | 483 | references to the Windows operating system | PASS | — | 6.94 | pilot — results-summary.md / results-raw.json |
| 2 | 1302 | shipping-related terms and phrases for large items | PASS | — | 3.28 | pilot — results-summary.md / results-raw.json |
| 3 | 1906 | commands and processes related to executing scripts or programs in a programming context | PASS | — | 15.80 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 4 | 3344 | words related to leaves and their conditions or characteristics | PASS | — | 15.12 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 5 | 4013 | topics related to training and preparation processes | PASS | — | 0.03 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 6 | 4207 | expressions of “coolness” or related positive attributes | PASS | — | 1.25 | pilot — results-summary.md / results-raw.json |
| 7 | 4593 | concepts related to simplicity and straightforwardness | PASS | — | 4.31 | pilot — results-summary.md / results-raw.json |
| 8 | 5015 | phrases specifically related to conditions and their descriptions in various contexts | PASS | — | 32.00 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 9 | 6295 | descriptions of physical spaces and their layout | PASS | — | 11.06 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 10 | 7091 | emotions and challenges related to difficult situations | PASS | — | 4.59 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 11 | 7808 | mentions and interactions on social media platforms, particularly Twitter | PASS | — | 8.06 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 12 | 8553 | specific programming constructs related to animation and image processing in game development | PASS | — | 2.16 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 13 | 8692 | terms related to the implementation process in various contexts | PASS | — | 47.50 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 14 | 9884 | concepts related to agriculture and food production | PASS | — | 4.19 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 15 | 10276 | products related to fashion and beauty | PASS | — | 0.16 | pilot — results-summary.md / results-raw.json |
| 16 | 10844 | instances of the word "indicate" and its derivatives related to signaling or specifying information | PASS | — | 23.88 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 17 | 12964 | references to crafting materials and methods | PASS | — | 4.56 | pilot — results-summary.md / results-raw.json |
| 18 | 13230 | terms related to electricity and power infrastructure | PASS | — | 10.97 | pilot — results-summary.md / results-raw.json |
| 19 | 13468 | references to monsters or monstrous entities | PASS | — | 11.16 | scale-up — scaleup/scaleup-summary.md / scaleup/scaleup-results.json |
| 20 | 15337 | mentions of the term “Mercury,” particularly in relation to its propulsion systems and legal implications | PASS | — | 0.06 | pilot — results-summary.md / results-raw.json |

## Appendix — Llama layer-16 failures for the Arms A/C spot check (20 of 69)

Source: `replication/replication-analysis.json`, cross-checked against `replication-results-llama-nov13.md`. Same selection rule applied to all 69 failed features sorted by index (the failed pool holds 51 silent, 16 partial, 2 near-miss-beat; the evenly spaced picks land on 16 silent and 4 partial). The two near-miss-beat failures — idx 18024 ("references to application-related dates and timelines") and idx 25296 ("expressions of seasonal or weather-related appreciation and enjoyment") — were not picked by the spacing rule; swap one in by hand if the spot check should include that class.

| # | Feature idx | Current label (verbatim) | Replication verdict | Failure class | Margin |
|---|---|---|---|---|---|
| 1 | 49 | dates and locations related to events | FAIL | silent | 0.00 |
| 2 | 630 | elements associated with religious sacraments and their significance | FAIL | partial | 0.00 |
| 3 | 1211 | terms related to the aging and flavoring process of beer | FAIL | partial | -2.34 |
| 4 | 3173 | phrases related to rarity and significance within various contexts | FAIL | silent | 0.00 |
| 5 | 3458 | URLs and web-related syntax | FAIL | silent | 0.00 |
| 6 | 4982 | elements related to recipes and cooking instructions | FAIL | silent | 0.00 |
| 7 | 6470 | phrases indicating emotional states or interactions with others | FAIL | silent | 0.00 |
| 8 | 8796 | references to specific airports and their connectivity | FAIL | partial | -0.56 |
| 9 | 9470 | specific quantities and their related context in various scenarios | FAIL | silent | 0.00 |
| 10 | 10870 | structured data or programming syntax related to hardware devices | FAIL | silent | 0.00 |
| 11 | 13568 | elements related to programming or technical specifications | FAIL | silent | 0.00 |
| 12 | 15837 | elements of tension and conflict in relationships | FAIL | silent | 0.00 |
| 13 | 18531 | dates and numerical references related to events | FAIL | silent | 0.00 |
| 14 | 19894 | dialogue and speech patterns within the text | FAIL | silent | 0.00 |
| 15 | 21341 | instances of significant numerical values or comparative phrases | FAIL | silent | 0.00 |
| 16 | 23860 | terms related to sports events and gambling | FAIL | partial | 0.00 |
| 17 | 25825 | concepts related to cultural identity and its components | FAIL | silent | 0.00 |
| 18 | 27382 | references to products and solutions related to construction and maintenance | FAIL | silent | 0.00 |
| 19 | 28808 | key events or dramatic situations in a narrative | FAIL | silent | 0.00 |
| 20 | 31073 | mentions of Java-related annotations and libraries | FAIL | silent | 0.00 |

## Verification

**Totals check (pooled Study 1, all 200 features).** Pilot 40: 12 pass / 28 fail. Scale-up 160: 47 pass / 113 fail (layer 6: 10/30, layer 12: 19/61, layer 18: 18/22). Pooled: **59 pass / 141 fail of 200** — exactly the totals the sample was specified against. Recomputed verdicts from the raw JSON agree with `results-summary.md` and `scaleup/scaleup-summary.md` on all 200 features; no duplicate (layer, index) pairs exist.

**Stratum pools found vs needed (layer-12 pool, n = 120).**

| Stratum | Needed | Available in L12 pool | Available in pooled 200 |
|---|---|---|---|
| Silent | 25 | 49 | 79 |
| Partial | 10 | 34 | 54 |
| Near-miss-beat | 5 | 6 | 8 |
| Passed | 20 | 31 | 59 |

All four strata fill from the layer-12 pool alone. Near-miss-beat is the thin one: only 6 candidates exist at layer 12, so the sample takes 5 of the 6.

**Discrepancy 1 — "200 layer-12 features" is not what the data holds.** The pilot is all layer 12 (40), but the scale-up spans three layers: 80 at layer 12, 40 at layer 6, 40 at layer 18 (`scaleup/scaleup-sample.md`). Only 120 of the 200 are layer-12 features. The 59 pass / 141 fail totals are correct for the pooled 200. This draft follows the design doc's own limit ("one layer, one model for the main run") and draws the 60 from the true layer-12 pool. If Danny wants the pooled-200 reading instead, the strata also fill from that pool (counts in the right-hand column above), but the sample would mix layers 6 and 18 into the main run.

**Discrepancy 2 — pilot failure-class split differs by one feature.** `pilot-writeup.md` reports the 28 pilot failures as 17 silent / 6 "one should-fire silent" / 5 "a near-miss matched or beat a should-fire". The mechanical rule above gives 17 / 7 / 4. The differing feature is idx 1501 ("moments of surprise or unexpected events, particularly those that are positive or celebratory in nature."): SF 54.00, 0.00; NM 0.00, 15.44. A near-miss beat its silent should-fire but not its best should-fire (54.00). The writeup's grouping appears to count it as near-miss-beat; the mechanical rule counts it partial. Pass/fail totals are unaffected, and idx 1501 is in the partial pool but was not picked. Two scale-up layer-12 failures sit on the same boundary: idx 13052 and idx 7199, where a near-miss exactly tied the best should-fire (margins -9.25 and -2.12 through the weaker should-fire); both are classed partial under the strict rule.

**Llama appendix check.** `replication/replication-analysis.json` holds all 80 scored features: 11 pass / 69 fail. Recomputing the classes from its per-prompt values under the same rule reproduces the writeup's split exactly: 51 silent / 16 partial / 2 near-miss-beat.

**Shortfalls and ambiguities.** None on counts: every stratum filled, all labels present verbatim, all verdicts cross-checked. The two open items are the layer-pool choice in Discrepancy 1 (a decision for Danny, flagged rather than resolved silently) and the boundary-class judgment in Discrepancy 2 (documented, no effect on the sample unless Danny prefers the writeup's grouping, which would move idx 1501 from the partial pool into the near-miss-beat pool; it is not picked under the current rule, so the sample itself is unchanged either way).
