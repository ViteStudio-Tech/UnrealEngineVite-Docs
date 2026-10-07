# Fixed Timestep

<tldr>
<p>
An optional Vite feature that steps PhysX at a fixed rate independent of frame rate, with render
interpolation so motion stays smooth. Compile-time switch <code>VITE_PHYSX_FIXED_TIMESTEP</code>
(default <code>0</code>), runtime CVar <code>p.VitePhysXFixedTimestep.Enabled</code>.
</p>
</tldr>

By default, Unreal steps physics with the frame's delta time. A frame that took 8&nbsp;ms steps physics by
8&nbsp;ms; a frame that took 33&nbsp;ms steps by 33&nbsp;ms. Simulation results therefore depend on frame
rate, which means the same input produces different outcomes on different hardware, and a replay recorded on
one machine does not reproduce on another.

Vite's fixed timestep mode decouples the two. Physics always advances in identical increments, and
components are placed between the two most recent physics states to keep motion smooth.

## Enabling

This is a two-stage opt-in. The feature is compiled out by default.

<procedure title="Enable fixed timestep physics" id="enable-fixed-timestep">
    <step>
        Set <code>VITE_PHYSX_FIXED_TIMESTEP</code> to <code>1</code>. See
        <a href="Compile-Time-Switches.md">Compile-Time Switches</a> for how to override it without
        editing <code>CoreDefines.h</code>.
    </step>
    <step>Rebuild the engine.</step>
    <step>
        Set <code>p.VitePhysXFixedTimestep.Enabled 1</code> at runtime, or in
        <code>DefaultEngine.ini</code>.
    </step>
    <step>
        Enable substepping in <b>Project Settings &gt; Engine &gt; Physics</b>. The fixed-step
        implementation runs through the substepping path.
    </step>
</procedure>

The compile-time gate exists because the feature changes hot paths in the physics scene, the substep task
and the animation physics blend. Projects that do not need determinism should not pay for the extra branches
and the double-buffered transform storage.

## Console variables

All of these exist only when `VITE_PHYSX_FIXED_TIMESTEP` is compiled in.

| CVar | Default | Range | Purpose |
|---|---|---|---|
| `p.VitePhysXFixedTimestep.Enabled` | `0` | 0/1 | Master enable |
| `p.VitePhysXFixedTimestep.DeltaTime` | `0.01667` (1/60) | 0.0013&ndash;1.0 | Fixed simulation step in seconds |
| `p.VitePhysXFixedTimestep.MaxTimesteps` | `16` | 1&ndash;50 | Maximum fixed steps per game tick before overload accumulates |
| `p.VitePhysXFixedTimestep.MaxCumulativeExtraSteps` | `50` | 0&ndash;100 | Cumulative overload budget before the limit policy applies |
| `p.VitePhysXFixedTimestep.LimitType` | `0` | 0/1 | `0` clamp fixed steps, `1` fall back to variable substeps |
| `p.VitePhysXFixedTimestep.InterpolationMode` | `1` | 0/1/2 | `0` disabled, `1` per component, `2` always |

## How it works

The implementation keeps a time bank. Each game tick adds the frame's delta to the bank, then runs as many
whole fixed steps as fit. The remainder stays in the bank for the next tick.

Because a fast frame may fit zero fixed steps and a slow frame may fit several, three things are handled
differently from stock substepping.

**Buffers are not rotated on frames with no physics step.** Standard substepping swaps the physics target
buffers every tick. In fixed-step mode the swap happens only when a step will run, so one-shot forces,
kinematic targets and custom physics callbacks queued during a zero-step frame wait for the next step instead
of being discarded.

**Custom physics callbacks are queued once.** Because the buffer can now live across several frames, a
component that registers the same custom physics delegate every frame would otherwise stack up copies of it.
Fixed-step mode adds each delegate to a body's queue only once.

**Results are only fetched when a step occurred.** `fetchResults` is skipped on frames with no simulation,
avoiding redundant work and stale transform reads.

## Overload handling

If the game cannot keep up &mdash; a long hitch, or a physics load too heavy for the fixed rate &mdash; the
bank grows faster than it drains. Left alone this becomes a death spiral: each frame takes longer, which
queues more steps, which makes the next frame longer still.

`MaxTimesteps` is the number of steps a tick may run without counting as overload. Every step beyond it adds
one to an overload counter, and every tick that runs fewer steps pays the counter back down. While the
counter stays within `MaxCumulativeExtraSteps`, all the steps that fit in the bank run. When a tick would push
it past that budget, `LimitType` decides what happens, and the log reports `Fixed Timestep limits exceeded`:

