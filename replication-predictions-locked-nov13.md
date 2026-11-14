# Llama 3.1 8B replication — predictions LOCKED

- **Study:** Llama 3.1 8B replication of the Neuronpedia label-validation study (second-model replication of the Gemma-2-2B pilot and scale-up).
- **Model:** Llama 3.1 8B (`llama3.1-8b`)
- **SAE set:** Llama Scope residual-stream, 32k width (`llamascope-res-32k`)
- **Layer:** 16 of 32 — source ID `16-llamascope-res-32k`
- **Sample:** 80 labeled features. Draw rule: successive `rng.randrange(32768)` values from `random.Random(20261113)` over feature indices 0–32767. Draws are taken in order; each drawn index is fetched from the public Neuronpedia feature API and its label is `explanations[0].description`. Skip rule: a drawn feature with no explanations (or no description on the first explanation) is skipped and logged, as is a duplicate draw; drawing continues until 80 labeled features are held. Result here: 80 draws, 0 skips — every drawn feature carried exactly one explanation.
- **Protocol (identical to the pilot and scale-up):** per feature, two should-fire prompts that plainly express the label, two near-miss prompts that each change exactly one variable relative to a should-fire, and one binary prediction (PASS / FAIL) registered before any scoring.
- **Pass rule (set in advance):** a label passes if both should-fire prompts activate the feature clearly above both near-miss prompts (min(should-fire) > max(near-miss)).
- **Predictions in this file:** 23 PASS, 57 FAIL.
- **Authorship:** Prompts and predictions drafted by Muse; approved and LOCKED by Danny Gleason on November 13, 2026, before any scoring. At lock time, no sampled feature had been run through the activation API.
- **SHA-256:** computed at lock (November 13, 2026) and recorded in the lock commit in this repository. This file must not be edited after locking.

## Sampling log

Seed 20261113, successive `randrange(32768)` draws, in order. 80 draws, 80 kept, 0 skipped (no unlabeled features and no duplicate draws occurred).

- Draw 1: idx 11708 — kept as sample #1
- Draw 2: idx 1195 — kept as sample #2
- Draw 3: idx 8560 — kept as sample #3
- Draw 4: idx 23860 — kept as sample #4
- Draw 5: idx 630 — kept as sample #5
- Draw 6: idx 30011 — kept as sample #6
- Draw 7: idx 4305 — kept as sample #7
- Draw 8: idx 8683 — kept as sample #8
- Draw 9: idx 6228 — kept as sample #9
- Draw 10: idx 3173 — kept as sample #10
- Draw 11: idx 25655 — kept as sample #11
- Draw 12: idx 3415 — kept as sample #12
- Draw 13: idx 7190 — kept as sample #13
- Draw 14: idx 19976 — kept as sample #14
- Draw 15: idx 2036 — kept as sample #15
- Draw 16: idx 19630 — kept as sample #16
- Draw 17: idx 32748 — kept as sample #17
- Draw 18: idx 919 — kept as sample #18
- Draw 19: idx 19894 — kept as sample #19
- Draw 20: idx 28449 — kept as sample #20
- Draw 21: idx 17146 — kept as sample #21
- Draw 22: idx 3072 — kept as sample #22
- Draw 23: idx 31968 — kept as sample #23
- Draw 24: idx 25849 — kept as sample #24
- Draw 25: idx 21787 — kept as sample #25
- Draw 26: idx 18531 — kept as sample #26
- Draw 27: idx 8796 — kept as sample #27
- Draw 28: idx 10870 — kept as sample #28
- Draw 29: idx 4693 — kept as sample #29
- Draw 30: idx 23420 — kept as sample #30
- Draw 31: idx 31577 — kept as sample #31
- Draw 32: idx 25825 — kept as sample #32
- Draw 33: idx 17678 — kept as sample #33
- Draw 34: idx 25900 — kept as sample #34
- Draw 35: idx 20562 — kept as sample #35
- Draw 36: idx 3272 — kept as sample #36
- Draw 37: idx 28808 — kept as sample #37
- Draw 38: idx 27382 — kept as sample #38
- Draw 39: idx 23054 — kept as sample #39
- Draw 40: idx 30566 — kept as sample #40
- Draw 41: idx 6470 — kept as sample #41
- Draw 42: idx 18758 — kept as sample #42
- Draw 43: idx 18024 — kept as sample #43
- Draw 44: idx 1739 — kept as sample #44
- Draw 45: idx 49 — kept as sample #45
- Draw 46: idx 10317 — kept as sample #46
- Draw 47: idx 10660 — kept as sample #47
- Draw 48: idx 8211 — kept as sample #48
- Draw 49: idx 4982 — kept as sample #49
- Draw 50: idx 31073 — kept as sample #50
- Draw 51: idx 24349 — kept as sample #51
- Draw 52: idx 9470 — kept as sample #52
- Draw 53: idx 14331 — kept as sample #53
- Draw 54: idx 25296 — kept as sample #54
- Draw 55: idx 20828 — kept as sample #55
- Draw 56: idx 15837 — kept as sample #56
- Draw 57: idx 13568 — kept as sample #57
- Draw 58: idx 27458 — kept as sample #58
- Draw 59: idx 21341 — kept as sample #59
- Draw 60: idx 6140 — kept as sample #60
- Draw 61: idx 5979 — kept as sample #61
- Draw 62: idx 10256 — kept as sample #62
- Draw 63: idx 16293 — kept as sample #63
- Draw 64: idx 28474 — kept as sample #64
- Draw 65: idx 4155 — kept as sample #65
- Draw 66: idx 9085 — kept as sample #66
- Draw 67: idx 1211 — kept as sample #67
- Draw 68: idx 479 — kept as sample #68
- Draw 69: idx 11342 — kept as sample #69
- Draw 70: idx 26722 — kept as sample #70
- Draw 71: idx 8866 — kept as sample #71
- Draw 72: idx 13355 — kept as sample #72
- Draw 73: idx 31854 — kept as sample #73
- Draw 74: idx 20386 — kept as sample #74
- Draw 75: idx 3458 — kept as sample #75
- Draw 76: idx 20197 — kept as sample #76
- Draw 77: idx 123 — kept as sample #77
- Draw 78: idx 14022 — kept as sample #78
- Draw 79: idx 25833 — kept as sample #79
- Draw 80: idx 23454 — kept as sample #80

