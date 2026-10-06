# Unreal Engine Vite documentation

Source for the Unreal Engine Vite manual (English and Japanese) and the Vite Technology product site,
published together on GitHub Pages.

| Site | Path | Source |
|---|---|---|
| Engine manual, English | `/` | `Writerside/` (Writerside instance `hi`) |
| Engine manual, Japanese | `/jp/` | `WritersideJP/` (instance `jp`) |
| Vite Technology | `/tech/` and `/tech/jp/` | `ViteTech/` |

Live site: <https://vitestudio-tech.github.io/UnrealEngineVite-Docs/>

## Layout

```
Writerside/            English manual: topics/, images/, hi.tree, cfg/vite-theme.html (shared theme)
WritersideJP/          Japanese manual: same topic names and order, jp.tree (see WritersideJP/README.md)
ViteTech/              Vite Technology site: src/pages/{en,ja}, build.py, public/ (see ViteTech/README.md)
Tools/                 Release-notes generator and the Japanese line joiner (see Tools/README.md)
.github/workflows/     DocsBuild.yml: builds both manuals and the tech site, deploys to Pages on push to main
```

## Editing

- Every English topic has a Japanese counterpart with the same file name and position in the tree. Change
  both in the same commit.
- Images and the theme live only in `Writerside/`; the workflow copies them into `WritersideJP/`.
- After editing Japanese text, run `python Tools/join_cjk_lines.py` so wrapped lines do not render as stray
  spaces.
- Ground technical claims in the engine source of the latest public release branch. The contribution guide
  in the manual, *Contributing to the Documentation*, covers conventions and the build pipeline.

## Building locally

The manuals build with JetBrains Writerside (IDE plugin or the Docker builder used by the workflow). The tech
site needs only Python 3:

```
python ViteTech/build.py
python -m http.server 8642 --directory ViteTech/public
```

## Licence

Documentation in this repository is licensed under the Apache License 2.0; see `LICENSE`. The engine it
documents is used under Epic's Unreal Engine EULA.
