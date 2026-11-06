# Forensic 9-Signal Scoring Rubric (EN & AR)

Synthesized from `harshaneel/humanize` (`ai-check`), `conorbronsdon/avoid-ai-writing`, and `rudra496/StealthHumanizer`.

## Severity-to-Score Mapping (Apply to Each Signal A–I)

| Evidence Found in Text | Score |
|---|---|
| Zero flagged instances | **0** (Human-consistent) |
| 1 weak/context-dependent instance | **1** (Weak signal / Judgment call) |
| 1 moderate instance OR 2–3 weak instances | **2** (Moderate AI pattern) |
| 1 unmistakable tell OR 2+ moderate instances OR 4+ weak instances | **3** (Strong AI pattern) |

**Total Cap:** `9 × 3 = 27`.
- **0–5:** Human-consistent (natural variance, grounded specifics, minimal scaffolding).
- **6–11:** Light AI polish or rigid corporate/academic human prose.
- **12–18:** Probable AI-assisted draft or heavily templated output.
- **19–27:** Strong unedited LLM fingerprint across vocabulary, rhythm, and RLHF framing.

---

## The 9 Signals (English & Arabic Criteria)

### Signal A — Lexical Predictability & Banned Vocabulary
- **English flags:** `delve`, `tapestry`, `pivotal`, `underscore`, `testament`, `intricate`, `meticulous`, `multifaceted`, `garner`, `bolster`, `realm`, `landscape` (abstract), `leverage` (verb), `utilize`, `streamline`, `seamless`, `robust` (figurative), `plethora`, `myriad`.
- **Arabic flags:** «في ظل التطورات المتسارعة»، «يلعب دوراً محورياً/جوهرياً»، «حجر الزاوية»، «نسيج متكامل / فسيفساء»، «المشهد الرقمي»، «التعمق في / الغوص في أعماق»، «إطلاق العنان»، «تسخير إمكانات»، «خارطة طريق شاملة».

### Signal B — Burstiness Deficit (Sentence Uniformity)
- **Flags:**
  - 3+ consecutive sentences within 4 words of the same length (e.g., `15, 16, 14, 17`).
  - Over 55% of sentences clustered in the `10–20` word band (EN) or `9–17` word band (AR).
  - No short punchy sentence (`≤ 6` words) in a 150+ word passage.
  - Standard deviation of sentence length `< 5.0` words on texts ≥ 100 words.

### Signal C — Institutional Hedge Density
- **English flags:** `it is important to note`, `it is worth mentioning`, `it can be argued`, `in many cases`, `generally speaking`, `results may vary`, stacked modals (`could potentially`).
- **Arabic flags:** «من المهم أن نلاحظ»، «تجدر الإشارة إلى أن»، «من الجدير بالذكر»، «يمكن القول إلى حد ما»، «في كثير من الأحيان قد يؤدي».

### Signal D — Imposed Structural Symmetry & Triads
- **Flags:**
  - Forced tricolons (`X, Y, and Z` adjectives/clauses; «الكفاءة والفعالية والابتكار»).
  - Every paragraph following micro `Topic -> Explanation -> Mini-lesson closer`.
  - Bullet lists with `**Bold Header:** explanation` where flowing prose belongs.
  - Formula closing sections (`Challenges and Future Outlook` / «التحديات والآفاق المستقبلية»).

### Signal E — Specificity & Concrete-Anchor Deficit
- **Flags:**
  - Sweeping claims with zero dates, numbers, named tools, places, or real examples (`Many organizations have seen significant gains` / «حققت العديد من المؤسسات نتائج ملموسة»).
  - Weasel authority (`Experts argue`, `Studies show`, «يرى الخبراء»، «تشير الدراسات» بدون مصدر).

### Signal F — Mechanical Transition & Announcement Fingerprint
- **English flags:** Paragraph-initial `Furthermore,`, `Moreover,`, `Additionally,`; fake discovery `Turns out...`; announcement colons `The key insight:` / `Here's the thing:`.
- **Arabic flags:** تكدس «علاوة على ذلك»، «فضلاً عن ذلك»، «بالإضافة إلى ذلك»، «ومن ناحية أخرى»، «وفي السياق ذاته» في مطالع الفقرات.

### Signal G — Punctuation & Typography Fingerprint
- **Flags:**
  - Em dashes (`—` or ` -- `) > 1 per 300 words in English, or **any** prose em-dash wrapping in Arabic.
  - Semicolons (`;`) linking ordinary clauses in casual/general writing.
  - Decorative emojis in headings (`## 🚀 Key Takeaways`), Title Case on every heading, or heading-echo first sentences.

### Signal H — Register Collapse, Synonym Cycling & Translation Calques
- **English flags:** Synonym cycling for the same noun (`the platform / the solution / the ecosystem`), copula avoidance (`serves as`, `boasts`, `features` instead of `is` / `has`), Slack updates written like press releases.
- **Arabic flags:** الركاكة المترجمة عن الإنجليزية: تكرار «تم + المصدر» للمجهول، «يقوم بـ + المصدر» بدل الفعل المباشر، «بشكل + صفة» في كل سطر، «من خلال» المفرطة.

### Signal I — RLHF "Helpful Assistant" & Rhetorical Scaffolding
- **Unmistakable (Score 3 immediately):** Chatbot wrappers (`Certainly!`, `Great question!`, `I hope this helps`, `بالتأكيد!`, `آمل أن يكون هذا مفيداً`), cutoff disclaimers (`As of my last update`), or citation leak tokens (`oaicite`, `contentReference`).
- **Rhetorical scaffolding:** Negative parallelisms (`Not X, but Y` / `It's not about X, it's about Y` / «لا يقتصر الأمر على X بل يتعداه إلى Y» / «ليس مجرد X بل هو Y»), mini-aphorism paragraph closers (`That is the real win.`), symmetric mirror sentences, and compulsive "both-sides" neutrality.

---

## Fairness & Exception Guardrails

Do **not** penalize:
1. Required domain terms (`robust` in robust regression, `landscape` in geography/GIS, `leverage` in corporate finance).
2. Numbered steps in actual installation guides, runbooks, or recipes.
3. Formal connectors or passive voice in genuine peer-reviewed methods sections where house style mandates objectivity (note as genre convention, not AI proof).
4. Quoted material, code blocks, legal statutes, or sacred texts.
