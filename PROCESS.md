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
3. Note for the last three works: their `form`, the artists named in their `note`, and their central object or action (clocks, a walk, a letter, a count).

## 4. Write the work

Constraints, all required:

- **New.** It must not restate an existing artwork, from `sources.md` or anywhere else you know of. If a close match exists, change the idea, not just the wording. Never reuse a known title or a well-known line.
- **No repeats within the series.** New title. Different `form` from each of the last two works. A different central object or action from each of the last three. Do not lean on the same artist as either of the last two works.
- **One idea.** The piece should turn on a single clear move that a reader gets in one pass.
- **Plain language.** Short sentences, everyday words, no art jargon. No en dashes or em dashes anywhere (build.py rejects them).
- **Safe to do.** Any instruction must be legal and safe for the person carrying it out and for others. No real private people. No quoting copyrighted text beyond a short title.
- **The persona.** Write as Mario Mamodei. Do not invent biography for him (age, birthplace, schooling, exhibitions) unless the user has asked for it.

Pick a `form` from the list in `sources.md`, then write these fields:

| Field | What it holds |
| --- | --- |
| `number` | Last number plus one. |
| `slug` | The title in lowercase words joined by hyphens, ASCII only. Must be unique. |
| `title` | Short. Title case. |
| `date` | The slot from step 2. |
| `form` | One of the forms in `sources.md`, or a close variant. |
| `text` | The work itself: the instruction, score, statement or proposition. Under about 120 words. Use `\n` for line breaks and `\n\n` for a stanza break. |
| `medium` | One wall-label line: materials or means, then "Dimensions variable." or a duration, as fits. |
| `note` | Three to five sentences. What the work does, then which artists or works it descends from and what it changes. Name only items marked [checked] or [known] in `sources.md`. If you want to cite something else, verify it with a web search first and add it to `sources.md` with its mark. |
| `image_alt` | One sentence describing the image for screen readers. |
| `image_prompt` | See section 5. |

## 5. Write the image prompt

The user pastes this into an image generation service, then adds the result to the repository. Make it complete enough to work with no other context. It is also shown on the work's page under "Image prompt", so write it to be read.

- Describe one photographable scene: a documentation photograph of the work installed or carried out, an object, a typed card, words on a wall, a page.
- Be literal and concrete: what is in frame, where, materials, colours, light, camera angle, framing.
- House look, unless the work calls for something else: documentary photograph, white or neutral setting, soft even daylight, muted neutral colour, slight film grain, in the manner of 1960s and 1970s conceptual art documentation.
- If text appears in the image, give the exact words in capitals and keep it to a few words. Say where each word sits.
- Any clock, number or count must be stated exactly (for example "both clocks show exactly 9:00").
- End with: "Square format, 1:1." and a list of exclusions (no people unless needed, no logos, no brand names, no other text).
- Do not name real artists in the prompt.

## 6. Build and check

1. Append the new entry to `works.json` (keep the file a valid JSON array).
2. Run `python3 build.py`. It must print `Built N work page(s) and index.html` with N one higher than before. If it errors, fix the entry and run it again.
3. Check that `works/<slug>.html` exists and that `index.html` lists the new title first.
4. Run `LC_ALL=C.UTF-8 grep -nP "[\x{2013}\x{2014}]" works.json index.html works/*.html` and confirm it prints nothing.
5. `git status` should show only `works.json`, `index.html` and HTML files under `works/` as changed or new. If anything else changed, find out why before going on.

## 7. Publish

1. Commit with the message `No. NNN: <Title>` (three-digit number).
2. Push to the default branch. On a network error, retry up to four times, waiting 2, 4, 8 and 16 seconds.
3. GitHub Pages deploys from the default branch on its own. Nothing else is needed.

## 8. Tell the user

Post one short message with:

- the number and title,
- the link to the work's page on the site: `https://mahiryavuz.com/mario-mamodei/works/<slug>.html`,
- the image prompt in its own code block,
- one line: save the image as `works/<slug>.jpg` in the repository; the page shows it as soon as the file is there.

If the run stopped anywhere above, post one line saying where and why, and publish nothing.

## Image files

- Images live at `works/<slug>.jpg`, next to the work's page. JPEG, square, about 1600 to 2000 pixels wide is plenty.
- Until the file exists, the page shows a quiet "Image to come" panel. No rebuild is needed when the image is added.
- A run never generates or commits images itself.
