# PhysX Test

<tldr>
<p>
Five PhysX test levels for 4.27: wrecking ball, dominoes, a stirred box of spheres, stacking towers and
falling cubes. Use them to check that a build's physics still behaves after engine changes, and to compare
cost between builds.
</p>
</tldr>

## Download

[PhysicsTest repository](https://github.com/tanger1n/PhysicsTest)

## What it covers

Each level has its own game mode that spawns the scene from C++, so Blueprint overhead does not distort the
timing, and exposes its counts, masses and sizes as properties. An on-screen readout shows the object count
and elapsed time.

| Level | Scenario | What it stresses |
|---|---|---|
| `L_WreckingBall` | A heavy ball hits a brick wall, or the wall collapses under gravity | Impulse transfer, a large simultaneous collapse |
| `L_Domino` | A curved chain of dominoes | Sequential contact propagation and timing |
| `L_FluidParticle` | 500 small spheres in a container, stirred | Broadphase load from many simultaneous contacts |
| `L_TowerStacking` | Cubes dropped from above until the towers collapse, up to 1000+ bodies | Stacking stability, body count |
| `L_CubeFalls` | Basic cube spawning | A baseline |

<img src="PhysXTest1.png" alt="Wrecking Ball level: a ball breaking through a 300-brick wall" border-effect="line"/>

<img src="PhysXTest2.png" alt="Domino level: 200 dominoes falling along an S-curve" border-effect="line"/>

<img src="PhysXTest3.png" alt="Fluid Particle level: 500 spheres settling in a container" border-effect="line"/>

*Wrecking Ball, Domino and Fluid Particle in the editor. Each shows a regression as a visible difference
as well as a number.*

Run it when you have changed something physics-adjacent and want to know whether you broke it; the larger
levels also make a quick before-and-after cost comparison.

## Relevance to Vite

Vite retains PhysX rather than migrating to Chaos, and that choice is only defensible if the PhysX layer
stays correct through engine changes. Anything touching:

- The physics scene or substepping, particularly with
  [`VITE_PHYSX_FIXED_TIMESTEP`](Fixed-Timestep.md) enabled
- Body instance transforms or interpolation
- Collision query paths, which the Character Movement Component uses heavily
- Apex Destruction or Cloth integration

should be verified here before it is considered done. See
[Coding Guidelines](Coding-Guidelines.md) for the verification requirements.

## Fixed timestep testing

If you are evaluating [fixed timestep physics](Fixed-Timestep.md), this project is a reasonable place to
observe the difference. Run Domino or Wrecking Ball at an unlocked frame rate and then with `t.MaxFPS` set to
various values: with the default variable timestep the outcome changes with frame rate, and with fixed
timestep it should not. Avoid Tower Stacking for this comparison when it is set to random cube sizes, since
that changes the result on its own.

Fixed timestep is a compile-time feature that also needs substepping turned on. Without
`VITE_PHYSX_FIXED_TIMESTEP=1` in the build, the `p.VitePhysXFixedTimestep.*` variables do not exist.

## See also

- [PhysX](PhysX.md)
- [Fixed Timestep](Fixed-Timestep.md)
- [Physics Cube Bench](Physics-Cube-Bench.md)
- [Compile-Time Switches](Compile-Time-Switches.md)
