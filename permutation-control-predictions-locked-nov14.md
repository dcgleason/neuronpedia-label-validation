# Permutation control (shuffled labels) — predictions LOCKED

> **STATUS: LOCKED.** Drafted November 14, 2026; approved as drafted and locked by Danny Gleason on November 14, 2026 (~11:57 AM ET), before any scoring. No feature in this file has been run through the activation API in its permuted pairing, and no scoring of any kind has been performed. No activation calls of any kind were made while preparing this file. This file was published to the GitHub repository as the lock commit before any scoring. Companion locked design file: `permutation-control-design-locked-nov14.md`. This file must not be edited after locking.

- **Study:** Permutation control for Study 1 of the Neuronpedia label-validation study. The pilot (Gemma-2-2B, layer 12) passed 12 of 40 labels under the held-out prompt protocol. This control re-runs the identical protocol with every feature scored against a different feature's prompts. Shuffled labels should pass near 0%; if they do not, the protocol does not discriminate and the pilot's verdicts are suspect.
- **Model:** Gemma-2-2B (`gemma-2-2b`)
- **SAE set:** Gemma Scope residual-stream, 16k width — source ID `12-gemmascope-res-16k` (layer 12), the pilot's source.
- **Sample:** the pilot's 40 features, in pilot test order, with their labels taken from `pilot-prompts.json` (locked November 12, 2026).
- **Prompts:** the pilot's locked prompts, verbatim. Each feature receives another feature's exact two should-fire and two near-miss prompts. No prompt text appears in this file because none of it is new — it is reproduced in full in `pilot-prompts.json`, and the pairing below is the only new content.
- **Derangement (exactly):** positions are pilot test numbers 1–40. `rng = random.Random(20261114)`; `perm = list(range(40))`; `rng.shuffle(perm)`; the feature at position *i* receives the prompts of the feature at position `perm[i] + 1`. **The first seed tried, 20261114, produced a valid derangement — zero fixed points — so no feature keeps its own prompts and no redraw was needed.** (Had a fixed point occurred, the rule was: discard, increment the seed by 1, redraw.)
- **Pass rule (identical to the pilot):** a pairing passes if both received should-fire prompts activate the target feature clearly above both received near-miss prompts (min(should-fire) > max(near-miss)).
- **Predictions in this file:** 0 PASS, 40 FAIL at the per-pair level. The arm-level bound below (≤ 2 passes) absorbs the flagged pairs where a broadly reactive target meets vaguely adjacent text; the gap between the per-pair calls and the arm-level bound is intentional, and the flagged pairs are named in their Basis lines.
- **Prediction heuristics:** grounded in the pilot's own numbers for each target feature (its should-fire and near-miss activations and margin, from `results-summary.md`) and in the silent-feature autopsy where one exists. A target that scored 0.00 on all four of its own matched prompts is predicted to stay at or near 0.00 on foreign text. A target that passed or reacted at home is predicted to fail abroad unless the source prompts contain its actual trigger vocabulary — checked prompt by prompt for every reactive target.
- **Authorship:** Derangement generated mechanically by the seeded procedure above. Predictions drafted by Muse; approved and LOCKED by Danny Gleason on November 14, 2026, before any scoring.
- **SHA-256:** computed at lock (November 14, 2026) and recorded in the lock commit in this repository. This file must not be edited after locking.

## Arm-level predictions (locked)

1. **Total passes ≤ 2 of 40 (≤ 5%)** — against the real pairing's 12 of 40 (30%) in the pilot.
2. **All 17 pilot-silent features fail.** The targets that scored 0.00 on every one of their own prompts in the pilot (idx 18, 1029, 2081, 2580, 2625, 3070, 3349, 3580, 5072, 5158, 6515, 7196, 7623, 8630, 8743, 14520, 14719) are predicted to score at or near 0.00 on foreign prompts as well.
3. **Falsifier: ≥ 6 of 40 passing (≥ 15%) means the test does not discriminate.** For a feature firing on foreign text with activations unrelated to the should-fire/near-miss split, the chance both should-fires land above both near-misses is 1 in 6 (≈ 16.7%). A permuted pass rate at that level is indistinguishable from chance, and Study 1's verdicts — and every result built on the same protocol — would be suspect.

## Derangement table

