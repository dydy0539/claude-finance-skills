# Claude Skills — Equity Research

Custom Claude Code / Cowork skills for US telecom equity research, plus a reusable PDF formatter that any future sector skill can build on.

## Contents

| Skill | Role |
|---|---|
| `analysis-snapshot-pdf/` | Reusable PDF formatter — block-based renderer (card / sections / numbered / table). Owns all typography. Other analysis skills invoke this one to save their output as a polished PDF. |
| `telecom-provider-analysis/` | Single-company operational snapshot for the US Big 5 (T, VZ, TMUS, CMCSA, CHTR). Step 6 saves a PDF via `analysis-snapshot-pdf`. |
| `industry-competitive-positions/` | Cross-provider comparison + industry view. Step 5 saves a PDF via `analysis-snapshot-pdf`. |

The pattern is intentionally factored: domain skills decide *what to say* and *where the file lives*; the PDF skill owns *how it's typeset*. Adding a new sector (banks, retail, energy, etc.) just means writing a new domain skill that emits the same block schema — no formatting code is duplicated.

## Deploy

The Cowork plugin manager periodically reconciles the live `skills/` directory against its manifest and can wipe folders that aren't recognized. So we treat the live plugin folder as a **deployment target**, not a source of truth — the source of truth lives in this repo, and we re-deploy on demand.

```bash
./deploy.sh
```

The script copies (with rsync semantics — overwrites) the three skills into your local plugin directory. Defaults to:

```
~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/<UUID>/<UUID>/skills/
```

If the path is different on your machine (e.g. UUIDs change after a reinstall), set `CLAUDE_SKILLS_DIR` first:

```bash
CLAUDE_SKILLS_DIR="/path/to/your/skills/" ./deploy.sh
```

## Sync

Push to GitHub for cloud backup + cross-machine availability:

```bash
git remote add origin git@github.com:<your-username>/<your-repo>.git
git branch -M main
git push -u origin main
```

On a fresh Mac:

```bash
git clone git@github.com:<your-username>/<your-repo>.git
cd <your-repo>
./deploy.sh
```

## Editing workflow

1. Edit the skill files in this repo (`_claude-skills/`)
2. `./deploy.sh` to push them into the live plugin folder
3. Test in a Cowork session
4. `git add` / `git commit` / `git push` when satisfied

That way the repo stays the canonical version even when the live plugin folder gets clobbered by Cowork updates.

## Notes

- The repo lives inside an iCloud-synced workspace folder. Pushing to GitHub promptly is the safest pattern; long-lived uncommitted changes inside `.git` under iCloud is a known-flaky combination, especially for repos with many small object files.
- If you'd rather host the repo outside iCloud, just `mv` the `_claude-skills/` directory anywhere else and update the deploy script's expected path (the script doesn't care where the repo lives).
