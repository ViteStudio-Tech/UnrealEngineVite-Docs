# PS5 CPU FPU

<tldr>
<p>
The PlayStation 5 CPU is Zen 2 with a <b>cut-down FPU</b>: two math pipes instead of four, 256-bit AVX2
kept, latencies unchanged. Desktop Ryzen 3000 is the wrong proxy for FPU-bound work. Vite uses the
<b>AMD 4700S</b> as the Windows-accessible stand-in for that FPU, and writes SIMD so it still issues on
two pipes.
</p>
</tldr>

PS5-class GPU numbers on an RX 6700 do not tell you how physics, animation, audio or batch math will behave
on the console CPU. Those kernels live on the floating-point unit, and the PS5 FPU is not a desktop Zen 2
FPU with a lower clock.

## Why the 4700S exists in the test matrix

AMD's 4700S desktop kit is eight Zen 2 cores with the on-die GPU fused off. The cores are the
console-derived cut: mainly the FPU, relative to desktop Zen 2 and to Series X Zen 2. That is the reason
the kit is in the lab. It is not a GPU box.

| Machine | What it is good for | What it is not |
|---|---|---|
| **AMD 4700S** | Windows + PS5-class CPU FPU. Physics, animation, audio, SSE/AVX kernels. | GPU. The iGPU is fused off. |
| **AMD 4800S** | Same class of kit; iGPU also fused off. | GPU testing. Do not treat it as a fuller FPU than the 4700S without measuring it. |
| **RX 6700 / 6700-class RDNA2** | Desktop RDNA2 compiler and throughput proxy for the PS5 GPU. | Cycle-accurate PS5 GPU. Cache, RB+, RT, and several ISA bits differ. |
| **AMD BC-250** | Harvested Oberon-class APU: same FPU family, working RDNA2-derived GPU. | Vite's Windows / DX12 path. No usable Windows GPU driver. |

