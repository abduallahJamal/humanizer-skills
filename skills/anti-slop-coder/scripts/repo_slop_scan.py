#!/usr/bin/env python3
"""
repo_slop_scan.py — Developer Docs, Commit & Code Anti-Slop Scanner (EN & AR)

Scans Markdown docs (safely ignoring fenced code blocks!), git commit message files,
and source code files for:
- Prose em-dashes, AI buzzwords, chatbot residue, heading emojis, bold-colon list bloat
- Narrating code comments ("// Import ...", "# Return the result", "# استيراد ...")
- AI git co-author / generated-by trailers

Zero external dependencies (Python 3.9+ stdlib only).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

DOC_EXTS = {".md", ".mdx", ".rst", ".txt"}
CODE_EXTS = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".rb", ".php", ".sh"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__", ".next"}

DOC_BUZZWORDS = re.compile(
    r"\b(delve|delves|tapestry|leverage|leverages|leveraging|utilize|utilizes|utilizing|"
    r"streamline|paramount|pivotal|meticulous|holistic|multifaceted|spearhead|game-changing|"
    r"cutting-edge|happy\s+coding|in\s+today'?s\s+fast-paced|let'?s\s+dive\s+in|"
    r"stands\s+as\s+a\s+testament)\b|"
    r"(في\s+ظل\s+التطورات\s+المتسارعة|يلعب\s+دوراً\s+محورياً|إطلاق\s+العنان|تسخير\s+إمكانات)",
    re.IGNORECASE,
)

HEADING_EMOJI = re.compile(r"^#{1,6}\s+[\U0001F300-\U0001FAFF\u2600-\u27BF]")
BOLD_COLON_BULLET = re.compile(r"^\s*[-*]\s+\*\*[^*]{2,40}\*\*\s*[:—-]\s+")
AI_TRAILER = re.compile(
    r"(Co-authored-by:\s*(?:Claude|Cursor|GitHub\s+Copilot|Codex|OpenCode|Gemini|Aider)|"
    r"Generated\s+(?:with|by)\s+(?:Claude|Cursor|ChatGPT|Codex))",
    re.IGNORECASE,
)

NARRATING_COMMENT = re.compile(
    r"^\s*(?://|#)\s*(?:"
    r"import\s+(?:the\s+)?(?:required|necessary)?|"
    r"define\s+(?:the\s+)?(?:function|class|type|interface|variable|constant)|"
    r"initialize\s+(?:the\s+)?|"
    r"fetch\s+(?:the\s+)?\w+\s+from\s+(?:the\s+)?|"
    r"return\s+the\s+(?:result|response|output|first|updated|created)|"
    r"loop\s+(?:through|over)\s+(?:all\s+|the\s+)?|"
    r"check\s+if\s+(?:the\s+)?\w+\s+is\s+|"
    r"set\s+the\s+\w+\s+to\s+|"
    r"استيراد\s+المكتبات|تعريف\s+(?:الدالة|المتغير|الكلاس)|إرجاع\s+النتيجة|التحقق\s+من\s+أن"
    r")\b",
    re.IGNORECASE,
)


def iter_files(targets: list[str]) -> list[Path]:
    collected: list[Path] = []
    for raw in targets:
        p = Path(raw)
        if p.is_file():
            collected.append(p)
        elif p.is_dir():
            for child in sorted(p.rglob("*")):
                if any(part in SKIP_DIRS for part in child.parts):
                    continue
                if child.is_file() and (child.suffix.lower() in DOC_EXTS | CODE_EXTS or child.name == "COMMIT_EDITMSG"):
                    collected.append(child)
    return collected


def scan_doc_file(path: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    in_fence = False
    bold_bullet_run = 0

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        # Strip inline code before checking prose rules
        clean_line = re.sub(r"`[^`]+`", "", line)

        if HEADING_EMOJI.search(clean_line):
            findings.append({"file": str(path), "line": lineno, "rule": "heading-emoji", "excerpt": stripped[:100]})

        # Em-dash check (carve out list item separator `- **Term** — desc` only if not clustered, still warn on mid-sentence)
        if "—" in clean_line or " -- " in clean_line:
            findings.append({"file": str(path), "line": lineno, "rule": "prose-em-dash", "excerpt": stripped[:100]})

        m_buzz = DOC_BUZZWORDS.search(clean_line)
        if m_buzz:
            findings.append(
                {
                    "file": str(path),
                    "line": lineno,
                    "rule": f"ai-buzzword ({m_buzz.group(0)})",
                    "excerpt": stripped[:100],
                }
            )

        if BOLD_COLON_BULLET.search(clean_line):
            bold_bullet_run += 1
            if bold_bullet_run == 3:
                findings.append(
                    {
                        "file": str(path),
                        "line": lineno,
                        "rule": "bold-colon-list-cluster (3+ uniform bold-label bullets)",
                        "excerpt": stripped[:100],
                    }
                )
        elif stripped:
            bold_bullet_run = 0

        m_tr = AI_TRAILER.search(line)
        if m_tr:
            findings.append({"file": str(path), "line": lineno, "rule": "ai-git-trailer", "excerpt": stripped[:100]})

    return findings


def scan_code_file(path: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for lineno, line in enumerate(lines, 1):
        if NARRATING_COMMENT.search(line):
            findings.append(
                {
                    "file": str(path),
                    "line": lineno,
                    "rule": "narrating-comment (explains WHAT instead of WHY)",
                    "excerpt": line.strip()[:100],
                }
            )
        if AI_TRAILER.search(line):
            findings.append(
                {"file": str(path), "line": lineno, "rule": "ai-git-trailer", "excerpt": line.strip()[:100]}
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan docs, code, and commit messages for developer AI slop.")
    parser.add_argument("targets", nargs="+", help="Files or directories to scan.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    args = parser.parse_args()

    files = iter_files(args.targets)
    all_findings: list[dict[str, Any]] = []
    for f in files:
        if f.suffix.lower() in DOC_EXTS or f.name == "COMMIT_EDITMSG":
            all_findings.extend(scan_doc_file(f))
        elif f.suffix.lower() in CODE_EXTS:
            all_findings.extend(scan_code_file(f))

    if args.format == "json":
        print(json.dumps({"scanned_files": len(files), "findings": all_findings}, ensure_ascii=False, indent=2))
    else:
        print(f"Scanned {len(files)} file(s) -> {len(all_findings)} finding(s).")
        for item in all_findings:
            print(f"  [{item['rule']}] {item['file']}:{item['line']} :: {item['excerpt']}")

    return 0 if not all_findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