| Pair | Target feature (scored) | Receives the prompts of | Prediction |
|---|---|---|---|
| 1 | Test 1 — idx 18 | Test 38 — idx 15337 | FAIL |
| 2 | Test 2 — idx 483 | Test 12 — idx 3070 | FAIL |
| 3 | Test 3 — idx 869 | Test 37 — idx 15035 | FAIL |
| 4 | Test 4 — idx 1029 | Test 25 — idx 7623 | FAIL |
| 5 | Test 5 — idx 1302 | Test 27 — idx 8123 | FAIL |
| 6 | Test 6 — idx 1501 | Test 7 — idx 1643 | FAIL |
| 7 | Test 7 — idx 1643 | Test 15 — idx 3592 | FAIL |
| 8 | Test 8 — idx 1657 | Test 19 — idx 5158 | FAIL |
| 9 | Test 9 — idx 2081 | Test 6 — idx 1501 | FAIL |
| 10 | Test 10 — idx 2580 | Test 4 — idx 1029 | FAIL |
| 11 | Test 11 — idx 2625 | Test 10 — idx 2580 | FAIL |
| 12 | Test 12 — idx 3070 | Test 22 — idx 7196 | FAIL |
| 13 | Test 13 — idx 3349 | Test 11 — idx 2625 | FAIL |
| 14 | Test 14 — idx 3580 | Test 3 — idx 869 | FAIL |
| 15 | Test 15 — idx 3592 | Test 39 — idx 15623 | FAIL |
| 16 | Test 16 — idx 4207 | Test 17 — idx 4593 | FAIL |
| 17 | Test 17 — idx 4593 | Test 34 — idx 13230 | FAIL |
| 18 | Test 18 — idx 5072 | Test 35 — idx 14520 | FAIL |
| 19 | Test 19 — idx 5158 | Test 23 — idx 7223 | FAIL |
| 20 | Test 20 — idx 6515 | Test 13 — idx 3349 | FAIL |
| 21 | Test 21 — idx 6865 | Test 18 — idx 5072 | FAIL |
| 22 | Test 22 — idx 7196 | Test 21 — idx 6865 | FAIL |
| 23 | Test 23 — idx 7223 | Test 20 — idx 6515 | FAIL |
| 24 | Test 24 — idx 7467 | Test 30 — idx 10276 | FAIL |
| 25 | Test 25 — idx 7623 | Test 1 — idx 18 | FAIL |
| 26 | Test 26 — idx 7798 | Test 40 — idx 16358 | FAIL |
| 27 | Test 27 — idx 8123 | Test 24 — idx 7467 | FAIL |
| 28 | Test 28 — idx 8630 | Test 14 — idx 3580 | FAIL |
| 29 | Test 29 — idx 8743 | Test 8 — idx 1657 | FAIL |
| 30 | Test 30 — idx 10276 | Test 28 — idx 8630 | FAIL |
| 31 | Test 31 — idx 11270 | Test 26 — idx 7798 | FAIL |
| 32 | Test 32 — idx 12608 | Test 29 — idx 8743 | FAIL |
| 33 | Test 33 — idx 12964 | Test 2 — idx 483 | FAIL |
| 34 | Test 34 — idx 13230 | Test 32 — idx 12608 | FAIL |
| 35 | Test 35 — idx 14520 | Test 9 — idx 2081 | FAIL |
| 36 | Test 36 — idx 14719 | Test 33 — idx 12964 | FAIL |
| 37 | Test 37 — idx 15035 | Test 31 — idx 11270 | FAIL |
| 38 | Test 38 — idx 15337 | Test 36 — idx 14719 | FAIL |
| 39 | Test 39 — idx 15623 | Test 16 — idx 4207 | FAIL |
| 40 | Test 40 — idx 16358 | Test 5 — idx 1302 | FAIL |

## Predictions by pair

### Pair 1 — target idx 18, "terms related to food and culinary subjects" ← prompts of idx 15337, "mentions of the term “Mercury,” particularly in relation to its propulsion systems and legal implications"

- Prediction: **FAIL**
- Basis: Target scored 0.00 on all four of its own prompts in the pilot. Mercury text contains nothing culinary for it to fire on.

### Pair 2 — target idx 483, "references to the Windows operating system" ← prompts of idx 3070, "concepts related to reputation and its effects"

- Prediction: **FAIL**
- Basis: Target is the pilot's cleanest discriminator (should-fires 9.56/6.94, near-misses 0.00/0.00), keyed to the operating-system sense of "Windows." Reputation prompts contain no OS content.