## Tests

### Test 1 — idx 11708, "references to specific locations and addresses"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/11708

- Should-fire 1: "The bakery is located at 412 Maple Street in downtown Springfield."
- Should-fire 2: "Please send the package to 88 Harbor Road, Portland, Maine."
- Near-miss 1: "The bakery is located on a quiet street downtown." (specific address removed)
- Near-miss 2: "Please send the package to my home address." (specifics removed)
- Prediction: **PASS**
- Basis: Street addresses and named places are a concrete, surface-detectable entity pattern.

### Test 2 — idx 1195, "words related to evaluation and assessment concepts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/1195

- Should-fire 1: "The committee will evaluate each proposal against the published criteria."
- Should-fire 2: "Her performance review assessed how well she met the annual goals."
- Near-miss 1: "The committee will read each proposal before the Friday deadline." (evaluation verb swapped for neutral reading)
- Near-miss 2: "Her supervisor described how busy she had been all year." (assessment element removed)
- Prediction: **FAIL**
- Basis: Abstract semantic field spanning many verbs and nouns, not one narrow pattern.

### Test 3 — idx 8560, "references to conflict or struggles within various contexts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/8560

- Should-fire 1: "The two brothers fought bitterly over their father's will."
- Should-fire 2: "She struggled for years to keep the small business alive."
- Near-miss 1: "The two brothers worked together on their father's farm." (conflict swapped for cooperation)
- Near-miss 2: "She worked for years to keep the small business alive." (struggle removed, topic kept)
- Prediction: **FAIL**
- Basis: Broad topic spanning arguments, wars, and personal hardship; no single detectable pattern.

### Test 4 — idx 23860, "terms related to sports events and gambling"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/23860

- Should-fire 1: "He placed a bet on the horse race at the track."
- Should-fire 2: "The championship game went into overtime on Sunday night."
- Near-miss 1: "He watched the horse race at the track on Saturday." (betting removed, race kept)
- Near-miss 2: "The board game went into overtime on Sunday night." (championship sport swapped for a board game)
- Prediction: **FAIL**
- Basis: Bundles two distinct domains, sports and gambling, under one label.

### Test 5 — idx 630, "elements associated with religious sacraments and their significance"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/630

- Should-fire 1: "The priest baptized the infant during Sunday mass at the cathedral."
- Should-fire 2: "They received communion together at her first Eucharist celebration."
- Near-miss 1: "The priest blessed the fishing boats during Sunday mass at the harbor." (sacrament swapped for a blessing; setting kept)
- Near-miss 2: "They lit candles together at her birthday celebration dinner." (communion swapped for a secular gathering)
- Prediction: **PASS**
- Basis: Sacraments are a small closed set of named rituals with distinctive vocabulary.

### Test 6 — idx 30011, "numerical values and their relationships in statistical or financial contexts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/30011

- Should-fire 1: "Revenue grew 14 percent last quarter, reaching 2.3 billion dollars."
- Should-fire 2: "The study found a correlation of 0.82 across 1,200 surveyed households."
- Near-miss 1: "Revenue grew steadily last quarter, reaching a record level." (numbers removed)
- Near-miss 2: "The study found a strong link across the surveyed households." (values removed, vague link kept)
- Prediction: **PASS**
- Basis: Digits, percentages, and quantities form one unitary surface pattern in quantitative prose.

### Test 7 — idx 4305, "code syntax and function definitions in programming language constructs"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/4305

- Should-fire 1: "def calculate_total(price, tax): return price * (1 + tax)"
- Should-fire 2: "function greet(name) { return 'Hello, ' + name; }"
- Near-miss 1: "The calculate function multiplies the price by one plus the tax rate." (same function described in prose; code form removed)
- Near-miss 2: "To greet someone, the program combines a greeting with their name." (prose description of the same behavior)
- Prediction: **PASS**
- Basis: Function-definition syntax is a narrow, surface-detectable code pattern.

### Test 8 — idx 8683, "elements related to horror film plotlines and character dynamics"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/8683

- Should-fire 1: "The haunted doll returns each night to torment the frightened family."
- Should-fire 2: "A lone survivor hides from the killer in the abandoned asylum."
- Near-miss 1: "The enchanted doll returns each night to delight the happy family." (horror valence flipped)
- Near-miss 2: "A lone traveler hides from the rain in the abandoned barn." (killer swapped for weather)
- Prediction: **FAIL**
- Basis: Genre plot summary is a broad topic; no narrow surface pattern distinguishes it.

### Test 9 — idx 6228, "repeated references to categories or groups"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/6228

- Should-fire 1: "The report sorts the data into three categories: age, income, and region."
- Should-fire 2: "Each group presented its findings to the other groups on Friday."
- Near-miss 1: "The report sorts the data into a single combined summary table." (categories removed)
- Near-miss 2: "Each student presented her findings to the class on Friday." (groups swapped for individuals)
- Prediction: **FAIL**
- Basis: Meta-level description of repetition, too diffuse for one feature to track.

### Test 10 — idx 3173, "phrases related to rarity and significance within various contexts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/3173

- Should-fire 1: "Such a flawless emerald is an exceptionally rare find for collectors."
- Should-fire 2: "The treaty was a landmark moment of enormous historical significance."
- Near-miss 1: "Such an emerald is a fairly common find for collectors." (rarity flipped)
- Near-miss 2: "The treaty was a routine agreement between the two towns." (significance removed)
- Prediction: **FAIL**
- Basis: Vague evaluative phrasing spanning unrelated senses of rare and significant.

### Test 11 — idx 25655, "phrases indicating a critique of systemic issues and social justice"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/25655

- Should-fire 1: "The report argues that housing policy systematically excludes low-income families."
- Should-fire 2: "Activists say the justice system fails the communities it should protect."
- Near-miss 1: "The report argues that housing policy effectively serves low-income families." (critique flipped to praise)
- Near-miss 2: "Officials say the transit system serves the communities along its routes." (justice and critique elements removed)
- Prediction: **FAIL**
- Basis: Broad ideological stance, not a concrete detectable pattern.

### Test 12 — idx 3415, "references to marine research and environmental sciences"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/3415

