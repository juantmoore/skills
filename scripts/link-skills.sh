#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [[ $# -eq 0 ]]; then
  TARGETS=("$HOME/.agents/skills" "$HOME/.codex/skills" "$HOME/.claude/skills")
else
  TARGETS=("$@")
fi

for dest in "${TARGETS[@]}"; do
  mkdir -p "$dest"
  for skill in "$ROOT"/skills/*; do
    [[ -f "$skill/SKILL.md" ]] || continue
    name="$(basename "$skill")"
    ln -sfn "$skill" "$dest/$name"
    echo "linked $name -> $dest/$name"
  done
done
