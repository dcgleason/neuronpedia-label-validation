# Study 2 — Can labels be made accurate? A bake-off of labeling methods

Designed Nov 13, 2026; revised Nov 14, 2026, to fold in the arm specs (study2-arm-specs.md). Follows Study 1 (Gemma 200 labels, 29.5% passed held-out testing) and the Llama replication (80 labels, 13.8% passed), both published in https://github.com/dcgleason/neuronpedia-label-validation

**Run framing.** This study runs in December on the public Neuronpedia stack. The faithful versions of Arm B, Arm F, and the dual scoring all need a corpus-scale activation cache, which the public stack does not provide; building one is a separate infrastructure project and is not on this study's path. The study therefore runs the closest named approximations and declares every one of them in "Deviations from published methods" below, in wording meant to be lifted directly into the pre-registration.

## The question

Study 1 showed the current labels fail. Study 2 asks whether a different way of *writing* labels produces labels that survive the same held-out test, on the same features, under the same pass rule.

## The proposed method (what this study tests)

"Validated labeling," a pipeline with four steps:

1. The label writer sees the full picture: strongest examples, weak examples, and text where the feature stayed off. (The arms split this step up: Arm B tests the activating-range part with activating examples only, matching the published method it is based on; contrast, in the form of observed failures, enters through Arm C.)
2. It drafts a label. Narrow labels are allowed and encouraged ("fires on the token btn in code" is a valid answer).
3. The draft label is tested on fresh held-out prompts, the Study 1 protocol, automatically.
4. If it fails, the writer sees exactly how it failed and revises once. The label ships with its test result attached, pass or fail, instead of shipping untested.

Arms B, C, and D below each isolate one piece of this pipeline, so the result shows which piece does the work.

## Arms (same features, same test, only the label-writing method changes)

- **Arm A — Baseline.** The current Neuronpedia label, retested with fresh prompts.
- **Arm B — Full-range examples (the published baseline, approximated).** The writer sees activating examples sampled across the feature's whole activation range instead of only the top ones. This is Paulo & Belrose's decile sampling, the known fix production labels ignore; in this study it is the strong published baseline to beat, not the novel claim. On this stack it runs as **Neuronpedia stored-example stratified sampling**: the feature's stored positives are de-duplicated, sorted by strength, split into 10 equal-frequency strata of the stored set's own ranks, and sampled at up to 4 per stratum, with shortfalls logged (no padding with duplicates, no backfilling from the top stratum). Delphi's non-CoT prompt shape; the explainer is the same model as every other arm, held fixed. Two honesty notes. The stored set is top-heavy (12 to 42 unique positives per feature, median 32), so the low strata are the low end of a dashboard sample, not true corpus deciles: if this arm loses, that does not refute decile sampling. And the published method shows the explainer no off examples, so this arm doesn't either. An earlier draft of this arm added off examples; that version was dropped rather than renamed and kept, because it confounds the one comparison this arm exists to make (sampling range vs. top-only) by mixing in a second treatment, contrast, and contrast is already tested on its own by Arm C's failure feedback. Full spec: study2-arm-specs.md §1.3.
- **Arm C — Feedback loop.** The writer starts from the current label, is shown its Study 1 failures (should-fires that stayed silent, near-misses that fired), and revises. (Prior-art note: feedback revision itself has prior art, from Bills et al. 2023 through SAEExplainer. The claim tested here is narrower: whether revision survives this protocol on the actual production labels.)
- **Arm D — Narrow-label instruction.** Same inputs as today (top examples only), with instructions to name the exact word form, register, or document structure when that is what the examples show, and to refuse a broad concept label the evidence does not support.
- **Arm E — Careful human (subset only, 20 features).** A person studies the feature's full activation data and writes the label by hand. Tests whether the bottleneck is the writer or the method.
- **Arm F — Verified selection (the SAEExplainer-style competitor, as an inference-time analogue).** The writer drafts several candidate labels for each feature, every candidate is tested, and the best-scoring candidate ships. This is the strongest published approach, added Nov 13 after the prior-art scan. SAEExplainer itself is a training pipeline (a vector-conditioned explainer, SFT, two rounds of DPO) that cannot run on this stack and was never run on Gemma-2-2B, so Arm F reproduces its selection rule at inference time: 6 candidates sampled at temperature 0.9 from the Arm B example prompt; for each candidate, 4 trigger texts written from the candidate text alone; each candidate scored by the maximum activation over its texts, via the checker's score.py (the paper's Eq. 7); the argmax ships, with all candidates and scores recorded. A feature where every candidate scores 0 ships the argmax anyway, flagged "no verified candidate." An optional round 2 rebuilds the candidate pool from the winner/loser pair (τ_diff = 0.1, τ_margin = 0.15) and reselects, the prompt-level analogue of the DPO rounds. Each candidate also gets a discrimination margin recorded (mean trigger-text activation minus mean near-miss-text activation): a named deviation from the paper's max-only score, added because max-only scoring rewards broad labels. Labels still ship by the paper's max score; how often the margin winner and the max winner disagree gets reported. Out of scope, stated plainly: vector conditioning, SFT, and DPO. Full spec: study2-arm-specs.md §2.3–2.4.

