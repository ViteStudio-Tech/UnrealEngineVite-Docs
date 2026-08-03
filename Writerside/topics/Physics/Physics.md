# Physics

<tldr>
<p>
Vite keeps <b>PhysX</b> as its physics backend rather than migrating to Chaos. It also retains
Apex Destruction and Apex Cloth, adds NVIDIA Blast, and ships an instanced physics subsystem for
mass rigid-body simulation.
</p>
</tldr>

Physics is the clearest example of Vite's general argument: the older system is faster, more predictable and
better supported by existing content, so Vite keeps it.

## What is in this section

| Topic | Covers |
|---|---|
| [PhysX](PhysX.md) | Why PhysX rather than Chaos, and what that means for your project |
| [Fixed Timestep](Fixed-Timestep.md) | Deterministic fixed-step simulation with render interpolation |
| [Destruction and Cloth](Destruction-And-Cloth.md) | Apex Destruction, Apex Cloth and NVIDIA Blast |
| [Instanced Physics Subsystem](Instanced-Physics.md) | Simulating thousands of rigid bodies through ISM components |

## The short version

Unreal Engine 5 replaced PhysX with Chaos. Chaos is architecturally more ambitious &mdash; it is built for
large-scale destruction, networked physics and deterministic replay. It is also, at the workloads most games
actually run, slower than the PhysX implementation it replaced.

Vite's [cost analysis](UE4-Versus-UE5-Cost-Analysis.md) covers the measurements. The summary is that for the
common case &mdash; a few hundred rigid bodies, character movement, some ragdolls, some vehicles &mdash;
PhysX does the work in less time.

Beyond raw performance, keeping PhysX means:

- **Apex Destruction and Apex Cloth keep working.** Both were deprecated and eventually removed in UE5.
  Existing destructible meshes and APEX clothing assets load and simulate in Vite.
- **PhysX-era content and knowledge transfer directly.** Physics assets, constraint setups, collision
  profiles and the accumulated body of workarounds all still apply.
- **Behaviour is stable.** Chaos changed simulation behaviour across UE5 point releases in ways that
  required content retuning. The PhysX behaviour in Vite is the behaviour 4.27 shipped with.

## Practical starting points

<procedure title="Set up physics for a new project" id="physics-setup">
    <step>
        Leave the default PhysX configuration alone. It is the tested path.
    </step>
    <step>
        Review <b>Project Settings &gt; Engine &gt; Physics</b> for substepping. Enabling substepping with a
        sensible <b>Max Substep Delta Time</b> and <b>Max Substeps</b> improves stability for fast-moving
        or heavily constrained bodies.
    </step>
    <step>
        If your project needs deterministic simulation &mdash; replays, networked physics, reproducible
        test results &mdash; read <a href="Fixed-Timestep.md">Fixed Timestep</a> before building content
        around variable-step behaviour.
    </step>
    <step>
        If you plan to simulate large numbers of small objects (debris, shells, foliage knock-down), read
        <a href="Instanced-Physics.md">Instanced Physics Subsystem</a> rather than spawning individual
        actors.
    </step>
</procedure>

## Reference workloads

Two demo projects exist specifically to measure physics behaviour:

- [Physics Cube Bench](Physics-Cube-Bench.md) &mdash; rigid body throughput
- [PhysX Instanced Subsystem demo](PhysX-Instanced-Subsystem.md) &mdash; the instanced path at scale
- [400 Characters CMC Bench](400-Characters-CMC-Bench.md) &mdash; character movement cost, which is closely
  tied to physics query cost

## See also

- [UE4 versus UE5 Cost Analysis](UE4-Versus-UE5-Cost-Analysis.md)
- [Performance Targets](Performance-Targets.md)
- [Profiling](Profiling.md)