- Should-fire 1: "Researchers tagged the sea turtles to track their migration across the Atlantic."
- Should-fire 2: "The team sampled ocean water to measure microplastic levels near the reef."
- Near-miss 1: "Researchers tagged the cattle to track their movement across the ranch." (marine swapped for terrestrial)
- Near-miss 2: "The team sampled tap water to measure chlorine levels at the plant." (ocean environment swapped for municipal water)
- Prediction: **FAIL**
- Basis: Bundles two broad scientific fields; a topic, not a narrow pattern.

### Test 13 — idx 7190, "specific online platforms or spaces intended for community connection and resource sharing"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/7190

- Should-fire 1: "She posted the question on the community forum and got helpful replies."
- Should-fire 2: "Neighbors share tools and updates in their local Discord group chat."
- Near-miss 1: "She posted the announcement on the company bulletin board at work." (online community swapped for a physical board)
- Near-miss 2: "Neighbors share tools and updates over the garden fence each morning." (platform removed)
- Prediction: **FAIL**
- Basis: Describes platforms by their social function, which has no single surface form.

### Test 14 — idx 19976, "keywords related to mining and crushing machinery"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/19976

- Should-fire 1: "The jaw crusher reduces the ore before it reaches the conveyor belt."
- Should-fire 2: "They replaced the worn screen on the vibrating separator at the quarry plant."
- Near-miss 1: "The bread machine kneads the dough before it reaches the oven tray." (machinery domain swapped for kitchen equipment)
- Near-miss 2: "They replaced the worn filter on the air separator at the office plant." (mining separator swapped for an HVAC separator)
- Prediction: **PASS**
- Basis: A tight keyword set for specific industrial machines.

### Test 15 — idx 2036, "references to historical architecture and its features"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/2036

- Should-fire 1: "The cathedral's flying buttresses and pointed arches date to the twelfth century."
- Should-fire 2: "Workers restored the marble columns of the old courthouse facade."
- Near-miss 1: "The stadium's steel trusses and glass panels opened in twenty nineteen." (historical swapped for modern architecture)
- Near-miss 2: "Workers restored the wooden fence around the old farmhouse yard." (architectural features removed)
- Prediction: **FAIL**
- Basis: Broad topic across centuries and building types; no single narrow pattern.

### Test 16 — idx 19630, "references to transitions or changes in narrative structure"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/19630

- Should-fire 1: "The novel then shifts to the villain's perspective for three chapters."
- Should-fire 2: "At this point the story jumps forward twenty years in time."
- Near-miss 1: "The novel then settles into the hero's perspective for three chapters." (shift swapped for continuation)
- Near-miss 2: "At this point the story stays in the same year and place." (time jump removed)
- Prediction: **FAIL**
- Basis: Abstract narratological concept with no consistent surface realization.

### Test 17 — idx 32748, "programming-related terminology and syntax"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/32748

- Should-fire 1: "The variable stores the result after the loop finishes iterating."
- Should-fire 2: "You must import the library before calling its main function."
- Near-miss 1: "The container stores the result after the machine finishes cycling." (programming terms swapped for physical ones)
- Near-miss 2: "You must unlock the cabinet before using its main handle." (import and function swapped for physical actions)
- Prediction: **FAIL**
- Basis: Covers all of programming at once; too broad for one feature's pattern.

### Test 18 — idx 919, "sports-related actions and events"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/919

- Should-fire 1: "She kicked the ball past the goalkeeper in the final minute."
- Should-fire 2: "He served the ball straight down the line for an ace."
- Near-miss 1: "She kicked the can down the sidewalk on her way home." (sport action swapped for the same verb used casually)
- Near-miss 2: "He served the soup straight from the pot for the guests." (served in its dining sense)
- Prediction: **FAIL**
- Basis: All sports actions under one label is a broad topic, not one pattern.

### Test 19 — idx 19894, "dialogue and speech patterns within the text"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/19894

- Should-fire 1: ""I never said that," she replied. "You must have misheard me.""
- Should-fire 2: ""Where were you last night?" he asked quietly."
- Near-miss 1: "She replied that she had never said any such thing." (direct speech converted to reported speech; quotes removed)
- Near-miss 2: "He wondered silently where she had been the night before." (spoken question converted to an unspoken thought)
- Prediction: **PASS**
- Basis: Quoted direct speech is a concrete formatting and punctuation pattern.

### Test 20 — idx 28449, "programming syntax related to function definitions and return statements"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/28449

- Should-fire 1: "def square(x): return x * x"
- Should-fire 2: "static int max(int a, int b) { return a > b ? a : b; }"
- Near-miss 1: "The square of a number is found by multiplying it by itself." (prose about the same computation)
- Near-miss 2: "The clerk ends his shift and returns home when the shop is empty." (return as an ordinary verb)
- Prediction: **PASS**
- Basis: Return statements and function signatures are a narrow code-syntax pattern.

### Test 21 — idx 17146, "details about all-inclusive resorts and their offerings"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/17146

- Should-fire 1: "The all-inclusive resort includes meals, drinks, and airport transfers in one price."
- Should-fire 2: "Guests at the beachfront resort enjoy unlimited cocktails and free snorkeling tours."
- Near-miss 1: "The city hotel charges extra for meals, drinks, and airport transfers." (all-inclusive swapped for pay-as-you-go)
- Near-miss 2: "Guests at the mountain lodge enjoy guided hikes and free bicycle rentals." (resort offerings swapped for lodge activities)
- Prediction: **PASS**
- Basis: A narrow commercial niche with distinctive offering vocabulary.

### Test 22 — idx 3072, "instances of conflict and tension within narratives"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/3072

- Should-fire 1: "Their marriage slowly crumbled as the arguments grew louder each night."
- Should-fire 2: "The crew waited in tense silence as the storm approached the ship."
- Near-miss 1: "Their marriage slowly strengthened as the conversations grew warmer each night." (conflict flipped to strengthening)
- Near-miss 2: "The crew waited in calm silence as the sun rose over the harbor." (tension removed)
- Prediction: **FAIL**
- Basis: Any story conflict qualifies; far too broad for a single feature.

### Test 23 — idx 31968, "variations and comparisons in artistic and creative contexts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/31968

- Should-fire 1: "Unlike the first draft, the revised painting uses warmer colors throughout."
- Should-fire 2: "Her later songs are slower and more melancholy than her early work."
- Near-miss 1: "The finished painting uses warm colors and soft light throughout." (comparison removed)
- Near-miss 2: "Her new album came out last spring to positive reviews." (comparison removed)
- Prediction: **FAIL**
- Basis: Vague meta-description spanning any creative comparison.

