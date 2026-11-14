# Study 2 — Arm Specs: Arm B (Delphi decile sampling), Arm F (SAEExplainer-style verified selection), and dual detection/fuzzing scoring

Specs only. No experiments were run for this document. Written Nov 14, 2026, from the primary sources listed at the end. Anything that could not be verified from a primary source is marked **Unverified** inline and collected in the register at the end.

Companion documents: `study2-design-labeling-bakeoff.md` (the design these specs serve) and `study2-prior-art-scan.md` (the novelty scan).

---

## Bottom line

| Piece | Faithful version feasible on the current stack? | Feasible approximation? | Binding constraint |
|---|---|---|---|
| Arm B — Paulo & Belrose / Delphi decile sampling | **No.** Needs a corpus-scale activation cache. The Neuronpedia API serves only a small stored set of top activations per feature, not examples by activation decile. | **Yes**, with named changes: stratified sampling over the stored set's own ranks ("stored-set strata"), not corpus deciles. | No decile-addressable example supply. |
| Arm F — SAEExplainer-style verified selection | **No.** SAEExplainer is a training pipeline (vector-conditioned explainer, SFT, two rounds of DPO). None of that exists in the checker setup, and the paper never ran it on Gemma-2-2B. | **Yes**: inference-time verified selection — sample 6 candidates, score each by the activations of generated trigger texts, ship the argmax. 1,440 extra activation calls per selection round. | No trained explainer; candidate generation has to come from a prompt, not from the feature vector. |
| Dual scoring — Paulo & Belrose detection + fuzzing on every arm's labels | **No** at the paper's scale via Neuronpedia: the held-out ground-truth pools (100 activating + 100 non-activating corpus sequences per feature) cannot be built from the API. | **Yes** at reduced scale (20 + 20 sequences per feature): 5,760 judge calls for 360 label instances. Scores from the reduced version are **not** comparable to the paper's published numbers. | Same cache gap as Arm B. Judge dollars are minor; ground truth is the problem. |

**The single biggest implementation gap** (details in §5): there is no corpus-scale, decile-addressable activation cache anywhere in the current setup. The checker can score arbitrary text against a feature, but nothing can answer "give me held-out examples of this feature from each activation decile, plus random contexts where it is off, with per-token ground truth." That one gap blocks faithful Arm B and faithful dual scoring. Arm F's gap is separate (no training pipeline) and has a clean inference-time workaround.

### What the current stack actually provides (verified from the code and connector docs)

- `checker/score.py`: scores one feature on one custom text via `POST /api/activation/new`; returns the maximum token activation; disk-cached; self-limits to 950 calls per rolling 60 minutes (documented Neuronpedia limit: 1,000/60 min).
- `checker/generate.py`: generates Study 1 test prompts (2 should-fire + 2 near-miss) through the Anthropic Messages API (temperature 0.2 in the current template path; the underlying `_anthropic_messages` accepts a temperature argument), or loads externally written prompts. It does not generate labels from activation examples, and it has no Delphi or SAEExplainer modes.
- `checker/mechanisms.py`: `fetch_feature()` does the public `GET /api/feature/{modelId}/{sourceId}/{index}` and caches the response. This is the only example supply the checker currently touches.
- No component loads Gemma-2-2B or the SAE locally, caches corpus activations, samples examples by quantile, or runs an LLM judge.

---

## 1. Arm B — Paulo & Belrose / Delphi decile sampling

### 1.1 The published method, as a reproducible spec

Source: Paulo, Mallen, Juang & Belrose, "Automatically Interpreting Millions of Features in Large Language Models" (arXiv:2410.13928), and the Delphi `article_version` branch README (the branch the authors identify as the code used for the article).

**Activation collection (their pipeline, before any explaining happens)**

1. Run the subject model + SAE over a **10M-token sample of RedPajama-v2**, in contexts of **256 tokens** beginning with the BOS token.
2. For Gemma SAEs, discard activations on the BOS token (those SAEs were not trained on BOS activations).
3. The article-branch README's caching example uses `EleutherAI/rpj-v2-sample`, split `train[:1%]`, `ctx_len=256`, `n_tokens=10_000_000`, and recommends caching over at least 10M tokens.
4. The paper notes context length matters: at 256-token contexts, ~30% of latents in the 131k Gemma-2-9B SAE fire fewer than 200 times in 10M tokens. A feature needs a minimum pool of positive occurrences before decile sampling means anything (the article-branch `FeatureConfig` example uses `min_examples=200`, `max_examples=10000`).

**Explainer input (the part Arm B is testing)**

