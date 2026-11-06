# Repository Contract (`AGENTS.md`)

`skills/` is the single canonical source of truth for all five Agent Skills (`humanize`, `humanize-text`, `ai-writing-detector`, `anti-slop-coder`, `academic-humanizer`).

## Invariants

1. **Edit only inside `skills/<skill-name>/`** and then run `./scripts/sync-platforms.sh` to mirror changes identically into `.opencode/skills/`, `.claude/skills/`, `.agents/skills/`, and `.dsh/skills/`.
2. **Flat depth-1 discovery:** Every skill directory must remain directly under `<root>/<skill-name>/SKILL.md` so `@deepseek-ai/dsh-skill-filesystem` (DeepSeek Harness) discovers all skills without silent category-folder skipping.
3. **Strict frontmatter:** Keep `description` in YAML frontmatter as a single-line double-quoted string so strict parsers in OpenCode and DeepSeek Harness never skip a skill on unquoted colons.
4. **Zero external dependencies:** All scripts under `skills/*/scripts/` must use Python 3.9+ standard library only.
5. **Pre-commit check:** Always run `./scripts/sync-platforms.sh --check && python3 scripts/validate.py` before committing.