### Test 24 — idx 25849, "terms related to satisfaction and client contentment"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/25849

- Should-fire 1: "Our clients reported high satisfaction with the new support service."
- Should-fire 2: "Customers said they were delighted with the quick, friendly help."
- Near-miss 1: "Our clients reported deep frustration with the new support service." (satisfaction flipped)
- Near-miss 2: "Customers said they were surprised by the quick, friendly help." (satisfaction swapped for surprise)
- Prediction: **FAIL**
- Basis: Diffuse sentiment vocabulary across all service contexts.

### Test 25 — idx 21787, "occurrences of the word "sum" and its variations in context"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/21787

- Should-fire 1: "The sum of the two numbers is forty-two."
- Should-fire 2: "She received a large sum of money for the painting."
- Near-miss 1: "The total of the two numbers is forty-two." (one word changed: sum to total)
- Near-miss 2: "She received a large amount of money for the painting." (sum swapped for amount)
- Prediction: **PASS**
- Basis: The label names one specific word form, the clearest kind of pattern in the pilot.

### Test 26 — idx 18531, "dates and numerical references related to events"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/18531

- Should-fire 1: "The conference took place on March 14, 2024, in Chicago."
- Should-fire 2: "He was born on June 2, 1990, the third of four children."
- Near-miss 1: "The conference took place last spring in Chicago." (date removed)
- Near-miss 2: "He was born in early summer, one of several children." (date and numbers removed)
- Prediction: **FAIL**
- Basis: Bundles dates, counts, and event references into one diffuse label.

### Test 27 — idx 8796, "references to specific airports and their connectivity"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/8796

- Should-fire 1: "Flights from Denver International connect to forty cities nonstop."
- Should-fire 2: "Passengers change planes at Heathrow for flights across Europe."
- Near-miss 1: "Flights from the regional airport connect to forty cities nonstop." (specific airport name removed)
- Near-miss 2: "Passengers change trains at the central station for trips across Europe." (airport swapped for rail)
- Prediction: **PASS**
- Basis: Named airports and hub connections form a concrete entity pattern.

### Test 28 — idx 10870, "structured data or programming syntax related to hardware devices"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/10870

- Should-fire 1: "The sensor register is set by writing 0xFF to address 0x20."
- Should-fire 2: "Each packet header contains a two-byte device identifier field."
- Near-miss 1: "The thermostat is set by turning the dial to the highest mark." (digital register swapped for an analog control)
- Near-miss 2: "Each shipping label contains a two-line customer address field." (data field swapped for a paper form field)
- Prediction: **FAIL**
- Basis: Bundles data formats, syntax, and hardware into one mixed label.

### Test 29 — idx 4693, "specific dates and related numeric values"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/4693

- Should-fire 1: "The lease begins on January 1, 2027, and ends December 31, 2027."
- Should-fire 2: "She filed the form on April 9, two days before the deadline."
- Near-miss 1: "The lease begins next year and ends the following year." (dates removed)
- Near-miss 2: "She filed the form in spring, a few days before the deadline." (specific date swapped for a season)
- Prediction: **PASS**
- Basis: Calendar dates are a narrow, surface-detectable pattern.

### Test 30 — idx 23420, "names, particularly related to people and organizations"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/23420

- Should-fire 1: "Maria Gonzalez announced that the World Health Organization would expand funding."
- Should-fire 2: "James Carter joined Microsoft as its new regional director."
- Near-miss 1: "The nurse announced that the agency would expand its funding." (names swapped for roles)
- Near-miss 2: "A young engineer joined the software company as its new regional director." (names removed)
- Prediction: **FAIL**
- Basis: All proper names at once is too broad for one feature to track.

### Test 31 — idx 31577, "references to regulations and licensing related to radio communication"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/31577

- Should-fire 1: "The FCC requires a license to operate on these radio frequencies."
- Should-fire 2: "Amateur radio operators must renew their call sign licenses every ten years."
- Near-miss 1: "The city requires a permit to operate a food truck downtown." (radio licensing swapped for another permit domain)
- Near-miss 2: "Amateur gardeners must renew their club memberships every ten years." (licensing frame kept, radio removed)
- Prediction: **PASS**
- Basis: A narrow regulatory niche with distinctive terms: FCC, frequencies, call signs.

### Test 32 — idx 25825, "concepts related to cultural identity and its components"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/25825

- Should-fire 1: "For many immigrants, language is central to their cultural identity."
- Should-fire 2: "The festival celebrates the heritage and traditions of the community."
- Near-miss 1: "For many immigrants, income is central to their household budget." (identity swapped for economics)
- Near-miss 2: "The festival celebrates the harvest and the food of the community." (heritage swapped for produce)
- Prediction: **FAIL**
- Basis: Abstract sociological concept with no single surface pattern.

### Test 33 — idx 17678, "concepts related to academic writing and the dissertation process"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/17678

- Should-fire 1: "Her dissertation committee asked for major revisions to chapter three."
- Should-fire 2: "He defended his thesis before the faculty panel last spring."
- Near-miss 1: "Her book editor asked for major revisions to chapter three." (dissertation swapped for a trade book)
- Near-miss 2: "He presented his project before the company board last spring." (thesis defense swapped for a business presentation)
- Prediction: **FAIL**
- Basis: Bundles academic-writing style with one degree ritual; too mixed.

### Test 34 — idx 25900, "terminology related to supply chain management and operations"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/25900

- Should-fire 1: "The warehouse reduced inventory by improving its logistics and procurement planning."
- Should-fire 2: "Suppliers ship components just in time to the assembly plant."
- Near-miss 1: "The kitchen reduced waste by improving its shopping and meal planning." (supply-chain terms swapped for household ones)
- Near-miss 2: "Farmers sell vegetables every morning at the outdoor market." (procurement frame removed)
- Prediction: **PASS**
- Basis: A tight professional keyword set: inventory, logistics, procurement, suppliers.

### Test 35 — idx 20562, "terms related to regulations and action plans in forestry and timber trade"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/20562

