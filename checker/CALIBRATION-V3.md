# Calibration report

Compared 40 features (matched by index) between the checker run and the human ground truth. Pass rule on both sides: min(should-fire) > max(near-miss).

**Agreement: 38/40 (95.0%)**

- Both PASS: 10
- Both FAIL: 28
- Checker PASS / human FAIL: 0
- Checker FAIL / human PASS: 2

## Disagreements

- idx 10276 "products related to fashion and beauty": checker FAIL (SF 4.50, 0.00 · NM 3.59, 0.00 · margin -3.59) vs human PASS (SF 4.50, 8.94 · NM 0.00, 4.34 · margin 0.16)
- idx 12964 "references to crafting materials and methods": checker FAIL (SF 10.69, 3.92 · NM 6.69, 17.38 · margin -13.45) vs human PASS (SF 4.56, 13.25 · NM 0.00, 0.00 · margin 4.56)

## Mechanism tags vs established classes

**Mechanism accuracy on tagged ground truth: 4/17 (23.5% of 17 established cases; a case with no checker tag counts as a miss)**

- idx 18: expected displaced-theme, checker register (MISS)
- idx 1029: expected word-form, checker register (MISS)
- idx 2081: expected document-bound, checker register (MISS)
- idx 2580: expected register, checker displaced-theme (MISS)
- idx 2625: expected document-bound, checker unresolved (MISS)
- idx 3070: expected unresolved, checker document-bound (MISS)
- idx 3349: expected document-bound, checker word-form (MISS)
- idx 3580: expected register, checker unresolved (MISS)
- idx 5072: expected register, checker register (match)
- idx 5158: expected word-form, checker word-form (match)
- idx 6515: expected document-bound, checker unresolved (MISS)
- idx 7196: expected unresolved, checker unresolved (match)
- idx 7623: expected register, checker unresolved (MISS)
- idx 8630: expected register, checker document-bound (MISS)
- idx 8743: expected word-form, checker register (MISS)
- idx 14520: expected unresolved, checker register (MISS)
- idx 14719: expected word-form, checker word-form (match)
