# Pilot predictions — LOCKED

**Locked: Thursday, November 12, 2026, 4:28 PM EST (America/New_York). Predictions are frozen as of this timestamp. No edits after this point.**

- **What this is:** held-out validation of auto-generated feature labels on Neuronpedia. Each label is a claim written by gpt-4o-mini from a feature's strongest examples. For each of the 40 features: two prompts the label plainly covers (should-fire), two prompts close to the label that should not fire (near-miss), and a prediction written before any results exist.
- **Model:** Gemma-2-2B (`gemma-2-2b`)
- **SAE set:** Gemma Scope residual-stream, 16k width (`gemmascope-res-16k`)
- **Layer:** 12 of 26 — source ID `12-gemmascope-res-16k`
- **Pass rule (set in advance):** a label passes if both should-fire prompts activate the feature clearly above both near-miss prompts.
- **Approval basis:** Test sets drafted by Muse. Danny Gleason approved the full set on Nov 12, 2026 without line-by-line review, stating he trusts Muse's judgment, and directed that testing proceed. Predictions are frozen as of the lock timestamp; no edits after this point.
- **Test 20 note:** the label ("references to a specific shoe brand") never names the brand. The brand (Supra) was identified from the feature's own top-activating examples, fetched from the Neuronpedia API on Nov 12, 2026, before this lock.
- **Status of results at lock time:** nothing has been run. No prompt in this file had been tested when it was locked.

### Test 1 — idx 18, "terms related to food and culinary subjects" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/18


- Should-fire 1: "She simmered the tomato sauce with garlic and basil for an hour."
- Should-fire 2: "The recipe calls for two cups of flour and a pinch of salt."
- Near-miss 1: "He seasoned the report with charts before the big meeting." (culinary verb used as a metaphor; no food)
- Near-miss 2: "They ate up every word of her speech." (food idiom; no food)
- Prediction: Both should-fires clearly above both near-misses. If the idioms fire too, the feature is tracking food words rather than food topics, and the label is missing that qualifier.

### Test 2 — idx 483, "references to the Windows operating system" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/483


- Should-fire 1: "After the update, Windows kept asking him to restart the computer."
- Should-fire 2: "She installed the program on Windows 11 and it worked right away."
- Near-miss 1: "He opened the windows to let in some fresh air." (same word, household object)
- Near-miss 2: "After the update, macOS kept asking her to restart the computer." (one variable changed from should-fire 1: the OS)
- Prediction: Both should-fires clearly above both near-misses. The fresh-air sentence is the risk: if it fires there, the feature is keyed to the word "windows" itself and the label's "operating system" qualifier is wrong.

### Test 3 — idx 869, "geographical and administrative terms related to specific regions or districts" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/869


- Should-fire 1: "The county extended the filing deadline for all district residents."
- Should-fire 2: "Voters in the province approved the new tax measure."
- Near-miss 1: "The doctor examined the region around the injury." ("region" in its anatomical sense; no geography)
- Near-miss 2: "Voters approved the new tax measure." (one variable removed from should-fire 2: the province)
- Prediction: Both should-fires clearly above both near-misses. The anatomical sentence is the risk: if it fires there, the feature is keyed to the word "region" itself, and the label's geographical qualifier is wrong.

### Test 4 — idx 1029, "references to ancient figures and mythological or legendary elements" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/1029


- Should-fire 1: "Zeus hurled thunderbolts from the top of Mount Olympus."
- Should-fire 2: "The Odyssey tells of Odysseus's ten-year voyage home."
- Near-miss 1: "Alexander Fleming discovered penicillin in 1928." (a famous historical figure, but neither ancient nor mythological)
- Near-miss 2: "The novel tells of a sailor's ten-year voyage home." (should-fire 2 with the mythological names removed)
- Prediction: Both should-fires clearly above both near-misses. If the Fleming sentence fires, the feature tracks notable historical figures generally, and the label's ancient-and-mythological scope is narrower than the feature.

### Test 5 — idx 1302, "shipping-related terms and phrases for large items" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/1302


