# Follow-up probes — predictions written before any probe was run

Thu Nov 12, 2026, ~8:12 PM EST. Written after inspecting the five features'
stored top examples (public API data) and before any probe activation was
queried. Probes run against gemma-2-2b, source 12-gemmascope-res-16k, via
Neuronpedia's activation endpoint. Score = max activation across tokens.

## idx 14719 — label: "terms related to colors and color coding"
Stored evidence: 40 of 45 stored peaks land on a form of the word "color"
(color / Color / COLOR / colors), many inside code constants such as
COLOR_MENU_TEXT. The feature's top promoted tokens are all forms of "color."
Pilot sentences named red, black, green, blue — never the word "color."
- Prediction: any probe containing the token "color"/"COLOR" fires strongly,
  including code; probes with color terms but no "color" token stay at or
  near zero; "Colorado" does not fire (different token).

## idx 2081 — label: "periods and punctuation that signify the end of sentences"
Stored evidence: 12 of 45 peaks land on the <bos> document-boundary token
immediately following a period at the end of a prior document; 7 more land
on "." itself. Isolated custom text contains no mid-text <bos>.
- Prediction: an ordinary mid-text period fires weakly or not at all; a
  period followed by a blank line and a new heading (document-boundary
  format) fires clearly higher; a sentence with no period stays at zero.

## idx 2625 — label: "specific scientific or technical terms related to genetics and molecular biology"
Stored evidence: 14 of 45 peaks land on <bos> after varied preceding text
(code, Wikipedia, legal text); the rest scatter. No genetics concentration
in the top examples.
- Prediction: genetics content alone, even a dense paragraph, stays low;
  document-boundary formats fire regardless of whether the following
  document is about genetics.

## idx 2580 — label: "references to literary works and notable authors"
Stored evidence: peaks land on small function words (of / to / and) inside
long descriptive blurbs about books and games; no peak lands on an author
name or title. Pilot prompts were single short factual sentences.
- Prediction: a full book-blurb paragraph fires; the same names compressed
  into one short sentence stay low; a video-game blurb of the same shape
  also fires, which would make this a creative-work-description register,
  not literature specifically.

## idx 18 — label: "terms related to food and culinary subjects"
Stored evidence: peaks concentrate on "Environmental" (7), "survival" (3),
"Architecture" (2) — mostly inside university institution names ("College of
Architecture and Environmental Design") and one genomics passage ("cell
death and survival"). Genuine food peaks (fish, Food, burgers) are rare and
weaker. Only 21 of 45 stored examples contain food words at all.
- Prediction: the institution-name phrases fire strongly; "survival" in a
  genomics-style sentence fires moderately; plain food sentences, even
  food-dense ones, stay at or near zero.