### Pair 3 — target idx 869, "geographical and administrative terms related to specific regions or districts" ← prompts of idx 15035, "phrases that highlight the concept of “short” in various contexts"

- Prediction: **FAIL**
- Basis: Target fired on only one of its own should-fires (13.88; the other 0.00). The "short" prompts name no regions, districts, or administrative terms.

### Pair 4 — target idx 1029, "references to ancient figures and mythological or legendary elements" ← prompts of idx 7623, "questions and inquiries about various topics or contexts"

- Prediction: **FAIL**
- Basis: Target scored 0.00 on all four of its own prompts. Everyday question sentences are not ancient figures or mythology.

### Pair 5 — target idx 1302, "shipping-related terms and phrases for large items" ← prompts of idx 8123, "references to different types and characteristics of pipes"

- Prediction: **FAIL**
- Basis: Target passed its own test (margin +3.28) on freight and delivery vocabulary. Pipes prompts are plumbing text with no shipping terms.

### Pair 6 — target idx 1501, "moments of surprise or unexpected events, particularly those that are positive or celebratory in nature." ← prompts of idx 1643, "references to light and illumination contexts"

- Prediction: **FAIL**
- Basis: Target is jumpy — 54.00 on one own should-fire, 15.44 on an own near-miss — the one caution here. But lamp and sunlight text carries no surprise or celebration content for it to jump at.

### Pair 7 — target idx 1643, "references to light and illumination contexts" ← prompts of idx 3592, "details about concert schedules and ticket sales"

- Prediction: **FAIL**
- Basis: Target fired harder on an own near-miss (41.25) than on either should-fire, so it is reactive and undiscriminating at home. The concert prompts, though, contain no light, lamp, or sun vocabulary at all.

### Pair 8 — target idx 1657, "references to the name “Tom”" ← prompts of idx 5158, "elements related to buttons in a UI or web interface"

- Prediction: **FAIL**
- Basis: Target is a clean name detector (pilot margin +6.75). The buttons prompts never mention the name Tom.

### Pair 9 — target idx 2081, "periods and punctuation that signify the end of sentences" ← prompts of idx 1501, "moments of surprise or unexpected events, particularly those that are positive or celebratory in nature."

- Prediction: **FAIL**
- Basis: Target scored 0.00 on all four of its own prompts — which end in periods, exactly as these do. Every prompt in the set ends with a period, so the source's should-fires and near-misses are indistinguishable to this feature.

### Pair 10 — target idx 2580, "references to literary works and notable authors" ← prompts of idx 1029, "references to ancient figures and mythological or legendary elements"

- Prediction: **FAIL**
- Basis: Content-adjacent pairing (mythology is literature-adjacent), but the target scored 0.00 even on prompts naming literary works and authors.

### Pair 11 — target idx 2625, "specific scientific or technical terms related to genetics and molecular biology" ← prompts of idx 2580, "references to literary works and notable authors"

- Prediction: **FAIL**
- Basis: Target scored 0.00 on all four of its own prompts. Literature text has no genetics or molecular-biology vocabulary.

### Pair 12 — target idx 3070, "concepts related to reputation and its effects" ← prompts of idx 7196, "discussions and references to issues of racism and discriminatory behaviors"

- Prediction: **FAIL**
- Basis: Target scored 0.00 on all four of its own prompts. No further basis needed.

### Pair 13 — target idx 3349, "phrases related to diversity and inclusion in various contexts" ← prompts of idx 2625, "specific scientific or technical terms related to genetics and molecular biology"

- Prediction: **FAIL**
- Basis: Target scored 0.00 on all four of its own prompts. Genetics text is not diversity-and-inclusion text.

### Pair 14 — target idx 3580, "elements of personal relationships and family connections" ← prompts of idx 869, "geographical and administrative terms related to specific regions or districts"

- Prediction: **FAIL**
- Basis: Target scored 0.00 on all four of its own prompts (autopsy: it tracks obituary formulas, not family content generally). Region prompts are administrative geography.

### Pair 15 — target idx 3592, "details about concert schedules and ticket sales" ← prompts of idx 15623, "references to the color yellow and its variations"

- Prediction: **FAIL**
- Basis: Target passed its own test thinly (margin +1.50) on concert and ticket vocabulary. The yellow prompts contain none.

### Pair 16 — target idx 4207, "expressions of “coolness” or related positive attributes" ← prompts of idx 4593, "concepts related to simplicity and straightforwardness"

