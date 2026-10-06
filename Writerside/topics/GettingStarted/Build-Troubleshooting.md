# Build Troubleshooting

<tldr>
<p>
Most build failures on Vite are toolchain failures wearing a disguise. Before investigating anything else,
confirm you have exactly one MSVC toolset and one Windows SDK installed, matching
<a href="Toolchain-Requirements.md">Toolchain Requirements</a>.
</p>
</tldr>

This page collects the errors that come up most often, what they actually mean, and how to clear them.

## Toolchain errors

### `error C4668: '__has_feature' is not defined as a preprocessor macro`

This is the signature error of a toolchain mismatch. Unreal Engine 4.27 predates the MSVC version you have
installed, and UBT has selected a toolset whose preprocessor behaviour the engine's headers do not expect.

**Fix.** Install a supported MSVC version, remove the others, and pin the SDK in `BuildConfiguration.xml`.
See [Toolchain Requirements](Toolchain-Requirements.md). Regenerate project files after changing anything.

### UnrealBuildTool picks the wrong compiler or SDK

UBT autodetects by scanning installed toolsets and generally prefers the newest. When you have several
installed, that is often not the one you want.

**Fix.** Pin both explicitly in `%APPDATA%\Unreal Engine\UnrealBuildTool\BuildConfiguration.xml`:

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <WindowsPlatform>
        <Compiler>VisualStudio2022</Compiler>
        <WindowsSdkVersion>10.0.26100.0</WindowsSdkVersion>
    </WindowsPlatform>
</Configuration>
```

Then run `GenerateProjectFiles.bat` again. Watch the build log just before linking to confirm the toolchain
UBT reports is the one you intended.

### `ViteSetup.bat` refuses to continue with a `[FAIL]` line

The assistant enforces its toolchain requirements deliberately and offers no bypass. The failing line names
the missing component. It accepts Visual Studio 2022 with MSVC 14.44 or newer, or Visual Studio 2026 with
MSVC 14.50 or newer, and in both cases Windows SDK 10.0.26100 at subversion .7705 or higher. An older MSVC
toolset or SDK subversion is the usual cause; update it through the Visual Studio Installer. See
[Toolchain Requirements](Toolchain-Requirements.md).

### C# tool projects fail to build (SwarmAgent, NetworkProfiler, UnrealControls)

These target .NET Framework 4.5, whose targeting pack modern Visual Studio installers no longer ship.

**Fix.** Install it, as described in [Toolchain Requirements](Toolchain-Requirements.md). A `v4.5` folder
containing only XML files is a runtime stub, not a targeting pack &mdash; check for
`v4.5\RedistList\FrameworkList.xml`.

## Dependency and setup errors

### `Setup.bat` fails to download dependencies

In stock Unreal Engine 4.27 this happens because the GitDeps endpoints have moved. **Vite already ships the
fix**, so if you are seeing download failures on this fork, the cause is environmental: a proxy, a firewall,
or an interrupted earlier run leaving a corrupt cache.

**Fix.** Delete the `UE4_Source_Cache` folder in the repository root and run `Setup.bat` again.
`ViteSetup.bat` removes this cache automatically after a successful setup.

### `Setup.bat` asks to overwrite local changes

Answer `N`. Answering `Y` reverts fork-specific files to their upstream state and will break the build.

### Missing `astcenc.exe` or other third-party tools in a Win64 build

You excluded the Win32 folders during setup. Win64 installed builds depend on tools that live under Win32,
including `ARM\Win32\astcenc.exe`.

**Fix.** Re-run `Setup.bat` without any `-exclude=Win32` argument. The `ViteSetup.bat` presets never exclude
Win32 for this reason.

## Compile and link errors

### Out of memory or heap exhaustion during compilation

Unreal's unity build system compiles very large translation units and parallelises aggressively. On machines
with high core counts and modest RAM, the default parallelism can exhaust memory.

**Fix.** Limit parallel actions in `BuildConfiguration.xml`:

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ParallelExecutor>
        <MaxProcessorCount>12</MaxProcessorCount>
    </ParallelExecutor>
</Configuration>
```

### The editor builds but fails to launch

Confirm all three targets were built: `UE4Editor`, `ShaderCompileWorker` and `UnrealLightmass`. Building
only the editor target produces a binary that starts and then fails as soon as it needs to compile a shader.

### Stale shaders or derived data after pulling engine changes

Rendering changes invalidate the shader cache. If you see shader compilation errors, missing materials or
visual corruption after a pull, wipe the engine-level caches:

```batch
WipeShaderCache.bat
```

This removes `Engine\DerivedDataCache`, `Engine\Intermediate\Shaders` and `Engine\Saved\ShaderDebugInfo`.
The engine rebuilds them on the next launch, which will take a while. Close the editor and any
`ShaderCompileWorker` processes first, or the deletion will fail. See
[Cache Management](Cache-Management.md).

## Runtime issues after a successful build

### A new project runs much slower than expected

New projects have ray tracing support and Dynamic DDGI enabled by default, so an empty project already
traces rays every frame. On GPUs without hardware ray tracing, or on low-end hardware, DDGI is the first
thing to check. Ray-traced reflections, shadows and ambient occlusion default to off; if they are running,
a project setting or post-process volume enabled them.

**Fix.** Profile with `stat gpu`, then disable what you do not need: `r.GlobalIllumination.ExperimentalPlugin 0`
for DDGI, or the individual `r.RayTracing.*` variables. See [Ray Tracing](Ray-Tracing.md) and
[Dynamic DDGI](DDGI-Dynamic.md).

### Gameplay behaves differently from stock 4.27

Vite changes several engine defaults for performance, and some of them affect behaviour rather than just
frame time &mdash; overlap events are disabled by default on primitive components, for instance.

**Fix.** Read [Engine Default Changes](Engine-Defaults.md) in full. Every changed default is listed there
with a link to the commit that changed it.

## Getting help

If none of the above applies, the `#support` channels on the
[community Discord](https://discord.gg/n9zQrYFhMb) are the fastest route. Include your Visual Studio
version, MSVC toolset version, Windows SDK version, the branch you are building, and the first error in the
log rather than the last &mdash; Unreal's build output cascades, and the final error is rarely the useful
one.

## See also

- [Toolchain Requirements](Toolchain-Requirements.md)
- [Building from Source](Build-From-Source.md)
- [Cache Management](Cache-Management.md)
- [Engine Default Changes](Engine-Defaults.md)
