# Frequently Asked Questions

<tldr>
<p>
The questions that come up most often, with short answers and links to the full explanation.
</p>
</tldr>

## About the fork

### Why 4.27 and not UE5?

Because for a large class of projects UE5's headline features cost more than they return. Nanite, Lumen and
Chaos each carry a base cost whether or not you exploit them, and UE5's core class and tick overhead is
higher. Vite takes 4.27's lower baseline and adds the rendering technology that was actually worth having.

The detailed argument, with numbers, is in [Why NvRTX 4.27](Why-NvRTX-427.md) and
[UE4 versus UE5 Cost Analysis](UE4-Versus-UE5-Cost-Analysis.md).

### Is Vite a drop-in replacement for stock 4.27?

Close, but not exactly. Vite changes a number of engine defaults for performance &mdash; overlap event
handling, skeletal mesh and actor defaults, shadow scalability, tick behaviour and others. A project moving
from stock 4.27 will mostly work, but should read [Engine Default Changes](Engine-Defaults.md) to understand
what changed. `ViteDefaults.bat` can switch the overlap and skeletal mesh defaults back while you migrate.

### Can I use UE5 marketplace assets?

Not directly. The Asset Downgrader plugin converts UE5 assets to 4.27, stripping data that has no 4.27
equivalent such as Nanite geometry. Features that do not exist in 4.27 cannot be ported, only removed. See
[Migrating from UE5](Migrating-From-UE5.md).

### What platforms does Vite support?

Windows 64-bit, primarily on DirectX 12. Android, Linux (servers) and macOS receive toolchain and build work;
other platforms inherit stock 4.27 support but are neither tested nor tuned. Console work is private. See
[Platforms](Platforms.md).

### Do I need an Unreal Engine licence to use Vite?

Yes, the same one every Unreal Engine source build uses. Vite is a 4.27 fork, so source and editor
tools are covered by Epic's [Unreal Engine EULA](https://www.unrealengine.com/eula/unreal). The
project you make with Vite is yours. See [License and Copyright](License-And-Copyright.md).

## Setup and building

### What toolchain do I need?

Vite is currently developed against Visual Studio 2026 with MSVC 14.51 and Windows SDK 10.0.26100.
`ViteSetup.bat` accepts Visual Studio 2026 with MSVC 14.50 or newer, or Visual Studio 2022 with MSVC 14.44
or newer, together with SDK 10.0.26100.7705 or newer; if both Visual Studio versions are installed it asks
which to use. See [Toolchain Requirements](Toolchain-Requirements.md).

### The build fails immediately on a fresh clone

Most often missing .NET Framework 4.5 reference assemblies, which recent Visual Studio installers no longer
include by default. See [Build Troubleshooting](Build-Troubleshooting.md).

### Do I need to build from source?

Only if you need to modify engine C++ or change a [compile-time switch](Compile-Time-Switches.md). For
everything else an [installed build](Install-Binary-Build.md) is faster to get running and needs far less
disk.

### How long does a build take?

A source build is hours on typical hardware, and an installed build is longer. Shader compilation dominates
the first launch afterwards. See [Shader Compilation and PSO](Shader-Compilation-And-PSO.md).

### The engine takes too much disk space

