#!/usr/bin/env python3
"""
validate.py — Repository, Cross-Harness Skill Schema & Functional CLI Validator

Checks:
1. Canonical skills/ (5 skills) + strict YAML frontmatter (OpenCode/DSH/Claude/Codex safe)
2. Codex sidecars (agents/openai.yaml), OpenCode command (.opencode/commands/humanize.md), and JSON manifests
3. Markdown relative link integrity across README.md, README.ar.md, and SKILL.md files
4. End-to-end execution of all 4 bundled zero-dependency Python CLI scripts on EN & AR fixtures
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = SUITE_ROOT / "skills"
EXPECTED_SKILLS = {
    "humanize",
    "humanize-text",
    "ai-writing-detector",
    "anti-slop-coder",
    "academic-humanizer",
}
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(msg: str, gh_annot: bool, file: str | None = None) -> None:
    if gh_annot and file:
        print(f"::error file={file}::{msg}")
    elif gh_annot:
        print(f"::error::{msg}")
    else:
        print(f"[FAIL] {msg}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(md_text: str, rel_file: str, gh_annot: bool) -> dict[str, str]:
    if not md_text.startswith("---\n"):
        fail("SKILL.md must open with '---\\n' YAML frontmatter", gh_annot, rel_file)
    end_idx = md_text.find("\n---\n", 4)
    if end_idx == -1:
        fail("SKILL.md must close YAML frontmatter with '\\n---\\n'", gh_annot, rel_file)
    block = md_text[4:end_idx]
    parsed: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.startswith("  "):
            continue
        if ":" not in line:
            fail(f"Invalid YAML line: {line}", gh_annot, rel_file)
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if ":" in val and not (
            (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'"))
        ):
            fail(f"Unquoted colon in frontmatter key '{key}' breaks strict parsers", gh_annot, rel_file)
        parsed[key] = val.strip('"').strip("'")
    return parsed


def check_skills_and_manifests(gh_annot: bool) -> None:
    print("[1/4] Validating 5 canonical skills, frontmatter, sidecars & JSON manifests...")
    discovered = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()}
    if discovered != EXPECTED_SKILLS:
        fail(f"Expected {EXPECTED_SKILLS}, got {discovered}", gh_annot)

    for skill_name in sorted(EXPECTED_SKILLS):
        sdir = SKILLS_DIR / skill_name
        if not KEBAB_RE.match(skill_name):
            fail(f"Invalid kebab-case skill directory: {skill_name}", gh_annot)
        skill_md = sdir / "SKILL.md"
        rel = str(skill_md.relative_to(SUITE_ROOT))
        if not skill_md.is_file():
            fail(f"Missing {rel}", gh_annot, rel)
        fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"), rel, gh_annot)
        if fm.get("name") != skill_name:
            fail(f"Frontmatter name '{fm.get('name')}' != directory '{skill_name}'", gh_annot, rel)
        desc = fm.get("description", "")
        if not (40 <= len(desc) <= 1024):
            fail(f"Description length ({len(desc)}) out of bounds [40, 1024]", gh_annot, rel)

        sidecar = sdir / "agents" / "openai.yaml"
        if not sidecar.is_file():
            fail(f"Missing Codex sidecar {sidecar.relative_to(SUITE_ROOT)}", gh_annot)
        if f"${skill_name}" not in sidecar.read_text(encoding="utf-8"):
            fail(f"Codex sidecar must reference ${skill_name}", gh_annot, str(sidecar.relative_to(SUITE_ROOT)))

    cmd_file = SUITE_ROOT / ".opencode" / "commands" / "humanize.md"
    if not cmd_file.is_file():
        fail("Missing .opencode/commands/humanize.md", gh_annot)

    claude_plugin = json.loads((SUITE_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if "$schema" in claude_plugin:
        fail("Remove top-level $schema from .claude-plugin/plugin.json", gh_annot, ".claude-plugin/plugin.json")
    json.loads((SUITE_ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    json.loads((SUITE_ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
    print("  OK")


def check_markdown_links(gh_annot: bool) -> None:
    print("[2/4] Checking relative links in README.md, README.ar.md & SKILL.md files...")
    md_files = [SUITE_ROOT / "README.md", SUITE_ROOT / "README.ar.md"] + list(SKILLS_DIR.glob("*/SKILL.md"))
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

    for md in md_files:
        if not md.is_file():
            fail(f"Missing markdown file: {md.relative_to(SUITE_ROOT)}", gh_annot)
        text = re.sub(r"```[\s\S]*?```", "", md.read_text(encoding="utf-8"))
        for m in link_re.finditer(text):
            target = m.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean_target = target.split("#", 1)[0]
            if not clean_target:
                continue
            resolved = (md.parent / clean_target).resolve()
            if not resolved.exists():
                fail(
                    f"Broken relative link '{target}' -> {resolved}",
                    gh_annot,
                    str(md.relative_to(SUITE_ROOT)),
                )
    print("  OK")


def check_bundled_scripts(gh_annot: bool) -> None:
    print("[3/4] Running functional tests on all 4 bundled Python CLI tools (EN & AR)...")
    det_script = SKILLS_DIR / "ai-writing-detector" / "scripts" / "detect_ai_metrics.py"
    gate_script = SKILLS_DIR / "humanize-text" / "scripts" / "humanize_gate.py"
    coder_script = SKILLS_DIR / "anti-slop-coder" / "scripts" / "repo_slop_scan.py"
    acad_script = SKILLS_DIR / "academic-humanizer" / "scripts" / "academic_prep.py"

    ar_slop = (
        "في ظل التطورات المتسارعة التي يشهدها العالم اليوم، مما لا شك فيه أن الذكاء الاصطناعي يلعب دوراً محورياً. "
        "علاوة على ذلك، يتم استخدام هذه التقنيات بشكل كبير في المشهد الرقمي لإطلاق العنان للابتكار. "
        "بالإضافة إلى ذلك، لا يقتصر الأمر على الشركات الكبرى فحسب، بل يتعداه إلى المؤسسات الناشئة. "
        "وفي الختام، يمكن القول إن المستقبل يبدو واعداً."
    )
    ar_human = (
        "عطّلنا خادم التخزين المؤقت يوم الثلاثاء الماضي لمدة عشرين دقيقة لمعرفة أين يختنق النظام فعلياً. "
        "النتيجة فاجأت الجميع. "
        "قاعدة البيانات تحمّلت الضغط دون أي تراجع في زمن الاستجابة (بقيت عند 42 مللي ثانية)، "
        "بينما انهارت خدمة الفوترة الخارجية لأنها تعيد فتح اتصال TLS جديد مع كل طلب فردي بدل إعادة استخدامه."
    )

    s_out = json.loads(
        subprocess.run([sys.executable, str(det_script), "--format", "json"], input=ar_slop, text=True, capture_output=True, check=True).stdout
    )
    h_out = json.loads(
        subprocess.run([sys.executable, str(det_script), "--format", "json"], input=ar_human, text=True, capture_output=True, check=True).stdout
    )
    if h_out["human_score"] <= s_out["human_score"] + 25:
        fail("Detector failed to separate Arabic AI slop from human Arabic writing", gh_annot)

    with tempfile.TemporaryDirectory() as tmp:
        tp = Path(tmp)
        orig = tp / "orig.txt"
        bad = tp / "bad.txt"
        good = tp / "good.txt"
        orig.write_text(
            "Certainly! Acme Analytics — nestled in Boulder — raised $40M in 2025 to streamline observability in Quranic NLP.",
            encoding="utf-8",
        )
        bad.write_text(
            "Acme Analytics — in Boulder — raised $50M in 2025 to leverage implementing of observability.",
            encoding="utf-8",
        )
        good.write_text(
            "Acme Analytics raised $40M in 2025. "
            "The Boulder startup builds observability tools for Quranic NLP pipelines, "
            "cutting query latency for engineering teams that outgrew ad-hoc log scripts.",
            encoding="utf-8",
        )
        if subprocess.run([sys.executable, str(gate_script), "-o", str(orig), "-r", str(bad)], capture_output=True).returncode == 0:
            fail("humanize_gate.py failed to reject broken rewrite", gh_annot)
        if subprocess.run([sys.executable, str(gate_script), "-o", str(orig), "-r", str(good)], capture_output=True).returncode != 0:
            fail("humanize_gate.py rejected valid human rewrite", gh_annot)

        code_sample = tp / "sample.py"
        code_sample.write_text("# Import the required libraries\nimport sys\n", encoding="utf-8")
        if subprocess.run([sys.executable, str(coder_script), str(code_sample)], capture_output=True).returncode == 0:
            fail("repo_slop_scan.py missed narrating code comment", gh_annot)

        p_in = tp / "p_in.txt"
        p_out = tp / "p_out.txt"
        p_diff = tp / "diff.md"
        p_in.write_text("We didn't observe drift [12] (Smith et al., 2025) at $\\alpha = 0.05$ across N = 240 runs.", encoding="utf-8")
        p_out.write_text("Across N = 240 runs at $\\alpha = 0.05$, we did not observe parameter drift [12] (Smith et al., 2025).", encoding="utf-8")
        if subprocess.run([sys.executable, str(acad_script), "verify", "-o", str(p_in), "-r", str(p_out), "-d", str(p_diff)], capture_output=True).returncode != 0:
            fail("academic_prep.py failed valid scholarly rewrite", gh_annot)
    print("  OK")


def check_dsh_single_level_rule(gh_annot: bool) -> None:
    print("[4/4] Verifying DeepSeek Harness single-level discovery across mirrored roots...")
    for root_rel in [".opencode/skills", ".claude/skills", ".agents/skills", ".dsh/skills"]:
        rpath = SUITE_ROOT / root_rel
        if not rpath.is_dir():
            fail(f"Missing mirrored root {root_rel} (run ./scripts/sync-platforms.sh)", gh_annot)
        children = {c.name for c in rpath.iterdir() if c.is_dir()}
        if children != EXPECTED_SKILLS:
            fail(f"Root {root_rel} has {children}, expected {EXPECTED_SKILLS}", gh_annot)
        for c in EXPECTED_SKILLS:
            if not (rpath / c / "SKILL.md").is_file():
                fail(f"Missing {root_rel}/{c}/SKILL.md", gh_annot)
    print("  OK")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate humanizer-skills repository.")
    parser.add_argument("--github-annotations", action="store_true", help="Emit GitHub Actions error annotations.")
    args = parser.parse_args()

    check_skills_and_manifests(args.github_annotations)
    check_markdown_links(args.github_annotations)
    check_bundled_scripts(args.github_annotations)
    check_dsh_single_level_rule(args.github_annotations)
    print("\n[SUCCESS] All validation checks passed!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
