# Held-out sanity check (Nov 13, 2026)

After the v1–v3 calibration runs, the checker was run once, unchanged, on the
62 features from the 200-label scale-up whose four test prompts all scored
0.00 ("silent" features): 32 at layer 12, 18 at layer 6, 12 at layer 18.
Configuration: locked prompts from the scale-up, no rewrites file, no style
probes — the plain held-out setup. Full per-feature output is in
`sanity1-summary.md`.

**Verdicts:** 0 pass, 62 fail. Expected by construction: these features were
selected because the scale-up's own scoring found no activation on the same
locked prompts, and the checker reproduced those verdicts exactly.

**Mechanism tags (distribution only — there is no ground truth for these 62,
so this is not an accuracy number):**

| Tag | Count |
| --- | --- |
| unresolved | 49 |
| document-bound | 7 |
| word-form | 5 |
| displaced-theme | 1 |
| register | 0 |

Read: on genuinely held-out silent features the sorter mostly declines to
name a mechanism, which matches the calibration finding — the verdict engine
is the reliable part; the mechanism sorter is a first pass, not a measurement.
