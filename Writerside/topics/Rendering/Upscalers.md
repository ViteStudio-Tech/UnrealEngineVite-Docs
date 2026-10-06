# Upscalers and Frame Generation

<tldr>
<p>
Vite bundles NVIDIA DLSS 4.5 with Ray Reconstruction and multi-frame generation, AMD FSR 4 with an FSR 3.1
fallback and vendor-agnostic frame generation, Intel XeSS 3.1 with XeFG, NVIDIA NIS, and the Reflex and
Anti-Lag 2 latency SDKs. They are <b>optional headroom</b>, not the rendering plan: Vite's
<a href="Performance-Targets.md">performance targets</a> are met at native resolution without any of them.
</p>
</tldr>

Check out the [UpscalerTest sample project](https://github.com/ViteStudio-Tech/ueVite-UpscalerTest).

Unreal Engine 5 treats upscaling as mandatory: the renderer is designed around rendering at a fraction of
output resolution and reconstructing the rest. Vite takes the opposite position. The targets are native, and
upscalers are available for users who want to spend the headroom on something else.

That distinction changes how you should use the plugins on this page. If your project only hits its frame
target with DLSS Performance enabled, the project is over budget &mdash; fix that first, then offer
upscaling as an option on top.

## Bundled plugins

All of these ship in the engine repository under `Engine/Plugins/Runtime`. None are enabled by default;
enable the ones your project offers from **Edit > Plugins**. Versions are those in the
[September Major](ueVite26-SeptemberMajor.md).

| Plugin | Version | What it provides | Location |
|---|---|---|---|
| NVIDIA DLSS | 8.7.0-NGX310.7.0 (DLSS 4.5 presets) | Super Resolution, Ray Reconstruction, DLAA | `Nvidia/DLSS` |
| NVIDIA DLSS Frame Generation | 1.3.0 plugin on Streamline SDK 2.12.0 | Frame generation, including multi-frame generation | `Nvidia/Streamline` |
| NVIDIA Reflex | 1.6 | Latency reduction | `Nvidia/Reflex` |
| NVIDIA RTX Dynamic Vibrance | 1.3.0 (Streamline) | Deep-learning dynamic vibrance | `Nvidia/StreamlineDeepDVC` |
| NVIDIA NIS | 1.2.1 | Image Scaling: spatial upscaling and sharpening | `Nvidia/NIS` |
| Movie Render Queue DLSS/DLAA Support | 2.3.3 | DLSS integration for Movie Render Queue | `Nvidia/DLSSMoviePipelineSupport` |
| AMD FSR 4 | 4.1.1 | FSR 4 ML upscaling with an FSR 3.1 fallback, native AA, and frame generation that works with any upscaler; DirectX 12 | `VitePlugins/FSR4-427/FSR4` |
| AMD Anti-Lag 2 | 2.0.4 | Latency reduction on AMD GPUs | `VitePlugins/AntiLag2.0.4` |
| Intel XeSS | 3.1.0 | Xe Super Sampling and XeFG frame generation | `VitePlugins/XeSS_UE4.27_Plugin_v3.1.0` |

FSR 4 and XeSS 3 are notable: both are backports that do not exist in stock 4.27. FSR 4 uses the native
`ffx-api` and requires DirectX 12. The [June Major](ueVite26-JuneMajor.md) introduced most of this set; the
[August Major](ueVite26-AugustMajor.md) moved XeSS to 3.1.0 and the DLSS runtime to NGX 310.7.129.

The FSR 2 plugin from earlier releases is still in the tree as `VitePlugins/FSR2-427`, but its descriptors
are renamed `.uplugin.disabled`, so the engine does not load it. FSR 4's built-in FSR 3.1 path covers the
hardware it served.

<warning>
<p>
The <a href="ViteSetup.md">ViteSetup</a> Express path moves every plugin under
<code>Engine\Plugins\Runtime\VitePlugins</code> except ACL and MotionSymphony to
<code>ViteDebloat_Moved</code>. FSR 4, Anti-Lag 2 and XeSS are among them. If you need them, choose the
Custom path, or copy the folders back from <code>ViteDebloat_Moved</code>. The NVIDIA plugins are not
affected.
</p>
</warning>

### Arbitrary render resolution

`r.Upscaler.ScreenPercentageOverride` lets FSR, DLSS and XeSS take any internal render resolution rather than
only their fixed quality modes. Those plugins own the screen percentage and ignore `r.ScreenPercentage`, so
this is the way to set one: `0` (the default) leaves the quality-mode preset in charge, and `1`&ndash;`100`
forces that screen percentage, clamped to the range the active upscaler supports. Use it for benchmarking
and for exposing a resolution slider.

## Choosing what to ship

You do not need all of them. Each enabled upscaler adds shaders, binaries, package size and a settings menu
entry that has to be tested.

| Situation | Recommendation |
|---|---|
| PC release, broad hardware support | DLSS + FSR 4. Covers NVIDIA and AMD; XeSS if Intel Arc matters to you. |
| NVIDIA-focused, ray tracing heavy | DLSS with Ray Reconstruction |
| Anti-aliasing quality at native resolution | DLAA (part of the DLSS plugin), FSR 4 native AA, or Vite's [SMAA](Anti-Aliasing.md) |
| No upscaling, native only | Ship nothing from this page. This is a valid and supported configuration. |

DLAA is worth calling out separately. It is DLSS's neural network applied at native resolution rather than
as an upscaler, so it competes with SMAA rather than complementing it. It generally resolves finer detail
than SMAA but reintroduces temporal accumulation, and therefore some of the artefacts SMAA avoids. Offer
both and let the player choose.

## Ray Reconstruction

Ray Reconstruction replaces the hand-tuned denoisers for ray-traced effects with a neural denoiser. In a
Vite project this interacts directly with the [ray tracing](Ray-Tracing.md) configuration:

- It can substantially improve [RT reflection](RT-Reflections.md) and [RTXDI](RTXDI.md) quality under
  motion, where hand-tuned denoisers struggle.
- It has no benefit for [DDGI](DDGI-Dynamic.md), which is noise-free by construction and has nothing to
  denoise.

Ray Reconstruction has its own preset console variable, separate from the Super Resolution presets. Preset F
is the DLSS 4.5 model.

If your ray tracing configuration is DDGI-led, Ray Reconstruction buys you less than it would in a
Lumen-based project. Measure before shipping it.

## Frame generation

Three frame generators ship with the engine:

- **DLSS Frame Generation** through Streamline, including DLSS-G multi-frame generation multipliers.
- **FSR frame generation**, driven from the swapchain at present time. It is upscaler-agnostic: it works
  with DLSS, XeSS or native rendering as well as with FSR, and full velocity output is forced whenever any
  frame generator is selected so generated frames do not ghost.
- **XeFG**, Intel's frame generation, enabled on UE 4.27 through XeSS 3.

Frame generation increases displayed frame rate without reducing input latency &mdash; it can make latency
slightly worse. Pair it with **Reflex** on NVIDIA hardware or **Anti-Lag 2** on AMD hardware whenever you
enable it.

> Frame generation works best when the base frame rate is already high. Generating from 30&nbsp;fps to
> 60&nbsp;fps produces visible artefacts around fast-moving UI and thin geometry; generating from
> 60&nbsp;fps to 120&nbsp;fps is far more convincing. Since Vite targets high native frame rates to begin
> with, frame generation is well positioned here &mdash; as a way to push a 4K60 target toward a
> high-refresh display, not as a way to rescue a 30&nbsp;fps one.
>
{style="note"}

## The DLSS translucency patch

Vite includes an optional compile-time patch that addresses a specific quality problem with upscaling:
separate translucency and volumetric fog rendering at the internal render resolution and then being
upscaled, which softens particles, glass and fog against an otherwise sharp reconstructed image.

| Switch | Default | Effect |
|---|---|---|
| `VITE_DLSS_PATCH` | `0` | Adds upscaled-resolution translucency passes and native-resolution volumetric fog |

When enabled, the renderer gains two additional translucency passes,
`TranslucencyAfterDOFUpscaledRT` and `TranslucencyAfterDOFModulateUpscaledRT`, which render selected
translucent primitives at output resolution after upscaling. Primitives opt in through the
`bRenderInTranslucencyUpscaledRTPass` relevance flag, and the passes are only used when a temporal upscaler
is actually active.

It also adds:

| CVar | Default | Effect |
|---|---|---|
| `r.VolumetricFog.UseUpScaledSizeVolumetricFog` | `0` | Computes the volumetric fog grid from the output resolution rather than the internal render resolution |

The switch is defined in `Engine/Source/Runtime/Core/Public/Misc/CoreDefines.h` and defaults to off, since
it costs frame time and only matters for projects that ship with upscaling enabled. See
[Compile-Time Switches](Compile-Time-Switches.md) for how to change it.

## Enabling an upscaler

<procedure title="Add DLSS to a project" id="enable-dlss">
    <step>Open <b>Edit &gt; Plugins</b>, find <b>NVIDIA DLSS Super Resolution/Ray Reconstruction/DLAA</b>, enable it and restart the editor.</step>
    <step>For frame generation, also enable <b>NVIDIA DLSS Frame Generation</b>, and <b>Reflex</b> for latency.</step>
    <step>
        Query support at runtime through the DLSS Blueprint library before exposing the option in your
        settings menu. Hardware and driver support vary, and an option that silently does nothing is worse
        than no option.
    </step>
    <step>Expose quality mode as a player setting rather than forcing one. Include an off state.</step>
    <step>
        Test the interaction with your <a href="Anti-Aliasing.md">anti-aliasing</a> setting. DLSS replaces
        the anti-aliasing pass; leaving SMAA enabled alongside it wastes frame time.
    </step>
</procedure>

## See also

- [Anti-Aliasing](Anti-Aliasing.md)
- [Performance Targets](Performance-Targets.md)
- [Ray Tracing](Ray-Tracing.md)
- [Bundled Plugins](Bundled-Plugins.md)
- [Compile-Time Switches](Compile-Time-Switches.md)
