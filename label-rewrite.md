# Label-rewrite test set — corrected labels for the 28 failed pilot features

Drafted November 12, 2026. Drafting only: no activations have been run for this set.

Sources: pilot results (results-summary.md, results-raw.json), follow-up part 1 (silent-features-addendum.md, five features), follow-up part 2 (silent-features-addendum-part2.md, twelve features). The remaining 11 failures were partial fires or near-miss bleeds in the pilot; their diagnoses below are read off the pilot score patterns and peak tokens.

**Standing prediction, registered before any run:** every corrected label below is predicted to PASS its own test under the pilot's pre-registered rule — min(should-fire) > max(near-miss), each value the feature's max activation across tokens for that prompt. That prediction is the point of the exercise: if evidence-based labels cannot pass either, the problem is deeper than label wording.

Prompts for each corrected label are in label-rewrite-prompts.json. All prompts are fresh: none reuses a pilot prompt, a follow-up probe, or a stored example text. Near-misses keep the should-fire's shape and swap one element so the corrected label no longer applies.

Outcome: 21 corrected labels, 7 features with no corrected label offered.

---

## Corrected labels (21)

### idx 18 — pilot test 1
- **Original label:** "terms related to food and culinary subjects"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** Displaced center of mass: strongest stored peaks and probes are academic field/institution names ("College of Architecture and Environmental Design" 31.1) and a genomics phrase ("cell death and survival" 34.0); food sentences score 0.
- **Corrected label (12 words):** "Academic discipline and institution names, plus the phrase 'cell death and survival'"

### idx 869 — pilot test 3
- **Original label:** "geographical and administrative terms related to specific regions or districts"
- **Pilot outcome:** FAIL — SF 0.00, 13.88; NM 0.00, 0.00 (one should-fire silent).
- **Diagnosis:** Only the "province" prompt fired (13.88, peak on "province"); the county/district wording scored 0. Evidence rests on a single positive, so the corrected label is deliberately narrow.
- **Corrected label (6 words):** "References to provinces as administrative districts"

### idx 1029 — pilot test 4
- **Original label:** "references to ancient figures and mythological or legendary elements"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** Word-form/culture-specific detector: Chinese proper names and terms fire ("Tianxiang…" 25.1, peak on a name fragment; "Chang'e" 7.1); Greek mythology scores 0.
- **Corrected label (10 words):** "Chinese proper names and terms, including historical and mythological figures"

### idx 1501 — pilot test 6
- **Original label:** "moments of surprise or unexpected events, particularly those that are positive or celebratory in nature."
- **Pilot outcome:** FAIL — SF 54.00, 0.00; NM 0.00, 15.44; margin −15.44 (a should-fire silent, a near-miss fired).
- **Diagnosis:** Fires on surprise-celebration phrasing ("surprised her with a party" 54.0, peak on "with"); celebration without surprise scored 15.44, an against-all-odds win scored 0. Narrower than "surprise or celebratory moments."
- **Corrected label (10 words):** "Moments when someone is surprised with a celebration or party"

### idx 1643 — pilot test 7
- **Original label:** "references to light and illumination contexts"
- **Pilot outcome:** FAIL — SF 7.94, 17.75; NM 41.25, 8.56; margin −33.31 (weight-sense near-miss swamped both should-fires).
- **Diagnosis:** Word-form detector across senses: the weight sense of "light" (41.25) dominates; illumination contexts fire weakly (7.94–17.75).
- **Corrected label (11 words):** "The word 'light' in any sense, most strongly meaning not heavy"

### idx 2580 — pilot test 10
- **Original label:** "references to literary works and notable authors"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** Register detector: recommendation/comparison language about creative works fires ("will appeal to fans of Shakespeare and Dickens" 39.0; game blurb "similar in style to" 33.5); plain references to works and authors score 0.
- **Corrected label (11 words):** "Recommendation and comparison language about books, films, and other creative works"

### idx 3580 — pilot test 14
- **Original label:** "elements of personal relationships and family connections"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** Register detector: obituary formulas fire ("survived by his loving wife" 33.25; "preceded in death by" 25.1); ordinary family sentences score 0.
- **Corrected label (9 words):** "Obituary formulas about the deceased's surviving and predeceasing relatives"

### idx 5072 — pilot test 18
- **Original label:** "terms related to medical conditions and anatomical processes"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** Register detector: dense clinical terminology in journal register fires (23.25, 16.1); plain patient-language medical sentences score 0.
- **Corrected label (7 words):** "Dense clinical terminology in medical journal register"

