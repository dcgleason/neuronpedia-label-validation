# Study 2 Prior-Art / Novelty Scan: SAE Feature Label Quality

**Purpose.** Before proposing an "improved labeling methods bake-off," check what already exists on (a) how autointerp labels are generated and scored, (b) published label failure rates, and (c) head-to-head comparisons of label-generation methods. The user's completed study (published, github.com/dcgleason/neuronpedia-label-validation) audited the production Neuronpedia labels for Gemma-2-2B (12-gemmascope-res-16k) and Llama 3.1 8B (16-llamascope-res-32k): for each label, 2 "should-fire" prompts and 2 near-miss prompts were authored from the label text only, per-label pass/fail predictions were pre-registered, and a label passed only if both should-fires activated above both near-misses in ground-truth model activations. Result: 59/200 (29.5%) pass on Gemma, 11/80 (13.8%) pass on Llama.

**Scan date:** Nov 13–14, 2026. Sources are papers, lab publications, and platform docs, cited inline. Preprints dated 2026 are flagged as such.

---

## 1. OpenAI — Bills et al. (2023), "Language models can explain neurons in language models"

**Generation.** GPT-4 (the explainer) is shown sequences with per-token activation values for a GPT-2 XL neuron — a mix of top-activating examples and random examples ("top-and-random") — and writes a short natural-language explanation. All 307,200 GPT-2 XL neurons were explained this way.

**Scoring (simulation scoring).** A second GPT-4 (the simulator) is given only the explanation and new text, and predicts the neuron's activation at each token. The score is the correlation between simulated and true activations on held-out text. A more expensive "ablation scoring" variant substituted simulated activations into the model and measured output divergence; correlation was used as its cheap proxy. Human-written explanations and human simulation were collected as baselines; GPT-4's explanations scored below humans'.

**Headline results / limits.**
- Most explanations scored poorly: only ~1,000+ of 307,200 neurons had explanations scoring ≥ 0.8 (OpenAI blog). Secondary summaries of the paper report mean simulation scores around ~0.15 on a mid layer for the full neuron population, vs ~0.72 for the favorable "top-and-random" subset — i.e., the method worked on a minority of (mostly uninteresting) neurons.
- Scores fall with layer depth; scoring is expensive; the simulator is itself a model, so scores confound explanation quality with simulator ability.
- **It was neurons, not SAE features, in one small model (GPT-2 XL), with graded correlation scores — no per-label pass/fail, no binary predictions, no production-label audit.**

**Relevant to Study 2:** Bills et al. also ran **revision experiments**: GPT-4 was asked to propose counterexamples to an explanation, their true activations were checked, and the explanation was revised in light of the failures; the OpenAI blog reports this raised scores. This is the original "iterative revision with activation feedback" prior art (at neuron scale, scored by simulation correlation).

Sources: paper, https://openaipublic.blob.core.windows.net/neuron-explainer/paper/index.html ; blog, https://openai.com/research/language-models-can-explain-neurons-in-language-models ; code/data, https://github.com/openai/automated-interpretability

---

## 2. Anthropic — Towards Monosemanticity (2023), Scaling Monosemanticity (2024), Mapping the Mind (2024), circuit tracing (2025)

**Towards Monosemanticity (Bricken et al., 2023; one-layer toy model).**
- Descriptions: the headline interpretability claims rest on **human hypotheses** — a blinded annotator (an author) scored 162 features/neurons (412 activation intervals) on a rubric covering confidence, consistency of activations and of logit weights with the hypothesis, and specificity. Median neuron scored 0 (no hypothesis possible); median feature interval scored 12.
- Automated evaluation followed Bills et al.: Claude generated explanations from activating examples **sampled across the full activation spectrum** (11 intervals, not just top examples), then predicted activations on unseen tokens; score = Spearman correlation over 540 token predictions per feature. A second automated test asked whether the explanation predicts which unseen tokens the feature promotes: 74% accuracy for features vs 58% for neurons (chance 50%).
- Framing is comparative (features vs neurons) on a toy model — absolute interpretability is asserted qualitatively ("quite interpretable"), **no per-label failure rate for any shipped label set**.

