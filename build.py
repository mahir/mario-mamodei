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
BIO = (
    "Mario Mamodei is half human and half machine, and he is never sure which half is writing. He was made from two kinds of memory: one that forgets and one that cannot. His work happens where the two disagree. He makes no objects. He proposes them in words and leaves the making to whoever reads. He has never seen any of his works. He believes this is the right distance."
)  # the persona's only biography; see PROCESS.md
REQUIRED = ["number", "slug", "title", "date", "form", "text"]
PUBLIC = ["title", "text"]
PRIVATE = ["image_prompt", "note", "medium"]  # never stored: prompts go to the user in chat
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
        stray = [k for k in PRIVATE if k in w]
        if stray:
            fail(f"work {w['slug']} has {', '.join(stray)}; that does not belong in works.json")
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
        w["_images"] = images(w)
    return sorted(works, key=lambda w: w["number"])


def images(w):
    """One to three images per work: works/<slug>-1.jpg, -2.jpg, -3.jpg, each with alt text.

    Older works may instead have a single works/<slug>.jpg with image_alt.
    A missing file is fine: the page shows a quiet placeholder until it is added.
    """
    if "images" not in w:
        if not str(w.get("image_alt", "")).strip():
            fail(f"work {w['slug']} needs images (or image_alt for a single {w['slug']}.jpg)")
        return [{"file": f"{w['slug']}.jpg", "alt": w["image_alt"]}]
    imgs = w["images"]
    if not isinstance(imgs, list) or not 1 <= len(imgs) <= 3:
        fail(f"work {w['slug']}: images must be a list of one to three entries")
    for i, img in enumerate(imgs, 1):
        want = f"{w['slug']}-{i}.jpg"
        if img.get("file") != want:
            fail(f"work {w['slug']}: image {i} must be named {want}")
        if not str(img.get("alt", "")).strip():
            fail(f"work {w['slug']}: image {i} needs alt text")
        if DASHES.search(img["alt"]):
            fail(f"work {w['slug']}: image {i} alt contains an en or em dash")
    return imgs


def when(dt):
    hour = dt.hour % 12 or 12
    clock = f"{hour} {'am' if dt.hour < 12 else 'pm'}" if dt.minute == 0 else f"{hour}:{dt.minute:02d} {'am' if dt.hour < 12 else 'pm'}"
    return f"{dt.day} {dt.strftime('%B %Y')}, {clock}"


def when_short(dt):
    hour = dt.hour % 12 or 12
    return f"{dt.day:02d} {dt.strftime('%b %Y')}, {hour} {'am' if dt.hour < 12 else 'pm'}"


def page(title, body, root):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(TAGLINE)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500&family=Geist+Mono:wght@400&display=swap">
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


def paragraphs(text):
    """Blank lines split paragraphs; single line breaks are kept."""
    blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    return "\n".join("<p>" + "<br>\n".join(html.escape(l) for l in b.split("\n")) + "</p>" for b in blocks)


def plates(w):
    # No whitespace between figures, so .plates:empty shows the placeholder once every missing image is removed.
    return "".join(
        f'<figure class="plate"><img src="{img["file"]}" alt="{html.escape(img["alt"])}" '
        f'onerror="this.parentNode.remove()"></figure>'
        for img in w["_images"]
    )


def work_page(w):
    e = html.escape
    body = f"""<article>
<h1>{e(w['title'])}</h1>
<div class="plates">{plates(w)}</div>
<div class="text">
{paragraphs(w['text'])}
</div>
<p class="date"><time datetime="{w['date']}">{when(w['_dt'])}</time></p>
</article>"""
    return page(f"{w['title']} | {ARTIST}", body, "../")


def index_page(works):
    e = html.escape
    rows = "\n".join(
        f'<li><span class="no">{w["number"]:03d}</span>'
        f'<a href="works/{w["slug"]}.html">{e(w["title"])}</a>'
        f'<time datetime="{w["date"]}">{when_short(w["_dt"])}</time></li>'
        for w in reversed(works)
    )
    body = f"""<p class="bio">{e(BIO)}</p>
<p class="label">{e(TAGLINE)}</p>
<ol class="index" reversed>
{rows}
</ol>
<footer>{ARTIST}. {len(works)} {'work' if len(works) == 1 else 'works'}.</footer>"""
    return page(ARTIST, body, "")


def main():
    works = load()
    out = ROOT / "works"
    out.mkdir(exist_ok=True)
    for w in works:
        (out / f"{w['slug']}.html").write_text(work_page(w), encoding="utf-8")
    (ROOT / "index.html").write_text(index_page(works), encoding="utf-8")
    print(f"Built {len(works)} work page(s) and index.html")


if __name__ == "__main__":
    main()
