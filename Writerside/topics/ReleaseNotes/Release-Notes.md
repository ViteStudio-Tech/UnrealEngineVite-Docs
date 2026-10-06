# Release Notes

<tldr>
<p>
Every public Unreal Engine Vite release, newest first. The latest is
<a href="ueVite26-SeptemberMajor.md"><b>ueVite26 September Major</b></a>. Each page leads with highlights and
upgrade notes, and ends with the complete commit history of its release branch.
</p>
</tldr>

## Releases

| Release | Type | Development window | Headline changes | Commits |
|---|---|---|---|---:|
| [ueVite26 September Major](ueVite26-SeptemberMajor.md) | **Latest** | Aug &ndash; Sep 2026 | C++20 and .NET upgrades, Embree 4.4.1 Lightmass, faster SSGI | 11 |
| [ueVite26 August Major](ueVite26-AugustMajor.md) | Major | Jul &ndash; Aug 2026 | UE5 editor/memory backports, RT reflections, specular occlusion, GAS, XeSS 3.1, macOS port | 438 |
| [ueVite26 July Major](ueVite26-JulyMajor.md) | Major | Jul &ndash; Aug 2026 | +12.3% FPS gating, Blast SDK upgrade, UE5 plugin backports, ViteSetup | 78 |
| [ueVite26 June Major](ueVite26-JuneMajor.md) | Major | Mar &ndash; Jul 2026 | FSR 4, DLSS 4, XeSS 3, frame generation, HBAO+, animation backports, fixed-timestep PhysX | 170 |
| [ueVite26 March Major](ueVite26-MarchMajor.md) | Major | Dec 2025 &ndash; Mar 2026 | Toon shading, compute SMAA, localized IBL, native PhysX actors, NDK 29 | 79 |
| [ueVite25 LTS](ueVite25-LTS.md) | **LTS** | Nov &ndash; Dec 2025 | NvRTX Caustics 4.27 base, performance defaults, VS 2026 | 174 |
| [Original Vite](Original-Vite.md) | Archived | Before Nov 2025 | NvRTX 5.0 (UE5) line, superseded by the LTS | &mdash; |

## Release lines

<deflist>
<def title="LTS">
<code>ueVite25-LTS</code> is the long-term base every major release builds on: NvRTX Caustics 4.27 merged
with Epic's 4.27-plus, plus Vite's default changes. Choose it when you need the most conservative branch.
</def>
<def title="Major releases">
<code>ueVite26-&lt;Month&gt;Major-release</code> branches. Each builds on the previous one, so upgrading
across several majors means reading every page in between. Major branches keep receiving fixes after
release; those are listed under <i>Maintenance after release</i> on each page.
</def>
<def title="Latest">
The newest major release. New projects should start here unless they need the LTS.
</def>
</deflist>

## How to read a release page

Each page has the same structure:

1. **Summary and release facts** &mdash; branch, development window, what it builds on, commit count.
2. **Highlights** &mdash; the changes most teams will notice.
3. **What's new** &mdash; grouped by area: rendering, ray tracing, upscaling, physics, animation, tools,
   platforms.
4. **Upgrade notes** &mdash; default changes and requirements that can change a project's behaviour.
5. **Full commit history** &mdash; generated from the release branch, grouped by area and collapsed by
   default. Merge commits are omitted from the tables.

## Where the source lives

All release branches are published in the
[Unreal Engine Vite repository](https://github.com/GapingPixel/UnrealEngineVite-PhysX).

<note>
<p>
Like every Unreal Engine source fork, the repository is only visible to GitHub accounts linked to Epic
Games. If branch or commit links return <i>404</i>, link your GitHub account in your Epic Games account
settings and accept the invitation to the EpicGames organisation.
</p>
</note>

The August Major was developed on an internal staging branch and published as a single release commit, so
its page lists the staged commits without links. Everything else links directly to the public commit.

## Related resources

- [Backporting Workflow](Backporting.md)
- [Commit and PR Conventions](Commit-Conventions.md)
- [Toolchain Requirements](Toolchain-Requirements.md)
- [Engine Overview](Engine-Overview.md)
