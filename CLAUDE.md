# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository state

Jekyll portfolio/blog for art director Sako Tenz, migrated from the Wix site https://sakotvildiani.wixsite.com/my-site-2. GitHub Pages builds it with Jekyll (`github-pages` gem). The Jekyll structure follows Vitor's own portfolio (`vitorventurin.github.io`), but the UI does not: there is no Bootstrap or Freelancer theme here. The look is Sako's own markup + `assets/css/style.css`.

- `_config.yml` — site settings (title, tagline, email, description), home filter pills, `home_sections` (order and grid style of the home sections), kramdown options, post defaults.
- `_posts/YYYY-MM-DD-<slug>.md` — one post per project. Served at `/<slug>/` (`permalink: /:title/`), which keeps the old Wix URLs. Front matter:
  - `title`, `page_title` (optional `<title>`), `label`, `subtitle` (optional), `description` (optional meta)
  - `section` (`featured` | `work` | `tedx` | `closing`; default `work`) + `order` (default 99) — where the card sits on the home page
  - `link` (default `true`; `false` = card is not clickable, the project page is not written yet)
  - `card:` `label`, `title`, then `video` + `poster` (looping preview) or `image` + `width` + `height`; optional `soon: true` (COMING SOON badge)
- Post body is Markdown with these includes:
  - `{% include row.html media="a.jpg 1920x1280 | b.webp 839x596 Alt text | c.mp4 1920x1080 cf001.jpg" %}` — justified media row (`.row > .cell` with flex/aspect-ratio computed from the dimensions). Video items: file, dimensions, poster.
  - `{% include vimeo.html id="…" %}`, `{% include player.html src="file.mp4" %}`
  - Style hooks via kramdown IAL: `## Text` + `{: .statement}`, `### Text` + `{: .section-label}`, paragraph + `{: .kicker}` / `{: .credits}`, list + `{: .awards}`. Raw HTML is fine for one-offs (`.stats`, `.press`); use `{{ site.baseurl }}/assets/…` for paths in it.
- `_data/press.yml` — press cards on the home page (external links open in a new tab; paths starting with `/` are internal).
- `index.html` — home page (loops over `home_sections`); `about-sako.html` — about page (`/about-sako/`).
- `_layouts/default.html` (shell), `_layouts/post.html` (project page). `_includes/`: `head`, `header`, `footer`, `card`, `row`, `vimeo`, `player`.
- `assets/css/style.css` — single shared stylesheet (fonts: Space Mono + Barlow from Google Fonts). Project body elements must stay direct children of `article.project` (CSS uses `.project > p`).
- `assets/img/`, `assets/video/` — media downloaded from Wix CDN, filenames keep Wix media IDs. `*_c.*` = cropped variant matching the Wix framing. Preview videos are 720p MP4; keep every file under GitHub's 100 MB limit.
- Full-length videos for hidden-portraits, make-room-4-love and truly-destroyed are Vimeo embeds (IDs 831532022, 798723245, 838250301) that are domain-restricted on Vimeo; they only play once the Vimeo owner allows the GitHub Pages domain.
- Links: never hard-code `/` paths. Use `| relative_url` in layouts/includes and `{{ site.baseurl }}` in raw HTML inside posts. `url`/`baseurl` are left unset in `_config.yml`; GitHub Pages fills them in (jekyll-github-metadata), so the site works as a project site (`/sakotenz.github.io/`), a user site or a custom domain.
- kramdown is set to keep straight quotes and `...` as typed (`smart_quotes`, `typographic_symbols`).
- File header comment `Created by Vitor Venturin on DD/MM/YYYY.` goes on code files only (layouts, includes, config, CSS, scripts) — no company/copyright line. Content files (`_posts`, `_data`, `index.html`, `about-sako.html`) carry no author signature.

## Branches

- `main` — published by GitHub Pages.
- `develop` — Jekyll/blog work in progress; merge into `main` to publish.

## GitHub Pages setup

Reference: https://docs.github.com/en/pages/quickstart

- Remote: `git@github-personal:sakotenzin/sakotenz.github.io.git` (SSH alias for the personal key). Repo is owned by personal account `sakotenzin`.
- User site (served at root URL) requires repo name `<owner>.github.io`. Current name `sakotenz.github.io` ≠ `sakotenzin.github.io`, so until renamed it publishes as a project site at `https://sakotenzin.github.io/sakotenz.github.io/`.
- Publishing source (Settings → Pages → Build and deployment): "Deploy from a branch" with `main` and folder `/(root)`.
- Pages settings and repo renames can only be done by the repo owner (collaborators on personal-account repos have write access only).
- Do not add `.nojekyll` — the site needs Jekyll.
- Changes can take up to 10 minutes to appear after pushing.

## Local preview

- `bundle install`, then `bundle exec jekyll serve` → http://localhost:4000/ (or `./build.sh` for a one-off build into `_site/`, which is git-ignored).
- To test the sub-path: `bundle exec jekyll serve --baseurl /sakotenz.github.io`.
- `bundle exec jekyll serve` also enables jekyll-admin at http://localhost:4000/admin for editing posts in a browser. Local only: GitHub Pages serves static files, so `/admin` does not exist on the live site.

## Online editing (Pages CMS)

- Sako edits online at https://app.pagescms.org (GitHub login), branch `main`. Config: `.pages.yml` (projects collection, `_data/press.yml`, media folders `assets/img` + `assets/video`).
- Front matter media values (`card.video/poster/image`, press `image/logo`) must be full paths (`/assets/img/x.jpg`, `/assets/video/x.mp4`): Pages CMS refuses to save a post whose image value doesn't start with the media folder. `card.html`/`head.html` strip the prefix before adding their own, so bare filenames also render. Media inside the body (`row.html`, `player.html`) stays bare filenames.
- Post body uses the raw markdown code editor (not rich-text) so `{% include %}` and `{: .class}` lines survive saves.
- On save Pages CMS rewrites front matter from the `.pages.yml` fields only and drops undeclared keys (no `settings.content.merge`, so clearing a field works). When adding a front matter key, declare it in `.pages.yml` too. It also re-serializes the YAML, so quoting/comments in front matter and `_data/press.yml` can change.
- Restart `jekyll serve` after editing `_config.yml`.
