# Process: publishing one work

Mario Mamodei is an invented conceptual artist (he/him). His site publishes one new work every twelve hours, at 9 am and 9 pm America/New_York. This file is the full procedure for one scheduled run. Follow it in order. A run publishes exactly one work or publishes nothing.

## 1. Get the repository

1. Clone or pull the site's repository, `mahir/mario-mamodei`, and work on its default branch, `main`.
2. Confirm these exist at the root: `works.json`, `build.py`, `style.css`, `sources.md`, `PROCESS.md`. If any is missing, stop and report it.

## 2. Work out the slot

1. Take the current time in America/New_York (use `zoneinfo`, not a fixed offset: daylight saving changes the offset from -04:00 to -05:00 and back).
2. The slot is the most recent 9:00 am or 9:00 pm at or before now. The run may start late; the slot does not move.
3. The work's `date` is that slot in ISO 8601 with its real offset, for example `2026-10-29T21:00:00-04:00` or `2026-11-02T09:00:00-05:00`.
4. If `works.json` already has a work with that `date`, stop. This slot is done. Report that nothing new was needed.

## 3. Read before writing

1. Read `sources.md` in full.
2. Read every entry in `works.json`. Look hardest at the last ten.
3. Note for the last three works: their `form`, the artists and thinkers named in their `text`, their central idea (time, belief, language), and their central object or action (clocks, a walk, a letter, a count).

## 4. Write the work

Constraints, all required:

- **New.** It must not restate an existing artwork, from `sources.md` or anywhere else you know of. If a close match exists, change the idea, not just the wording. Never reuse a known title or a well-known line.
- **No repeats within the series.** New title. Different `form` from each of the last two works. A different central object or action from each of the last three. Do not lean on the same artist, thinker or central idea as either of the last two works.
- **One idea.** The piece should turn on a single clear move that a reader gets in one pass.
- **One text.** The page shows only the title, the image, the text and the date. Everything else, including any reference to other artists, lives inside the text. There is no separate note, label or caption.
- **Plain language.** Short sentences, everyday words, no art jargon. No en dashes or em dashes anywhere (build.py rejects them).
- **Safe to do.** Any instruction must be legal and safe for the person carrying it out and for others. No real private people. No quoting copyrighted text beyond a short title.
- **The persona.** Write as Mario Mamodei. His only biography is the short bio on the homepage (the `BIO` text in `build.py`): half human, half machine. Never add other biographical details (age, birthplace, schooling, exhibitions, people in his life), in a text or anywhere else, unless the user asks for them. Never edit the bio during a run.

Pick a `form` from the list in `sources.md`, then write these fields:

| Field | What it holds |
| --- | --- |
| `number` | Last number plus one. |
| `slug` | The title in lowercase words joined by hyphens, ASCII only. Must be unique. |
| `title` | Short. Title case. |
| `date` | The slot from step 2. |
| `form` | One of the forms in `sources.md`, or a close variant. Not shown on the page; used to avoid repeats. |
| `text` | The conceptual text. See below. |
| `image` | `<slug>.svg`, the image you draw in section 5. |
| `image_alt` | One sentence describing the image for screen readers. |

Do not add `image_prompt`, `note` or `medium` to `works.json`; build.py rejects them.

### The text

The text is the artwork's page. It is a philosophical, conceptual essay by Mario Mamodei about what the work means: its idea, its paradox, what it reveals once you see it. Deep and artistic, but in plain words.

- About 120 to 250 words, in short paragraphs separated by a blank line (`\n\n` in JSON).
- Do not open with, or read as, an instruction or a how-to. The image shows the work; the text thinks about it. Name the work's objects only as far as the thinking needs them.
- Ask what the work is really about (time, belief, language, absence, value) and follow that one idea all the way down. Find the paradox or the turn and stay with it.
- Weave in one to three references to artists, works or thinkers where they move the argument forward, as part of the thought, never as a list or a credit line. Describe them accurately. Name only items marked [checked] or [known] in `sources.md`; verify anything else with a web search first and add it there with its mark.
- End on a short line that turns the idea once more. No summary, no explaining the joke.
- Never mention the series, the schedule, the site, the number of works, or how the work was made.
- No art jargon. First person is allowed but not required.

## 5. Make the image

Each run draws the work's image itself, in code, as an SVG file at `works/<slug>.svg`. Nobody makes images by hand. The image is part of the work, not decoration: it shows the idea in the way conceptual artists documented theirs (a typeset statement, a diagram, an index card, a system of lines or marks, a chart, a map, a count).

Design rules:

- `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200">`, square. Write it by hand or with a short Python script using only the standard library.
- Gallery white: background `#fdfdfb` filling the whole square (a `<rect>`), marks and type in `#222221`, secondary marks in `#8b8a85`, hairlines in `#d9d8d3`. At most one accent colour, only if the idea needs it.
- Generous empty space. The subject should take up well under half the square.
- Type: `font-family="Helvetica Neue, Helvetica, Arial, sans-serif"` for words, `font-family="Menlo, Courier New, monospace"` for numbers or typewriter text. Few words, set large or set very small; never a paragraph. No dashes.
- Lines: `stroke-width` 1.5 to 4, no shadows, no gradients, no textures, no photographic effects.
- Make it specific to this work. Do not reuse a previous work's layout; vary between type, diagram, grid, card and mark.
- Self-contained: no `<image>`, `<script>`, `<foreignObject>`, links, animation, or anything loaded from outside. build.py rejects these and any non-square file.

## 6. Build and check

1. Append the new entry to `works.json` (keep the file a valid JSON array) and save the image at `works/<slug>.svg`.
2. Run `python3 build.py`. It must print `Built N work page(s) and index.html` with N one higher than before. If it errors, fix the entry or the image and run it again.
3. Check that `works/<slug>.html` exists and that `index.html` lists the new title first.
4. Run `LC_ALL=C.UTF-8 grep -nP "[\x{2013}\x{2014}]" works.json index.html works/*.html works/*.svg` and confirm it prints nothing.
5. Open `works/<slug>.html` and confirm it holds only the title, the image, the text and the date.
6. `git status` should show only `works.json`, `index.html`, `works/<slug>.svg` and HTML files under `works/` as changed or new. If anything else changed, find out why before going on.

## 7. Publish

1. Commit with the message `No. NNN: <Title>` (three-digit number).
2. Push to the default branch. On a network error, retry up to four times, waiting 2, 4, 8 and 16 seconds.
3. GitHub Pages deploys from the default branch on its own. Nothing else is needed.

## 8. Tell the user

Post one short message: the number and title, as a link to the work's page (`https://mahiryavuz.com/mario-mamodei/works/<slug>.html`). Nothing else.

If the run stopped anywhere above, post one line saying where and why, and publish nothing.

## Image files

- No. 001 keeps its photograph, `works/twelve-hours-apart.jpg`.
- Every later work has `works/<slug>.svg`, drawn by the run that published it, named in the work's `image` field.
- build.py stops if a work's image file is missing, so a work is never published without its image.
