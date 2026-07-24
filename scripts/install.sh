#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_dir=$(CDPATH= cd -- "$script_dir/.." && pwd)
source_dir="$repo_dir/skills/design-app-icons"
codex_root=${CODEX_HOME:-"$HOME/.codex"}
target_dir="$codex_root/skills/design-app-icons"

if [ ! -f "$source_dir/SKILL.md" ]; then
  echo "error: installable skill not found at $source_dir" >&2
  exit 1
fi

mkdir -p "$target_dir"
cp -R "$source_dir/." "$target_dir/"
echo "Installed design-app-icons at $target_dir"
echo 'Invoke it with: Use $design-app-icons to ...'
