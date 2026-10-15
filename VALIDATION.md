# Functional validation

Validated 15 October 2026 using local production and development builds.

- `npm test`: 8 tests passed, including all 113 answer sets, multi-select omissions/extras, single-select replacement, multi-select toggling, perfect full-quiz score 113/113, storage recovery/round-trip, revision, shuffle identity, all KaTeX expressions, and a numerical check of the Week 3 Q4 gradients.
- `python3 scripts/validate_bank.py`: passed all 12 inventories, 113 unique IDs and sequential question numbers, option/answer membership, key provenance, balanced math delimiters and 649 local image references.
- `npm run build`: TypeScript and Vite production build passed. Production files include an offline precache service worker.
- Playwright/Chromium browser checks passed: weekly start, immediate incorrect/correct feedback, radio/checkbox controls, multi-select incomplete/complete feedback, previous/next, answer restoration on navigation, refresh and resume, unanswered submit confirmation, results and answer review, full 113-question palette and final question, original diagram lightbox and zoom, exam answer hiding and Week 3 Q4 native math rendering. No browser JavaScript errors were recorded.
- Desktop inspected at 1440 px wide. Mobile inspected at 390 × 844. Tablet checked at 820 × 1180. No horizontal page overflow was found.
- A fresh mobile session was visually inspected after responsive transitions settled. The sidebar stays off-screen until opened, and real extracted question text/options are readable and selectable.

Scoring is exact match with no partial credit, using saved final selections. Practice mode intentionally reveals feedback during the session. Its scores are feedback-assisted practice scores, not blind exam measurements. Exam mode keeps answers hidden until submission.

The only unrecoverable source fragment is the final distractor and official feedback of Week 3 Q4. That restoration is clearly labelled; its independently derived answer is B. This source limitation is not concealed by the validation results.
- Production offline check passed after repairing cache matching for server Vary headers: after service-worker activation, an offline browser reload loaded the home page, the complete 113-question challenge, and the original Week 12 Q5 diagram.
