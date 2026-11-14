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
