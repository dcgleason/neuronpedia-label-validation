# Explainer swap — design note (LOCKED)

**Status:** LOCKED, November 14, 2026. Drafted November 14, 2026; approved as drafted by Danny Gleason on November 14, 2026 (~11:57 AM ET), before any scoring. Companion locked file: `explainer-swap-predictions-locked-nov14.md` (the 40 tests). The 40 new labels described here were generated during drafting (generation is part of drafting, not scoring — a label cannot be reviewed before it exists). No label in this arm has been scored, and no prompt in the companion file has been run through the activation API. This file must not be edited after locking.

## The question

Study 1's headline result is that Neuronpedia's served labels fail held-out testing most of the time: on the pilot's 40 Gemma-2-2B layer-12 features, 12 of 40 GPT-4o-mini labels passed. Every label in that result came from one explainer — GPT-4o-mini, a small, older model — writing from each feature's top-activating examples. So the result supports two different claims that the pilot cannot separate:

- **Auto-labels fail:** labels written by any explainer from top examples systematically overstate what features detect, because the evidence itself (top examples only) invites concept-shaped stories about form- and register-shaped features.
- **GPT-4o-mini labels fail:** this particular explainer is weak, and a stronger explainer shown the same evidence would write labels that survive testing.

The swap holds everything else constant — same 40 features, same kind of evidence, same test protocol, same pass rule — and changes the explainer to claude-sonnet-5-5. If the pass rate jumps, explainer quality is a major part of the pilot result. If it does not move, the failure lives in the labeling setup itself, and Study 2's method arms (feedback, verified selection) matter more than model choice. This is the "different explainer" variable from the November 14 variables list, run as a standalone Study 1 extension in the same style as the Llama multi-layer extension. It is not one of Study 2's lettered arms.

## Design

- **Features.** The pilot's 40 features, in pilot test order (`pilot-final-40.md`; model `gemma-2-2b`, source `12-gemmascope-res-16k`). Reusing the pilot sample is the point: every new label gets a paired comparison against a known GPT-4o-mini outcome on the same feature (12 pass / 17 silent / 6 partial / 5 near-miss-beat).
- **Explainer.** `claude-sonnet-5-5`, one call per feature, through the Anthropic connector helper (`anthropic_api.py generate`). The helper exposes no temperature control, so calls ran at the API's default sampling settings; that is recorded here rather than tuned. Maximum output was capped at 300 tokens; the longest reply used 190.
- **Explainer input (exactly what the model saw).** For each feature, the 10 highest-`maxValue` unique positive examples from the feature's stored Neuronpedia set (public feature API, via the checker's `fetch_feature()`; duplicates across the API's value bins removed by exact token sequence). Each example was shown as whole text with tokens of activation > 0 wrapped in `<< >>`, consecutive firing tokens grouped — the display format Paulo & Belrose's Delphi uses, and the closest documented standard for "show an explainer the top examples." Every pilot feature had at least 12 unique positives (range 12–42, median 32), so all 40 explainers saw the full 10. The instruction, identical for all 40 calls, asked for "a single short label for what the marked tokens have in common across these passages: one line, a plain noun phrase, roughly ten words or fewer," as specific as the evidence allows, with no mention of markers or passages, reply with only the label. Exact prompts are preserved in `explainer-swap/explainer_prompts.json`.
- **Blindness.** The explainer never saw the feature's existing Neuronpedia explanation (the prompt builder reads only the `activations` field of the feature response) and never saw any Study 1 result, prompt, or autopsy finding. Whatever the new labels get right about a feature's real trigger, they got from the examples.
- **Shipped labels.** The model's label ships unedited. A mechanical parse rule handles replies that were not a clean single line: an explicit trailing "Label:" line wins, else a fully bolded final line, else the first line verbatim. 37 of 40 replies were single-line and shipped verbatim; the rule changed the shipped text for idx 2625 and idx 3580, and restored closing quotation marks on idx 2580 and idx 4593. Raw generations and per-feature parse notes: `explainer-swap/generations_raw.json`; the rule itself: `explainer-swap/apply_parse_rule.py`.
- **Testing (at lock, not yet run).** Identical protocol and pass rule to the pilot: 2 should-fire + 2 near-miss prompts per label, each near-miss changing one variable, pass = min(should-fire) > max(near-miss). Prompts and per-label predictions were drafted by Muse and are pending Danny's approval, with the arm-level predictions and falsifier stated in the companion draft. Scoring is **40 × 4 = 160 activation calls**. No mechanism probes are specified; classifying the new labels' failures would be a separate decision (~8–10 calls per silent failure at pilot rates).
- **What the swap changes, stated plainly.** Relative to the original labeling, this arm changes the explainer model (GPT-4o-mini → claude-sonnet-5-5), the example presentation (Neuronpedia's pipeline format → Delphi-style `<< >>` marking of the top-10 stored examples), and carries one light instruction difference (an explicit "as specific as the evidence allows"). A win therefore supports the claim "a stronger current explainer, shown top examples in a standard marked format, writes labels that survive held-out testing more often." It does not isolate raw model quality from presentation format. Isolating those would take a second swap cell (GPT-4o-mini re-run in this arm's format), which is not proposed here.

