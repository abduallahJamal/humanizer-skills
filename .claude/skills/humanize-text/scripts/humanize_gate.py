#!/usr/bin/env python3
"""
humanize_gate.py — Deterministic Post-Rewrite Verification Gate (EN & AR)

Synthesizes verification gates from:
- harshaneel/humanize (em-dash/semicolon limits, burstiness spread & mid-band cap)
- rudra496/StealthHumanizer (sentenceLooksBroken grammar check & digitsPreserved fact lock)
- haidrrrry/humanize-ai-writing (copy-paste & chat residue scan)
- ZAYUVALYA/AI-Text-Humanizer (protected fixed-terms shield)

Zero external dependencies (Python 3.9+ stdlib only).
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

ARABIC_RE = re.compile(r"[\u0600-\u06FF]")
ARABIC_INDIC_MAP = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

EN_BANNED_PATTERNS: list[tuple[str, str]] = [
    (r"\bdelv(?:e|es|ed|ing)\b", "delve -> dig into / examine"),
    (r"\btapestr(?:y|ies)\b", "tapestry -> mix / combination"),
    (r"\bleverag(?:e|es|ed|ing)\b", "leverage -> use"),
    (r"\butiliz(?:e|es|ed|ing|ation)\b", "utilize -> use"),
    (r"\bmultifaceted\b", "multifaceted -> complex / many-sided"),
    (r"\bmeticulous(?:ly)?\b", "meticulous -> careful / thorough"),
    (r"\bparamount\b", "paramount -> critical / top"),
    (r"\bpivotal\b", "pivotal -> key / major"),
    (r"\bunderscor(?:e|es|ed|ing)\b", "underscore -> show / stress"),
    (r"\btestament\s+to\b", "testament to -> proof of / sign of"),
    (r"\bplethora\s+of\b", "plethora of -> many"),
    (r"\bmyriad\s+of\b", "myriad of -> many"),
    (r"\bin\s+the\s+realm\s+of\b", "in the realm of -> in"),
    (r"\bnestled\s+in\b", "nestled in -> in / located in"),
    (r"\bembark(?:s|ed|ing)?\s+on\b", "embark on -> start / begin"),
    (r"\bspearhead(?:s|ed|ing)?\b", "spearhead -> lead"),
    (r"\bgame-chang(?:er|ing)\b", "game-changer -> major shift (or state impact)"),
    (r"\bin\s+today'?s\s+(?:fast-paced\s+)?world\b", "cut canned opener"),
    (r"\bit\s+is\s+(?:important|worth)\s+to\s+note\b", "cut hedge opener"),
    (r"\bit(?:'s|\s+is)\s+worth\s+(?:noting|mentioning)\b", "cut hedge opener"),
    (r"\bneedless\s+to\s+say\b", "cut filler phrase"),
    (r"\bin\s+conclusion\b", "cut summary closer"),
    (r"\bserves\s+as\s+a\b", "serves as a -> is a"),
    (r"\bstands\s+as\s+a\b", "stands as a -> is a"),
    (r"\bplays\s+a\s+(?:crucial|pivotal|vital)\s+role\b", "plays a pivotal role -> state exact effect"),
]

EN_NEGATION_PIVOTS: list[str] = [
    r"\bnot\s+(?:just|merely|simply)\s+[^.?!]{2,60},\s*but\b",
    r"\bit(?:'s|\s+is)\s+not\s+(?:just\s+)?about\s+[^.?!]{2,50}[,;—-]\s*it(?:'s|\s+is)\s+about\b",
    r"\blet\s+that\s+sink\s+in\b",
    r"\bread\s+that\s+again\b",
    r"\blet(?:'s|\s+us)\s+(?:dive\s+in|unpack\s+this|break\s+this\s+down)\b",
]

AR_BANNED_PATTERNS: list[tuple[str, str]] = [
    (r"في\s+ظل\s+التطورات\s+المتسارعة", "مقدمة آلية معلّبة — ادخل في الموضوع مباشرة"),
    (r"مما\s+لا\s+شك\s+فيه", "مقدمة إنشائية مستهلكة — اذكر الحقيقة مباشرة"),
    (r"منذ\s+فجر\s+التاريخ", "مبالغة إنشائية — احذفها"),
    (r"علاوة\s+على\s+ذلك", "رابط آلي متكرر — اربط بالواو/الفاء أو بالمعنى"),
    (r"تجدر\s+الإشارة\s+إلى\s+أن", "حشو تمهيدي — اذكر المعلومة مباشرة"),
    (r"من\s+الجدير\s+بالذكر", "حشو تمهيدي — اذكر المعلومة مباشرة"),
    (r"من\s+المهم\s+أن\s+نلاحظ", "ترجمة حرفية لـ it is important to note"),
    (r"يلعب\s+دوراً\s+(?:محورياً|حيوياً|جوهرياً|بارزاً)", "كليشيه مترجم — اذكر الأثر الفعلي"),
    (r"تلعب\s+دوراً\s+(?:محورياً|حيوياً|جوهرياً|بارزاً)", "كليشيه مترجم — اذكر الأثر الفعلي"),
    (r"حجر\s+الزاوية", "كليشيه مستهلك — استبدله بوصف دقيق"),
    (r"يُعد\s+بمثابة|تُعد\s+بمثابة|يعد\s+بمثابة|تعد\s+بمثابة", "حشو — استخدم جملة اسمية مباشرة (هو/هي)"),
    (r"لا\s+يقتصر\s+(?:الأمر\s+)?على\s+[^.؟!]{2,60}بل\s+(?:يتعداه|يمتد)", "توازي سلبي مترجم (Not X but Y)"),
    (r"ليس\s+مجرد\s+[^.؟!]{2,50}[،,]\s*بل\s+هو", "توازي سلبي مترجم (Not merely X, it's Y)"),
    (r"إطلاق\s+العنان", "ترجمة حرفية لـ unleash"),
    (r"تسخير\s+إمكانات", "ترجمة حرفية لـ harness/leverage"),
    (r"المشهد\s+(?:الرقمي|التكنولوجي|المتغير)", "ترجمة حرفية لـ digital/evolving landscape"),
    (r"وفي\s+الختام[،,]?\s+يمكن(?:نا)?\s+القول", "خاتمة آلية معلّبة — توقف عند آخر فكرة"),
    (r"في\s+نهاية\s+المطاف", "ترجمة حرفية لـ at the end of the day"),
]

RESIDUE_PATTERNS: list[str] = [
    r"^\s*(?:certainly!|of\s+course!|great\s+question!|sure!|بالتأكيد!|بالطبع!|سؤال\s+رائع!)",
    r"(?:i\s+hope\s+this\s+helps|let\s+me\s+know\s+if\s+you(?:'d|\s+would)\s+like|آمل\s+أن\s+يكون\s+هذا\s+مفيداً)",
    r"(?:oaicite|contentReference|oai_citation|turn\d+search\d+|grok_card)",
    r"utm_source=",
]

DEFAULT_FIXED_TERMS: list[str] = [
    "Quran", "Qur'an", "Bible", "Torah", "Gospel", "halal", "haram", "zakat",
    "sharia", "hajj", "umrah", "القرآن", "السنة",
]

LEGITIMATE_EN_DOUBLES = {"had", "that", "very"}


def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks and inline code before prose scanning."""
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"`[^`\n]+`", " ", text)
    return text