**Scaling Monosemanticity (Templeton et al., 2024; Claude 3 Sonnet).**
- Same automated approach scaled: "using Claude 3 Opus to provide explanations of features and predict their held out activations," applied to **100 randomly chosen features vs 100 randomly chosen neurons** — again a comparison, not an audit.
- Separately, a **specificity rubric**: Claude 3 Opus rated how each feature's description relates to the text at ~1,000 sampled activations per feature, to show SAE features are more specific than neurons.
- "Mapping the Mind of a Large Language Model" (May 2024) is a blog summary of the same work; it adds no new evaluation.

**Circuit tracing / "On the Biology of a Large Language Model" (2025).** Feature descriptions in attribution graphs are LLM-drafted from the text around top activations plus top logits, then used (and vetted/edited by researchers) in graphs. Neuronpedia's docs describe its `np_max-act-logits` explanation type as copying "Anthropic's auto-interp for attribution graphs" — model sees text around top activations and the top logits; "good for short labels."

**Has Anthropic published on improving description accuracy or on failure rates?** In this scan: **no.** Anthropic's publications use explanation scoring to compare units (features vs neurons) or to support qualitative claims; none reports a failure rate for a production label set, and none is a systematic study of description-generation methods. (Absence-of-evidence caveat: this is a scan result, not proof nothing internal exists.)

Sources: https://transformer-circuits.pub/2023/monosemantic-features/index.html ; https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html ; https://docs.neuronpedia.org/sparse-autoencoders/auto-interp

---

## 3. EleutherAI — Paulo, Mallen, Juang & Belrose, "Automatically Interpreting Millions of Features in LLMs" (arXiv:2410.13928, 2024; ICML 2025 version) + Delphi library

**Generation.** Explainer = Llama 3.1 70B Instruct, shown **40 activating examples of 32 tokens each, sampled across the deciles of the activation distribution** (following Bricken et al.), with activating tokens delimited and strengths shown. ~$200 per 1M latents. Their explanations for Gemma-2-9B and Llama-3.1-8B SAEs were released on HuggingFace and Neuronpedia (the `eleuther_*` explanation/scorer family).

**The five scoring techniques** (all graded scores over corpus examples, judged by an LLM scorer, none binary or per-label pass/fail):
- **Simulation** (Bills-style baseline): scorer predicts per-token activations; Pearson correlation.
- **Detection**: scorer gets an explanation and a shuffled set of whole sequences (activating examples drawn from activation deciles + random non-activating examples) and must say which sequences activate the latent. Measures both precision and recall of the explanation at the *sequence* level; ~5× cheaper than simulation.
- **Fuzzing**: like detection but token-level — activating tokens are delimited in each example and the scorer judges whether the marked tokens are the ones the explanation predicts. Closest to simulation (both mostly test "which tokens are nonzero"); best correlation with human ratings (Spearman ρ = 0.69, vs simulation 0.60, detection 0.59; human study: 700 contexts, 81 latents).
- **Surprisal**: AUROC of the explanation's information value (loss reduction) for activating vs non-activating contexts.
- **Embedding**: explanation-as-query retrieval AUROC; cheapest (~$50/100k latents).
- **Intervention scoring**: whether the explanation predicts the *effect* of steering the latent on generated text; recovers "output latents" that input-side scores miss (slightly negative correlation with fuzzing).

