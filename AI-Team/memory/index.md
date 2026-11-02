# Memory Index

Read this index first, then load 1-3 relevant files per task.
Never load all memory files by default.

| Category | File | When to read |
| --- | --- | --- |
| User preferences | `user-preferences.md` | Communication, output, or interaction preferences |
| Tech stack | `tech-stack.md` | Technology selection, build, compatibility |
| Completion criteria | `completion-criteria.md` | Defining acceptance or delivery boundaries |
| Feedback patterns | `feedback-patterns.md` | Handling recurring user feedback |
| Defect patterns | `defect-patterns.md` | Debugging or regression risk |
| Effective solutions | `effective-solutions.md` | Reusable implementation or troubleshooting |
| Technical decisions | `technical-decisions.md` | Architecture, dependencies, tradeoffs |
| Project history | `project-history.md` | Modifying existing projects or restoring context |

Each entry max 300 chars; each file max 40 entries and 8,000 chars.
When either limit is reached, merge duplicates and compress the oldest entries,
keeping still-valid conclusions. Only record new, stable lessons;
do not invoke a model just to update memory.

When the project is complete or the team is about to be carried away,
AgentA compresses the project summary into `project-history.md`
and updates other categories as needed. Only carry stable, reusable
conclusions. Never record business source code, secrets, raw logs,
build artifacts, or project dependencies.

**Credential lookup rule (2026-10-30, after recurring misplacement):** When the user says "记下来/按规定放" about any account+password (database / Windows / LLM / web login), the ONLY correct target is `credentials.md` (authoritative) + `团队经验速查手册.md` §11 (mirror). Do NOT write to `.env` (runtime config only), tickets, README, or chat. Search both `Portable-AI-Team/` AND `Portable-AI-TeamV3.0/` before concluding a team file doesn't exist.
**Important:** Never commit `credentials.md`, API keys, or any plaintext
passwords to version control. Sensitive credentials must stay in
`LLM配置.json` (git-ignored) and be rotated immediately if exposed.

