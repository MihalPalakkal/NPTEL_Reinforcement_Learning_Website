# Extraction and validation audit

Source: Assignments.pdf (59 pages), supplied locally by the user. All 59 embedded screenshots were extracted at their original 1366 × 768 resolution and inspected visually. The PDF has no selectable text. Tesseract OCR was run at native and enlarged resolutions, followed by cropped-region OCR and reviewed corrections. Upscaling aids reading but does not create additional source detail.

The complete identified inventory is **113 questions across 12 weeks**. No question visible in the supplied PDF was silently omitted. Question numbers restart per week and are kept unchanged. The source ends Week 5 at Q8 and Week 12 at Q5; there is no evidence of further questions in those sections.

## Inventory

| Week | PDF pages | Identified | Extracted | Verified PDF keys | Independent keys | Questions with figures |
|---|---|---:|---:|---:|---:|---:|
| 1 | 1–5 | 10 | 10 | 10 | 0 | 0 |
| 2 | 6–10 | 10 | 10 | 10 | 0 | 0 |
| 3 | 11–15 | 10 | 10 | 9 | 1 | 0 |
| 4 | 16–20 | 10 | 10 | 10 | 0 | 0 |
| 5 | 21–24 | 8 | 8 | 8 | 0 | 0 |
| 6 | 25–30 | 10 | 10 | 10 | 0 | 1 |
| 7 | 31–35 | 10 | 10 | 10 | 0 | 0 |
| 8 | 36–40 | 10 | 10 | 10 | 0 | 0 |
| 9 | 41–45 | 10 | 10 | 10 | 0 | 0 |
| 10 | 46–50 | 10 | 10 | 10 | 0 | 0 |
| 11 | 51–56 | 10 | 10 | 10 | 0 | 4 |
| 12 | 57–59 | 5 | 5 | 5 | 0 | 1 |

**Totals: 113 extracted; 112 PDF answer keys; 1 independently derived key; 0 unresolved scored answer keys.** There is one unrecoverable original option fragment, handled as the labelled restoration below. Coverage and answer correctness are separate claims: the 112 keys reproduce the PDF labels; they are not presented as a new independent proof of every course statement.

## Week 3, Question 4: user-authorized restoration

Page 12 cuts off the bottom of this question. The statement, four candidate update equations, and options A–C are visible. The final option and accepted-answer label are not visible anywhere else in this PDF. The user explicitly requested that the correct answer and proper options be supplied independently.

- A: (i), (ii) — visible in the PDF.
- B: (i), (iv) — visible in the PDF; independently verified correct.
- C: (ii), (iii) — visible in the PDF.
- D: (ii), (iv) — independently reconstructed distractor, clearly labelled in the quiz; not claimed to be recovered original text.

Let p1 = exp(w1ᵀs)/(exp(w1ᵀs)+exp(w2ᵀs)) and p2 = 1−p1. For chosen action a1, the gradient of log π(a1|s) with respect to w1 is (1−p1)s, and with respect to w2 it is −p2s. REINFORCE adds αr times these gradients, giving updates (i) and (iv). A numerical finite-difference test agrees with both derivatives to within 1e−7.

The independent derivation uses the standard log-policy gradient and softmax definitions documented in [OpenAI Spinning Up](https://spinningup.openai.com/en/latest/spinningup/rl_intro3.html). This is explicitly labelled an independent explanation, not an official NPTEL explanation.

## Original diagrams and shared information

| Asset | Mapping | Source |
|---|---|---|
| week6-q7-cliff.png | Week 6 Q7 | Page 28; entire cliff grid, safe/optimal paths, rewards, S/G labels and caption |
| week11-shared-taxi-grid.png | Week 11 Q3, Q4, Q5, Q6 | Page 52; complete taxi-world grid, obstacles, R/G/B/Y labels |
| week11-shared-call-graph.png | Week 11 Q3, Q4, Q5, Q6 | Page 52; complete call graph, arrows, primitive and composite tasks |
| week12-q5-grid.png | Week 12 Q5 | Page 59; grid, gray obstacles, outer wall and direction compass |

The images are direct crops of original embedded screenshots. There are no redrawn, generated, stock, or externally hosted replacements. Cropping coordinates are documented in `scripts/finalize.py`. Diagrams retain their aspect ratio and have a zoomable lightbox. Missing-image fallbacks identify a missing local asset. Shared Week 11 information is duplicated by reference onto all four applicable records. Week 12 Q2 includes the shared observation assumptions from Q1.

## Text, math, answer provenance

- The rendered quiz uses extracted and reviewed text with radio buttons or checkboxes. It is not a screenshot-based quiz.
- Greek letters, subscripts, superscripts, fractions, sums and piecewise expressions are transcribed to KaTeX. Every math expression is parsed in the test suite.
- Original statement and option crops remain available under an optional source-comparison control. Original answer evidence is hidden until feedback or review is allowed.
- The 112 source keys use accepted-answer labels, including when a screenshot's selected answer was incorrect. Selected screenshot controls were never treated as the key on their own.
- All option orderings are retained for the visible source content. Only the explicitly identified Week 3 Q4 distractor was reconstructed.
- All source questions are worth one mark. The app uses exact-match scoring with no partial credit. The source's historical partial scores are not copied into personal results.
- No official explanations were present in the PDF. All other explanations remain null; the UI says when no official explanation was provided.
- Course-specific wording/ambiguities remain source-faithful. In particular, the official Week 1 Q6, Week 5 Q4 and Week 8 Q7 answer keys are preserved as printed rather than silently substituted with a different theoretical interpretation.

## Repeatability and checks

`scripts/extract.py` extracts all 59 screenshots, uses the reviewed coordinate inventory to crop statements and options, and runs batch OCR. `scripts/finalize.py` applies reviewed transcriptions and maps original figures. `scripts/validate_bank.py` validates all IDs, week counts, sequential question numbers, option counts/IDs, answer membership and provenance, balanced math delimiters, and every local asset reference. It checked 649 referenced local image files successfully.

`data/questions.json` is the final application bank. `data/questions-ocr.json` is unreviewed intermediate OCR and is never loaded by the application. `question-inventory.csv` lists every question, type, option count, key, provenance, and source page. `data/audit.json` supplies machine-readable week counts and validation status.

See `VALIDATION.md` in the source package for functional and browser test coverage. The original PDF itself is not redistributed in the website.