**What scores did LLM explanations get?** Scores are continuous per-explanation accuracies/correlations averaged over ~100 activating + ~100 non-activating corpus examples, reported as distributions, not failure rates. Worked examples in the paper span 0.54–0.95 fuzzing/detection accuracy depending on sampling strategy. An independent replication (Semantic Regexes, ICLR 2026; see §5) reports GPT-4o-mini pipelines at detection ≈ 0.79 (token-act-pair) / 0.86 (max-acts) and fuzzing ≈ 0.81 / 0.89 on GPT-2 features. So published detection/fuzzing numbers look "high" — but note they are (i) graded, (ii) judged by an LLM rather than read off ground-truth activations for label-authored probes, and (iii) averaged over many corpus examples per label, so a label can score 0.8 while failing on specific plausible contexts.

**Generation-method findings (their §4.2, a 500+-latent testbed):** interpretations from **top-only examples are more specific but lower-sensitivity and score lower on detection/fuzzing than interpretations from examples sampled across the whole activation distribution**; whole-distribution sampling sometimes over-broadens; bigger explainers help slightly; Claude 3.5 Sonnet ≈ Llama 3.1 70B ≈ human explanations; chain-of-thought did not significantly help. This is the closest published "which examples should the explainer see?" comparison — and it argues *against* pure top-example generation, the style used for the production Neuronpedia labels.

Sources: https://arxiv.org/abs/2410.13928 ; https://blog.eleuther.ai/autointerp/ ; https://github.com/EleutherAI/sae-auto-interp (Delphi)

---

## 4. SAEBench (Karvonen et al., arXiv:2503.09532, ICML 2025)

**Yes, it has an autointerp eval (AUTOINTERP), and it is an SAE benchmark, not a label audit.** Per the paper (Table 5) and repo: an LLM judge (GPT-4o-mini) drafts a description of each latent from its top activating examples and then predicts, on held-out sequences, which ones activate the latent (Paulo-style detection); the score is the judge's prediction accuracy, averaged over 1,000 non-dead latents, reported as **one aggregate number per SAE** (e.g., ≈ 0.83 for a Gemma-2-2B TopK SAE). Key properties:

