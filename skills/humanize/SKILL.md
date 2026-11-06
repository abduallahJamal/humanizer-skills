---
name: humanize
description: "Orchestrator router for bilingual (EN & AR) AI-writing humanization and forensic detection. Routes requests automatically to humanize-text, ai-writing-detector, anti-slop-coder, or academic-humanizer based on task and register (موجّه مهارات أنسنة النصوص وكشف بصمات الذكاء الاصطناعي بالعربية والإنجليزية)."
license: MIT
metadata:
  version: "1.0.0"
  languages: "en, ar"
---

# Humanize Router (`/humanize`)

Classify the user's request and delegate immediately to the right specialized skill in this suite so rules never conflict across registers:

## Routing Table

1. **Audit / Score Only ("Does this sound like AI?", "افحص النص بدون تعديل"):**
   - Load **`ai-writing-detector`**.
   - Run `detect_ai_metrics.py` + the 9-signal forensic rubric (`0–27`). Do **not** rewrite the source text unless asked next.

2. **Developer Artifacts (READMEs, technical docs, PRs, git commits, issue replies, code comments):**
   - Load **`anti-slop-coder`**.
   - Enforce terse commit messages, WHY-only comments, zero AI git trailers, and `repo_slop_scan.py` verification while protecting fenced code blocks, CLI flags, and paths.

3. **Academic, Research, Scientific, Legal, or Formal Reports (with citations, equations, or formal MSA Arabic):**
   - Load **`academic-humanizer`**.
   - Expand contractions, forbid casual fragments and stock `Moreover/علاوة على ذلك` spam, apply syntactic inversion, and verify 100% survival of citations, LaTeX math, and numbers via `academic_prep.py`.

4. **General Prose, Essays, Articles, Blogs, LinkedIn, Emails, or Creative Drafts (EN & AR):**
   - Load **`humanize-text`**.
   - Run the 3-pass rewrite + voice profile (`clear-thinker` default or `mirror` when samples exist) and verify against `humanize_gate.py`.

## Multi-Step Requests

If the user asks to **"audit first, then humanize"** (e.g., *"افحص النص وقولي مشاكله وبعدين أنسنه"*):
1. Run **`ai-writing-detector`** first and present a compact diagnostic summary.
2. Route to **`academic-humanizer`** (if scholarly/formal) or **`humanize-text`** (if general prose) and verify the final rewrite with its bundled gate script.
