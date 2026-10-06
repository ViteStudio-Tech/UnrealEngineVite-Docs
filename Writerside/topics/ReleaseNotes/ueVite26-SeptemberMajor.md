# ueVite26 September Major

<tldr>
<p>
The latest major release. September moves the codebase onto modern language and tooling foundations
&mdash; an initial <b>C++20</b> upgrade, an initial <b>.NET</b> upgrade for the engine's C# programs and
<b>Embree 4.4.1</b> in Lightmass &mdash; and carries SSGI and TressFX improvements on top of the August
Major.
</p>
<p>
Branch <code>ueVite26-SeptemberMajor-release</code> &middot; builds on
<a href="ueVite26-AugustMajor.md">ueVite26 August Major</a>.
</p>
</tldr>

| Status | Development window | Builds on | Commits |
|---|---|---|---:|
| **Latest** | 26 August &ndash; 30 September 2026 | [ueVite26 August Major](ueVite26-AugustMajor.md) | 11 |

## Highlights

<deflist>
<def title="C++20 foundation">
The initial C++20 upgrade brings the codebase in line with the language model UE 5.0 introduced: C++20 is
enabled per module or per target, while the engine itself continues to build as C++17. Engine headers are
kept parseable from C++20 translation units, so project code can adopt C++20 without forking the engine.
</def>
<def title=".NET upgrade">
The initial .NET upgrade bundles the .NET 6 SDK (6.0.302) with the engine, the runtime UE 5.0 uses for its
C# programs &mdash; the build and automation tooling. It is the first step in moving those programs off
.NET Framework, continuing the toolchain modernisation that began with Visual Studio 2026 support.
</def>
<def title="Lightmass on Embree 4.4.1">
Lightmass now uses Embree 4.4.1 for its CPU ray tracing, with the Windows deployment fixed so packaged
Lightmass builds pick up the new runtime. Contributed by the community.
</def>
<def title="Faster SSGI">
SSAO is now skipped when SSGI is guaranteed to run and replace its ambient-occlusion mask, removing a
redundant pass from the recommended <a href="Global-Illumination.md">DDGI plus SSGI</a> setup.
</def>
</deflist>

## What's new

### Rendering

- **SSGI performance:** skips SSAO when SSGI is guaranteed to execute and provides the occlusion term.
- **TressFX:** integration update carried forward from the August line. See [Hair Rendering](Hair-Rendering.md).

### Toolchain and platforms

- **C++20:** initial upgrade. Opt in per target or module with `CppStandard = CppStandardVersion.Cpp20`.
- **.NET:** initial upgrade of the engine's C# programs; the .NET 6 SDK (6.0.302) is bundled under
  `Engine/Binaries/ThirdParty/DotNet`.
- **Lightmass:** updated to Embree 4.4.1, with a fix for deploying the Embree runtime on Windows.
- **Linux:** fixed a `TScopeLock` issue in the Unix platform file layer (RAII locking).

## Upgrade notes

- Run `Setup.bat` and regenerate project files after switching to this branch; the C++20 and .NET changes
  touch the build tooling. See [ViteSetup](ViteSetup.md).
- C++20 is opt-in. Projects that do not set `CppStandard` keep building as C++17, so no source changes are
  required to upgrade.
- If you build Lightmass yourself, rebuild it after updating so it links against Embree 4.4.1.

## Community contributions

Lightmass's Embree 4.4.1 update and the Linux `TScopeLock` fix arrived as community pull requests
(#166 and #167). Contributions are welcome &mdash; see [Contributing](Contributing.md).

<!-- BEGIN GENERATED COMMIT RECORD -->

## Full commit history {id="commit-history"}

Branch: [`ueVite26-SeptemberMajor-release`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/tree/ueVite26-SeptemberMajor-release)

### Commits by area

| Area | Commits |
|---|---:|
| Toolchain and platforms | 9 |
| Rendering | 1 |
| Hair | 1 |

### Public release branch — 11 commits {collapsible="true" default-state="collapsed"}

11 commits (5 merge commits omitted from the table).

| Date | Commit | Author | Change |
|---|---|---|---|
| 2026-09-28 | [`3827a62413`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3827a62413cbdb30c514467669a2028044f5f8fd) | Michael Taulli | Fix Windows Embree 4.4.1 Lightmass deployment |
| 2026-09-28 | [`714417496d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/714417496df642be8493ce0c7c03bca5b1ffb01a) | Michael Taulli | Fix Windows Embree 4.4.1 Lightmass deploymentclear |
| 2026-09-28 | [`b93b5d402a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b93b5d402a1438ace93bf0b3929f94c807053155) | unknown | Restore dotnet files(sorry) |
| 2026-09-28 | [`f364b63345`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f364b63345f3484af9419b068b21612cefa0a659) | unknown | Remove accidentally committed DotNet setup files |
| 2026-09-28 | [`8eb537d9e5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8eb537d9e5359a2a585b67a3f2f1107c46127080) | unknown | Remove accidentally committed dotnet binaries |
| 2026-09-28 | [`725a6893d9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/725a6893d9b37fb5d3818541e4f137531f82d56c) | unknown | Update lightmass to Embree 4.4.1 |
| 2026-09-27 | [`8855719c60`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8855719c60ab2c9c2cd66ca62b25f3b7978e8eea) | unknown | Fix TScopeLock issue on linux |
| 2026-08-30 | [`1115b3e822`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1115b3e822dc2c6af240e7538cc8d213d107b7a8) | RedPixel | Initial CPP 20 Upgrade |
| 2026-08-30 | [`ec3ebdef2f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ec3ebdef2f1138a4549e7abec390111fa462e07d) | RedPixel | Initial NET Upgrade |
| 2026-08-26 | [`940af70a05`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/940af70a0551904442adde2c560a24fe1e3242a9) | RedPixel | \[Rendering\] SSGI Performance improvement |
| 2026-08-26 | [`bacc4aaaa2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bacc4aaaa22eeabcce8189a0e66240105aae673d) | RedPixel | \[Rendering\] TressFX Update |

<!-- END GENERATED COMMIT RECORD -->

## See also

- [All release notes](Release-Notes.md)
- [ueVite26 August Major](ueVite26-AugustMajor.md)
- [Toolchain Requirements](Toolchain-Requirements.md)
- [Build from Source](Build-From-Source.md)
