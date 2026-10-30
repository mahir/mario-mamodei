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
| `images` | One to three entries, in page order: `{"file": "<slug>-1.jpg", "alt": "..."}`, then `-2.jpg`, `-3.jpg`. `alt` is one sentence describing that image for screen readers. The files themselves come later (section 9). |

Do not add `image_prompt`, `note` or `medium` to `works.json`; build.py rejects them. Image prompts go only to the user in chat (section 8).

### The text

The text is the artwork's page. It is a philosophical, conceptual essay by Mario Mamodei about what the work means: its idea, what it opens up, what it reveals once you see it. Deep and artistic, but in plain words.

- About 120 to 250 words, in short paragraphs separated by a blank line (`\n\n` in JSON).
- Before writing, read No. 001's text in `works.json` ("Twelve Hours Apart") and treat it as the bar for tone and depth. This is conceptual art writing, not a description or a set of steps.
- Do not open with, or read as, an instruction or a how-to. The image shows the work; the text thinks about it. Name the work's objects only as far as the thinking needs them.
- Ask what the work is really about and follow that all the way down. It might be an idea, a feeling, a question, an observation or a contradiction; let the work decide. Write about a paradox only when the work actually has one.
- Weave in one to three references to artists, works or thinkers where they move the argument forward, as part of the thought, never as a list or a credit line. Describe them accurately. Name only items marked [checked] or [known] in `sources.md`; verify anything else with a web search first and add it there with its mark.
- End on a short line that turns the idea once more. No summary, no explaining the joke.
- Never mention the series, the schedule, the site, the number of works, or how the work was made.
- No art jargon. First person is allowed but not required.

## 5. Write the image prompts

The user generates the images with an image service from your prompts. Never make images yourself, in code or otherwise. Prompts never go on the site or in the repository; they go only in the message in section 8.

Write one to three prompts, your choice, to suit the concept. One strong installation shot is often enough. Add a second or third only when it shows something the first cannot: a close up of a detail that carries the idea, a different view or moment, or a different image altogether.

- Each prompt describes one photographable scene: the work installed or carried out, an object, a typed card, words on a wall, a page.
- Make each prompt complete on its own, with no reference to the others.
- Be literal and concrete: what is in frame, where, materials, colours, light, camera angle, framing.
- House look, unless the work calls for something else: documentary photograph, white or near white gallery setting, soft even daylight, muted neutral colour, slight film grain, in the manner of 1960s and 1970s conceptual art documentation. The site is light, so bright white walls sit well on it.
- If text appears in an image, give the exact words in capitals and keep it to a few words. Say where each word sits.
- Any clock, number or count must be stated exactly (for example "both clocks show exactly 9:00").
- End each with: "Square format, 1:1." and a list of exclusions (no people unless needed, no logos, no brand names, no other text).
- Do not name real artists in the prompts.

## 6. Build and check

1. Append the new entry to `works.json` (keep the file a valid JSON array).
2. Run `python3 build.py`. It must print `Built N work page(s) and index.html` with N one higher than before. If it errors, fix the entry and run it again.
3. Check that `works/<slug>.html` exists and that `index.html` lists the new title first.
4. Run `LC_ALL=C.UTF-8 grep -nP "[\x{2013}\x{2014}]" works.json index.html works/*.html` and confirm it prints nothing.
5. Open `works/<slug>.html` and confirm it holds only the title, the image slots, the text and the date. Until the image files arrive the page shows a quiet "Image to come" panel; that is expected, and publishing goes ahead.
6. `git status` should show only `works.json`, `index.html` and HTML files under `works/` as changed or new. If anything else changed, find out why before going on.

## 7. Publish

1. Commit with the message `No. NNN: <Title>` (three-digit number).
2. Push to the default branch. On a network error, retry up to four times, waiting 2, 4, 8 and 16 seconds.
3. GitHub Pages deploys from the default branch on its own. Nothing else is needed.

## 8. Tell the user

Post one short message with:

- the number and title, as a link to the work's page (`https://mahiryavuz.com/mario-mamodei/works/<slug>.html`),
- each image prompt in its own code block, numbered 1 to 3 in page order,
- one line asking the user to send the generated images back in the chat, in that order.

If the run stopped anywhere above, post one line saying where and why, and publish nothing.

## 9. Adding images the user sends

This is not part of the scheduled run; it happens whenever the user sends images for a work.

1. Match each image to its work and position (the user sends them in prompt order; ask if unclear).
2. Convert each to JPEG, square, about 1600 to 2000 pixels wide, quality about 88, and save as `works/<slug>-N.jpg`.
3. Commit with the message `No. NNN: images` and push. No rebuild is needed: the page shows each image as soon as its file is there.

## Image files

- No. 001 keeps its single photograph, `works/twelve-hours-apart.jpg` (described by `image_alt`).
- Every later work lists one to three images in `images` and gets them at `works/<slug>-1.jpg`, `-2.jpg`, `-3.jpg`.
- Images are made by the user from the run's prompts. A run never makes or commits images itself.
