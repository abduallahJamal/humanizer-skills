---
description: Route any English or Arabic text, codebase doc, or research draft to the right Humanizer skill — 3-pass prose rewrite, 12-metric forensic AI detection, developer anti-slop hygiene, or citation-locked academic humanization.
---

Load and follow the `humanize` router skill immediately to handle the user's request with the exact specialist skill:

1. **Detect-only audit (`ai-writing-detector`):** When asked whether text sounds AI-generated or why detectors flag it — run `detect_ai_metrics.py` + the 9-signal rubric (`0–27`) without altering the text.
2. **Developer & repo artifacts (`anti-slop-coder`):** When writing or cleaning `README.md`, technical docs, PRs, commit messages, thread replies, or code comments — enforce WHY-only comments, no AI git trailers, and run `repo_slop_scan.py`.
3. **Scholarly & formal prose (`academic-humanizer`):** When editing research papers, theses, legal memos, or formal reports — lock citations, equations, and numbers via `academic_prep.py` without introducing contractions or stock `Moreover` transitions.
4. **General prose (`humanize-text`):** When rewriting blogs, essays, posts, emails, or Arabic/English articles — run the 3-pass humanizer + voice profile and verify with `humanize_gate.py`.

User request:
$ARGUMENTS
