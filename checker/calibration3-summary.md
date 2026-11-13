# Checker results

Pass rule (pilot rule): min(should-fire) > max(near-miss). Prompts were locked before scoring (SHA-256 in calibration3-prompts-locked.sha256).

**Scored so far: 10 pass, 30 fail, 0 incomplete of 40.**
- Layer 12: 10 pass, 30 fail, 0 incomplete
- Prediction accuracy: 15/40 (38%)

- Test 1 (L12, idx 18) "terms related to food and culinary subjects": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: register
- Test 2 (L12, idx 483) "references to the Windows operating system": SF 12.44, 4.19 · NM 0.00, 0.00 · margin 4.19 · **PASS** (predicted PASS)
- Test 3 (L12, idx 869) "geographical and administrative terms related to specific regions or districts": SF 11.56, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: displaced-theme
- Test 4 (L12, idx 1029) "references to ancient figures and mythological or legendary elements": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: register
- Test 5 (L12, idx 1302) "shipping-related terms and phrases for large items": SF 3.81, 5.34 · NM 0.00, 0.00 · margin 3.81 · **PASS** (predicted PASS)
- Test 6 (L12, idx 1501) "moments of surprise or unexpected events, particularly those that are positive or celebratory in nature.": SF 47.25, 0.00 · NM 19.00, 0.00 · margin -19.00 · **FAIL** (predicted FAIL) · mechanism: displaced-theme
- Test 7 (L12, idx 1643) "references to light and illumination contexts": SF 30.00, 17.75 · NM 41.25, 38.75 · margin -23.50 · **FAIL** (predicted FAIL) · mechanism: word-form
- Test 8 (L12, idx 1657) "references to the name “Tom”": SF 20.25, 21.38 · NM 0.00, 13.50 · margin 6.75 · **PASS** (predicted PASS)
- Test 9 (L12, idx 2081) "periods and punctuation that signify the end of sentences": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · mechanism: register
- Test 10 (L12, idx 2580) "references to literary works and notable authors": SF 5.28, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: displaced-theme
- Test 11 (L12, idx 2625) "specific scientific or technical terms related to genetics and molecular biology": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: unresolved
- Test 12 (L12, idx 3070) "concepts related to reputation and its effects": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: document-bound
- Test 13 (L12, idx 3349) "phrases related to diversity and inclusion in various contexts": SF 3.30, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: word-form
- Test 14 (L12, idx 3580) "elements of personal relationships and family connections": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: unresolved
- Test 15 (L12, idx 3592) "details about concert schedules and ticket sales": SF 23.12, 34.25 · NM 4.62, 0.00 · margin 18.50 · **PASS** (predicted PASS)
- Test 16 (L12, idx 4207) "expressions of “coolness” or related positive attributes": SF 33.75, 33.75 · NM 26.00, 0.00 · margin 7.75 · **PASS** (predicted FAIL)
- Test 17 (L12, idx 4593) "concepts related to simplicity and straightforwardness": SF 17.00, 18.25 · NM 0.00, 16.88 · margin 0.12 · **PASS** (predicted PASS)
- Test 18 (L12, idx 5072) "terms related to medical conditions and anatomical processes": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: register
- Test 19 (L12, idx 5158) "elements related to buttons in a UI or web interface": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: word-form
- Test 20 (L12, idx 6515) "references to a specific shoe brand": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · mechanism: unresolved
- Test 21 (L12, idx 6865) "references to personal beliefs, self-identification, and emotional experiences": SF 5.53, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · mechanism: unresolved
- Test 22 (L12, idx 7196) "discussions and references to issues of racism and discriminatory behaviors": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: unresolved
- Test 23 (L12, idx 7223) "phrases that indicate summary or overall conclusions": SF 0.00, 21.12 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: word-form
- Test 24 (L12, idx 7467) "words related to reading devices and the eBook industry": SF 0.00, 3.95 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: document-bound
- Test 25 (L12, idx 7623) "questions and inquiries about various topics or contexts": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted FAIL) · mechanism: unresolved
- Test 26 (L12, idx 7798) "expressions of happiness and positive emotions": SF 8.25, 12.81 · NM 0.00, 0.00 · margin 8.25 · **PASS** (predicted PASS)
- Test 27 (L12, idx 8123) "references to different types and characteristics of pipes": SF 36.75, 37.25 · NM 23.88, 24.75 · margin 12.00 · **PASS** (predicted FAIL)
- Test 28 (L12, idx 8630) "discussions related to music and artistic collaborations": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: document-bound
- Test 29 (L12, idx 8743) "negative phrases and expressions related to obligation or denial": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: register
- Test 30 (L12, idx 10276) "products related to fashion and beauty": SF 4.50, 0.00 · NM 3.59, 0.00 · margin -3.59 · **FAIL** (predicted PASS) · mechanism: displaced-theme
- Test 31 (L12, idx 11270) "forward-looking statements regarding business projections and associated risks": SF 0.00, 22.88 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: displaced-theme
- Test 32 (L12, idx 12608) "terms related to control and regulation": SF 37.75, 0.00 · NM 37.25, 33.25 · margin -37.25 · **FAIL** (predicted FAIL) · mechanism: word-form
- Test 33 (L12, idx 12964) "references to crafting materials and methods": SF 10.69, 3.92 · NM 6.69, 17.38 · margin -13.45 · **FAIL** (predicted PASS) · mechanism: displaced-theme
- Test 34 (L12, idx 13230) "terms related to electricity and power infrastructure": SF 15.12, 16.62 · NM 0.00, 0.00 · margin 15.12 · **PASS** (predicted PASS)
- Test 35 (L12, idx 14520) "terms related to governance and political processes": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: register
- Test 36 (L12, idx 14719) "terms related to colors and color coding": SF 0.00, 0.00 · NM 0.00, 0.00 · margin 0.00 · **FAIL** (predicted PASS) · mechanism: word-form
- Test 37 (L12, idx 15035) "phrases that highlight the concept of “short” in various contexts": SF 38.25, 44.75 · NM 33.25, 44.25 · margin -6.00 · **FAIL** (predicted FAIL) · mechanism: word-form
- Test 38 (L12, idx 15337) "mentions of the term “Mercury,” particularly in relation to its propulsion systems and legal implications": SF 12.00, 13.44 · NM 6.38, 0.00 · margin 5.62 · **PASS** (predicted FAIL)
- Test 39 (L12, idx 15623) "references to the color yellow and its variations": SF 44.50, 34.25 · NM 16.38, 39.25 · margin -5.00 · **FAIL** (predicted PASS) · mechanism: word-form
- Test 40 (L12, idx 16358) "questions and statements regarding intentions, plans, or purposes": SF 0.00, 0.00 · NM 0.00, 3.81 · margin -3.81 · **FAIL** (predicted PASS) · mechanism: word-form