| `LimitType` | Behaviour | Use when |
|---|---|---|
| `0` &mdash; Clamp | Runs only the steps the budget allows (at most `MaxTimesteps` once the budget is used up). The rest of the time stays in the bank and is stepped through on later ticks. | Every step must have the same size: replays, deterministic tests |
| `1` &mdash; Variable substeps | Empties the bank and steps this tick with Unreal's normal variable substeps, using **Max Substep Delta Time** and **Max Substeps** from the physics settings. Fixed stepping resumes once the counter drops back under the budget. | Keeping up with real time matters more: general gameplay |

Under sustained overload, Clamp makes physics fall behind real time and then catch up, at most
`MaxTimesteps` steps per tick, once the load drops. Every step keeps the same size. Variable substeps keep
physics in step with real time but break the fixed step size for the ticks where the fallback engages.

## Render interpolation

Fixed stepping at 60&nbsp;Hz while rendering at 120&nbsp;fps would show each physics state twice without
interpolation, producing visible judder. Each body stores its two most recent stepped transforms
(`PreviousPhysicsTransform` and `LatestPhysicsTransform`). When physics results are synced back to
components, an interpolated component is placed between the two by the fraction of a step left in the bank.
The component therefore lags the simulation by up to one step: `GetComponentLocation` returns the blended
position, while the body itself stays at the latest physics state. Location is interpolated linearly and
rotation spherically; scale is not interpolated. Teleports and other explicit `SetBodyTransform` calls reset both stored transforms, so a
teleported body does not smear across the jump.

`InterpolationMode` controls which components are interpolated:

- **`0` Disabled.** Bodies snap to the latest physics state. Cheapest, and correct if your render rate
  matches your fixed step rate exactly.
- **`1` Per component (default).** Interpolates only components whose `bInterpolateFixedTimestep` is set.
  It is a C++ member of `UPrimitiveComponent`, off by default and not exposed to Blueprint or the Details
  panel, so with the default mode nothing interpolates until your code turns it on for the components that
  need it.
- **`2` Always.** Interpolates every simulated body.

Skeletal mesh physics blending reads the same interpolated transforms, so ragdolls and physics-blended
animation follow the skeletal mesh component's setting.

```cpp
// In the constructor of an actor whose simulated mesh should move smoothly under fixed stepping
#if VITE_PHYSX_FIXED_TIMESTEP
    Mesh->bInterpolateFixedTimestep = true;
#endif
```

## Choosing a step rate

`DeltaTime` is the central tuning decision.

| Step rate | Value | Notes |
|---|---|---|
| 30&nbsp;Hz | `0.03333` | Cheapest. Acceptable for slow, heavy objects. Fast bodies will tunnel. |
| 60&nbsp;Hz | `0.01667` | Default. Good general choice. |
| 120&nbsp;Hz | `0.00833` | Better for fast projectiles and tight constraints. Roughly double the CPU cost. |

Physics cost scales linearly with step rate, so 120&nbsp;Hz stepping costs about twice 60&nbsp;Hz. Pick the
lowest rate that keeps your fastest-moving simulated bodies stable, and use CCD rather than a higher step
rate to solve isolated tunnelling problems.

> Choose the step rate early and do not change it after content is tuned. Physics content &mdash; impulse
> magnitudes, constraint stiffness, damping values &mdash; is implicitly tuned against the step rate.
> Changing it late means retuning everything.
>
{style="warning"}

## When to use this

**Use fixed timestep for** replays, automated tests that assert on physics outcomes, networked physics that
compares client and server results, and anything else where the same input should give the same simulation.

A fixed step removes frame rate from the equation, but PhysX still only repeats a result exactly for the same
sequence of API calls on the same platform and build. Also turn on **Enable Enhanced Determinism** in
**Project Settings &gt; Engine &gt; Physics**, so that adding or removing unrelated actors does not change
the outcome, and do not count on bit-identical results across different CPUs or platforms.

**Do not use it for** projects with no reproducibility requirement. The default variable-step path is cheaper
and the compile-time switch defaults to off for that reason.

## See also

- [PhysX](PhysX.md)
- [Compile-Time Switches](Compile-Time-Switches.md)
- [Instanced Physics Subsystem](Instanced-Physics.md)
- [Profiling](Profiling.md)