The BC-250 is how public microbenchmarks (notably [Chips and Cheese](https://chipsandcheese.com/p/the-nerfed-fpu-in-ps5s-zen-2-cores))
characterised the PS5 FPU. It is not a substitute for running Vite Editor or D3D12 shipping builds. The
4700S is the machine that can actually run those builds against the cut-down FPU.

<note>
Console platform code stays private. This page is about portable SIMD and a Windows proxy CPU. It is not a
PS5 SDK document. See <a href="Platforms.md">Platforms</a>.
</note>

## What was actually cut

Desktop Zen 2 has a four-port FPU (`FP0`–`FP3`). Two ports do FMA/MUL, two do FADD, and vector stores share
the cluster. Die shots and 4700S / BC-250 measurements show the console-derived core does this:

- **`FP3` deleted.**
- **`FP2` stores only** — math units removed or folded into `FP0`/`FP1`.
- **Math issue width is two**, not four.
- **256-bit data path and AVX2 remain.** 256-bit and 128-bit vector FP drop by about the same factor versus
  desktop Zen 2, which is the signature of a 256-bit FPU with fewer pipes, not a 128-bit FPU executing AVX
  in two beats.
- **160 × 256-bit FP register file, 36-entry FP scheduler, 64-entry non-scheduling queue, and execution
  latencies are unchanged.**

Approximate steady-state throughput versus a Matisse core at the same clock:

| Operation | Desktop Zen 2 | PS5 / 4700S-class |
|---|---|---|
| Packed FMA (the physics/animation default) | 2 × 256-bit / cycle | **1 × 256-bit / cycle** |
| Packed FADD / FMUL | 2 × 256-bit / cycle each | **1 × 256-bit / cycle each** |
| Vector store | Dedicated-ish | Still on `FP2` — stores do not steal the remaining math pipes |
| Packed integer MUL | 1 pipe (already) | Unchanged |
| Packed integer ADD | 3 pipes | ~2 pipes |
| Scalar integer, branch, load | Full Zen 2 | Full Zen 2 (some integer IPC is slightly *better* than Matisse) |
| FMA latency | ~5 cycles | ~5 cycles |

That split is the whole optimisation problem. A kernel that is FMA-throughput bound runs at about **half**
desktop Zen 2 rate. A kernel that is latency-bound, cache-bound, integer-bound or store-bound often does
not. Games in the large rarely fill four FP pipes; PhysX islands, pose blending, IK, cloth, audio
convolution and procedural animation do.

<warning>
A Ryzen 7 3700X, a 5800X3D or a 13700K will lie about FPU-bound speedups. If the optimisation is for the
PS5 CPU, time it on the 4700S. Use the desktop chip only to answer "did the codegen get worse?"
</warning>

## What this means for Vite code

Unreal 4.27 `VectorRegister` is four `float`s (SSE). PhysX 3.4 narrow phase and solver are SSE2/SSE4
kernels over batched `float`. Neither automatically uses the second 128 bits of a 256-bit FMA. AVX2 is
still legal on this CPU; it doubles floats per FMA **instruction**, but you still have **one FMA pipe**.
You do not get desktop Zen 2's second FMA.

Rules that follow from the pipe map:

1. **Issue-bound packed FMA is the budget that shrank.** Independent FMAs that a 3700X dual-issues now
   queue on one pipe. Two accumulators still help (latency hiding: five-cycle FMA × one pipe ≈ five in
   flight), they do not restore the missing pipe.
2. **FMA + FADD no longer hide behind extra ADD ports.** On desktop, FADD can sit on `FP2`/`FP3` while FMA
   occupies `FP0`/`FP1`. Here FMA and FADD share two math pipes. Prefer `fmadd` form (`a * b + c`) over
   separate mul and add when the math allows it — one uop, one pipe.
3. **Stores are comparatively cheap.** Streaming SoA writes can use `FP2`. Do not scalar-extract in the
   inner loop just to "simplify" stores.
4. **Do not rewrite AVX2 down to SSE because of the old 128-bit-FPU rumour.** Width is 256-bit. SSE-only
   inner loops leave half the register on the table and still hit the same two math pipes.
5. **Do not emit AVX-512.** Not present. Keep `/arch:AVX2` (or Clang `-mavx2 -mfma`) for hot translation
   units; leave `VectorRegister` SSE unless the kernel is explicitly AVX2.
6. **FP64 halves occupancy again.** Animation, physics and audio stay FP32. LWC-style doubles on this FPU
   are a last resort, not a default.
7. **Integer work is not the bottleneck you are modelling.** The 4700S exists to catch FPU throughput
   regressions, not to re-tune the task graph.

The [physics SIMD notes](Physics.md) still apply: occupancy across the whole step beats a heroic kernel
that never runs. Chaos ISPC AVX2 paths assume more FPU issue bandwidth than this core has; that is one
reason they are the wrong reference for Vite's PhysX target.

## Complete FPU-side patterns

All of the following is portable Windows code. Time it on the 4700S. The first snippet is a pipe probe;
the rest is the shape hot Vite/PhysX-adjacent math should have.

### 1. Measure FMA issue width

This is the check that distinguishes a 4700S from a 3700X. Independent `_mm256_fmadd_ps` should approach
**8 floats × 1 FMA/cycle** on the console-cut FPU and **8 floats × 2 FMA/cycle** on desktop Zen 2 (at the
same clock, ignoring frequency and thermal noise).

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

// Independent FMAs: throughput bound. Dependent FMAs: latency bound.
// On 4700S, independent should be ~2x dependent (5-cycle latency, 1 pipe).
// On desktop Zen 2, independent should be ~4x dependent (5-cycle latency, 2 pipes).
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

	const float CyclesPerFma = float(Dt) / float(Iters * 4u);
	(void)Out;
	return CyclesPerFma; // ~1.0 on 4700S, ~0.5 on desktop Zen 2 if clocks are comparable
}
```

Compile that translation unit with AVX2+FMA (`/arch:AVX2` or `-mavx2 -mfma`). If independent FMA sits at
~1 cycle/uop on the 4700S and ~0.5 on a 3700X, the pipe map is matching the silicon you think you have.

Dependent-chain variant (same `Acc` on every line) should land near **5 cycles/uop on both chips**. If a
"win" only shows up on the dependent test, you improved latency hiding, not PS5 FPU throughput.

### 2. SoA integrate — keep FMA fused, stores vectorised

Scalar `FVector` in a particle or body loop wastes issue slots on shuffles and scalar stores. Structure of
arrays lets one `VectorMultiplyAdd` produce four bodies and lets `FP2` eat the stores.

```cpp
#include "Math/UnrealMathSSE.h"

struct FBodySoA
{
	TArray<float> Px, Py, Pz;
	TArray<float> Vx, Vy, Vz;
	TArray<float> Ax, Ay, Az;

	void Reset(int32 Count)
	{
		Px.SetNumZeroed(Count); Py.SetNumZeroed(Count); Pz.SetNumZeroed(Count);
		Vx.SetNumZeroed(Count); Vy.SetNumZeroed(Count); Vz.SetNumZeroed(Count);
		Ax.SetNumZeroed(Count); Ay.SetNumZeroed(Count); Az.SetNumZeroed(Count);
	}
};

void IntegrateBodiesSoA(FBodySoA& Bodies, float Dt, int32 Count)
{
	const float Half = 0.5f;
	const VectorRegister VDt = VectorLoadFloat1(&Dt);
	const VectorRegister HalfDt = VectorMultiply(VDt, VectorLoadFloat1(&Half));
	const int32 Padded = Count & ~3;
	int32 I = 0;

	for (; I < Padded; I += 4)
	{
		VectorRegister Px = VectorLoad(Bodies.Px.GetData() + I);
		VectorRegister Py = VectorLoad(Bodies.Py.GetData() + I);
		VectorRegister Pz = VectorLoad(Bodies.Pz.GetData() + I);
		VectorRegister Vx = VectorLoad(Bodies.Vx.GetData() + I);
		VectorRegister Vy = VectorLoad(Bodies.Vy.GetData() + I);
		VectorRegister Vz = VectorLoad(Bodies.Vz.GetData() + I);
		VectorRegister Ax = VectorLoad(Bodies.Ax.GetData() + I);
		VectorRegister Ay = VectorLoad(Bodies.Ay.GetData() + I);
		VectorRegister Az = VectorLoad(Bodies.Az.GetData() + I);

		Vx = VectorMultiplyAdd(Ax, VDt, Vx);
		Vy = VectorMultiplyAdd(Ay, VDt, Vy);
		Vz = VectorMultiplyAdd(Az, VDt, Vz);

		Px = VectorMultiplyAdd(Vx, VDt, Px);
		Py = VectorMultiplyAdd(Vy, VDt, Py);
		Pz = VectorMultiplyAdd(Vz, VDt, Pz);
		Px = VectorMultiplyAdd(Ax, VectorMultiply(HalfDt, VDt), Px);
		Py = VectorMultiplyAdd(Ay, VectorMultiply(HalfDt, VDt), Py);
		Pz = VectorMultiplyAdd(Az, VectorMultiply(HalfDt, VDt), Pz);

		VectorStore(Px, Bodies.Px.GetData() + I);
		VectorStore(Py, Bodies.Py.GetData() + I);
		VectorStore(Pz, Bodies.Pz.GetData() + I);
		VectorStore(Vx, Bodies.Vx.GetData() + I);
		VectorStore(Vy, Bodies.Vy.GetData() + I);
		VectorStore(Vz, Bodies.Vz.GetData() + I);
	}

	for (; I < Count; ++I)
	{
		Bodies.Vx[I] += Bodies.Ax[I] * Dt;
		Bodies.Vy[I] += Bodies.Ay[I] * Dt;
		Bodies.Vz[I] += Bodies.Az[I] * Dt;
		Bodies.Px[I] += Bodies.Vx[I] * Dt + 0.5f * Bodies.Ax[I] * Dt * Dt;
		Bodies.Py[I] += Bodies.Vy[I] * Dt + 0.5f * Bodies.Ay[I] * Dt * Dt;
		Bodies.Pz[I] += Bodies.Vz[I] * Dt + 0.5f * Bodies.Az[I] * Dt * Dt;
	}
}
```

Do not "simplify" that inner loop to `FVector P = ...; P += V * Dt;`. Three scalar lanes become three
dependency chains and twelve scalar stores. On this FPU you cannot buy those issue slots back with clock.

AVX2 variant of the same loop (`__m256`, stride 8) is worth it once the working set is aligned and the
kernel is actually FMA-bound. It does not recover the missing second FMA pipe; it only uses the 256-bit
path that is still there.

### 3. Pose blend — FMA form, engine quaternion multiply

Pose blending is FMA-bound. Keep it as `a*(1-t) + b*t` in registers. For quaternion products, call
Unreal's existing `VectorQuaternionMultiply` rather than a hand-rolled Hamilton product; the shuffle
sequence is already SSE and does not need a 4700S-specific rewrite.

```cpp
#include "Math/UnrealMathSSE.h"

void BlendPosesLinear(
	const VectorRegister* RESTRICT A,
	const VectorRegister* RESTRICT B,
	VectorRegister* RESTRICT Out,
	const VectorRegister Alpha,
	int32 Count)
{
	const VectorRegister OneMinus = VectorSubtract(VectorOne(), Alpha);
	for (int32 I = 0; I < Count; ++I)
	{
		Out[I] = VectorMultiplyAdd(B[I], Alpha, VectorMultiply(A[I], OneMinus));
	}
}

void MulQuatArrays(
	const FQuat* RESTRICT A,
	const FQuat* RESTRICT B,
	FQuat* RESTRICT Out,
	int32 Count)
{
	for (int32 I = 0; I < Count; ++I)
	{
		VectorQuaternionMultiply(&Out[I], &A[I], &B[I]);
	}
}
```

If a profiler on the 4700S shows this blend as FMA-throughput bound at scale, switch the arrays to SoA
(`Xxxx`, `Yyyy`, `Zzzz`, `Wwww`) so each FMA covers four bones. AoS quaternion multiply stays
shuffle-heavy; that cost is permute/decode, not the missing FPU pipe. Measure both layouts on the 4700S
before touching the engine pose path.

### 4. Reciprocal / rsqrt instead of DIV/SQRT in inner loops

Divide and sqrt occupy the FPU for many cycles and block the scheduler. On a two-pipe FPU a blocked
scheduler is the failure mode Chips and Cheese measured (Y-Cruncher: FP scheduler full ~17% of cycles
versus ~6% on desktop Zen 2).

```cpp
#include "Math/UnrealMathSSE.h"

FORCEINLINE VectorRegister VectorRcpNewton(const VectorRegister V)
{
	const float NegOne = -1.0f;
	const VectorRegister Est = VectorReciprocal(V);
	return VectorMultiplyAdd(
		VectorLoadFloat1(&NegOne),
		VectorMultiply(V, VectorMultiply(Est, Est)),
		VectorAdd(Est, Est));
}

FORCEINLINE VectorRegister VectorNormalize3Fma(const VectorRegister V)
{
	const VectorRegister LenSq = VectorDot3(V, V);
	return VectorMultiply(V, VectorReciprocalSqrt(LenSq));
}
```

Use the Newton rcp only when the caller can tolerate ~11 bits then ~22 bits. Collision contact
normalisation can; debug drawing can. Do not replace IEEE div in gameplay-visible integration if the
4700S is not actually DIV-bound.

### 5. What not to ship

```cpp
// BAD: scalar extract in the hot loop — kills FP2 vector stores and the FMA pipe
for (int32 I = 0; I < Count; ++I)
{
	FVector V = Particles[I].Velocity;
	V.Z += GravityZ * Dt;
	Particles[I].Velocity = V;
}

// BAD: mul and add as separate ops when an FMA exists
VectorRegister Tmp = VectorMultiply(A, B);
R = VectorAdd(Tmp, C);

// BAD: FP64 in a per-body kernel on this FPU
double X = (double)P.X + (double)V.X * Dt;
```

Corrected inner loop for the gravity case, still SoA:

```cpp
const float GravityDt = GravityZ * Dt;
const VectorRegister GDt = VectorLoadFloat1(&GravityDt);
for (int32 I = 0; I < Padded; I += 4)
{
	VectorRegister Vz = VectorLoad(&VzSoA[I]);
	Vz = VectorAdd(Vz, GDt);
	VectorStore(Vz, &VzSoA[I]);
}
```

## How to test FPU work on the 4700S

<procedure title="Validate an FPU optimisation against the PS5 CPU" id="fpu-4700s">
    <step>
        Land the change behind a compile-time guard if it can affect codegen globally. See
        <a href="Compile-Time-Switches.md">Compile-Time Switches</a>.
    </step>
    <step>
        Build Shipping or Test, AVX2 enabled for the kernel TU, identical flags on the 4700S and on a
        desktop Zen 2 box.
    </step>
    <step>
        Run the FMA probe above. Confirm ~1 cycle/FMA independent on the 4700S before trusting the box.
    </step>
    <step>
        Time the real kernel (PhysX step, pose eval, audio) with <code>stat physics</code> /
        <code>stat anim</code> / ETW, not with a 13700K Unreal Insights capture.
    </step>
    <step>
        Compare ratios, not absolute milliseconds: <code>time_4700S / time_3700X</code> for the kernel
        should move toward 1.0 if you removed FMA traffic, and stay ~2× if you only added ILP the extra
        desktop pipes were eating.
    </step>
    <step>
        Re-run the same scene GPU-bound on the RX 6700-class card. If frame time did not move, you were
        not CPU-FPU bound on that scene — keep the code only if the 4700S physics/anim capture still
        needs it.
    </step>
</procedure>

Pin the 4700S test to a fixed clock if the kit will boost. SMT on or off must match between runs; PS5
ships SMT on. Do not compare 8C/16T 4700S numbers to a 16-core desktop and call it FPU.

## GPU testing stays on a different box

The 4700S / 4800S kits cannot answer GPU compiler questions. Their GPUs are fused off.

The RX 6700 already on the [system requirements](System-Requirements.md) list is the desktop RDNA2
stand-in: same generation, close enough throughput to catch ISA and driver compiler behaviour. It is
**not** PS5 RDNA2. Treat 6700 captures as "RDNA2-class", not as a substitute for a console GPU trace.

The BC-250 has a working GPU on the same APU family. Without Windows D3D12 it cannot run Vite's primary
RHI. Do not build a test plan that requires it for Editor or Shipping Windows packages.

## See also

- [System Requirements](System-Requirements.md)
- [Performance Targets](Performance-Targets.md)
- [Physics](Physics.md)
- [Profiling](Profiling.md)
- [Coding Guidelines](Coding-Guidelines.md)
- [Platforms](Platforms.md)
