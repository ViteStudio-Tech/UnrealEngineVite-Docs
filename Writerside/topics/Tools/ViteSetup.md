# ViteSetup Assistant

<tldr>
<p>
<code>ViteSetup.bat</code> at the engine root takes a fresh clone to a launched editor in nine guided
steps. The <b>Express</b> path is the recommended one: Win64 dependencies only, a source build, then a
strip-down that moves everything it removes to a recovery folder. <code>ViteSetup.bat menu</code> gives you
the individual operations instead. This page describes the
<a href="ueVite26-SeptemberMajor.md">September Major</a> version.
</p>
</tldr>

The assistant exists because setting up an Unreal source build has many steps, each with failure modes that
produce unhelpful errors when you get them wrong. It checks the environment first, so a missing toolchain
component fails at step 1 with a clear message rather than at step 5 with a linker error.

## Guided mode

Run `ViteSetup.bat` with no arguments.

| Step | Source build (Express or Custom) | Precompiled binary build |
|---|---|---|
| 1 | Check the environment and enforce the toolchain | Same |
| 2 | Choose how to build | Same |
| 3 | Set up dependencies | Set up dependencies |
| 4 | Generate Visual Studio project files | Generate Visual Studio project files |
| 5 | Build the engine from source | Build the installed binary and its archive |
| 6 | Strip the engine down | Register the build |
| 7 | Register the build | Create the desktop shortcut |
| 8 | Create the desktop shortcut | Finish (binary builds are not launched) |
| 9 | Launch the editor | &mdash; |

Each step pauses so you can read the output before continuing. Failures stop the assistant and report an
error code rather than pushing on. Before setup and again at the end, the assistant reports the expected and
actual disk use; a full Windows source tree is around 137&nbsp;GB once built, and the Express path exists to
cut that down.

## Step 1 &mdash; environment check

The assistant accepts either of two toolchains and will not proceed without one:

