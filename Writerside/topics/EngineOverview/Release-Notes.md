# Release Notes

<tldr>
<p>
Release history for Unreal Engine Vite, ordered from the latest major release to the original NvRTX 5.0-based Vite line.
Each release page records its audited scope, source branches, highlights and commit history.
</p>
</tldr>

## Releases

| Release | Window | Captured commits | Status |
|---|---|---:|---|
| [ueVite26-AugustMajor](ueVite26-AugustMajor.md) | 1–26 August 2026 | 518 | Latest |
| [ueVite26-JulyMajor](ueVite26-JulyMajor.md) | 1 July–1 August 2026 | 148 | Major |
| [ueVite26-JuneMajor](ueVite26-JuneMajor.md) | 1 April–30 June 2026 | 38 | Major |
| [ueVite26-MarchMajor](ueVite26-MarchMajor.md) | 1 January–31 March 2026 | 48 | Major |
| [ueVite25-LTS](ueVite25-LTS.md) | 1 November–31 December 2025 | 82 | LTS |
| [Original Vite](Original-Vite.md) | Original NvRTX 5.0 codebase | 0 | Archive |

## How the history is scoped

- **ueVite26-AugustMajor** combines the final release branch's latest five commits with the non-overlapping deltas from August staging snapshot 1 and staging snapshot 9.
- **ueVite26-JulyMajor**, **ueVite26-JuneMajor** and **ueVite26-MarchMajor** use committer-date windows so later maintenance on the named branch does not leak into an older release.
- **ueVite25-LTS** uses the requested 1 November–31 December 2025 audit window. The branch snapshot currently ends on 26 November, so no December-dated commits are present.
- **Original Vite** has no commit table because its public NvRTX 5.0 repository history was wiped.

<note>
<p>
Merge, revert, upload and maintenance commits remain in the commit record. The tables are an auditable branch history, while each page's highlights provide the curated release summary.
</p>
</note>

## Related resources

- [Engine Overview](Engine-Overview.md)
- [Backporting Workflow](Backporting.md)
- [Commit and PR Conventions](Commit-Conventions.md)
- [Bundled Plugins](Bundled-Plugins.md)

