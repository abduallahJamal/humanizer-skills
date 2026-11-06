---
name: ai-writing-detector
description: "Audit and score English or Arabic text for AI-writing patterns without rewriting it. Runs a 12-metric stylometric analysis plus a 9-signal forensic rubric with quoted evidence and sentence-level heatmap. Use when asked if text sounds like AI, why it gets flagged, or to audit drafts in detect-only mode (فحص وكشف بصمات الذكاء الاصطناعي في النصوص العربية والإنجليزية بدون تعديل النص)."
license: MIT
metadata:
  version: "1.0.0"
  languages: "en, ar"
---

# AI Writing Detector — Forensic Audit & Stylometric Scorer (EN & AR)

Analyze text for statistical and rhetorical signs of AI generation **without rewriting or altering the source text**. Every flagged signal must cite exact quotes or measured counts.

## Detect-Only Contract

1. **Never rewrite the text** unless the user explicitly asks for a rewrite after seeing the report (in which case hand off to `humanize-text` or `academic-humanizer`).
2. **Signals, not courtroom proof.** Commercial and open-source AI detectors exhibit high false-positive rates on non-native writers, deadline-pressed authors, and rigid technical templates. Present findings as **stylistic & statistical signals** that explain *why* readers or detectors flag a passage — never as an accusation of misconduct.
3. **Separate real tells from judgment calls.** Distinguish **Strong Markers** (chat residue, Tier-1A clusters, negative parallelisms, uniform 15-word pulse, Arabic `تم + مصدر` / `لا يقتصر على` calques) from **Context-Dependent Judgment Calls** (legitimate technical terms like `robust` in statistics, numbered API steps, or house-style em dashes).

## Workflow

### Step 1: Run Deterministic 12-Metric Stylometric Scan
Whenever `python3` is available, run the bundled local analyzer first so your numbers (word counts, sentence lengths, burstiness CV, bigram diversity, punctuation counts, and flagged sentences) are exact rather than estimated:

```bash
python3 <skill-dir>/scripts/detect_ai_metrics.py --file input.txt --format markdown
```
*(Or pipe stdin: `cat input.txt | python3 <skill-dir>/scripts/detect_ai_metrics.py`)*

### Step 2: Score the 9 Forensic Signals (0–27 Rubric)
Read `references/scoring-rubric.md` and score each of the 9 categories from `0` (human-consistent) to `3` (strong AI pattern):
- **Signal A:** Lexical Predictability & Tier-1 AI Vocabulary (EN & AR)
- **Signal B:** Burstiness Deficit & Metronomic Sentence Lengths
- **Signal C:** Institutional Hedge Density
- **Signal D:** Imposed Document Architecture & Forced Triads
- **Signal E:** Specificity & Concrete-Anchor Deficit
- **Signal F:** Mechanical Transition & Announcement Fingerprint (`Furthermore`, `Turns out`, `علاوة على ذلك`, `تجدر الإشارة`)
- **Signal G:** Punctuation & Typography Fingerprint (Em dashes, semicolons, bold-colon lists)
- **Signal H:** Register Collapse & Translation Calques (e.g. Arabic `تم + مصدر`, `يقوم بـ`, `بشكل + صفة`, synonym cycling)
- **Signal I:** RLHF "Helpful Assistant" & Rhetorical Scaffolding (`Not X, but Y`, mini-aphorism closers, both-sides diplomacy, chat leftovers)

**Double-counting rule:** A single phrase may fire at most **two** distinct categories when genuinely diagnostic for both, and never counts twice inside the same category.

### Step 3: Deliver the Structured Forensic Report

Format your response in the user's preferred language (Arabic if they asked in Arabic, English otherwise) with four concise sections:

1. **Overall Signal Summary:**
   - Forensic Score: `X / 27` (`0–5` Low / Human-consistent, `6–11` Mild / Mixed, `12–18` Moderate-High AI Footprint, `19–27` Heavy Unedited LLM Output)
   - Local Stylometric Human Score from `detect_ai_metrics.py` (`0–100%`) + sentence length sequence.
2. **Signal Breakdown Table (A–I):** Score (`0–3`) + exact quoted evidence from the text (or `Clean` if `0`).
3. **Top Flagged Sentences (Heatmap):** The 3–5 highest-risk sentences and the exact fix principle for each (without rewriting the whole piece).
4. **Protected / Intentional Exceptions:** Note any matches that are actually fine in context (e.g., domain terms, legal/academic conventions) so the writer does not over-edit good prose.
