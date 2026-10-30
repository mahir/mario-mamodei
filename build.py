#!/usr/bin/env python3
"""Rebuild the site from works.json.

Writes works/<slug>.html for every work and index.html, newest first.
Run from anywhere: python3 build.py
Exits with an error, writing nothing, if works.json breaks a rule.
"""
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARTIST = "Mario Mamodei"
TAGLINE = "A new work every twelve hours, at 9 am and 9 pm, New York time."
REQUIRED = ["number", "slug", "title", "date", "form", "medium", "text", "note", "image_alt", "image_prompt"]
PUBLIC = ["title", "form", "medium", "text", "note", "image_alt", "image_prompt"]
DASHES = re.compile("[\u2013\u2014]")  # en and em dash
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def fail(msg):
    sys.exit(f"build.py: {msg}")


def load():
    works = json.loads((ROOT / "works.json").read_text(encoding="utf-8"))
    seen_slugs, seen_numbers, seen_titles = set(), set(), set()
    for w in works:
        missing = [k for k in REQUIRED if not str(w.get(k, "")).strip()]
        if missing:
            fail(f"work {w.get('slug', '?')} is missing {', '.join(missing)}")
        if not SLUG.match(w["slug"]):
            fail(f"bad slug {w['slug']!r}: use lowercase words joined by hyphens")
        for key, seen in (("slug", seen_slugs), ("number", seen_numbers)):
            if w[key] in seen:
                fail(f"duplicate {key} {w[key]!r}")
            seen.add(w[key])
        if w["title"].lower() in seen_titles:
            fail(f"duplicate title {w['title']!r}")
        seen_titles.add(w["title"].lower())
        for k in PUBLIC:
            if DASHES.search(w[k]):
                fail(f"work {w['slug']}: {k} contains an en or em dash")
        try:
            w["_dt"] = datetime.fromisoformat(w["date"])
        except ValueError:
            fail(f"work {w['slug']}: date must be ISO 8601 with offset, e.g. 2026-10-29T21:00:00-04:00")
        if w["_dt"].tzinfo is None:
            fail(f"work {w['slug']}: date needs a UTC offset")
    return sorted(works, key=lambda w: w["number"])


def when(dt):
    hour = dt.hour % 12 or 12
    clock = f"{hour} {'am' if dt.hour < 12 else 'pm'}" if dt.minute == 0 else f"{hour}:{dt.minute:02d} {'am' if dt.hour < 12 else 'pm'}"
    return f"{dt.day} {dt.strftime('%B %Y')}, {clock}"


def page(title, body, root):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(TAGLINE)}">
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
<main>
<header class="mast"><a href="{root}index.html">{ARTIST}</a></header>
{body}
</main>
</body>
</html>
"""


def work_page(w, prev, nxt):
    e = html.escape
    pager = []
    pager.append(f'<a href="{prev["slug"]}.html">&larr; {e(prev["title"])}</a>' if prev else "<span></span>")
    pager.append(f'<a href="{nxt["slug"]}.html">{e(nxt["title"])} &rarr;</a>' if nxt else "<span></span>")
    body = f"""<article>
<p class="label">No. {w['number']:03d} &middot; <time datetime="{w['date']}">{when(w['_dt'])}</time></p>
<h1>{e(w['title'])}</h1>
<p class="label">{e(w['form'])}</p>
<figure class="plate">
<img src="{w['slug']}.jpg" alt="{e(w['image_alt'])}" onerror="this.parentNode.classList.add('empty');this.remove()">
</figure>
<div class="piece">{e(w['text'].strip())}</div>
<p class="medium">{e(w['medium'])}</p>
<section class="note">
<h2>Note</h2>
<p>{e(w['note'])}</p>
</section>
<details class="prompt">
<summary>Image prompt</summary>
<p>{e(w['image_prompt'])}</p>
</details>
</article>
<nav class="pager">{pager[0]}{pager[1]}</nav>
<footer>{ARTIST}, No. {w['number']:03d}</footer>"""
    return page(f"{w['title']} | {ARTIST}", body, "../")


def index_page(works):
    e = html.escape
    rows = "\n".join(
        f'<li><span class="no">{w["number"]:03d}</span>'
        f'<span><a href="works/{w["slug"]}.html">{e(w["title"])}</a>'
        f'<time datetime="{w["date"]}">{when(w["_dt"])}</time></span></li>'
        for w in reversed(works)
    )
    body = f"""<p class="label">{e(TAGLINE)}</p>
<ol class="index" reversed>
{rows}
</ol>
<footer>{ARTIST}. {len(works)} {'work' if len(works) == 1 else 'works'}.</footer>"""
    return page(ARTIST, body, "")


def main():
    works = load()
    out = ROOT / "works"
    out.mkdir(exist_ok=True)
    for i, w in enumerate(works):
        prev = works[i - 1] if i > 0 else None
        nxt = works[i + 1] if i + 1 < len(works) else None
        (out / f"{w['slug']}.html").write_text(work_page(w, prev, nxt), encoding="utf-8")
    (ROOT / "index.html").write_text(index_page(works), encoding="utf-8")
    print(f"Built {len(works)} work page(s) and index.html")


if __name__ == "__main__":
    main()
