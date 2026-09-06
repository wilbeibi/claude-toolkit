# wilbeibi-skills

> A trillion-parameter brain to wash my digital dishes.

22 agent skills for **Claude Code** and **Codex**: code review, test writing, documentation, pre-coding planning, codebase onboarding, evidence-driven investigation, repo health evaluation, research paper search, skill authoring, data visualization, hand-drawn technical illustration, browser history recall, macOS automation, and Obsidian note capture and search. Each is a single `SKILL.md` your agent loads on demand; install one with `npx skills`, or clone the repo and let [load-skill](skills/load-skill/SKILL.md) pull in whatever the current host or project needs.

```bash
npx skills add wilbeibi/wilbeibi-skills --skill '*'
```

## Skills

| Skill | Description |
|-------|-------------|
| [load-skill](skills/load-skill/SKILL.md) | Browse this catalog from any directory, use a skill once without installing it, or link it into the host or the current project; fetches from GitHub when there is no checkout. |
| [obsidian-search](skills/obsidian-search/SKILL.md) | Search an Obsidian vault three-tier: Meilisearch for topic/fuzzy queries, ripgrep for exact matches, date-aware helper for natural-language dates and tasks. |
| [obsidian-capture](skills/obsidian-capture/SKILL.md) | Append quick todos (with due dates), log lines, learnings, and reflections to the right section of Obsidian daily and weekly notes; run the separate `#agent-todo` queue. |
| [test-writing](skills/test-writing/SKILL.md) | Guide effective, maintainable test writing. |
| [newcomer-lens-review](skills/newcomer-lens-review/SKILL.md) | Review code for missing context, onboarding gaps, and undocumented assumptions. |
| [code-review](skills/code-review/SKILL.md) | Review a diff, package, or API through one of three lenses — necessity and layering (Russ Cox), invariant and cost honesty (BurntSushi), or product-versus-library fit (Mitsuhiko). |
| [complexity-budget](skills/complexity-budget/SKILL.md) | Explicit-only review of ownership, coupling, and value before a substantial design change. |
| [grill-me](skills/grill-me/SKILL.md) | Explicit-only design interview, one question at a time; capture durable terminology and decisions when useful. |
| [questionnaire](skills/questionnaire/SKILL.md) | Batch a long discussion's open decisions into an offline HTML questionnaire (branching, autosaved drafts) whose answers come back as markdown keyed by stable question ids. |
| [write-skill](skills/write-skill/SKILL.md) | Write compact shared skills for Codex, Claude Code, and Pi; isolate harness-specific behavior. |
| [skill-curator](skills/skill-curator/SKILL.md) | Audit and de-duplicate an existing skill library — forked scripts, contradictory instructions, bloat, internal defects. |
| [write-docs](skills/write-docs/SKILL.md) | Write or critique codebase prose — READMEs, developer guides and runbooks, CLI text, comments, agent guides, and commit/PR descriptions — with an advisory clarity checker. |
| [show-me](skills/show-me/SKILL.md) | Answer with a compact visual — call tree, component tree, file tree, pseudocode, type signature, diff, or Mermaid — instead of a wall of prose. Adapted from [humanlayer/skills](https://github.com/humanlayer/skills). |
| [dataviz](skills/dataviz/SKILL.md) | Turn real measurements into evidence-first editorial charts for benchmarks, performance comparisons, technical articles, reports, and READMEs. |
| [sketch-concept](skills/sketch-concept/SKILL.md) | Generate a hand-drawn illustration that explains one technical mechanism as a small physical world — metaphor, palette, and prompt skeleton, plus a meaning/legibility/coherence check on the draft. |
| [grok-repo](skills/grok-repo/SKILL.md) | Understand an unfamiliar codebase through a full briefing, scoped dataflow trace, or reconstruction of why and how a feature changed. |
| [sherlock](skills/sherlock/SKILL.md) | Work an open question like a case: log graded clues, run competing theories through a consistency matrix, kill by evidence, backtrack, converge — for puzzling bugs, reverse-engineering a product from public signals, or "what happened here". |
| [repo-eval](skills/repo-eval/SKILL.md) | Score a public GitHub repo on momentum (popularity trajectory) and maintenance (how well it is run) via the OSS Insight API and `gh`. |
| [paper-search](skills/paper-search/SKILL.md) | Find papers across Semantic Scholar, OpenAlex, and arXiv, ranked by impact relative to field and age — so recent work and credible work are told apart from noise. |
| [web-recap](skills/web-recap/SKILL.md) | Extract browser history (Chrome, Firefox, Safari, Edge, Brave) to find URLs by topic or get visit stats. Adapted from [robzolkos/web-recap](https://github.com/robzolkos/web-recap). |
| [karpathy-planning](skills/karpathy-planning/SKILL.md) | Explicit-only implementation planning: scope, material assumptions, and verifiable completion. |
| [hammerspoon](skills/hammerspoon/SKILL.md) | Operate macOS via Hammerspoon: one-off `hs -c` Lua for apps, browser tabs, and system toggles, plus authoring persistent automations in ~/.hammerspoon. |

## Install

Two ways. `npx skills` copies one or all skills into place, per the usual conventions:

```bash
npx skills add wilbeibi/wilbeibi-skills --skill test-writing
npx skills add wilbeibi/wilbeibi-skills --skill '*'
```

Or keep one clone and decide per host and per project what to link. The repo does not record which
machine has which skills; that lives only in the symlinks on each machine.

```bash
git clone https://github.com/wilbeibi/wilbeibi-skills ~/src/wilbeibi-skills
lsk=~/src/wilbeibi-skills/skills/load-skill/scripts/load_skill.py
$lsk link load-skill                # the only skill worth linking everywhere
$lsk link code-review write-docs    # global on this host: ~/.agents/skills + Claude/Codex/Pi/Hermes dirs
cd ~/some/project && $lsk link -p dataviz   # this project only: ./.agents/skills, ./.claude/skills
$lsk list                           # * global here, + this project, blank = loadable on demand
$lsk get sketch-concept             # path to use a skill once; installs nothing
```

With `load-skill` linked, an agent working anywhere can `list` the catalog, `get` a skill for one task,
or `link -p` it for the project, without touching the global set. `get` also works with no clone at all:
it fetches a tarball of `main` and caches it for a day.

## Update

```bash
bin/skills-sync        # git pull --ff-only, then repair the agent-dir links; policy stays on the host
npx skills update      # for skills installed via npx
```

## Layout

Each skill lives in `skills/<name>/SKILL.md`. Supporting scripts and reference docs are colocated in the same directory.

## Validation

Check skill frontmatter and script tests before pushing (CI runs the same):

```bash
uv run scripts/check_skill_frontmatter.py
python3 skills/load-skill/scripts/test_load_skill.py
```
