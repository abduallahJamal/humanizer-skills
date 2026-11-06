# English AI Writing Patterns & Replacement Reference

Synthesized from Wikipedia's *Signs of AI Writing* (`blader/humanizer`), `avoid-ai-writing`, `humanize-writing-skill`, `haidrrrry/humanize-ai-writing`, `harshaneel/humanize`, and `StealthHumanizer`.

---

## 1. Three-Tier Word & Phrase Replacement Table

### Tier 1A — High-Frequency AI Markers (Replace on sight in general prose)
| Flagged AI Word | Plain Human Alternatives | Notes / Exceptions |
|---|---|---|
| delve / delves | dig into, examine, look at | Never use figuratively |
| tapestry | mix, combination, history | Keep only for literal cloth |
| testament | proof, sign, evidence | Cut `stands as a testament to` |
| underscore / underscores | show, point to, stress | Overused standalone verb |
| pivotal | key, major, decisive, turning | Cut `pivotal moment` |
| intricate / intricacies | complex, detailed, tricky | — |
| meticulous / meticulously | careful, thorough, exact | — |
| multifaceted | complex, many-sided | — |
| garner / garnered | earn, get, draw, win | — |
| bolster / bolstered | support, back up, strengthen | — |
| interplay | interaction, link, balance | — |
| realm | field, area, world | Cut `in the realm of` -> `in` |
| landscape (abstract) | field, market, space | Keep for physical geography |
| embark | start, begin | Cut `embark on a journey` |
| spearhead | lead, run, start | — |
| nestled | located, in, near | Brochure cliché (`nestled in the heart of`) |
| vibrant | busy, active, lively | Brochure cliché |
| groundbreaking | new, first, major | Keep only if historically accurate |
| plethora / myriad | many, plenty of, dozens of | `a myriad of` -> `many` |
| beacon / cornerstone | center, foundation, model | — |
| synergy / paradigm | teamwork, model, shift | — |
| unleash / unlock / supercharge | enable, speed up, open | Marketing fluff |

### Tier 1B — Clarity & Verbosity Edits
| Verbose AI Form | Concise Human Form |
|---|---|
| utilize / utilization | use / using |
| leverage (as verb) | use (keep literal financial leverage) |
| facilitate | help, enable, run |
| streamline | simplify, speed up, cut steps |
| due to the fact that | because |
| in order to / for the purpose of | to / for |
| has the ability / capacity to | can |
| with regard to / with respect to | about, on, for |
| prior to / subsequent to | before / after |
| in the event that | if |
| a wide range of / a variety of | many, several |

### Tier 2 — Cluster-Flagged Words (Fine once if earned; rewrite when 2+ appear nearby)
`robust` (keep in formal statistics/systems resilience), `comprehensive`, `holistic`, `seamless`, `crucial`, `vital`, `foster`, `cultivate`, `elevate`, `empower`, `showcase`, `illuminate`, `resonate`, `navigate` (abstract), `enduring`, `cutting-edge`, `state-of-the-art`, `transformative`, `dynamic`, `nuanced`, `valuable`, `notably`.

### Tier 3 — Connective & Boilerplate Density Words (Max 1 formal connector per 200 words)
`Furthermore,`, `Moreover,`, `Additionally,`, `Consequently,`, `Nevertheless,`, `Nonetheless,`, `Subsequently,`, `Hence,`, `Thus,`, `In conclusion,`, `In summary,`, `To summarize,`, `It is important to note that`, `It is worth mentioning that`, `Needless to say,`, `At the end of the day,`, `When it comes to`.

---

## 2. The 26 Structural, Staging & Leftover Patterns

### A. Staging Instead of Stating (Act on one sighting)
1. **Negative Parallelism (`Not X, but Y`):**
   - *Forms:* `Not just X, but Y`; `It's not about X; it's about Y`; split-sentence `The problem isn't speed. It's trust.`; multi-negation countdown `It's not price. It's not features. It's support.`; clipped tail `..., no guessing.`
   - *Fix:* State the positive claim directly. Keep a negation only when correcting an actual misconception (`It was a cache miss, not a timeout`).
2. **One-Line Closers & Dramatic Fragments:**
   - *Forms:* `That is the real win.`, `Let that sink in.`, `Read that again.`, `The message was clear.`, `Full stop.`, or explaining an example right after showing it (`This highlights the importance of...`).
   - *Fix:* Delete the closer or merge real information into the preceding sentence.
3. **Pseudo-Profound Sayings:**
   - *Forms:* `At its core,`, `The real question is,`, `What really matters is,`, `X is the currency of Y`, `Efficiency becomes a trap when...`
   - *Fix:* State the concrete cause and effect.
4. **Staged Run-Ups & Narrated Candor:**
   - *Forms:* `Let's dive in.`, `Let's unpack this.`, `Here's what you need to know.`, `Here's the thing:`, `Honestly?`, `Real talk:`.
   - *Fix:* Cut the drumroll and start with the claim.
