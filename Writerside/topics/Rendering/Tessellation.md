# Tessellation and Displacement

<tldr>
<p>
Hardware tessellation with world displacement, deprecated in 4.26 and removed in Unreal Engine 5, still works
in Vite. Set the material's <b>D3D11 Tessellation Mode</b> and drive the <b>World Displacement</b> and
<b>Tessellation Multiplier</b> pins. Ray tracing sees the undisplaced base mesh.
</p>
</tldr>

Tessellation subdivides geometry on the GPU and displaces the resulting vertices along a displacement map,
producing real geometric detail in the rasterised passes: silhouettes change, and surfaces self-occlude and
cast displaced shadow-map shadows. Ray-traced effects are the exception; see
[Interaction with ray tracing](#interaction-with-ray-tracing).

## Why this page exists

Epic deprecated hardware tessellation in 4.26 and Unreal Engine 5.0 removed it. Nanite solves a different
problem: it renders very dense authored meshes efficiently. Later UE5 releases added an experimental Nanite
tessellation path for displacement, but it works only on Nanite meshes and the UE5 renderer, neither of which
4.27 has.

The workflows that break without tessellation:

- **Terrain and landscape displacement** driven by a heightmap, where the detail is procedural and
  view-dependent rather than baked into a mesh.
- **Runtime displacement** &mdash; snow accumulation, footprints, deformation, water surfaces &mdash; where
  the displacement changes during play.
- **Texture-driven detail on tiling surfaces**, where a single material adds real depth to brick, cobble or
  bark across many meshes without authoring unique high-poly geometry for each.
- **Memory-constrained detail**, where a heightmap is dramatically cheaper than the equivalent dense mesh.

Vite keeps the entire 4.27 tessellation pipeline intact, which means these workflows still work.

## Enabling tessellation on a material

The settings are in the material's **Tessellation** category.

<procedure title="Set up a displaced material" id="setup-tessellation">
    <step>
        Set <b>D3D11 Tessellation Mode</b>. <b>Flat Tessellation</b> subdivides without smoothing the base
        surface; <b>PN Triangles</b> smooths the base surface as it subdivides. PN Triangles is usually what
        you want on organic shapes; Flat is correct when the base silhouette should be preserved exactly.
    </step>
    <step>
        Connect a scalar to <b>Tessellation Multiplier</b>. This controls how much subdivision the surface
        receives. Drive it from distance so that far geometry is not subdivided.
    </step>
    <step>
        Connect a vector to <b>World Displacement</b>. The usual form is the vertex normal multiplied by a
        heightmap sample multiplied by a displacement scale.
    </step>
    <step>
        Leave <b>Adaptive Tessellation</b> on (the default) to scale subdivision by screen-space triangle
        size, and turn on <b>Crack Free Displacement</b> if the mesh shows cracks along its UV seams.
    </step>
</procedure>

## Global controls

| CVar | Default | Effect |
|---|---|---|
| `r.TessellationAdaptivePixelsPerTriangle` | `48.0` | Target screen-space triangle area in pixels for materials using adaptive tessellation |

Lowering the value produces smaller triangles and more subdivision; raising it produces fewer. It is a
useful global scalability lever: expose it through your scalability groups so that lower quality presets
back off tessellation across the whole project without touching individual materials.

## Cost and control

Tessellation is not free, and the failure mode is severe: an unbounded tessellation multiplier on a large
surface can generate millions of triangles and collapse frame rate.

**Always bound the multiplier by distance.** The standard pattern multiplies the tessellation factor by a
distance falloff so that only nearby surfaces are subdivided:

- Sample `Camera Position` and the object or pixel world position.
- Compute distance, remap it through a `Divide` and `Saturate` into a 0&ndash;1 falloff.
- Multiply the falloff into the tessellation multiplier.

**Watch triangle density directly.** The wireframe view mode shows runaway subdivision immediately, and
`stat rhi` reports the triangles drawn.

**Displacement cracks** appear at UV seams and mesh boundaries where adjacent vertices displace by
different amounts. Turn on **Crack Free Displacement** in the material (off by default), make the heightmap
continuous across the seam, or mask displacement to zero at boundaries.

**Culling.** Bounds come from the undisplaced mesh, so geometry displaced far outside them can pop out at the
edge of the screen or in shadows. Raise the component's **Bounds Scale** for strongly displaced meshes.

## Interaction with ray tracing {id="interaction-with-ray-tracing"}

Ray tracing does not see tessellation. The acceleration structure is built from the base mesh; for static
meshes it can evaluate World Position Offset (when the component's **Evaluate World Position Offset** ray
tracing setting is on), but it never runs the tessellation stages or applies World Displacement. To
ray-traced [reflections](RT-Reflections.md), [shadows](RT-Shadows-And-Ambient-Occlusion.md) and
[DDGI](DDGI-Dynamic.md) probe rays, a tessellated brick wall is as flat as a parallax-mapped one.

What that means in practice:

- **Reflections** show the flat base surface. At glancing angles on a strongly displaced surface the
  mismatch with the primary view is visible.
- **Ray-traced shadows** are cast by the flat surface and land on the displaced one, so strong displacement
  can show self-shadowing errors and light leaks where the two disagree. Keep displacement amplitude modest
  on surfaces that receive ray-traced shadows, or turn off **Cast Ray Tracing Shadows** on the light that
  shows the problem so it uses shadow maps, which do see the displacement.
- **DDGI** probe rays work at probe resolution, where the difference rarely matters.
- If the flat stand-in is worse than nothing, untick **Visible in Ray Tracing** on the component to remove it
  from ray-traced effects entirely.

When ray-traced effects must see the shape, author it into the mesh, or for large, smooth deformation use
World Position Offset with the component's ray tracing evaluation enabled.

## Alternatives

Tessellation is the right tool when you need real geometry. When you do not:

| Technique | When it is enough |
|---|---|
| Normal mapping | Lighting detail only; silhouette and self-occlusion do not matter |
| Parallax occlusion mapping | Convincing depth from the primary view, no geometry cost |
| Authored high-poly meshes | Static detail, known in advance, memory budget allows it |
| **Tessellation** | Silhouette or shadow-map shadows matter, or displacement changes at runtime. Ray tracing still sees the base mesh. |

## See also

- [Rendering](Rendering.md)
- [Ray Tracing](Ray-Tracing.md)
- [UE4 versus UE5 Cost Analysis](UE4-Versus-UE5-Cost-Analysis.md)
- [Shading Models](Shading-Models.md)