### idx 5158 — pilot test 19
- **Original label:** "elements related to buttons in a UI or web interface"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** Word-form detector: the code token "btn" fires (`<button class="btn btn-primary">` 45.0; CSS ".btn-default" 41.75); the English word "button" in prose scores 0.
- **Corrected label (10 words):** "The code token 'btn' in markup, CSS, and class names"

### idx 6865 — pilot test 21
- **Original label:** "references to personal beliefs, self-identification, and emotional experiences"
- **Pilot outcome:** FAIL — SF 0.00, 5.31; NM 0.00, 3.50; margin −3.50 (weak fire, near-miss close behind).
- **Diagnosis:** Only political self-identification fired, weakly: "identifies as an independent" 5.31 (peak "as") vs "registered as an independent" 3.50; a general belief statement scored 0.
- **Corrected label (7 words):** "Statements identifying oneself as a political independent"

### idx 7223 — pilot test 23
- **Original label:** "phrases that indicate summary or overall conclusions"
- **Pilot outcome:** FAIL — SF 0.00, 21.12; NM 0.00, 0.00; margin 0.00 (one should-fire silent).
- **Diagnosis:** Single stock phrase: "All in all" fired (21.12, peak on "all"); "In summary" scored 0.
- **Corrected label (9 words):** "The phrase 'all in all' used to sum up"

### idx 7467 — pilot test 24
- **Original label:** "words related to reading devices and the eBook industry"
- **Pilot outcome:** FAIL — SF 3.23, 0.00; NM 0.00, 0.00; margin 0.00 (one weak fire, one silent).
- **Diagnosis:** Brand-token detector: only "Kindle" fired, weakly (3.23, peak on "Kindle"); a generic eBook-edition sentence scored 0.
- **Corrected label (4 words):** "Mentions of Kindle e-readers"

### idx 7623 — pilot test 25
- **Original label:** "questions and inquiries about various topics or contexts"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** Register detector: forum-style question posts fire (question plus follow-up text and thread furniture, 18.0); a clean bare question scores 0.
- **Corrected label (9 words):** "Forum-style question posts with follow-up text and thread furniture"

### idx 8630 — pilot test 28
- **Original label:** "discussions related to music and artistic collaborations"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** Register detector: talk-show/podcast guest segments fire ("the host talks with a jazz pianist" 35.5; radio appearance 33.0); music news and collaboration sentences score 0.
- **Corrected label (9 words):** "Talk-show and podcast segments introducing or interviewing a guest"

### idx 8743 — pilot test 29
- **Original label:** "negative phrases and expressions related to obligation or denial"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** Word-form detector: the words "or" (33.0) and "nor" (16.6) fire; obligation and denial sentences score 0.
- **Corrected label (9 words):** "The coordinating words 'or' and 'nor' in running text"

### idx 11270 — pilot test 31
- **Original label:** "forward-looking statements regarding business projections and associated risks"
- **Pilot outcome:** FAIL — SF 0.00, 22.88; NM 0.00, 0.00; margin 0.00 (one should-fire silent).
- **Diagnosis:** Hedged risk-warning register: "future results may be affected by…" fired (22.88, peak on "may"); a plain "expects revenue to grow" projection scored 0.
- **Corrected label (10 words):** "Business risk warnings using hedged modals like 'may be affected'"

### idx 12608 — pilot test 32
- **Original label:** "terms related to control and regulation"
- **Pilot outcome:** FAIL — SF 0.00, 36.00; NM 0.00, 37.25; margin −37.25 (near-miss beat the best should-fire).
- **Diagnosis:** Word-form detector across senses: "control" (aircraft, 36.0) and "controlled" (temper, 37.25) both fire; the regulation sentence scored 0.
- **Corrected label (8 words):** "The words 'control' and 'controlled' in any sense"

### idx 14719 — pilot test 36
- **Original label:** "terms related to colors and color coding"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** Word-form detector: the word "color" itself fires in any form ("The color of the first wire is red" 46.0; code constant COLOR_MENU_TEXT 43.0); color terms without the word score 0.
- **Corrected label (9 words):** "The word 'color' itself, in any of its forms"

