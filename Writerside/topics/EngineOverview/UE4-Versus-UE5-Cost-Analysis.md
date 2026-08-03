# UE4 versus UE5 Cost Analysis

<tldr>
<p>
The performance gap is not one system. It is shader instruction counts, physics, character movement,
memory, Slate, skeletal meshes, tick cost, render thread structure, the loss of Blueprint nativization,
and volumetric shaders &mdash; each contributing independently.
</p>
</tldr>

This page documents where the measured cost differences between Unreal Engine 4.27 and modern UE5 come
from. It exists because "UE5 is slower" is not actionable; knowing *which* subsystem regressed and by how
much is what lets you decide whether a fork is worth maintaining.

Supporting measurements are collected in a
[public spreadsheet](https://docs.google.com/spreadsheets/d/1TabQV7UTDLMHI9GVFCbMzXohax2Agm2qzET7tOOXN7w/edit?usp=sharing).

## Materials and shaders

From UE 5.1, Shader Model 6 became the preferred rendering path, and general shader instruction count
increased significantly for both the SM5 and SM6 paths. Subsequent versions expanded both instruction counts
and permutation counts further.

Unreal Engine 4.27 produces lighter-weight shaders that deliver the same visual result, which translates
directly into faster GPU time across the board &mdash; not just in scenes that use the new features.

<img src="https://github.com/user-attachments/assets/5bf7e5c8-1342-4cb6-a1af-a96fed1ddab6" alt="Shader instruction count comparison" width="2518" height="1231"/>

## Physics

Chaos is significantly slower than PhysX across many workloads, largely from less efficient SIMD
utilisation, comparatively poor multithreading, and generally less efficient engineering decisions.

Internal stress tests show Chaos performing over 5x slower than PhysX in heavily physics-bound scenarios.
The gap is not limited to rigid body simulation: it also affects physics queries, collision calculation and
transform propagation, which means projects that make little or no explicit use of physics simulation still
pay a measurable CPU cost.

The practical consequence is scale. The same CPU budget buys substantially more complex cloth simulation and
destruction under PhysX. See [PhysX Overview](PhysX.md).

## Character Movement Component

CMC has become progressively more expensive. Against Unreal Engine 5.6, version 4.27 performs 2.2&ndash;2.8x
faster in movement and collision calculations, and that figure does not even account for PhysX's faster
sweeps.

This dominates scenes with many players or AI characters, and directly limits the feasible scale of
simulation. The [400 Characters CMC Bench](400-Characters-CMC-Bench.md) scene exists to measure exactly
this.

## Memory

Overall memory usage has increased with each engine iteration. In a typical multiplayer map scene, Vite uses
approximately 1 GB less total memory than UE 5.7, measured on the Stylized demo.

On memory-constrained targets &mdash; handhelds, Switch 2, base consoles &mdash; a gigabyte is not a
rounding error. It is often the difference between a texture pool that holds and one that thrashes.

## Slate and UI

From UE 5.0, Slate's rendering cost increased considerably, alongside a more complex system for handling
Slate object updates, layout calculation and transformations. The rendering of UI itself became more
expensive in the pursuit of higher UI rendering fidelity.

For UI-heavy games &mdash; which is most of them, once you count HUDs, inventories and menus &mdash; this is
a persistent per-frame cost that never goes away.

## Skeletal meshes

Skeletal meshes became more complex around 5.1 to 5.4. The base cost of a skeletal mesh component in 4.27 is
far lighter.

This matters disproportionately because skeletal meshes are frequently the worst CPU offenders in a shipped
game. Vite additionally ships an optimised skeletal mesh configuration as the default &mdash; see
[Engine Default Changes](Engine-Defaults.md).

## World tick and game thread

Newer UE5 iterations increased the general cost of the ticking systems, and made physics, Niagara and
controller ticks heavier to run. This is a flat tax on every frame, independent of what your game does.

## Render thread

With the deeper integration of Lumen, Nanite, VSM, Virtual Textures, TSR, Substrate, Chaos Cloth and Hair,
the render thread became larger and more fragmented, and PSOs became heavier. This affects overall renderer
performance in every circumstance, not only when those features are enabled.

## Loss of Blueprint nativization

This one is frequently overlooked and is often the largest single factor in real projects.

The Blueprint VM is a slow runtime. For simple gameplay logic it is typically 50&ndash;80x slower than
equivalent native C++. For algorithmic workloads &mdash; sorting, node operations, pathfinding &mdash; it can
be 150&ndash;400x slower.

In Unreal Engine 4, Blueprint Nativization mitigated this by converting Blueprint bytecode into native C++
during packaging, producing code roughly 10x faster than VM execution. UE5 removed the feature.

Because most Unreal projects rely heavily on Blueprints &mdash; especially through plugins and third-party
code that you do not control &mdash; retaining nativization can make UE4's game thread substantially faster
in real-world projects, reducing input latency, improving responsiveness and allowing higher simulation
scale.

## Volumetrics, fog and engine shaders

There is a large performance regression in the systems and materials handling volumetrics, fog and sky, and
in many other default engine shaders. The increased shader complexity compounds on top of the base material
cost increases described above.

<img src="https://github.com/user-attachments/assets/5147cb2c-fa33-4ef7-83e8-59833c5b9dd4" alt="Volumetric and fog cost comparison" width="2559" height="1386"/>

<img src="https://github.com/user-attachments/assets/2d913d08-15ad-478d-bb04-371ebdd986da" alt="Engine shader cost comparison" width="2544" height="1156"/>

## Core class base costs

Beyond any individual system, the base cost of core engine classes increased in both execution time and
memory footprint, across both game and render logic.

<img src="https://github.com/user-attachments/assets/bf6497f6-ed1b-48bb-b5ca-27a856da3842" alt="Core class base cost comparison" width="686" height="732"/>

## Reading these numbers honestly

A few caveats worth stating, because they affect how you should use this page.

These are comparisons of engine baselines and specific benchmark scenes, not of shipped games. A UE5 title
that avoids Nanite and VSM and uses a conservative material setup will not exhibit the full gap. Conversely,
a Vite project that enables the entire ray tracing suite on a low-end GPU will not hit the numbers in
[Performance Targets](Performance-Targets.md) either.

The argument Vite makes is about *where the baseline sits* &mdash; what you pay before you have built
anything. A lower baseline leaves more of the frame for the game.

## See also

- [Why NvRTX 4.27](Why-NvRTX-427.md)
- [Performance Targets](Performance-Targets.md)
- [Engine Default Changes](Engine-Defaults.md)
- [Profiling and Benchmarking](Profiling.md)
