# Do auto-generated feature labels survive held-out text? A 40-label pilot on Gemma-2-2B

Daniel Gleason — November 12, 2026

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