5. **Arguing With No One (Strawman Defense):**
   - *Forms:* `I'm not saying X...`, `Don't get me wrong...`, `A tempting approach would be X, but...` when nobody proposed X.
   - *Fix:* Cut the imaginary objection and state what actually works.

### B. Rhythm & Mechanics by Rule
6. **Forced Triads (Rule of Three):** Three adjectives, nouns, or parallel examples in a row (`fast, reliable, and scalable`). Keep three only when there are literally three distinct facts.
7. **Anaphora / Repeated Sentence Openers:** Starting 3+ consecutive sentences with the same pronoun or noun (`The system... The system... The system...`).
8. **Em-Dash Connectors (`—` and ` -- `):** Models use dashes to avoid choosing a logical relationship. Use periods, commas, colons, or parentheses.
9. **Stacked Qualifiers:** `could potentially`, `might arguably`, `in many cases tends to`. Keep one honest modal (`may`) or name the exact condition (`fails when payload > 10MB`).
10. **Predicate Hyphenation:** Keep hyphens before nouns (`a real-time check`), drop them after nouns (`the check runs in real time`), except dictionary permanents (`third-party`, `cross-functional`).
11. **Missing Actors / Reflexive Passive:** Prefer clear actors (`The worker retries failed jobs`) unless the object is genuinely the topic.

### C. Inflation & Borrowed Authority
12. **Inflated Significance & Legacy Sections:** `marks a watershed moment`, `leaves an indelible mark`, or stock closing sections titled `Challenges and Future Outlook`. End on the last concrete fact.
13. **Vague Association:** `associated with`, `in connection with`. Name the exact role if in the source (`founded`, `advised`, `part of`).
14. **Shallow `-ing` Riders:** `..., highlighting its commitment to innovation` / `..., ensuring a seamless experience`. Cut the participial tail.
15. **Brochure / Sales Tone:** `boasts`, `stunning`, `must-visit`, `rich cultural heritage`, `passionate about`.
16. **Weasel Authority:** `Experts say`, `Studies show`, `Industry observers note`. Name the source from the input or cut the attribution.
17. **Copula Avoidance:** Replace `serves as`, `stands as`, `functions as`, `features`, `boasts`, `represents` with `is`, `are`, or `has`.

### D. Formatting, Chat Leftovers & Reader Context
18. **Bold-Colon Lists & Decorative Bold:** Convert `- **Speed:** Speed is fast` into plain prose or unbolded unequal bullets.
19. **Decorative Headings:** Use sentence case (`## How token rotation works`, not `## 🚀 Strategic Token Rotation And Security`).
20. **Curly Quotes & Copy-Paste Artifacts:** Normalize `“ ” ‘ ’` to straight quotes `" '` unless publishing house style requires typographic quotes; strip `oaicite`, `contentReference`, `utm_source=`.
21. **Chatbot Wrappers:** Delete `Certainly!`, `Great question!`, `Here is a draft:`, `Let me know if you want changes!`.
22. **Knowledge-Cutoff & Speculative Filler:** Delete `As of my last update`, `maintains a low profile`, `likely grew up in...`.
23. **Heading Echo:** Delete one-line sentences right under a heading that merely repeat the heading (`## Security` -> `Security is crucial.`).
24. **Document Self-Narration:** Delete `This section is organized by...` or `The table below shows...` when self-evident.
25. **Re-Explaining Shared Context in Replies:** In emails, PRs, and Slack replies, lead with the decision/answer in sentence 1 instead of recapping the thread.
26. **Synonym Cycling ("Elegant Variation"):** Do not call the same subject `the tool`, `the utility`, `the solution`, and `the framework` across four sentences. Repeat the noun or use `it`.

---

## 3. Signal I Rhetorical Scaffolding Audit (Survives Naive Edits)

Check drafts >150 words against these subtle LLM habits:
- **Mini-aphorism paragraph closers:** 4–10 word "mic-drop" lessons at the end of paragraphs (`Slide decks don't.`, `That's the real work.`). Cut or fold in.
- **Thesis-first personal openers:** `The hardest part of distributed systems is...` -> Start with the actual incident or fact.
- **"Turns out" / "What surprised me was" pivots:** Fake discovery narratives (`Turns out the timeout was 5s` -> `The timeout was 5s`).
- **Symmetric mirror sentences:** `Juniors optimize code. Seniors optimize teams.` -> Break the grammatical symmetry.
- **Chiasmus:** `failing to plan / planning to fail` style reversals. Make comparisons plain and asymmetric.
- **RLHF "both-sides" diplomacy:** `While X has merits, Y also offers benefits, and the choice depends on your needs.` -> State the actual boundary condition where X beats Y.
