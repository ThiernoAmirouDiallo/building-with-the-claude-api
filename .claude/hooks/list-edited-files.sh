#!/usr/bin/env bash
# SessionStart hook (matcher: compact): hand Claude the list of repo files edited
# this session, so it can show it in chat right after a compaction. Hook output
# itself isn't drawn in the app, but a reply from Claude is.
# Needs jq, skips quietly without it.
command -v jq >/dev/null || exit 0
f=$(jq -r '.transcript_path // empty')
[ -f "$f" ] || exit 0
dir=${CLAUDE_PROJECT_DIR:-$PWD}

files=$(jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use" and (.name=="Edit" or .name=="Write" or .name=="NotebookEdit")) | (.input.file_path // .input.notebook_path) // empty' "$f" \
  | sort -u | sed "s|^$dir/||" | grep -v '^/')
[ -n "$files" ] || exit 0

jq -n --arg files "$files" '{
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: ("The conversation was just compacted. Files edited in this session (repo-relative):\n" + $files + "\n\nIn your next reply, start by showing the user this list under the heading \"Files edited this session\", then answer what they asked.")
  }
}'
