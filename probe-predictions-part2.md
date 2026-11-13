# Follow-up part 2 — predictions for the remaining 12 silent features

Thu Nov 12, 2026, ~8:25 PM EST. Written after token-level inspection of each
feature's stored positive examples, before any probe ran. Same endpoint and
scoring as the pilot (max activation across tokens).

- **1029, "ancient figures and mythological or legendary elements":** peaks
  sit on Chinese name fragments (xiang, ian, chi) in Chinese-legend and
  card-game-code contexts. Prediction: Chinese-mythology text fires; Greek
  myth stays at zero.
- **3070, "reputation and its effects":** peaks scatter across generic web
  text, maximum stored value only 12.47; one peak is the word "reputation"
  in forum text. Prediction: weak firing at best, on forum-style reputation
  talk; possibly no consistent trigger exists.
- **3349, "diversity and inclusion":** peaks sit on formatting tokens
  (":" , ".", blank lines) in heading-and-list business pages. Prediction:
  heading/colon/list formats fire; diversity prose does not.
- **3580, "personal relationships and family connections":** peaks sit on
  "his" inside obituaries ("preceded in death by his father," "survived by
  his loving wife of 42 years"). Prediction: obituary formulas fire
  strongly; ordinary family sentences stay at zero.
- **5072, "medical conditions and anatomical processes":** peaks sit on
  dense clinical terms (perfusion, radiation, overuse) in journal prose.
  Prediction: clinical register fires; plain patient language does not.
- **5158, "buttons in a UI or web interface":** 30 of 40 positive peaks sit
  on the token "btn" in HTML class attributes. Prediction: "btn" in code
  fires at full strength; the word "button" never fires.
- **6515, "a specific shoe brand":** peaks sit on "shoes" inside
  keyword-stuffed SEO spam repeating "supra shoes." Prediction: spam-style
  repetition fires; natural brand sentences stay at zero.
- **7196, "racism and discriminatory behaviors":** peaks scatter over
  argumentative prose, maximum ~15. Prediction: weak firing on formal
  case-report register at best; possibly diffuse.
- **7623, "questions and inquiries":** peaks sit mostly on newline tokens
  in forum Q&A pages; one strong peak on "?" inside a forum question.
  Prediction: forum Q&A format fires; a bare question does not.
- **8630, "music and artistic collaborations":** peaks sit on "talk,"
  "episode," "joins," "show" in radio/talk-show contexts. Prediction:
  guest-appearance register fires; music content alone does not.
- **8743, "negative phrases… obligation or denial":** 28 of 40 peaks sit on
  the token "or," 7 more on "nor." Prediction: or/nor constructions fire;
  obligation and denial language does not.
- **14520, "governance and political processes":** peaks sit on function
  words; one strong context is archaic Federalist-style prose, another is
  nature writing. Prediction: archaic formal prose fires; modern political
  process stays at zero; the verdict may end diffuse.
