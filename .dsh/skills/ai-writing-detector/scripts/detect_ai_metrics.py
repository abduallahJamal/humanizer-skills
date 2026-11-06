#!/usr/bin/env python3
"""
detect_ai_metrics.py — 12-Metric On-Device Stylometric AI Writing Detector (EN & AR)

Synthesizes deterministic local metrics from:
- rudra496/StealthHumanizer (12-metric stylometric engine + EN/AR phrase banks + sentence heatmap)
- conorbronsdon/avoid-ai-writing (tiered pattern density & protected code-block skipping)
- harshaneel/humanize (burstiness spread, uniform sentence runs, punctuation & anchor density)

Zero external dependencies (Python 3.9+ stdlib only). Never modifies input files.
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

EN_AI_PHRASES = [
    "it is important to note", "it is worth mentioning", "it is worth noting",
    "in conclusion", "in summary", "to summarize", "furthermore", "moreover",
    "additionally", "plays a crucial role", "plays a pivotal role", "plays a vital role",
    "stands as a testament", "serves as a", "boasts a", "in the realm of",
    "navigating the landscape", "evolving landscape", "a myriad of", "a plethora of",
    "delve into", "delves into", "tapestry of", "multifaceted", "meticulous",
    "seamless", "streamline", "paradigm shift", "holistic", "cutting-edge",
    "groundbreaking", "transformative", "unprecedented", "utilize", "leverage",
    "spearhead", "embark on", "let's dive in", "here's the thing", "let that sink in",
    "not just about", "needless to say", "in today's fast-paced",
]

EN_TRANSITIONS = [
    "furthermore", "moreover", "additionally", "consequently", "nevertheless",
    "nonetheless", "subsequently", "hence", "thus", "accordingly", "conversely",
    "however", "therefore",
]

EN_HEDGES = [
    "it could be argued", "one might consider", "it is possible that",
    "it would seem", "this suggests that", "this may indicate", "could potentially",
    "might arguably", "generally speaking", "in many cases",
]

AR_AI_PHRASES = [
    "في ظل التطورات المتسارعة", "مما لا شك فيه", "من الجدير بالذكر", "تجدر الإشارة إلى",
    "من المهم أن نلاحظ", "علاوة على ذلك", "فضلاً عن ذلك", "بالإضافة إلى ذلك",
    "يلعب دوراً محورياً", "تلعب دوراً محورياً", "يلعب دوراً حيوياً", "حجر الزاوية",
    "يعد بمثابة", "تعد بمثابة", "يُعد بمثابة", "تُعد بمثابة", "لا يقتصر الأمر على",
    "ليس مجرد", "المشهد الرقمي", "المشهد التكنولوجي", "نسيج متكامل", "إطلاق العنان",
    "تسخير إمكانات", "خارطة طريق شاملة", "نهج شمولي", "في الختام", "وخلاصة القول",
    "في نهاية المطاف", "سلاح ذو حدين", "نقلة نوعية",
]

AR_TRANSITIONS = [
    "علاوة على ذلك", "بالإضافة إلى ذلك", "فضلاً عن ذلك", "ومن ناحية أخرى",
    "وفي المقابل", "نتيجة لذلك", "وبناءً على ذلك", "وفي هذا السياق", "وفي هذا الصدد",
    "ومع ذلك", "لذلك", "ختاماً",
]

AR_HEDGES = [
    "من الملاحظ أن", "يمكن القول إن", "إلى حد ما", "في كثير من الأحيان",
    "ربما يمكن", "بصورة عامة", "بشكل عام",
]


def strip_protected(text: str) -> str:
    text = re.sub(r"^---\n[\s\S]*?\n---\n", "", text)
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"`[^`\n]+`", " ", text)
    return text


def detect_lang(text: str) -> str:
    ar = len(ARABIC_RE.findall(text))
    en = len(re.findall(r"[A-Za-z]", text))
    return "ar" if ar > en else "en"


def split_sentences(text: str) -> list[str]:
    lines = [
        ln.strip()
        for ln in text.splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    joined = " ".join(lines)
    parts = re.split(r"(?<=[.!?؟])\s+", joined)
    return [p.strip() for p in parts if len(p.strip().split()) >= 2]


def tokenize_words(text: str) -> list[str]:
    return re.findall(r"[\w\u0600-\u06FF']+", text.lower())


def analyze_text(raw_text: str) -> dict[str, Any]:
    prose = strip_protected(raw_text)
    lang = detect_lang(prose)
    sentences = split_sentences(prose)
    words = tokenize_words(prose)
    word_count = len(words)
    sent_count = max(len(sentences), 1)
    sent_lengths = [len(s.split()) for s in sentences]

    # Metric 1: Bigram Diversity (Perplexity proxy, 0-100 higher = more human)
    if len(words) >= 6:
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]
        bigram_div = len(set(bigrams)) / len(bigrams)
        freq: dict[str, int] = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        uniformity = max(freq.values()) / (len(words) / max(len(freq), 1))
        perplexity_score = min(100.0, max(0.0, bigram_div * 75.0 + max(0.0, 25.0 - uniformity * 2.5)))
    else:
        perplexity_score = 50.0

    # Metric 2: Burstiness CV (0-100 higher = more human)
    if len(sent_lengths) >= 3:
        mean_len = sum(sent_lengths) / len(sent_lengths)
        variance = sum((x - mean_len) ** 2 for x in sent_lengths) / len(sent_lengths)
        std_dev = math.sqrt(variance)
        cv = std_dev / max(mean_len, 1.0)
        burstiness_score = min(100.0, cv * 180.0)
        spread = max(sent_lengths) - min(sent_lengths)
    else:
        mean_len = float(sent_lengths[0]) if sent_lengths else 0.0
        std_dev = 0.0
        burstiness_score = 50.0
        spread = 0

    # Metric 3: Vocabulary Diversity / Content TTR (0-100 higher = more human)
    content_words = [w for w in words if len(w) > 2]
    vocab_div = (len(set(content_words)) / len(content_words) * 100.0) if len(content_words) >= 10 else 50.0

    # Metric 4: Sentence-Length Spread Score (0-100 higher = more human)
    spread_target = 16.0 if lang == "ar" else 20.0
    spread_score = min(100.0, (spread / spread_target) * 85.0) if len(sent_lengths) >= 3 else 50.0

    # Metric 5: Sentence-Starter Diversity (0-100 higher = more human)
    if len(sentences) >= 4:
        starters = [ tokenize_words(s)[0] for s in sentences if tokenize_words(s) ]
        starter_div = (len(set(starters)) / max(len(starters), 1)) * 100.0
    else:
        starter_div = 65.0

    # Metric 6: AI Phrase Hits (lower = more human)
    lower_prose = prose.lower()
    matched_phrases: list[str] = []
    for p in EN_AI_PHRASES:
        if p in lower_prose:
            matched_phrases.append(p)
    for p in AR_AI_PHRASES:
        if p in prose:
            matched_phrases.append(p)
    neg_en = re.findall(r"\bnot\s+(?:just|merely|simply)\s+[^.?!]{2,50},\s*but\b", lower_prose)
    neg_ar = re.findall(r"لا\s+يقتصر\s+(?:الأمر\s+)?على\s+[^.؟!]{2,50}بل", prose)
    matched_phrases.extend(neg_en)
    matched_phrases.extend(neg_ar)
    ai_phrase_penalty = min(100.0, (len(matched_phrases) / sent_count) * 85.0)

    # Metric 7: Mechanical Transition Density (lower = more human)
    trans_hits = 0
    for t in EN_TRANSITIONS:
        trans_hits += len(re.findall(rf"\b{re.escape(t)}\b", lower_prose))
    for t in AR_TRANSITIONS:
        trans_hits += prose.count(t)
    transition_penalty = min(100.0, (trans_hits / max(word_count, 1)) * 900.0)

    # Metric 8: Hedge Density (lower = more human)
    hedge_hits = sum(lower_prose.count(h) for h in EN_HEDGES) + sum(prose.count(h) for h in AR_HEDGES)
    hedge_penalty = min(100.0, (hedge_hits / sent_count) * 90.0)

    # Metric 9: Passive / Calque Ratio (EN passive + AR تم/بشكل calques)
    if lang == "ar":
        calque_hits = len(re.findall(r"\b(?:تم|يتم|يقوم\s+بـ|تقوم\s+بـ|بشكل)\s+[\u0600-\u06FF]{3,}", prose))
        passive_calque_penalty = min(100.0, (calque_hits / sent_count) * 55.0)
    else:
        passive_hits = len(re.findall(r"\b(?:is|are|was|were|been|being)\s+\w+(?:ed|en)\b", lower_prose))
        passive_calque_penalty = min(100.0, (passive_hits / sent_count) * 45.0)

    # Metric 10: Punctuation & Formatting Tell Penalty (Em dashes, bold-colon lists)
    em_dashes = prose.count("—") + len(re.findall(r"\s--\s", prose))
    bold_labels = len(re.findall(r"^\s*[-*]\s+\*\*[^*]+\*\*\s*[:—-]", raw_text, flags=re.MULTILINE))
    punct_penalty = min(100.0, em_dashes * (35.0 if lang == "ar" else 18.0) + bold_labels * 10.0)

    # Metric 11: Concrete Specificity Anchor Bonus (numbers, years, percentages, quotes)
    anchors = len(re.findall(r"\b\d+(?:[.,]\d+)?%?\b", prose))
    anchor_score = min(100.0, 40.0 + (anchors / max(sent_count, 1)) * 120.0)

    # Metric 12: Consecutive Uniform Rhythm Penalty
    uniform_windows = 0
    for i in range(max(0, len(sent_lengths) - 2)):
        w = sent_lengths[i : i + 3]
        if max(w) - min(w) <= 4:
            uniform_windows += 1
    uniform_penalty = min(100.0, (uniform_windows / max(len(sent_lengths) - 2, 1)) * 80.0) if len(sent_lengths) >= 4 else 0.0

    # Composite Human Score (0-100, higher = more human-consistent)
    positive = (
        perplexity_score * 0.20
        + burstiness_score * 0.22
        + vocab_div * 0.12
        + spread_score * 0.14
        + starter_div * 0.12
        + anchor_score * 0.20
    )
    penalties = (
        ai_phrase_penalty * 0.34
        + transition_penalty * 0.14
        + hedge_penalty * 0.12
        + passive_calque_penalty * 0.14
        + punct_penalty * 0.14
        + uniform_penalty * 0.12
    )
    human_score = round(max(0.0, min(100.0, positive - penalties * 0.75 + 12.0)), 1)
    ai_risk_score = round(100.0 - human_score, 1)

    # Per-sentence heatmap
    heatmap: list[dict[str, Any]] = []
    for idx, sent in enumerate(sentences, 1):
        s_low = sent.lower()
        reasons: list[str] = []
        risk = 15
        for p in EN_AI_PHRASES:
            if p in s_low:
                reasons.append(f"AI phrase: '{p}'")
                risk += 25
        for p in AR_AI_PHRASES:
            if p in sent:
                reasons.append(f"عبارة آلية: '{p}'")
                risk += 25
        if "—" in sent or " -- " in sent:
            reasons.append("Em dash (—)")
            risk += 20
        if re.search(r"\bnot\s+(?:just|merely|simply)\b", s_low) or re.search(r"لا\s+يقتصر|ليس\s+مجرد", sent):
            reasons.append("Negative parallelism (Not X, but Y)")
            risk += 28
        if lang == "ar" and re.search(r"\b(?:تم|يقوم\s+بـ|بشكل)\s+[\u0600-\u06FF]{3,}", sent):
            reasons.append("ترجمة حرفية (تم/يقوم بـ/بشكل)")
            risk += 16
        if idx >= 3 and max(sent_lengths[idx - 3 : idx]) - min(sent_lengths[idx - 3 : idx]) <= 3:
            reasons.append(f"Uniform rhythm ({sent_lengths[idx-3:idx]} words)")
            risk += 15
        if reasons:
            heatmap.append(
                {
                    "sentence_index": idx,
                    "word_count": len(sent.split()),
                    "ai_risk": min(99, risk),
                    "reasons": reasons,
                    "excerpt": sent[:140] + ("..." if len(sent) > 140 else ""),
                }
            )
    heatmap.sort(key=lambda x: x["ai_risk"], reverse=True)

    verdict = (
        "Human-Consistent (Low AI Signal)"
        if human_score >= 72
        else "Mixed / Edited AI or Templated Prose"
        if human_score >= 48
        else "High AI Signal Footprint"
    )

    return {
        "language": lang,
        "word_count": word_count,
        "sentence_count": len(sentences),
        "human_score": human_score,
        "ai_risk_score": ai_risk_score,
        "verdict": verdict,
        "sentence_lengths": sent_lengths,
        "metrics": {
            "1_bigram_perplexity_proxy": round(perplexity_score, 1),
            "2_burstiness_score": round(burstiness_score, 1),
            "3_vocabulary_diversity": round(vocab_div, 1),
            "4_sentence_spread_score": round(spread_score, 1),
            "5_sentence_starter_diversity": round(starter_div, 1),
            "6_ai_phrase_penalty": round(ai_phrase_penalty, 1),
            "7_transition_density_penalty": round(transition_penalty, 1),
            "8_hedge_density_penalty": round(hedge_penalty, 1),
            "9_passive_or_calque_penalty": round(passive_calque_penalty, 1),
            "10_punctuation_formatting_penalty": round(punct_penalty, 1),
            "11_specificity_anchor_score": round(anchor_score, 1),
            "12_uniform_rhythm_penalty": round(uniform_penalty, 1),
        },
        "counts": {
            "em_dashes": em_dashes,
            "bold_list_labels": bold_labels,
            "ai_phrases_matched": matched_phrases,
            "transition_hits": trans_hits,
            "hedge_hits": hedge_hits,
            "mean_sentence_words": round(mean_len, 1),
            "sentence_std_dev": round(std_dev, 2),
            "sentence_spread": spread,
        },
        "top_flagged_sentences": heatmap[:6],
    }


def render_markdown(rep: dict[str, Any]) -> str:
    c = rep["counts"]
    m = rep["metrics"]
    lines = [
        f"## Stylometric AI Audit ({rep['language'].upper()})",
        f"- **Human Consistency Score:** `{rep['human_score']}/100` (AI Signal Risk: `{rep['ai_risk_score']}/100` — *{rep['verdict']}*)",
        f"- **Volume & Rhythm:** `{rep['word_count']}` words across `{rep['sentence_count']}` sentences | Mean `{c['mean_sentence_words']}`w | StdDev `{c['sentence_std_dev']}`w | Spread `{c['sentence_spread']}`w",
        f"- **Sentence Lengths:** `{rep['sentence_lengths']}`",
        f"- **Mechanical Counts:** Em-dashes=`{c['em_dashes']}`, Bold-list-labels=`{c['bold_list_labels']}`, Transitions=`{c['transition_hits']}`, Hedges=`{c['hedge_hits']}`",
        "",
        "### 12-Metric Breakdown",
        f"- Positive Signals (higher=human): Perplexity=`{m['1_bigram_perplexity_proxy']}`, Burstiness=`{m['2_burstiness_score']}`, Vocab=`{m['3_vocabulary_diversity']}`, Spread=`{m['4_sentence_spread_score']}`, Starters=`{m['5_sentence_starter_diversity']}`, Anchors=`{m['11_specificity_anchor_score']}`",
        f"- Penalty Signals (higher=AI-like): Phrases=`{m['6_ai_phrase_penalty']}`, Transitions=`{m['7_transition_density_penalty']}`, Hedges=`{m['8_hedge_density_penalty']}`, Passive/Calques=`{m['9_passive_or_calque_penalty']}`, Punctuation=`{m['10_punctuation_formatting_penalty']}`, UniformRuns=`{m['12_uniform_rhythm_penalty']}`",
    ]
    if c["ai_phrases_matched"]:
        lines.append(f"- **Matched AI Phrases:** {', '.join(repr(x) for x in c['ai_phrases_matched'][:12])}")
    if rep["top_flagged_sentences"]:
        lines.append("\n### Highest-Risk Sentences (Heatmap)")
        for item in rep["top_flagged_sentences"]:
            lines.append(
                f"- **[S{item['sentence_index']} | {item['word_count']}w | Risk {item['ai_risk']}%]** "
                f"({'; '.join(item['reasons'])}): \"{item['excerpt']}\""
            )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="12-metric local stylometric AI writing detector (EN & AR).")
    parser.add_argument("--file", "-f", help="Input file path (reads stdin if omitted).")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Report output format.")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    report = analyze_text(text)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
