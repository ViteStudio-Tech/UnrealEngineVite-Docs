# Physics

<tldr>
<p>
Vite's physics stack uses <b>PhysX 3.4</b>, with Vite extensions for fixed-timestep simulation,
modern toolchains, NVIDIA Blast and high-count instanced rigid bodies. This page leads with the measured
results, then explains the CPU architecture behind them; the <a href="PhysX.md">PhysX page</a> documents
backend features.
</p>
</tldr>

<img src="ChaosVsPhysX3000.png" alt="In-engine comparison of 3,000 simulated cubes: Unreal 5.7 Chaos at 33.26 FPS against Unreal Vite 26 PhysX 3.4 at 157.88 FPS" border-effect="line"/>

*3,000 engine-managed cubes, same scene, same primitive count. Unreal Engine 5.7 with Chaos (left) runs at
33.26 FPS; Unreal Vite 26 with PhysX 3.4 (right) runs at 157.88 FPS.*

Vite treats physics as a frame-time-critical engine system. Simulation cost includes more than the solver:
broad phase, contact generation, island construction, constraint preparation, iterative solving, integration,
callbacks and synchronization with engine state all contribute to the final physics time.

## Results at a glance

| Workload | Comparison | Vite result |
|---|---|---|
| [3,000 cubes in engine](#cubes-3000) | Unreal 5.7 Chaos vs Unreal Vite 26 PhysX 3.4 | **4.75× the frame rate**, 78.9% lower frame time |
| [Box Container Pile 10K, 1 thread](#box-pile-10k) | Unreal Chaos vs Vite PhysX 3.4 | Chaos takes **29.55× as long** per step |
| [Box Container Pile 10K, 6 threads](#box-pile-10k) | Unreal Chaos vs Vite PhysX 3.4 | Chaos takes **67.34× as long** per step |
| [Box Container Pile 10K, 1–6 threads](#box-pile-10k) | Stock NVIDIA PhysX 3.4 vs Vite PhysX 3.4 | Vite needs **25.2–28.2% less** physics time (1.34–1.39×) |
| [Box Container Pile 10K, 1–6 threads](#box-pile-10k) | Stock NVIDIA PhysX 5.6.1 (CPU) vs Vite PhysX 3.4 | Vite is **1.15–1.44× faster** at every thread count |
| [1,425 native PhysX actors](#native-actors-1425) | Vite native actor path, UE Vite 5.0 build | **374 FPS**, 2.67 ms frame time |

Every number on this page is tied to a named workload, host and build. Read the methodology notes with each
result before quoting it; none of them is a universal PhysX-versus-Chaos multiplier.

## What is in this section

| Topic | Covers |
|---|---|
| [PhysX](PhysX.md) | PhysX 3.4 features, Vite extensions, configuration and profiling |
| [Fixed Timestep](Fixed-Timestep.md) | Fixed-step simulation with render interpolation |
| [Destruction and Cloth](Destruction-And-Cloth.md) | APEX Destruction, APEX Cloth and NVIDIA Blast |
| [Instanced Physics Subsystem](Instanced-Physics.md) | Simulating large rigid-body sets through instanced meshes |

## In-engine cube workload

The [Vite PhysX Cube Test](https://github.com/ViteStudio-Tech/Vite-PhysX-Cube-Test) runs inside Unreal
Engine, so its numbers include the surrounding engine work a shipping game pays for. The public
[cube-spawner implementation](https://github.com/ViteStudio-Tech/Vite-PhysX-Cube-Test/blob/5ae89c3b7b9d6993fdc535a54769e39ca7a116b4/Source/PhysXTest/CubeSpawner.cpp)
creates one `UStaticMeshComponent` per cube, registers it with the engine and enables simulation through
`SetSimulatePhysics(true)`. The spawner itself is a single `AActor`, so this measures an engine-managed
component path rather than 3,000 separately spawned Unreal Actors.

### 3,000 engine-managed cubes {id="cubes-3000"}

The matched capture shown at the top of this page reports 3,000 spawned cubes and 3,016 rendered primitives
in both engine variants. Unlike the Box Container Pile 10K runner below, these values include the
surrounding Unreal runtime work and are not physics-solver milliseconds in isolation.

| Reported metric | Unreal 5.7 — Chaos | Unreal Vite 26 — PhysX 3.4 | Vite relative result |
|---|---:|---:|---:|
| Spawned cubes | 3,000 | 3,000 | Matched |
| Rendered primitives | 3,016 | 3,016 | Matched |
| FPS | 33.26 | 157.88 | **4.75× as high** |
| Frame time | 30.07 ms | 6.33 ms | **78.9% lower** |
| Game time | 30.01 ms | 6.11 ms | **79.6% lower** |

The captured Chaos game time is **4.91×** the Vite PhysX game time, while its frame time is **4.75×** the
Vite PhysX frame time. Game time accounts for almost the complete frame in both captures, so the result is
CPU-side rather than a GPU-limited comparison.

### 1,425 native PhysX actors {id="native-actors-1425"}

<img src="NativePhysXActors1425.png" alt="In-engine Vite native PhysX actor test with 1,425 simulated cubes at 374 FPS" border-effect="line"/>

*Native PhysX actor capture running in Unreal Engine without a separate UE Actor representation for each
simulated cube.*

The native-path capture represents simulated cubes directly as PhysX actors instead of giving every body a
separate Unreal `AActor`. This removes the per-body Unreal Actor lifecycle from the simulation representation
while the scene continues to run and render inside Unreal Engine. Any remaining render representation and
transform-bridge cost depends on the native integration.

| Reported metric | Native PhysX actor path |
|---|---:|
| Engine label | UE Vite 5.0 — PxActors |
| Spawned cubes | 1,425 |
| Rendered primitives | 1,447 |
| FPS | 374.28 |
| Frame time | 2.67 ms |
| Game time | 2.11 ms |

<warning>
Do not calculate a direct multiplier between the native-path capture and the 3,000-cube comparison. The
native result uses 1,425 cubes, a different object representation and a different engine: its on-screen
label reads UE Vite 5.0, Vite's UE5-based PhysX build, not one of the 4.27 releases this manual documents.
It illustrates the lower-overhead native integration path; it is not a matched Chaos-versus-PhysX result.
</warning>

## Box Container Pile 10K benchmark {id="box-pile-10k"}

A deliberately physics-bound pile of **10,005 active rigid bodies and 10,005 shapes**, run headless so the
number is solver time rather than frame time. The metric is median physics milliseconds per frame; lower is
better.

<img src="BoxContainerPile10KVitePhysX.jpg" alt="Box Container Pile 10K benchmark report comparing Vite PhysX 3.4 with stock NVIDIA PhysX 3.4, PhysX 5.6.1 and other physics engines from one to six threads" border-effect="line"/>

*Vite PhysX and comparison-engine report. The shared table below uses only the thread counts reported for
Chaos, NVIDIA PhysX 3.4 and Vite PhysX 3.4.*

### Matching thread-count results

| Reported threads | Unreal Chaos | NVIDIA PhysX 3.4 | NVIDIA PhysX 5.6.1 | Vite PhysX 3.4 | Chaos / Vite | PhysX 3.4 / Vite | PhysX 5.6.1 / Vite |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1,052.09 ms | 49.61 ms | 51.28 ms | 35.60 ms | **29.55×** | **1.39×** | **1.44×** |
| 3 | 1,051.41 ms | 21.98 ms | 20.99 ms | 15.95 ms | **65.92×** | **1.38×** | **1.32×** |
| 4 | 951.36 ms | 18.94 ms | 17.44 ms | 14.17 ms | **67.14×** | **1.34×** | **1.23×** |
| 5 | 857.89 ms | 17.09 ms | 14.90 ms | 12.47 ms | **68.80×** | **1.37×** | **1.19×** |
| 6 | 791.97 ms | 15.82 ms | 13.54 ms | 11.76 ms | **67.34×** | **1.35×** | **1.15×** |

The NVIDIA PhysX 5.6.1 column is the CPU SDK from the same report. Vite's PhysX 3.4 build is faster than
stock PhysX 5.6.1 at every reported thread count from one to six, by 1.15× to 1.44×; the gap narrows as
threads are added, so the comparison favours Vite most on the core counts a console game can dedicate to
physics.

<note>
Chaos had to be benched through Win64, not Headless as the rest of the SDKs.
</note>

Vite PhysX improves from 35.60 ms at one reported thread to 11.76 ms at six, a **3.03× throughput
increase**. NVIDIA PhysX 3.4 improves from 49.61 ms to 15.82 ms, a **3.14× increase**, while Chaos improves
from 1,052.09 ms to 791.97 ms over the same range, a **1.33× increase**. The Chaos report continues to 24
threads and reaches 581.25 ms, **1.81× the throughput of its one-thread result**.

At matching thread counts, Chaos takes **21.21× as long as stock NVIDIA PhysX at one thread** and **50.06×
as long at six threads**. NVIDIA PhysX takes 1.34–1.39× as long as Vite PhysX across the shared thread counts;
equivalently, Vite reduces the reported median physics time by **25.2–28.2%** relative to the NVIDIA PhysX
3.4 baseline. Vite PhysX enters the 16.67 ms budget for 60 Hz at three threads, and NVIDIA PhysX enters it at
six. The reported Chaos result remains outside that budget at 24 threads.

The one-thread result shows that task scaling cannot explain the complete gap: the reported physics time is
already 29.55× as long for Chaos as for Vite PhysX and 21.21× as long for Chaos as for NVIDIA PhysX before
additional worker scaling. The multi-thread results show that scaling widens a difference that also includes
solver work, data access, collision and constraint processing, build configuration and engine integration.
The stock NVIDIA result also separates the base PhysX architecture from the additional improvements in
Vite's PhysX build.

<img src="BoxContainerPile10KChaos.jpg" alt="Unreal Chaos Box Container Pile 10K benchmark report across one to 24 threads" border-effect="line"/>

*Unreal Chaos report. Median physics milliseconds per frame; lower is better.*

### Test configuration

Rendering is removed (except for Chaos), sleeping is disabled and all runs use four solver iterations, a
60 Hz simulation step, 30 warm-up steps and 300 measured steps.

<note>
This is purely a performance test; simulation precision and SDK features should be evaluated separately.
</note>

| Test property | Reported configuration |
|---|---|
| Host | Intel Core i7-13700K (8P+8E / 24 threads), maximum 3.40 GHz |
| Memory | 64 GB DDR5-4800 |
| Platform | Windows 11 Pro for Workstations x64, build 10.0.26200 |
| Workload | Headless; 10,005 bodies; 10,005 shapes; rigid-body sleeping disabled |
| Solver | Four iterations; 60 Hz |
| Sampling | 300 measured steps after 30 warm-up steps |
| Chaos build | Unreal release-branch Chaos Program target; Win64 Shipping; one reported repeat |
| NVIDIA PhysX build | NVIDIA PhysX 3.4; Visual Studio 2026 MSBuild Release; SDK and runner; ten reported repeats |
| Vite PhysX build | Vite PhysX 3.4; clang-cl 22 Release; runtime DLLs; ten reported repeats |

<note>
The reports use the same host and high-level workload settings, but not identical executables: Chaos is a
Win64 Shipping Chaos Program target, NVIDIA PhysX is a Visual Studio 2026 MSBuild Release SDK runner, and
Vite PhysX is a clang-cl 22 Release runtime build. Chaos had to be tested as Win64 because it cannot be
compiled independently of UE5. Cite these values as the <b>reported Box Container Pile 10K result</b>, not
as a universal PhysX-versus-Chaos multiplier.
</note>

## Why the gap exists: physics CPU architecture

### Threading and the critical path

PhysX and Chaos both support multithreaded simulation. Chaos can execute through the Task Graph, use a
dedicated physics thread and parallelize selected particle, collision and island work. A dedicated thread
moves work away from the game thread, but it does not by itself reduce the time between starting and
finishing a simulation step.

Physics contains ordered phases and data dependencies. Constraints within a connected island cannot all be
solved independently, and later stages must wait for the state produced by earlier stages. Scaling therefore
depends on the number and size of independent islands, task granularity, synchronization frequency and the
amount of state transferred between the game and physics representations.

PhysX 3.4 exposes a dependency-linked `TaskManager` and `CpuDispatcher`. Simulation stages create
`LightCpuTask` jobs and submit them to the engine worker pool as their prerequisites complete. Vite's Unreal
integration can batch dispatcher submissions to trade scheduling overhead against available parallelism.
See NVIDIA's [PhysX 3.4 threading documentation](https://docs.nvidia.com/gameworks/content/gameworkslibrary/physx/guide/Manual/Threading.html?highlight=cpudispatcher).

### SIMD coverage

Chaos contains optional Intel ISPC kernels. ISPC is a SIMD technology: it compiles an SPMD program for the
vector units of the target CPU. The relevant constraint is coverage and utilization, not "ISPC versus SIMD."
Only work implemented by an ISPC kernel receives that vector path. Divergent contacts, indirect memory
access, gathers and scatters, heterogeneous constraint types and pointer-heavy data reduce effective lane
occupancy. Intel's [ISPC documentation](https://ispc.github.io/index.html) describes the compiler and its SIMD
execution model.

PhysX's narrow phase and solver were developed around batched float data and platform SIMD kernels. The
useful measurement is effective vector occupancy across the complete simulation step, including work that
remains scalar or loses time to data movement.

On the PS5 CPU that occupancy hits **one 256-bit FMA pipe** (`FP3` deleted, `FP2` stores only), not
desktop or Series X Zen 2's two FMA pipes. FMA-throughput-bound solver work runs at about half a 3700X
at the same clock. Vite's PhysX 3.4 modernisation is timed on the 4700S for that reason. Keep kernels
FMA-fused (`V3ScaleAdd`) and SoA. Do not treat a desktop Ryzen or Series X capture as the PS5 result.
Patterns are in [PS5 CPU FPU](PS5-CPU-FPU.md).

### Numeric precision

UE5 Large World Coordinates changed core world-space types to double precision. Epic's
[LWC documentation](https://dev.epicgames.com/documentation/unreal-engine/large-world-coordinates-in-unreal-engine-5)
explicitly documents double precision in Chaos destruction. This does not mean that every field in every
Chaos subsystem is FP64. Modern Chaos uses mixed precision in selected paths, while the experimental Chaos
implementation in the UE4.27 base aliases its primary `FReal` to `float`.

Double precision remains SIMD-capable. A fixed-width register, however, carries half as many doubles as
floats: a 256-bit register holds four 64-bit values or eight 32-bit values. Double-based fields also require
twice the storage and memory bandwidth of equivalent float fields. In affected kernels this can reduce
theoretical element throughput, increase cache pressure and add conversion work at float/double boundaries.
Epic's [LWC conversion guide](https://dev.epicgames.com/documentation/unreal-engine/large-world-coordinates-project-conversion-guidelines-in-unreal-engine-5)
documents both `VectorRegister4f` and `VectorRegister4d`; the constraint is lane width and data cost, not an
absence of vector instructions.

There is no accurate universal percentage for the FP64 cost. Scalar FP32 and FP64 instructions can have
similar latency on some CPUs, while vector-throughput- or bandwidth-bound kernels can experience a much
larger difference. Any percentage must be attached to a named workload, platform and build.

## Reproducing the comparison

For a controlled engine decision:

1. Pin both engine and benchmark-project commits.
2. Use equivalent compiler optimization, checks, logging and instrumentation.
3. Match collision shapes, material settings, solver iterations, sleeping, timestep and event generation.
4. Record thread affinity and P-core/E-core placement on hybrid CPUs.
5. Publish raw frame samples, median, percentiles and variance.
6. Capture the solver critical path and worker utilization with the appropriate CPU profiler.
7. Repeat with a representative production scene; a fully awake 10,005-body pile is a stress workload.

## Practical starting points

<procedure title="Set up physics for a new project" id="physics-setup">
    <step>
        Review the <a href="PhysX.md">PhysX feature and configuration reference</a>.
    </step>
    <step>
        Configure substepping under <b>Project Settings &gt; Engine &gt; Physics</b> when fast-moving or heavily
        constrained bodies require smaller simulation steps.
    </step>
    <step>
        For a fixed simulation cadence, read <a href="Fixed-Timestep.md">Fixed Timestep</a> before authoring
        systems around variable frame delta.
    </step>
    <step>
        For large sets of debris, shells or other repeated bodies, evaluate the
        <a href="Instanced-Physics.md">Instanced Physics Subsystem</a>.
    </step>
    <step>
        PhysX behaves best with a consistent frame rate. At very high or uneven frame rates, stuttering can
        occur, so cap the FPS for steadier frame pacing. Setting <code>MaxDepenetrationVelocity</code> to
        around 100 can also help reduce stutter caused by uneven frame pacing.
    </step>
</procedure>

## Reference workloads

- [Physics Cube Bench](Physics-Cube-Bench.md) — in-engine rigid-body throughput
- [PhysX Instanced Subsystem demo](PhysX-Instanced-Subsystem.md) — instanced simulation at scale
- [400 Characters CMC Bench](400-Characters-CMC-Bench.md) — character movement and physics-query cost

## See also

- [PS5 CPU FPU](PS5-CPU-FPU.md)
- [PhysX](PhysX.md)
- [UE4 versus UE5 Cost Analysis](UE4-Versus-UE5-Cost-Analysis.md)
- [Performance Targets](Performance-Targets.md)
- [Profiling](Profiling.md)
