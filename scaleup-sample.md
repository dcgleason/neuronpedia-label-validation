# Scale-up sample — Neuronpedia feature-label validation

- **Model:** Gemma-2-2B (`gemma-2-2b`)
- **SAE set:** Gemma Scope residual-stream, 16k width; source `<layer>-gemmascope-res-16k`
- **Size:** 160 NEW features — 80 from layer 12, 40 from layer 6, 40 from layer 18
- **Index range:** 0..16383 per layer
- **Exclusions:** the 60 layer-12 candidate indices used by the pilot (see `pilot-feature-candidates.md`) are excluded from the layer-12 population. Layers 6 and 18 are different SAE sources, so no exclusion applies there.

## Sampling method

Deterministic pseudo-random sampling, seed **20261112**, Python 3 `random`:

```python
rng = random.Random(20261112)
for layer, primary_n, draw_n in ((12, 80, 120), (6, 40, 60), (18, 40, 60)):
    population = sorted(set(range(16384)) - (PILOT_60 if layer == 12 else set()))
    draw = rng.sample(population, draw_n)   # layers drawn in order 12, 6, 18
    primary = draw[:primary_n]             # the sample below, in draw order
    reserve = draw[primary_n:]             # ordered replacement pool
```

Labels were fetched for every primary and reserve feature from the public API (`GET /api/feature/gemma-2-2b/<source>/<index>`, no key); the label is the first explanation's `description` (type `oai_token-act-pair`, the gpt-4o-mini autointerp label), verbatim apart from leading/trailing whitespace — the same rule the pilot used.

## Replacements

None. All 160 primary features carried an autointerp label, so no reserve draw was used. The reserve pools are listed below for the record and remain the replacement order if a feature is dropped later.

## Layer 12 — `12-gemmascope-res-16k` (80 features)

Primary sample, in draw order (= test order within the prompt file):

3473, 12984, 8317, 3387, 6295, 13468, 12076, 14567, 4116, 15741, 9939, 16078, 1906, 14547, 12503, 4013, 7165, 5830, 2899, 13052, 7808, 8936, 3420, 15873, 3816, 8127, 7091, 7199, 416, 8553, 5015, 15744, 1508, 8692, 11314, 14189, 14167, 4117, 11027, 1963, 5620, 11998, 13804, 14968, 15465, 8903, 270, 1797, 10243, 16163, 5390, 15886, 13957, 3120, 6793, 6196, 4871, 825, 896, 6785, 12314, 14530, 10356, 15792, 10820, 4584, 2819, 7088, 1109, 3344, 10844, 10816, 9211, 13961, 12878, 1283, 5545, 9884, 6811, 4330

Reserve pool, in replacement order (40):

3791, 4636, 3627, 11798, 14752, 10703, 2128, 10438, 14956, 64, 2053, 9151, 8841, 3990, 9955, 7776, 7553, 7819, 14816, 10735, 692, 7066, 11425, 11473, 2357, 14140, 13087, 4621, 10691, 1795, 9222, 1070, 6928, 2132, 7727, 2137, 3883, 14302, 11155, 10905

## Layer 6 — `6-gemmascope-res-16k` (40 features)

Primary sample, in draw order (= test order within the prompt file):

15620, 5661, 4689, 3292, 2547, 4758, 791, 8148, 11089, 10141, 14786, 11563, 4687, 13771, 1065, 16247, 7358, 7633, 1417, 4160, 2783, 11231, 13783, 14452, 10006, 11236, 14758, 1541, 2570, 15755, 4649, 635, 7011, 8615, 16152, 9442, 11722, 11452, 10507, 4846

Reserve pool, in replacement order (20):

1399, 15645, 10079, 5255, 1275, 3634, 15997, 12157, 6626, 14984, 15600, 13760, 13931, 11218, 10991, 10023, 12135, 9163, 10375, 8697

## Layer 18 — `18-gemmascope-res-16k` (40 features)

Primary sample, in draw order (= test order within the prompt file):

5397, 1922, 11259, 11711, 8767, 7935, 3567, 13353, 15775, 14571, 3432, 6630, 7593, 13540, 14996, 1765, 15986, 1963, 4857, 4319, 5378, 15475, 248, 15031, 11048, 5188, 15842, 348, 428, 14479, 2758, 16032, 3108, 14737, 955, 4475, 10702, 12235, 12239, 8013

Reserve pool, in replacement order (20):

717, 5787, 7848, 3866, 5004, 1623, 11240, 7368, 9301, 12172, 7512, 10492, 13747, 12333, 5766, 6624, 15917, 5733, 7034, 6169
