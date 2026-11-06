#!/usr/bin/env python3
"""
academic_prep.py — Scholarly Pre-Processor, Citation/Digit Integrity Verifier & Word-Level Diff

Synthesizes engineering features from:
- DadaNanjesha/AI-Text-Humanizer-App (contraction expansion + difflib word-level change highlighting)
- rudra496/StealthHumanizer (digitsPreserved + grammar sanity check + zero-width/NMT artifact cleanup)
- ZAYUVALYA/AI-Text-Humanizer (protected domain/fixed terms + Markdown/HTML diff report)

Subcommands:
  prep   — Clean artifacts, expand English contractions outside quotes/code, list locked citations & numbers
  verify — Verify 100% survival of citations, equations, numbers & fixed terms; optionally emit diff report

Zero external dependencies (Python 3.9+ stdlib only).
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path
from typing import Any

ARABIC_INDIC_MAP = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

CONTRACTIONS: list[tuple[str, str]] = [
    (r"\bcan't\b", "cannot"),
    (r"\bwon't\b", "will not"),
    (r"\bshan't\b", "shall not"),
    (r"\bdon't\b", "do not"),
    (r"\bdoesn't\b", "does not"),
    (r"\bdidn't\b", "did not"),
    (r"\bisn't\b", "is not"),
    (r"\baren't\b", "are not"),
    (r"\bwasn't\b", "was not"),
    (r"\bweren't\b", "were not"),
    (r"\bhasn't\b", "has not"),
    (r"\bhaven't\b", "have not"),
    (r"\bhadn't\b", "had not"),
    (r"\bwouldn't\b", "would not"),
    (r"\bshouldn't\b", "should not"),
    (r"\bcouldn't\b", "could not"),
    (r"\bit's\b", "it is"),
    (r"\bthat's\b", "that is"),
    (r"\bthere's\b", "there is"),
    (r"\bwe're\b", "we are"),
    (r"\bthey're\b", "they are"),
    (r"\bwe've\b", "we have"),
    (r"\bthey've\b", "they have"),
    (r"\bwe'll\b", "we will"),
    (r"\bthey'll\b", "they will"),
]

CITATION_PATTERNS = [
    r"\[\d+(?:\s*[-–,]\s*\d+)*\]",  # [1], [12-15], [3, 7]
    r"\([A-Z][A-Za-z\-]+(?:\s+et\s+al\.)?,\s*\d{4}[a-z]?(?:;\s*[^)]+)?\)",  # (Smith et al., 2024)
    r"\([\u0600-\u06FF\s]+،\s*\d{4}\)",  # (العلي، 2024)
    r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b",  # DOI
]

EQUATION_PATTERN = re.compile(r"\$\$[\s\S]*?\$\$|\$[^$\n]+\$")


def match_case(original: str, replacement: str) -> str:
    if original.isupper():
        return replacement.upper()
    if original[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def expand_contractions_safe(text: str) -> tuple[str, int]:
    """Expand contractions outside fenced code, inline code, and math."""
    protected: list[str] = []

    def stash(m: re.Match[str]) -> str:
        protected.append(m.group(0))
        return f"__LOCKED_SPAN_{len(protected) - 1}__"

    working = re.sub(r"```[\s\S]*?```|`[^`\n]+`|\$\$[\s\S]*?\$\$|\$[^$\n]+\$", stash, text)
    total_expansions = 0

    for pat, repl in CONTRACTIONS:
        def _sub(m: re.Match[str]) -> str:
            nonlocal total_expansions
            total_expansions += 1
            return match_case(m.group(0), repl)

        working = re.sub(pat, _sub, working, flags=re.IGNORECASE)

    for idx, val in enumerate(protected):
        working = working.replace(f"__LOCKED_SPAN_{idx}__", val)

    return working, total_expansions


def clean_artifacts(text: str) -> str:
    text = text.replace("\u200b", "").replace("\ufeff", "")
    text = re.sub(r"\s*:contentReference\[[^\]]*\]\{[^}]*\}", "", text)
    text = re.sub(r"\s*\(\s*oaicite:[^)]+\)", "", text)
    return text


def extract_citations(text: str) -> list[str]:
    found: list[str] = []
    for pat in CITATION_PATTERNS:
        found.extend(re.findall(pat, text))
    return sorted(found)


def extract_numbers(text: str) -> list[str]:
    norm = text.translate(ARABIC_INDIC_MAP)
    return sorted(n.replace(",", "") for n in re.findall(r"\d+(?:[.,]\d+)*", norm))


def extract_equations(text: str) -> list[str]:
    return [e.strip() for e in EQUATION_PATTERN.findall(text)]


def build_word_diff_markdown(original: str, rewritten: str) -> str:
    """DadaNanjesha / ZAYUVALYA style word-level diff in clean Markdown/HTML."""
    orig_words = original.split()
    rew_words = rewritten.split()
    matcher = difflib.SequenceMatcher(None, orig_words, rew_words)

    parts: list[str] = []
    changed_spans = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            parts.append(" ".join(rew_words[j1:j2]))
        elif tag == "replace":
            changed_spans += 1
            parts.append(f"~~{' '.join(orig_words[i1:i2])}~~ **{' '.join(rew_words[j1:j2])}**")
        elif tag == "insert":
            changed_spans += 1
            parts.append(f"**{' '.join(rew_words[j1:j2])}**")
        elif tag == "delete":
            changed_spans += 1
            parts.append(f"~~{' '.join(orig_words[i1:i2])}~~")

    header = (
        f"# Academic Humanization Diff Report\n\n"
        f"- **Original words:** `{len(orig_words)}`\n"
        f"- **Rewritten words:** `{len(rew_words)}`\n"
        f"- **Modified spans:** `{changed_spans}`\n\n"
        f"## Highlighted Changes\n\n"
    )
    return header + " ".join(parts) + "\n"


def cmd_prep(args: argparse.Namespace) -> int:
    raw = Path(args.input).read_text(encoding="utf-8") if args.input else sys.stdin.read()
    cleaned = clean_artifacts(raw)
    expanded, exp_count = expand_contractions_safe(cleaned)
    citations = extract_citations(expanded)
    numbers = extract_numbers(expanded)
    equations = extract_equations(expanded)

    if args.output:
        Path(args.output).write_text(expanded, encoding="utf-8")
    else:
        print(expanded)

    summary = {
        "contractions_expanded": exp_count,
        "locked_citations_count": len(citations),
        "locked_citations": citations,
        "locked_numbers_count": len(numbers),
        "locked_equations_count": len(equations),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2), file=sys.stderr)
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    orig = Path(args.original).read_text(encoding="utf-8")
    rew = Path(args.rewritten).read_text(encoding="utf-8")

    issues: list[str] = []

    # 1. Citations survival
    orig_cit = extract_citations(orig)
    rew_cit = extract_citations(rew)
    missing_cit = [c for c in set(orig_cit) if rew_cit.count(c) < orig_cit.count(c)]
    if missing_cit:
        issues.append(f"Missing or altered citations: {missing_cit}")

    # 2. Equations survival
    orig_eq = extract_equations(orig)
    rew_eq = extract_equations(rew)
    missing_eq = [e for e in orig_eq if e not in rew_eq]
    if missing_eq:
        issues.append(f"Missing or altered LaTeX equations: {missing_eq}")

    # 3. Digits survival
    orig_nums = extract_numbers(orig)
    rew_nums = extract_numbers(rew)
    missing_nums = [n for n in set(orig_nums) if rew_nums.count(n) < orig_nums.count(n)]
    added_nums = [n for n in set(rew_nums) if rew_nums.count(n) > orig_nums.count(n)]
    if missing_nums:
        issues.append(f"Numbers/statistics dropped: {missing_nums}")
    if added_nums:
        issues.append(f"Unverified numbers introduced: {added_nums}")

    # 4. Contractions regression check
    _, leftover_contractions = expand_contractions_safe(rew)
    if leftover_contractions > 0:
        issues.append(f"Informal contractions found in academic output ({leftover_contractions}); expand them.")

    # 5. Stock transition spam check (DadaNanjesha counter-lesson)
    stock_spam = len(
        re.findall(
            r"(?:^|[.!?]\s+)(?:Moreover|Furthermore|Additionally),|(?:\bعلاوة\s+على\s+ذلك|\bبالإضافة\s+إلى\s+ذلك)",
            rew,
            flags=re.MULTILINE,
        )
    )
    if stock_spam >= 2:
        issues.append(
            f"Stock transition cluster ({stock_spam}x Moreover/Furthermore/علاوة على ذلك) — replace with referential cohesion."
        )

    # 6. Optional fixed terms check
    if args.fixed_terms:
        for term in [t.strip() for t in args.fixed_terms.split(",") if t.strip()]:
            if term.lower() in orig.lower() and term.lower() not in rew.lower():
                issues.append(f"Protected domain term dropped: '{term}'")

    if args.diff:
        diff_md = build_word_diff_markdown(orig, rew)
        Path(args.diff).write_text(diff_md, encoding="utf-8")

    result = {
        "status": "PASS" if not issues else "FAIL",
        "citations_preserved": f"{len(orig_cit) - len(missing_cit)}/{len(orig_cit)}",
        "numbers_preserved": f"{len(set(orig_nums)) - len(missing_nums)}/{len(set(orig_nums))}",
        "issues": issues,
        "diff_written_to": args.diff,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Scholarly pre-processor, citation/number verifier & diff generator.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_prep = sub.add_parser("prep", help="Expand contractions & clean artifacts while locking citations/math.")
    p_prep.add_argument("--input", "-i", help="Input text path (stdin if omitted).")
    p_prep.add_argument("--output", "-o", help="Output path (stdout if omitted).")

    p_ver = sub.add_parser("verify", help="Verify citation/number integrity and optionally write diff.")
    p_ver.add_argument("--original", "-o", required=True, help="Original source file.")
    p_ver.add_argument("--rewritten", "-r", required=True, help="Rewritten academic file.")
    p_ver.add_argument("--fixed-terms", help="Comma-separated domain terms to lock.")
    p_ver.add_argument("--diff", "-d", help="Optional path to save Markdown word-level diff.")

    args = parser.parse_args()
    return cmd_prep(args) if args.cmd == "prep" else cmd_verify(args)


if __name__ == "__main__":
    raise SystemExit(main())
