# NPTEL Quiz Arena

A complete local-first React + TypeScript quiz application for the 59-page NPTEL Reinforcement Learning assignment PDF. All 12 weeks and 113 source questions are included. Questions and options are real text; mathematical expressions use bundled KaTeX. Only original diagrams and optional source-comparison evidence use images.

## Run

Requires Node.js 20.19+ (or 22.12+) and npm.

```sh
npm install
npm run dev
```

Open the local URL printed by Vite. For a production build:

```sh
npm run build
npm run preview
```

The built `dist/` directory can be served by any static web server. Do not open `index.html` directly using a file URL. The production service worker caches the application, question bank, font files, and images after the first successful online load, allowing offline revisits. The development server does not register the service worker.

## Features

- 12 weekly quizzes: 10 questions each except Week 5 (8) and Week 12 (5), matching the PDF.
- Full 113-question challenge, with no truncation.
- Custom practice: selected weeks, random subset, original or shuffled order.
- Immediate feedback by default, including right/wrong and complete correct answers. Multi-select selections are evaluated after each click; all required answers must be selected.
- Optional exam mode hides answers until submission.
- Previous/next navigation, full question palette, marks for review, clear selection, unanswered warning, confirmation before submission.
- Keyboard: arrows navigate, number keys select options when focus is outside form controls; standard Tab and Space work on controls.
- Exact-match scoring: 1 mark per question, no partial credit. Practice and exam both score the saved final answer set. Practice scores reflect feedback-assisted learning.
- Results, answer review, weekly breakdown, retry incorrect, weak-question revision, attempt history, best weekly scores, streak.
- localStorage persistence, resume after refresh through the home page, reset confirmation, JSON progress export.
- Original diagram lightboxes and zoom. Shared taxi-world context stays with Week 11 Q3–Q6, even in shuffled or retry quizzes.
- Responsive layout, light/dark appearance, labelled controls, native focus-trapped dialogs, reduced-motion support.

## Accuracy and restoration

112 answer keys were checked against visible **accepted-answer labels**, not the screenshot's selected radio/checkbox values. Week 3 Q4 is cut off in the PDF. At the user's request, it is independently solved as **B: (i), (iv)**. A, B and C are original; the fourth distractor is reconstructed and explicitly labelled. The derivation is included in the app and checked numerically by the tests. It is not represented as a recovered official key.

Source wording and accepted keys are preserved, including course-specific ambiguities. Explanations are absent where the PDF supplied none. Only the restored question has an independently authored explanation, clearly labelled. Topic names are app navigation labels, not original assignment titles.

See [the extraction audit](public/extraction-audit.md) and [machine-readable validation](public/data/audit.json).

## Validation

```sh
npm test
npm run validate:data
npm run build
```

The Python validator uses only the standard library. Unit tests cover the full bank, exact-match scoring, option toggling, persistence, revision, shuffling, all KaTeX expressions, and the restored gradient derivation. See `VALIDATION.md` for browser checks.

## Repeatable PDF processing

The original input remains at the user's chosen location; it is not required at runtime. To repeat extraction, install Python packages `pymupdf`, `pillow`, and `numpy`, plus the Tesseract executable. Native embedded screenshots are extracted losslessly. Coordinate inventory and reviewed transcriptions are committed in `scripts/`.

```sh
python3 scripts/extract.py /absolute/path/Assignments.pdf --work /absolute/path/to/project-work
python3 scripts/finalize.py
python3 scripts/validate_bank.py
```

`finalize.py` expects the batch extraction directory to be the task workspace's `work/` folder. You can set `NPTEL_EXTRACTION_WORK` to use another location. Raw OCR (`questions-ocr.json`) is an intermediate; the application reads only reviewed `questions.json`. Never promote raw OCR to the final bank without reviewing it.

## Data and privacy

There is no application backend, login system, analytics, paid API, or remote image dependency. Progress stays in this browser on this origin. Switching between localhost and the hosted site creates separate progress stores. The optional private hosting platform may enforce access before serving the static files. Export progress before clearing browser storage. Export is a backup file; importing is not implemented.

Source layout: `src/engine.ts` (scoring/state), `src/main.tsx` (React views), `src/style.css`, `public/data/questions.json`, `public/assets/`, `scripts/`, `tests/`.
