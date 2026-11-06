---
name: anti-slop-coder
description: "Prevent and surgically clean AI tells in developer artifacts: READMEs, technical docs, PR descriptions, git commit messages, issue replies, and code comments (EN & AR). Blocks narrating comments, AI co-author trailers, em dashes, bold-label bloat, and verbose commit marketing (منع بصمات الذكاء الاصطناعي في الكود والتوثيق والـ README ورسائل Git والتعليقات البرمجية)."
license: MIT
metadata:
  version: "1.0.0"
  languages: "en, ar"
---

# Anti-Slop Coder — Developer, Docs, Git & Code Hygiene (EN & AR)

Keep repositories, documentation, pull requests, commit history, and source comments reading like a sharp human engineer wrote them.

## Two Operating Modes

1. **Proactive Generation Mode:** Activate automatically when drafting READMEs, changelogs, PR descriptions, issue/review replies, architecture docs, commit messages, or code comments.
2. **Surgical Edit-in-Place Mode (`edit`):** Activate when asked to clean AI slop from existing `.md` / `.mdx` / `.rst` docs or code comments in a repo. Make **minimal, targeted edits**; preserve passages that already read fine, and **never touch** executable logic, fenced code blocks, CLI flags, URLs, file paths, tables, or YAML frontmatter.

Read `references/dev-antipatterns.md` for side-by-side before/after patterns in English and Arabic.

## Ten Hard Rules for Engineering Artifacts

### 1. Code Comments: Explain WHY, Never WHAT
- **Ban narrating comments** that restate the next line (`// Import dependencies`, `// Loop through users`, `# استيراد المكتبات`, `# إرجاع النتيجة`).
- Delete section-banner ASCII art (`// ==================== HELPERS ====================`) unless already established across the file.
- Comment only non-obvious invariants, performance traps, browser/OS quirks, protocol specs, or issue links.

### 2. Git Commits: Terse & Specific, Zero Marketing
- Write concise subject lines (< 55 chars) naming the concrete change (`fix token refresh race on 401`, `add Arabic RTL support to table header`).
- Follow the repo's existing commit style (`git log -n 10 --oneline`) — only add `feat:` / `fix:` prefixes if the repo already uses Conventional Commits.
- **Never** write commit bodies like `"This commit introduces a comprehensive and robust module that leverages..."`. Add a short body only when the *why* or migration impact isn't obvious from the diff.

### 3. Never Add AI Git Trailers Unless Asked
- Do **not** append `Co-authored-by: Claude...`, `Co-authored-by: Cursor...`, `Co-authored-by: GitHub Copilot...`, or `Generated with...` trailers unless the user or repository `CONTRIBUTING.md` explicitly requires them.

### 4. READMEs & Technical Docs: Substance First
- Open with **one plain sentence** stating what the package/tool actually does — never `"In today's fast-paced cloud-native landscape..."` or `"أداة ثورية شاملة لإطلاق العنان..."`.
- Follow immediately with copy-pasteable install and usage commands.
- Cut `Happy coding!`, `Let's dive in!`, decorative heading emojis (`## 🚀 Features`), Title Case on every subheading, and heading-echo first sentences (`## Caching\n\nCaching is crucial for performance.`).

### 5. Kill Bold-Label List Disease & Em Dashes in Prose
- Do not format every bullet as `- **Fast:** Lightning-quick processing` / `- **Reliable:** Battle-tested`. Write uneven, concrete bullets or plain prose.
- Avoid prose em dashes (`—` / ` -- `); use periods, commas, colons, or parentheses. Never touch hyphens/dashes inside code, CLI flags (`--profile`), or paths.

### 6. PR Descriptions & Code Review Replies: Lead With the Decision
- **PRs:** State (1) what changed, (2) why / linked issue, and (3) how it was verified. Cut `"This PR introduces a seamless..."`.
- **Review / Issue / Slack replies:** The reviewer already knows the thread context. Put the decision or answer in **sentence 1**, followed only by the single constraint or trade-off they haven't seen yet.

### 7. Do Not Narrate Deleted History Inside Permanent Docs
- In docs and code comments, describe how the system works **now** (`Uses an LRU cache with 5m TTL`), not how you edited it (`This function was updated to replace the old O(n^2) loop`). Save history for commit messages and `CHANGELOG.md`.

### 8. Clean Bilingual Arabic Technical Writing
- Avoid awkward calques in Arabic docs: write `يعالج الخادم الطلبات` instead of `يقوم الخادم بمعالجة الطلبات`, and `أضفنا المصادقة عبر JWT` or `يدعم النظام...` instead of repetitive `تم إضافة نظام مصادقة شامل يقوم بتوفير...`.
- Keep technical identifiers (`JWT`, `OAuth2`, `SKILL.md`, CLI commands) in backticks without mangling them into ambiguous translations.

### 9. Protect Structured Content During Cleanup
- Refuse prose-humanization passes on raw source code, JSON/YAML configs, lockfiles, SQL migrations, or test fixtures unless specifically asked to clean **comments/docstrings only**.

### 10. Verify With the Repo Slop Scanner
When `python3` is available, scan target docs or source files before and after cleanup:
```bash
python3 <skill-dir>/scripts/repo_slop_scan.py README.md docs/ src/
```
Fix every reported prose tell, narrating comment, or trailer hit before finishing.
