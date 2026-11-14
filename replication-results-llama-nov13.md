# Does the label problem replicate in a second model? An 80-label replication on Llama 3.1 8B

Daniel Gleason — November 13, 2026

## The question

The Gemma study (pilot + scale-up) found that only 59 of 200 Neuronpedia feature labels (29.5%) survived held-out text: most features stayed silent on sentences their labels plainly cover. That result could have been a Gemma Scope quirk — one model, one SAE family, one labeler's behavior on one feature set. This run repeats the identical protocol on a different model and a different SAE: Llama 3.1 8B, the Llama Scope residual-stream 32k SAE, layer 16. If the labels overclaim there too, the problem sits with how the labels are written, not with one model.

## Setup and method

I drew 80 features at random (`random.Random(20261113)` over indices 0–32767 of source `16-llamascope-res-32k`; every drawn feature carried exactly one label). For each feature I wrote two prompts the label plainly covers (should-fires) and two close to the label that should stay quiet (near-misses), changing one variable at a time, plus a one-line prediction of whether the label would pass. The prompts and predictions were drafted with the assistance of an AI research assistant and approved and locked by me before any activation was queried.

The lock is public and predates the scoring. The locked predictions file (`replication-predictions-locked-nov13.md`, SHA-256 d95186abbc694800886401859d5d9f947c88cbd06512fd0719d9302558a8aac6) was published to the project repository as commit [fb147fb](https://github.com/dcgleason/neuronpedia-label-validation/commit/fb147fba1b577d7f1e3852c6a0767ca03cd836ce) on November 13, 2026, and scoring ran only after that commit was verified visible. The locked tally was 23 predicted PASS, 57 predicted FAIL. All 320 prompts were extracted from the locked file verbatim — two of them are quoted dialogue and carry their quotation marks as content.

A label passed under the same rule as the Gemma study: its weaker should-fire beat its stronger near-miss, min(should-fire) > max(near-miss), each score the feature's maximum activation across one prompt's tokens, read through Neuronpedia's API. One scale note: Llama Scope activations in this run are far smaller in absolute terms than Gemma Scope's (the largest single score was 6.31, against 40+ in the Gemma pilot). The pass rule is a within-feature comparison, so the verdicts do not depend on the absolute scale.

## Results

11 of 80 labels passed (13.8%) — less than half the Gemma rate.

| Study | Tested | Passed | Pass rate |
|---|---|---|---|
| Gemma-2-2B pilot (layer 12) | 40 | 12 | 30.0% |
| Gemma-2-2B scale-up (layers 6/12/18) | 160 | 47 | 29.4% |
| **Llama 3.1 8B replication (layer 16)** | **80** | **11** | **13.8%** |

The 69 failures fall into three classes:

| Failure class | Count |
|---|---|
| Silent — both should-fires at 0.00 | 51 |
| Partial — one should-fire beat both near-misses, the other did not | 16 |
| A near-miss matched or beat a should-fire | 2 |

Every one of the 51 silent failures scored 0.00 on all four prompts, near-misses included. Silence is a bigger share of failure here than in either Gemma run: 51 of 69 failures (74%), against 62 of 113 (55%) in the scale-up and 17 of 28 (61%) in the pilot.

Predictions held up better than in the Gemma scale-up: 56 of 80 (70%) were right, against 94 of 160 (59%) there — mostly because predicting FAIL was usually correct. Of the 23 labels predicted to pass, only 5 did; of the 57 predicted to fail, 51 did.

The checker's mechanism sorter (v3, plain held-out configuration, no ground truth for these features) ran on the 51 silent features and tagged 50 of them **unresolved** and one **word-form** (index 31073, "mentions of Java-related annotations and libraries"). As in the Gemma sanity check, the sorter mostly declines to name a mechanism on genuinely held-out silent features; the verdicts are the measurement, the tags are a first pass.

## What the failures look like

The most surprising silence is the dialogue feature (index 19894), labeled "dialogue and speech patterns within the text." It was predicted to pass — quoted direct speech is a concrete formatting pattern — and it scored 0.00 on all four prompts, including two that are nothing but quoted dialogue: `"I never said that," she replied. "You must have misheard me."` and `"Where were you last night?" he asked quietly.` Code and symbol labels failed the same way: features for function definitions (index 4305), URLs (index 3458), and mathematical notation (index 27458) never fired on plain examples of exactly what they name.

The two near-miss wins are both minimal pairs. The application-dates feature (index 18024) fired harder on "Registration stays open all winter; applicants may submit forms anytime" (3.19) than on either deadline sentence (3.03, 2.61): it tracks registration talk, not the deadline its label emphasizes. The seasonal-appreciation feature (index 25296) peaked on "We dread these crisp autumn walks through the pumpkin patch" (2.78), above both of its appreciation should-fires — it tracks the seasonal scene and ignores the sentiment the label is about.

The cleanest pass is a word-form label behaving exactly as written: the word "sum" feature (index 21787), margin +2.32, near-misses quiet. The largest pass margin was +2.77 ("harnessing or unlocking," index 6140), and the thinnest +0.59 (index 20386). Six of the 11 passes were predicted to fail — narrow or word-bound labels that turned out to be accurate.

## Reading the results

The Gemma finding replicates, and it gets stronger. A second model, a second SAE, and a fresh random feature sample produce the same failure shape at a lower pass rate: labels written from top activations describe features as broader and more concept-shaped than the features behave on fresh sentences, and the modal failure is total silence on on-label text. Nothing about the pattern depends on Gemma, on one layer, or on the features picked for the pilot. A reader who trusts these labels will mispredict activations in both models, most often by expecting fire that never comes.

## Limits

Four limits bound what this replication can claim. First, the all-zero ambiguity from the pilot carries over and is larger here: an all-zero score cannot separate "the feature is far narrower than its label" from "the feature keys on surface forms my prompts never used," and 51 of 80 features landed in that bucket. The pre-registered rule scores both readings as a failed label; a token-level follow-up is the way to pull them apart. Second, this is one layer of one SAE in the second model — Llama Scope at other layers could differ. Third, the same single-rater caveat applies: my reading of each label is baked into the prompts and the pass rule, and the prompts and predictions were drafted with an AI research assistant and approved by me before locking. Fourth, layer 16 of Llama 3.1 8B sits at a different relative depth and width (32k features) than the Gemma layers tested, so the two pass rates are comparable as label-quality measurements, not as controlled model comparisons.

## What comes next

The replication closes the "one model" objection to the Gemma result. The open thread is the silent majority in both models: a token-level pass over the all-zero features, in both SAEs, to separate narrow features from surface-form keying — that split decides whether the fix is better labels or better label *types* (concept, word-form, register, document-structure). The checker that scored this run is the same harness as the Gemma study; the protocol, the locked predictions, and the raw scores for all 80 features are in the project repository and in `replication/` locally.