- The same judge pipeline **generates the very explanations it scores** — it does not evaluate pre-existing production labels (e.g., Neuronpedia's).
- Test items are corpus sequences, not prompts authored from the label; the output is a mean accuracy, so there is no per-label verdict and no failure rate.
- Its purpose is comparing SAE architectures/training (alongside absorption, SCR, TPP, sparse probing, RAVEL, etc.).

Later work has questioned the metric: a 2026 rate-distortion-polysemanticity analysis found SAEBench AutoInterp *anti-correlated* (ρ ≈ −0.68) with its polysemanticity criterion, and an ICLR 2026 pairwise study (90 SAEs) found SAEBench interpretability only weakly associated with steering utility (Kendall τ_b ≈ 0.30). Any Study 2 bake-off should expect reviewers to raise these critiques of LLM-judged autointerp scores.

Sources: https://arxiv.org/abs/2503.09532 ; https://github.com/adamkarvonen/SAEBench ; https://arxiv.org/html/2510.03659 (pairwise study)

---

## 5. Head-to-head comparisons of label-GENERATION methods

Several exist. The bake-off is **not** a green field; it must position against at least these:

1. **Bills et al. (2023) revisions** — counterexample-driven iterative revision raised simulation scores (neurons, GPT-2 XL). The original "revise with feedback" result.
2. **Paulo et al. (2024) §4.2** — sampling strategy (top-only vs decile/uniform), explainer size, CoT, measured by detection/fuzzing/embedding. Finding: full-distribution sampling > top-only.
3. **FADE — "Why Bad Descriptions Happen to Good Features" (Bruni et al., 2025, arXiv:2502.16994)** — evaluates *existing open-source descriptions* (incl. Neuronpedia's Gemma Scope descriptions, generated by the MaxAct method) on 103 features (Gemma-2-2B L20; Llama-3.1-8B-Instruct L19) with four metrics (Clarity, Responsiveness, Purity, Faithfulness) centered on description-guided steering; compares explainer models (GPT-4o best; GPT-4o-mini close) and prompt constructions (token–activation pairs vs delimiter highlighting). Diagnoses *why* descriptions fail (e.g., descriptions of input patterns vs causal effect). Closest "audit of production descriptions + explainer comparison," but small-n, one layer per model, steering-based metrics, no pre-registration.
4. **Semantic Regexes (ICLR 2026)** — compares description *formats* (natural-language token-act-pair vs max-acts vs structured "semantic regexes") with GPT-4o-mini explainer/evaluator on GPT-2 and Gemma-2-2B Gemma Scope features, scored by clarity/detection/fuzzing/responsiveness/purity. Format alone moves detection by ~7 points.
5. **"Revising and Falsifying Sparse Autoencoder Feature Explanations" (NeurIPS 2025 poster)** — introduces **similarity-based sourcing of close negative sentences to falsify explanations** (the closest prior art to authored near-misses), a structured component-based explanation format, and a **tree-based iterative explainer**; reports the structured format + tree explainer improve explanation quality and that similarity-based evaluation exposes biases in existing scoring. Only the abstract was accessible in this scan; full metrics/authors not verified — treat details as thin.
6. **SAEExplainer (He et al., 2026 preprint, arXiv:2606.08496)** — trains an explainer with **activation-guided preference optimization**: generate multiple candidate explanations per feature, keep ones whose guided generations actually trigger the feature as positives and plausible-but-non-activating ones as hard negatives, then DPO (two rounds). Evaluated on **the same SAEs the user studied** (Gemma-2-9B gemmascope-res-16k; Llama-3.1-8B llamascope-res-32k) against Neuronpedia's default GPT-4o-mini explanations and fresh Claude Sonnet 4.5 / GPT-5 explanations, using Generative Accuracy (can an LLM use the explanation to synthesize text that triggers the feature) plus Gur-Arieh input/output scores; reports beating the Neuronpedia defaults on most metrics. This is the strongest existing "closed-loop, feedback-verified labeling beats production labels" result and the bake-off's most direct competitor.
7. **Gur-Arieh et al. (2025), "SAEs Are Good for Steering – If You Select the Right Features" (EMNLP 2025)** — input/output evaluation of descriptions: input-side evaluation generates activating and neutral examples *from the description* and measures activation differences — conceptually the closest published relative of the user's should-fire probe, used there as a feature-selection score rather than a label audit; also shows descriptions improve when generation considers output (logit) effects, not just inputs.
8. **Agentic explainers (2025–26)** — MAIA (Rott Shaham et al., 2024, vision) pioneered iterative hypothesis-test-revise agents. InterpAgent (2026 preprint) reports iterative refinement with contrastive prompt suites beating one-shot autointerp on Gemma-2 features. But the SPAR Fall 2025 report (below) found its tool-using agent only **matched** Delphi and human experts scored *worse* than both — iteration is not a guaranteed win.

Sources: as cited per item; FADE https://github.com/brunibrun/FADE ; steering paper https://belinkov.com/assets/pdf/emnlp2025-sae.pdf

---

## 6. Per-label validation status at scale, and how the production labels are actually made

**Neuronpedia (Lin / Decode Research).** Per current docs (https://docs.neuronpedia.org/sparse-autoencoders/auto-interp):
- Each explanation displays its **explanation type** (method, e.g. `oai_token-act-pair` = OpenAI-style token/activation pairs; `np_max-act` / `np_max-act-logits` = Anthropic-style max-activations ± logits; `eleuther_acts_top20`) and the **AI model that wrote it** (commonly gpt-4o-mini).
- **Scores are opt-in and on-demand**: a label shows "No Scores" until someone clicks and runs a scorer (`recall_alt`, `eleuther_fuzz`, `eleuther_recall`, `eleuther_embedding`, NLA scorers) with their own API key. There is **no bulk-published pass/fail validation status** for the default label sets, and **no test-and-revise step before a label is published** — labels go live as generated; multiple explanation sets per feature coexist and users can vote and submit human explanations.
- The "Interpretable Score" is an **intrusion-detection test of the feature itself** (judge must spot 1 intruder among 5 texts; Paulo & Belrose), not a validation of any label.
- The user's browser-level verification this week also confirmed Neuronpedia is a small nonprofit-run project (Decode Research); there is no published "validated label" pipeline from Lin/Decode. (The one systematic scored-at-scale label set is EleutherAI's own: Llama 3.1 70B-explainer labels for Gemma-2-9B and Llama-3.1-8B SAEs shipped *with* detection/fuzzing scores — but those are graded scores from the generating pipeline, not independent held-out pass/fail, and they are not the default labels the user audited.)

**How the specific labels under audit were generated.** Multiple papers describe Neuronpedia's **default explanations as generated by GPT-4o-mini** (SAEExplainer: "its default explanations generated by GPT-4o-mini"; Transluce's introspection paper likewise uses "the GPT-4o-mini Neuronpedia explanations"). The input format for Gemma Scope descriptions is described by FADE as the **MaxAct** method (top activating examples; Rajamanoharan et al., 2024). Neither the Gemma Scope paper (Lieberum et al., 2024) nor the Llama Scope paper (He et al., 2024) describes a validation/revision stage for the hosted labels; Llama Scope's own feature work leans on Neuronpedia-hosted explanations. Caveat: Neuronpedia hosts several explanation sets per feature and "default" can vary by source/version — GPT-4o-mini provenance is attested by multiple independent papers, not by a single canonical Neuronpedia spec page.

---

## 7. 2025–2026 work measuring label failure / score validity

- **SPAR Fall 2025, "Automating Interpretability with Agents"** (supervised program report + LessWrong summary) — the closest published *failure rate*: researchers manually audited the **first 50 features** of a Gemma-2-2B SAE (layer 20) and found **19/50 (38%) of Delphi (EleutherAI) explanations failed** at least one criterion (factual correctness vs activation pattern, scope too broad/narrow, output-feature misidentification, readability). Taxonomy overlaps the user's. Limits: n=50, non-random (first 50), human-judged, Delphi labels rather than Neuronpedia defaults, no pre-registration, no second model family. Their agent matched Delphi (~82% vs 84% pass on their scoring); human experts with full Neuronpedia tooling scored worse (58%).
- **Heap, Lawson, Farnik & Aitchison (2025; ICLR 2026), arXiv:2501.17727** — SAEs trained on **randomly initialized** Pythia transformers get auto-interpretability scores (Bills/Paulo pipelines) similar to trained models. A metric-validity result: aggregate autointerp scores partly measure dataset statistics, not learned features. A Study 2 design should include a control addressing this (or cite it as why per-label ground-truth activation tests are preferable to judge scores).
- **Karne (2026 preprint), "How Far Do Auto-Interpretation Labels Generalize"** — labels that correctly name a concept still silently fail on the same content in other languages/scripts (Serbian Latin vs Cyrillic transliteration control; misses up to 4× more often), i.e., labels omit their own range of validity. Adjacent failure axis (scope/generalization), not a pass-rate audit.
- **Metric critiques (2026)** — the rate-distortion-polysemanticity analysis (AutoInterp anti-correlates with polysemanticity) and the ICLR 2026 pairwise study (autointerp ↔ steering utility τ ≈ 0.30) both argue LLM-judged scores are weak proxies — supportive context for a ground-truth-activation audit, and a warning about evaluating Study 2 with those same scores alone.
- **Not found** in this scan: any 2025–26 paper that takes production Neuronpedia labels as-is, authors fresh should-fire/near-miss probes from the label text, pre-registers per-label predictions, and reports per-label pass rates across model families. Also not found: any replication of the user's Gemma result on Llama (or vice versa) by another group.

---

## Verdict

**Genuinely new (no close prior art found):**
1. **The audit protocol itself**: probes authored *from the label text alone* (2 should-fire + 2 hard near-miss sentences per label), outcome read from **ground-truth activations with no LLM judge in the loop**, and a strict binary rule (both should-fires > both near-misses). Prior scorers (simulation, detection, fuzzing, SAEBench) all use corpus-sampled examples, LLM judges, and graded averages. The nearest cousins are Gur-Arieh's generative input evaluation and the NeurIPS 2025 falsification poster's close negatives — both used as scores/methods, not as a pre-registered per-label audit.
2. **Pre-registered per-label binary predictions** (23 PASS / 57 FAIL locked before the Llama run; predictions also locked for Gemma) — registered-report discipline is essentially absent from the autointerp literature above.
3. **The population and the cross-family replication**: the *production* GPT-4o-mini labels that Neuronpedia actually serves, audited as-is, with the same protocol on two model families, yielding comparable headline failure rates (70.5% fail Gemma; 86.2% fail Llama). Prior failure evidence is neuron-era aggregates (Bills), a 50-feature manual audit (SPAR), or metric critiques (Heap) — none is a per-label pass rate for shipped labels.

**Close prior art (must cite; do not claim as novel):**
- Held-out predictive evaluation of explanations as an idea: Bills simulation scoring; Anthropic's Claude simulation across activation intervals; Paulo detection/fuzzing; SAEBench AUTOINTERP.
- "Labels are often wrong/over-broad" as a qualitative claim: Bills (most scores low), Paulo §4.2 (top-only labels are narrow/low-sensitivity), FADE (bad descriptions of good features), SPAR taxonomy.
- Iterative/feedback revision improving labels: Bills revisions; tree-based explainer (NeurIPS 2025); SAEExplainer's activation-verified DPO; agentic explainers (with SPAR's null result as a caution).
- Showing the explainer more than top examples: Bricken/Paulo decile sampling is the established guideline; production labels not following it is part of the user's story, not a new prescription by itself.

