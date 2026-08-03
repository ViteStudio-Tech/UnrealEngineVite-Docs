# Anti-Aliasing

<tldr>
<p>
Vite adds <b>SMAA</b> as a fifth anti-aliasing method alongside None, FXAA, TemporalAA and MSAA. SMAA is
the recommended default: it removes aliasing without the ghosting, smearing and temporal instability that
make TAA unacceptable at native resolution.
</p>
</tldr>

Anti-aliasing is where Vite's rendering philosophy is most visible. The engine renders at native resolution
and targets high frame rates, which means the anti-aliasing solution must not introduce the temporal
artefacts that modern engines accept as the price of reconstruction.

## Available methods

The **Anti-Aliasing Method** setting under **Project Settings > Engine > Rendering > Default Settings**
offers:

| Method | Enum | `r.DefaultFeature.AntiAliasing` | Notes |
|---|---|---|---|
| None | `AAM_None` | 0 | Aliased. Useful for comparison and for debugging AA artefacts. |
| FXAA | `AAM_FXAA` | 1 | Cheap post-process filter. Blurs texture detail along with edges. |
| TemporalAA | `AAM_TemporalAA` | 2 | Stock UE4 TAA. Ghosting and smearing under motion. |
| MSAA | `AAM_MSAA` | 3 | Forward shading only. Sample count via `r.MSAACount`. |
| **SMAA** | `AAM_SMAA` | **4** | **Added by Vite. Recommended.** |

## SMAA

Subpixel Morphological Anti-Aliasing analyses the image for edge patterns and blends across them
geometrically. It is a spatial technique: it looks at one frame and resolves the aliasing in that frame.

That single property is why it fits Vite. Temporal techniques accumulate samples across frames, which is
what produces ghosting behind moving objects, smearing on fast camera motion, and the general softness that
makes TAA output look like it is rendered behind a thin layer of vaseline. SMAA has no history buffer, so it
has none of those failure modes. What it gives up is subpixel detail reconstruction &mdash; it cannot
recover information that was never rendered &mdash; which matters much less when you are rendering at native
4K in the first place.

### Enabling SMAA

```ini
; Config/DefaultEngine.ini
[/Script/Engine.RendererSettings]
r.DefaultFeature.AntiAliasing=4
```

Or per-camera through the post process volume's **Anti-Aliasing Method** override, or at runtime:

```
r.DefaultFeature.AntiAliasing 4
```

### Quality

| CVar | Default | Values |
|---|---|---|
| `r.Vite.SMAA.Mode` | `1` | `0` = Low, `1` = High |

Marked `ECVF_Scalability`, so it can be driven from scalability groups. High quality is the default and is
what the [performance targets](Performance-Targets.md) assume; Low exists for the lowest scalability bucket
where the difference in edge quality is a reasonable trade for the frame time.

### Where SMAA runs in the pipeline

Vite applies SMAA **before tonemapping**, unlike FXAA which runs after. This is deliberate: resolving edges
in linear HDR space avoids the tonemapper amplifying partially-resolved edge pixels into visible fringing on
high-contrast boundaries, which is a common complaint about post-tonemap SMAA implementations.

The practical consequence is that post-process materials in the **After Tonemapping** blend location see an
already-anti-aliased image, and that SMAA composes correctly with HDR output.

### Debugging

In non-Shipping builds:

| CVar | Values |
|---|---|
| `r.AntiAliasing.SMAA.Debug` | `0` = off, `1` = show detected edges, `2` = show blend weights |

Edge visualisation is the fastest way to diagnose SMAA that appears to be doing nothing (usually the method
is not actually selected) or is over-blurring (usually excessive high-frequency content in the source image,
often from an aggressive sharpening or noise post-process).

## The other methods

**FXAA** remains available and is the cheapest option. Vite exposes `r.AntiAliasing.FXAA.ExtraSharpness`
(default `0`), which anti-aliases less but preserves more sharpness and geometry, and is roughly 1.5&times;
faster than standard FXAA. If you need AA on a very tight budget, FXAA with extra sharpness is a reasonable
low-end fallback.

**TemporalAA** is stock UE4.27 TAA. It is not removed, and it is still the correct choice if your project
depends on temporal accumulation for a specific effect. But it is not what Vite's rendering targets are
built around, and enabling it re-introduces the temporal artefacts the SMAA path exists to avoid.

**MSAA** requires forward shading. Vite's default configuration is deferred, so MSAA is not applicable to
the standard path.

## Choosing

<procedure title="Pick an anti-aliasing method" id="pick-aa">
    <step>
        Start with SMAA at High quality. For native-resolution rendering this is the intended configuration.
    </step>
    <step>
        If frame time is tight at the low end of your hardware range, drop <code>r.Vite.SMAA.Mode</code> to
        <code>0</code> before considering a different method.
    </step>
    <step>
        If that is still too expensive, fall back to FXAA with
        <code>r.AntiAliasing.FXAA.ExtraSharpness 1</code>.
    </step>
    <step>
        Only choose TemporalAA if you have a specific dependency on temporal accumulation, and accept the
        ghosting that comes with it.
    </step>
</procedure>

## Aliasing that anti-aliasing will not fix

Some aliasing is authored in rather than introduced by rasterisation, and no AA method resolves it:

- **Specular aliasing** from high-frequency normal maps on smooth materials. Fix with proper mip generation
  and normal-to-roughness conversion, not with AA.
- **Texture aliasing** from missing or badly generated mips. Fix in the texture import settings.
- **Alpha-test shimmer** on foliage. Consider dithered opacity, or reduce the alpha-tested surface area.

Diagnose these by switching to `AAM_None` and looking at where the aliasing appears. Aliasing that moves
with the surface rather than sitting on silhouette edges is a content problem.

## See also

- [Rendering](Rendering.md)
- [Upscalers and Frame Generation](Upscalers.md)
- [Performance Targets](Performance-Targets.md)
- [Colour Management](Color-Management.md)
