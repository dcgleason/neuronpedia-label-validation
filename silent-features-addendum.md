# Why were the silent features silent? A follow-up on five labels

Daniel Gleason — November 12, 2026

## The question

In the pilot, 17 of 40 features scored exactly zero on all four test prompts. A zero cannot tell two stories apart: the feature is far narrower than its label, or the feature keys on a form the test sentences did not use. This follow-up takes five of the silent features and asks what actually makes each one fire. Method: I inspected each feature's stored top examples token by token, wrote predictions down before probing, then ran focused probes through the same Neuronpedia activation endpoint, changing one thing at a time — a word, a phrasing, a format. 42 probes in two rounds. As in the pilot, the probes were drafted with the assistance of an AI research assistant and approved by me before running.

## What actually triggers each feature

| Feature (label) | What the label promises | What actually fires it | Key evidence |
|---|---|---|---|
| 14719, "terms related to colors and color coding" | Color terms | The word "color" itself, in any form | "The color of the first wire is red" 46.0; code constant COLOR_MENU_TEXT 43.0; "Red, green, blue, and yellow" with no "color" token 0.0; "Colorado" 10.75 |
| 18, "terms related to food and culinary subjects" | Food and cooking | Academic field and institution names, plus a biomedical phrase | "College of Architecture and Environmental Design" 31.1, peak on "Environmental"; "'cell death and survival'" in a genomics sentence 34.0; "The food festival served fish, burgers, and fresh bread" 0.0 |
| 2580, "references to literary works and notable authors" | Works and authors | Recommendation language about creative works | "This novel will appeal to fans of Shakespeare and Dickens" 39.0; "Shakespeare wrote Hamlet…" 0.0; "Hamlet is a tragedy by William Shakespeare" 0.0; a game blurb with "similar in style to" 33.5; a textbook blurb with "will appeal to students" 3.3 |
| 2081, "periods and punctuation that signify the end of sentences" | Sentence-final periods | Punctuation at document and citation boundaries in long formatted text | A legal citation cluster "(Colo. 2000))." 4.09, scored on that token; ten probes of ordinary sentence periods, including a full paragraph, all 0.0; strongest stored peaks sit on the document-boundary token following a period |
| 2625, "specific scientific or technical terms related to genetics and molecular biology" | Genetics terms | Nothing genetic that I could find; a weak code trace over a dominant boundary pattern | A five-sentence genetics abstract 0.0; a Swift code snippet 7.25 on "unknownFields"; 14 of 45 stored peaks sit on the document-boundary token after unrelated documents (code, Wikipedia, legal text) |

## What this adds

The pilot's failures were mostly filed under one shape: labels broader than behavior. These five split that shape into distinct mechanisms, and each mechanism suggests a different rule for checking labels at scale.

- **A label can name a topic while the feature tracks one word for it.** Colors is the clean case. A label check that only uses topic vocabulary will miss this; a check should also test the topic with the label's own keyword removed.
- **A label can describe a minority theme of the top examples.** Only 21 of the food feature's 45 stored examples contain food words, and its strongest peaks are not among them. A label written from a sample can inherit the sample's loudest theme rather than the feature's center of mass.
- **A label can name the subject while the feature tracks the rhetorical move.** The literature feature ignores references and answers recommendation language. The same author scored 0 in two phrasings and 39 in a third.
- **A label can describe a mark while the feature needs the document around it.** The punctuation and genetics features live at document boundaries inside long texts. No isolated sentence reproduces the punctuation feature's strong behavior, and nothing genetic reproduces the genetics feature at all. A label check run only on short isolated text will call both dead; a check run only on top examples will call both accurate. The test format itself decides the verdict.

One data note: each feature's stored set mixes its top examples with a shared zero-activation bin, identical across features. Only the positive examples carry information, and several verdicts above rest on reading those peaks token by token rather than reading the example texts as wholes — which is, in miniature, the same mistake the labels made.

Files: probe-predictions.md and probe-predictions-round2.md (written before each round), probe-results.json and probe-results-round2.json (every probe with its score and peak tokens), run_probes.py and run_probes_round2.py.