## Sample

60 Gemma layer-12 features. Correction to this design's original premise: only 120 of the 200 features tested in Study 1 are layer 12. The 40-feature pilot is all layer 12; the 160-feature scale-up is 80 layer 12, 40 layer 6, and 40 layer 18. Per the one-layer rule for the main run, the sample is drawn from the true 120-feature layer-12 pool:

- 40 that failed (25 silent of 49 available, 10 partial of 34, 5 near-miss-beat of 6)
- 20 that passed, of 31 available (checks the new methods do not break good labels)

The built sample is study2-sample-draft.md: a draft for review, not locked, hashed, or published.

Optional cross-model spot check: 20 failed Llama layer-16 features, Arms A and C only (appendix in the sample draft).

## Protocol (identical to Study 1, so results are comparable)

- For every label in every arm: 2 should-fire + 2 near-miss prompts, written from the label alone by a writer who has not seen activation data for that feature.
- Pass rule: min(should-fire) > max(near-miss).
- A pass/fail prediction for every label is written down, hashed (SHA-256), and committed to the public repo before any scoring runs.
- Prompt-sensitivity guard: the best-performing arm and the baseline get a second, independently written prompt set on the same features. A method only counts as better if it wins on both sets.

## Pre-registered predictions (to lock before the run)

- Arm A on the 40 failed features: 15% or fewer pass on fresh prompts.
- Arm B: at least 35% of the 40 pass. (Arm B as implemented here, stored-example stratified sampling; the prediction is about the approximation as run, not about true corpus decile sampling.)
- Arm C: at least 50% of the 40 pass (feedback is the strongest lever, per the Study 1 rewrite round, where 15 of 21 hand-revised labels passed).
- Arm D: beats Arm A, loses to Arm C.
- On the 20 already-passing features, no arm drops below 80% pass.
- If Arm C lands under 30%, the feedback idea is wrong and the pipeline claim gets dropped.

## Metrics

- Primary: pass rate per arm.
- Secondary: failure-class mix per arm, prediction accuracy per arm, cost per label (generation calls + activation calls), and Arm E vs the best automated arm on the 20-feature subset.
- Dual scoring: the finalist arms (best arm and baseline) also get scored under Paulo & Belrose's detection and fuzzing, so a win cannot be dismissed as an artifact of this study's pass rule. On this stack that runs at reduced scale, named **reduced detection/fuzzing (20 + 20, stored-set pools)**: per feature, one pool of up to 20 stored positives and 20 API-verified zero-activation negatives, built once and reused across arms (about 1,920 judge calls for the 120 finalist label instances). Per-label scores rest on 40 judged sequences, so they are coarse (2.5-point granularity); arm-level medians are the informative unit. These scores are explicitly not comparable to the paper's published numbers, which use 100 + 100 corpus sequences per feature.