## What the generated labels look like (drafting observation, not a result)

The 40 Sonnet labels are visibly narrower and more form-aware than the originals. Shown only the examples, the explainer independently re-derived several findings that Study 1 needed hand autopsies to reach: idx 5158 became "Bootstrap "btn" CSS class names in HTML button/link class attributes" (the autopsy: the feature is the code token "btn," prose "button" scores 0.0); idx 14719 became "The word "color" (or COLOR_ prefix) as a token" (autopsy: word-form detector for "color"); idx 8743 became "Continuation of a negated clause with "nor/or/no" coordination extending a negation" (autopsy: fires on "or"/"nor"). It also produced labels no prompt set can test (idx 2081 and 2625: document-boundary tokens) and at least one plausible overshoot into narrowness (idx 483: .NET namespaces, where the pilot showed the feature fires on prose). These observations motivated the companion draft's predictions; they are not evidence until the locked run scores them.

## Cost accounting

**Drafting (already spent, all of it Anthropic generation):**

| Item | Count |
|---|---|
| Explainer calls (one test call on idx 18, kept as that feature's generation; then the remaining 39) | 40 total, 0 wasted |
| Input tokens (API usage fields, summed) | 94,571 |
| Output tokens (API usage fields, summed) | 1,749 |
| Cost at claude-sonnet list prices ($3 / M input, $15 / M output) | **≈ $0.31** ($0.284 input + $0.026 output) |

The token counts are exact; the dollar figure applies list prices to them and is labeled an estimate for that reason. $0.31 is well under the $3 drafting cap for this task and about 1.6% of the $20 Anthropic balance reserved for study work. Neuronpedia-side drafting cost: 40 public feature GETs (keyless; several were already in the checker's cache) and **zero activation calls** — the rate-limited endpoint was never touched.

**Eventual scoring run (not yet run):** 160 activation calls (40 features × 4 prompts), inside one rate-limit window. Optional mechanism probes on failures are excluded and would be decided separately.

## Lock procedure

1. Danny reviewed the predictions draft and approved it as drafted, including the three arm-level predictions and the falsifier. (Done November 14, 2026, ~11:57 AM ET.)
2. The approved file carries a locked filename, its SHA-256 is computed, and it is published to the GitHub repository (dcgleason/neuronpedia-label-validation) as the lock commit — **before any scoring**. This design note carries a locked filename and is published alongside it.
3. Only then is a run script written (mirroring the replication's runner, same Scorer, asserting the locked prediction tally before scoring) and the run executed.

Integrity note: at draft time, no new-label prompt has been scored and no activation call of any kind has been made for this arm. The predictions were drafted by Muse with knowledge of Study 1's outcomes — disclosed in the companion file, as in prior arms — but the labels themselves were generated blind, by a model that saw only the features' stored examples.