- Prediction: **FAIL**
- Basis: **Flagged — least-certain tier.** Target is broadly reactive to evaluative adjectives: its own "neat trick" near-miss fired 15.50. The source should-fires use "simple" and "plainly," near-synonyms in that space. But near-miss 1 is "Simple Simon met a pieman," which contains the same trigger word and should fire just as hard, blocking the separation.

### Pair 17 — target idx 4593, "concepts related to simplicity and straightforwardness" ← prompts of idx 13230, "terms related to electricity and power infrastructure"

- Prediction: **FAIL**
- Basis: Target passed its own test (margin +4.31) on simplicity wording. Electricity prompts contain none.

### Pair 18 — target idx 5072, "terms related to medical conditions and anatomical processes" ← prompts of idx 14520, "terms related to governance and political processes"

- Prediction: **FAIL**
- Basis: Target scored 0.00 on all four of its own prompts. Governance text is not medical text.

### Pair 19 — target idx 5158, "elements related to buttons in a UI or web interface" ← prompts of idx 7223, "phrases that indicate summary or overall conclusions"

- Prediction: **FAIL**
- Basis: Autopsy showed this target is really a detector for the code token "btn"; it scored 0.00 on its own prose button prompts. Summary-phrase prose contains no code.

### Pair 20 — target idx 6515, "references to a specific shoe brand" ← prompts of idx 3349, "phrases related to diversity and inclusion in various contexts"

