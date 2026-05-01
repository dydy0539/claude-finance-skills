#!/usr/bin/env bash
# Deploy the three skills in this repo into Cowork's live plugin skills directory.
# Re-run after any Cowork update that wipes locally-added skills.
#
# Usage:
#   ./deploy.sh                          # uses default path
#   CLAUDE_SKILLS_DIR=/path ./deploy.sh  # override target
set -euo pipefail

REPO_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Default path matches the Cowork research-preview layout on macOS. Override
# CLAUDE_SKILLS_DIR if your UUIDs differ (e.g. after a reinstall) or you're
# on a different OS.
DEFAULT_DIR="$HOME/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/237904b0-4b8a-4990-b342-322a8dfc4dfc/4568f1d2-ca54-4e8b-aec8-bccca75d54d4/skills"
TARGET="${CLAUDE_SKILLS_DIR:-$DEFAULT_DIR}"

if [[ ! -d "$TARGET" ]]; then
  echo "ERROR: target skills dir does not exist: $TARGET" >&2
  echo "Set CLAUDE_SKILLS_DIR to the right path and retry." >&2
  echo "" >&2
  echo "To find it on macOS, run:" >&2
  echo "  find \"\$HOME/Library/Application Support/Claude\" -name SKILL.md -path '*telecom-provider-analysis*' 2>/dev/null" >&2
  exit 1
fi

SKILLS=( analysis-snapshot-pdf telecom-provider-analysis industry-competitive-positions earnings-analysis )

echo "Deploying from: $REPO_DIR"
echo "          into: $TARGET"
echo ""

for skill in "${SKILLS[@]}"; do
  src="$REPO_DIR/$skill"
  dst="$TARGET/$skill"
  if [[ ! -d "$src" ]]; then
    echo "  skip $skill (not in repo)"
    continue
  fi
  rm -rf "$dst"
  cp -R "$src" "$dst"
  echo "  ✓ $skill"
done

echo ""
echo "Done. Restart your Cowork session for changes to take effect."