### idx 15035 — pilot test 37
- **Original label:** "phrases that highlight the concept of “short” in various contexts"
- **Pilot outcome:** FAIL — SF 33.50, 43.75; NM 44.25, 37.75; margin −10.75 (both near-misses beat one should-fire).
- **Diagnosis:** Token detector, not concept detector: "shortbread" (44.25) beat both plain "short" should-fires, and the scarcity sense ("running short on flour" 37.75) also fired; peaks sit on the token "short," including inside compounds.
- **Corrected label (8 words):** "The token 'short', including inside compounds like 'shortbread'"

### idx 15623 — pilot test 39
- **Original label:** "references to the color yellow and its variations"
- **Pilot outcome:** FAIL — SF 33.50, 36.50; NM 22.88, 39.00; margin −5.50 (the "yellowed" near-miss beat both should-fires).
- **Diagnosis:** Token-level response that overshoots the label: "yellowed" (39.0) outscored plain yellow sentences, and orange also fired (22.88); color specificity is weaker than the label claims.
- **Corrected label (12 words):** "The token 'yellow', including inside 'yellowed', with weaker response to other colors"

### idx 16358 — pilot test 40
- **Original label:** "questions and statements regarding intentions, plans, or purposes"
- **Pilot outcome:** FAIL — SF 11.88, 0.00; NM 4.47, 9.94; margin −9.94 (one should-fire silent, near-miss close).
- **Diagnosis:** Specific phrasings only: "I plan to…" fired (11.88) and "the purpose of the hammer" scored 9.94, while "intends to…" scored 0.
- **Corrected label (9 words):** "'Plan to' intention statements and 'the purpose of' phrasing"

---

## No corrected label offered (7)

### idx 2081 — pilot test 9
- **Original label:** "periods and punctuation that signify the end of sentences"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** Document-structure bound: strongest stored peaks sit on the document-boundary token following a period in long formatted text; ten probes of ordinary sentence periods scored 0, and only a legal citation cluster reproduced a weak response (4.09).
- **Corrected label:** None offered — the behavior barely reproduces in isolated text, so any one-line label would describe the stored documents, not a testable trigger.

### idx 2625 — pilot test 11
- **Original label:** "specific scientific or technical terms related to genetics and molecular biology"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** Document-structure bound: 14 of 45 stored peaks sit on the document-boundary token after unrelated documents; a five-sentence genetics abstract scored 0 and only a weak Swift-code trace (7.25) reproduced.
- **Corrected label:** None offered — nothing genetic was found to fire the feature, and the reproducible residue is too weak and off-label to state as a corrected label.

### idx 3070 — pilot test 12
- **Original label:** "concepts related to reputation and its effects"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** No consistent trigger found (addendum part 2): best responses across nine probes were 6.6, 4.7, 4.6 on scattered unrelated tokens ("franchise," "reputation," "upvoted").
- **Corrected label:** None offered — no consistent trigger was found, and a corrected label would be a guess.

### idx 3349 — pilot test 13
- **Original label:** "phrases related to diversity and inclusion in various contexts"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** Document-structure bound and weak: business-page formatting produced 8.4 and 6.8; diversity prose of any kind scored 0, and the strong behavior was not reproducible in isolation.
- **Corrected label:** None offered — the only signal is weak formatting sensitivity, not a stateable trigger.

### idx 6515 — pilot test 20
- **Original label:** "references to a specific shoe brand"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero; both should-fires named the brand, Supra).
- **Diagnosis:** Document-structure bound and weak: only a ~120-token keyword-stuffed commerce paragraph repeating "supra shoes" responded (5.34); short spam and natural brand sentences scored 0.
- **Corrected label:** None offered — the response depends on document length and stuffing, not on a stateable brand trigger.

### idx 7196 — pilot test 22
- **Original label:** "discussions and references to issues of racism and discriminatory behaviors"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** No consistent trigger found (addendum part 2): a formal jury-discrimination sentence scored 0; a longer argumentative passage scored 11.9 peaking on "," and "but," not on any content word.
- **Corrected label:** None offered — no consistent trigger was found, and a corrected label would be a guess.

### idx 14520 — pilot test 35
- **Original label:** "terms related to governance and political processes"
- **Pilot outcome:** FAIL — SF 0.00, 0.00; NM 0.00, 0.00 (all-zero).
- **Diagnosis:** No consistent trigger found (addendum part 2): a Federalist-style sentence scored 28.75 and one stored-example sentence 26.6, but the Gettysburg Address and modern parliamentary sentences scored 0 — particular older prose passages, no coherent rule.
- **Corrected label:** None offered — the responses follow no coherent rule, so there is nothing accurate to state in one line.