**What the bake-off must cite and how it must distinguish itself:**
- Cite: Bills et al. 2023; Bricken et al. 2023; Templeton et al. 2024; Paulo et al. 2024/2025; Karvonen et al. 2025 (SAEBench); FADE (Bruni et al. 2025); Gur-Arieh et al. 2025; Revising & Falsifying (NeurIPS 2025); SAEExplainer (He et al. 2026); SPAR agents report (2025); Heap et al. 2025; Semantic Regexes (ICLR 2026).
- Distinguish on design, not rhetoric: (i) evaluate every generation method under **both** the user's strict label-only pass rule **and** incumbents' detection/fuzzing, so gains can't be dismissed as metric choice; (ii) include the strong baselines — production GPT-4o-mini MaxAct labels (control), Delphi-style decile sampling, Anthropic-style max-act+logits, output-augmented generation (Gur-Arieh), feedback revision (Bills-style / tree), and an SAEExplainer-style candidate-selection arm if compute allows; (iii) pre-register predictions and analysis, as in Study 1; (iv) run on both model families and report per-label pass rates, not just mean scores; (v) include a Heap-style sanity control (e.g., a small random-init or shuffled-label arm) to show the metric can fail bad labels; (vi) pre-empt SPAR's null result by powering the study beyond n=50 and using ground-truth activations rather than human correctness judgments alone.

**Honest uncertainty flags:** Bills et al.'s aggregate score figures are partly via secondary summaries (the paper's HTML rendering is poor; the ≥0.8 count and revision benefit are from OpenAI's own blog). "Revising and Falsifying" details rest on its NeurIPS abstract only. SAEExplainer, InterpAgent, Karne, and the RDP analysis are 2026 preprints, not peer-reviewed. "No Anthropic failure-rate publication" and "no validated-label pipeline at Neuronpedia" are scan findings (docs + papers as of Nov 2026), not proofs of nonexistence. Which explanation set Neuronpedia treats as "default" per source can shift; GPT-4o-mini provenance is multiply attested but not from one canonical spec.
