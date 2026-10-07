# Documentation tools

Scripts that maintain the manual and the Vite Technology site. All of them use
the Python 3 standard library only.

| Script | What it does |
|---|---|
| `ReleaseNotes/generate_release_notes.py` | Regenerates the commit record on every release notes page, between `<!-- BEGIN GENERATED COMMIT RECORD -->` and `<!-- END GENERATED COMMIT RECORD -->`. Hand-written summaries above the block are left alone. |
| `join_cjk_lines.py` | Joins hard-wrapped lines in the Japanese sources where the break would render as a stray space. Run after editing any Japanese page; the docs workflow also runs it. |
| `check_docs.py` | Checks both manuals without a Writerside build: tree files parse, every topic is in its tree, local links and images resolve, Writerside tags balance, and the Japanese tree matches the English one topic for topic. Exits 1 on any error; the docs workflow runs it before building. |

## Release notes

The generator reads commit history from an engine clone. A treeless clone is
enough and keeps the download small:

```
git init --bare vite.git
git -C vite.git remote add pub https://github.com/GapingPixel/UnrealEngineVite-PhysX.git
git -C vite.git remote add int https://github.com/ViteStudio-Tech/ueVite-Internal.git
git -C vite.git config remote.pub.promisor true
git -C vite.git config remote.pub.partialclonefilter tree:0
git -C vite.git config remote.int.promisor true
git -C vite.git config remote.int.partialclonefilter tree:0
git -C vite.git fetch --filter=tree:0 --no-tags pub "+refs/heads/ueVite*:refs/remotes/pub/ueVite*" "+refs/heads/4.27-plus:refs/remotes/pub/4.27-plus"
git -C vite.git fetch --filter=tree:0 --no-tags int "+refs/heads/ueVite26-AugustMajor-staging-9:refs/remotes/int/ueVite26-AugustMajor-staging-9"

python Tools/ReleaseNotes/generate_release_notes.py --git-dir vite.git
python Tools/ReleaseNotes/generate_release_notes.py --git-dir vite.git --locale ja
```

The public repository is visible only to GitHub accounts linked to an Epic
Games account, and the internal repository needs team access. Commits that
exist only in the internal staging branch are listed without links.

`--dump <folder>` writes the raw commit lists as tab-separated files instead of
editing the pages, which is useful when writing a new release summary.

## Japanese line breaks

```
python Tools/join_cjk_lines.py           # rewrite WritersideJP/topics and ViteTech/src/pages/ja
python Tools/join_cjk_lines.py --check   # exit 1 if anything would change
```
