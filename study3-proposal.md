# Proposed Study 3: the evaluate–correct–retest loop, systematized

Status: proposed, not yet run. Nothing in this file is a result. The predictions below are stated in advance and will be locked and hashed, with the prompt sets, before any activation is scored — the same discipline as Studies 1 and 2.

## Why

Studies 1 and 2 established the base rates: 59 of 200 Gemma labels and 32 of 160 Llama labels passed a held-out test written from the label itself; corrected labels passed 15 of 21 where the originals passed 0 of 21; shuffled label–feature pairings passed 0 of 40 against 12 of 40 for the real pairings; a stronger explainer's labels passed 28 of 40 against the shipped labels' 12 of 40. The correction result is the one that does not scale by hand. Each corrected label took an autopsy: stored examples read token by token, probes written and run one variable at a time, a diagnosis, a rewrite, a locked retest. Study 3 asks whether that loop can be systematized without losing the two properties that made it trustworthy: scoring that never asks a model to judge a label, and corrections that say only what the evidence supports.

## The pipeline

**Stage 1 — Evaluate.** For each sampled label, generate should-fire and near-miss prompts from the label alone (near-misses change one variable at a time, as in the pilot), lock and hash the set, score the activations, and compute the margin: min(should-fire) − max(near-miss). A label passes if the margin is above zero — the registered rule throughout this repo.

**Stage 2 — Autopsy.** For each failure, gather the evidence the manual autopsies used: the feature's top-activating stored examples with their peak tokens, the label's theme counted across all stored examples rather than just the top few, and the cheap mechanism checks the autopsies produced — remove the keyword and retest; swap the register and keep the content; test at document length. Sort the failure into the five mechanisms found in Study 1 (word-form, register, displaced center of mass, document-structure bound, no consistent trigger), or mark it unclassified.

**Stage 3 — Correct, or decline to.** Where the evidence states a trigger, draft a corrected label that says only that: the token, the register, the narrowed topic. Where it does not — document-structure-bound features, features with no consistent trigger — the pipeline offers no corrected label and records the feature as unresolved, with the evidence attached. A system that invents a label for every failure would reproduce the original problem at scale.

**Stage 4 — Retest.** Fresh held-out prompts for every corrected label, written from the corrected label, locked and hashed before scoring, same pass rule. The standing prediction from the manual rewrite carries over: corrected labels pass. The run measures how often the systematized version keeps that promise.

**Stage 5 — Score.** Publish each label, original or corrected, with its margin as a trust score, plus the failure-mechanism breakdown for its layer and model. The deliverable is a label set where the "No Scores" marker is replaced by a measured number and, for failures, a named reason.

## Scale and scoring source

Target: thousands of features across layers in both model families, sampled with the seed fixed in advance. Neuronpedia's API is one scoring source; the models and SAEs are public weights, so the same activations can be computed locally (for example with SAELens). Local scoring is also what reopens the width question Study 1 had to close, because Neuronpedia does not serve inference for the wider Gemma SAEs. Local numbers enter the results only after the bridge validation the earlier attempt failed: on an overlapping sample, local and API activations must agree on magnitudes, not just token counts and peak positions, or the local arm closes unscored, like the width control did.

## Relation to existing tools

Automated interpretability pipelines already generate labels and score them with a model acting as judge (OpenAI's 2023 explainer-and-simulator setup; EleutherAI's Delphi; SAEBench's evaluations). This proposal differs in the scoring and in the loop: the verdict comes from activations under a locked rule, not from a judge model's rating, and evaluation is only the first stage — the pipeline goes on to diagnose, correct, and retest, with "unresolved" as a legitimate terminal state.

## Predictions to register before the run

Stated here in advance; the exact thresholds lock with the design file.

1. Systematized corrected labels will pass at a rate far above the original labels' rate on the same features, and at or below the manual rewrite's 15 of 21. The gap between the automated and manual rates is itself a result.
2. A substantial share of failures will terminate as unresolved rather than corrected, concentrated in the document-structure-bound and no-consistent-trigger mechanisms.
3. The automated mechanism sorter will agree with the 17 hand autopsies from Study 1 on most, not all, features. Disagreements get hand-checked and reported.

## What would change my mind

If corrected labels from the pipeline pass no better than the originals, the manual rewrite result was artisanal — a person reading evidence beats the systematized version — and the honest product is the trust score alone, without correction. If most failures sort as unresolved, the labels are worse than Study 1 suggested: not miswritten, but attached to features that do not have a statable trigger at all.
