# PS5 CPU FPU

<tldr>
<p>
PS5 Zen 2 deletes <code>FP3</code>, turns <code>FP2</code> into a store-only port, and keeps
<b>one 256-bit FMA pipe</b>. AVX2 and FMA latency stay. Series X Zen 2 does not take that cut.
Vite validates FPU-bound work — above all the <b>PhysX 3.4</b> modernisation — on an
<b>AMD 4700S</b>, whose CPU is that further-cut Zen 2, not a desktop Matisse FPU and not Series X.
</p>
</tldr>

The 4700S is in the lab for the CPU, not the GPU. Its Zen 2 is the further-cut FPU relative to Series X
Zen 2. The practical use is to see how FPU-side changes in the PhysX 3.4 libraries behave on a PS5-class
core: island solve, contact generation, constraint prep and integration are FMA-throughput work, and that
is the load Vite is modernising toward.

A desktop Ryzen 3000 FPU will overstate that work. Series X will overstate it too. The 4700S will not.

## Why Series X is the wrong CPU proxy

Scarlett (Series X) is **15.3 billion** transistors. Oberon (PS5) is **10.6 billion**. That is about
**1.4×** the transistor count, often rounded to 50% more. The extra silicon is not only the larger GPU
(52 CUs vs 36). Series X also spends more transistors on the CPU, including a fuller Zen 2 FPU.

PS5 Zen 2 keeps the integer, load/store and out-of-order side of Matisse close to stock, and saves area in
the FPU:

| Port | Desktop Zen 2 / Series X-class | PS5 / 4700S-class |
|---|---|---|
| `FP0` | 256-bit FMA / FMUL | **256-bit FMA / FMUL (the remaining FMA pipe)** |
| `FP1` | 256-bit FMA / FMUL | Non-FMA FP math (FADD and similar) |
| `FP2` | FADD + vector store | **Vector store only** |
| `FP3` | FADD | **Deleted** |
| AVX2 | 256-bit | 256-bit (not a 128-bit FPU executing AVX in two beats) |
| FMA latency | ~5 cycles | ~5 cycles |
| FP physical register file | 160 × 256-bit | 160 × 256-bit |

Steady-state issue versus a Matisse core at the same clock:

| Operation | Desktop Zen 2 | PS5 / 4700S |
|---|---|---|
| Packed FMA (`vfmadd` / `a*b+c`) | **2 × 256-bit / cycle** | **1 × 256-bit / cycle** |
| Packed FADD / FMUL as separate ops | 2 × 256-bit / cycle each | 1 × 256-bit / cycle each |
| Vector store | Shares the FP cluster | Still on `FP2`; does not steal the FMA pipe |
| Packed integer MUL | 1 pipe | Unchanged |
| Packed integer ADD | 3 pipes | ~2 pipes |

Independent FMAs dual-issue on Series X and on a 3700X. They **queue on one pipe** on PS5 and on the 4700S.
FMA + FADD no longer hide on `FP2`/`FP3`. Two accumulators still cover the five-cycle FMA latency; they do
not restore the second FMA unit.

<warning>
Time PhysX and other FPU-bound kernels on the 4700S. A 3700X, a 5800X3D, a 13700K, or Series X silicon
will dual-issue FMA that the PS5 core cannot. Use those chips only to answer "did the compiler get worse?"
</warning>

## Test boxes, and what each one is for

| Machine | Role | Not for |
|---|---|---|
| **AMD 4700S** | Windows + PS5-class CPU FPU. PhysX 3.4, animation SIMD, audio. | GPU. The iGPU is fused off. |
| **AMD 4800S** | Same class of kit; GPU also fused off. | GPU. Do not assume a fuller FPU than the 4700S without measuring it. |
| **RX 6700 RDNA2** | Desktop RDNA2 compiler and throughput proxy. Close enough in performance and architecture to catch shader-compiler behaviour. | Cycle-accurate PS5 GPU. PS5 RDNA2 diverges (cache, RB+, export, primitive shaders, RT ISA). That limits how far a 6700 capture can be trusted as console GPU. |
| **AMD BC-250** | Harvested Oberon-class APU: same FPU family, GPU **works**. | Vite's Windows / D3D12 path. No usable Windows GPU driver, so it is not a practical Editor or Shipping test box. |