| Requirement | Accepted |
|---|---|
| Visual Studio and MSVC | Visual Studio 2022 with MSVC 14.44 or higher, **or** Visual Studio 2026 with MSVC 14.50 or higher |
| MSBuild | Required by UnrealBuildTool and the C# tools |
| Windows SDK | 10.0.26100, subversion .7705 or higher, major pinned to 26100 |
| .NET Framework targeting packs | 4.6.2 (UnrealBuildTool, AutomationTool) and 4.5 (SwarmAgent and C# tools) |

If both Visual Studio versions are installed, it asks which one to build with and passes `-2022` or
`-2026` to every build. If the SDK is below the minimum or the .NET 4.5 targeting pack is missing, it offers
to install them and re-checks the full toolchain afterwards. See
[Toolchain Requirements](Toolchain-Requirements.md).

The .NET Framework 4.5 targeting pack is the component people most often lack, since recent Visual Studio
installers no longer offer it by default. See [Build Troubleshooting](Build-Troubleshooting.md).

## Step 2 &mdash; choose how to build

| Option | What it does |
|---|---|
| **1. Source build &ndash; Express** (recommended) | Win64 only unless you tick more platforms. Downloads the smallest dependency set, compiles, then strips the engine down. |
| 2. Source build &ndash; Custom | The same build, but you pick the platforms, optional content and strip items yourself |
| 3. Precompiled binary build | A packaged engine with no usable engine source. Not recommended. |

**Choose a source build.** It is the supported configuration: you can step into engine code in the
debugger, apply fork patches, rebuild after every pull and change
[compile-time switches](Compile-Time-Switches.md). A precompiled binary can do none of that, takes longer to
produce than the source build it is made from, and bug reports made against one cannot be supported. See
[Installed Builds](Installed-Builds.md) for when a binary still makes sense.

## Step 3 &mdash; dependency setup

On the Express path, Win64, the Win32 support files and templates are always downloaded, and a platform
picker lets you add Android, Linux, iOS/tvOS or Mac. Samples, feature packs, documentation, GoogleVR,
LeapMotion, WinRT, HTML5, consoles and every platform left unticked are never downloaded, which is where
most of the space is saved.

The Custom path offers setup profiles instead:

| Profile | What it does |
|---|---|
| Step-by-step assistant | Choose platforms and optional content individually, then review |
| Recommended Win64 | Win64 only. Excludes non-Windows platforms, samples, templates, feature packs, docs, XR and consoles. |
| Win64 ultra compact | As recommended, with the smallest optional content set |
| Win64 + templates / feature packs | Keeps project templates and starter content |
| Win64 + Android | Adds Android dependencies |
| Win64 + Linux | Adds Linux and cross-compile dependencies |
| Full setup | Passes no `-exclude` argument to `Setup.bat` |

Dependencies are cached in `UE4_Source_Cache` and fetched with 20 threads, so re-running setup does not
download them again.

## Step 5 &mdash; build

A source build compiles `UE4Editor`, `ShaderCompileWorker`, `UnrealLightmass` and `UnrealInsights` for
Win64 Development in the source tree.

A binary build runs the BuildGraph `Make Installed Build Win64` target with Development and Shipping game
configurations, then packages the result. It archives with WinRAR into `UE_ViteFork.rar` when WinRAR is
installed, offers to download the WinRAR trial when it is not, and falls back to 7-Zip and
`UE_ViteFork.7z`.

## Step 6 &mdash; strip the engine down

The Express path moves, after a dry-run review:

- every platform folder except Win64
- debug symbols (`.pdb`)
- Starter Content and Mobile Starter Content
- the NVIDIA sample projects `NGXTest` and `RTXGI_Test`
- every template except Third Person, C++ and Blueprint
- every plugin under `Engine\Plugins\Runtime\VitePlugins` except ACL and MotionSymphony

<warning>
<p>
The last item moves FSR 4, Anti-Lag 2, XeSS, the PhysX Instanced Subsystem, KawaiiPhysics, ImGui, GPA,
Automatron and SplashAbilities. If your project uses any of them, take the Custom path, or copy the folders
back from <code>ViteDebloat_Moved</code>.
</p>
</warning>

Nothing is deleted. Everything goes to `ViteDebloat_Moved` next to the engine folder, keeping its layout,
and the reference check confirms the remaining tree still builds. Express then offers a second, optional
pass over the plugin exclusion list, UnrealFileServer, non-Windows tools and platform binaries. The Custom
path opens the same picker directly. Full detail is in the [Debloat Guide](Debloat-Guide.md).

## Registration and shortcut

Registration writes the engine path to `HKCU\Software\Epic Games\Unreal Engine\Builds` under the name
`UE_ViteFork`, which is what makes the build selectable in a `.uproject` file's engine association. It
first removes any auto-generated GUID entry pointing at the same folder, so the engine does not appear
twice in the version switcher.

The shortcut step creates `UEViteFork.lnk` on the desktop, pointing at `UE4Editor.exe`.

<note>
<p>
The standalone <code>LocalBuilds\RegistryAdd.bat</code> and <code>RegistryRemove.bat</code> still use the
older name <code>UEViteFork</code>. A project's engine association must match the registered name exactly,
so register a given engine through one route only. The scripts that ViteSetup writes into a binary package
use <code>UE_ViteFork</code>.
</p>
</note>

## Menu mode

`ViteSetup.bat menu` skips the guided flow and presents the operations individually:

| Option | Action |
|---|---|
| 1 | Check the environment and toolchain |
| 2 | Set up dependencies (assistant) |
| 3 | Generate Visual Studio files |
| 4 | Build Unreal Engine source |
| 5 | Set up dependencies, then generate Visual Studio files |
| 6 | Open `UE4.sln` |
| 7 | Show setup profiles |
| 8 | Build precompiled binary (not recommended) |
| 9 | Strip the engine down (picker) |
| 0 | Exit |

Menu mode is what you want for day-to-day work. Regenerating project files after adding a module, or
rebuilding after a pull, does not need the whole guided flow.

`ViteSetup.bat --sync-only` runs only the dependency sync, non-interactively, with any remaining arguments
passed through to `Setup.bat`. Use it on build machines.

## Key paths

| Item | Path |
|---|---|
| Editor executable | `Engine\Binaries\Win64\UE4Editor.exe` |
| Installed build staging | `LocalBuilds\Engine\Windows` |
| Installed build archive | `LocalBuilds\Engine\UE_ViteFork.rar` (or `.7z` with 7-Zip) |
| Dependency cache | `UE4_Source_Cache` |
| Strip recovery folder | `..\ViteDebloat_Moved` |
| Engine association | `UE_ViteFork` |

## See also

- [Build from Source](Build-From-Source.md)
- [Toolchain Requirements](Toolchain-Requirements.md)
- [Installed Builds](Installed-Builds.md)
- [Build Troubleshooting](Build-Troubleshooting.md)
- [Debloat Guide](Debloat-Guide.md)
