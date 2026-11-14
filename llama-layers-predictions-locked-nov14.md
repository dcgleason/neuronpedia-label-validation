# Llama 3.1 8B multi-layer extension — predictions LOCKED

> **STATUS: LOCKED.** Approved and locked by Danny Gleason on November 14, 2026, before any scoring. No sampled feature in this file has been run through the activation API. The only activation calls made during preparation were two source-verification calls on feature idx 0 (one per layer), and idx 0 is in neither sample. This file was published to the GitHub repository as the lock commit before any scoring. This file must not be edited after locking.

- **Study:** Multi-layer extension of the Llama 3.1 8B replication of the Neuronpedia label-validation study. The replication tested layer 16 only; this extension tests layers 8 and 24 with the identical protocol, so pass rates can be compared across depth within one model and against the Gemma-2-2B layer pattern (L6 10/40, L12 31/120, L18 18/40).
- **Model:** Llama 3.1 8B (`llama3.1-8b`)
- **SAE set:** Llama Scope residual-stream, 32k width (`llamascope-res-32k`)
- **Layers:** 8 of 32 — source ID `8-llamascope-res-32k`; 24 of 32 — source ID `24-llamascope-res-32k`. Both sources verified live on November 14, 2026 (one test activation call each via the connector helper, HTTP 200, response layer field matching the requested source).
- **Sample:** 40 labeled features per layer (80 total). Draw rule (mirrors the replication exactly): successive `rng.randrange(32768)` values over feature indices 0–32767; each drawn index is fetched from the public Neuronpedia feature API and its label is `explanations[0].description`. Skip rule: a drawn feature with no explanations (or no description on the first explanation) is skipped and logged, as is a duplicate draw; drawing continues until 40 labeled features are held. Result here: 40 draws per layer, 40 kept, 0 skips, 0 duplicates at each layer.
- **Seeding (exactly):** one `random.Random` instance per layer, seeded independently. Layer 8 seed = `2026111408`; layer 24 seed = `2026111424`. Each seed is the base value 20261114 (the draft date, matching the replication's date-seed convention) with the two-digit layer number appended. The two samples share no index numbers (checked; and indices at different layers are different SAEs in any case).
- **Protocol (identical to the pilot, scale-up, and replication):** per feature, two should-fire prompts that plainly express the label, two near-miss prompts that each change exactly one variable relative to a should-fire, and one binary prediction (PASS / FAIL) registered before any scoring.
- **Pass rule (set in advance):** a label passes if both should-fire prompts activate the feature clearly above both near-miss prompts (min(should-fire) > max(near-miss)).
- **Predictions in this file:** 11 PASS, 69 FAIL (layer 8: 5 PASS, 35 FAIL; layer 24: 6 PASS, 34 FAIL).
- **Prediction heuristics:** the same reasoning as the locked replication file (narrow surface patterns, closed keyword sets, and single tokens predicted to pass; broad topics, abstract concepts, bundled domains, and meta-labels predicted to fail), updated where the layer-16 replication produced direct evidence about a category. Where a Basis line cites a layer-16 result, that result is the reason for the call.
- **Authorship:** Prompts and predictions drafted by Muse; approved and LOCKED by Danny Gleason on November 14, 2026, before any scoring. At lock time, no sampled feature had been run through the activation API.
- **SHA-256:** computed at lock (November 14, 2026) and recorded in the lock commit in this repository. This file must not be edited after locking.

## Sampling log — layer 8 (seed 2026111408)

Successive `randrange(32768)` draws, in order. 40 draws, 40 kept, 0 skipped.

- Draw 1: idx 27277 — kept as sample #1
- Draw 2: idx 2189 — kept as sample #2
- Draw 3: idx 16108 — kept as sample #3
- Draw 4: idx 23753 — kept as sample #4
- Draw 5: idx 14695 — kept as sample #5
- Draw 6: idx 19465 — kept as sample #6
- Draw 7: idx 18188 — kept as sample #7
- Draw 8: idx 22224 — kept as sample #8
- Draw 9: idx 28300 — kept as sample #9
- Draw 10: idx 104 — kept as sample #10
- Draw 11: idx 15695 — kept as sample #11
- Draw 12: idx 20596 — kept as sample #12
- Draw 13: idx 9110 — kept as sample #13
- Draw 14: idx 17737 — kept as sample #14
- Draw 15: idx 16835 — kept as sample #15
- Draw 16: idx 29439 — kept as sample #16
- Draw 17: idx 21205 — kept as sample #17
- Draw 18: idx 7223 — kept as sample #18
- Draw 19: idx 23375 — kept as sample #19
- Draw 20: idx 22669 — kept as sample #20
- Draw 21: idx 28106 — kept as sample #21
- Draw 22: idx 20778 — kept as sample #22
- Draw 23: idx 6788 — kept as sample #23
- Draw 24: idx 4527 — kept as sample #24
- Draw 25: idx 14979 — kept as sample #25
- Draw 26: idx 22894 — kept as sample #26
- Draw 27: idx 25256 — kept as sample #27
- Draw 28: idx 27400 — kept as sample #28
- Draw 29: idx 31301 — kept as sample #29
- Draw 30: idx 2250 — kept as sample #30
- Draw 31: idx 32520 — kept as sample #31
- Draw 32: idx 29812 — kept as sample #32
- Draw 33: idx 3727 — kept as sample #33
- Draw 34: idx 13137 — kept as sample #34
- Draw 35: idx 6127 — kept as sample #35
- Draw 36: idx 31687 — kept as sample #36
- Draw 37: idx 15158 — kept as sample #37
- Draw 38: idx 27446 — kept as sample #38
- Draw 39: idx 28584 — kept as sample #39
- Draw 40: idx 6627 — kept as sample #40

## Sampling log — layer 24 (seed 2026111424)

Successive `randrange(32768)` draws, in order. 40 draws, 40 kept, 0 skipped.

- Draw 1: idx 16917 — kept as sample #1
- Draw 2: idx 10092 — kept as sample #2
- Draw 3: idx 6962 — kept as sample #3
- Draw 4: idx 3510 — kept as sample #4
- Draw 5: idx 18249 — kept as sample #5
- Draw 6: idx 24816 — kept as sample #6
- Draw 7: idx 14728 — kept as sample #7
- Draw 8: idx 5588 — kept as sample #8
- Draw 9: idx 23530 — kept as sample #9
- Draw 10: idx 10617 — kept as sample #10
- Draw 11: idx 19500 — kept as sample #11
- Draw 12: idx 4680 — kept as sample #12
- Draw 13: idx 23356 — kept as sample #13
- Draw 14: idx 29911 — kept as sample #14
- Draw 15: idx 8994 — kept as sample #15
- Draw 16: idx 29746 — kept as sample #16
- Draw 17: idx 7981 — kept as sample #17
- Draw 18: idx 26744 — kept as sample #18
- Draw 19: idx 27334 — kept as sample #19
- Draw 20: idx 3103 — kept as sample #20
- Draw 21: idx 9044 — kept as sample #21
- Draw 22: idx 19170 — kept as sample #22
- Draw 23: idx 24001 — kept as sample #23
- Draw 24: idx 19832 — kept as sample #24
- Draw 25: idx 29452 — kept as sample #25
- Draw 26: idx 21040 — kept as sample #26
- Draw 27: idx 20626 — kept as sample #27
- Draw 28: idx 6413 — kept as sample #28
- Draw 29: idx 8246 — kept as sample #29
- Draw 30: idx 26702 — kept as sample #30
- Draw 31: idx 15269 — kept as sample #31
- Draw 32: idx 31920 — kept as sample #32
- Draw 33: idx 12653 — kept as sample #33
- Draw 34: idx 27839 — kept as sample #34
- Draw 35: idx 8622 — kept as sample #35
- Draw 36: idx 3155 — kept as sample #36
- Draw 37: idx 12706 — kept as sample #37
- Draw 38: idx 1726 — kept as sample #38
- Draw 39: idx 25362 — kept as sample #39
- Draw 40: idx 31376 — kept as sample #40

## Tests — layer 8 (source `8-llamascope-res-32k`)

### Test 1 — idx 27277, "references to sports organizations or events"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/27277

- Should-fire 1: "UEFA confirmed that the Champions League final will be held in Munich."
- Should-fire 2: "The New York Yankees signed a new starting pitcher for the season."
- Near-miss 1: "The committee confirmed that the chess final will be held in Munich." (sports organization and event swapped for a chess committee)
- Near-miss 2: "The New York theater company signed a new lead actor for the season." (sports team swapped for a theater company)
- Prediction: **FAIL**
- Basis: All sports organizations and events at once is a broad topic, not one pattern.

### Test 2 — idx 2189, "references to global diversity and inclusiveness"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/2189

- Should-fire 1: "The festival celebrates the diversity of cultures from every continent."
- Should-fire 2: "The school promotes inclusiveness for students of all backgrounds."
- Near-miss 1: "The festival celebrates the harvest of crops from every region." (diversity swapped for an agricultural harvest)
- Near-miss 2: "The school promotes punctuality for students of all grades." (inclusiveness swapped for punctuality)
- Prediction: **FAIL**
- Basis: Abstract social values with diffuse vocabulary and no surface form.

### Test 3 — idx 16108, "phrases related to scientific and technical concepts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/16108

- Should-fire 1: "The experiment measured the velocity of the falling object."
- Should-fire 2: "Photosynthesis converts sunlight into chemical energy inside the leaf."
- Near-miss 1: "The rehearsal measured the tempo of the opening number." (scientific measurement swapped for a musical one)
- Near-miss 2: "The recipe converts plain flour into a rich cake batter." (technical process swapped for cooking)
- Prediction: **FAIL**
- Basis: All of science and technology in one label; far too broad for one feature.

### Test 4 — idx 23753, "references to royal titles and their associated entities"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/23753

- Should-fire 1: "Queen Elizabeth II met the Prime Minister at Buckingham Palace."
- Should-fire 2: "The Duke of Edinburgh presented the awards alongside the Duchess."
- Near-miss 1: "Mrs. Elizabeth Hart met the Prime Minister at the town hall." (royal title swapped for a plain honorific)
- Near-miss 2: "The depot manager presented the awards alongside the deputy director." (royal titles swapped for workplace titles)
- Prediction: **PASS**
- Basis: Royal titles are a small closed vocabulary set: queen, prince, duke, duchess, palace.

### Test 5 — idx 14695, "structural elements and syntax related to programming and coding conventions"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/14695

- Should-fire 1: "for (int i = 0; i < n; i++) { sum += arr[i]; }"
- Should-fire 2: "if (user.isActive) { return renderDashboard(); }"
- Near-miss 1: "For each item in the list, add its value to the running total." (loop converted to prose)
- Near-miss 2: "When the user is active, the clerk displays the main notice board." (conditional code converted to a workplace scene)
- Prediction: **FAIL**
- Basis: Programming syntax in general, not one construct; general code labels failed at layer 16.

### Test 6 — idx 19465, "code-related keywords and structures within programming syntax"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/19465

- Should-fire 1: "while (!queue.isEmpty()) { process(queue.poll()); }"
- Should-fire 2: "public static void main(String[] args) { start(); }"
- Near-miss 1: "While the line is not empty, the clerk processes each waiting customer." (code keywords converted to a service-desk scene)
- Near-miss 2: "The public hall's main entrance opens when the event starts." (code declaration converted to prose; public and main kept as traps)
- Prediction: **FAIL**
- Basis: All common code keywords bundled; broader than one feature's pattern.

### Test 7 — idx 18188, "references to images and photography in various contexts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/18188

- Should-fire 1: "She uploaded the photograph to the gallery website."
- Should-fire 2: "The image shows a mountain lake at sunrise."
- Near-miss 1: "She uploaded the manuscript to the publisher's website." (photograph swapped for a manuscript)
- Near-miss 2: "The painting shows a mountain lake at sunrise." (photographic image swapped for a painting)
- Prediction: **FAIL**
- Basis: Images and photography across all contexts is a broad topic.

### Test 8 — idx 22224, "specific identifiers and structured data in text"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/22224

- Should-fire 1: "User ID: 88412; Account: XZ-9917; Status: active."
- Should-fire 2: "The record lists product_code = 'A-102', batch = 4471."
- Near-miss 1: "The user has an account, and the account status is active." (structured fields converted to prose)
- Near-miss 2: "The record describes the blue product from the recent batch." (identifier values removed)
- Prediction: **FAIL**
- Basis: Bundles identifiers with structured formats; the layer-16 names-in-structured-format label (idx 4155) failed on the same two-condition shape.

### Test 9 — idx 28300, "references to the concept of change"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/28300

- Should-fire 1: "The town changed completely after the factory closed."
- Should-fire 2: "Her views on the subject have changed over the years."
- Near-miss 1: "The town stayed the same after the factory closed." (change flipped to continuity)
- Near-miss 2: "Her views on the subject have held firm over the years." (changed swapped for held firm)
- Prediction: **FAIL**
- Basis: Change is among the most abstract concepts in the language.

### Test 10 — idx 104, "terms related to measurements and adjustments of rates or effectiveness"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/104

- Should-fire 1: "The technician adjusted the flow rate to 40 liters per minute."
- Should-fire 2: "They measured the effectiveness of the drug in a controlled trial."
- Near-miss 1: "The technician opened the valve fully for the afternoon shift." (rate adjustment removed)
- Near-miss 2: "They praised the usefulness of the drug in a published review." (measured effectiveness swapped for praise)
- Prediction: **FAIL**
- Basis: Measurements, rate adjustments, and effectiveness bundled into one label.

### Test 11 — idx 15695, "references to fame and success in the context of individuals or groups"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/15695

- Should-fire 1: "The singer rose to fame after her first album topped the charts."
- Should-fire 2: "Their startup became a success story told in business schools."
- Near-miss 1: "The singer released her first album to quiet reviews." (fame removed)
- Near-miss 2: "Their startup became a small firm employing twelve people." (success framing removed)
- Prediction: **FAIL**
- Basis: Fame and success across all domains; diffuse evaluative vocabulary.

### Test 12 — idx 20596, "phrases concerning the consequences and effects of actions or decisions"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/20596

- Should-fire 1: "The decision led to serious consequences for the whole department."
- Should-fire 2: "Cutting the budget had an immediate effect on hiring."
- Near-miss 1: "The decision was recorded in the minutes for the whole department." (consequences swapped for record-keeping)
- Near-miss 2: "The budget discussion took most of the morning meeting." (effect on hiring removed)
- Prediction: **FAIL**
- Basis: Abstract consequence-and-effect framing with no consistent surface realization.

### Test 13 — idx 9110, "words related to romantic relationships and interpersonal conflicts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/9110

- Should-fire 1: "He finally asked her out, and they had their first date on Friday."
- Should-fire 2: "Their breakup left both of them angry and hurt."
- Near-miss 1: "He finally emailed her, and they had their first meeting on Friday." (romantic date swapped for a work meeting)
- Near-miss 2: "Their reunion left both of them relieved and calm." (breakup conflict swapped for a warm reunion)
- Prediction: **FAIL**
- Basis: Romance and all interpersonal conflict bundled into one label.

### Test 14 — idx 17737, "technical terms and concepts related to radar systems and their components"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/17737

- Should-fire 1: "The radar antenna sweeps the sky for incoming aircraft."
- Should-fire 2: "Doppler radar tracks the storm's rotation and rainfall intensity."
- Near-miss 1: "The dish antenna sweeps the sky for the evening news broadcast." (radar swapped for a broadcast dish)
- Near-miss 2: "Weather satellites track the storm's movement and rainfall totals." (radar swapped for satellites)
- Prediction: **PASS**
- Basis: A tight technical keyword set (radar, Doppler, antenna, sweep), like the radio-licensing niche that passed at layer 16.

### Test 15 — idx 16835, "references to wedding photography in North Wales"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/16835

- Should-fire 1: "Their wedding photographer in Bangor captured the ceremony at the castle."
- Should-fire 2: "A North Wales wedding photography studio offers albums and prints."
- Near-miss 1: "Their wedding photographer in Manchester captured the ceremony at the castle." (North Wales swapped for Manchester)
- Near-miss 2: "A North Wales landscape photography studio offers albums and prints." (wedding swapped for landscape)
- Prediction: **FAIL**
- Basis: Two conditions at once, a niche service and a region; two-condition labels failed at layer 16.

### Test 16 — idx 29439, "references to web URLs"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/29439

- Should-fire 1: "Visit https://www.example.org/apply for the application form."
- Should-fire 2: "The manual links to www.support.example.com/downloads for the files."
- Near-miss 1: "Visit the main office on Broad Street for the application form." (URL swapped for a physical address)
- Near-miss 2: "The manual refers to the printed catalog for the files." (web link swapped for print)
- Prediction: **FAIL**
- Basis: The layer-16 URL feature (idx 3458) was predicted to pass on exactly this reasoning and failed; URL strings appear not to isolate in this SAE.

### Test 17 — idx 21205, "inquiries and requests for assistance or information"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/21205

- Should-fire 1: "Could you please help me find the nearest station?"
- Should-fire 2: "I am writing to ask for information about the course schedule."
- Near-miss 1: "You can find the nearest station two blocks from here." (request converted to a plain statement)
- Near-miss 2: "I am writing to confirm the details of the course schedule." (asking for information swapped for confirming it)
- Prediction: **FAIL**
- Basis: Requests are a speech act with countless surface forms.

### Test 18 — idx 7223, "UI navigation elements and commands related to closing or canceling actions"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/7223

- Should-fire 1: "Click Cancel to close the dialog without saving your changes."
- Should-fire 2: "Press the X in the corner, or choose Close from the menu."
- Near-miss 1: "Click Save to keep the document with all your changes." (close and cancel swapped for save)
- Near-miss 2: "He decided to cancel the meeting and close the office early." (same words used as ordinary verbs, not UI commands)
- Prediction: **PASS**
- Basis: Close and cancel as interface commands form a narrow UI register distinct from ordinary prose.

### Test 19 — idx 23375, "items in a navigation or menu list structure"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/23375

- Should-fire 1: "Home | Products | Services | About Us | Contact"
- Should-fire 2: "Menu: Dashboard, Orders, Customers, Settings, Log out."
- Near-miss 1: "The homepage describes our products, services, and company history." (menu list converted to prose)
- Near-miss 2: "She read the dashboard report, then checked the orders and settings." (menu items converted to a prose sequence)
- Prediction: **FAIL**
- Basis: Bundles document layout with navigation content; the structured-format label at layer 16 failed.

### Test 20 — idx 22669, "citation formats and references in the text"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/22669

- Should-fire 1: "As shown by Carter et al. (2019), the effect persists across samples."
- Should-fire 2: "The claim is supported by several studies [4, 7, 12]."
- Near-miss 1: "As the teacher showed the class, the effect persists across examples." (citation swapped for a classroom reference)
- Near-miss 2: "The claim is supported by several studies from recent years." (bracketed reference numbers removed)
- Prediction: **FAIL**
- Basis: Citation apparatus spans author names, years, and bracket numbers; the bundled citations label at layer 16 (idx 14022) failed.

### Test 21 — idx 28106, "mentions of individuals involved in incidents of violence or crime"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/28106

- Should-fire 1: "The suspect was arrested after the robbery at the gas station."
- Should-fire 2: "Witnesses identified the attacker who fled the scene on foot."
- Near-miss 1: "The cashier was promoted after the inspection at the gas station." (crime and arrest swapped for an inspection and promotion)
- Near-miss 2: "Bystanders greeted the jogger who crossed the park on foot." (attacker swapped for a jogger)
- Prediction: **FAIL**
- Basis: A news topic spanning suspects, victims, and witnesses; no narrow pattern.

### Test 22 — idx 20778, "code and programming concepts related to state management and hooks in React"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/20778

- Should-fire 1: "const [count, setCount] = useState(0);"
- Should-fire 2: "useEffect(() => { fetchData(); }, []);"
- Near-miss 1: "The counter starts at zero and updates whenever the button is clicked." (hook converted to a prose description)
- Near-miss 2: "The side effect runs the data fetch once when the page loads, as a plain script." (effect hook converted to prose)
- Prediction: **FAIL**
- Basis: Every code-syntax PASS prediction in the layer-16 replication failed (function definitions, Java annotations, class definitions); code labels have not validated in this SAE.

### Test 23 — idx 6788, "concepts related to underlying issues and their consequences in various contexts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/6788

- Should-fire 1: "The underlying issue is a shortage of trained staff."
- Should-fire 2: "Poor drainage caused deeper problems throughout the building."
- Near-miss 1: "The visible issue is a shortage of office chairs." (underlying swapped for visible, and the issue trivialized)
- Near-miss 2: "Good drainage protected the structure throughout the building." (consequence flipped to protection)
- Prediction: **FAIL**
- Basis: Abstract problem-and-consequence framing across all contexts.

### Test 24 — idx 4527, "punctuations and ellipses in the text"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/4527

- Should-fire 1: "She paused... then whispered, 'I don't know...'"
- Should-fire 2: "Wait — what did you say? Really... after all that?"
- Near-miss 1: "She paused, then whispered that she did not know." (ellipses removed)
- Near-miss 2: "Tell me plainly what you said at the meeting yesterday." (question and ellipsis marks removed)
- Prediction: **FAIL**
- Basis: Bundles all punctuation with ellipses; the layer-16 punctuation feature (idx 8211) failed because terminal punctuation is in every sentence.

### Test 25 — idx 14979, "specific non-English characters and texts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/14979

- Should-fire 1: "El niño jugó en el parque con su hermana."
- Should-fire 2: "La bibliothèque ouvre à neuf heures du matin."
- Near-miss 1: "The child played in the park with his sister." (same meaning in English)
- Near-miss 2: "The library opens at nine in the morning." (same meaning in English)
- Prediction: **PASS**
- Basis: Non-English text is a character-level pattern clearly distinct from English prose.

### Test 26 — idx 22894, "terms related to nudity and body exposure"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/22894

- Should-fire 1: "The painting depicts a nude figure reclining on a couch."
- Should-fire 2: "Swimmers were warned that naked sunbathing is not allowed on this beach."
- Near-miss 1: "The painting depicts a draped figure reclining on a couch." (nude swapped for draped)
- Near-miss 2: "Swimmers were warned that loud music is not allowed on this beach." (nudity swapped for noise)
- Prediction: **FAIL**
- Basis: A semantic topic with varied wording (nude, undressed, exposed, stripped), not one surface pattern.

### Test 27 — idx 25256, "programming-related terms and structures"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/25256

- Should-fire 1: "The compiler reported an error in the module's main function."
- Should-fire 2: "She debugged the script until the output matched the spec."
- Near-miss 1: "The editor reported an error in the magazine's main article." (compiler and module swapped for editor and magazine)
- Near-miss 2: "She revised the essay until the draft matched the outline." (debugging swapped for essay revision)
- Prediction: **FAIL**
- Basis: All of programming at once; too broad for one feature.

### Test 28 — idx 27400, "coding syntax and structure"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/27400

- Should-fire 1: "if (x > 0) { y = x * 2; } else { y = 0; }"
- Should-fire 2: "class Point { constructor(x, y) { this.x = x; } }"
- Near-miss 1: "If the value is positive, double it; otherwise set it to zero." (code converted to prose)
- Near-miss 2: "A point is defined by its two coordinates on the plane." (class definition converted to prose)
- Prediction: **FAIL**
- Basis: Coding syntax in general, not one construct; general code labels failed at layer 16.

### Test 29 — idx 31301, "terms related to coordination and organizational activities"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/31301

- Should-fire 1: "The committee coordinated the relief effort across three counties."
- Should-fire 2: "She organized the conference schedule for two hundred attendees."
- Near-miss 1: "The committee funded the relief effort across three counties." (coordinated swapped for funded)
- Near-miss 2: "She attended the conference sessions with two hundred colleagues." (organizing swapped for attending)
- Prediction: **FAIL**
- Basis: Coordination and organizing across all contexts; diffuse vocabulary.

### Test 30 — idx 2250, "references to gun ownership and related legislative discussions"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/2250

- Should-fire 1: "The senator proposed a bill expanding background checks for gun buyers."
- Should-fire 2: "Gun owners in the state must renew their permits every five years."
- Near-miss 1: "The senator proposed a bill expanding tax credits for home buyers." (gun legislation swapped for housing legislation)
- Near-miss 2: "Car owners in the state must renew their registrations every five years." (gun permits swapped for car registrations)
- Prediction: **FAIL**
- Basis: A policy topic bundling ownership with legislation.

### Test 31 — idx 32520, "references to organizations and groups related to veterans and women's associations"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/32520

- Should-fire 1: "The veterans' association hosted a dinner for local service members."
- Should-fire 2: "The women's league raised funds for the community center."
- Near-miss 1: "The farmers' association hosted a dinner for local growers." (veterans swapped for farmers)
- Near-miss 2: "The chess club raised funds for the community center." (women's league swapped for a chess club)
- Prediction: **FAIL**
- Basis: Two unrelated constituencies bundled in one label.

### Test 32 — idx 29812, "elements related to instructional content and product information"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/29812

- Should-fire 1: "To assemble the shelf, first attach the side panels with the screws provided."
- Should-fire 2: "The product manual lists the dimensions, weight, and care instructions."
- Near-miss 1: "The shelf's side panels are made of solid oak with a matte finish." (assembly instruction converted to a product description)
- Near-miss 2: "The travel guide lists the distances, prices, and visiting hours." (product information swapped for travel information)
- Prediction: **FAIL**
- Basis: Instructions and product details are two different registers bundled in one label.

### Test 33 — idx 3727, "references to organizational meetings and events"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/3727

- Should-fire 1: "The board meeting is scheduled for Tuesday at ten in the boardroom."
- Should-fire 2: "Staff attended the annual company retreat last weekend."
- Near-miss 1: "The board decision was announced in a memo on Tuesday morning." (meeting swapped for a memo)
- Near-miss 2: "Staff received the annual company report last weekend." (retreat swapped for a report)
- Prediction: **FAIL**
- Basis: Meetings and events across all organizations; a broad topic.

### Test 34 — idx 13137, "phrases related to investment opportunities in various locations"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/13137

- Should-fire 1: "Investors are funding new hotels in coastal resorts this year."
- Should-fire 2: "The fund offers opportunities to invest in emerging markets abroad."
- Near-miss 1: "Tourists are visiting new hotels in coastal resorts this year." (investors swapped for tourists)
- Near-miss 2: "The fund offers grants to support small farms abroad." (investment swapped for grants)
- Prediction: **FAIL**
- Basis: Investment as a broad business topic spanning many locations and forms.

### Test 35 — idx 6127, "phrases indicating large groups or quantities"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/6127

- Should-fire 1: "Thousands of fans filled the stadium for the final."
- Should-fire 2: "Dozens of volunteers signed up within the first hour."
- Near-miss 1: "A handful of fans reached the stadium for the final." (thousands swapped for a handful)
- Near-miss 2: "Two volunteers signed up within the first hour." (dozens swapped for two)
- Prediction: **FAIL**
- Basis: Large-quantity phrasing spans crowds, dozens, and thousands; the layer-16 quantities label (idx 9470) failed the same way.

### Test 36 — idx 31687, "words indicating a state of being or existence"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/31687

- Should-fire 1: "The old house is still standing on the hill."
- Should-fire 2: "There are three chairs in the empty room."
- Near-miss 1: "The old house stands on the hill above the town." (is removed, meaning kept)
- Near-miss 2: "Three chairs fill the empty room by the window." (there are removed, meaning kept)
- Prediction: **FAIL**
- Basis: Being-verbs are basic grammar present in nearly every sentence; like the layer-16 possession label, too pervasive to isolate.

### Test 37 — idx 15158, "abbreviations or acronyms related to organizations or associations"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/15158

- Should-fire 1: "NASA announced a new launch date, and the ESA confirmed its support."
- Should-fire 2: "The FBI and the CDC issued a joint statement on Tuesday."
- Near-miss 1: "The space agency announced a new launch date, and its European partner confirmed its support." (acronyms expanded to plain names)
- Near-miss 2: "Federal investigators and health officials issued a joint statement on Tuesday." (acronyms swapped for descriptions)
- Prediction: **PASS**
- Basis: All-caps initialisms are a character-level pattern distinct from ordinary prose.

### Test 38 — idx 27446, "key terms and phrases related to significant entities and their associations"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/27446

- Should-fire 1: "Apple, led by its chief executive, dominates the smartphone market."
- Should-fire 2: "The United Nations, through its agencies, coordinates relief worldwide."
- Near-miss 1: "The bakery, led by its owner, dominates the local bread market." (significant entity swapped for a local business)
- Near-miss 2: "The town council, through its committees, coordinates events locally." (global entity swapped for a local one)
- Prediction: **FAIL**
- Basis: A vague meta-description; "significant entities" defines no detectable pattern.

### Test 39 — idx 28584, "references to regulatory actions and legal settlements involving investigations"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/28584

- Should-fire 1: "The bank agreed to a $2 billion settlement after the federal investigation."
- Should-fire 2: "Regulators fined the company for violations found during the probe."
- Near-miss 1: "The bank agreed to a new lending program after the federal review." (settlement and investigation swapped for a program and review)
- Near-miss 2: "Auditors praised the company for records kept during the audit." (fine flipped to praise)
- Prediction: **FAIL**
- Basis: Regulatory actions, settlements, and investigations bundled into one topic.

### Test 40 — idx 6627, "specific formatting or coding elements, often related to bibliographic references or citations"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/8-llamascope-res-32k/6627

- Should-fire 1: "See \\cite{smith2020} for the full derivation of the result."
- Should-fire 2: "The entry reads: doi:10.1000/xyz123, pp. 45–61."
- Near-miss 1: "See Smith's 2020 book for the full derivation of the result." (citation markup converted to prose)
- Near-miss 2: "The entry describes the journal, the volume, and the page range in words." (bibliographic format converted to prose)
- Prediction: **FAIL**
- Basis: A hedged label ("often related to") mixing formatting, code, and citations; no single pattern.

## Tests — layer 24 (source `24-llamascope-res-32k`)

### Test 41 — idx 16917, "terms related to marine organisms and their health benefits"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/16917

- Should-fire 1: "Salmon is rich in omega-3 fatty acids that support heart health."
- Should-fire 2: "Seaweed provides iodine and minerals that benefit the thyroid."
- Near-miss 1: "Chicken is rich in protein that supports muscle growth." (marine organism swapped for poultry)
- Near-miss 2: "Spinach provides iron and minerals that benefit the blood." (seaweed swapped for a land vegetable)
- Prediction: **FAIL**
- Basis: Marine life and health claims bundled; a topic pairing, not one pattern.

### Test 42 — idx 10092, "details about construction projects and their schedules"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/10092

- Should-fire 1: "The bridge project is on schedule, with completion expected in March."
- Should-fire 2: "Contractors poured the foundation two weeks ahead of the timeline."
- Near-miss 1: "The festival is on schedule, with the opening expected in March." (construction project swapped for an event)
- Near-miss 2: "Gardeners planted the flower beds two weeks ahead of the season." (contractors swapped for gardeners)
- Prediction: **FAIL**
- Basis: Construction as a broad project topic spanning buildings, bridges, and renovations.

### Test 43 — idx 6962, "academic and educational qualifications"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/6962

- Should-fire 1: "She holds a Ph.D. in biology and a master's degree in education."
- Should-fire 2: "Applicants need a bachelor's degree or an equivalent diploma."
- Near-miss 1: "She holds a senior post in biology and a teaching role in education." (credentials swapped for job roles)
- Near-miss 2: "Applicants need three years of experience or a strong portfolio." (degree swapped for experience)
- Prediction: **PASS**
- Basis: Degree and credential names are a closed lexical set: Ph.D., master's, bachelor's, diploma.

### Test 44 — idx 3510, "numerical values and identifiers used in scientific and technical contexts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/3510

- Should-fire 1: "The sample was heated to 350 K for 2.5 hours."
- Should-fire 2: "Sensor B-17 reported a pressure of 101.3 kPa."
- Near-miss 1: "The sample was heated gently for most of the afternoon." (values removed)
- Near-miss 2: "The oldest sensor reported a pressure near normal levels." (identifier and value removed)
- Prediction: **FAIL**
- Basis: Numbers plus identifiers in technical prose; the numeric labels at layer 16 (idx 30011, 9470, 21341) all failed.

### Test 45 — idx 18249, "elements related to cryptography and hashing processes"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/18249

- Should-fire 1: "The password is hashed with SHA-256 before it is stored."
- Should-fire 2: "Public-key encryption lets two parties share a secret over an open channel."
- Near-miss 1: "The file is compressed with a standard algorithm before it is stored." (hashing swapped for compression)
- Near-miss 2: "A locked diary lets its owner keep a secret from casual readers." (encryption swapped for a physical lock)
- Prediction: **PASS**
- Basis: A tight technical keyword set (hash, SHA-256, encryption, keys), like the niches that passed at layer 16.

### Test 46 — idx 24816, "instances of dialogue or verbal expressions within the text"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/24816

- Should-fire 1: ""Where are you going?" she asked. "To the market," he said."
- Should-fire 2: ""Stop!" he shouted. "Wait for me at the gate.""
- Near-miss 1: "She asked where he was going, and he said the market." (direct speech converted to reported speech; quotes removed)
- Near-miss 2: "He shouted for them to stop and wait at the gate." (spoken words converted to a summary)
- Prediction: **FAIL**
- Basis: The layer-16 dialogue feature (idx 19894) was predicted to pass and scored 0.00 even on pure quoted dialogue; dialogue labels have not validated in this SAE.

### Test 47 — idx 14728, "references to academic papers or publications"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/14728

- Should-fire 1: "The paper, published in Nature, reports a new catalyst."
- Should-fire 2: "Her article in the journal reviews fifty years of research."
- Near-miss 1: "The report, presented in March, describes a new catalyst." (published paper swapped for an internal report)
- Near-miss 2: "Her lecture in the hall reviews fifty years of research." (journal article swapped for a lecture)
- Prediction: **FAIL**
- Basis: Academic publishing as a broad topic across every field and venue.

### Test 48 — idx 5588, "key issues related to economic impact and industry growth"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/5588

- Should-fire 1: "The plant closure had a severe economic impact on the region."
- Should-fire 2: "Industry growth slowed as exports fell for a third quarter."
- Near-miss 1: "The plant closure had a severe traffic impact on the region." (economic impact swapped for traffic impact)
- Near-miss 2: "Population growth slowed as families moved away for a third year." (industry growth swapped for population growth)
- Prediction: **FAIL**
- Basis: Abstract economic framing with no consistent surface form.

### Test 49 — idx 23530, "references to published articles and sources in a document"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/23530

- Should-fire 1: "Sources: the committee's 2022 report and two newspaper articles."
- Should-fire 2: "As the article in yesterday's paper noted, prices are rising."
- Near-miss 1: "The committee's own findings and two internal memos follow." (published sources swapped for internal documents)
- Near-miss 2: "As the speaker at yesterday's meeting noted, prices are rising." (article swapped for a speaker)
- Prediction: **FAIL**
- Basis: References to sources span every citation style and document type; diffuse.

### Test 50 — idx 10617, "elements related to sports events and scores"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/10617

- Should-fire 1: "The final score was 3–1 after a late goal in extra time."
- Should-fire 2: "She won the match 6–4, 6–2 in straight sets."
- Near-miss 1: "The final turnout was strong after a late surge in ticket sales." (score and goal swapped for turnout and sales)
- Near-miss 2: "She finished the puzzle quickly and without a single error." (match swapped for a puzzle)
- Prediction: **FAIL**
- Basis: Sports events in general, with scores as one sub-pattern; both sports labels at layer 16 failed.

### Test 51 — idx 19500, "online resources and services related to academic assistance and e-commerce"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/19500

- Should-fire 1: "The site offers tutoring help and sells textbooks online."
- Should-fire 2: "Students buy courses and get homework help on the platform."
- Near-miss 1: "The office offers tutoring help and files paperwork in person." (online service swapped for an in-person office)
- Near-miss 2: "Students borrow books and get reading help at the library." (platform swapped for a library)
- Prediction: **FAIL**
- Basis: Two unrelated service domains (tutoring and e-commerce) bundled in one label.

### Test 52 — idx 4680, "specific types of agreements and collective decisions"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/4680

- Should-fire 1: "The two parties signed a trade agreement after months of talks."
- Should-fire 2: "The committee reached a consensus on the new budget."
- Near-miss 1: "The two parties signed a birthday card after months of planning." (agreement swapped for a greeting card)
- Near-miss 2: "The committee published a summary of the new budget." (consensus removed)
- Prediction: **FAIL**
- Basis: Agreements and decisions across law, politics, and business; diffuse forms.

### Test 53 — idx 23356, "expressions of uncertainty or conditions in various contexts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/23356

- Should-fire 1: "If it rains tomorrow, we might cancel the picnic."
- Should-fire 2: "Perhaps the package will arrive unless the road closes."
- Near-miss 1: "Since it is sunny today, we will hold the picnic." (condition and uncertainty flipped to certainty)
- Near-miss 2: "The package will certainly arrive because the road is open." (uncertainty flipped to certainty)
- Prediction: **FAIL**
- Basis: Uncertainty and conditionals are basic grammar expressible in countless forms.

### Test 54 — idx 29911, "details about professional achievements and background in photography and film"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/29911

- Should-fire 1: "The photographer won international awards for her documentary films."
- Should-fire 2: "His career in cinematography spans thirty years and forty features."
- Near-miss 1: "The painter won international awards for her landscape canvases." (photography and film swapped for painting)
- Near-miss 2: "His career in architecture spans thirty years and forty buildings." (cinematography swapped for architecture)
- Prediction: **FAIL**
- Basis: A biographical topic spanning two professions and any career detail.

### Test 55 — idx 8994, "terms related to social sciences and their theories"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/8994

- Should-fire 1: "Sociologists study how institutions shape individual behavior."
- Should-fire 2: "The theory of social capital explains trust within communities."
- Near-miss 1: "Biologists study how environments shape individual organisms." (social science swapped for natural science)
- Near-miss 2: "The theory of plate tectonics explains movement within the crust." (social theory swapped for a geological theory)
- Prediction: **FAIL**
- Basis: An entire academic division in one label.

### Test 56 — idx 29746, "elements related to Python programming concepts and functionalities"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/29746

- Should-fire 1: "Use a list comprehension to square every number in the list."
- Should-fire 2: "The script imports pandas and prints the first five rows."
- Near-miss 1: "Use a spreadsheet formula to square every number in the column." (Python construct swapped for a spreadsheet formula)
- Near-miss 2: "The clerk imports ledgers and prints the first five pages." (script actions converted to office work)
- Prediction: **FAIL**
- Basis: Every code label failed in the layer-16 replication, including the language-specific Java ones (idx 31073, 23454).

### Test 57 — idx 7981, "geographical or location-based terms"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/7981

- Should-fire 1: "The river flows north through the valley toward the coast."
- Should-fire 2: "Their village sits on the border between the two provinces."
- Near-miss 1: "The pipe runs straight through the building toward the basement." (geography swapped for plumbing)
- Near-miss 2: "Their house sits on the street between the two shops." (regional geography swapped for a street scene)
- Prediction: **FAIL**
- Basis: Location language in general is everywhere in prose; the specific-locations label at layer 16 (idx 11708) also failed.

### Test 58 — idx 26744, "concepts related to eco-friendliness and nature immersion"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/26744

- Should-fire 1: "The retreat offers eco-friendly cabins deep in the forest."
- Should-fire 2: "Guests unplug and immerse themselves in nature for a week."
- Near-miss 1: "The hotel offers luxury suites deep in the city center." (eco retreat swapped for a city hotel)
- Near-miss 2: "Guests check in and attend conferences for a week." (nature immersion swapped for conferences)
- Prediction: **FAIL**
- Basis: A marketing-flavored theme with diffuse vocabulary.

### Test 59 — idx 27334, "various levels of measurement or evaluation"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/27334

- Should-fire 1: "The scale rates moisture from low to high in five levels."
- Should-fire 2: "Inspectors graded the building's condition as fair overall."
- Near-miss 1: "The recipe lists ingredients from largest to smallest in five groups." (measurement scale swapped for a recipe ordering)
- Near-miss 2: "Inspectors described the building's condition in a short note." (grade swapped for a description)
- Prediction: **FAIL**
- Basis: Measurement and evaluation at every level of abstraction; a meta-label.

### Test 60 — idx 3103, "references to the Persian Sassanians and their historical context"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/3103

- Should-fire 1: "The Sassanian Empire ruled Persia until the seventh century."
- Should-fire 2: "Khosrow I reformed the Sassanian tax system and army."
- Near-miss 1: "The Roman Empire ruled its provinces until the fifth century." (Sassanians swapped for Romans)
- Near-miss 2: "The mayor reformed the municipal tax system and budget." (Sassanian ruler swapped for a mayor)
- Prediction: **PASS**
- Basis: A single named historical civilization with distinctive names and terms; a closed entity cluster.

### Test 61 — idx 9044, "references to individuals and organizations involved in technology and machine learning"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/9044

- Should-fire 1: "Researchers at Google published a new machine learning model."
- Should-fire 2: "The AI startup hired engineers from three universities."
- Near-miss 1: "Researchers at the institute published a new ocean survey." (machine learning swapped for oceanography)
- Near-miss 2: "The bakery startup hired bakers from three culinary schools." (AI startup swapped for a bakery)
- Prediction: **FAIL**
- Basis: The whole technology industry as a topic; no narrow pattern.

### Test 62 — idx 19170, "references to companies and organizational structures"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/19170

- Should-fire 1: "The company reorganized its subsidiaries into three divisions."
- Should-fire 2: "The corporation's board oversees a holding structure abroad."
- Near-miss 1: "The family reorganized its kitchen into three sections." (company structure swapped for a household one)
- Near-miss 2: "The club's committee oversees a membership roster locally." (corporation swapped for a club)
- Prediction: **FAIL**
- Basis: Companies and organizational structures in general; diffuse.

### Test 63 — idx 24001, "phrases related to the frequency and regularity of activities or occurrences"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/24001

- Should-fire 1: "The bus runs every thirty minutes on weekdays."
- Should-fire 2: "She visits her dentist twice a year for a checkup."
- Near-miss 1: "The bus is at the depot on weekdays for cleaning." (frequency removed)
- Near-miss 2: "She visits her dentist across town for a checkup." (twice a year removed)
- Prediction: **FAIL**
- Basis: Frequency expressions are ordinary grammar in all prose.

### Test 64 — idx 19832, "references to storage facilities and related concepts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/19832

- Should-fire 1: "They rented a climate-controlled storage unit for the furniture."
- Should-fire 2: "The self-storage facility offers 10x10 units with drive-up access."
- Near-miss 1: "They rented a furnished apartment downtown for the summer." (storage unit swapped for an apartment)
- Near-miss 2: "The parking facility offers monthly passes with garage access." (storage swapped for parking)
- Prediction: **PASS**
- Basis: A narrow commercial niche with distinctive vocabulary (self-storage, units, climate-controlled), like the resorts niche that passed at layer 16.

### Test 65 — idx 29452, "references to blame and criticism regarding media and political narratives"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/29452

- Should-fire 1: "Commentators blamed the media for distorting the election story."
- Should-fire 2: "Critics say the coverage pushed a misleading political narrative."
- Near-miss 1: "Commentators praised the media for clarifying the election story." (blame flipped to praise)
- Near-miss 2: "Analysts say the coverage reflected a cautious editorial approach." (criticism swapped for a neutral assessment)
- Prediction: **FAIL**
- Basis: An abstract stance toward media narratives; diffuse vocabulary.

### Test 66 — idx 21040, "conjunctions and interrogative phrases related to inquiries or questions"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/21040

- Should-fire 1: "What did he say, and where did he go afterward?"
- Should-fire 2: "Tell me whether you agree, or if you would rather wait."
- Near-miss 1: "He said his piece at the meeting this morning." (question and conjunction removed)
- Near-miss 2: "Tell me your answer at noon tomorrow, please." (whether/or construction removed)
- Prediction: **FAIL**
- Basis: Conjunctions and question words are basic grammar present everywhere.

### Test 67 — idx 20626, "references to specific locations and entities"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/20626

- Should-fire 1: "The office is at 1200 Sixth Avenue in New York."
- Should-fire 2: "Trains leave from Gare du Nord in Paris every hour."
- Near-miss 1: "The office is on a wide avenue in the city center." (specific address removed)
- Near-miss 2: "Trains leave from the main station in the capital every hour." (named station and city removed)
- Prediction: **FAIL**
- Basis: The near-identical layer-16 label (idx 11708, specific locations and addresses) failed, with one should-fire scoring 0.00.

### Test 68 — idx 6413, "positive descriptors and expressions of success"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/6413

- Should-fire 1: "Her presentation was brilliant, and the launch was a triumph."
- Should-fire 2: "The team celebrated an outstanding result this quarter."
- Near-miss 1: "Her presentation was lengthy, and the launch was on Tuesday." (positive descriptors swapped for neutral ones)
- Near-miss 2: "The team recorded a routine result this quarter." (outstanding swapped for routine)
- Prediction: **FAIL**
- Basis: Positive wording spans every domain; diffuse sentiment vocabulary.

### Test 69 — idx 8246, "CSS styling properties related to borders and box shadows"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/8246

- Should-fire 1: "border: 1px solid #333; box-shadow: 0 2px 6px rgba(0,0,0,0.2);"
- Should-fire 2: "The card uses border-radius: 8px and a subtle box-shadow for depth."
- Near-miss 1: "The frame has a thin dark edge and a soft shadow beneath it." (CSS properties converted to prose)
- Near-miss 2: "The designer described the card's rounded corners and soft shadow in the style guide." (properties described in words, no CSS syntax)
- Prediction: **FAIL**
- Basis: In the layer-16 replication every code-syntax label failed, including narrow ones like Java annotations (idx 31073); narrowness did not rescue code labels in this SAE.

### Test 70 — idx 26702, "references to programming tasks and documentation practices"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/26702

- Should-fire 1: "Update the README after you refactor the login module."
- Should-fire 2: "The developer documented each function and opened a pull request."
- Near-miss 1: "Update the itinerary after you rearrange the travel schedule." (programming task swapped for a travel task)
- Near-miss 2: "The author revised each chapter and sent the manuscript to the editor." (developer documentation swapped for book editing)
- Prediction: **FAIL**
- Basis: Programming work plus documentation habits bundled; two practices in one label.

### Test 71 — idx 15269, "references to charter schools and related educational systems"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/15269

- Should-fire 1: "The charter school admits students through a public lottery."
- Should-fire 2: "Charter schools in the district must renew their charters every five years."
- Near-miss 1: "The private school admits students through an application review." (charter swapped for private)
- Near-miss 2: "Public schools in the district must renew their budgets every five years." (charter renewal swapped for budget renewal)
- Prediction: **PASS**
- Basis: A single institution type with distinctive terms (charter, lottery admissions, charter renewal), like the regulatory niche that passed at layer 16.

### Test 72 — idx 31920, "punctuation marks and related terms that emphasize arrangements or structures"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/31920

- Should-fire 1: "Note: the items are grouped as follows — first, second, third."
- Should-fire 2: "Use a semicolon; it links the two clauses in the list."
- Near-miss 1: "Note that the items are grouped in the order given here." (colon and dash removed)
- Near-miss 2: "Use a pause there since it links the two clauses in the list." (semicolon named and used, then removed)
- Prediction: **FAIL**
- Basis: Punctuation labels failed at layer 16 (idx 8211); marks appear in all text and do not isolate.

### Test 73 — idx 12653, "information related to giveaways and contests"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/12653

- Should-fire 1: "Enter our giveaway for a chance to win a free laptop."
- Should-fire 2: "The contest deadline is Friday; winners will be announced Monday."
- Near-miss 1: "Read our newsletter for a chance to learn about laptops." (giveaway swapped for a newsletter)
- Near-miss 2: "The survey deadline is Friday; results will be announced Monday." (contest swapped for a survey)
- Prediction: **FAIL**
- Basis: Promotions are a broad marketing topic with varied wording (giveaway, sweepstakes, raffle, contest).

### Test 74 — idx 27839, "references to outdoor activities and sports"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/27839

- Should-fire 1: "They spent the weekend hiking and kayaking in the mountains."
- Should-fire 2: "Cycling along the river trail is popular in the summer."
- Near-miss 1: "They spent the weekend reading and cooking at the cabin." (outdoor activities swapped for indoor ones)
- Near-miss 2: "Driving along the river road is popular in the summer." (cycling swapped for driving)
- Prediction: **FAIL**
- Basis: All outdoor recreation in one label; a broad topic.

### Test 75 — idx 8622, "themes related to digital privacy and data control issues"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/8622

- Should-fire 1: "Users should control who can access their personal data online."
- Should-fire 2: "The new privacy law limits how apps track their users."
- Near-miss 1: "Users should choose who can borrow their garden tools this spring." (data access swapped for tool lending)
- Near-miss 2: "The new traffic law limits how trucks use the bridge." (privacy law swapped for a traffic law)
- Prediction: **FAIL**
- Basis: A policy theme spanning law, apps, and user rights; thematic, not a surface pattern.

### Test 76 — idx 3155, "mentions of specific dates in February"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/3155

- Should-fire 1: "The workshop is scheduled for February 12 at the main hall."
- Should-fire 2: "Her visa expires on February 28 of next year."
- Near-miss 1: "The workshop is scheduled for March 12 at the main hall." (February swapped for March)
- Near-miss 2: "Her visa expires late next winter, sometime after the holidays." (specific February date removed)
- Prediction: **FAIL**
- Basis: The layer-16 specific-dates feature (idx 4693) was predicted to pass and failed; date labels have not validated in this SAE despite their crisp surface form.

### Test 77 — idx 12706, "terms related to DNS (Domain Name System) configurations and settings"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/12706

- Should-fire 1: "Update the DNS A record and set the TTL to 300 seconds."
- Should-fire 2: "The nameservers point the domain to the new hosting provider."
- Near-miss 1: "Update the IP address table and set the timeout to 300 seconds." (DNS record swapped for a generic table)
- Near-miss 2: "The phone directory lists the business at the new office address." (nameservers swapped for a phone directory)
- Prediction: **PASS**
- Basis: A tight technical keyword set (DNS records, TTL, nameservers), like the radio-licensing niche that passed at layer 16.

### Test 78 — idx 1726, "programming constructs and syntax, particularly related to setting values and property definitions"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/1726

- Should-fire 1: "config.timeout = 30; config.retries = 3;"
- Should-fire 2: "user.name = 'Ana'; user.active = true;"
- Near-miss 1: "The settings give a timeout of thirty and three retries in total." (assignments converted to prose)
- Near-miss 2: "Ana is an active user of the records system." (property assignments converted to prose)
- Prediction: **FAIL**
- Basis: Code-syntax labels failed uniformly at layer 16, including narrow assignment-like patterns.

### Test 79 — idx 25362, "phrases indicating relationships or connections among subjects"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/25362

- Should-fire 1: "The two companies are partners in a joint venture."
- Should-fire 2: "Her health is closely linked to her sleep habits."
- Near-miss 1: "The two companies are rivals in a crowded market." (partnership swapped for rivalry)
- Near-miss 2: "Her health is described in detail in the annual report." (linkage removed)
- Prediction: **FAIL**
- Basis: Relationships in the abstract have no consistent surface form.

### Test 80 — idx 31376, "words and phrases related to cyclical or revolving concepts"

Neuronpedia: https://www.neuronpedia.org/llama3.1-8b/24-llamascope-res-32k/31376

- Should-fire 1: "The wheel completes one full cycle every twelve seconds."
- Should-fire 2: "The seasons revolve in an endless recurring pattern."
- Near-miss 1: "The wheel moves in a straight line for twelve meters." (cycle swapped for linear motion)
- Near-miss 2: "The displays change in a fixed sequence every year." (revolving pattern swapped for a fixed sequence)
- Prediction: **FAIL**
- Basis: A concept family expressed through many unrelated words (cycle, revolve, rotate, recur).

---

*End of locked predictions. Prediction tally: 11 PASS / 69 FAIL (layer 8: tests 1–40, 5 PASS; layer 24: tests 41–80, 6 PASS). Locked November 14, 2026. This file must not be edited after locking.*
