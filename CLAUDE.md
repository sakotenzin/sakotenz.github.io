# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository state

GitHub Pages site, not yet built: only `README.md` exists. No build system, package manager, tests, or linter. Update this file once a stack (plain HTML, Jekyll, static generator, etc.) is chosen.

## GitHub Pages setup

Reference: https://docs.github.com/en/pages/quickstart

- Remote: `https://github.com/sakotenzin/sakotenz.github.io.git`, default branch `main`. Repo is owned by personal account `sakotenzin`.
- User site (served at root URL) requires repo name `<owner>.github.io`. Current name `sakotenz.github.io` ≠ `sakotenzin.github.io`, so until renamed it publishes as a project site at `https://sakotenzin.github.io/sakotenz.github.io/`. Use relative asset paths so links work under either URL.
- Publishing source (Settings → Pages → Build and deployment): "Deploy from a branch" with `main` and folder `/(root)` or `/docs`, or "GitHub Actions" for a custom workflow. If `/docs` is chosen, deleting that folder breaks the build.
- Pages settings can only be changed by the repo owner (collaborators on personal-account repos have write access only). Contributors can push content; owner must enable Pages.
- GitHub Pages runs Jekyll by default; add an empty `.nojekyll` to disable it (needed if any paths start with `_`).
- Changes can take up to 10 minutes to appear after pushing.

## Local preview

No tooling configured. For plain static files: `python3 -m http.server 8000` from the repo root.
