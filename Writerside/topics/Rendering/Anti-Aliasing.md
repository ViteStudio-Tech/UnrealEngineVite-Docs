# Anti-Aliasing

<tldr>
<p>
Vite adds <b>SMAA</b> as a fourth anti-aliasing method alongside None, FXAA, TemporalAA and MSAA. SMAA is
recommended for the highest raw image quality, especially in competitive titles. Vite also improves
<b>UE4's TAA</b>, with better stability, better colour reproduction on materials (glossy ones in
particular) and sharper textures.
</p>
</tldr>

Anti-aliasing is where Vite’s rendering philosophy is most apparent. Unlike Epic’s Unreal Engine 5, Vite renders at native resolution by default and targets high frame rates. Its antialiasing solution therefore prioritizes temporal stability while preserving the image-quality benefits of a full native 4K output, 
whose higher pixel density already reduces aliasing compared with lower internal resolutions. Compared with UE5, Vite effectively uses supersampling when the two engines are evaluated at the same output resolution but different internal rendering resolutions.

<note>
Epic’s UE 5.8 defaults to an internal resolution with only one quarter of the target pixel count &mdash; a
50% scale on each axis. This behaviour appears across several rendering paths: even when TSR is disabled,
the engine may fall back to another non-native scaling method, such as TAAU or basic spatial upscaling. Vite
has no such behaviour; it always defaults to the full native screen resolution.
When comparing Vite with UE5, always verify that both engines are rendering at the same native internal 
resolution. Use stat unit to confirm the active resolution and performance characteristics.
</note>

## Available methods

The **Anti-Aliasing Method** setting under **Project Settings > Engine > Rendering > Default Settings**
offers:

| Method | Enum | `r.DefaultFeature.AntiAliasing` | Notes                                                                                                |
|---|---|---|------------------------------------------------------------------------------------------------------|
| None | `AAM_None` | 0 | Aliased. Useful for comparison and for debugging AA artefacts.                                       |
| FXAA | `AAM_FXAA` | 1 | Cheap post-process filter. Blurs texture detail along with edges. Vite's FXAA is higher quality and faster than stock (March Major). |
| TemporalAA | `AAM_TemporalAA` | 2 | Improved over UE4 TAA in quality and stability. Resolves aliasing well, at a cost in sharpness. |
| MSAA | `AAM_MSAA` | 3 | Forward shading only. Sample count via `r.MSAACount`. |
| **SMAA** | `AAM_SMAA` | **4** | Vite's recommended method. Spatial, no history buffer, four quality levels. |

## SMAA

Subpixel Morphological Anti-Aliasing analyses the image for edge patterns and blends across them
geometrically. It is a spatial technique: it looks at one frame and resolves the aliasing in that frame.

That single property is why it fits Vite. Temporal techniques accumulate samples across frames, which is
what produces ghosting behind moving objects, smearing on fast camera motion, and the general softness that
makes TAA output look like it is rendered behind a thin layer of vaseline. SMAA has no history buffer, so it
has none of those failure modes. What it gives up is subpixel detail reconstruction &mdash; it cannot
recover information that was never rendered &mdash; which matters much less when you are rendering at native
4K in the first place.

Vite's first SMAA implementation measured 32% faster than CMAA2 in Unreal Engine, which is why CMAA2 was deemed
redundant.
Other morphological solutions were evaluated, and none offered an objective reason to be implemented in
Vite. The implementation has gone through two generations:

| Release | Implementation |
|---|---|
| [March Major](ueVite26-MarchMajor.md) to [July Major](ueVite26-JulyMajor.md) | Vite compute SMAA: three compute passes with the SMAA maths inlined, quality set by `r.Vite.SMAA.Mode` |
| [August Major](ueVite26-AugustMajor.md) onwards | Port of Epic's UE 5.7 SMAA pipeline: edge detection, blending weight calculation stencil-masked to edge pixels only, and neighbourhood blending, with four quality levels and selectable edge detection |

The reference SMAA algorithm itself is unchanged from upstream. What Vite keeps from its own implementation
is the asynchronous loading of the SMAA area and search textures, which avoids loading texture assets from
the render thread. 

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
| `r.SMAA.Quality` | `2` | `0` = Low, `1` = Medium, `2` = High, `3` = Ultra |
| `r.SMAA.EdgeMode` | `0` | `0` = colour edge detection, `1` = luminance edge detection |

`r.SMAA.Quality` is marked `ECVF_Scalability`, so it can be driven from scalability groups. High is the
default and is what the [performance targets](Performance-Targets.md) assume; Low and Medium exist for the
lower scalability buckets where the difference in edge quality is a reasonable trade for the frame time.
Colour edge detection catches edges between colours of similar brightness; luminance detection is slightly
cheaper and finds fewer false edges in noisy textures.

<note>
<p>
Releases up to <a href="ueVite26-JulyMajor.md">July Major</a> use <code>r.Vite.SMAA.Mode</code>
(<code>0</code> = Low, <code>1</code> = High) and <code>r.AntiAliasing.SMAA.Debug</code> instead. Rename
them in your config files when you move to August or later; the old names are silently ignored.
</p>
</note>

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
| `r.SMAA.DebugVisualization` | `0` = off, `1` = edge texture, `2` = blend weights, `3` = scene colour with the smoothed edges highlighted |

Edge visualisation is the fastest way to diagnose SMAA that appears to be doing nothing (usually the method
is not actually selected) or is over-blurring (usually excessive high-frequency content in the source image,
often from an aggressive sharpening or noise post-process).

## Aliasing that anti-aliasing will not fix

Some aliasing is authored in rather than introduced by rasterisation, and no regular AA method resolves it:

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
