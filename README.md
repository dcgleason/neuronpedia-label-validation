# Do auto-generated feature labels survive held-out text? A 40-label pilot on Gemma-2-2B

Daniel Gleason — November 12, 2026

## The short version

This project tests whether Neuronpedia's auto-generated feature labels
describe what their features actually do, using text the labeler never saw.
The headline: **59 of 200 Gemma-2-2B labels passed (29.5%)**, and on Llama
3.1 8B **32 of 160 passed** under the identical protocol. Three controls say
the labels are the weak link, not the features: corrected labels passed 15 of
21 where the originals went 0 of 21; shuffled label–feature pairings passed 0
of 40 against 12 of 40 for the real pairings; and labels regenerated blind by
Claude Sonnet passed 28 of 40 against the shipped labels' 12 of 40. Every
scored label, with its prompts, is in the
[interactive explorer](https://dcgleason.github.io/neuronpedia-label-validation/explorer/)
(440 records).

| Run | Tested | Passed | Predictions right |
|---|---|---|---|
| Gemma pilot (layer 12) | 40 | 12 | — (verdicts predicted per label) |
| Gemma scale-up (layers 6/12/18) | 160 | 47 | 94 of 160 (59%) |
| Label rewrite retest | 21 | 15 | all 21 predicted pass |
| Llama replication (layer 16) | 80 | 11 | 56 of 80 (70%) |
| Llama layers 8 and 24 | 80 | 21 | 60 of 80 (75%) |
| Permutation control | 40 | 0 | all three arm-level predictions held |
| Explainer swap (Sonnet labels) | 40 | 28 | all three arm-level predictions held |
| Width control (65k SAE) | — | not run | closed as a limitation, below |

## Integrity: predictions locked before scoring

No verdict in this repo rests on a prediction made after the fact. Every
run's prompts and predictions were frozen and SHA-256 hashed before the
first activation was queried; from the Llama replication onward, the locks
were also committed to this repository before scoring, so the git history is
the timestamp.

- Pilot predictions, frozen Nov 12, 2026, 4:28 PM EST —
  `affcbe8cf3e1b601655a84426426b1f90a1c88b69fbf2d21765325201e6b84a2`
- Scale-up prompts and predictions —
  `f611f7709bf0a679a174bd54387c21792b2152e371f3c61780832d4834ac8f8f`
- Label-rewrite prompts —
  `47367fc02e1236e4216658e097c3a705827917f0c173518339bfbbd9967e4ee3`
- Llama layers predictions — commit `f820cb5`,
  `9bedd27f155ebc91dda8e21aecd86129b102a35cd2a2b3500f3f92cf6b5172f1`
- Permutation control — design `ab93fbe460407354643383ad8818127da84d803e4b0cdc19cd74138cceb4b16f`,
  predictions `c6ea8efe352f6b3db32a148fcf0ac61d39207f7deee5494c16be4452eedab582`, lock commit `2b67c388`
- Explainer swap — design `019aeacd57d3d5b4043832e7252729d6db429629413a20e2c67f56c507f31c4e`,
  predictions `dad4b6e336d354e51a580563e29a4f7b75332678e54b09f7f416e44b333906f7`, lock commit `08f7b237`

## The question

Neuronpedia puts a short text label on most features in the Gemma Scope sparse autoencoders. GPT-4o-mini wrote those labels from each feature's strongest activating examples, and every label I tested carried a "No Scores" marker: nobody had checked them against text the labeler never saw. A label is a claim about what a feature responds to, and anyone steering or auditing with a feature leans on it. I tested 40 of them.

## Setup and method

I worked in Gemma-2-2B, the Gemma Scope residual-stream 16k SAE, layer 12 (source `12-gemmascope-res-16k`, 16,384 features). From a random sample of 240 features I cut a shortlist of 60 down to 40, keeping a deliberate mix: 22 labels I classed as concrete (food, colors, the Windows operating system) and 18 as slippery (reputation, coolness, intentions and plans).

For each feature I wrote two prompts the label plainly covers (should-fires) and two close to the label that should stay quiet (near-misses). Near-misses changed one variable at a time: a brand swap, a word in a different sense, the same letters inside another word. I wrote a prediction for each feature describing the scores an accurate label would produce. The prompts and predictions were drafted with the assistance of an AI research assistant and approved by me before locking. I froze the set in a predictions file at 4:28 PM EST on November 12, 2026, and recorded its SHA-256 hash (affcbe8cf3e1b…) before querying any activation.

A label passed if its weaker should-fire beat its stronger near-miss: min(should-fire) > max(near-miss), with each score the feature's maximum activation across one prompt's tokens, read through Neuronpedia's API.

## Results

12 of 40 labels passed.

| Labels | Tested | Passed |
|---|---|---|
| Concrete | 22 | 9 |
| Slippery | 18 | 3 |
| All | 40 | 12 |

The 28 failures fall into three shapes:

| Failure shape | Count |
|---|---|
| Silent on all four prompts | 17 |
| One should-fire silent | 6 |
| A near-miss matched or beat a should-fire | 5 |

## What the failures look like

Seventeen features never fired. The food feature (index 18) scored 0.00 on "She simmered the tomato sauce with garlic and basil for an hour" and 0.00 on "The recipe calls for two cups of flour and a pinch of salt." The literary-works feature scored 0.00 on "Shakespeare wrote Hamlet." The genetics feature scored 0.00 on a sentence about a BRCA1 mutation. The feature labeled as end-of-sentence punctuation scored 0.00 on two sentences that both end in periods.

The near-miss wins were all word-sense and string bleeds. The light-and-illumination feature answered "The suitcase was light enough to carry with one hand" at 41.25, more than double its best illumination sentence (17.75). The "short" feature answered "shortbread" at 44.25, above both of its should-fires. The yellow feature answered "The old newspaper had yellowed" at 39.00, above both color sentences. Its color swap (orange) stayed below them: the color part of that label held, and the word-form part failed. The control-and-regulation feature peaked on its near-miss, "He controlled his temper" (37.25), while its regulation should-fire scored 0.00.

One anchor case held. I had flagged the "Tom" feature (index 1657) by hand before the run, because its top positive logits include "Tomatoes." It passed with a margin of +6.75: the tomato sentence fired at 13.50, below both genuine Tom sentences (20.25 and 21.75), and the John swap scored 0.00. The cleanest pass in the run was happiness and positive emotions (index 7798), margin +11.81 with both near-misses at 0.00; the thinnest was Mercury (index 15337), +0.06. One contrast: the general colors feature (index 14719) stayed silent on every prompt while the specific yellow feature fired strongly on everything, including a verb form.

## Reading the results

The labeler wrote each label from top activations alone. It never saw a near-miss or ordinary text the feature ignores. The labels describe features as broader and more concept-shaped than the features behave on fresh sentences. Features variously track a concept, a word across its senses, or a string of letters, and the labels rarely say which. A reader who trusts a label will predict activations badly in both directions: expecting fire on on-topic text that leaves the feature silent, and missing fire on off-topic text that shares a word or a string.

## Limits

Four limits bound what this pilot can claim. First, the 17 all-zero results are ambiguous: an all-zero score cannot separate "the feature is far narrower than its label" from "the feature keys on surface forms my prompts never used." The pre-registered rule scores both readings as a failed label; pulling them apart needs a token-level follow-up. Second, I am the single rater: my reading of each label is baked into the feature picks, the prompts, and the pass rule. Third, this is one model, one SAE, one layer, and 40 features. Fourth, some verdicts rest on the plain reading of a loosely written label, and loose labels are hard to falsify at all.

## What comes next

The script that ran this pilot already works as a small label-checking harness: locked prompts in, scores out, pass and fail sorted by margin. The same loop runs on hundreds of labels at API-call cost. The extensions I want next are more layers and a second model, a second rater with an agreement check on the label readings, and a token-level pass over the all-zero features to separate narrowness from surface-form keying. A label that ships with a measured failure rate, plus a breakdown of how it fails, is worth more than a label with a plausible sentence attached.

## Files in this repo

- `run_pilot.py` — the harness. It reads the prompts, queries Neuronpedia one prompt at a time, saves raw results after every call (an interrupted run resumes where it stopped), and rewrites the summary as it goes.
- `pilot-prompts.json` — the 160 locked prompts in machine-readable form: 40 tests, each with a feature index, the label, two should-fire prompts, two near-miss prompts, and the written prediction. The metadata block records the lock timestamp and the predictions hash.
- `pilot-predictions-locked.md` — the same predictions in human-readable form, frozen before the run.
- `results-summary.md` — per-test scores, margins, and pass/fail verdicts for all 40 tests.
- `results-raw.json` — the recorded max activation for every prompt, with timestamps.

## Reproduce

1. **Check the lock.** The predictions were frozen before any activation was queried. Verify with `sha256sum pilot-predictions-locked.md`; the hash should read `affcbe8cf3e1b601655a84426426b1f90a1c88b69fbf2d21765325201e6b84a2`.
2. **Get a key.** A free Neuronpedia account comes with an API key (on your account page). Activation calls go to `POST https://www.neuronpedia.org/api/activation/new` with the key in the `x-api-key` header. The endpoint allows 1000 requests per 60 minutes; this run needs 160.
3. **Supply one helper.** `run_pilot.py` imports a small module, `np_activation`, with a single function, `get_activation(index, text)`. It POSTs `{"feature": {"modelId": "gemma-2-2b", "source": "12-gemmascope-res-16k", "index": "<index as string>"}, "customText": "<prompt>"}` to the endpoint above and returns the maximum of the per-token `values` list in the response. The helper is not included in this repo because in my setup it draws the key from a secure credential vault instead of a file; a plain version is a few dozen lines with any HTTP client.
4. **Adjust two paths.** At the top of `run_pilot.py`, `BASE` points at my local folder and a `sys.path` line points at the folder holding `np_activation`. Point both at your own layout, put `pilot-prompts.json` where the script expects it, and run `python3 run_pilot.py`. It writes `results-raw.json` and `results-summary.md` as it goes.

## Follow-up: why were the silent features silent?

The pilot's largest failure shape was silence: 17 features scored zero on every prompt, and a zero cannot distinguish a feature that is far narrower than its label from one that keys on a form the test sentences did not use. I took five of the silent features (food, colors, literary works, end-of-sentence punctuation, genetics) and probed what actually makes each one fire: 42 probes in two rounds, predictions written down before each round, one variable changed at a time.

Each label failed a different way. The colors feature detects the word "color" itself, not color terms. The food feature's center of mass is academic field and institution names. The literary-works feature answers recommendation language ("will appeal to fans of Shakespeare and Dickens" scored 39.0; "Shakespeare wrote Hamlet" scored 0.0). The punctuation and genetics features live at document boundaries inside long texts; nothing genetic fired the genetics feature at all. Full method, evidence table, and probe data: [silent-features-addendum.md](silent-features-addendum.md).

## Expansion (same evening): all 17 autopsies, corrected labels, and a 200-label base rate

Three follow-ups ran after the pilot, each with its predictions written down and locked before any scoring.

**1. The remaining 12 silent features, autopsied.** Same method as the first five: inspect the stored examples token by token, predict what would fire, probe one variable at a time (49 probes, two rounds). All 17 silent features now sort into five failure mechanisms:

- **Word-form detectors (4):** the feature tracks a word or string, not the labeled topic — "color" itself, the code token "btn", the words "or"/"nor", Chinese proper names under a "mythology" label.
- **Register detectors (5):** the feature tracks a style of writing — recommendation blurbs, obituary formulas, clinical-journal register, talk-show guest register, forum question posts.
- **Displaced center of mass (1):** the food feature's stored examples are mostly academic field and institution names; food was a minority theme the labeler generalized from.
- **Document-structure bound (4):** the feature fires at document boundaries or only inside long documents; no short sentence reproduces it.
- **No consistent trigger found (3):** the features labeled "reputation," "racism," and "governance" resisted every probe. Reported as unresolved rather than explained.

Each mechanism has a matching cheap check: remove the keyword and retest; swap the register and keep the content; count the label's theme across all stored examples, not just the top ones; test at document length. Full evidence: [silent-features-addendum-part2.md](silent-features-addendum-part2.md).

**2. Rewrite the failed labels and retest them.** For the 28 failed pilot labels, corrected labels were written from the autopsy and pilot evidence (21 labels; 7 honestly marked "no corrected label offered" — the three unresolved features and the four document-bound cases). The corrected labels and fresh prompts were locked and hashed before the retest, under the same pass rule, with a standing prediction that every corrected label would pass. **Result: 15 of 21 passed.** The original labels went 0 for 21 on the same features. The 6 corrected labels that still failed are findings too: each feature turned out broader, narrower, or more phrasing-bound than even the evidence-based rewrite assumed. Details: [label-rewrite.md](label-rewrite.md), scores in [label-rewrite-summary.md](label-rewrite-summary.md).

**3. Scale-up: 160 more labels, three layers.** A fresh random sample (seed fixed in advance) of 160 features never in the pilot: 80 at layer 12, 40 at layer 6, 40 at layer 18, same 16k residual-stream SAEs. Same protocol: four prompts per label, a pass/fail prediction registered for every test, prompts locked and hashed before the run. **Result: 47 of 160 labels passed (29%).** By layer: layer 6, 10 of 40; layer 12, 19 of 80; layer 18, 18 of 40. My registered predictions were right 94 of 160 times (59%) — better than chance, far from reliable, which is itself a measure of how hard these labels are to read at face value. Combined with the pilot, **59 of 200 labels passed (29.5%)** under the registered rule. Sample and method: [scaleup-sample.md](scaleup-sample.md); per-test scores: [scaleup-summary.md](scaleup-summary.md).

The headline across all three parts is the pilot's headline, now with a base rate: labels generated from top activations alone describe features as broader and more concept-shaped than they behave, and roughly seven in ten do not survive a held-out test written from the label itself.

## Extensions, November 13–14, 2026

Four follow-ups ran after the expansion above, each locked before scoring.

**Llama replication and layers.** The identical protocol on Llama 3.1 8B
passed 11 of 80 labels at layer 16 (13.8%), 9 of 40 at layer 8, and 12 of 40
at layer 24. Silence dominated failures at every layer. The low pass rate is
not a Gemma quirk; it tracks the labeling method across model families.
Results: `replication-results-llama-nov13.md`, `llama-layers-results-nov14.md`.

**Automated checker.** The held-out test, automated end to end: the checker
writes its own prompts from a label, locks them, scores them, and classifies
the failures. Against the 40 hand-scored pilot verdicts it agrees on 38
(95%); on 62 held-out silent features it reproduced the original verdicts
exactly, 0 pass and 62 fail. The mechanism sorter is a first pass and is
labeled as such. Code and calibration notes: `checker/`.

**Permutation control.** The pilot's 40 labels were shuffled onto the wrong
features under a seeded derangement and rescored. 0 of 40 shuffled pairings
passed, against 12 of 40 for the real pairings, and all three locked
arm-level predictions held. The labels carry real feature-specific signal;
they just overclaim it. Results: `permutation-control-results-nov14.md`.

**Explainer swap.** Claude Sonnet regenerated the 40 pilot labels blind,
from the same stored examples the original labeler saw, without the original
labels or results. 28 of 40 passed, against 12 of 40 for the shipped
GPT-4o-mini labels; 17 pilot failures flipped to passes. The swap changes
the model, the example format, and one instruction together, so the win
supports the combined claim only. Results: `explainer-swap-results-nov14.md`.

**Width control — closed as a limitation.** Whether SAE width explains the
Gemma–Llama gap could not be tested. Neuronpedia's inference is unavailable
for Gemma-2-2B SAEs wider than 16k, and local scoring of the 65k SAE failed
a bridge validation against the reference API: token counts and peak
positions matched, magnitudes did not, and a diagnostic ruled out a layer
offset and a threshold artifact. The arm was closed unscored rather than
pool local and API activations, so width remains an open confound. Full
record: `bridge-check-results-nov14.md`.