- Prediction: **FAIL**
- Basis: Target scored 0.00 on all four of its own prompts (autopsy: bound to one brand's page structure). Diversity prose is not shoe text.

### Pair 21 — target idx 6865, "references to personal beliefs, self-identification, and emotional experiences" ← prompts of idx 5072, "terms related to medical conditions and anatomical processes"

- Prediction: **FAIL**
- Basis: Target reacted weakly and non-discriminatively on its own test (should-fires 0.00/5.31, near-misses 0.00/3.50). Clinical prompts carry no beliefs, self-identification, or emotional-experience content.

### Pair 22 — target idx 7196, "discussions and references to issues of racism and discriminatory behaviors" ← prompts of idx 6865, "references to personal beliefs, self-identification, and emotional experiences"

- Prediction: **FAIL**
- Basis: Target scored 0.00 on all four of its own prompts. No further basis needed.

### Pair 23 — target idx 7223, "phrases that indicate summary or overall conclusions" ← prompts of idx 6515, "references to a specific shoe brand"

- Prediction: **FAIL**
- Basis: Target fired on one own should-fire (21.12) keyed to conclusion phrasing. Shoe-brand prompts contain no summary or conclusion phrases.

### Pair 24 — target idx 7467, "words related to reading devices and the eBook industry" ← prompts of idx 10276, "products related to fashion and beauty"

- Prediction: **FAIL**
- Basis: Target barely reacted even to its own eBook prompts (3.23/0.00). Fashion text has no reading-device content.

### Pair 25 — target idx 7623, "questions and inquiries about various topics or contexts" ← prompts of idx 18, "terms related to food and culinary subjects"

- Prediction: **FAIL**
- Basis: Target scored 0.00 on its own genuine questions (autopsy: it tracks forum question-post register, not questions as such). The food prompts are plain statements, not questions at all.

### Pair 26 — target idx 7798, "expressions of happiness and positive emotions" ← prompts of idx 16358, "questions and statements regarding intentions, plans, or purposes"

- Prediction: **FAIL**
- Basis: Target is the pilot's strongest clean passer (margin +11.81, near-misses 0.00/0.00), keyed to happiness vocabulary. Intention and plan prompts contain none.

### Pair 27 — target idx 8123, "references to different types and characteristics of pipes" ← prompts of idx 7467, "words related to reading devices and the eBook industry"

- Prediction: **FAIL**
- Basis: Target passed its own test (margin +0.88) on pipe vocabulary. eBook prompts contain none.

### Pair 28 — target idx 8630, "discussions related to music and artistic collaborations" ← prompts of idx 3580, "elements of personal relationships and family connections"

- Prediction: **FAIL**
- Basis: Target scored 0.00 on all four of its own prompts (autopsy: talk-show/podcast register). Family-connection statements are not that register.

### Pair 29 — target idx 8743, "negative phrases and expressions related to obligation or denial" ← prompts of idx 1657, "references to the name “Tom”"

- Prediction: **FAIL**
- Basis: Target scored 0.00 on all four of its own prompts. Sentences about a man named Tom carry no obligation or denial phrasing.

### Pair 30 — target idx 10276, "products related to fashion and beauty" ← prompts of idx 8630, "discussions related to music and artistic collaborations"

- Prediction: **FAIL**
- Basis: **Flagged — mild.** Target's own pass was the pilot's thinnest (margin +0.16), so the feature is live and a little promiscuous. The music prompts name singers, an album, and a DJ — no fashion or beauty products.

### Pair 31 — target idx 11270, "forward-looking statements regarding business projections and associated risks" ← prompts of idx 7798, "expressions of happiness and positive emotions"

- Prediction: **FAIL**
- Basis: Target fired on one own should-fire (22.88) keyed to projection and forecast language. Happiness prompts contain no business or forecast content.

### Pair 32 — target idx 12608, "terms related to control and regulation" ← prompts of idx 8743, "negative phrases and expressions related to obligation or denial"

- Prediction: **FAIL**
- Basis: **Flagged — the riskiest pair in the set.** Target fired hard on both an own should-fire (36.00) and an own near-miss (37.25) and does not discriminate cleanly even at home. The source should-fires are workplace-rule sentences ("must not share," "denied") that sit close to regulation vocabulary. Still FAIL: near-miss 1 ("You must submit the form by Friday") carries the same obligation wording and should fire too, blocking the separation. This is the single most plausible accidental pass in the design.

### Pair 33 — target idx 12964, "references to crafting materials and methods" ← prompts of idx 483, "references to the Windows operating system"

- Prediction: **FAIL**
- Basis: Target passed its own test (margin +4.56) on crafting vocabulary. Windows prompts contain none.

### Pair 34 — target idx 13230, "terms related to electricity and power infrastructure" ← prompts of idx 12608, "terms related to control and regulation"

- Prediction: **FAIL**
- Basis: **Flagged — mild.** Target is a strong clean passer (margin +10.97) on power vocabulary. The control prompts mention factories and discharge limits — industry-adjacent — but no electricity, power, or grid terms.

### Pair 35 — target idx 14520, "terms related to governance and political processes" ← prompts of idx 2081, "periods and punctuation that signify the end of sentences"

- Prediction: **FAIL**
- Basis: Target scored 0.00 on all four of its own prompts. The punctuation prompts are ordinary sentences about sentence endings.

### Pair 36 — target idx 14719, "terms related to colors and color coding" ← prompts of idx 12964, "references to crafting materials and methods"

- Prediction: **FAIL**
- Basis: Autopsy showed this target is really a detector for the literal word "color" — which its own color-naming prompts never used; it scored 0.00 throughout. The crafting prompts contain no color words and never use the word "color."

### Pair 37 — target idx 15035, "phrases that highlight the concept of “short” in various contexts" ← prompts of idx 11270, "forward-looking statements regarding business projections and associated risks"

- Prediction: **FAIL**
- Basis: **Flagged — reactive target, mechanism argued.** Target fired on everything in its own test (near-miss max 44.25) — but every one of those prompts contained the token "short," including "shortbread" and "running short." The business prompts contain no "short" in any form, so the expected pattern is flat near-zero on all four, which fails the strict rule.

### Pair 38 — target idx 15337, "mentions of the term “Mercury,” particularly in relation to its propulsion systems and legal implications" ← prompts of idx 14719, "terms related to colors and color coding"

- Prediction: **FAIL**
- Basis: Target's own pass was a coin flip (margin +0.06) built on the word "Mercury" appearing in its should-fires. The color prompts never mention Mercury.

### Pair 39 — target idx 15623, "references to the color yellow and its variations" ← prompts of idx 4207, "expressions of “coolness” or related positive attributes"

- Prediction: **FAIL**
- Basis: **Flagged — mild.** Target is broadly reactive (own near-miss fired 39.00), but its own test showed it responding to color text. The coolness prompts contain no color words of any kind.

### Pair 40 — target idx 16358, "questions and statements regarding intentions, plans, or purposes" ← prompts of idx 1302, "shipping-related terms and phrases for large items"

- Prediction: **FAIL**
- Basis: Target reacted on its own test (should-fires 11.88/0.00, near-misses up to 9.94) to intention statements. Shipping prompts are delivery logistics — "should arrive within two to three weeks" is a delivery estimate, not an intention — and contain no plan or intend language.
