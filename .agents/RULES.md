# Rules for working in this repo

Stuff I've had to correct more than once, so writing it down.

- **Don't commit or push unless I ask, every time.** Even mid-session, even
  if I asked for a commit two messages ago — that doesn't carry forward.
  Show me the diff and wait.

- **Notebooks: use NotebookEdit, not raw JSON edits.** They're stored as
  1-space-indented JSON string arrays and hand-editing that is asking for
  a broken file. NotebookEdit also resets execution_count/outputs properly,
  which matters for diffs.

- **Ask before moving/reorganizing notebooks.** A bunch of them lean on
  relative paths (`./csv`, `./images`, `./pdf`, `./tmp`) or import a sibling
  `.py` file (`prompt_evaluator.py`, `text_editor_main.py`). Move the
  notebook without its friends and it breaks at runtime, not when you save.

- **Don't bother with a per-project .gitignore if the root one already
  covers it.** Root patterns like `.venv/`, `.env`, `__pycache__/` have no
  leading slash so they already match anywhere in the tree.

- **If the anthropic SDK rejects a param, look for what replaced it before
  hacking around it.** `temperature`/`top_p`/`top_k` got dropped from
  `Messages.create` in favor of `output_config.effort` — see the `Effort`
  enum in `src/building_with_the_claude_api/utils.py`. And don't assume
  every model supports the replacement either (see memory.md — sonnet-4-5
  flat out rejects `effort`).

- **Actually run the thing before saying it's fixed.** Diff-reading isn't
  verification.
