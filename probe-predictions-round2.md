# Round 2 predictions — written after round 1 results, before round 2 ran

Thu Nov 12, 2026, ~8:20 PM EST.

Round 1 outcome that motivates round 2: every idx 2081 and idx 2625 probe
scored 0, including document-boundary formats. Inspection of the full
stored sets then showed: (a) entries with maxValue 0 are a shared
zero-activation bin, identical across features, and carry no information;
(b) idx 2081's positive non-boundary peaks cluster on citation punctuation
(")).", ").", "]).") at 5–13, with plain periods in long prose at 3–9;
(c) idx 2625's positive peaks are the boundary token plus two Swift code
identifiers (unknownFields 12.56, Decoder 9.84).

- idx 2081: a citation-cluster sentence fires moderately (5–13 range);
  a long ordinary paragraph fires weakly if accumulated context is the
  missing ingredient; both may still be zero, which would leave
  "fires only inside long multi-document windows" as the finding.
- idx 2625: a Swift protobuf code snippet fires moderately if the code
  trace is real; a long dense genetics abstract stays at or near zero.
- idx 2580 clarifiers: present-tense catalog copy about canonical works
  ("Hamlet is a tragedy by William Shakespeare. The play tells the story
  of...") fires if the trigger is catalog register; stays low if the
  trigger is modern blurb language specifically.