- Should-fire 1: "The forestry plan limits timber harvesting to protect old-growth stands."
- Should-fire 2: "New regulations require permits for exporting logs across the border."
- Near-miss 1: "The garden plan limits vegetable planting to protect the flower beds." (forestry swapped for gardening)
- Near-miss 2: "New guidelines require passes for exporting crafts across the border." (timber and regulations weakened to crafts and guidelines)
- Prediction: **FAIL**
- Basis: Regulations, plans, forestry, and trade bundled into one label.

### Test 36 — idx 3272, "concepts related to disruption and its impact on supply chains and customer relations"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/3272

- Should-fire 1: "The port strike disrupted deliveries and frustrated customers for weeks."
- Should-fire 2: "Supply shortages caused delays that damaged the company's reputation."
- Near-miss 1: "The port expansion improved deliveries and pleased customers for weeks." (disruption flipped to improvement)
- Near-miss 2: "Reliable shipping kept customers happy and protected the company's reputation." (shortage and delay removed)
- Prediction: **FAIL**
- Basis: Abstract causal framing about impact, not a detectable pattern.

### Test 37 — idx 28808, "key events or dramatic situations in a narrative"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/28808

- Should-fire 1: "Suddenly the bridge collapsed, and the chase ended in the river."
- Should-fire 2: "At midnight, the letter arrived that would change everything."
- Near-miss 1: "The bridge held firm, and the convoy crossed the river safely." (collapse and drama removed)
- Near-miss 2: "At midnight, the household slept, and nothing unusual happened." (dramatic arrival removed)
- Prediction: **FAIL**
- Basis: Any plot beat qualifies; no consistent surface form.

### Test 38 — idx 27382, "references to products and solutions related to construction and maintenance"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/27382

- Should-fire 1: "This sealant repairs cracked concrete and prevents water damage."
- Should-fire 2: "The kit includes a drill, replacement filters, and mounting brackets."
- Near-miss 1: "This lotion soothes cracked skin and prevents dryness damage." (construction product swapped for a cosmetic)
- Near-miss 2: "The kit includes a brush, replacement canvases, and wooden easels." (construction kit swapped for an art kit)
- Prediction: **FAIL**
- Basis: All construction products at once is a broad commercial topic.

### Test 39 — idx 23054, "the term "One" and its variations, indicating a focus on unity or singularity concepts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/23054

- Should-fire 1: "One nation, indivisible, stood united after the crisis."
- Should-fire 2: "One should always finish what one starts."
- Near-miss 1: "A nation, indivisible, stood united after the crisis." (One swapped for A)
- Near-miss 2: "You should always finish what you start." (one swapped for you)
- Prediction: **FAIL**
- Basis: Bundles a single token with an abstract unity concept; the concept half dilutes it.

### Test 40 — idx 30566, "keywords related to news articles and announcements"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/30566

- Should-fire 1: "Officials announced Tuesday that the mayor will resign next month."
- Should-fire 2: "Breaking: the city council has approved the new budget, reports say."
- Near-miss 1: "Officials mentioned at lunch that the mayor might retire someday." (announcement swapped for a casual mention)
- Near-miss 2: "The city council approved the new budget during its regular session." (Breaking and reports-say framing removed)
- Prediction: **FAIL**
- Basis: Meta-label about news style in general; no narrow pattern.

### Test 41 — idx 6470, "phrases indicating emotional states or interactions with others"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/6470

- Should-fire 1: "She felt a wave of relief when the results came back normal."
- Should-fire 2: "He apologized to his sister, and they hugged for a long time."
- Near-miss 1: "She felt a wave of nausea when the results came back normal." (emotion swapped for a physical sensation)
- Near-miss 2: "He passed his sister in the hallway without a word." (interaction removed)
- Prediction: **FAIL**
- Basis: All emotions and interactions at once; a diffuse semantic field.

### Test 42 — idx 18758, "elements of mathematical notation and programming syntax"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/18758

- Should-fire 1: "Let f(x) = x^2 + 3x, where x is a real number."
- Should-fire 2: "if (count > 10) { total += count; }"
- Near-miss 1: "Let the function grow steadily as the input value increases." (notation converted to prose)
- Near-miss 2: "When the count passes ten, add it to the running total." (code syntax converted to prose)
- Prediction: **FAIL**
- Basis: Two different symbol systems bundled into one label.

### Test 43 — idx 18024, "key dates and details related to applications or registrations for events"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/18024

- Should-fire 1: "Registration closes on November 30; applicants must submit forms by midnight."
- Should-fire 2: "The application deadline for the workshop is Friday, April 12."
- Near-miss 1: "Registration stays open all winter; applicants may submit forms anytime." (deadline removed)
- Near-miss 2: "The workshop itself takes place on Friday, April 12." (same date, but the event day instead of the application deadline)
- Prediction: **FAIL**
- Basis: A bureaucratic context, not a pattern; dates alone would be narrower.

### Test 44 — idx 1739, "words or phrases that indicate importance or significance in a context"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/1739

- Should-fire 1: "Most importantly, the bridge must be inspected before winter."
- Should-fire 2: "The key finding is that the well water is safe to drink."
- Near-miss 1: "Incidentally, the bridge must be inspected before winter." (importance marker swapped for an incidental marker)
- Near-miss 2: "The final finding is that the well water is safe to drink." (key swapped for final)
- Prediction: **FAIL**
- Basis: A diffuse class of common evaluative words, no single form.

### Test 45 — idx 49, "dates and locations related to events"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/49

- Should-fire 1: "The festival runs August 5 through 7 in Burlington, Vermont."
- Should-fire 2: "Their wedding is set for June 18 at a vineyard in Napa."
- Near-miss 1: "The festival runs for three days in Burlington, Vermont." (dates removed)
- Near-miss 2: "Their wedding is set for June 18 at a vineyard nearby." (specific place removed)
- Prediction: **FAIL**
- Basis: Bundles two patterns, dates and places, into one label.

### Test 46 — idx 10317, "themes related to veterans and their experiences"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/10317

- Should-fire 1: "After twenty years in the army, the veteran struggled to adjust at home."
- Should-fire 2: "The memorial honors soldiers who never returned from the war."
- Near-miss 1: "After twenty years at the factory, the worker struggled to adjust at home." (veteran swapped for a civilian worker)
- Near-miss 2: "The memorial honors firefighters who never returned from the blaze." (soldiers swapped for firefighters)
- Prediction: **FAIL**
- Basis: A broad human topic spanning service, memory, and homecoming.

