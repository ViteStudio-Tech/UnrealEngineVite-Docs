# Debloat Guide

<tldr>
<p>
Scripts in <code>devops\</code>, driven by a single <code>config.txt</code>, remove engine content you do
not need. Everything defaults to <b>dry run</b> and <b>move rather than delete</b>, and since the July
Major a reference check confirms the stripped tree still builds. <a href="ViteSetup.md">ViteSetup</a>
runs the same scripts for you on its Express path.
</p>
</tldr>

A full Unreal Engine 4.27 source tree contains support for every platform, every workflow and every
template Epic ships. A Win64-only project uses a fraction of it. ViteSetup estimates a full Windows source
tree at around 137&nbsp;GB once built; debloating recovers much of that and reduces build time.

Original Vite debloat scripts by Bikouz.

## The suite

| Script | Purpose |
|---|---|
| `ueVite-debloat-SetupSlim.bat` | Runs engine dependency setup with a Win64-only focus, so unneeded platform dependencies are never downloaded |
| `ueVite-debloat-StripExecute.bat` | Removes platform binaries, non-Windows tools, templates, sample content and optionally plugins |
| `ueVite-debloat-StripDebugSymbols.bat` | Removes debug symbols according to `ExcludedPdbs.txt` |
| `ueVite-debloat-ValidateRefs.ps1` | Checks that no module left in the tree references a module that was moved out, and can move the missing ones back. Since [July Major](ueVite26-JulyMajor.md). |
| `ViteSpaceReport.ps1` | Estimates the download from the dependency manifest before setup, and measures the tree afterwards. Used by ViteSetup. Since July Major. |
| `ueVite-ApplyVitePluginDefaults.bat` | Applies or reverts Vite's engine plugin profile. See [Engine Default Changes](Engine-Defaults.md#disabled-plugins). Since July Major. |

All of them live in `devops\` at the engine root. The strip scripts read `devops\config.txt`; you can pass
an alternative config path as the first argument.

## Safety model

The scripts are deliberately conservative, and it is worth understanding how before running them.

**Dry run is the default.** `DRYRUN=1` prints every action without touching a file. Review the output
before changing it.

**Move is the default, not delete.** `MODE=move` relocates targeted files into `MOVE_DIR`, preserving their
relative layout so they can be restored by copying back. `MODE=delete` is permanent.

**The move destination cannot be inside the engine tree.** The script refuses, because a move destination
inside the tree would be caught by subsequent passes.

**Drive roots are refused.** Both the engine root and the move destination are checked.

**The engine root is validated.** The script confirms `Engine\Binaries\` exists before doing anything.

**References are checked afterwards.** With `VALIDATE_REFERENCES=1`, the default, a strip run ends by
scanning the `.Build.cs` and `.uplugin` files left in the tree for modules that now live in `MOVE_DIR`. A
clean result reads "No dangling references in the editor build". Otherwise it lists each missing module
and who needs it.

## Configuration

`devops\config.txt` uses `KEY=VALUE` lines. Comment a line out with `#` to **preserve** what it targets;
uncomment to **enable** an optional target. This inversion is worth internalising: an uncommented `STRIP`
line means that thing gets removed.

### Core settings

```
MODE=move
MOVE_DIR=..\ViteDebloat_Moved
DRYRUN=1
VALIDATE_REFERENCES=1
```

`MOVE_DIR` resolves against the engine root, so the default is a sibling folder of the engine.

### Platforms

Win64 is always kept. Uncomment a platform to also download and keep its dependencies during
`SetupSlim`:

```
#KEEP_PLATFORM=Android
#KEEP_PLATFORM=IOS
#KEEP_PLATFORM=Linux
#KEEP_PLATFORM=Mac
#KEEP_PLATFORM=HTML5
```

Do this **before** running setup. Not downloading a dependency is cheaper than downloading and then
deleting it.

### Templates

```
STRIP_OTHER_TEMPLATES=1
KEEP_TEMPLATE=TP_ThirdPerson
KEEP_TEMPLATE=TP_ThirdPersonBP
KEEP_TEMPLATE=TemplateResources
```

