# Scholarly Syntactic Transforms & Academic Anti-Slop Reference (EN & AR)

Synthesized from `rudra496/StealthHumanizer` (`academic-inversion.ts` & `humanize-transforms.ts`), `DadaNanjesha/AI-Text-Humanizer-App`, and `ZAYUVALYA/AI-Text-Humanizer`.

---

## 1. Why Academic AI Prose Gets Flagged (And Why Naive Fixes Fail)

1. **The Stock-Transition Trap:** Early rule-based tools prepended `Moreover,`, `Furthermore,`, and `Consequently,` at random. Modern detectors treat dense sentence-initial `Furthermore/Moreover` as a *primary AI marker*. Use **lexical/demonstrative cohesion** instead (`These findings...`, `Under that assumption...`, `Contrastingly...` -> `By contrast,`).
2. **Nominalization Chains:** LLMs stack abstract nouns (`"The utilization of transformer-based architectures for the facilitation of..."`). Unpack at least one noun per chain into an active verb or gerund.
3. **Uniform 18–22 Word Sentences:** Academic LLMs rarely write a 7-word empirical pointer (`Figure 3 illustrates this threshold.`) or a 32-word conditional synthesis. Deliberately alternate short empirical pointers with multi-clause analytical sentences.

---

## 2. Position-Aware Denominalization Rules (English)

Never perform blind regex swaps that produce ungrammatical `"implementing of X"`. Match sentence position:

| AI Nominalized Span | Sentence-Initial Fix | Mid-Sentence (After Preposition/Verb) Fix |
|---|---|---|
| `The implementation of X` | `Implementing X ...` | `... from implementing X` (drop `the` & `of`) |
| `The utilization of X` | `Using X ...` | `... by using X` |
| `The integration of X into Y` | `Integrating X into Y ...` | `... through integrating X into Y` |
| `conduct an investigation into` | `Investigate ...` | `... to investigate ...` |
| `perform an evaluation of` | `Evaluate ...` | `... evaluated ...` |
| `proven to be particularly beneficial in the realm of` | — | `proven useful in` |
| `facilitated unprecedented advancements in` | — | `enabled major advances in` |

---

## 3. الصياغة الأكاديمية العربية الرصينة مقابل ركاكة الـ AI

في الأوراق البحثية والرسائل الجامعية والتقارير الرسمية بالعربية:

| صياغة الـ AI الركيكة في الأبحاث | الصياغة الأكاديمية العربية الأصيلة |
|---|---|
| «تهدف هذه الدراسة إلى القيام بفحص شامل لـ...» | «تبحث هذه الدراسة في أثر...» / «تستقصي الدراسة...» |
| «تم إجراء التجربة على عينة مكونة من 120 مشاركاً» | «أُجريت التجربة على عينة قوامها 120 مشاركاً» |
| «علاوة على ذلك، أظهرت النتائج بشكل واضح أن...» | «وأظهرت النتائج بوضوح أن...» / «وتبيّن من التحليل أن...» |
| «يلعب المتغير المستقل دوراً محورياً في عملية تحسين...» | «يؤثر المتغير المستقل تأثيراً دالاً إحصائياً في تحسين...» |
| «وعلى الرغم من هذه الإيجابيات، تواجه الطريقة تحديات...» | «بيد أن هذه المقاربة تصطدم بمحدوديتين رئيستين:...» |
| «وفي الختام، توصي الدراسة بضرورة تسليط الضوء على...» | «وتخلص الدراسة إلى التوصية بـ...» |

### أدوات الربط الأكاديمي العربي الطبيعي (بدل حشو علاوة على ذلك / بالإضافة إلى ذلك)
- **للاستدراك والتقييد:** `غير أن`، `بيد أن`، `إلا أن هذا التفسير لا يستقيم حين...`، `ومع وجاهة هذا الطرح، فإنه يغفل...`
- **للسببية والتعليل:** `ويُعزى ذلك إلى...`، `ومردّ هذا التباين أن...`، `إذ تشير البيانات إلى...`
- **للبناء والتفريع:** `ويتفرع عن هذه النتيجة...`، `وتتسق هذه المعطيات مع ما توصل إليه (فلان، 2023)...`
