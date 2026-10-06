# Compiler Explorer

<tldr>
<p>
<a href="https://gcc.godbolt.org/">Compiler Explorer</a> compiles a self-contained C++ snippet and shows
the assembly MSVC and Clang emit. Use it to check Clang 22 compliance and codegen. It does
<b>not</b> measure runtime. For timings use
<a href="https://quick-bench.com/">Quick Bench</a> (GCC or Clang on Linux). MSVC versus clang-cl still
has to be timed on your machine.
</p>
</tldr>

Vite requires code that is well-defined under both [MSVC and Clang](Coding-Guidelines.md). Compiler
Explorer is the fastest way to put the same kernel in front of both compilers without a full engine
build. It is not a profiler, and it is not a substitute for [stat unit](Profiling.md) on real content.

The public instance is [https://gcc.godbolt.org/](https://gcc.godbolt.org/) (also
[godbolt.org](https://godbolt.org/)). They are the same site.

## What it is for

| Question | Compiler Explorer |
|---|---|
| Does this snippet compile as C++ under MSVC and Clang 22? | Yes |
| What assembly do they generate at `/O2` / `-O2`? | Yes |
| Did Clang vectorise a loop that MSVC left scalar, or the reverse? | Yes |
| How many nanoseconds does it take on MSVC versus Clang? | **No** |

Extract a kernel. Unreal headers, `FORCEINLINE`, `TArray` and the rest of the engine will not resolve on
the site. Rewrite the hot function in standard C++ so the compilers are looking at the algorithm, not at
missing includes.

## Open a session

<procedure title="Compare a snippet on Compiler Explorer" id="open-compiler-explorer">
    <step>
        Open <a href="https://gcc.godbolt.org/">https://gcc.godbolt.org/</a>. Set the language dropdown
        to <b>C++</b>.
    </step>
    <step>
        Paste a self-contained function. A <code>main</code> is only needed if you later tick
        <b>Execute the code</b>.
    </step>
    <step>
        In the compiler pane, choose the newest <b>x64 msvc</b>. Set the compiler options to
        <code>/O2 /std:c++17</code>.
    </step>
    <step>
        Use <b>Add new&hellip;</b> &rarr; <b>Compiler</b> and add <b>clang-cl</b> 22 (or
        <b>x86-64 clang</b> 22). For clang-cl use the same MSVC-style flags
        (<code>/O2 /std:c++17</code>). For Linux clang use <code>-O2 -std=c++17</code>.
    </step>
    <step>
        Enable <b>Intel asm syntax</b> on the Clang pane so both sides use Intel mnemonics. MSVC already
        does. Filter <b>Unused labels</b> and <b>Directives</b> so the noise drops out.
    </step>
    <step>
        Share the session with the URL in the address bar once both panes have compiled. That link is the
        artefact to paste into a review, not a screenshot of one compiler.
    </step>
</procedure>

clang-cl is the closer match to Vite's Windows Clang. Linux `x86-64 clang` is still useful for
standard-conformance, but it is not the ABI or object format Unreal Build Tool uses on Windows.

A snippet small enough to paste:

```c++
float clampf(float x, float lo, float hi) {
    const float y = x < lo ? lo : x;
    return y > hi ? hi : y;
}
```

If the function is not used, some compilers will emit nothing. Call it from another function in the same
editor, or compile with `/O2` while keeping the symbol live (a second function that returns
`clampf(x, 0.f, 1.f)` is enough).

## Matching flags

Compare like with like. A Release MSVC pane against an unoptimised Clang pane is not a compiler
comparison.

| | MSVC / clang-cl | Linux clang / GCC |
|---|---|---|
| Optimise | `/O2` | `-O2` |
| Language | `/std:c++17` | `-std=c++17` |
| Fast math / FMA (optional) | `/fp:fast` | `-ffast-math` or `-ffp-contract=on` |

`/O2` on MSVC is the usual Release setting. `-O3` on Clang is more aggressive than that; if you use it,
say so in the shared link. For FPU-bound kernels that Vite cares about on
[PS5-class Zen 2](PS5-CPU-FPU.md), `/fp:fast` versus contracted FMA is often the difference that shows
up in the assembly, not the C++ source.

## What the assembly is telling you

Look for differences in control flow, spills and vectorisation, not line count.

- A shorter listing is not a faster function. MSVC and Clang format assembly differently.
- `cmov` / `blend` versus a branch is a real codegen difference. Whether it is faster depends on how
  predictable the branch is on the target CPU.
- Auto-vectorisation (`movaps`, `vfmadd`, `ymm`) on one compiler and a scalar loop on the other is the
  kind of result worth taking back to the engine.
- Compile time shown in the pane is how long Godbolt's machine took to compile the snippet. It is not
  engine build time and it is not runtime.

The **llvm-mca** tool (Add tool on a Clang/LLVM pane) estimates port pressure from the assembly. That is
static analysis of the listing, not a measurement of the compiled binary running. It also does not run
against MSVC's object code.

## Runtime performance: not here

<warning>
Compiler Explorer does not benchmark MSVC against Clang. <b>Execute the code</b> runs a program for its
printed output on a shared VM. A <code>chrono</code> loop in that box is not a result: no warmup, no
statistical framework, noisy neighbours, and often a different OS than Vite ships on.
</warning>

Use Compiler Explorer to decide *what* to time. Time it somewhere that actually runs the binary.

## Quick Bench

[Quick Bench](https://quick-bench.com/) is the site for that when the compilers are GCC or Clang on
Linux. It wraps [Google Benchmark](https://github.com/google/benchmark), runs the registered functions
repeatedly, and charts CPU time relative to a no-op baseline.

<procedure title="Time a kernel on Quick Bench" id="run-quick-bench">
    <step>Open <a href="https://quick-bench.com/">https://quick-bench.com/</a>.</step>
    <step>
        Put each variant in its own <code>BENCHMARK</code> function. Keep setup outside the timed loop,
        and use <code>benchmark::DoNotOptimize</code> so the compiler cannot delete the work.
    </step>
    <step>
        Set <b>compiler</b> to a current Clang or GCC, <b>std</b> to C++17, <b>optim</b> to <code>O3</code>
        (or <code>O2</code> if you are matching Vite flags).
    </step>
    <step>Run Benchmark. The chart compares the functions you registered under <b>that one compiler</b>.</step>
    <step>
        To compare GCC against Clang, change the compiler dropdown and run again. Quick Bench does not
        put two compilers on one chart.
    </step>
</procedure>

Godbolt's own UI links out to Quick Bench (the **Quick-bench** control next to CppInsights). That
handoff is for the same snippet in Google Benchmark form; it does not add MSVC.

<note>
Quick Bench has no MSVC. It runs GCC and Clang on Linux with libstdc++ or libc++. A Clang-beats-GCC
chart is not an MSVC-versus-clang-cl chart, and it is not a PS5 or Windows result. See
<a href="Performance-Targets.md">Performance Targets</a>.
</note>

## MSVC versus clang-cl on your machine

That is the comparison Vite actually ships. Neither Godbolt nor Quick Bench will produce it.

1. Isolate the kernel in a small Google Benchmark (or a dedicated test binary) that both toolchains
   can compile.
2. Build it twice: MSVC 14.50 Release, and clang-cl 22 Release, with matching `/O2` and floating-point
   flags.
3. Run both binaries on the same machine, pinned, with other work idle. For FPU-bound PhysX-style
   kernels, prefer the [4700S / PS5-class FPU](PS5-CPU-FPU.md) over a desktop Zen 2.
4. Treat engine-level questions as [profiling](Profiling.md) problems (`stat unit`, Unreal Insights),
   not as microbenchmarks of a ten-line snippet.

A codegen win on Godbolt that does not show up in a frame capture is not a win you should ship on.

## See also

- [Coding Guidelines](Coding-Guidelines.md)
- [Toolchain Requirements](Toolchain-Requirements.md)
- [Profiling](Profiling.md)
- [PS5 CPU FPU](PS5-CPU-FPU.md)
- [Performance Targets](Performance-Targets.md)
- [Contributing](Contributing.md)