Every folder under `Templates\` not named by a `KEEP_TEMPLATE` line is targeted. `TemplateResources` is
shared by all templates and must be kept if you keep any template.

### Strip targets

The default target list, grouped by category:

**Platform binaries not needed for Win64**

```
STRIP=Engine\Binaries\Win64\Android
STRIP=Engine\Binaries\Win64\IOS
STRIP=Engine\Binaries\Win64\Lumin
STRIP=Engine\Binaries\DotNET\IOS
```

**Non-Windows deployment and development tools**

```
STRIP=Engine\Extras\Android
STRIP=Engine\Extras\iTunes
STRIP=Engine\Extras\Xcode
STRIP=Engine\Extras\Instruments
STRIP=Engine\Extras\GDBPrinters
STRIP=Engine\Extras\LLDBDataFormatters
STRIP=Engine\Extras\Maya_AnimationRiggingTools
STRIP=Engine\Extras\MayaVelocityGridExporter
```

3ds Max scripts are preserved by default, since 3ds Max is a Windows DCC tool.

**UnrealFileServer**

```
STRIP=Engine\Binaries\Win64\UnrealFileServer.exe
#STRIP=Engine\Source\Programs\UnrealFileServer
```

UnrealFileServer serves cooked and staged files to remote devices and powers network Cook-on-the-Fly. It is
safe to remove if you develop and package only for local Win64, do not deploy to remote devices, do not use
network Cook-on-the-Fly, and do not target consoles or mobile through the file-server workflow.

The prebuilt binary is targeted by default; the source folder is preserved so the tool can be rebuilt later.

**Engine content**

```
STRIP=Samples\StarterContent
STRIP=Samples\MobileStarterContent
STRIP=FeaturePacks\StarterContent.upack
STRIP=FeaturePacks\MobileStarterContent.upack
STRIP=Samples\NGXTest
STRIP=Samples\RTXGI_Test
#STRIP=Samples\PixelStreaming
```

Starter Content is removed per the debloat policy. The NVIDIA test samples are demo content and are
stripped by default; comment their lines out to keep them. `RTXGI_Test` in particular is useful when
verifying [DDGI](DDGI-Dynamic.md). Pixel Streaming is a working feature rather than a demo, so it is kept.

Entries that do not exist in the tree are skipped with a notice, which is harmless.

## The plugin pass

Disabled by default, because plugin needs vary per project:

```
#PLUGIN_LIST=ExcludedPlugins.txt
```

`ExcludedPlugins.txt`, at the engine root, lists roughly 200 engine plugin paths, covering mobile and XR
platforms, source control providers other than the one you use, Chaos plugins (unnecessary since Vite uses
[PhysX](PhysX.md)), enterprise and virtual production tooling, and a large set of experimental plugins.

The file is looked up next to the scripts first, then in the engine root.

<warning>
Read <code>ExcludedPlugins.txt</code> before enabling this pass. It includes entries your project may need
&mdash; <code>Engine/Plugins/Runtime/GameplayAbilities/</code>,
<code>Engine/Plugins/Runtime/ApexDestruction/</code>, <code>Engine/Plugins/Runtime/HairStrands/</code>,
<code>Engine/Plugins/Runtime/Nvidia/</code> (which contains the
<a href="Upscalers.md">DLSS and Streamline plugins</a>) and
<code>Engine/Plugins/Runtime/PhysXVehicles/</code> are all on the list.
<p>
Comment out the lines for anything you use before running the pass.
</p>
</warning>

## Running it

The simplest route is [ViteSetup](ViteSetup.md). Its Express path runs these scripts after the build with
a fixed selection, and its Custom path and menu option 9 open a picker over the same targets. Run the
scripts directly when you want to control `config.txt` yourself.

<procedure title="Debloat an engine installation" id="run-debloat">
    <step>
        Open <code>devops\config.txt</code> and review every uncommented <code>STRIP</code> line. Comment
        out anything you need.
    </step>
    <step>Confirm <code>DRYRUN=1</code> and <code>MODE=move</code>.</step>
    <step>
        Run <code>ueVite-debloat-StripExecute.bat</code> and read the full output. This is the step people
        skip and then regret.
    </step>
    <step>Set <code>DRYRUN=0</code> and run it again. Read the reference check at the end.</step>
    <step>
        Build the engine and open the editor. Confirm your projects still load and the plugins you need
        are present.
    </step>
    <step>
        Once you are confident, delete <code>MOVE_DIR</code> to actually reclaim the space. Until you do,
        the files are still on disk.
    </step>
</procedure>

For a fresh clone, run `ueVite-debloat-SetupSlim.bat` instead of `Setup.bat` so unneeded platform
dependencies are never downloaded in the first place.

## What the Express path strips

ViteSetup's Express path moves, with no prompt beyond the dry-run review:

- every platform folder except Win64
- debug symbols (`.pdb`)
- Starter Content and Mobile Starter Content
- the NVIDIA sample projects `NGXTest` and `RTXGI_Test`
- every template except Third Person, C++ and Blueprint
- **every plugin under `Engine\Plugins\Runtime\VitePlugins` except ACL and MotionSymphony**

The last item is the one to check. It moves FSR 4, Anti-Lag 2, XeSS, the PhysX Instanced Subsystem,
KawaiiPhysics, ImGui, GPA, Automatron and SplashAbilities. If your project uses any of them, take the
Custom path or copy the folders back from `ViteDebloat_Moved`. Express then offers a second, optional pass
over the plugin list, UnrealFileServer, non-Windows tools and platform binaries.

## Debug symbols

`ueVite-debloat-StripDebugSymbols.bat` removes PDB files according to `ExcludedPdbs.txt`. Debug symbols are
a large fraction of a source build's disk footprint.

Keep symbols for anything you might need to debug. Stripping symbols for the engine modules you never step
into is a large saving; stripping symbols for the ones you do turns a readable callstack into hexadecimal.

## Restoring

In `move` mode, `MOVE_DIR` mirrors the engine tree's relative layout. Copy the contents back over the engine
root to restore everything.

To restore only what the build needs, use the validator:

```
powershell -NoProfile -ExecutionPolicy Bypass -File devops\ueVite-debloat-ValidateRefs.ps1 -Restore
```

`-Restore` moves back the modules the editor build references. `-RestoreAll` also restores those needed by
programs, templates and the game target.

If you used `delete` mode, restoration means re-cloning or re-running `Setup.bat`.

## What this does not do

Debloating reduces disk footprint and, through the plugin pass, build time. It does **not** improve runtime
performance &mdash; a plugin that is present but disabled costs nothing at runtime.

For runtime performance, see [Profiling](Profiling.md) and
[Engine Default Changes](Engine-Defaults.md). For build time specifically, removing the added Vite plugins
saved roughly three minutes on a full 15-minute build while Houdini Engine was bundled, and less since the
June Major removed it; see
[Shader Compilation and PSO](Shader-Compilation-And-PSO.md).

## See also

- [ViteSetup](ViteSetup.md)
- [Build from Source](Build-From-Source.md)
- [Engine Default Changes](Engine-Defaults.md)
- [Bundled Plugins](Bundled-Plugins.md)
- [Cache Management](Cache-Management.md)
