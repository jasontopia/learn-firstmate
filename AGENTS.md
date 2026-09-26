# Project agent memory

This file is the project's committed home for project-intrinsic agent knowledge: build, test, release, architecture, and sharp-edge notes that should travel with the code.

## What this repo is

A pure documentation repo: a Chinese-language tutorial teaching newcomers how to use FirstMate, one chapter per feature, each chapter ending in a hands-on exercise the reader runs against a live FirstMate session. No build system, dependency manifest, test framework, or package manager - do not add one. `README.md` owns the chapter roadmap; chapters live in `chapters/NN-slug.md`.

## Writing rules

- Write in Chinese. Give the English term alongside the Chinese one on first use (船长 / captain, 大副 / firstmate, 船员 / crewmate), then use Chinese only.
- Every statement about how FirstMate behaves must be traceable to an authoritative tracked file in the local FirstMate checkout, read in this priority order: `AGENTS.md` (the firstmate supervisor contract), `README.md`, the relevant file under `docs/`, then the header comment of the relevant `bin/` script. Do not describe FirstMate behavior from memory or inference - if it has no source there, leave it out.
- That checkout is READ-ONLY. Never write to it or run a state-changing command in it.
- `data/`, `state/`, `config/`, `projects/`, and `.no-mistakes/` in that checkout are captain-private. Never use their contents as tutorial material, and never put a captain's local absolute path into this repo.
- Diagrams are ASCII inside a Markdown code block. No drawing dependencies.
- Exercises must be read-only or safely reversible - never have the reader mutate someone else's repo or take an unrecoverable action.

## Docs check

`scripts/check-docs.py` is the repo's only check. It is stdlib-only python3 and
takes an optional root argument. It owns the definition of both rule families
(relative link integrity, and the formatting-hygiene rules); read the script
rather than restating its rules here. Run it before pushing:

```
python3 scripts/check-docs.py
```

It is pinned as the canonical command in `.no-mistakes.yaml`, so the local gate
and GitHub CI run the same thing.

## The CI workflow is generated, not hand-written

`.github/workflows/ci.yml` comes from `no-mistakes ci-workflow`, which reads the
commands pinned in `.no-mistakes.yaml`. Change the command there and regenerate
with `no-mistakes ci-workflow --force` instead of editing the workflow.

Sharp edge: that generator unconditionally emits an `actions/setup-go` step with
`go-version-file: go.mod`. This repo has no `go.mod`, so the step fails every
run and has to be removed again after each regeneration. A comment at that spot
in the workflow records this.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