### Test 47 — idx 10660, "proper names, particularly those associated with people and organizations"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/10660

- Should-fire 1: "Barack Obama met with leaders from the European Union in Brussels."
- Should-fire 2: "The report cited Harvard University and the Ford Foundation."
- Near-miss 1: "The former president met with leaders from the union in the capital." (names swapped for descriptions)
- Near-miss 2: "The report cited a famous university and a large foundation." (names removed)
- Prediction: **FAIL**
- Basis: Proper names in general are too broad for one feature.

### Test 48 — idx 8211, "punctuation marks, specifically periods and questions marks"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/8211

- Should-fire 1: "What time is it? Where did you put the keys?"
- Should-fire 2: "Dr. Lee arrived at 3.30 p.m. He was late."
- Near-miss 1: "Tell me the time, and tell me where you put the keys." (one plain statement: single terminal period, no question marks)
- Near-miss 2: "Lee arrived late in the afternoon and apologized for the delay." (internal periods removed)
- Prediction: **FAIL**
- Basis: Every sentence carries terminal punctuation, so no prompt set isolates the pattern.

### Test 49 — idx 4982, "elements related to recipes and cooking instructions"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/4982

- Should-fire 1: "Fold in the flour, then bake at 350 degrees for 25 minutes."
- Should-fire 2: "Season the chicken with salt and simmer gently for one hour."
- Near-miss 1: "She folded the letter, then left it to sit for 25 minutes." (folding applied to paper; baking removed)
- Near-miss 2: "Season tickets for the theater go on sale in one hour." (season in its ticketing sense)
- Prediction: **PASS**
- Basis: Recipe instructions are a distinctive imperative register with quantities and temperatures.

### Test 50 — idx 31073, "mentions of Java-related annotations and libraries"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/31073

- Should-fire 1: "Add @Override above the method to indicate it replaces the parent version."
- Should-fire 2: "The class imports java.util.ArrayList from the standard library."
- Near-miss 1: "Add a note above the method to indicate it replaces the parent version." (@Override swapped for a plain note)
- Near-miss 2: "The class imports steel beams from the standard supplier catalog." (library import swapped for a physical import)
- Prediction: **PASS**
- Basis: Java annotations like @Override are a narrow, unmistakable surface pattern.

### Test 51 — idx 24349, "discussions about change and its impact on various systems and arrangements"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/24349

- Should-fire 1: "The merger changed how both companies share their computer systems."
- Should-fire 2: "New rules transformed the way the agency arranges its inspections."
- Near-miss 1: "The merger preserved how both companies share their computer systems." (change flipped to continuity)
- Near-miss 2: "Old rules maintained the way the agency arranges its inspections." (transformation removed)
- Prediction: **FAIL**
- Basis: Abstract discussion framing with no consistent surface realization.

### Test 52 — idx 9470, "specific quantities and their related context in various scenarios"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/9470

- Should-fire 1: "The recipe needs exactly three cups of flour and two eggs."
- Should-fire 2: "The warehouse holds forty pallets stacked five high."
- Near-miss 1: "The recipe needs plenty of flour and a few eggs." (specific swapped for vague quantities)
- Near-miss 2: "The warehouse holds many pallets stacked in rows." (quantities removed)
- Prediction: **FAIL**
- Basis: Quantities in any context is close to all prose; too diffuse.

### Test 53 — idx 14331, "references to pricing and cost estimates related to services and products"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/14331

- Should-fire 1: "The plumber quoted $450 to replace the water heater."
- Should-fire 2: "Renting the hall costs 1,200 dollars, including the deposit."
- Near-miss 1: "The plumber offered to replace the water heater this week." (price removed)
- Near-miss 2: "Renting the hall requires a signed contract, including the deposit." (cost removed, deposit kept as a trap)
- Prediction: **PASS**
- Basis: Currency amounts are a crisp surface pattern in commercial prose.

### Test 54 — idx 25296, "expressions of seasonal appreciation and activities"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/25296

- Should-fire 1: "We love these crisp autumn walks through the pumpkin patch."
- Should-fire 2: "Nothing beats a snowy December evening by the fire."
- Near-miss 1: "We dread these crisp autumn walks through the pumpkin patch." (appreciation flipped)
- Near-miss 2: "Nothing special about a rainy Tuesday evening by the fire." (seasonal appreciation made plain)
- Prediction: **FAIL**
- Basis: Vague seasonal sentiment spanning all four seasons and activities.

### Test 55 — idx 20828, "phrases expressing desires or aspirations"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/20828

- Should-fire 1: "Someday I hope to sail across the Atlantic on my own boat."
- Should-fire 2: "She dreams of opening a bakery in her hometown one day."
- Near-miss 1: "Last year I sailed across the Atlantic on my own boat." (aspiration converted to an accomplished fact)
- Near-miss 2: "She works at a bakery in her hometown every day." (dream converted to a routine fact)
- Prediction: **FAIL**
- Basis: Aspirations are a semantic stance expressible in countless forms.

### Test 56 — idx 15837, "elements of tension and conflict in relationships"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/15837

- Should-fire 1: "He resented her for years after she broke his trust."
- Should-fire 2: "Their friendship never recovered from the argument last winter."
- Near-miss 1: "He trusted her completely, even years after they first met." (resentment swapped for trust)
- Near-miss 2: "Their friendship only deepened after the trip last winter." (argument swapped for a shared trip)
- Prediction: **FAIL**
- Basis: Relationship conflict in any form is a broad narrative topic.

### Test 57 — idx 13568, "elements related to programming or technical specifications"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/13568

- Should-fire 1: "The device supports up to 16 GB of memory and a 2.4 GHz processor."
- Should-fire 2: "Set the timeout parameter to 30 seconds in the configuration file."
- Near-miss 1: "The suitcase holds up to sixteen changes of clothes and a warm coat." (spec numbers swapped for luggage contents)
- Near-miss 2: "Set the kitchen timer to 30 minutes in the recipe steps." (technical parameter swapped for a kitchen timer)
- Prediction: **FAIL**
- Basis: Programming and all technical specifications bundled; too heterogeneous.

### Test 58 — idx 27458, "mathematical symbols and notation used in formal definitions and theorems"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/27458

