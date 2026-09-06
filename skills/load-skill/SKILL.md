---
name: load-skill
description: Browse the wilbeibi-skills catalog, use a skill that is not installed here, or link one into this host or this project. Fetches from GitHub when there is no local checkout. Use when a task fits a skill you have heard of but no installed skill fires, when asked to use a skill by name that is not installed, or before writing a new skill to check for an existing one.
---

# load-skill

The repo holds every skill; nothing says which host or project gets which. That is decided
here, on this machine, by what is linked. One command to see the catalog, one to use a skill
once, one to keep it.

## Commands

```bash
scripts/load_skill.py list                 # every skill: name, description; * = global here, + = this project
scripts/load_skill.py list chart           # substring filter over name + description
scripts/load_skill.py get sketch-concept   # prints .../sketch-concept/SKILL.md, then its other files
scripts/load_skill.py link sketch-concept  # make it global on this host (asks nothing; undo with unlink)
scripts/load_skill.py link -p dataviz      # this project only: ./.agents/skills + ./.claude/skills
scripts/load_skill.py sync                 # after git pull: repair links across agent dirs
```

After `get`, read the printed `SKILL.md` and follow it; paths inside are relative to its directory.
Prefer `get` for a one-off and `link -p` when a project will keep needing the skill; `link`
without `-p` only when the user asks for it on this host.

## Notes

- A row starting with `*` or `+` is already installed; call it directly instead.
- Inside a checkout reads are local and instant. Elsewhere the repo tarball is cached under
  `~/.cache/load-skill` for 24h; `--refresh` forces a re-download, `--remote` ignores a checkout.
- `list` exits 1 when the query matches nothing, so retry without the query rather than guessing a name.
- Project links are symlinks into the checkout; whether they are committed or ignored is the project's call.
- `LOAD_SKILL_REPO` / `LOAD_SKILL_REF` point at another repo or branch.