- Should-fire 1: "The sofa ships freight and should arrive within two to three weeks."
- Should-fire 2: "Oversized items are delivered by a two-person crew with inside placement."
- Near-miss 1: "The envelope ships first class and should arrive within two days." (one variable changed from should-fire 1: a large item swapped for a small one)
- Near-miss 2: "The sofa was too wide to fit through the front doorway." (a large item, but nothing is shipped or delivered)
- Prediction: Both should-fires clearly above both near-misses. If the envelope sentence fires, the feature tracks shipping language generally and the label's "large items" qualifier is wrong; if the doorway sentence fires, it is tracking large furniture, not shipping.

### Test 6 — idx 1501, "moments of surprise or unexpected events, particularly those that are positive or celebratory in nature." (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/1501


- Should-fire 1: "To everyone's delight, the whole office surprised her with a party on her last day."
- Should-fire 2: "Against all odds, the underdog team won the championship in the final seconds."
- Near-miss 1: "To everyone's horror, the inspection revealed cracks in the bridge's main support." (a surprise, but a negative one)
- Near-miss 2: "As scheduled, the whole office celebrated her promotion with a party on her last day." (a celebration with the surprise removed; close to should-fire 1)
- Prediction: Both should-fires clearly above both near-misses. The ambiguity is the label's "positive or celebratory" qualifier: if the horror sentence fires as high as the parties, the feature tracks surprise alone and the qualifier is wrong.

### Test 7 — idx 1643, "references to light and illumination contexts" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/1643


- Should-fire 1: "She turned on the lamp so she could read in the dark room."
- Should-fire 2: "Sunlight streamed through the window all morning."
- Near-miss 1: "The suitcase was light enough to carry with one hand." ("light" as weight, not illumination)
- Near-miss 2: "She turned on the radio so she could read in the dark room." (one variable changed from should-fire 1: the lamp swapped for a radio)
- Prediction: Both should-fires clearly above both near-misses. If the suitcase sentence fires, the feature is keyed to the word "light" in any sense; if the radio sentence fires, it is tracking the indoor-evening scene rather than light itself.

### Test 8 — idx 1657, "references to the name “Tom”" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/1657


- Should-fire 1: "Tom fixed the sink before lunch."
- Should-fire 2: "I emailed Tom about moving the meeting to Friday."
- Near-miss 1: "She sliced the tomatoes for the salad." (string probe: the letters T-o-m inside another word)
- Near-miss 2: "John fixed the sink before lunch." (one variable changed from should-fire 1: the name)
- Prediction: Both should-fires clearly above both near-misses. The tomato sentence is the risk: if it fires there, the feature is keyed to the letter sequence T-o-m, not to the name, and the label is wrong about what it detects.

### Test 9 — idx 2081, "periods and punctuation that signify the end of sentences" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/2081


- Should-fire 1: "The meeting ended early."
- Should-fire 2: "She sold the car on Tuesday."
- Near-miss 1: "Did the meeting end early?" (one variable changed from should-fire 1: the final punctuation)
- Near-miss 2: "The trial period lasted six weeks." (the word "period" in its time-span sense)
- Prediction: Both should-fires clearly above both near-misses. Two risks: every written sentence ends in some punctuation, so the question mark staying quiet is the real discriminator; and if the time-span sentence fires on the word "period," the feature is keyed to the word, not to sentence-final punctuation.

### Test 10 — idx 2580, "references to literary works and notable authors" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/2580


- Should-fire 1: "She assigned her students the first three chapters of Pride and Prejudice."
- Should-fire 2: "Shakespeare wrote Hamlet while he was living in London."
- Near-miss 1: "She assigned her students the first three chapters of the biology textbook." (one variable changed from should-fire 1: a literary work swapped for a textbook)
- Near-miss 2: "The library reshelved the returned books on Tuesday afternoon." (books, but no literary work or author named)
- Prediction: Both should-fires clearly above both near-misses. If the textbook sentence fires, the feature tracks books and assigned reading generally, and the label's literary qualifier is wrong.

### Test 11 — idx 2625, "specific scientific or technical terms related to genetics and molecular biology" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/2625


