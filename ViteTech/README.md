# Vite Technology site

The product site for Vite's technology suite — Vite ReSTIR, ViteX Physics,
Vite BRDF, Vite Vertis and Vite Hair FX. It is the sister site to the
Unreal Engine Vite manual and is published beside it on GitHub Pages:

| Language | URL |
|---|---|
| English | `https://vitestudio-tech.github.io/UnrealEngineVite-Docs/tech/` |
| Japanese | `https://vitestudio-tech.github.io/UnrealEngineVite-Docs/tech/jp/` |

The manual's header links here as **Vite Technology** (resolved in
`Writerside/cfg/vite-theme.html`).

## Layout

```
ViteTech/
  build.py              wraps page fragments in the shared header/footer
  src/pages/en/*.html   English page bodies (front matter + HTML)
  src/pages/ja/*.html   Japanese page bodies, same file names
  public/               generated site + static assets (published as-is)
    assets/css|js|img|fonts
  tools/make_art.py     regenerates the Vertis and Hair FX illustrations
```

## Editing

1. Edit a fragment in `src/pages/<locale>/`. Keep English and Japanese pages
   structurally identical: same sections, same images, same numbers.
2. After editing Japanese pages, run `python Tools/join_cjk_lines.py` so that
   wrapped lines do not render as stray spaces (see `WritersideJP/README.md`).
3. Run `python ViteTech/build.py` (standard library only).
4. Preview with `python -m http.server 8642 --directory ViteTech/public`.

The docs workflow runs `build.py` again before publishing, so `public/` is
always regenerated from `src/` on deploy.

## Content rules

- **Numbers must be measured.** Every figure on the site is a like-for-like
  result already published in the manual (Physics, Global Illumination,
  Performance Targets, release notes). Technologies without published
  measurements describe design goals as goals.
- **Status must be current.** The availability table on the home page and the
  callout on each product page separate what ships in Unreal Engine Vite today
  from what is in development. Update both when a technology ships.
- **No internal implementation detail.** Product pages describe capabilities,
  not source files, classes or unreleased internals.
