# Cache Management

<tldr>
<p>
<code>WipeShaderCache.bat</code> at the engine root deletes the engine's derived data cache, intermediate
shaders and shader debug info. Reach for it when the editor's behaviour stops matching your source
changes.
</p>
</tldr>

Unreal caches aggressively. That is what makes iteration bearable, but it also means a stale cache can make
a correct change appear not to work &mdash; or an incorrect one appear to.

## What the script clears

`WipeShaderCache.bat` deletes three directories relative to the engine root. In a source build the first
one is the engine's local DDC, which every project opened with that engine shares.

| Directory | Contents |
|---|---|
| `Engine\DerivedDataCache` | Compiled shaders, cooked textures, built meshes and every other derived artefact |
| `Engine\Intermediate\Shaders` | Intermediate shader compilation output |
| `Engine\Saved\ShaderDebugInfo` | Shader debug symbols and preprocessed source dumps |

It reports each directory as deleted, not found, or failed. A failure almost always means something still
holds a file handle.

<warning>
Close the editor and all <code>ShaderCompileWorker.exe</code> processes before running the script. Shader
compile workers can outlive the editor; check Task Manager if a deletion fails.
</warning>

After wiping, the next editor launch recompiles everything it needs. On a large project this can be tens of
minutes or more. Do not do it casually.

## When to wipe

<deflist>
<def title="You changed a .usf or .ush file and nothing happened">
Shader source changes are usually picked up, but engine-level global shader changes sometimes are not.
Try <code>recompileshaders global</code> or <code>recompileshaders changed</code> in the console first
&mdash; it is far faster than a full wipe.
</def>
<def title="You changed a compile-time switch">
Changing <a href="Compile-Time-Switches.md">VITE_RT_PSO_DEBLOAT</a>, <code>VITE_O_SSAO</code> or any other
<code>VITE_*</code> switch changes which shader permutations exist. The engine rebuild handles the C++,
but cached shaders from the old configuration can linger. Wipe after switching.
</def>
<def title="You pulled engine changes that touched the renderer">
A merge that changes shader code or the shader map keying can leave a cache the engine misreads.
</def>
<def title="You are getting shader compilation errors that do not match the source">
A classic stale-cache symptom: the reported error line does not exist in the file you are looking at.
</def>
<def title="The editor crashes on startup after an engine change">
Worth trying before deeper investigation, since it is cheap to rule out.
</def>
</deflist>

## When not to wipe

Wiping the DDC is a heavy hammer and is frequently applied to problems it cannot solve.

- **Problems in one project.** In a source build the engine DDC holds cached data for every project opened
  with that engine, so wiping it makes all of them recompile. It does not touch the project's own
  `Intermediate` and `Saved` folders or its boot cache, `<Project>\DerivedDataCache\Boot.ddc`, which is
  read before the engine DDC. If one project misbehaves, delete its `Boot.ddc` and `Intermediate` first.
- **Runtime rendering bugs.** If an effect renders wrongly but consistently, that is a code or
  configuration problem, not a cache problem. Check the
  [compile-time switch availability table](Ray-Tracing.md) first &mdash; many ray tracing features are
  compiled out by default and their console variables silently do nothing.
- **Long shader compile times.** Wiping makes this worse, not better. See
  [Shader Compilation and PSO](Shader-Compilation-And-PSO.md).

## Lighter-weight alternatives

Try these before a full wipe:

| Approach | Clears | Cost |
|---|---|---|
| `recompileshaders changed` | Modified shaders only | Seconds |
| `recompileshaders global` | Global shaders | Under a minute |
| `recompileshaders material <name>` | One material | Seconds |
| Delete the project's `Intermediate\` | Project build intermediates | Project rebuild |
| Delete `Engine\Intermediate\Shaders` only | Intermediate shader output, keeping the DDC | Partial recompile |

The last one is worth knowing: the DDC is the expensive part to rebuild. If you only need to clear
intermediate shader state, deleting that one directory by hand is much cheaper than running the full
script.

## Cache locations

For a source build, `BaseEngine.ini` (`[DerivedDataBackendGraph]`) reads caches in this order: the project's
boot cache, any pre-built `DDC.ddp` paks, the engine's local DDC, then a shared DDC if one is configured.

| Cache | Path | Cleared by the script |
|---|---|---|
| Project boot cache | `<Project>\DerivedDataCache\Boot.ddc` (up to 512&nbsp;MB) | No |
| Engine local DDC | `Engine\DerivedDataCache` | Yes |
| Engine intermediate shaders | `Engine\Intermediate\Shaders` | Yes |
| Shader debug info | `Engine\Saved\ShaderDebugInfo` | Yes |
| Project intermediates | `<Project>\Intermediate` | No |
| Shared DDC | None by default; set with the `UE-SharedDataCachePath` environment variable, `-SharedDataCachePath` or Editor Preferences | No |
| Installed (binary) build local DDC | `%LOCALAPPDATA%\UnrealEngine\Common\DerivedDataCache` | No |

The script only clears the default location. If the `UE-LocalDataCachePath` environment variable or the
**Local Derived Data Cache** editor preference points the local DDC elsewhere, delete that folder instead.
On an [installed build](Installed-Builds.md) the local DDC lives under `%LOCALAPPDATA%`, so the script does
not clear it at all.

<note>
If your team uses a shared network DDC, wiping locally is usually pointless: the local cache repopulates
from the share, including whatever stale entries prompted the wipe. Confirm the shared DDC's state before
concluding your local cache was the problem.
</note>

## Disk footprint

The engine DDC grows with every material, texture and ray tracing permutation you build, and on a large
project it can reach tens of gigabytes. The engine deletes files that have not been used for 34 days in the
background (`UnusedFileAge=34`), so it settles around the working set of the projects you open rather than
growing forever. Wiping it reclaims that space at the cost of a full recompile.

If disk space is the actual concern, the [Debloat Guide](Debloat-Guide.md) covers larger and more permanent
savings.

## See also

- [Shader Compilation and PSO](Shader-Compilation-And-PSO.md)
- [Compile-Time Switches](Compile-Time-Switches.md)
- [Build Troubleshooting](Build-Troubleshooting.md)
- [Debloat Guide](Debloat-Guide.md)