5. Explainer model: **Llama 3.1 70B Instruct**.
6. Show the explainer **40 activating examples**. Each example is **32 tokens**; the activating tokens can be at any position.
7. Examples are **sampled across the quantiles of the feature's activation distribution** (the paper follows Bricken et al. here; the stratified variant is the "decile sampling" condition). The article-branch `ExperimentConfig` example sets `n_examples_train=40`, `n_quantiles=10`, `example_ctx_len=32`, `train_type="quantiles"`. The direct operational reading is **4 examples per decile**. The paper's prose does not print the per-decile allocation explicitly — treat 4-per-decile as config-derived, not as a quoted sentence.
8. Only **activating** examples are shown. There are no non-activating examples in the generation prompt. (This matters for the design doc; see §1.5.)
9. Display format: the whole example is shown as natural text. Activating tokens are delimited with `<<` and `>>`, consecutive activating tokens grouped inside one pair of delimiters. After each example, an `Activations:` line lists each marked token with its strength.
10. The exact numeric rule for which tokens get marked (every token with activation > 0 vs. a threshold relative to the example's maximum) is **not stated in the paper**. The EleutherAI blog says the pipeline highlights max-activating tokens and optionally uses a threshold of the example's max activation. **Unverified:** the precise marking threshold in the article-version code.
11. Explainer sampling temperature is **not stated** in the paper sections read. **Unverified.**

**Explainer prompt structure (Appendix A.2, non-CoT version — paraphrased, not quoted)**

- System prompt, in substance: the model is a meticulous AI researcher studying patterns in language; it will receive text examples with selected words between `<< >>` delimiters; consecutive important tokens are grouped between one pair of delimiters; importance values are listed after each example; produce a concise description of the common pattern; do not focus on listing example tokens; do not mention the marker tokens; do not list multiple possible interpretations; keep it short; the final line must be the interpretation in the format `[interpretation]: ...`.
- Few-shot demonstrations follow, showing short examples with delimited spans and their activation tuples, ending in a formatted interpretation line. The paper's worked example uses idioms (a delimited span glossed with per-token strengths) and lands on a one-line interpretation.
- The target feature's 40 examples are then presented in the same format, and the text after `[interpretation]:` is the label.
- A CoT variant exists (three stages: list special words and patterns; write shared properties; formulate the interpretation). The paper's main experiments did **not** use CoT — it did not significantly help and cost more time. **Arm B spec: non-CoT.**

**What the paper found about this choice (§4.2, Appendix A.6.4–A.6.5; 500+-latent testbed, Llama 3.1 70B Instruct as explainer and scorer, 4-bit quantized in the ablations)**

- Median detection / fuzzing by generation-example sampling: randomly sampled 0.74 / 0.76; sampled from quantiles 0.74 / 0.77; top-only 0.72 / 0.73.
- Scores had largely saturated by 40 examples; 60 did not improve them.
- Top-only interpretations are narrower and more specific but lower-sensitivity. Stratified sampling can occasionally over-broaden.
- The paper's stated cost for this interpretation setup: about $200 per 1M latents with Llama 70B. Generation cost is not the constraint at Study 2's scale (60 labels).

### 1.2 What the Neuronpedia API can and cannot supply

The question the design turns on: can the API give examples **by activation decile** for a feature? **No.** Verified from the official docs and from inspecting actual feature responses:

- The docs describe the feature endpoint as returning a feature's "activations, explanations, logits, and density," and direct bulk users to the exports instead of per-feature API calls.
- The exports tree contains an `activations/` folder described as "**top activations** for each feature." The feature dashboard docs likewise call the panel "**Top Activations** — text where the feature fires the most."
- No decile, quantile, or activation-range query parameter is documented for the feature endpoint. **Unverified** in the strict sense that an undocumented parameter could exist; nothing in the docs, the exports structure, or the response schema offers one.
- What a feature response actually contains (inspected Nov 14, 2026, on the checker's own cache of 63 responses for `12-gemmascope-res-16k`, plus the live response for feature 18):
  - An `activations[]` array of **32–45 records** per feature. Each record has `tokens` (128-token contexts; the source metadata says `num_tokens_in_prompt: 128`, dataset `monology/pile-uncopyrighted`), per-token `values`, `maxValue`, and `maxValueTokenIndex`.
  - Records come in groups: one all-range group (`binMin=-1`, `binMax=maxActApprox`, always 20 records in this sample) plus five groups in **equal-width activation-value bins** spanning 0 to the feature's maximum, usually 5 records each and fewer for sparse features. Equal-width value bins are not deciles: deciles are equal-frequency, these are equal-range, and they are drawn from a top-heavy stored set.
  - Records **duplicate across groups** (the same context appears in the all-range group and in its value bin). After de-duplicating by token sequence, the 63 cached features have **18–45 unique sequences** and only **12–42 unique positive examples (median 32)**. **58 of 63 have fewer than 40 unique positives** — so even the raw count for a 40-example prompt is frequently unavailable, before any decile requirement.
  - The bin fields are not a reliable sampling contract: in the same cache inspection, 285 of 1,536 non-all-range records had a `maxValue` outside their stated `[binMin, binMax]` range.
  - A handful of zero-activation records appear (typically ~5, in the lowest bin). The endpoint does **not** provide a representative sample of random non-activating corpus contexts for a feature.
  - The response does include a 50-bar frequency histogram (`freq_hist_data_*`) and `frac_nonzero`, so the *shape* of the activation distribution can be estimated — but no example texts are attached to the low bars. A histogram cannot be shown to an explainer.
- Corpus mismatch, for the record: Neuronpedia's stored Gemma Scope activations come from `monology/pile-uncopyrighted` at 128-token contexts; Delphi's cache is RedPajama-v2 at 256-token contexts. (The paper's own dataset ablation, Appendix A.6.1, found RPJ-v2 vs. Pile made little difference to scores — median fuzzing 0.76 either way — so corpus choice is a second-order concern next to the decile problem.)

**Conclusion:** faithful decile sampling cannot be built on the Neuronpedia API. The API gives a truncated, top-heavy dashboard set. Any Arm B run on this stack is an approximation and must be named as one.

### 1.3 Arm B approximation spec (implementable on the current stack)

Name it in the writeup: **"Neuronpedia stored-example stratified sampling"** — Delphi's prompt and sampling *shape*, Neuronpedia's stored set as the universe.

1. Fetch the feature with `mechanisms.fetch_feature()` (public GET, cached). Use model `gemma-2-2b`, source `12-gemmascope-res-16k`.
2. Take `activations[]`. De-duplicate by exact token sequence, keeping the record with the highest `maxValue`.
3. Keep positives only (`maxValue > 0`). Log the unique-positive count per feature. If it is below 40, the feature ships with fewer examples — **do not pad with duplicates**; padding would fake decile coverage. (Expect this to bite: median unique positives in the cached sample is 32.)
4. Sort unique positives by `maxValue`. Split the sorted list into **10 equal-frequency strata** (stored-set strata). Sample up to **4 per stratum** with a fixed, recorded seed, for up to 40 examples. If a stratum has fewer than 4, take all of them and record the shortfall; do not backfill from the top stratum (backfilling re-introduces top-heaviness through the back door). Record the realized per-stratum counts in the run output.
5. For each selected example, extract a **32-token window** containing the max-activation token: deterministic rule — window start = `clamp(maxValueTokenIndex − 16, 0, len(tokens) − 32)`. Keep the per-token `values` for the window. (Delphi's exact window alignment is **unverified** from the paper prose; peak-centering is this study's recorded choice.)
6. Format each example as Delphi does: whole text; every token with value > 0 wrapped in `<< >>`, consecutive runs grouped; then an `Activations:` line listing each marked token with its value (raw values, rounded to 2 decimals — an implementation choice, flagged here because the paper's few-shot display uses small integers and does not specify a scaling).
7. Prompt: the non-CoT system prompt and few-shot structure from Appendix A.2 (described in §1.1), then the feature's examples. Parse the text after the final `[interpretation]:` as the Arm B label.
8. Explainer model — two tiers, pick one and name it in the writeup:
   - **Faithful tier:** Llama 3.1 70B Instruct (via OpenRouter or local vLLM). This is the paper's explainer.
   - **Study tier:** the same LLM used by every other generation arm in Study 2 (the checker's Anthropic plug-in; code default `claude-sonnet-5-5`, overridable via `CHECKER_MODEL`), temperature 0 for a single deterministic sample. This holds the explainer constant across arms, which the design doc already commits to ("the study compares methods holding the explainer fixed"). The cost of this tier: the arm is then "Delphi sampling with a Claude explainer," and its results cannot be compared numerically to the paper's.
9. Generation cost: 60 explainer calls (one per feature). Trivial next to everything else in this document.

### 1.4 What the approximation changes

- **The strata are quantiles of a truncated set, not of the corpus distribution.** The stored set was selected for a dashboard — it over-represents strong activations. The true lowest deciles of a feature's positive distribution (the many contexts where it fires weakly) are mostly absent, so the approximation's "low deciles" are the low end of a top-heavy sample. The treatment Arm B is supposed to test — seeing the feature's full range — is delivered only in weakened form.
- **Some features cannot fill the prompt.** With as few as 12 unique positives, a feature may get 12 examples across ragged strata. Per-feature example counts must be reported alongside pass rates, or Arm B's result will mix "sampling didn't help" with "sampling wasn't available."
- **Generation/test separation is weaker.** In Delphi, generation examples and scoring examples are disjoint draws from a large cache. Here, generation draws from the same small stored pool that any Neuronpedia-based scoring would draw from. Study 2's primary protocol (fresh authored prompts) is unaffected. Dual scoring is affected; see §3.5.
- If Arm B-approx wins, the honest claim is "stratifying the examples a label writer sees — even within Neuronpedia's stored top set — improves labels." If it loses, the honest claim is narrower still: the loss does **not** refute decile sampling, because true deciles were never shown.

### 1.5 Correction the design doc needs

The design doc's Arm B says the writer sees "top examples plus mid-strength **and off examples**." Paulo & Belrose's generation prompt contains **no off (non-activating) examples** — decile sampling is a statement about which *activating* examples to show. Adding off examples changes the treatment and confounds the comparison (sampling range vs. contrast). Two clean options:

- **Arm B (faithful shape):** activating examples only, per §1.3. Rename the design doc's current version **Arm B+contrast** and treat it as a separate variant if it is run at all.
- Do not describe the off-examples version as "Paulo & Belrose's decile sampling" in the writeup.

### 1.6 The faithful route (what it would actually take)

Install Delphi's `article_version` branch; load Gemma-2-2B with the Gemma Scope layer-12 16k SAE; cache activations over ≥10M tokens (article-branch example: `EleutherAI/rpj-v2-sample`, `train[:1%]`, 256-token contexts, BOS activations discarded for Gemma); build feature records with the article-branch `ExperimentConfig` (`n_examples_train=40`, `n_examples_test=100`, `n_quantiles=10`, `example_ctx_len=32`, `n_random=100`, `train_type="quantiles"`, `test_type="even"`); run `DefaultExplainer` with Llama 3.1 70B Instruct via local vLLM (GPU) or OpenRouter. This is a new pipeline with a GPU requirement, not an extension of the checker — but note that **building this cache is the same investment that unlocks faithful dual scoring** (§3). One infrastructure decision covers both.

---

## 2. Arm F — SAEExplainer-style verified selection

Source: He et al., "SAEExplainer: Interpreting SAE Features with Activation-Guided Preference Optimization" (arXiv:2606.08496, 2026 preprint, not peer-reviewed as of this scan). Code: https://github.com/he-jingyi/SAEExplainer

### 2.1 The published pipeline, extracted

SAEExplainer is **not** a prompting method. It trains an explainer LLM whose input is the SAE feature vector itself.

**Stage 0 — vector-conditioned explainer.** The input is $X^i = (x_{text}, v_i)$: a fixed instruction template containing a placeholder token `<ACT>`, plus the feature's decoder vector $v_i$. During the forward pass, $v_i$ is injected into the residual stream at the placeholder position, just after the second Transformer layer (Layer 1 in their indexing), norm-matched to the residual activation: $h'_p = h_p + \frac{\|h_p\|}{\|v_i\|} v_i$. The backbone must have the **same hidden dimension as the target model**, so the explainer is the instruction-tuned variant of the target itself (Gemma-2-9B target → Gemma-2-9B-IT explainer, and so on).

**Stage 1 — SFT warm-up.** Randomly sample $K_1$ feature vectors; use their existing **Neuronpedia explanations** as targets; LoRA fine-tune ($r=32$, $\alpha=64$, dropout 0.05, warmup ratio 0.03, learning rate $5\times10^{-5}$). $K_1$ by setting: 10,000 (Gemma-2-9B layers 20 and 31), 20,000 (Llama 3.1 8B layers 15 and 25), 40,000 / 20,000 (Gemma-2-27B layers 10 / 22).

**Stage 2 — mechanistic preference construction.** From the SFT explainer, sample $K_2$ **unseen** features ($K_2$: 5,000 for Gemma-2-9B; 10,000 for Llama 3.1 8B and Gemma-2-27B). For each feature:

- Sample **$M = 6$ candidate explanations** at temperature **0.9**.
- For each candidate, a separate Generator LLM synthesizes **$W = 4$ text samples** intended to manifest the candidate's semantics.
- Score each candidate by the **maximum target-feature activation over its generated texts**: $s(e_j^m) = \max_{t \in T_j^m} a_t$.
- A feature is valid for preference construction only if its best candidate score reaches an activation threshold $\tau_{act}$ **and** the relative spread across candidates reaches $\tau_{diff} = 0.1$. ($\tau_{act}$ is scale-specific per model/layer: 10 and 15 for Gemma-2-9B layers 20/31; 1 and 5 for Llama layers 15/25; 50 and 100 for Gemma-2-27B layers 10/22. **No value exists for Gemma-2-2B** — the paper never ran this target.)
- Positive: the highest-scoring candidate. Negative pool: candidates scoring lower than the positive by a relative margin of at least $\tau_{margin} = 0.15$. Negative: the **highest-scoring** candidate inside that pool (a hard negative); if the pool is empty, the lowest-scoring candidate.

**Stage 3 — two rounds of DPO.** Round 1: policy and reference both start from the SFT model; $\beta = 0.1$, learning rate $5\times10^{-6}$. Round 2: the DPO-1 model generates a fresh on-policy preference dataset (same $K_2$ features, except Gemma-2-27B layer 10, which resampled 10,000); policy/reference start from DPO-1; $\beta = 0.15$, learning rate $3\times10^{-6}$.

**Compute reported:** a single NVIDIA A100; 40 GB VRAM for the 8B/9B explainers, 80 GB for 27B; SFT ≈ 1 hour and one DPO round ≈ 1 hour for the 8B/9B models; preference-dataset construction ≈ 3–4 hours per round; 27B roughly double.

**Evaluation.** 300 unseen features per layer. Downstream evaluation model: `gpt-5.4-mini` (as named in the preprint). Metrics:

- **Generative Accuracy:** a Generator LLM writes $N = 10$ novel sentences from the explanation alone; the score is the fraction whose maximum token activation exceeds 50% of the feature's cached maximum activation (cached max retrieved from Neuronpedia). Evaluation prompts were isolated from preference-construction prompts.
- **Input Score:** the evaluator generates 5 activating and 5 neutral examples from the explanation; the explanation passes if mean max-activation of the activating set exceeds the neutral set's. (Reported as a percentage over features.)
- **Output Score:** generate text while amplifying the target feature vs. two random control features; a judge LLM picks which of the three randomized text sets matches the explanation; pass if it picks the target's.
- **Discriminative Activation Metrics:** $A_{high}$, $A_{low}$, $\Delta A = A_{high} - A_{low}$ over generated high-/low-activation sample sets.

**Unverified from the HTML extraction:** the exact prompt texts. Appendix G lists prompt section headings (SFT, preference generation, generative evaluation, input metric, output metric) but the bodies were not exposed in the HTML rendering. The identity of the Generator LLM used in preference construction is likewise **not named** in the extracted text.

**Reported results vs. Neuronpedia's default GPT-4o-mini explanations** (the paper's "Neuronpedia" baseline is the default explanation set, which the paper states was generated by GPT-4o-mini; values are percentages, Generative Accuracy / Input Score / Output Score):

| Target | SAEExplainer | Neuronpedia (GPT-4o-mini) | Difference (points) |
|---|---|---|---|
| Gemma-2-9B, layer 20 (Gemma Scope res-16k) | 46.13 / 77.33 / 71.00 | 21.03 / 62.67 / 62.67 | +25.10 / +14.66 / +8.33 |
| Gemma-2-9B, layer 31 | 54.50 / 84.33 / 72.33 | 27.77 / 70.33 / 57.33 | +26.73 / +14.00 / +15.00 |
| Llama 3.1 8B, layer 15 (Llama Scope res-32k) | 58.40 / 68.00 / 76.00 | 33.93 / 49.00 / 69.33 | +24.47 / +19.00 / +6.67 |
| Llama 3.1 8B, layer 25 | 52.33 / 77.67 / 77.00 | 27.87 / 56.00 / 69.00 | +24.46 / +21.67 / +8.00 |

Paired bootstrap on Llama layer 15 (Appendix E.2): Generative Accuracy +24.5 (95% CI [20.2, 28.8], $p<0.0001$); Input Score +19.0 (CI [13.7, 24.3], $p<0.0001$); Output Score +6.7 (CI [0.7, 12.7], $p=0.0358$). Ablation prose: DPO round 1 alone raised Generative Accuracy by 26% and Input Score by 20.33 points on that layer, with further gains after round 2. Human evaluation (Appendix F): SAEExplainer 43.67/50 vs. Neuronpedia 31.00/50 average correct judgments.

**Transfer limits, stated plainly:**

- SAEExplainer was evaluated on Gemma-2-9B, Gemma-2-27B, and Llama 3.1 8B. **Never on Gemma-2-2B**, which is Study 2's target (`12-gemmascope-res-16k`). No trained SAEExplainer exists for this target, and the published gains do not transfer as numbers.
- Its metrics (Generative Accuracy / Input / Output) are not Study 1's pass rule. Any Arm F label still has to survive Study 2's own protocol; cross-paper numeric comparisons are not valid.

### 2.2 What Danny's setup can and cannot reproduce

**Can reproduce** (with new code on the existing stack — the pieces exist):

- Multiple candidate labels per feature, sampled from an LLM at temperature 0.9 (the checker's Anthropic plug-in accepts a temperature argument, even though the Study 1 template path uses 0.2).
- Per candidate, $W = 4$ generated trigger texts from a Generator prompt.
- Candidate scoring exactly as in the paper's Eq. 7: score each text with `score.py` (its returned value is the maximum token activation, matching $a_t$ as used here), candidate score = maximum over its 4 texts.
- Winner/loser pair construction using the paper's $\tau_{diff} = 0.1$ and $\tau_{margin} = 0.15$.
- A second, on-policy-flavored round: feed the winner/loser pair and their scores back into a prompt, sample fresh candidates, rescore, ship the overall argmax. This mimics the *structure* of the two DPO rounds (regenerate from an improved starting point, reselect) without any weight updates.
- Final evaluation of shipped labels under Study 1's pass rule and, if built, dual scoring.

**Cannot reproduce:**

- **The vector-conditioned explainer.** No local model, no residual-stream injection. (For this source, the inspected feature response also reports `hasVector: false` with an empty `vector` list, so the decoder vector is not even supplied by the API response — moot, since an API LLM could not consume it the way the method requires anyway.)
- **SFT** on 10,000–40,000 Neuronpedia-labeled features, and **both DPO rounds** (LoRA training, A100-class compute, a training stack that does not exist in this setup).
- **The trained weights' candidate distribution.** SAEExplainer's candidates come from a model trained on thousands of features. Danny's candidates come from a prompted general LLM. Same selection rule, different candidate pool — this is the core sense in which Arm F is an analogue, not a reproduction.
- **The paper's exact prompts** (Appendix G bodies unverified, §2.1) and its exact Generator LLM (unnamed in the extracted text).
- In principle the method could be trained for Gemma-2-2B (Gemma-2-2B-IT shares the 2304 hidden dimension), but that is a research project of its own — SFT data construction, local Gemma-2-2B + SAE inference for preference scoring, two DPO rounds — wildly disproportionate to labeling 60 features, and it is not what Study 2's Arm F can claim.

### 2.3 Closest faithful approximation: inference-time verified selection

Name it in the writeup: **"SAEExplainer-inspired verified selection (inference-time, no training)."**

Per feature:

1. **Candidate generation.** Show the LLM the same stratified stored-example prompt as Arm B (§1.3) — the fullest evidence available on this stack, standing in for the vector input. Sample **$M = 6$ candidates as 6 separate calls at temperature 0.9** (the paper samples candidates; one call asking for a list of 6 is not sampling and would be a recorded deviation).
2. **Trigger generation.** For each candidate, one Generator call produces **$W = 4$ texts** intended to make the feature fire, written from the candidate text alone.
3. **Verification.** Score all 24 texts with `score.py`. Candidate score $s(e) = \max$ activation over its 4 texts (paper Eq. 7, unchanged).
4. **Selection.** Ship the argmax candidate as the Arm F label. Record all 6 candidates and scores in the run output.
5. **Silent-feature rule.** Study 2's sample includes 25 previously silent features; for some, every candidate may score 0. Ship the argmax anyway (ties broken by candidate order) and flag the feature "no verified candidate." Do not silently drop these features — they are the population the study is about.
6. **Optional round 2 (the DPO analogue).** Build the paper's pair: positive = argmax; negative = highest-scoring candidate at least 15% below the positive ($\tau_{margin} = 0.15$), else the lowest-scoring candidate. Only proceed if the relative spread across candidates is at least $\tau_{diff} = 0.1$. Prompt the LLM with the pair and their scores, sample 6 fresh candidates, repeat steps 2–4, and ship the overall argmax across both rounds. **Deviation flagged:** the paper's $\tau_{act}$ validity filter is dropped — its values are scale-specific to other SAEs and no Gemma-2-2B value exists.
7. The shipped label then goes through the standard Study 2 protocol (fresh authored prompts, locked prediction, pass rule) like every other arm.

**Counts (activation calls are the scarce resource; the checker caps itself at 950/rolling hour):**

| Stage | Per feature | 60 features |
|---|---|---|
| Candidate sampling (LLM calls, temp 0.9) | 6 | 360 |
| Trigger-text generation (LLM calls) | 6 | 360 |
| Trigger scoring (activation calls) | 6 × 4 = 24 | **1,440** |
| Optional round 2 (all of the above again) | 24 activation + 12 LLM | **+1,440 activation**, +720 LLM |
| Final Study 1-protocol test of shipped labels | 4 | 240 (already inside the bake-off's primary budget, §4) |

One selection round (1,440 uncached calls) spans at least two rolling rate-limit windows; two rounds (2,880) span roughly four. That is machine time, and it is affordable — but it makes Arm F the most expensive arm in the study by an order of magnitude, which belongs in the design doc's cost section.

### 2.4 Known weakness of the faithful score, and the guarded variant

The paper's candidate score is **maximum activation only**. A broad label ("text about food") can win by producing one text that fires hard, even if it also fires on everything else. SAEExplainer's training can absorb that because DPO contrasts candidates across thousands of features; a one-shot selection on 60 features cannot. Study 2 should therefore also record, for each candidate, a **discrimination margin**: generate 4 neutral/near-miss texts per candidate alongside the 4 trigger texts, and compute (mean trigger max) − (mean neutral max). Ship by the paper's max score (that is the faithful arm), but report how often the max-score winner and the margin winner disagree. A variant that ships by margin is a **deviation** — it borrows the logic of SAEExplainer's Input Score *evaluation*, not its preference-construction score — and if it is ever run as an arm it must be named separately (e.g., Arm F-margin). Cost of recording margins: +24 activation calls per feature per round (+1,440 per round across 60 features).

---

## 3. Dual scoring — Paulo & Belrose detection and fuzzing on every arm's labels

The prior-art scan's credibility requirement: every arm's labels get scored under the incumbents' graded metrics as well as Study 1's binary pass rule, so a win cannot be dismissed as metric choice. Here is what that operationally requires.

### 3.1 The two metrics (paper §3.3.1–3.3.2, Appendices A.4.1–A.4.2)

- **Detection (sequence level).** The judge is given one label and a shuffled group of **5 whole sequences**, with no tokens highlighted. For each sequence it returns 1 ("this sequence activates the latent, given the interpretation") or 0, as a Python list of 1/0 values, one per example, and nothing else. It measures precision + recall of the label at the context level; the judge does not need to localize the activating token. Prompt structure (paraphrased): the judge is a meticulous linguistics researcher; it is given a latent description and several text examples; it decides which examples possess the latent; few-shot demonstrations precede the target group.
- **Fuzzing (token level).** Same shape, but each example has some tokens delimited with `<< >>`. The judge returns 1 for an example only if **every** delimited token is correctly marked — i.e., every marked token is genuinely representative of the latent. A mix of correctly and incorrectly marked examples is the point. Also 5 shuffled examples per call, Python-list output.
- **Scoring:** per label, the score is the judge's accuracy against ground truth across all judged examples (the paper reports distributions/medians across latents). Fuzzing had the highest correlation with human judgments in the paper (Spearman ρ = 0.69; simulation 0.60; detection 0.59).
- **Judge model:** **Llama 3.1 70B Instruct** for detection, fuzzing, and simulation (Appendix A.4.6). Several ablations used the 4-bit-quantized version. The paper found scorer choice moves scores: a smaller Llama 8B scorer gave lower scores, while Claude Sonnet 3.5 and Llama 70B gave similar detection/fuzzing distributions. Scores from a different judge are therefore **not** the paper's scores, even with identical examples.
- Judge temperature is **not stated** in the paper sections read. **Unverified.** This study should set temperature 0 and record the choice.

### 3.2 Ground truth: where the sequences come from

Both metrics are judged against **corpus ground truth from an activation cache** — the same cache used for generation, with train/test separation:

- **Activating pool (per feature):** held-out contexts where the feature's activation is > 0, stratified across the activation distribution. For the paper's design-choice testbed (§4.2) and its score-correlation analysis (Appendix A.4.6), each latent is scored on **100 activating examples — 10 from each of the 10 activation deciles — plus 100 non-activating examples**. The article-branch config matches this shape: `n_examples_test=100`, `n_random=100`, `test_type="even"`, and the sampler keeps test examples disjoint from the explainer's training examples.
- **Non-activating pool (per feature):** random corpus contexts in which this feature's activation is exactly 0 in the cache.
- **Detection items:** the pools as-is, unmarked, ground truth = activating or not.
- **Fuzzing items:** activating examples with their truly activating tokens delimited (correctly marked), plus incorrectly marked examples. **The paper does not print the exact correct/incorrect construction for the article-version scorer. Unverified.** The EleutherAI blog describes the earlier Experiments-branch construction: 7 activating examples per decile, 5 correctly marked and 2 incorrectly marked per decile (70 total), where an incorrectly marked example has N non-activating tokens delimited, N set to the average number of marked tokens across examples. The blog's scale conflicts with the paper's 100 + 100 pool, so neither source alone settles the article-version fuzzing set. **Operational definition adopted for Study 2 (recorded as this study's choice, following the paper's pool sizes and the blog's marking method):** fuzzing set = the 100 held-out activating examples with all truly activating tokens (value > 0) delimited, plus the 100 non-activating examples with delimiters placed on the same number of tokens as the median correctly marked count for that feature. Ground truth: activating = correctly marked (1), non-activating = incorrectly marked (0).

Building these pools **once per feature and reusing them across all six arms** is essential and legitimate: the pools depend only on the feature, not the label. Only the label text inside the judge prompts changes per arm. Judge calls still scale with label instances (360), not features (60).

**Why Neuronpedia cannot supply these pools:** §1.2. The stored set offers a median of 32 unique positives per feature (paper scale needs 100 held-out positives *plus* Arm B's generation examples, disjoint), and ~5 zero-activation records (paper scale needs 100 random negatives). Negatives could in principle be manufactured — draw random Pile texts and verify each is zero with one `/api/activation/new` call (~100 calls per feature, 6,000 total, feasible) — but positives cannot: a sparse feature fires in well under 1% of random contexts (`frac_nonzero` for feature 18 is 0.00283), so random search for 100 fresh positives per feature, let alone stratified by decile, is not a plan.

### 3.3 Call counts for 60 features × 6 arms (360 label instances)

The paper presents two scales, so both are costed, plus the reduced Neuronpedia-feasible scale from §3.5. All scenarios group 5 sequences per judge call, per the paper.

| Scenario | Sequences per label per scorer | Judge calls per label (both scorers) | **Total judge calls (360 labels)** | Sequence presentations |
|---|---|---|---|---|
| **P — paper testbed scale** (§4.2 / A.4.6: 100 activating + 100 non-activating) | 200 | 40 + 40 = 80 | **28,800** | 144,000 |
| **T — Table 1 scale** (the paper's token-cost table is normalized to 100 contexts per scorer) | 100 | 20 + 20 = 40 | **14,400** | 72,000 |
| **R — reduced, Neuronpedia-feasible** (§3.5: 20 + 20) | 40 | 8 + 8 = 16 | **5,760** | 28,800 |

Notes on the scenarios:

- Scenario P is the defensible headline number: it matches the pool sizes the paper states in prose for latent scoring. Scenario T exists because Table 1's token accounting is normalized to 100 contexts; which of the two the authors' released scorer used per latent in each experiment is **not fully settled by the paper text**. Report the scenario used, by name.
- Token volume, scaled from Table 1 (per 100 contexts: detection 17.0k input / 240 output tokens; fuzzing 19.6k input / 249 output): Scenario P ≈ **26.4M input tokens** and ≈ 0.35M output tokens across all 360 labels. Scenario T ≈ 13.2M input. Scenario R ≈ 5.3M input.
- Historical dollar scale, from Table 1's own per-100k-latent estimates (2024-era prices, **not current quotes**): Scenario P ≈ $9 with Llama 70B, ≈ $84 with Claude Sonnet 3.5, for all 360 labels. Judge inference is cheap *at the paper's assumed prices*; current OpenRouter pricing for Llama 3.1 70B Instruct is **unverified** in this document.
- Arm E adjustment: the design runs Arm E on only 20 features, so the true label-instance count is 320, not 360. Scenario P at 320 instances = 25,600 judge calls. The 360 figures above follow the requested 6 × 60 denominator and are the conservative upper bound.
- Ground-truth construction (one-time, shared across arms): Scenario P needs 60 × 200 = **12,000 held-out sequences** with token-level ground truth (6,000 activating, stratified; 6,000 non-activating), disjoint from Arm B's 40 generation examples per feature. Scenario R needs 60 × 40 = 2,400.

### 3.4 Judge access and cost/access flags, plainly

1. **The judge is the easy part; the pools are the hard part.** 28,800 judge calls sounds large, but at paper-era prices the inference itself is on the order of $10–$85. The blocker is that Scenario P/T pools cannot be built without the Delphi cache (§3.2). Dual scoring at paper scale and faithful Arm B stand or fall on the **same** infrastructure decision (§1.6).
2. **Access routes for a Llama 3.1 70B Instruct judge:** (a) local vLLM — needs a GPU that can serve a 70B model (the Delphi README's examples run 70B-class models via vLLM or OpenRouter; exact VRAM for a given quantization is **unverified** here); (b) OpenRouter API — Delphi's clients support it, and Neuronpedia's own `eleuther_fuzz` / `eleuther_recall` scorers also require an OpenRouter key per the docs. Danny's checker currently has **no judge client at all**; its only LLM plug-in is Anthropic.
3. **Substituting a Claude judge** is technically trivial (the plug-in exists) and the paper's own comparison suggests detection/fuzzing distributions would be broadly similar — but the results must then be reported as "detection/fuzzing-style scores with a Claude judge," not as Paulo & Belrose scores. Within-study arm comparisons remain valid because the judge is held constant.
4. **Neuronpedia's built-in Eleuther scorers are not a shortcut this spec can rely on.** The docs confirm `eleuther_fuzz` and `eleuther_recall` exist and need an OpenRouter key. **Unverified:** whether they accept arbitrary user-supplied explanations (all six arms' labels) at API scale, which example pools they draw from, and whether those pools are held out from anything. Treat them as a lead to check, not infrastructure.
5. **Call-volume mechanics:** 28,800 judge calls is a substantial API workload regardless of price — concurrency limits, retries, and parse failures (the judge must return a clean Python list) need engineering. Budget a parse-failure rate and a re-ask policy in the runner; do not silently drop malformed responses, or per-label n will vary invisibly.

### 3.5 Reduced dual scoring (feasible on Neuronpedia, honestly labeled)

Per feature:

- **Activating pool:** up to 20 unique stored positives, drawn as 2 per stored-set stratum where available (features with fewer unique positives ship fewer; record n). Keep them disjoint from Arm B's generation examples where the stored pool allows — with a median of only 32 unique positives, full disjointness at 20 + up-to-40 is often impossible; record the actual overlap per feature.
- **Non-activating pool:** 20 contexts verified zero for this feature: start from the feature's stored zero-activation records (~5 available), fill the remainder with random texts scored once each via `/api/activation/new` and kept only if the max activation is exactly 0. Expected extra activation calls: roughly 15–20 per feature, ≈ 900–1,200 total.
- **Fuzzing items:** activating examples with all value->0 tokens delimited; non-activating examples delimited per §3.2's operational rule.
- **Judge calls:** Scenario R — 5,760 for 360 label instances.
- **Naming and comparability:** call the outputs "reduced detection/fuzzing (20 + 20, stored-set pools)." With 40 judged sequences per label, a label's score has a granularity of 2.5 points and wide per-label uncertainty; arm-level medians over 60 features are still informative. These scores **cannot** be placed next to the paper's published medians as if they were the same measurement.

---

## 4. Revised Study 2 call budget (all-in)

The design doc's cost section predates Arm F and dual scoring. Corrected totals:

| Component | Activation calls (Neuronpedia) | LLM calls |
|---|---|---|
| Primary Study 1-protocol scoring: 320 label instances (5 arms × 60 + Arm E × 20) × 4 prompts | 1,280 | prompt-writing ≈ 320 |
| Finalist retest: best arm + baseline, second prompt set (2 × 60 × 4) | 480 | ≈ 120 |
| Arm B generation | — | 60 |
| Arm F selection, one round (§2.3) | 1,440 | 720 |
| Arm F selection, optional round 2 | +1,440 | +720 |
| Arm F margin recording (optional, §2.4) | +1,440 per round | +360 per round |
| Reduced dual scoring: negative-pool verification (§3.5) | ≈ 900–1,200 | — |
| **Total, one-round Arm F, no margins, reduced dual scoring** | **≈ 4,100–4,400** | ≈ 1,220 |
| Dual scoring judge calls (separate budget; §3.3) | — | 5,760 (R) / 14,400 (T) / 28,800 (P) |

Excluded: mechanism-sorter probes on failures (Study 1's checker used 493 extra calls for 51 silent features; Study 2's count depends on how many labels fail). At the checker's 950-calls-per-rolling-hour self-limit, the one-round total above spans roughly five rolling windows of machine time. Generation/judge LLM costs are small at these volumes; Danny's review time remains the real cost, as in Study 1.

---

## 5. The single biggest implementation gap, and the decision it forces

**Gap:** no corpus-scale activation cache. Everything faithful in Paulo & Belrose — decile-sampled generation examples, held-out stratified scoring pools, random non-activating contexts with token-level ground truth — is a query against a cache of SAE activations over millions of corpus tokens. The current stack has exactly two data sources: a per-feature dashboard response (32–45 stored records, top-heavy, duplicated) and a custom-text scorer (one text at a time, rate-limited). Neither can express a decile.

**The decision it forces** (one decision, three consequences):

- **Build the Delphi cache** (§1.6: Gemma-2-2B + Gemma Scope L12, ≥10M tokens, GPU for caching and optionally for the 70B judge/explainer, or OpenRouter for the LLM side). Then Arm B is faithful, dual scoring can run at Scenario P/T, and generation/test separation is clean.
- **Or don't build it**, and run the named approximations: Arm B as stored-set stratified sampling (§1.3), Arm F as inference-time verified selection (§2.3), dual scoring at Scenario R (§3.5). The study remains coherent — its primary metric is still the ground-truth pass rule, which needs none of this — but every Delphi-flavored number must carry its approximation name, and no result can be stated as a refutation or confirmation of Paulo & Belrose's decile result.

Arm F is the exception: its gap (no training pipeline) does not force a build decision, because the inference-time analogue preserves the paper's selection rule and scoring equation exactly, and its limits can be stated in one sentence — same selection, untrained candidate pool.

---

## Sources

Primary sources, accessed Nov 14, 2026:

- Paulo, Mallen, Juang & Belrose, "Automatically Interpreting Millions of Features in Large Language Models." Abstract: https://arxiv.org/abs/2410.13928 · Full text: https://arxiv.org/html/2410.13928v2 (ICML 2025 version: https://proceedings.mlr.press/v267/paulo25a.html)
- Delphi code, article branch (identified by the authors as the code used for the article): https://github.com/EleutherAI/delphi/tree/article_version
- EleutherAI blog, "Open Source Automated Interpretability for Sparse Autoencoder Features": https://blog.eleuther.ai/autointerp/
- He et al., "SAEExplainer: Interpreting SAE Features with Activation-Guided Preference Optimization." Abstract: https://arxiv.org/abs/2606.08496 · Full text: https://arxiv.org/html/2606.08496 · Code: https://github.com/he-jingyi/SAEExplainer
- Neuronpedia docs — API: https://docs.neuronpedia.org/api-and-data/api · Exports: https://docs.neuronpedia.org/api-and-data/exports · Feature dashboards: https://docs.neuronpedia.org/sparse-autoencoders/feature-dashboards · Auto-interp: https://docs.neuronpedia.org/sparse-autoencoders/auto-interp
- Live feature response used for the §1.2 inspection: https://www.neuronpedia.org/api/feature/gemma-2-2b/12-gemmascope-res-16k/18 , plus the checker's local cache of 63 feature responses for the same source (`checker/cache/`), inspected Nov 14, 2026.

Local documents and code: `study2-design-labeling-bakeoff.md`; `study2-prior-art-scan.md`; `checker/score.py`, `checker/generate.py`, `checker/mechanisms.py`, `checker/README.md`; `~/workspace/custom-connectors/custom.neuronpedia/CONNECTOR.md`.

## Unverified register

Everything below is used in this spec only as flagged, or not relied on at all:

1. The exact token-marking threshold in Delphi's article-version explainer (paper states the display format, not the threshold; the blog describes max-token highlighting with an optional relative threshold).
2. Delphi's exact 32-token window alignment (peak-centered vs. other) and the explainer's sampling temperature — not stated in the paper sections read. §1.3 records this study's choices instead.
3. The per-decile allocation of the 40 generation examples (4/decile is the direct reading of `n_examples_train=40` + `n_quantiles=10` + `train_type="quantiles"` in the article-branch config; the paper prose does not state it).
4. The exact correct/incorrect example construction in the article-version fuzzing scorer, and whether each latent's detection/fuzzing pool in every experiment was 200 sequences (paper §4.2 / A.4.6 prose) or 100 (Table 1's normalization). §3.2 adopts a recorded operational definition; §3.3 costs both scales.
5. SAEExplainer's Appendix G prompt bodies (headings only in the HTML rendering) and the identity of its preference-construction Generator LLM.
6. Whether Neuronpedia's built-in `eleuther_fuzz` / `eleuther_recall` scorers accept arbitrary user-supplied explanations at API scale, and which example pools they use.
7. Current (Nov 2026) pricing and rate limits for Llama 3.1 70B Instruct via OpenRouter or any host. All dollar figures in §3 are the paper's 2024-era estimates, scaled.
8. VRAM required to self-host Llama 3.1 70B Instruct under a given quantization for vLLM judging/explaining.
9. The §1.2 cache statistics (record counts, unique positives, bin inconsistencies) are an inspection of 63 cached responses for one source, not a documented Neuronpedia guarantee; they describe what this study would actually be working with, and could differ for other sources or after platform changes.