def detect_language(text: str) -> str:
    ar_chars = len(ARABIC_RE.findall(text))
    latin_chars = len(re.findall(r"[A-Za-z]", text))
    if ar_chars > 0 and latin_chars > 0:
        if ar_chars / max(ar_chars + latin_chars, 1) >= 0.35:
            return "ar" if ar_chars >= latin_chars else "mixed"
    return "ar" if ar_chars > latin_chars else "en"


def split_sentences(text: str) -> list[str]:
    clean = strip_code_blocks(text)
    lines = [ln.strip() for ln in clean.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    joined = " ".join(lines)
    raw = re.split(r"(?<=[.!?؟])\s+", joined)
    return [s.strip() for s in raw if len(s.strip().split()) >= 2]


def extract_numbers(text: str) -> list[str]:
    clean = strip_code_blocks(text).translate(ARABIC_INDIC_MAP)
    nums = re.findall(r"\d+(?:[.,]\d+)*", clean)
    return sorted(n.replace(",", "").replace("٬", "") for n in nums)


def check_broken_sentences(sentences: list[str]) -> list[str]:
    """StealthHumanizer-inspired grammar defect gate."""
    defects: list[str] = []
    for s in sentences:
        if re.search(r"[A-Za-z]\$\d", s):
            defects.append(f"Regex placeholder artifact in: '{s[:80]}'")
        m_en = re.search(
            r"\b(of|to|in|for|with|by|from|at|on|as|the|a|an|and|or|is|are|was|were)\s+\1\b",
            s,
            re.IGNORECASE,
        )
        if m_en and m_en.group(1).lower() not in LEGITIMATE_EN_DOUBLES:
            defects.append(f"Doubled function word '{m_en.group(0)}' in: '{s[:80]}'")
        m_ar = re.search(r"\b(في|من|على|إلى|عن|مع|أن|إن|هذا|هذه)\s+\1\b", s)
        if m_ar:
            defects.append(f"تكرار لفظي مكسور '{m_ar.group(0)}' في: '{s[:80]}'")
        if re.search(
            r"\b(?:implementing|deploying|using|integrating|adopting|applying|analyzing|evaluating)\s+of\b",
            s,
            re.IGNORECASE,
        ):
            defects.append(f"Broken nominalization ('gerund + of') in: '{s[:80]}'")
        for op, cl in [("(", ")"), ("[", "]")]:
            if s.count(op) != s.count(cl):
                defects.append(f"Unbalanced '{op}{cl}' in: '{s[:80]}'")
    return defects


def evaluate_gate(
    rewritten: str,
    original: str | None = None,
    extra_fixed_terms: list[str] | None = None,
    formal: bool = False,
) -> dict[str, Any]:
    prose = strip_code_blocks(rewritten)
    lang = detect_language(prose)
    words = prose.split()
    word_count = len(words)
    sentences = split_sentences(rewritten)
    sent_lengths = [len(s.split()) for s in sentences]

    issues: list[str] = []
    warnings: list[str] = []

    # 1. Punctuation gate
    em_dashes = prose.count("—") + len(re.findall(r"\s--\s", prose))
    if lang == "ar" and em_dashes > 0:
        issues.append(f"Em dashes in Arabic prose: {em_dashes} found (must be 0; use ، or : or parentheses).")
    elif lang != "ar":
        allowed_dashes = 0 if word_count < 300 else word_count // 300
        if em_dashes > allowed_dashes:
            issues.append(f"Em-dash count ({em_dashes}) exceeds limit ({allowed_dashes} for {word_count} words).")

    semicolons = prose.count(";")
    if not formal and lang == "en" and semicolons > 0:
        issues.append(f"Semicolons found ({semicolons}) in non-formal English prose (target: 0).")

    curly_count = sum(prose.count(ch) for ch in ("“", "”", "‘", "’"))
    if curly_count > 0 and not formal:
        warnings.append(f"Curly quotes/apostrophes found ({curly_count}); normalize to straight quotes unless house style requires them.")

    # 2. Banned vocabulary & clichés (EN + AR)
    banned_hits: list[str] = []
    for pat, hint in EN_BANNED_PATTERNS:
        for m in re.finditer(pat, prose, flags=re.IGNORECASE):
            banned_hits.append(f"EN '{m.group(0)}' ({hint})")
    for pat in EN_NEGATION_PIVOTS:
        for m in re.finditer(pat, prose, flags=re.IGNORECASE):
            banned_hits.append(f"EN structural tell '{m.group(0)}'")
    for pat, hint in AR_BANNED_PATTERNS:
        for m in re.finditer(pat, prose):
            banned_hits.append(f"AR '{m.group(0)}' ({hint})")

    # Check excessive Arabic translation calques (تم + مصدر / بشكل + صفة)
    tamm_count = len(re.findall(r"\bتم\s+[\u0600-\u06FF]{3,}", prose))
    bishakl_count = len(re.findall(r"\bبشكل\s+[\u0600-\u06FF]{3,}", prose))
    if lang in ("ar", "mixed") and sentences:
        if tamm_count >= max(2, len(sentences) // 3):
            issues.append(f"الإفراط في صيغة 'تم + المصدر' ({tamm_count} مرات) — استبدلها بالفعل المبني للمعلوم أو المجهول الصرفي.")
        if bishakl_count >= max(2, len(sentences) // 3):
            warnings.append(f"تكرار 'بشكل + صفة' ({bishakl_count} مرات) — استبدلها بالمفعول المطلق أو الحال.")

    if banned_hits:
        issues.append(f"Banned AI phrases/structures ({len(banned_hits)}): " + "; ".join(banned_hits[:8]))

    # 3. Residue & artifact gate
    for pat in RESIDUE_PATTERNS:
        m = re.search(pat, rewritten, flags=re.IGNORECASE | re.MULTILINE)
        if m:
            issues.append(f"Chat/copy-paste residue detected: '{m.group(0)}'")

    # 4. Burstiness & sentence rhythm gate
    rhythm_stats: dict[str, Any] = {"sentence_count": len(sent_lengths), "sentence_lengths": sent_lengths}
    if len(sent_lengths) >= 4:
        avg_len = sum(sent_lengths) / len(sent_lengths)
        variance = sum((x - avg_len) ** 2 for x in sent_lengths) / len(sent_lengths)
        std_dev = math.sqrt(variance)
        spread = max(sent_lengths) - min(sent_lengths)
        low_band, high_band = (9, 17) if lang == "ar" else (10, 20)
        mid_band_ratio = sum(1 for x in sent_lengths if low_band <= x <= high_band) / len(sent_lengths)

        uniform_run = False
        for i in range(len(sent_lengths) - 2):
            window = sent_lengths[i : i + 3]
            if max(window) - min(window) <= 4:
                uniform_run = True
                break

        rhythm_stats.update(
            {
                "mean_words": round(avg_len, 2),
                "std_dev": round(std_dev, 2),
                "spread": spread,
                "mid_band_ratio": round(mid_band_ratio, 2),
                "has_uniform_3_sentence_run": uniform_run,
            }
        )

        min_spread = 14 if lang == "ar" else 18
        if word_count >= 80 and spread < min_spread:
            issues.append(
                f"Low sentence-length spread ({spread} words; target >= {min_spread}). Add a short punchy sentence (<=6 words) and a longer unfolding clause."
            )
        if word_count >= 80 and mid_band_ratio >= 0.55:
            warnings.append(
                f"{int(mid_band_ratio * 100)}% of sentences sit in the uniform {low_band}-{high_band} word band (target < 50%)."
            )
        if uniform_run and len(sent_lengths) >= 5:
            warnings.append("3+ consecutive sentences have nearly identical length (within 4 words); vary rhythm.")

    # 5. Grammar defect gate
    defects = check_broken_sentences(sentences)
    issues.extend(defects)

    # 6. Fact/number preservation & fixed-terms gate (when original provided)
    fact_check: dict[str, Any] = {}
    if original is not None:
        orig_nums = extract_numbers(original)
        rew_nums = extract_numbers(rewritten)
        missing_nums = [n for n in set(orig_nums) if rew_nums.count(n) < orig_nums.count(n)]
        added_nums = [n for n in set(rew_nums) if rew_nums.count(n) > orig_nums.count(n)]
        fact_check["original_numbers"] = orig_nums
        fact_check["rewritten_numbers"] = rew_nums
        if missing_nums:
            issues.append(f"Numbers/dates dropped from source: {missing_nums}")
        if added_nums:
            issues.append(f"Unverified numbers added (Zero-Invention rule): {added_nums}")

        terms = list(DEFAULT_FIXED_TERMS) + (extra_fixed_terms or [])
        dropped_terms = [
            t for t in terms if t and (t.lower() in original.lower()) and (t.lower() not in rewritten.lower())
        ]
        if dropped_terms:
            issues.append(f"Protected fixed terms altered or dropped: {dropped_terms}")

        orig_wc = max(len(strip_code_blocks(original).split()), 1)
        shrink_ratio = word_count / orig_wc
        fact_check["length_ratio"] = round(shrink_ratio, 2)
        if shrink_ratio < 0.5:
            warnings.append(
                f"Output is {int((1 - shrink_ratio) * 100)}% shorter than input (substantial puffery removed; do not pad back up, append honesty note)."
            )

    passed = len(issues) == 0
    return {
        "status": "PASS" if passed else "NEEDS_FIX",
        "language": lang,
        "word_count": word_count,
        "em_dashes": em_dashes,
        "semicolons": semicolons,
        "rhythm": rhythm_stats,
        "fact_check": fact_check,
        "issues": issues,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify humanized prose against hard quality gates (EN & AR).")
    parser.add_argument("--rewritten", "-r", help="Path to rewritten text file (reads stdin if omitted).")
    parser.add_argument("--original", "-o", help="Optional path to original source file for fact/number integrity check.")
    parser.add_argument("--fixed-terms", help="Comma-separated protected terms that must survive unchanged.")
    parser.add_argument("--formal", action="store_true", help="Allow formal punctuation (e.g. semicolons in academic prose).")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    args = parser.parse_args()

    if args.rewritten:
        rewritten_text = Path(args.rewritten).read_text(encoding="utf-8")
    else:
        rewritten_text = sys.stdin.read()

    original_text = Path(args.original).read_text(encoding="utf-8") if args.original else None
    extra_terms = [t.strip() for t in args.fixed_terms.split(",") if t.strip()] if args.fixed_terms else []

    report = evaluate_gate(
        rewritten=rewritten_text,
        original=original_text,
        extra_fixed_terms=extra_terms,
        formal=args.formal,
    )

    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Gate Status: {report['status']} | Lang: {report['language']} | Words: {report['word_count']}")
        if "sentence_lengths" in report["rhythm"]:
            print(f"Sentence Lengths: {report['rhythm']['sentence_lengths']}")
            if "spread" in report["rhythm"]:
                print(
                    f"Rhythm: spread={report['rhythm']['spread']}, std_dev={report['rhythm']['std_dev']}, "
                    f"mid_band={int(report['rhythm']['mid_band_ratio'] * 100)}%"
                )
        if report["issues"]:
            print("\n[FAILING ISSUES - FIX BEFORE RETURNING]")
            for idx, item in enumerate(report["issues"], 1):
                print(f"  {idx}. {item}")
        if report["warnings"]:
            print("\n[WARNINGS]")
            for idx, item in enumerate(report["warnings"], 1):
                print(f"  {idx}. {item}")

    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