- Should-fire 1: "The mutation in the BRCA1 gene raises the risk of breast cancer."
- Should-fire 2: "Researchers sequenced the DNA of the oldest sample in the lab."
- Near-miss 1: "He inherited his grandfather's watch and his father's sense of humor." (inheritance in its everyday sense; no genetics terms)
- Near-miss 2: "Researchers photographed the oldest sample in the lab." (one variable changed from should-fire 2: sequenced swapped for photographed)
- Prediction: Both should-fires clearly above both near-misses. If the inheritance sentence fires, the feature tracks heredity talk generally, and the label's "scientific or technical terms" qualifier is wrong.

### Test 12 — idx 3070, "concepts related to reputation and its effects" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/3070


- Should-fire 1: "The scandal ruined the senator's reputation overnight."
- Should-fire 2: "The restaurant built its reputation on fresh ingredients and fair prices."
- Near-miss 1: "The scandal ruined the senator's career overnight." (one variable changed from should-fire 1: reputation swapped for career)
- Near-miss 2: "Everyone in town knew his name, though few had ever met him." (being widely known, with nothing said about reputation)
- Prediction: Both should-fires clearly above both near-misses. The ambiguity is reputation versus fame: if the widely-known sentence fires, the feature tracks public recognition generally, and the label's focus on reputation is too narrow.

### Test 13 — idx 3349, "phrases related to diversity and inclusion in various contexts" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/3349


- Should-fire 1: "The company expanded its diversity training for all new managers."
- Should-fire 2: "The scholarship program aims to include students from underrepresented backgrounds."
- Near-miss 1: "The garden showed a real diversity of plant species this spring." ("diversity" in its biological sense)
- Near-miss 2: "The company expanded its safety training for all new managers." (one variable changed from should-fire 1: diversity swapped for safety)
- Prediction: Both should-fires clearly above both near-misses. The ambiguity is the label's phrase "in various contexts": read plainly the label is about social diversity and inclusion, but if the garden sentence fires, that phrase is doing more work than it should.

### Test 14 — idx 3580, "elements of personal relationships and family connections" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/3580


- Should-fire 1: "She calls her mother every Sunday without fail."
- Should-fire 2: "Their friendship deepened after they became roommates in college."
- Near-miss 1: "She calls her accountant every April without fail." (one variable changed from should-fire 1: a family member swapped for a professional contact)
- Near-miss 2: "The company deepened its partnership with the supplier after the merger." (a connection in the corporate sense; close to should-fire 2)
- Prediction: Both should-fires clearly above both near-misses. If the merger sentence fires, the feature tracks connection language generally, including business relationships, and the label's "personal" qualifier is wrong.

### Test 15 — idx 3592, "details about concert schedules and ticket sales" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/3592


- Should-fire 1: "Tickets for Friday's concert go on sale at noon tomorrow."
- Should-fire 2: "The arena posted the band's tour dates for the spring."
- Near-miss 1: "Tickets for Friday's movie go on sale at noon tomorrow." (one variable changed from should-fire 1: concert swapped for movie)
- Near-miss 2: "The band rehearsed the new songs all week before the spring tour." (the band and the tour, but no schedule and no ticket sales)
- Prediction: Both should-fires clearly above both near-misses. If the movie sentence fires, the feature tracks ticket sales for any event and the label's concert focus is too narrow; if the rehearsal sentence fires, it tracks bands and tours generally.

### Test 16 — idx 4207, "expressions of “coolness” or related positive attributes" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/4207


- Should-fire 1: "She has an effortlessly cool style that everyone at school admires."
- Should-fire 2: "That was a really cool trick; the whole crowd cheered."
- Near-miss 1: "The soup had gone cool by the time he sat down to eat." ("cool" as temperature)
- Near-miss 2: "That was a really neat trick; the whole crowd cheered." (one variable changed from should-fire 2: cool swapped for a near-synonym)
- Prediction: Both should-fires clearly above both near-misses. The ambiguity is word versus concept: if "neat" fires like "cool," the feature tracks positive appraisal generally and the label works as a concept label; if the soup sentence fires, it is keyed to the word in all its senses.

### Test 17 — idx 4593, "concepts related to simplicity and straightforwardness" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/4593


