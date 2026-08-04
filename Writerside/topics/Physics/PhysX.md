# PhysX

<tldr>
<p>
Vite uses NVIDIA PhysX as its physics backend, not Chaos. This is a deliberate performance decision, and it
is the reason Apex Destruction and Apex Cloth still work.
</p>
</tldr>

PhysX is the physics engine Unreal Engine used from UE3 through UE4.27. Unreal Engine 5 replaced it with
Chaos. Vite stays on PhysX.

## The decision

Chaos was built to solve problems PhysX did not: large-scale fracture with the Chaos Destruction system,
deterministic networked physics, and a physics solver Epic owns outright rather than licenses. Those are
real engineering goals and Chaos is a serious piece of work.

They are not, however, goals that improve frame time for a typical game. For the workloads most projects
actually run, the Chaos solver does the same job as PhysX for more CPU time. Vite's
[cost analysis](UE4-Versus-UE5-Cost-Analysis.md) documents the measurements.

Since Vite's entire premise is hitting high frame rates at native resolution on console-class hardware, and
since physics runs on the game thread where Vite is already fighting for budget, the cheaper solver wins.

<img src="ChaosVsPhysX3000.png" alt="3000 simulated cubes side by side, Unreal 5.7 Chaos at 33.26 FPS against Vite PhysX 3.4 at 157.88 FPS" border-effect="line"/>

*3000 simulated cubes, same scene, same hardware. Unreal 5.7 with Chaos (left) 33.26 FPS at a 30.07 ms
frame; Vite with PhysX 3.4 (right) 157.88 FPS at a 6.33 ms frame. Game thread time is 30.01 ms against
6.03 ms &mdash; the gap is almost entirely solver cost.*

At a lower body count the ratio narrows but does not close: the
[Physics Cube Bench](Physics-Cube-Bench.md) measures 75.45 FPS against 148.44 FPS at 1400 cubes.

## What you get by staying on PhysX

**Apex Destruction and Apex Cloth.** Both are PhysX-era NVIDIA systems. UE5 deprecated and then removed
them; there is no migration path for existing destructible mesh or APEX clothing assets. In Vite they
continue to work. See [Destruction and Cloth](Destruction-And-Cloth.md).

**Stable behaviour.** PhysX simulation behaviour in Vite is what 4.27 shipped. Content tuned against it
stays tuned. Chaos changed behaviour meaningfully across UE5 point releases, and projects that shipped
content tuned against one version found it behaving differently in the next.

**Mature tooling.** The PhysX Visual Debugger works. Physics asset tooling, constraint setup and collision
authoring are the workflows the entire 4.27 ecosystem was built around.

**A large body of existing solutions.** Fifteen years of accumulated knowledge about PhysX behaviour in
Unreal &mdash; how to stop ragdolls exploding, how to tune vehicle suspension, which constraint
configurations are stable &mdash; applies directly.

## What you give up

Being straightforward about the trade:

- **Chaos Destruction's geometry collections and fields.** Vite offers [Blast](Destruction-And-Cloth.md)
  instead, which is a different system with different authoring, not a drop-in equivalent.
- **Chaos Vehicles.** Vite has the 4.27 PhysX vehicle system.
- **Chaos Cloth.** Vite has Apex Cloth and the 4.27 clothing tools.
- **Networked physics determinism as a first-class feature.** Vite's answer is
  [fixed timestep simulation](Fixed-Timestep.md), which is an optional compile-time feature rather than a
  built-in architectural property.

## Configuration

Physics settings live under **Project Settings > Engine > Physics**. The settings that matter most:

| Setting | Notes |
|---|---|
| Default Gravity Z | `-980.0` for the standard 1 uu = 1 cm scale |
| Substepping | Off by default. Enable for stability with fast bodies or complex constraints. |
| Max Substep Delta Time | Smallest timestep the substepper will use |
| Max Substeps | Upper bound on substeps per frame. Prevents a slow frame becoming a death spiral. |
| Simulate Skeletal Mesh on Dedicated Server | Usually off. Skeletal physics on the server is expensive and rarely needed. |
| Default Degrees Of Freedom | Constrain to a plane for 2D or 2.5D games |

Substepping deserves attention. Without it, physics steps once per frame with the frame's delta time, so
simulation quality varies with frame rate &mdash; a body that behaves correctly at 120&nbsp;fps may tunnel
through geometry at 30. Substepping fixes this at a CPU cost proportional to the number of substeps.

For projects that need this to be exact rather than merely better, see
[Fixed Timestep](Fixed-Timestep.md).

## Profiling physics

| Command | Shows |
|---|---|
| `stat physics` | Overall physics time, broken down by phase |
| `stat game` | Physics time in the context of total game thread time |
| `p.NumPhysScenes` | Scene count |
| `show Collision` | Collision geometry in the viewport |

The number to watch is physics time as a fraction of game thread time. Physics runs on the game thread, and
[the game thread is where UE4-era engines usually bottleneck first](UE4-Versus-UE5-Cost-Analysis.md). If
physics is consuming a large share of a 16.6&nbsp;ms budget, the fix is usually reducing simulated body
count or moving debris to the [instanced subsystem](Instanced-Physics.md), not tuning solver iterations.

## See also

- [Fixed Timestep](Fixed-Timestep.md)
- [Destruction and Cloth](Destruction-And-Cloth.md)
- [Instanced Physics Subsystem](Instanced-Physics.md)
- [UE4 versus UE5 Cost Analysis](UE4-Versus-UE5-Cost-Analysis.md)
- [Physics Cube Bench](Physics-Cube-Bench.md)