## Cost and dependencies

- Activation calls: roughly 4,100 to 4,400 (corrected Nov 14 from the earlier 1,500–2,000 estimate, which predates Arm F and dual scoring). Breakdown: primary protocol scoring 1,280 (320 label instances x 4 prompts); finalist retest 480; Arm F selection, one round, 1,440; verified-negative pools for dual scoring, roughly 900 to 1,200. At the checker's self-limit of 950 calls per rolling hour, that is roughly five rolling windows of machine time. Costed options on top: Arm F round 2 adds about 1,440, and Arm F margin recording adds about 1,440 per round.
- Generation calls: Arms B, C, D, F, and the prompt writing run through the checker's Anthropic plug-in with Danny's API key, against his Console credits, with a hard spend cap in the runner (core generation estimated at $5–10). The dual-scoring judge calls (about 1,920) are a separate, minor LLM budget.
- Time: the sample is already built as a draft; locking the predictions is one short session. The run sits in December, inside the Thursday study blocks. Scoring is machine time. Danny's real cost is reviewing the design and the disagreements, same as Study 1.

## Phase 2 (only if Phase 1 works): does an accurate label help anyone do a job?

Detection task: given only the label, a fresh reader (human or model) picks which of 4 unseen texts activates the feature. Compare baseline labels vs winning-arm labels on accuracy. This is the downstream usefulness test, and it is also where close prior art exists (detection metrics), so Phase 2 cites it directly.

## Deviations from published methods (for the pre-registration)

The December run uses the public Neuronpedia stack. The following deviations from the published methods are declared in advance and apply to the run as a whole:

1. **Arm B example sampling (Paulo & Belrose / Delphi).** True decile sampling requires a corpus-scale activation cache, which the Neuronpedia API does not provide; the API serves only a small stored set of top activations per feature (12–42 unique positive examples per feature in the checker's cache, median 32). Arm B instead uses Neuronpedia stored-example stratified sampling: stored positives are de-duplicated, sorted by activation strength, split into 10 equal-frequency strata of the stored set's own ranks, and sampled at up to 4 per stratum, with per-stratum shortfalls logged and no padding or backfilling. Strata of a top-heavy stored set are not corpus deciles. A loss by Arm B does not refute decile sampling.
2. **Arm B explainer.** The published method uses Llama 3.1 70B Instruct as explainer. This study holds one explainer fixed across all arms, so Arm B's labels are written by the study's explainer, not Llama 3.1 70B Instruct. Arm B results are not numerically comparable to the paper's.
3. **Arm B inputs.** Following the published method, Arm B shows activating examples only. No off-example contrast variant is run. (An earlier draft of this design included off examples in Arm B; they were dropped because they confound sampling range with contrast, and contrast is tested separately by Arm C.)
4. **Arm F method (SAEExplainer).** The published method trains a vector-conditioned explainer (SFT plus two rounds of DPO) and was never run on Gemma-2-2B. Arm F is an inference-time analogue: candidate sampling from a prompted general LLM, verification scoring by the published Eq. 7 rule via the checker's score.py, pair construction with the published τ_diff = 0.1 and τ_margin = 0.15, one selection round plus an optional prompt-level second round. No vector conditioning, fine-tuning, or DPO is performed. The published τ_act validity filter is dropped: its values are specific to other SAEs, and no Gemma-2-2B value exists.
5. **Arm F margin recording.** For each Arm F candidate, a discrimination margin (mean trigger-text activation minus mean near-miss-text activation) is recorded alongside the published max-only score. This is a deviation from SAEExplainer's scoring, added because max-only scoring rewards broad labels. Labels still ship by the published max score; the rate at which the margin winner and the max winner disagree is reported. Shipping by margin instead would be a separate arm and is not done here.
6. **Dual scoring scale and scope (Paulo & Belrose detection/fuzzing).** Detection and fuzzing run at reduced scale — 20 activating and 20 non-activating sequences per feature, drawn from the Neuronpedia stored set plus API-verified zero-activation contexts — and are applied to the finalist arms only (best arm and baseline), not to every arm. Outputs are named "reduced detection/fuzzing (20 + 20, stored-set pools)." They are not comparable to the paper's published numbers, which use 100 + 100 corpus sequences per feature. The fuzzing set follows this study's recorded operational construction (activating examples with all truly activating tokens marked; non-activating examples marked on a matched number of tokens), because the paper does not print the article-version construction.
7. **Example-pool overlap.** The dual-scoring pools and Arm B's generation examples are drawn from the same small stored set, so they cannot always be kept disjoint, unlike the published pipeline's cache draws. The overlap per feature is recorded and reported.

## Honest limits

- One infrastructure gap shapes three pieces of this study: there is no corpus-scale activation cache on the public stack, so Arm B, Arm F, and the dual scoring run as named approximations, each declared in the deviations section above.
- Prompt sensitivity is real (the checker calibration disagreed with the hand protocol on 2 of 40, both prompt-sensitive). The two-prompt-set rule for finalists is the guard.
- One layer, one model for the main run. The Llama spot check says whether the winner travels.
- The explainer model is a choice, not a constant of nature. The study compares methods holding the explainer fixed, and says so.
- Division of labor stays stated in the writeup: prompts, labels, and predictions drafted with an AI research assistant, approved and locked by Danny before scoring.

## What would make this a field-level contribution

- A head-to-head, pre-registered comparison of labeling methods on identical features with an identical held-out test.
- A working open pipeline (the checker already does step 3) that any label publisher, including Neuronpedia, could run before shipping labels.
- Per-label test results published alongside labels, so "validated" becomes a visible property of a label rather than an assumption.

## Prior-art scan (Nov 13, 2026) — what exists, what is still open

Full scan: ~/workspace/anthropic-residency/study2-prior-art-scan.md

- Held-out predictive scoring is established prior art: Bills et al. 2023 (simulation scoring, plus counterexample-driven revision), Anthropic's own explanation evaluations (simulation on 100 features vs 100 neurons, no published failure rate for any shipped label set), Paulo & Belrose 2024 (detection and fuzzing, graded scores, never per-label pass/fail; their §4.2 already shows decile sampling beats top-only), SAEBench's autointerp metric (benchmarks SAEs, does not audit production labels).
- Direct neighbors for the bake-off: FADE (audits Neuronpedia's Gemma Scope descriptions, 103 features), Semantic Regexes (description-format comparison), "Revising and Falsifying" (NeurIPS 2025, close negatives + iterative explainer), SAEExplainer (2026 preprint, candidate generation + activation-verified selection on the same Gemma/Llama SAE families — the closest competitor), Gur-Arieh et al. 2025 (generates activating/neutral examples from the description), SPAR Fall 2025 manual audit (19 of 50 Delphi explanations failed human-judged criteria, n=50).
- Still open, per the scan: no per-label validation gate exists anywhere in production. Neuronpedia labels publish as generated; scores are opt-in, run on demand with the reader's own key. Nobody has published per-label pass/fail rates for the served labels, pre-registered binary predictions, or a cross-model-family audit using probes written from the label text alone with verdicts read from ground-truth activations and no LLM judge.
- Credibility requirements this adds to the design: score under detection/fuzzing as well as the pass rule (adopted for the finalists at reduced scale; see Metrics and Deviations from published methods); treat decile sampling as a baseline arm; keep n well above SPAR's 50; cite the neighbors above and state exactly how this protocol differs (label-authored probes, no LLM judge, binary per-label verdicts, production population).
