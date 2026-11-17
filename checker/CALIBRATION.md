# Calibration summary

The checker was calibrated against the 40 hand-tested pilot labels:
fresh prompts written from each label's plain reading, the pilot's
pass rule (min(should-fire) > max(near-miss)) applied on both sides,
verdicts compared by feature index, and mechanism tags compared
against the 17 silent features the pilot analyzed by hand.

## Verdicts

All three sorter versions share the same verdict engine, and all
three calibration runs agree with the human verdicts on **38/40
(95%)**:

- Both PASS: 10
- Both FAIL: 28
- Checker PASS / human FAIL: 0
- Checker FAIL / human PASS: 2

The two disagreements are the same in every run: idx 10276
("products related to fashion and beauty") and idx 12964
("references to crafting materials and methods"). Both are thin
human passes whose verdict flips with prompt wording — prompt
sensitivity, not a scorer error. The checker's own fresh-prompt
pass split was 10 pass / 30 fail in each run.

## Mechanism sorter accuracy (17 manually analyzed silent features)

- v1: 2/17 (11.8%) — see `CALIBRATION-V1.md`
- v2: 4/17 (23.5%) — see `CALIBRATION-V2.md`
- v3: 4/17 (23.5%) — see `CALIBRATION-V3.md`

v3's correct tags: idx 5072 (register — the style probes landed
this one), idx 5158 (word-form, the mined "btn" token), idx 7196
(unresolved), idx 14719 (word-form). What v3 changed relative to
v2: `register` is now over-tagged (five wrong register tags —
idx 18, 1029, 2081, 8743, 14520 — because many features respond
somewhat to styled text), and idx 6515 flipped from v2's correct
document-bound to unresolved once the topical length document
stopped counting as evidence.

## Honest summary

The verdict engine is the reliable part: 95% agreement with
hand testing, stable across all three versions. The mechanism
sorter is not solved. Each redesign traded one error type for
another rather than converging — v1 over-tagged displaced-theme,
v2 under-tagged register, v3 over-tags register. Read the sorter
tags as hypotheses for a human to check, not as findings.

Caveat: the 17 mechanism cases were also the tuning set for all
three versions, so these numbers are in-sample. A held-out check
on silent features from the 200-label scale-up (never used in
tuning) is the honest next measurement.
