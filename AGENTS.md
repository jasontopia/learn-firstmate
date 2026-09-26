# Project agent memory

This file is the project's committed home for project-intrinsic agent knowledge: build, test, release, architecture, and sharp-edge notes that should travel with the code.

This is a Chinese-language tutorial repo: the deliverable is prose in `README.md`
and `chapters/`, not an application. There is nothing to build and no unit tests.

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
