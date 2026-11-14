# Llama multi-layer extension — design note (LOCKED)

**Status:** LOCKED, November 14, 2026. Approved by Danny Gleason and pre-registered with the companion locked predictions file before any scoring. Companion locked file: `llama-layers-predictions-locked-nov14.md` (the 80 tests).

## The question

Does the label pass rate vary by layer in Llama 3.1 8B, and does the pattern match Gemma-2-2B's? In Gemma, the pass rate was flat early and rose late: layer 6 passed 10/40 (25.0%), layer 12 passed 31/120 (25.8%), layer 18 passed 18/40 (45.0%). The Llama replication tested only layer 16 and passed 11/80 (13.8%) — lower than every Gemma cell, but with no depth profile, so we cannot tell whether Llama labels are uniformly weaker or whether layer 16 is simply a weak layer. This extension fills in the profile at two more depths with the identical protocol.

## Design

- **Layers 8 and 24.** Llama 3.1 8B has 32 layers; layer 8 is quarter depth, layer 24 is three-quarter depth, and together they bracket the existing layer 16 (half depth). Sources `8-llamascope-res-32k` and `24-llamascope-res-32k` (Llama Scope residual-stream, 32k width). Both sources were verified live on November 14, 2026 — one test activation call each through the connector helper, HTTP 200, response layer field matching the requested source. No substitute layers were needed.
- **n = 40 per layer**, matching the Gemma layer-6 and layer-18 cell sizes, so every cell in the combined model × layer table is directly comparable. Sampling mirrors the replication exactly: successive `randrange(32768)` draws, one `random.Random` per layer (seeds 2026111408 and 2026111424 — base 20261114 with the two-digit layer appended), labels taken from `explanations[0].description` via the public feature API, unlabeled or duplicate draws skipped and logged. Both layers drew 40/40 labeled features with no skips.
- **Identical protocol and pass rule.** Two should-fire and two near-miss prompts per feature (each near-miss changes one variable), one pre-registered PASS/FAIL prediction per label, pass = min(should-fire) > max(near-miss). Same failure classification as the replication after scoring.

## Arm-level predictions (locked)

1. **Layer 8 passes at or below layer 16's rate:** ≤ 13.8% (at most ~5 of 40). Early-layer Llama features are expected to be at least as token- and syntax-bound as layer 16's, and their concept-shaped labels should fail at least as often.
2. **Layer 24 passes at or above 25%** (at least 10 of 40) **if** Gemma's late-layer pattern generalizes across model families. This is the headline test: a high layer-24 rate would say the late-layer rise is a depth effect, not a Gemma quirk; a layer-24 rate near 14% would say Llama's labels are uniformly weak and Gemma's rise is family-specific.
3. **The silent class remains the dominant failure class at every layer** — more failures with both should-fires at 0.00 than any other failure shape, as at layer 16 (51 of 69 failures were silent on all four prompts) and throughout the Gemma work.

One tension, recorded at lock time: the per-label predictions are conservative — they call only 5/40 PASS at layer 8 and 6/40 at layer 24, because they are calibrated category-by-category on layer 16, where only 5 of 23 predicted passes actually passed. Prediction 2 (≥ 25% at layer 24) is therefore bolder than the per-label calls imply. Danny approved the draft as written on November 14, 2026: prediction 2 stands at ≥ 25%, and the per-label calls stand as drafted. The gap is intentional — prediction 2 is a claim about the layer, not about individual labels.

## Estimated cost

Scoring is 80 features × 4 prompts = **~320 activation calls**. Mechanism probes run on silent features only: at layer-16 rates (~64% of features silent), expect roughly 45–55 silent features at ~8–10 probe calls each, adding ~400–550 calls. Total ≈ 720–870 calls — inside one 1000-calls-per-60-minutes API window with pacing, or split across two windows. No other API use is planned.

## Lock procedure

1. Danny reviewed the predictions draft and approved it as written, including the three arm-level predictions above. (Done November 14, 2026.)
2. The approved file carries a locked filename, its SHA-256 is computed, and it is published to the GitHub repository (dcgleason/neuronpedia-label-validation) as the lock commit — **before any scoring**.
3. Only then is a run script written (mirroring `replication/run_replication.py`, same Scorer, per-layer sources, the script asserting the locked prediction tally before scoring) and the run executed.

Integrity note: at lock time, no sampled feature has been run through the activation API. The only activation calls made during preparation were the two source-verification calls on feature idx 0, which is in neither sample.
