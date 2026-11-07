# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository state

Plain static HTML/CSS portfolio for art director Sako Tenz, migrated from the Wix site https://sakotvildiani.wixsite.com/my-site-2. No build system, package manager, JS, tests, or linter — edit the HTML files directly.

- `index.html` — home grid of project cards (hand-written card list; looping muted preview videos).
- `<slug>/index.html` — one folder per page, slugs match the old Wix URLs (`about-sako`, `truly-destroyed`, `hidden-portraits`, `make-room-4-love`, `greenforce`, `tedx-tbilisi-2023-event`, `classic-that-shouldnt-be`, `europebet`). Subpages reference assets with `../`.
- `assets/css/style.css` — single shared stylesheet (fonts: Space Mono + Barlow from Google Fonts).
- `assets/img/`, `assets/video/` — media downloaded from Wix CDN, filenames keep Wix media IDs. `*_c.*` = cropped variant matching the Wix framing. Preview videos are 720p MP4; keep every file under GitHub's 100 MB limit.
- Media rows in project pages use `.row > .cell` with inline `flex`/`aspect-ratio` = image aspect ratio (justified rows).
- Full-length videos for hidden-portraits, make-room-4-love and truly-destroyed are Vimeo embeds (IDs 831532022, 798723245, 838250301) that are domain-restricted on Vimeo; they only play once the Vimeo owner allows the GitHub Pages domain.
- All links must stay relative (site is served under a sub-path, see below).
- File header comment: `Created by Vitor Venturin on DD/MM/YYYY.` — no company/copyright line.

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
