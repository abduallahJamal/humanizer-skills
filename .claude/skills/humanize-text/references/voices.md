# Writing Voice Profiles (EN & AR Calibration)

Pass 1 and Pass 2 strip AI vocabulary and robotic structures regardless of voice. Pass 3 uses one of the five profiles below to give the prose a recognizable human pulse.

## Priority Order for Choosing a Voice

1. **User provided writing samples?** Always use **`mirror`** (silent style distillation).
2. **User named a tone or audience?** Pick the matching preset below.
3. **Reference, documentation, or factual encyclopedia text?** Stay **neutral-plain** (clean facts, zero decoration, no forced personality).
4. **General draft and user wants fast results without extra questions?** Default to **`clear-thinker`**.

---

## 1. `clear-thinker` (Default — الفكر الواضح المباشر)
*Inspired by essayists like Paul Graham (EN) and crisp analytical columnists (AR). Feels like a sharp mind working through a real problem without trying to sound smart.*

- **Rhythm:** Short and medium sentences, punctuated by an occasional longer sentence when an argument unfolds. Occasional crisp fragment (`Not even close.` / `وهذا بيت القصيد.`).
- **Openings & Transitions:** Logic carries the transition. Starts sentences naturally with `And`, `But`, `So` (أو `والنتيجة؟`, `لكن`, `ولهذا`) instead of `Furthermore` / `علاوة على ذلك`.
- **Stance:** Direct on facts; honest when uncertain (`I think`, `أظن`, `لست متأكداً إن كان هذا ينطبق على...`).
- **Avoids:** TED-talk drama, corporate buzzwords, neat moralizing endings.

## 2. `casual-storyteller` (السرد العفوي الدافئ)
*Like explaining something over coffee to a smart friend. Warm, concrete, slightly digressive.*

- **Rhythm:** Wide swings — 4-word reactions followed by a 28-word observational sentence. Contractions in English (`don't`, `it's`, `you'll`); smooth, lively Modern Standard or requested local register in Arabic without stiff classical filler.
- **Texture:** Concrete sensory or situational anchors, natural parenthetical asides, candid admission of mistakes or surprises.
- **Avoids:** Topic sentences, numbered-essay scaffolding, stiff connectors.

## 3. `sharp-opinionated` (الحاسم صاحب الرأي)
*Experienced practitioner who skips diplomacy and backs strong claims with specifics.*

- **Rhythm:** Punchy, high-impact declaratives. Short paragraphs. Zero throat-clearing.
- **Stance:** Picks a clear side instead of RLHF "both sides have merit" hedging. Names exact trade-offs and failure modes.
- **Avoids:** `It could be argued`, `ربما يمكن القول`, `لكل خيار إيجابياته وسلبياته`, passive voice hiding responsibility.

## 4. `warm-professional` (المهني الرصين والودود)
*Credible business, client, newsletter, or product writing that sounds like a real colleague, not a press release or committee memo.*

- **Rhythm:** Smooth medium sentences (10–22 words) interspersed with clear 6-word takeaways. No jarring slang, no fragments that feel sloppy.
- **Stance:** Uses `we` / `you` naturally (`وجدنا أن...`, `ستلاحظ أن...`), states requests and deadlines in the first two sentences, respects the reader's time.
- **Avoids:** `synergy`, `stakeholder alignment`, `في إطار سعينا الدؤوب`, `يسرّنا ويشرفنا`, over-bolded bullet lists.

## 5. `mirror` (محاكاة أسلوب الكاتب من عيّناته)
When the user supplies 1+ samples of their own writing, silently extract 6–8 concrete style hypotheses before touching the draft:
1. **Sentence length & variance:** Typical range, fragment frequency.
2. **Lexical register:** Everyday plain words vs domain-dense terminology; Arabic register (فصحى رصينة vs فصحى صحفية خفيفة vs عامية/مزيج).
3. **Paragraph entry:** Scene-first, claim-first, or question-first?
4. **Punctuation fingerprint:** Do they legitimately use em dashes, ellipses, parentheses, or exclamation marks? Match *their* rate (overrides default dash ban).
5. **Connector habits:** Implicit jumps vs favorite conjunctions.
6. **Signature verbal tics:** Keep natural human habits without caricaturing them.

Apply the profile silently — never output the profile analysis unless asked.
