# Contributing to the Documentation

<tldr>
<p>
These docs are a JetBrains Writerside project with two modules: English in <code>Writerside\</code> and
Japanese in <code>WritersideJP\</code>. Add the Markdown file to both, register it in both trees, and push
to <code>main</code> &mdash; GitHub Actions builds both languages and the Vite Technology site and deploys
them to GitHub Pages.
</p>
</tldr>

Documentation that lags the engine is worse than no documentation, because people trust it. If you change
a default, add a console variable or compile out a feature, the page describing it needs to change in the
same pass.

## Repository layout

| Path | Contents |
|---|---|
| `Writerside\topics\` | English topic Markdown files, organised in subfolders by section |
| `Writerside\images\` | Images for both languages, referenced by filename alone |
| `Writerside\hi.tree` | English navigation tree (instance `hi`); a topic not listed here is not published |
| `Writerside\cfg\vite-theme.html` | The shared theme: header, navigation, landing page styling |
| `WritersideJP\topics\` | Japanese topics, with the same file names and folders as the English ones |
| `WritersideJP\jp.tree` | Japanese navigation tree (instance `jp`), in the same order with localised titles |
| `Tools\ReleaseNotes\generate_release_notes.py` | Regenerates the commit records on the release notes pages |
| `ViteTech\` | The Vite Technology site: `src\pages\en` and `src\pages\ja`, built by `build.py` |
| `.github\workflows\DocsBuild.yml` | Build and deploy pipeline |

## Adding a topic

<procedure title="Add a documentation page" id="add-topic">
    <step>
        Create the Markdown file in the appropriate <code>Writerside\topics\</code> subfolder. Use
        <code>Title-Case-With-Hyphens.md</code>.
    </step>
    <step>
        Add a <code>&lt;toc-element topic="Your-File.md"/&gt;</code> entry to
        <code>Writerside\hi.tree</code> in the right section.
    </step>
    <step>
        Cross-link it. Add it to the parent section page's topic table and to the
        <b>See also</b> lists of related pages.
    </step>
    <step>
        Create the Japanese page at the same path under <code>WritersideJP\topics\</code> and add it to
        <code>WritersideJP\jp.tree</code> in the same position, with a Japanese <code>toc-title</code>.
        If you cannot translate it yet, copy the English page so the two trees stay identical.
    </step>
    <step>Push to <code>main</code>. The workflow builds and deploys automatically.</step>
</procedure>

<note>
Browsers show a line break between two Japanese characters as a space. Write Japanese paragraphs on one
line, or run <code>python Tools/join_cjk_lines.py</code> before committing; it joins wrapped lines where
both sides are Japanese and leaves code blocks alone. The workflow runs it too.
</note>

<note>
Images and <code>vite-theme.html</code> live only in the English module. The workflow copies them into
<code>WritersideJP</code> before the Japanese build, and those copies are ignored by Git, so never commit
images under <code>WritersideJP\images\</code>.
</note>

<note>
Writerside resolves topic links by filename, not by path, so <code>[Ray Tracing](Ray-Tracing.md)</code>
works regardless of which folder either file is in. Filenames must therefore be unique across the whole
project.
</note>

## Writing conventions

### Structure

Most pages follow the same shape:

1. `# Title`
2. A `<tldr>` block giving the answer in two or three sentences
3. Body sections
4. A `## See also` list

The `<tldr>` is not optional on substantial pages. Readers arriving from search need to know within a
sentence whether they are in the right place.

### Writerside elements

| Element | Use |
|---|---|
| `<tldr>` | The summary at the top |
| `<note>` | Useful context that is not a hazard |
| `<warning>` | Something that will cost the reader time or break their build |
| `<procedure>` | Numbered steps with an `id` attribute |
| `<deflist>` / `<def>` | Term-and-explanation lists |
| `<code-block lang="ini">` | Code inside an HTML-like element, where fenced blocks do not work |

Inside `<tldr>`, `<note>`, `<warning>` and `<def>`, use HTML rather than Markdown &mdash; `<b>`, `<code>`,
`<a href="Page.md">`, `<p>`. Markdown syntax is not processed there.

### Tone

- State the answer, then the reasoning. Not the reverse.
- Say what something costs, not only what it does.
- Where a feature is unavailable by default, say so at the top of the page, not in a footnote. The
  [RTXDI](RTXDI.md) and [path tracing](Path-Tracing.md) pages are the pattern to follow.
- Tables for enumerable facts, prose for explanation. Do not put explanations in table cells.

### Accuracy

Ground claims in the engine source. Console variable names, defaults and help text should be checked
against their definition rather than remembered:

```
Engine\Source\Runtime\Renderer\Private\        renderer CVars
Engine\Source\Runtime\Engine\Classes\Engine\Scene.h    post-process settings
Engine\Source\Runtime\Core\Public\Misc\CoreDefines.h   VITE_* compile switches
```

<warning>
Console variable help text in the engine is sometimes out of date. HBAO+ describes itself as DX11-only in
its help string but has a working D3D12 implementation. When source and help text disagree, trust the
source and document the discrepancy.
</warning>

## Building locally

Install the Writerside plugin for a JetBrains IDE, or Writerside standalone, and open the repository root.
The instance IDs are `hi` (English) and `jp` (Japanese). Before previewing `jp`, copy
`Writerside\images\` and `Writerside\cfg\vite-theme.html` into `WritersideJP\` as the workflow does.

The Vite Technology site needs only Python 3:

```
python ViteTech/build.py
```

It writes plain HTML to `ViteTech\public\`, English at the root and Japanese under `jp\`.

Writerside's own inspections catch broken topic links, unreferenced topics and missing images, which is
faster than discovering them after a deploy.

## The build pipeline

`.github\workflows\DocsBuild.yml` runs on every push to `main` and on manual dispatch. It builds the `hi`
and `jp` instances in parallel with the Writerside Docker builder, then assembles one site: English at the
root, Japanese under `/jp/`, and the Vite Technology site under `/tech/`.

A Japanese build failure does not block the English deploy, but an English failure stops the deploy so a
stale site is never published. A build failure usually means a topic referenced in a tree does not exist,
or a topic exists but is not referenced. Both are reported by name in the workflow log.

## Release notes

Each release page has a hand-written summary and a generated commit record between
`<!-- BEGIN GENERATED COMMIT RECORD -->` and `<!-- END GENERATED COMMIT RECORD -->`. Regenerate the records
from an engine clone with the public repository as remote `pub` and the internal repository as remote `int`
(the August record lists internal staging commits). A treeless clone (`--filter=tree:0`) is enough:

```
python Tools/ReleaseNotes/generate_release_notes.py --git-dir <path to engine clone>
python Tools/ReleaseNotes/generate_release_notes.py --git-dir <path to engine clone> --locale ja
```

Edit the summaries by hand; never edit inside the generated block.

## Documenting engine changes

If your engine change affects any of the following, update the documentation in the same pull request:

| Change | Page to update |
|---|---|
| New or changed console variable | The relevant feature page |
| New `VITE_*` switch | [Compile-Time Switches](Compile-Time-Switches.md) |
| Changed engine default | [Engine Defaults](Engine-Defaults.md) |
| New or updated plugin | [Bundled Plugins](Bundled-Plugins.md) |
| New tool or script | The [Tools](Tools.md) section |
| A feature becoming unavailable in default builds | The feature's page, and [Ray Tracing](Ray-Tracing.md) if applicable |

## See also

- [Contributing](Contributing.md)
- [Coding Guidelines](Coding-Guidelines.md)
- [Commit Conventions](Commit-Conventions.md)
