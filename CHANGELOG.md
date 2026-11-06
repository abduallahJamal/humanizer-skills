# Changelog

All notable changes to `humanizer-skills` are documented in this file.

## [1.0.0] — 2026-11-06

### Added
- **5 Cross-Agent Skills (`skills/`):**
  - `humanize` — Orchestrator router (`/humanize`) dispatching requests by register and intent.
  - `humanize-text` — Bilingual (EN & AR) 3-pass + 9-lever humanizer with 5 voice profiles (`voices.md`), English 26-pattern reference (`en-patterns.md`), Arabic calque & rhetoric dictionary (`ar-patterns.md`), and deterministic post-rewrite verifier (`humanize_gate.py`).
  - `ai-writing-detector` — Detect-only forensic scorer combining a 12-metric local stylometric analyzer (`detect_ai_metrics.py`) with a 9-signal rubric (`0–27`, `scoring-rubric.md`) and sentence-level heatmap.
  - `anti-slop-coder` — Proactive and edit-in-place hygiene for `README.md`, docs, PRs, git commits, review replies, and code comments, paired with `repo_slop_scan.py`.
  - `academic-humanizer` — Scholarly & formal humanizer for English and MSA Arabic with contraction expansion, position-aware denominalization, 100% citation/equation/number lock, and word-level diff output (`academic_prep.py`).
- **4-Agent Native Packaging:** Mirrored roots and plugin manifests for **OpenCode** (`.opencode/`), **Claude Code** (`.claude/` + `.claude-plugin/`), **OpenAI Codex CLI** (`.agents/` + `agents/openai.yaml`), and **DeepSeek Harness** (`.dsh/skills/` flat single-level layout).
- **Tooling & CI:** `install.sh`, `install.py`, `install.ps1`, `scripts/sync-platforms.sh` (SHA-256 parity check), `scripts/validate.py`, and GitHub Actions workflow `.github/workflows/validate.yml`.