Take the Express path in [ViteSetup](ViteSetup.md), or run the debloat suite in `devops\` yourself. Both
move platform binaries, templates, samples and optionally plugins out of the tree, with a dry-run review
and a recovery folder rather than deletion. See [Debloat Guide](Debloat-Guide.md).

## Rendering

### I set a ray tracing console variable and nothing happened

This is the single most common question, and the answer is almost always
`VITE_RT_PSO_DEBLOAT`. It defaults to `1`, which compiles out the shader permutations for:

- RTXDI (`r.RayTracing.SampledDirectLighting`)
- Path tracing
- Ray-traced translucency and both caustics systems
- Per-pixel ray-traced global illumination
- The non-deferred reflection path, and with it reflected translucency and RT reflection captures

The console variables still exist and still set. Nothing renders. Rebuild the engine with
`VITE_RT_PSO_DEBLOAT=0` to use them. See [Compile-Time Switches](Compile-Time-Switches.md) and
[Ray Tracing](Ray-Tracing.md).

### Which ray tracing features work out of the box?

Dynamic DDGI is enabled by default. Reflections, shadows, ambient occlusion and sky light are compiled
into a default build and can be switched on with their console variables, but start disabled. The rest are
compiled out. Full table in [Ray Tracing](Ray-Tracing.md).

### Which GI should I use?

For most projects, DDGI plus SSGI. DDGI provides the low-frequency indirect bounce and SSGI adds
contact-scale detail its probe grid cannot resolve. Static DDGI is cheaper and correct if nothing moves.
Per-pixel ray-traced GI is reference-only and compiled out by default. See
[Global Illumination](Global-Illumination.md).

### Why SMAA instead of TAA?

TAA's ghosting, smearing and motion softness are structural, not tuning problems. SMAA is spatial and does
not have them. It is Vite's recommended method: select it with `r.DefaultFeature.AntiAliasing=4` and set its quality with `r.SMAA.Quality`. See
[Anti-Aliasing](Anti-Aliasing.md).

### Which upscaler should I use?

DLSS if you are on NVIDIA hardware and shipping to NVIDIA users. FSR 4 (DirectX 12, with its FSR 3.1 path
for older GPUs) or XeSS for cross-vendor coverage. NIS as a cheap fallback with no temporal component. Most
projects should offer more than one. See [Upscalers](Upscalers.md).

### Volumetric fog looks wrong with upscaling enabled

That is what `VITE_DLSS_PATCH` fixes. It adds
`r.VolumetricFog.UseUpScaledSizeVolumetricFog`, which renders fog at output rather than internal
resolution, along with translucency fixes. It defaults to `0`, so it requires a rebuild. See
[Upscalers](Upscalers.md).

### Does Vite have Nanite or Lumen?

No. Those are UE5 systems built on UE5 assumptions, with base costs Vite exists to avoid. Vite's shipping
answers are hardware tessellation and LODs for geometry, and DDGI plus SSGI for global illumination. Its
own successors &mdash; **Vite Vertis** for geometry and **Vite ReSTIR** for GI and real-time path tracing
&mdash; are in development; see the
[Vite Technology](https://vitestudio-tech.github.io/UnrealEngineVite-Docs/tech/) site.

## Physics

### Why PhysX instead of Chaos?

PhysX is faster and more predictable on the workloads Vite targets, and it keeps Apex Destruction and Apex
Cloth &mdash; both removed in UE5 &mdash; available. See [PhysX](PhysX.md).

### How do I get deterministic physics?

Rebuild with `VITE_PHYSX_FIXED_TIMESTEP=1`, then enable
`p.VitePhysXFixedTimestep.Enabled`. Without the compile-time switch the console variables do nothing. See
[Fixed Timestep](Fixed-Timestep.md).

### I need thousands of physics objects

Use the [PhysX Instanced Subsystem](Instanced-Physics.md). Conventional actor-per-body physics hits actor
overhead, not solver limits, at a few thousand bodies. The subsystem removes that overhead by driving
instanced mesh transforms directly.

## Performance

### Can I measure MSVC versus Clang on Compiler Explorer?

No. [Compiler Explorer](https://gcc.godbolt.org/) shows the assembly each compiler emits; it does not
time the generated code. [Quick Bench](https://quick-bench.com/) times GCC or Clang on Linux and has no
MSVC. Time MSVC versus clang-cl locally. See [Compiler Explorer](Compiler-Explorer.md).

### Where do I start optimising?

`stat unit`, and identify which of Game, Draw or GPU is the largest. Optimising the wrong one produces no
frame time improvement at all. See [Profiling](Profiling.md).

### My game thread is the bottleneck

The usual suspects, in rough order of frequency: Character Movement Components, animation evaluation,
Blueprint tick logic, and actor tick overhead generally. See
[400 Characters CMC Bench](400-Characters-CMC-Bench.md) and
[Performance Targets](Performance-Targets.md).

### Shader compilation is taking forever

Check what your permutation count actually is before assuming it is unavoidable. Every shading model in
use, every enabled plugin and every quality level multiplies. `VITE_RT_PSO_DEBLOAT=1` already removes a
large share of the ray tracing permutations, which is why it is the default. See
[Shader Compilation and PSO](Shader-Compilation-And-PSO.md).

### Shaders behave as though my change did not happen

Stale cache. Try `recompileshaders changed` or `recompileshaders global` first &mdash; both are far cheaper
than a full wipe. If neither helps, run `WipeShaderCache.bat`. See
[Cache Management](Cache-Management.md).

## Plugins

### A feature is missing from the editor

Check whether its plugin is enabled. Most bundled plugins default to off. Only RTXGI, ACL and the custom
splash screen are on by default. If the plugin's folder is missing altogether, the ViteSetup Express path
may have moved it to `ViteDebloat_Moved`. See [Bundled Plugins](Bundled-Plugins.md).

### Can I get plugin X bundled?

If it is 4.21&ndash;4.27 compatible, permissively licensed and worth its size and compile cost, propose it.
UE5-only plugins are out of scope. See [Proposed Plugins](Proposed-Plugins.md).

### The debloat script removed a plugin I need

`ExcludedPlugins.txt` is aggressive and includes plugins many projects use. If you ran in move mode, the
files are in `ViteDebloat_Moved` next to the engine folder. If you ran in delete mode, they are gone and
you need to restore from source control. See [Debloat Guide](Debloat-Guide.md).

## Contributing

### What gets a pull request rejected fastest?

Modifying an ABI: ray tracing payload bitfields, shader-visible enums, packed RHI or RenderCore bitmasks,
reflection bitmask definitions, or any CPU/GPU shared struct layout. These are rejected regardless of the
rest of the change. See [Coding Guidelines](Coding-Guidelines.md).

### Can I use recursion, virtuals or templates?

Recursion is banned. New virtuals need strict justification. Templates are discouraged unless they earn
their compile-time and binary-size cost. New Blueprint-exposed functions need explicit approval.

### How do I document my change?

In the same pull request. New console variables go on the relevant feature page, new `VITE_*` switches go
in [Compile-Time Switches](Compile-Time-Switches.md), and changed defaults go in
[Engine Defaults](Engine-Defaults.md). See
[Documentation Contributions](Documentation-Contributions.md).

## See also

- [Console Variables](Console-Variables.md)
- [Glossary](Glossary.md)
- [License and Copyright](License-And-Copyright.md)
- [Compile-Time Switches](Compile-Time-Switches.md)
- [Build Troubleshooting](Build-Troubleshooting.md)
