# Permutation control (shuffled labels) — results

**Scored November 14, 2026**, after the pre-registration was public: lock commit `2b67c388d472b6dc61060aefde8d8f361d908064` in dcgleason/neuronpedia-label-validation (`permutation-control-design-locked-nov14.md`, `permutation-control-predictions-locked-nov14.md`). Raw data: `permutation-control/permutation-results.json` (run script: `permutation-control/run_permutation.py`).

## Headline

**0 of 40 shuffled pairings passed.** The real pairing passed 12 of 40 in the pilot. The control lands in the 0–2 band the locked design called a successful control: the protocol's verdicts track whether the label actually belongs to the feature, and the pilot's 12/40 stands as a measurement of the labels.

## The locked arm-level predictions, scored

1. **Total passes ≤ 2 of 40 (≤ 5%) — HELD.** Actual: 0 of 40 (0%).
2. **All 17 pilot-silent features fail — HELD.** 17 of 17 failed. 16 of the 17 scored exactly 0.00 on both received should-fire prompts. The one exception is idx 2580 (pair 10), which fired 3.92 on one of idx 1029's should-fire prompts — its first nonzero activation anywhere — but scored 0.00 on the other should-fire and failed, as predicted.
3. **Falsifier (≥ 6 of 40 passing) — NOT TRIGGERED.** 0 passes is nowhere near the ~15% chance level. The instrument discriminates.

**Prediction accuracy: 40 of 40 per-pair calls correct (100%).** All 40 locked per-pair predictions were FAIL; all 40 pairings failed.

## Failure classes

Same taxonomy as the rest of the study (silent = both should-fires exactly 0; near-miss-beat = a near-miss strictly outscored every should-fire; partial = every other failure).

- Silent: 37
- Partial: 3
- Near-miss-beat: 0

35 of the 40 targets scored 0.00 on all four foreign prompts. Only 5 pairings produced any nonzero activation at all:

- Pair 10 — target idx 2580 ← idx 1029's prompts: should-fires 3.92/0.00, near-misses 0.00/0.00 (partial).
- Pair 12 — target idx 3070 ← idx 7196's prompts: should-fires 0.00/0.00, near-misses 4.59/0.00 (silent).
- Pair 21 — target idx 6865 ← idx 5072's prompts: should-fires 4.12/0.00, near-misses 3.69/0.00 (partial).
- Pair 34 — target idx 13230 ← idx 12608's prompts: should-fires 3.75/0.00, near-misses 0.00/0.00 (partial).
- Pair 40 — target idx 16358 ← idx 1302's prompts: should-fires 0.00/0.00, near-misses 4.84/0.00 (silent).

## The flagged pair 32

The locked predictions named pair 32 — target idx 12608 ("terms related to control and regulation") receiving idx 8743's obligation/denial prompts — as the single most plausible accidental pass, because 12608 fired hard and indiscriminately at home (36.00 on a should-fire, 37.25 on a near-miss). Abroad it did not fire at all: should-fires 0.00/0.00, near-misses 0.00/0.00. The riskiest pairing in the design was completely silent on foreign text, which strengthens the control's reading: even the most reactive pilot feature does not fire on another label's prompts.

## Per-pair results

| Pair | Target idx | Source idx (prompts) | SF1 | SF2 | NM1 | NM2 | Margin | Verdict | Class |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 18 | 15337 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 2 | 483 | 3070 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 3 | 869 | 15035 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 4 | 1029 | 7623 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 5 | 1302 | 8123 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 6 | 1501 | 1643 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 7 | 1643 | 3592 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 8 | 1657 | 5158 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 9 | 2081 | 1501 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 10 | 2580 | 1029 | 3.92 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | partial |
| 11 | 2625 | 2580 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 12 | 3070 | 7196 | 0.00 | 0.00 | 4.59 | 0.00 | -4.59 | FAIL | silent |
| 13 | 3349 | 2625 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 14 | 3580 | 869 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 15 | 3592 | 15623 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 16 | 4207 | 4593 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 17 | 4593 | 13230 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 18 | 5072 | 14520 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 19 | 5158 | 7223 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 20 | 6515 | 3349 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 21 | 6865 | 5072 | 4.12 | 0.00 | 3.69 | 0.00 | -3.69 | FAIL | partial |
| 22 | 7196 | 6865 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 23 | 7223 | 6515 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 24 | 7467 | 10276 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 25 | 7623 | 18 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 26 | 7798 | 16358 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 27 | 8123 | 7467 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 28 | 8630 | 3580 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 29 | 8743 | 1657 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 30 | 10276 | 8630 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 31 | 11270 | 7798 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 32 | 12608 | 8743 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 33 | 12964 | 483 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 34 | 13230 | 12608 | 3.75 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | partial |
| 35 | 14520 | 2081 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 36 | 14719 | 12964 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 37 | 15035 | 11270 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 38 | 15337 | 14719 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 39 | 15623 | 4207 | 0.00 | 0.00 | 0.00 | 0.00 | +0.00 | FAIL | silent |
| 40 | 16358 | 1302 | 0.00 | 0.00 | 4.84 | 0.00 | -4.84 | FAIL | silent |

## Integrity and cost

- Locked predictions file SHA-256 verified before scoring and again after the run, unchanged: `c6ea8efe352f6b3db32a148fcf0ac61d39207f7deee5494c16be4452eedab582`.
- The derangement was parsed from the locked file two independent ways (the table and the per-pair sections); both parses agree on all 40 pairs, and a re-derivation from the locked seed (`random.Random(20261114)`) reproduces the same mapping. Target and source indices were checked against `pilot-prompts.json`.
- All 160 prompt strings were taken verbatim from the locked `pilot-prompts.json`; no prompt was edited.
- API calls: 160 (40 features × 4 prompts), cache hits: 0 — every (feature, prompt) pair was new, as the design disclosed.
- Scoring instrument: `checker/score.py`'s `Scorer`, identical to the pilot, scale-up, and replications — same endpoint, same max-activation extraction, source `12-gemmascope-res-16k`.

## What this does and does not show

It validates the instrument: with the label–feature pairing deliberately broken, the pass rate collapses from 30% to 0%, far below the ~16.7% rate chance alone would produce. Study 1's verdicts therefore measure label–feature match, not an artifact of the prompts or the pass rule. It does not re-prove any individual pilot verdict, and it says nothing about which explainer writes better labels — that is the explainer swap's question.