The BC-250 is how public microbenchmarks (notably [Chips and Cheese](https://chipsandcheese.com/p/the-nerfed-fpu-in-ps5s-zen-2-cores))
mapped the PS5 FPU. It cannot run Vite Editor. The 4700S can, against the cut FPU, with a discrete GPU
handling the RHI.

<note>
Console platform code stays private. This page is portable SIMD, PhysX 3.4, and a Windows CPU proxy. It is
not a PS5 SDK document. See <a href="Platforms.md">Platforms</a>.
</note>

## PhysX 3.4 is the FPU load

Vite is modernising the **PhysX 3.4** libraries (newer Clang/MSVC, FMA contraction, batched float kernels)
with the PS5 CPU as the optimisation target. That SDK is SSE2/SSE4 over `float` in
`physx::shdfnd::aos` (`Vec3V`, `FloatV`, `V3ScaleAdd`, `V3MulAdd`). Narrow phase, constraint prep,
the PGS solver and integration are packed FMA. They are exactly the kernels that lose the second FMA
pipe.

Chaos ISPC AVX2 paths assume more FPU issue bandwidth than this core has. They are the wrong reference
for this work. Occupancy across the whole step still beats a heroic kernel that never runs — see
[Physics](Physics.md) — but the remaining FMA pipe is the budget the SDK rewrite has to hit.

Rules for that rewrite:

1. **Issue-bound packed FMA is what shrank.** Independent `V3ScaleAdd` / `fmadd` that a 3700X dual-issues
   now wait on one pipe. Keep independent islands and contact batches; do not expect 2 FMA/cycle inside
   one dependency chain.
2. **Contract mul+add to FMA.** `V3ScaleAdd(a, s, b)` (`a * s + b`) is one uop. `V3Scale` then `V3Add`
   is two uops that now compete for the leftover math port. Desktop hid the add on `FP2`/`FP3`. PS5 does
   not.
3. **SoA / `Vec3V` batches, aligned loads.** Scalar `PxVec3` in the inner loop spends issue on inserts
   and scalar stores. `FP2` can still retire vector stores; use it.
4. **AVX2 is legal; it does not restore the second FMA.** A 256-bit FMA doubles floats per instruction
   versus SSE. It still retires at 1/cycle. Do not drop AVX2 because of the old "128-bit FPU" rumour —
   256-bit and 128-bit vector FP drop by about the same factor versus Matisse, which is a 256-bit FPU with
   fewer pipes.
5. **Do not emit AVX-512.** Not present. Hot TUs: `/arch:AVX2` or `-mavx2 -mfma`. Leave Unreal
   `VectorRegister` SSE unless the kernel is explicitly AVX2.
6. **Stay FP32.** Solver, contacts and integration are `float`. FP64 halves SIMD occupancy again. LWC
   doubles do not belong in this path.
7. **Validate on the 4700S with SMT on** (PS5 ships SMT on). Ratio:
   `time_4700S / time_3700X` at matched clocks. Toward 1.0 means you removed FMA traffic. Stuck near 2×
   means you only added ILP the extra desktop FMA pipe was eating.

### Probe: confirm one FMA pipe

Independent `_mm256_fmadd_ps` should sit at **~1 cycle/uop** on the 4700S and **~0.5 cycle/uop** on
desktop Zen 2 at the same clock. Dependent-chain (same accumulator) should sit at **~5 cycles/uop on
both**. If a "win" only appears on the dependent test, you hid latency; you did not recover PS5 FPU
throughput.

```cpp
#include <immintrin.h>
#include <stdint.h>

#if defined(_MSC_VER)
#include <intrin.h>
static uint64_t Ticks() { return __rdtsc(); }
#else
static uint64_t Ticks()
{
	uint32_t Lo, Hi;
	__asm__ volatile("rdtsc" : "=a"(Lo), "=d"(Hi));
	return (uint64_t(Hi) << 32) | Lo;
}
#endif

float ProbeFmaThroughput(uint32_t Iters)
{
	__m256 A = _mm256_set1_ps(1.0001f);
	__m256 B = _mm256_set1_ps(1.0002f);
	__m256 Acc0 = _mm256_set1_ps(1.0f);
	__m256 Acc1 = _mm256_set1_ps(1.0f);
	__m256 Acc2 = _mm256_set1_ps(1.0f);
	__m256 Acc3 = _mm256_set1_ps(1.0f);

	const uint64_t T0 = Ticks();
	for (uint32_t I = 0; I < Iters; ++I)
	{
		Acc0 = _mm256_fmadd_ps(Acc0, A, B);
		Acc1 = _mm256_fmadd_ps(Acc1, A, B);
		Acc2 = _mm256_fmadd_ps(Acc2, A, B);
		Acc3 = _mm256_fmadd_ps(Acc3, A, B);
	}
	const uint64_t Dt = Ticks() - T0;

	Acc0 = _mm256_add_ps(Acc0, Acc1);
	Acc0 = _mm256_add_ps(Acc0, Acc2);
	Acc0 = _mm256_add_ps(Acc0, Acc3);
	alignas(32) float Out[8];
	_mm256_store_ps(Out, Acc0);

	(void)Out;
	return float(Dt) / float(Iters * 4u); // ~1.0 on 4700S, ~0.5 on Matisse
}
```

Compile that TU with `/arch:AVX2` or `-mavx2 -mfma`.

### Solver-shaped FMA: `V3ScaleAdd`, not scale-then-add

PhysX 3.4 already has the fused form. Use it. A PGS delta on a batched normal impulse is one FMA per
lane; splitting it wastes the pipe the 4700S does not have a spare of.

```cpp
#include "PsVecMath.h"
using namespace physx::shdfnd::aos;

// deltaV = deltaV + n * (impulse * invMass)   — one FMA, not V3Scale + V3Add
inline void ApplyNormalImpulse(
	Vec3V& DeltaLin,
	const Vec3V N,
	const FloatV Impulse,
	const FloatV InvMass)
{
	const FloatV S = FMul(Impulse, InvMass);
	DeltaLin = V3ScaleAdd(N, S, DeltaLin);
}

// BAD on this FPU: two math uops, FADD can no longer hide on FP2/FP3
inline void ApplyNormalImpulseSplit(
	Vec3V& DeltaLin,
	const Vec3V N,
	const FloatV Impulse,
	const FloatV InvMass)
{
	const Vec3V Tmp = V3Scale(N, FMul(Impulse, InvMass));
	DeltaLin = V3Add(DeltaLin, Tmp);
}
```

Integrate the same way: `x += v * dt` is `V3ScaleAdd`, not a scalar `PxVec3` loop. `FP2` still takes the
vector store.

```cpp
void IntegrateLinearSoA(
	PxF32* RESTRICT Px, PxF32* RESTRICT Py, PxF32* RESTRICT Pz,
	const PxF32* RESTRICT Vx, const PxF32* RESTRICT Vy, const PxF32* RESTRICT Vz,
	PxF32 Dt,
	PxU32 Count)
{
	const FloatV VDt = FLoad(Dt);
	const PxU32 Padded = Count & ~3u;
	PxU32 I = 0;

	for (; I < Padded; I += 4)
	{
		Vec3V P = V3LoadA(Px + I); // SoA: load X of four bodies; same for Y/Z in real code
		Vec3V V = V3LoadA(Vx + I);
		P = V3ScaleAdd(V, VDt, P);
		V3StoreA(P, Px + I);
		(void)Py; (void)Pz; (void)Vy; (void)Vz;
	}

	for (; I < Count; ++I)
	{
		Px[I] += Vx[I] * Dt;
		Py[I] += Vy[I] * Dt;
		Pz[I] += Vz[I] * Dt;
	}
}
```

The SoA sketch above loads one component per call; a real kernel uses three `Vec3V` lanes or an AoSoA
block of four bodies. The point is FMA + aligned vector store, not the toy layout.

### What not to put in the SDK hot path

```cpp
// Scalar PxVec3 in the solver inner loop — insert/extract plus scalar stores
for (PxU32 I = 0; I < Count; ++I)
{
	PxVec3 V = Bodies[I].linearVelocity;
	V.z += gravityZ * dt;
	Bodies[I].linearVelocity = V;
}

// Separate mul and add when V3ScaleAdd exists
Vec3V Tmp = V3Scale(N, Impulse);
Delta = V3Add(Delta, Tmp);

// FP64 in a per-body kernel
PxF64 X = PxF64(p.x) + PxF64(v.x) * dt;

// Assuming AVX2 restores Series X / Matisse dual FMA
// Acc0 and Acc1 independent fmadd — desktop/SX: 2/cycle; PS5/4700S: 1/cycle
```

## How to test PhysX FPU work on the 4700S

<procedure title="Validate a PhysX 3.4 FPU change against the PS5 CPU" id="fpu-4700s-physx">
    <step>
        Guard codegen-global changes. See
        <a href="Compile-Time-Switches.md">Compile-Time Switches</a>.
    </step>
    <step>
        Build the modernised PhysX 3.4 libs and the engine Test/Shipping target with identical ISA flags
        on the 4700S and on a desktop Zen 2 box (<code>/arch:AVX2</code> or <code>-mavx2 -mfma</code>
        on the kernel TUs).
    </step>
    <step>
        Run the FMA probe. Confirm ~1 cycle per independent FMA on the 4700S before trusting the box.
    </step>
    <step>
        Time the actual SDK path: <code>stat physics</code>, island/contact/solver breakdown, ETW.
        Do not use a 13700K Insights capture as the PS5 number.
    </step>
    <step>
        Report <code>time_4700S / time_3700X</code> at matched clocks, SMT on. Toward 1.0: less FMA
        traffic. Stuck near 2×: extra ILP that only the second desktop FMA pipe was eating.
    </step>
    <step>
        Re-run the scene GPU-bound on the RX 6700. If frame time did not move, the scene was not CPU-FPU
        bound — keep the SDK change only if the 4700S physics capture still needs it.
    </step>
</procedure>

Pin clocks if the kit boosts. Do not compare 8C/16T 4700S numbers to a 16-core desktop and call it FPU.

## GPU testing stays on the 6700

The 4700S and 4800S cannot answer GPU compiler questions. Their GPUs are fully cut down.

The RX 6700 is close in performance and architecture to PS5 RDNA2, which is enough to inspect **GPU
compiler behaviour**. PS5 RDNA2 still differs from PC RDNA2 (cache hierarchy, RB+, export path, primitive
shaders, RT intersection ISA, last-level cache). Those differences cap how far a 6700 trace can stand in
for the console GPU.

The BC-250's GPU works, on Oberon-class silicon, but it is not usable for Windows D3D12. That blocks
practical Vite Editor and Shipping tests. Do not plan GPU validation around it.

## See also

- [PhysX](PhysX.md)
- [Physics](Physics.md)
- [System Requirements](System-Requirements.md)
- [Performance Targets](Performance-Targets.md)
- [Profiling](Profiling.md)
- [Coding Guidelines](Coding-Guidelines.md)
- [Platforms](Platforms.md)
