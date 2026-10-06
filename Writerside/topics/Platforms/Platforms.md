# Platforms

<tldr>
<p>
Vite's primary target is 64-bit Windows on DirectX 12, where every feature is built and measured. Android
and Linux receive targeted fixes; other platforms inherit stock 4.27 support. Console work is private.
</p>
</tldr>

Vite is a focused fork. The features that distinguish it &mdash; the NvRTX ray tracing suite, DDGI, RTXDI,
DLSS and its alternatives, HBAO+, hardware tessellation &mdash; are deferred-renderer GPU features aimed at
desktop PCs and current-generation consoles. Platform work outside Windows concentrates on what keeps
projects shipping there: toolchains, compile fixes and the forward (mobile) renderer.

## Support levels

| Platform | Level | Notes |
|---|---|---|
| Windows 64-bit | **Primary** | What everything is built and measured against |
| Windows 32-bit | Support files only | Required by Win64 tooling; not a shipping target |
| Android | Maintained | Android NDK 29 with C++20 fixes, arm32 fixes and Android Vulkan preview in the editor ([March Major](ueVite26-MarchMajor.md)); Meta Quest device profiles and packaging fixes ([LTS](ueVite25-LTS.md)); NEON math upgrades ([June Major](ueVite26-JuneMajor.md)) |
| Linux | Maintained for servers | Server toolchain fix (March), dedicated-server plugin updates ([August Major](ueVite26-AugustMajor.md)), Unix file-layer locking fix ([September Major](ueVite26-SeptemberMajor.md)). The ray tracing suite is untested. |
| Mac | Inherited | Stock 4.27 support. No DXR, so the ray tracing suite does not apply. |
| iOS / tvOS | Inherited | Stock 4.27 support, plus the shared forward-renderer changes |
| HTML5 | Not available | Epic moved HTML5 out of the engine into a community-maintained extension in 4.24. The name survives only as a dependency filter in the setup scripts. |
| Consoles | Private | Console SDKs are under NDA, so console-specific changes cannot be published in this repository |

"Inherited" means the stock 4.27 code is present and has not been deliberately broken, but Vite does not
test it and the fork's rendering features are unavailable or unvalidated there. "Maintained" means Vite
fixes and updates the platform's toolchain and build, without promising the full rendering feature set.

## Enabling other platforms

Platform dependencies are opt-in at setup time.

Through [ViteSetup](ViteSetup.md), tick the platform in the Express path's platform picker, or on the
Custom path choose the **Win64 + Android** or **Win64 + Linux** profile, or use the step-by-step assistant
to toggle platforms individually. **Full setup** passes no `-exclude` argument to `Setup.bat` and
downloads everything.

For the debloat scripts, uncomment the relevant line in `devops\config.txt`:

```ini
# Win64 is always kept. Uncomment a platform to ALSO download and keep
# its dependencies during setup.
#KEEP_PLATFORM=Android
#KEEP_PLATFORM=IOS
#KEEP_PLATFORM=Linux
#KEEP_PLATFORM=Mac
```

<warning>
Adding a platform after the fact requires re-running dependency setup and rebuilding. Decide before your
first build if you can.
</warning>

## Graphics APIs

| API | Status | Notes |
|---|---|---|
| DirectX 12 | **Primary** | Required for DXR, and therefore for everything ray-traced |
| DirectX 11 | Supported | Raster features work; ray tracing does not |
| Vulkan | Inherited | Stock 4.27 support plus Vite stability fixes (August Major); Vite's ray tracing suite is DXR-based |
| Metal | Inherited | Mac and iOS |
| OpenGL ES / Vulkan mobile | Maintained | Android |

### What requires DX12

Everything ray-traced needs DXR, which in Vite means DirectX 12:

- [Ray-traced reflections](RT-Reflections.md), shadows, ambient occlusion and sky light
- [Dynamic DDGI](DDGI-Dynamic.md)
- Per-pixel ray-traced GI, [RTXDI](RTXDI.md), [path tracing](Path-Tracing.md),
  [translucency and caustics](RT-Translucency-And-Caustics.md), if you rebuild with
  `VITE_RT_PSO_DEBLOAT=0`

[FSR 4](Upscalers.md) is also DX12-only, independently of ray tracing.

### What works on DX11

- [HBAO+](Ambient-Occlusion.md) &mdash; it also has a D3D12 back end since the June Major, despite the
  console variable help text
- [SMAA](Anti-Aliasing.md)
- [SSGI](SSGI.md)
- [Hardware tessellation](Tessellation.md)
- The [Callisto BRDF and Toon shading models](Shading-Models.md), when compiled in

A DX11 target is viable if you are willing to give up ray tracing. It is the right choice for a project
whose [performance targets](Performance-Targets.md) do not leave budget for DXR.

## Hardware

See [System Requirements](System-Requirements.md) for development and runtime hardware.

PS5-class CPU work &mdash; especially the PhysX 3.4 modernisation &mdash; is timed on the AMD 4700S, whose
Zen 2 FPU is cut further than Series X's: `FP3` gone, `FP2` store-only, one FMA pipe. GPU compiler checks
use a discrete RX 6700, since the 4700S and 4800S GPUs are fused off and the BC-250 has no usable Windows
D3D12 driver. Detail is in [PS5 CPU FPU](PS5-CPU-FPU.md).

## Packaging

The [installed build](Installed-Builds.md) is produced with Development and Shipping game configurations
for Win64; ViteSetup adds Linux when you tick it. If you need other configurations or platforms, edit the
`RunUAT.bat` BuildGraph arguments:

```
-set:WithLinux=true
-set:GameConfigurations=Development;Test;Shipping
```

Each additional platform and configuration lengthens an already long build considerably.

## See also

- [System Requirements](System-Requirements.md)
- [Installed Builds](Installed-Builds.md)
- [ViteSetup Assistant](ViteSetup.md)
- [Ray Tracing](Ray-Tracing.md)
- [Debloat Guide](Debloat-Guide.md)
