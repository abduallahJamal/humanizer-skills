---
name: academic-humanizer
description: "Humanize formal, research, scientific, legal, and academic text in English or Modern Standard Arabic without introducing casual slang, contractions, or broken citations. Preserves citations, p-values, equations, and domain terms while disrupting AI rhythm and nominalization bloat (أنسنة الأبحاث العلمية والرسائل الأكاديمية والتقارير الرسمية بالعربية والإنجليزية)."
license: MIT
metadata:
  version: "1.0.0"
  languages: "en, ar"
---

# Academic & Formal Humanizer (EN & MSA Arabic)

General humanizers inject contractions (`don't`, `it's`), fragments (`Like this.`), and conversational asides (`Honestly,`) that break scholarly register. Conversely, naive rule-based academic rewriters prepend `"Moreover,"` and `"Furthermore,"` everywhere, which *increases* AI detection scores.

This skill humanizes **research papers, literature reviews, theses, grant proposals, executive reports, and formal Arabic/English prose** while keeping full scholarly rigor and 100% citation/statistic integrity.

## Mandatory Integrity Locks

1. **Zero Citation or Number Drift:** Every inline citation (`[1]`, `[12–15]`, `(Smith et al., 2025)`, `(العلي، 2024)`), DOI, equation (`$...$`, `$$...$$`), sample size (`N = 312`), confidence interval, and p-value (`p < 0.001`) must survive verbatim.
2. **Formal Register Guard:**
   - **English:** Expand all contractions (`cannot`, `do not`, `does not`, `is not`). No colloquialisms (`stuff`, `kind of`, `turns out`), no standalone dramatic fragments, and no first-person `I think` unless the paper's discipline explicitly uses first-person plural (`we observe`).
   - **Arabic (الفصحى الأكاديمية الرصينة):** No colloquialisms, no journalistic clickbait, and no translationese (`تم إجراء` / `يقوم بدراسة`). Use authentic scholarly Arabic verbs (`أظهرت النتائج`، `فحصت الدراسة`، `يُستدل من ذلك`، `تتفق هذه النتيجة مع`).
3. **Domain Terminology Shield:** Never swap established technical, medical, legal, or statistical terms for thesaurus synonyms (`homoscedasticity`, `gradient descent`, `الشريعة`, `الزكاة`, `الانحدار اللوجستي` stay exact).

Read `references/academic-transforms.md` for position-aware syntactic inversions, denominalization rules, and scholarly Arabic transformations.

## The 4-Step Scholarly Workflow

### Step 1: Deterministic Pre-Processing (`academic_prep.py`)
When `python3` is available, run `prep` mode to expand contractions, strip copy-paste citation artifacts (`oaicite`, zero-width spaces), and inventory all citations and numbers that must survive:
```bash
python3 <skill-dir>/scripts/academic_prep.py prep --input draft.txt --output prepped.txt
```

### Step 2: Strip Academic AI Tells (Without Adding Stock Transitions!)
- **Ban stock transition spam:** Do **not** prepend `Moreover,`, `Furthermore,`, `Additionally,`, `علاوة على ذلك،`, or `بالإضافة إلى ذلك،` to paragraphs. Connect sentences through **referential cohesion** (`This discrepancy...`, `Such constraints...`, `ويعزى هذا التباين إلى...`, `غير أن هذا الافتراض يصطدم بـ...`).
- **Cut empty significance inflation:** Replace `"plays a pivotal role in the evolving landscape of X"` with the exact mechanism or empirical scope (`"governs latency in distributed consensus"`).
- **Cut hollow literature-review boilerplate:** Replace `"Numerous studies have extensively investigated X"` with direct synthesis of what the cited works actually found (`"Prior work links X to Y [3, 7], yet leaves Z untested"`).

### Step 3: Syntactic Inversion & Denominalization (Natural Scholarly Burstiness)
Instead of casual fragments, create sentence-length variance (`8–34` words) using authentic academic syntax:
1. **Position-aware denominalization:** Turn noun-heavy padding (`"benefit from the implementation of quantization"` / `"تحقيق الاستفادة من عملية تطبيق التكميم"`) into crisp verbal/gerund clauses (`"benefit from quantizing weights"` / `"الاستفادة من تكميم الأوزان"`). Never leave dangling `"implementing of"`.
2. **Clause-order inversion:** Alternate subject-first declaratives (`We evaluated three architectures across four benchmarks.`), subordinate-first framing (`When packet loss exceeds 2%, throughput collapses under Cubic.`), and concise empirical anchors (`Table 2 summarizes the ablation.`).
3. **Balanced active/passive voice:** Use active voice for your methodology/claims (`We normalize token counts...` / `حلّلنا العينة...`) and natural passive only where the process or specimen is the true topic (`Samples were annealed at 400 °C` / `عُولجت العينات عند درجة...`).

### Step 4: Citation, Digit & Diff Verification
Verify that zero citations, numbers, or fixed terms were lost, and optionally generate a word-level change diff:
```bash
python3 <skill-dir>/scripts/academic_prep.py verify --original draft.txt --rewritten final.txt --diff diff.md
```
If `verify` exits non-zero, restore every missing citation or number before returning the text.