- Should-fire 1: "For every ε > 0 there exists a δ > 0 such that |x − a| < δ."
- Should-fire 2: "Theorem: the sum ∑ of the first n integers equals n(n + 1)/2."
- Near-miss 1: "For every small amount there is another small amount that works." (symbols converted to words)
- Near-miss 2: "Adding up the first several whole numbers gives a tidy formula." (notation converted to prose)
- Prediction: **PASS**
- Basis: Formal notation is a narrow symbol-level pattern, unlike ordinary prose.

### Test 59 — idx 21341, "instances of significant numerical values or comparative phrases"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/21341

- Should-fire 1: "Sales this year were twice as high as last year, reaching 900,000 units."
- Should-fire 2: "The new bridge is longer and carries more traffic than the old one."
- Near-miss 1: "Sales this year matched last year, holding steady as usual." (comparison and large value removed)
- Near-miss 2: "The new bridge is open and carries traffic like the old one." (comparative removed)
- Prediction: **FAIL**
- Basis: Bundles large numbers with comparatives, two unrelated patterns.

### Test 60 — idx 6140, "phrases that relate to the concept of harnessing or unlocking potential and power, particularly in various contexts such as data, energy, and entrepreneurship"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/6140

- Should-fire 1: "Our platform unlocks the full potential of your customer data."
- Should-fire 2: "The new turbine harnesses the power of the river year-round."
- Near-miss 1: "Our platform stores the full contents of your customer data." (unlocks potential swapped for stores)
- Near-miss 2: "The new dam blocks the flow of the river year-round." (harnesses power swapped for blocks)
- Prediction: **FAIL**
- Basis: Marketing metaphor stretched across data, energy, and business domains.

### Test 61 — idx 5979, "concepts related to divine love and accountability"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/5979

- Should-fire 1: "God's love, the sermon said, calls every believer to account."
- Should-fire 2: "She believed divine mercy would judge her deeds with compassion."
- Near-miss 1: "The manager's memo, the report said, calls every employee to account." (divine swapped for managerial accountability)
- Near-miss 2: "She believed the committee's mercy would judge her deeds with compassion." (divine mercy swapped for a committee)
- Prediction: **FAIL**
- Basis: Two abstract theological concepts bundled together.

### Test 62 — idx 10256, "occurrences of the term "System" related to programming or software development contexts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/10256

- Should-fire 1: "In Java, System.out.println sends text to the console."
- Should-fire 2: "The System class provides access to the standard input stream."
- Near-miss 1: "In Java, the console print command sends text to the screen." (System removed, topic kept)
- Near-miss 2: "The filing system provides access to the standard record archive." (system lowercase, in its office sense)
- Prediction: **PASS**
- Basis: One named token in code contexts, a narrow surface pattern.

### Test 63 — idx 16293, "topics related to storytelling and personal narratives"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/16293

- Should-fire 1: "In her memoir, she recounts the summer that changed her life."
- Should-fire 2: "He told us the story of how he met his wife."
- Near-miss 1: "In her report, she summarizes the quarter that changed the budget." (memoir swapped for a report)
- Near-miss 2: "He showed us the map of how he drove to the coast." (story swapped for directions)
- Prediction: **FAIL**
- Basis: Storytelling in general is a broad discourse category.

### Test 64 — idx 28474, "terms related to astrophysics and cosmic phenomena"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/28474

- Should-fire 1: "The supernova outshone its entire galaxy for several weeks."
- Should-fire 2: "Astronomers detected a quasar near the edge of the observable universe."
- Near-miss 1: "The lighthouse outshone every boat lamp in the harbor for several weeks." (supernova and galaxy swapped for local lights)
- Near-miss 2: "Botanists detected a fungus near the edge of the forest reserve." (astronomy swapped for botany)
- Prediction: **PASS**
- Basis: A tight physical-science vocabulary: supernova, galaxy, quasar, universe.

### Test 65 — idx 4155, "names and their associated details, specifically in a structured format such as lists or tables"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/4155

- Should-fire 1: "Name: Priya Nair; Role: Surgeon; City: Denver."
- Should-fire 2: "Employee: Tom Reed — Department: Sales — Start date: May 3."
- Near-miss 1: "Priya Nair works as a surgeon in Denver." (structured list converted to a prose sentence)
- Near-miss 2: "Tom Reed joined the sales department on May third." (table format converted to prose)
- Prediction: **FAIL**
- Basis: Bundles names with document layout; two conditions, unlikely for one feature.

### Test 66 — idx 9085, "programming-related keywords and function structures commonly used in code"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/9085

- Should-fire 1: "Use the return statement to exit the function early."
- Should-fire 2: "A while loop repeats until its condition becomes false."
- Near-miss 1: "Use the exit door to leave the theater early." (return and exit as physical actions)
- Near-miss 2: "The song's chorus repeats until the final verse fades out." (loop swapped for musical repetition)
- Prediction: **FAIL**
- Basis: All common code keywords at once; broader than one feature's pattern.

### Test 67 — idx 1211, "terms related to the aging and flavoring process of beer"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/1211

- Should-fire 1: "The stout was aged in oak barrels for eighteen months."
- Should-fire 2: "Dry hopping gives the ale its bright citrus aroma."
- Near-miss 1: "The cheese was aged in oak crates for eighteen months." (beer swapped for cheese aging)
- Near-miss 2: "Dry soil gives the grapes their bright citrus notes." (hopping swapped for vineyard conditions; dry and citrus kept as traps)
- Prediction: **PASS**
- Basis: A narrow process vocabulary: barrel aging, dry hopping, stout, ale.

### Test 68 — idx 479, "references to choices and options in various contexts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/479

- Should-fire 1: "You can choose the window seat or the aisle seat."
- Should-fire 2: "She had two options: renew the lease or move out."
- Near-miss 1: "You will get the window seat or the aisle seat." (choice converted to assignment; or kept)
- Near-miss 2: "She faced one outcome: the lease would end in June." (options converted to a single outcome)
- Prediction: **FAIL**
- Basis: Choice is expressed everywhere in language; no narrow pattern.

### Test 69 — idx 11342, "phrases related to public scrutiny and controversy"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/11342

