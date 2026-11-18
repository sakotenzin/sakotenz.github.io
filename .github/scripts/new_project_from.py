#
#  new_project_from.py
#  sakotenz.github.io
#
#  Created by Vitor Venturin on 18/11/2026.
#
#  Copies a project (post) to a new post with a new title. Run by
#  .github/workflows/new-project-from.yml, triggered from the "New project from this"
#  button in Pages CMS. Reads the Pages CMS payload (JSON) from the PAYLOAD env var:
#    context.path   source post, e.g. _posts/2023-04-01-greenforce.md
#    inputs.title   title of the new project
#    inputs.hidden  true = keep the copy off the home grid until it is ready
#  Writes _posts/<today>-<slug>.md and prints its path. The page address is /<slug>/, so the
#  slug must be unique across all posts (any date); a number is appended when it is taken.
#  Front matter is edited as text so everything else stays exactly as in the source:
#  `title` and `card.title` get the new title, `hidden` is set, and `page_title` and
#  `description` (specific to the source project) are dropped.
#

import datetime
import json
import os
import re
import sys
import unicodedata

POSTS = "_posts"
DROP = ("page_title", "description")


def fail(message):
    print(f"::error::{message}")
    sys.exit(1)


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60].strip("-")


def yaml_string(text):
    return json.dumps(text, ensure_ascii=False)  # a JSON string is a valid YAML string


def post_slug(filename):
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", filename[:-3])


payload = json.loads(os.environ.get("PAYLOAD") or "{}")
source = ((payload.get("context") or {}).get("path") or "").strip()
inputs = payload.get("inputs") or {}
title = str(inputs.get("title") or "").strip()
hidden = inputs.get("hidden", True)
if isinstance(hidden, str):
    hidden = hidden.strip().lower() not in ("false", "0", "no", "")
hidden_line = f"hidden: {'true' if hidden else 'false'}"

if not re.fullmatch(POSTS + r"/[A-Za-z0-9._-]+\.md", source) or not os.path.isfile(source):
    fail(f"Source must be an existing post in {POSTS}/, got {source!r}")
if not title:
    fail("A title for the new project is required")
slug = slugify(title)
if not slug:
    fail(f"The title {title!r} has no letters or digits to build the page address from")

text = open(source, encoding="utf-8").read()
match = re.match(r"---\n(.*?\n)---\n?", text, re.S)
if not match:
    fail(f"{source} has no front matter")
front, body = match.group(1), text[match.end():]

out, in_card, skipping, saw_title, saw_hidden = [], False, False, False, False
for line in front.splitlines():
    top_key = re.match(r"^([A-Za-z_]+):", line)
    if skipping and not top_key:
        continue  # continuation lines of a dropped multi-line value
    skipping = False
    if top_key:
        key = top_key.group(1)
        in_card = key == "card"
        if key in DROP:
            skipping = True
            continue
        if key == "title":
            line, saw_title = f"title: {yaml_string(title)}", True
        elif key == "hidden":
            line, saw_hidden = hidden_line, True
    elif in_card and re.match(r"^  title:", line):
        line = f"  title: {yaml_string(title)}"
    out.append(line)
if not saw_title:
    out.insert(0, f"title: {yaml_string(title)}")
if not saw_hidden:
    out.insert(1, hidden_line)

taken = {post_slug(f) for f in os.listdir(POSTS) if f.endswith(".md")}
final_slug, n = slug, 2
while final_slug in taken:
    final_slug, n = f"{slug}-{n}", n + 1

target = f"{POSTS}/{datetime.date.today().isoformat()}-{final_slug}.md"
with open(target, "w", encoding="utf-8") as f:
    f.write("---\n" + "\n".join(out) + "\n---\n" + body)
print(target)
