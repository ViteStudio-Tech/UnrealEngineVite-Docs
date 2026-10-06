# WritersideJP

Japanese documentation module. Built as instance `jp` and published under
`/jp` on GitHub Pages.

Topic file names and folders mirror `Writerside/topics`, and `jp.tree` lists
them in the same order as `hi.tree`, so the language switcher can map any
English page to its Japanese counterpart by inserting `/jp/` in the path.
Only the `toc-title` values are localised.

Every published topic is translated. When an English page changes, update the
Japanese page in the same commit; if you cannot translate yet, copy the English
text so the two trees never diverge. Never rename a topic in one module only.

## Shared assets

`images/` and `cfg/vite-theme.html` are not stored here. The docs workflow
copies them from `Writerside/` before the Japanese build, and both paths are
ignored by Git. Copy them yourself before previewing the `jp` instance locally.

## Line breaks

Browsers render a line break between two Japanese characters as a visible
space. Write Japanese paragraphs on one line, or run

```
python Tools/join_cjk_lines.py
```

before committing. It joins wrapped lines where both sides are Japanese (or
the line ends in full-width punctuation) and leaves code blocks and list
items alone. The workflow runs it as well, so a missed edit never reaches the
site.

## Style

- Spaces between Japanese text and Latin words, numbers and inline code
  (`Vite の SSAO`, `1 つ`), none around full-width punctuation.
- Product, plugin, console variable and UI names stay in English as they appear
  in the engine (`r.SMAA.Quality`, **Project Settings**).
- Headings, anchors (`{id="..."}`) and procedure ids match the English page.
