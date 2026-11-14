# Permutation control (shuffled labels) — design note (LOCKED)

**Status:** LOCKED, November 14, 2026. Drafted November 14, 2026; approved as drafted by Danny Gleason on November 14, 2026 (~11:57 AM ET) and pre-registered with the companion locked predictions file before any scoring. Companion locked file: `permutation-control-predictions-locked-nov14.md` (the derangement table and all 40 predictions). No scoring of any kind has been performed. No activation calls of any kind were made while preparing this design — it reuses the pilot's already-verified SAE source and its locked prompts verbatim, so no source-verification call was needed. This file must not be edited after locking.

## The question

Study 1's headline result — only 12 of 40 Neuronpedia labels passed a held-out prompt test on Gemma-2-2B layer 12 — is only meaningful if the test itself discriminates. If the protocol would also "pass" labels attached to the wrong features, the pass/fail verdicts measure something about the prompts or the scoring rule rather than about label quality. This control runs the identical protocol with the label–feature pairing deliberately broken: every pilot feature is scored against a *different* feature's four locked prompts. Shuffled labels should pass near 0%. If they pass at anything like the real pairing's rate (12/40, 30%), the instrument is broken and Study 1's verdicts — and the scale-up and replications built on the same protocol — are suspect. This is the random-control condition the prior-art scan flagged (Heap et al.: autointerp scores that cannot distinguish a trained model from a random one are not measuring anything).

A pass under permutation requires a specific accident: the target feature's true trigger must happen to be present in the source feature's two should-fire prompts and absent (or weaker) in its two near-miss prompts. The near-miss structure is what makes the control sharp — a feature that merely fires a lot on foreign text still fails, because its firing does not track the other label's should-fire/near-miss contrast.

## Design

- **Sample: the 40 pilot features, unchanged.** Gemma-2-2B, Gemma Scope residual 16k, layer 12, source `12-gemmascope-res-16k`. Same features, same order (pilot test numbers 1–40), as `pilot-final-40.md` and `pilot-prompts.json`.
- **Prompts: the locked pilot prompts, verbatim.** Each feature receives another feature's exact two should-fire and two near-miss prompts from `pilot-prompts.json` (locked November 12, 2026). No prompt is edited, added, or rewritten. Disclosure: this reuses the pilot's locked prompt set in full; the only new element is the pairing. Any weakness in the original prompts is inherited by design — that is the point of a control.
- **Derangement rule (exact).** Let positions 1–40 be the pilot test numbers in order. Draw a permutation with `random.Random(seed)`: `perm = list(range(40))`, `rng.shuffle(perm)`. The feature at position *i* receives the prompts of the feature at position `perm[i] + 1`. Accept the permutation only if it is a true derangement — `perm[i] != i` for every *i*, so no feature keeps its own prompts. If any fixed point occurs, discard the permutation, increment the seed by 1, and redraw. **Outcome: the first seed tried, 20261114, produced a valid derangement with zero fixed points; no redraw was needed.** The full mapping is in the companion predictions draft.
- **Pass rule (identical to the pilot).** A pairing passes if both received should-fire prompts activate the target feature clearly above both received near-miss prompts: min(should-fire) > max(near-miss). Same failure classification as the pilot (silent / partial / near-miss-beat) after scoring.
- **Scoring instrument (identical).** `checker/score.py`'s `Scorer` — same endpoint (`POST https://www.neuronpedia.org/api/activation/new`), same max-activation extraction, same model and source. One disclosure: the scorer's disk cache is keyed by source + feature index + prompt text. Every (feature, prompt) pair in this run is a combination the pilot never scored — the derangement guarantees no feature is ever paired with its own prompts — so the pilot cache can serve none of the 160 calls. All 160 will be genuine API calls.

## Arm-level predictions (locked — full text in the companion file)

1. **Total passes ≤ 2 of 40 (≤ 5%).** All 40 per-pair predictions are FAIL; the bound of 2 absorbs the small number of flagged pairs where a broadly reactive target meets vaguely adjacent text.
2. **All 17 pilot-silent features fail.** These features scored 0.00 on all four of their own carefully matched prompts in the pilot; they are predicted to score at or near 0.00 on foreign prompts as well.
3. **Falsifier: ≥ 6 of 40 passing (≥ 15%) kills the instrument.** The threshold is not arbitrary. For a feature that fires at all on foreign text with activations unrelated to the should-fire/near-miss split, the chance that both should-fires land above both near-misses is 1 in 6 (the two should-fires must be the top two of four values), ≈ 16.7%. A permuted pass rate at or above ~15% is therefore indistinguishable from chance and would mean the protocol's verdicts carry no information about label–feature match.

Reading the outcome: 0–2 passes means the control succeeds and the pilot's 12/40 stands as a measurement of the labels. 3–5 passes is a gray zone — the passed pairs get inspected individually; if they concentrate in the flagged broadly reactive features, the binary rule needs a margin floor for high-reactivity features before further use. ≥ 6 passes triggers the falsifier above.

What this control cannot show: it validates the instrument, not any individual pilot verdict. A label that passed the pilot is not re-proven here, and a pilot failure is not re-litigated. It answers one question — does the test separate matched labels from mismatched ones?

## Estimated cost

Scoring is 40 features × 4 prompts = **exactly 160 activation calls** — one sixth of one 1000-calls-per-60-minutes API window, no pacing concerns. No mechanism probes are planned: a feature that is silent under permutation is the expected outcome, not a finding, so there is no autopsy budget. No other API use is planned.

## Lock procedure

1. Danny reviewed the design and predictions drafts and approved them as drafted. (Done November 14, 2026, ~11:57 AM ET.)
2. The approved files carry locked filenames, their SHA-256 hashes are computed, and the locked files are published to the GitHub repository (dcgleason/neuronpedia-label-validation) as the lock commit — **before any scoring**.
3. Only then is a run script written (reusing `checker/score.py`'s `Scorer`, asserting the locked derangement and the locked prediction tally before scoring) and the run executed.

Integrity note: at lock time, no feature in this design has been run through the activation API in its permuted pairing, and no activation calls at all were made during preparation.
