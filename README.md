# Mario Mamodei

A static site that publishes a new conceptual work by the invented artist Mario Mamodei every twelve hours, at 9 am and 9 pm New York time.

## Files

- `works.json`: every work, one entry each. The single source of truth.
- `build.py`: regenerates `index.html` and `works/<slug>.html` from `works.json`. Python 3, no packages.
- `style.css`: the shared stylesheet.
- `works/<slug>.svg`: each work's image, drawn in code by the run that published it (No. 001 is a photograph, `works/twelve-hours-apart.jpg`).
- `sources.md`: the artists and texts the works draw on.
- `PROCESS.md`: the procedure each scheduled run follows.
- `.nojekyll`: tells GitHub Pages to serve the files as they are.

## Preview locally

```
python3 build.py && python3 -m http.server 8000
```

Then open http://localhost:8000.

## GitHub Pages

In the repository's Settings, under Pages, set the source to "Deploy from a branch", branch `main`, folder `/ (root)`.

## Custom subdomain (later)

There is no `CNAME` file yet on purpose. When the subdomain is registered:

1. Add a file named `CNAME` at the root containing only the subdomain, for example `art.example.com`.
2. At the DNS provider, add a CNAME record for that subdomain pointing to `<github-username>.github.io`.
3. In Settings, under Pages, enter the same subdomain and turn on "Enforce HTTPS" once it is offered.

All links on the site are relative, so nothing else changes.
