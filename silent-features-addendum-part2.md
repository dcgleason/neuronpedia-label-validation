# The silent seventeen, completed — follow-up part 2

Daniel Gleason — November 12, 2026

Part 1 of this follow-up (silent-features-addendum.md) asked what actually triggers five of the pilot's 17 all-zero features. This part finishes the set: the remaining twelve, probed the same way — stored examples read token by token, predictions written down first, then focused probes changing one thing at a time. 49 probes in two rounds.

## The twelve

| Feature (label) | What actually fires it | Key evidence |
|---|---|---|
| 5158, "elements related to buttons in a UI or web interface" | The code token "btn" | `<button class="btn btn-primary">` 45.0 on "btn"; CSS ".btn-default" 41.75; "Press the button to continue" 0.0 |
| 8743, "negative phrases and expressions related to obligation or denial" | The words "or" and "nor" | "It was not the only factor, or even the main one necessarily" 33.0 on "or"; "Neither the manager nor the employees…" 16.6 on "nor"; obligation and denial sentences 0.0 in the pilot |
| 1029, "references to ancient figures and mythological or legendary elements" | Chinese proper names and terms | "Tianxiang was a famous general of the Song dynasty" 25.1 on "xiang"; "In Chinese mythology, Chang'e flew to the moon" 7.1; "Zeus and Hera ruled from Mount Olympus" 0.0 |
| 3580, "elements of personal relationships and family connections" | Obituary formulas | "He is survived by his loving wife of 42 years" 33.25; "preceded in death by his father" 25.1; ordinary family sentences 0.0 in the pilot |
| 8630, "discussions related to music and artistic collaborations" | Talk-show and podcast guest register | "In this episode, the host talks with a jazz pianist" 35.5; "Sosa joins Team LeftJab Boxing Radio to talk…" 33.0; "She released a new album on Friday" 0.0 |
| 5072, "terms related to medical conditions and anatomical processes" | Dense clinical terminology in journal register | "positional vertigo… radiation-induced fibrosis" 23.25; "Reperfusion injury… ischemia" 16.1; plain patient-language sentences 0.0 in the pilot |
| 7623, "questions and inquiries about various topics" | Forum question posts | A forum-style question with follow-up text and "Please answer me! Answers: 2" 18.0, peak on the paragraph break; a clean bare question 0.0 in the pilot |
| 3349, "phrases related to diversity and inclusion" | Weakly, business-page formatting; strong behavior not reproducible in isolation | A heading-and-colon event page 8.4; a longer version 6.8; diversity prose of any kind 0.0 |
| 6515, "references to a specific shoe brand" | Weakly, keyword-stuffed commerce text at length | A ~120-token spam paragraph repeating "supra shoes" 5.34; short spam and natural brand sentences 0.0 |
| 3070, "concepts related to reputation and its effects" | No consistent trigger found | Best responses across nine probes: 6.6 ("franchise"), 4.7 ("reputation" in a forum passage), 4.6 ("upvoted") — scattered tokens, nothing semantic |
| 7196, "discussions and references to issues of racism and discriminatory behaviors" | No consistent trigger found | A formal jury discrimination sentence 0.0; a longer argumentative passage about a racial case 11.9, peaking on "," and "but," not on any content word |
| 14520, "terms related to governance and political processes" | No coherent rule; fires on particular older prose passages | A Federalist-style sentence 28.75; a nature-essay sentence copied from a stored example 26.6; the Gettysburg Address 0.0; modern parliamentary sentences 0.0 in the pilot |

## The seventeen, sorted

With all 17 silent features analyzed, the pilot's single largest failure shape — silence — resolves into five mechanisms:

- **Word-form detectors (4).** The feature tracks a token; the label names the token's topic. Colors (the word "color"), buttons ("btn"), obligation/denial ("or"/"nor"), ancient figures (Chinese name fragments).
- **Register detectors (5).** The feature tracks a genre's phrasing; the label names the genre's subject. Literary works (recommendation blurbs), family connections (obituaries), medical terms (clinical journal prose), music collaborations (talk-show appearances), questions (forum posts).
- **Displaced center of mass (1).** The label names a minority theme of the top examples. Food, whose feature centers on academic field and institution names.
- **Document-structure bound (4).** The feature's strong behavior lives inside long formatted documents and barely reproduces in isolated text, whatever the words are. Punctuation, genetics, diversity pages, shoe-brand spam.
- **No consistent trigger found (3).** Reputation, racism, governance. Probes modeled on their stored examples produced only scattered weak responses on unrelated tokens. Reporting these as unresolved is part of the result: a label can be attached to a feature whose behavior no short test characterizes, and a validation method should say so instead of guessing.

The practical lesson is the same one the pilot pointed at, now with a mechanism attached to each failure: a label written from top examples inherits whatever those examples make salient — a word, a genre, a theme, a document shape — and only some of those are the concept the label claims. Each mechanism has a matching cheap test. Word-form: rerun the topic with the label's keyword removed. Register: rerun the subject in a different genre's phrasing. Center of mass: count themes across all stored examples, not the loudest few. Document structure: test at document length, in formatted text. Unresolved: say unresolved.

Files: probe-predictions-part2.md, probe-predictions-part2-round2.md, probe-results-part2.json, probe-results-part2-round2.json, run_probes_part2.py, run_probes_part2_round2.py. Part 1 files are listed in silent-features-addendum.md.