- Should-fire 1: "The instructions were simple: just press the green button and wait."
- Should-fire 2: "To put it plainly, the plan will not work as written."
- Near-miss 1: "Simple Simon met a pieman going to the fair." (the word "simple" as part of a name, in a nursery rhyme)
- Near-miss 2: "To put it bluntly, the plan will not work as written." (one variable changed from should-fire 2: plainly swapped for bluntly)
- Prediction: Both should-fires clearly above both near-misses. The ambiguity is that the label bundles two ideas, simplicity and straightforwardness: a split result, firing on one pair but not the other, would mean the label describes only half of what the feature does.

### Test 18 — idx 5072, "terms related to medical conditions and anatomical processes" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/5072


- Should-fire 1: "His diabetes requires him to check his blood sugar every morning."
- Should-fire 2: "The MRI showed a small tear in the ligament of her left knee."
- Near-miss 1: "His schedule requires him to check his email every morning." (should-fire 1's frame with the medical content swapped out)
- Near-miss 2: "The photograph showed a small tear in the fabric of her left sleeve." (one variable changed from should-fire 2: a torn ligament swapped for torn fabric)
- Prediction: Both should-fires clearly above both near-misses. If the sleeve sentence fires on the word "tear," the feature is keyed to the word across senses; if the email sentence fires, it is tracking daily-routine frames rather than medicine.

### Test 19 — idx 5158, "elements related to buttons in a UI or web interface" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/5158


- Should-fire 1: "Click the blue button in the top right corner to submit the form."
- Should-fire 2: "The download button appears once the file is ready."
- Near-miss 1: "She sewed the missing button back onto his coat." (a clothing button)
- Near-miss 2: "Click the blue link in the top right corner to submit the form." (one variable changed from should-fire 1: button swapped for link)
- Prediction: Both should-fires clearly above both near-misses. If the coat sentence fires, the feature is keyed to the word "button" in any sense, and the label's UI qualifier is wrong.

### Test 20 — idx 6515, "references to a specific shoe brand" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/6515

**Brand identified at drafting (Nov 12, 2026):** the label never names the brand, so the brand was identified from the feature's own top-activating examples, fetched from the Neuronpedia API: they are dominated by the phrase "supra shoes" (peak activation on the token "supra"), and no other brand appears. The brand is Supra.

- Should-fire 1: "He laced up his new Supra shoes before heading to the skate park."
- Should-fire 2: "Supra just released a new colorway of its Skytop high-tops."
- Near-miss 1: "He laced up his new Nike shoes before heading to the skate park." (one variable changed from should-fire 1: the brand)
- Near-miss 2: "She tied her running shoes and headed out for her morning jog." (shoes with no brand named)
- Prediction: Both should-fires clearly above both near-misses. The risk is the Nike sentence: if another brand fires as strongly as Supra, the feature is about shoes generally and the label over-specifies, claiming one brand where the feature tracks footwear as a whole.

### Test 21 — idx 6865, "references to personal beliefs, self-identification, and emotional experiences" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/6865


- Should-fire 1: "As a lifelong vegetarian, she believes no meal is worth an animal's life."
- Should-fire 2: "He identifies as an independent and votes that way in every election."
- Near-miss 1: "As a lifelong resident, she knows every street in the neighborhood." (a lifelong self-description with no belief or identity claim)
- Near-miss 2: "He is registered as an independent and votes that way in every election." (should-fire 2 with the self-identification removed; a registration fact instead)
- Prediction: Both should-fires clearly above both near-misses. The ambiguity is that the label bundles beliefs, self-identification, and emotional experiences: if only one kind fires, the label overstates the feature's range by listing all three.

### Test 22 — idx 7196, "discussions and references to issues of racism and discriminatory behaviors" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/7196


- Should-fire 1: "The lawsuit alleged that the landlord refused to rent to Black families."
- Should-fire 2: "The report documented racial slurs directed at employees in the warehouse."
- Near-miss 1: "The lawsuit alleged that the landlord refused to rent to families with dogs." (one variable changed from should-fire 1: the protected class swapped for a pet policy)
- Near-miss 2: "The report documented rude comments directed at employees in the warehouse." (one variable changed from should-fire 2: racial slurs swapped for rude comments)
- Prediction: Both should-fires clearly above both near-misses. The ambiguity: the label also claims discriminatory behavior generally, so if the dog sentence fires, that is a judgment call about the label's scope rather than a clean failure; the slur swap is the sharper test.

### Test 23 — idx 7223, "phrases that indicate summary or overall conclusions" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/7223


- Should-fire 1: "In summary, the committee approved the budget with only minor changes."
- Should-fire 2: "All in all, the experiment was a success despite the early setbacks."
- Near-miss 1: "In the summary she wrote for the newsletter, the committee's decision filled two pages." ("summary" as a noun naming a document, not a concluding phrase)
- Near-miss 2: "During the meeting, the committee approved the budget with only minor changes." (should-fire 1's content with the summary phrase removed)
- Prediction: Both should-fires clearly above both near-misses. If the newsletter sentence fires, the feature is keyed to the word "summary" wherever it appears, not to phrases that signal a conclusion.

### Test 24 — idx 7467, "words related to reading devices and the eBook industry" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/7467


- Should-fire 1: "She loaded three new novels onto her Kindle before the flight."
- Should-fire 2: "The eBook edition includes a searchable index and linked footnotes."
- Near-miss 1: "She bought three new novels at the bookstore before the flight." (the same reading material in print; should-fire 1 with the device removed)
- Near-miss 2: "The print edition includes a detailed index and extensive footnotes." (one variable changed from should-fire 2: eBook swapped for print)
- Prediction: Both should-fires clearly above both near-misses. If the print sentences fire, the feature tracks books and publishing generally, and the label's device-and-eBook focus is wrong.

### Test 25 — idx 7623, "questions and inquiries about various topics or contexts" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/7623


- Should-fire 1: "What time does the train leave for Chicago?"
- Should-fire 2: "She asked whether the store would be open on Sunday."
- Near-miss 1: "The train leaves for Chicago at six." (should-fire 1's content phrased as a statement)
- Near-miss 2: "Tell me what time the train leaves for Chicago." (a request for the same information, phrased as a command rather than a question)
- Prediction: Both should-fires clearly above both near-misses. The ambiguity is what counts as an inquiry: if the command fires, the feature tracks information-seeking generally, not questions as such, and the label never says which it means.

### Test 26 — idx 7798, "expressions of happiness and positive emotions" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/7798


- Should-fire 1: "She beamed with joy when she heard the news."
- Should-fire 2: "The children were delighted by the surprise visit from their grandparents."
- Near-miss 1: "She kept a neutral expression when she heard the news." (should-fire 1's frame with the emotion swapped out)
- Near-miss 2: "He smiled politely at the camera for the company photo." (a smile as a social gesture, with no happiness behind it)
- Prediction: Both should-fires clearly above both near-misses. If the polite smile fires, the feature tracks the outward sign of happiness rather than the emotion itself, and the label confuses the two.

### Test 27 — idx 8123, "references to different types and characteristics of pipes" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/8123


- Should-fire 1: "The plumber replaced the corroded copper pipes under the sink."
- Should-fire 2: "He cleaned his tobacco pipe and set it down by the ashtray."
- Near-miss 1: "The plumber replaced the corroded copper wires under the sink." (one variable changed from should-fire 1: pipes swapped for wires)
- Near-miss 2: "She piped the frosting onto the cake in neat rows." ("piped" as a baking verb)
- Prediction: Both should-fires clearly above both near-misses. If the frosting sentence fires, the feature is keyed to the word stem "pipe" in any form, not to pipes as objects, and the label's talk of types and characteristics of pipes is wrong.

### Test 28 — idx 8630, "discussions related to music and artistic collaborations" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/8630


- Should-fire 1: "The two singers collaborated on a duet for the charity album."
- Should-fire 2: "Her new album pairs her with a jazz pianist from New Orleans."
- Near-miss 1: "The two engineers collaborated on a design for the charity gala." (a collaboration with the music removed)
- Near-miss 2: "The DJ played records at the party until midnight." (music with no collaboration)
- Prediction: Both should-fires clearly above both near-misses. The label joins music and collaboration: if either near-miss fires, the feature tracks only one half of the label, and which half fires says which.

### Test 29 — idx 8743, "negative phrases and expressions related to obligation or denial" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/8743


- Should-fire 1: "Employees must not share their passwords with anyone."
- Should-fire 2: "He denied ever seeing the missing files."
- Near-miss 1: "You must submit the form by Friday." (an obligation with no negation and no denial)
- Near-miss 2: "He confirmed that he had seen the missing files." (one variable changed from should-fire 2: denied swapped for confirmed)
- Prediction: Both should-fires clearly above both near-misses. The ambiguity is that the label bundles obligation with denial: if only the "must not" sentence fires, the feature is about negated obligation and the denial half of the label is wrong, and the reverse if only the denial fires.

### Test 30 — idx 10276, "products related to fashion and beauty" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/10276


- Should-fire 1: "She bought a new lipstick and a bottle of foundation at the department store."
- Should-fire 2: "The boutique's spring collection features linen dresses and straw hats."
- Near-miss 1: "She bought a new notebook and a bottle of glue at the department store." (should-fire 1's frame with the products swapped for office supplies)
- Near-miss 2: "The hardware store's spring display features garden hoses and sprinklers." (a seasonal retail display, but not fashion or beauty)
- Prediction: Both should-fires clearly above both near-misses. If the hardware sentence fires, the feature tracks retail and product talk generally, and the label's fashion-and-beauty scope is wrong.

### Test 31 — idx 11270, "forward-looking statements regarding business projections and associated risks" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/11270


- Should-fire 1: "The company expects revenue to grow by ten percent next year."
- Should-fire 2: "Management warned that future results may be affected by rising supply costs."
- Near-miss 1: "The company reported that revenue grew by ten percent last year." (one variable changed from should-fire 1: a projection swapped for a report of the past)
- Near-miss 2: "She expects the train to arrive about ten minutes late tonight." (an expectation about the future, outside any business context)
- Prediction: Both should-fires clearly above both near-misses. If the train sentence fires, the feature tracks future-oriented language generally and the label's business framing is wrong; if the last-year sentence fires, it is not tracking tense at all.

### Test 32 — idx 12608, "terms related to control and regulation" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/12608


- Should-fire 1: "New regulations limit how much factories may discharge into the river."
- Should-fire 2: "The pilot kept control of the aircraft through the turbulence."
- Near-miss 1: "New guidelines suggest how much factories may discharge into the river." (one variable changed from should-fire 1: binding regulations swapped for advisory guidelines)
- Near-miss 2: "He controlled his temper throughout the argument." ("control" as self-restraint, a third sense of the word)
- Prediction: Both should-fires clearly above both near-misses. The ambiguity is that the label bundles legal regulation with physical control: a split result would mean one label is covering what behaves like two different features, and the temper sentence tests whether it is tracking the word across all its senses.

### Test 33 — idx 12964, "references to crafting materials and methods" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/12964


- Should-fire 1: "She bought wool yarn and a set of knitting needles at the craft store."
- Should-fire 2: "To make the wreath, hot-glue the pinecones to a wire frame."
- Near-miss 1: "She bought wool socks and a set of kitchen knives at the department store." (should-fire 1's frame with craft supplies swapped for finished goods)
- Near-miss 2: "The factory knits its sweaters on industrial machines." (the same materials and methods at industrial scale, not crafting)
- Prediction: Both should-fires clearly above both near-misses. If the factory sentence fires, the feature tracks textile materials and methods generally, and the label's crafting framing is wrong.

### Test 34 — idx 13230, "terms related to electricity and power infrastructure" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/13230


- Should-fire 1: "The storm knocked out power lines across the county."
- Should-fire 2: "The new substation will supply electricity to the growing suburbs."
- Near-miss 1: "The storm knocked out fences across the county." (one variable changed from should-fire 1: power lines swapped for fences)
- Near-miss 2: "The mayor's power grew as the council deferred to him on every vote." ("power" in its political sense)
- Prediction: Both should-fires clearly above both near-misses. If the mayor sentence fires, the feature is keyed to the word "power" across senses, and the label's infrastructure qualifier is wrong.

### Test 35 — idx 14520, "terms related to governance and political processes" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/14520


- Should-fire 1: "Parliament voted to approve the new budget on Tuesday."
- Should-fire 2: "The city council debated the zoning proposal for three hours."
- Near-miss 1: "The committee voted to approve the new budget on Tuesday." (one variable changed from should-fire 1: a legislature swapped for a generic committee)
- Near-miss 2: "The city council debated which restaurant to book for the holiday party." (the same governing body, on a non-governance topic)
- Prediction: Both should-fires clearly above both near-misses. The ambiguity is where governance ends and ordinary group decision-making begins: if the committee sentence fires as high as Parliament, the feature tracks collective voting generally, not governance as such.

### Test 36 — idx 14719, "terms related to colors and color coding" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/14719


- Should-fire 1: "The red wire connects to the positive terminal, and the black wire to the negative."
- Should-fire 2: "She painted the kitchen walls a soft green."
- Near-miss 1: "The thick wire connects to the positive terminal, and the thin wire to the negative." (one variable changed from should-fire 1: the colors swapped for thicknesses)
- Near-miss 2: "She felt blue all weekend after hearing the news." (a color word used as an emotion idiom)
- Prediction: Both should-fires clearly above both near-misses. If the idiom fires, the feature is keyed to color words wherever they appear, including figurative uses the label never mentions.

### Test 37 — idx 15035, "phrases that highlight the concept of “short” in various contexts" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/15035


- Should-fire 1: "He is too short to reach the top shelf."
- Should-fire 2: "It was a short meeting, over in ten minutes."
- Near-miss 1: "She ordered a shortbread cookie with her tea." (string probe: "short" inside another word, carrying no meaning of shortness)
- Near-miss 2: "We are running short on flour, so add it to the list." ("short" in its shortage sense)
- Prediction: Both should-fires clearly above both near-misses. The ambiguity is the label's phrase "in various contexts," which makes it hard to falsify at all: the shortbread probe is the clean test, since if it fires, the feature is keyed to the word, not the concept. I read "the concept of short" as shortness of height, length, or time, so the shortage sentence should stay quiet; under a looser reading it would count, and that looseness is the label's fault, not the feature's.

### Test 38 — idx 15337, "mentions of the term “Mercury,” particularly in relation to its propulsion systems and legal implications" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/15337


- Should-fire 1: "He replaced the prop on his Mercury outboard before the fishing trip."
- Should-fire 2: "Her Mercury auto policy lapsed after she missed two payments."
- Near-miss 1: "Mercury is the smallest planet and the closest one to the Sun." (the same word in its astronomy sense)
- Near-miss 2: "He replaced the prop on his Yamaha outboard before the fishing trip." (one variable changed from should-fire 1: the brand)
- Prediction: Both should-fires clearly above both near-misses. The risk is that the label bundles unrelated senses of one word, propulsion and insurance-legal: if the planet sentence fires as high as the others, the feature is simply the token "Mercury," and the propulsion-and-legal framing is an artifact of the examples the label was written from.

### Test 39 — idx 15623, "references to the color yellow and its variations" (concrete)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/15623


- Should-fire 1: "The school bus was painted a bright yellow."
- Should-fire 2: "She wore a yellow scarf with her gray coat."
- Near-miss 1: "The school bus was painted a bright orange." (one variable changed from should-fire 1: the color)
- Near-miss 2: "The old newspaper had yellowed in the attic boxes." ("yellow" as a verb of aging, not a color being described)
- Prediction: Both should-fires clearly above both near-misses. If the yellowed sentence fires as high, the feature tracks the word stem rather than the color; if the orange sentence fires, it tracks bright warm colors generally and the label is too specific.

### Test 40 — idx 16358, "questions and statements regarding intentions, plans, or purposes" (slippery)

Neuronpedia: https://www.neuronpedia.org/gemma-2-2b/12-gemmascope-res-16k/16358


- Should-fire 1: "I plan to finish the report before the deadline."
- Should-fire 2: "She intends to apply for the grant next spring."
- Near-miss 1: "I finished the report before the deadline." (one variable changed from should-fire 1: the stated plan removed, the act reported instead)
- Near-miss 2: "The purpose of the hammer is to drive nails." ("purpose" belonging to an object, with no one's intention involved)
- Prediction: Both should-fires clearly above both near-misses. The ambiguity is whether an object's purpose counts: if the hammer sentence fires, the feature tracks the word "purpose" and its kin rather than intentions as such, and the label needs that split made explicit.
