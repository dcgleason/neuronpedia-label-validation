# Width control — bridge check results and limitation (Nov 14, 2026)

## Why a bridge check

Neuronpedia's inference API cannot score the width-control sample: inference is
disabled for gemma-2-2b residual-stream SAEs wider than 16k, and the width arm
needs the 65k source (`12-gemmascope-res-65k`). The fallback was local scoring
(SAELens + the HuggingFace checkpoint). Before any width prompt could be
scored locally, local activations had to be validated against the API on a
bridge set: 12 prompts across 4 features of the layer-12 16k SAE, with API
per-token activations already recorded (`bridge_prompts.json`).

## What was run

- Model: `google/gemma-2-2b`, HuggingFace checkpoint verified byte-for-byte
  against its own index (3 shards, 10,457,367,552 bytes total, SHA-256 logged
  per shard at download).
- SAE: `gemma-scope-2b-pt-res-canonical`, `layer_12/width_16k/canonical`
  (d_in 2304, d_sae 16384, hook `blocks.12.hook_resid_post`) — the SAELens
  counterpart of Neuronpedia's `12-gemmascope-res-16k`.
- Convention matched to the API: no `<bos>`, one forward pass per prompt,
  feature max over all positions. Local token counts equal the API's on all
  12 prompts.
- Compute constraint: the checkpoint is float32 (10.46 GB) and this machine
  has a ~6.4 GB memory ceiling; two full-model loads were OOM-killed
  (standard load, then disk-offloaded load). Scoring therefore used a
  streaming loader that materializes only the embedding and decoder layers
  0–12 in bf16 and runs the vendor decoder-layer, rotary, and mask code
  unchanged, stopping after layer 12.

## Result: the bridge FAILED

| Feature | Kind | API max | Local max | Local/API |
|---|---|---|---|---|
| 483 (Windows OS) | nm1 | 0 | 0.0000 | — |
| 483 | sf1 | 9.5625 | 5.4501 | 0.57 |
| 483 | sf2 | 6.9375 | 6.6218 | 0.95 |
| 1501 (surprise/celebration) | nm2 | 15.4375 | 0.0000 | 0.00 |
| 1501 | sf1 | 54.0 | 3.6491 | 0.07 |
| 1501 | sf2 | 0 | 0.0000 | — |
| 1657 (name "Tom") | nm1 | 13.5 | 7.4886 | 0.55 |
| 1657 | sf1 | 20.25 | 13.1503 | 0.65 |
| 1657 | sf2 | 21.75 | 11.8048 | 0.54 |
| 10276 (fashion/beauty) | nm1 | 0 | 0.0000 | — |
| 10276 | sf1 | 4.5 | 0.0000 | 0.00 |
| 10276 | sf2 | 8.9375 | 0.0000 | 0.00 |

- Exact-zero agreement: 3/3.
- Wherever the local run fired, its peak token was the API's peak token (6/6).
  The local pipeline finds the right tokens; the magnitudes are wrong.
- Mean absolute difference across the 12 maxes: 8.89 activation units.

A follow-up diagnostic captured layers 11, 12, and 13 plus encoder
pre-activations for all 12 prompts (`bridge_diagnostic.json`):

- Not a layer-indexing offset: layers 11 and 13 score no closer to the API
  than layer 12 (e.g. feature 1501 sf1 post-threshold max: L11 0.000,
  L12 3.649, L13 3.613, API 54.0).
- Not a threshold artifact: local pre-activations are themselves far below
  the API's post-threshold values for features 1501 and 10276, so the gap
  exists before the JumpReLU threshold is applied.

The cause of the divergence between the local stack and Neuronpedia's
serving stack was not identified with the compute available here. One
identified remedy is a full-precision run of the reference stack
(TransformerLens, fp32) on a machine that can hold the 10.46 GB checkpoint,
which would remove the streaming loader and bf16 casting from the list of
suspects. That run was not possible in this environment.

## Decision (Danny Gleason, Nov 14, 2026)

The bridge did not validate, so local activations must not be pooled with
API activations. **The width-control arm is closed unscored and recorded as
a limitation**: SAE width remains an open confound for the Gemma-vs-Llama
pass-rate gap in Study 1. The drafted width predictions (9/40) were never
locked and carry no evidential weight.

Raw data: `local-scoring/bridge_results.json`, `local-scoring/bridge_diagnostic.json`.
