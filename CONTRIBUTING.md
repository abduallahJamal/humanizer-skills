# Contributing

Contributions that sharpen detection precision, expand English or Arabic pattern coverage, or improve cross-agent compatibility are welcome.

## Workflow

1. Make edits inside `skills/<skill-name>/` (never directly inside mirrored dot-directories).
2. Sync mirrored directories across OpenCode, Claude Code, Codex, and DeepSeek Harness:
   ```bash
   ./scripts/sync-platforms.sh
   ```
3. Run the validation suite:
   ```bash
   ./scripts/sync-platforms.sh --check
   python3 scripts/validate.py
   ```
4. Keep commit messages terse and specific, and keep all bundled Python scripts strictly zero-dependency (`stdlib` only).