- Should-fire 1: "The senator faced intense scrutiny over the leaked emails."
- Should-fire 2: "The policy sparked controversy among voters across the state."
- Near-miss 1: "The senator received intense applause over the leaked emails." (scrutiny swapped for applause)
- Near-miss 2: "The policy won broad support among voters across the state." (controversy swapped for support)
- Prediction: **FAIL**
- Basis: Diffuse media-discourse vocabulary, not one pattern.

### Test 70 — idx 26722, "comparisons and parallels in policies and practices related to mental health and subscription models"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/26722

- Should-fire 1: "Like therapy plans, the app charges a monthly fee for continued care."
- Should-fire 2: "The clinic's subscription model mirrors how gyms bill their members."
- Near-miss 1: "The app charges a monthly fee for its premium features." (comparison and therapy removed)
- Near-miss 2: "The clinic's waiting room mirrors the calm design of a spa." (comparison kept, the policy and subscription pairing removed)
- Prediction: **FAIL**
- Basis: Two unrelated domains yoked together; no single feature tracks that pairing.

### Test 71 — idx 8866, "instances of encouragement and motivation in various contexts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/8866

- Should-fire 1: "You can do it — just take the first step today."
- Should-fire 2: "Keep going; your hard work will pay off in the end."
- Near-miss 1: "You may submit it — just use the first form today." (encouragement converted to a clerical instruction)
- Near-miss 2: "Keep records; your hard work will be audited at the end." (motivation converted to compliance)
- Prediction: **FAIL**
- Basis: Encouragement is a speech act with countless surface forms.

### Test 72 — idx 13355, "content related to systematic reviews and scientific research"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/13355

- Should-fire 1: "This systematic review pooled data from forty-two randomized trials."
- Should-fire 2: "The meta-analysis found a small but consistent treatment effect."
- Near-miss 1: "This annual review pooled data from forty-two regional offices." (systematic and trials swapped for annual and offices)
- Near-miss 2: "The book review found a small but consistent narrative thread." (meta-analysis swapped for a book review)
- Prediction: **FAIL**
- Basis: Systematic reviews plus all scientific research is too broad a bundle.

### Test 73 — idx 31854, "phrases indicating possession or ownership"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/31854

- Should-fire 1: "The house on the hill is hers, and the car is mine."
- Should-fire 2: "John's signature appears on the deed to the property."
- Near-miss 1: "The house on the hill is rented, and the car is borrowed." (ownership swapped for temporary use)
- Near-miss 2: "The signature appears at the foot of the long letter." (possessor removed)
- Prediction: **FAIL**
- Basis: Possession is basic grammar spread across pronouns, names, and phrases.

### Test 74 — idx 20386, "phrases that highlight violations of authority and rights"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/20386

- Should-fire 1: "The ruling violated the protesters' right to free speech."
- Should-fire 2: "Officers exceeded their authority by searching the home without a warrant."
- Near-miss 1: "The ruling protected the protesters' right to free speech." (violation flipped to protection)
- Near-miss 2: "Officers used their authority by searching the home with a warrant." (exceeded swapped for lawful use)
- Prediction: **FAIL**
- Basis: Abstract legal-political framing, expressible in many forms.

### Test 75 — idx 3458, "URLs and web-related syntax"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/3458

- Should-fire 1: "Download the form at https://www.example.gov/forms/apply.html today."
- Should-fire 2: "Her homepage links to www.cookingblog.example.net/recipes every week."
- Near-miss 1: "Download the form at the main office on Fifth Street today." (URL swapped for a physical address)
- Near-miss 2: "Her cookbook links every recipe to a seasonal menu every week." (homepage and links swapped for print)
- Prediction: **PASS**
- Basis: URLs have an unmistakable character-level pattern: scheme, dots, slashes.

### Test 76 — idx 20197, "the presence of the verb "do" and its various forms in sentences"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/20197

- Should-fire 1: "I do my homework before dinner every night."
- Should-fire 2: "Does she know what the committee did last week?"
- Near-miss 1: "I finish my homework before dinner every night." (do removed, meaning kept)
- Near-miss 2: "She knows what the committee decided last week." (does and did removed)
- Prediction: **PASS**
- Basis: One verb and its forms: a single-token pattern like the pilot's clearest passes.

### Test 77 — idx 123, "phrases related to the founding and establishment of organizations or companies"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/123

- Should-fire 1: "Founded in 1987, the software company now employs two thousand people."
- Should-fire 2: "He established the charity to fund scholarships for nurses."
- Near-miss 1: "Expanded in 1987, the software company now employs two thousand people." (founded swapped for expanded)
- Near-miss 2: "He donated to the charity that funds scholarships for nurses." (establish swapped for donate to an existing charity)
- Prediction: **FAIL**
- Basis: A business-history topic; founding is one event described many ways.

### Test 78 — idx 14022, "various numbers and references typically associated with academic publications, citations, or statistical data"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/14022

- Should-fire 1: "The effect was significant (p < .05), as shown in Table 3 [12]."
- Should-fire 2: "Smith et al. (2020) reported response rates of 68 percent."
- Near-miss 1: "The effect was clearly visible in the third chart at the meeting." (statistics and citation apparatus removed)
- Near-miss 2: "Smith reported that most participants answered the survey questions." (et al., year, and percentage removed)
- Prediction: **FAIL**
- Basis: Numbers, citations, and statistics bundled; three patterns in one label.

### Test 79 — idx 25833, "themes related to powerlessness and conflict"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/25833

- Should-fire 1: "Trapped in the feud, she had no say in her own future."
- Should-fire 2: "The workers felt helpless as the owners fought over the factory."
- Near-miss 1: "Leading the negotiations, she had full say in her own future." (powerlessness flipped)
- Near-miss 2: "The workers felt confident as the owners agreed on the factory." (helplessness and conflict removed)
- Prediction: **FAIL**
- Basis: Two abstract themes bundled; no surface pattern.

### Test 80 — idx 23454, "Java class and component definitions within a programming context"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/16-llamascope-res-32k/23454

- Should-fire 1: "public class Invoice extends Document implements Printable {"
- Should-fire 2: "@Component public class EmailService { private final Sender sender; }"
- Near-miss 1: "The public document class includes invoices and printable forms." (code definition converted to office prose; keywords kept as traps)
- Near-miss 2: "The email service component sends messages for the billing team." (Java definition converted to a prose description)
- Prediction: **PASS**
- Basis: Java class declarations are a narrow, formulaic code pattern.
