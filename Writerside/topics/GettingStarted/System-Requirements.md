# System Requirements

<tldr>
<p>
Windows 10 or 11 x64. A ray-tracing capable GPU is recommended but not required &mdash;
<a href="DDGI-Static.md">Static DDGI</a> and the raster paths run on hardware with no DXR support at all.
Dynamic DDGI is designed to scale down to GTX 1060 6&nbsp;GB class GPUs.
</p>
</tldr>

Vite has two distinct sets of requirements: what it takes to *run* content built on the engine, and what it
takes to *build the engine itself*. They are very different, and the second one is much heavier.

## Running Vite content

Vite is explicitly designed to scale across a wide hardware range, which is the point of choosing DDGI over
Lumen in the first place.

| | Minimum                         | Recommended |
|---|---------------------------------|---|
| OS | Windows 10 x64                  | Windows 11 x64 |
| GPU (no ray tracing) | Any DirectX 11 capable GPU      | &mdash; |
| GPU (Dynamic DDGI) | GTX 1060 6&nbsp;GB or any RDNA2 | RTX 2060 / RX 6600 or better |
| GPU (full RT suite) | RTX 2060 / RX 6600              | RTX 3070 / RX 6700 XT or better |
| VRAM | 6&nbsp;GB                       | 8&nbsp;GB or more |

Dynamic DDGI works from GTX 1060 6&nbsp;GB class GPUs upward. Below that, or on any GPU with no ray tracing
support, use [Static DDGI](DDGI-Static.md), which bakes irradiance into probe volumes and has no runtime
ray tracing cost.

### Test Hardware

These are the configurations Vite is actively benchmarked and tuned against, all owned by the fork's core
developers.



CPU FPU work and GPU compiler work are different boxes. The 4700S is further-cut Zen 2 versus Series X
(mainly the FPU) and exists to time PhysX 3.4 and other FPU kernels as they will on the PS5 CPU. The RX
6700 is a PC RDNA2 compiler proxy; PS5 RDNA2 still differs. 4700S/4800S GPUs are fused off. The BC-250
GPU works but not under Windows. Detail is in [PS5 CPU FPU](PS5-CPU-FPU.md).

| Vendor | Hardware                        | Why it matters                               |
|---|---------------------------------|----------------------------------------------|
| AMD | 4700S (Zen 2, iGPU fused off)   | PS5 CPU FPU proxy (one FMA pipe). PhysX 3.4  |
| AMD | RX 6700 (RDNA2)                 | PC RDNA2 compiler/throughput proxy for PS5   |
| AMD | Steam Deck LCD Van Gogh (RDNA2) | Handheld class                               |
| AMD | RX 9060 XT (RDNA4)              | Mid-tier GPU                                 |
| NVIDIA | RTX 2060 (Turing)               | Lower bound for hardware RT and DLSS         |
| NVIDIA | RTX 3060 (Ampere)               | Close to the most common GPU in the Steam Hardware Survey |
| NVIDIA | RTX 4080 Super (Ada Lovelace)   | Upper-bound reference for 4K native captures |

Testing is most useful on a 4K native monitor or TV (with an RX 6700 / RTX 4060 or faster), because Vite's whole argument is about holding native
resolution rather than upscaling from a lower internal one.

If you want to showcase results in your hardware (as in from the Demos), the `#showcase` channel on Discord is where testing is coordinated.

## Building the engine from source

Building is CPU-, RAM- and disk-bound. Treat these as practical guidance rather than hard cutoffs.

| | Practical minimum           | Comfortable                         |
|---|-----------------------------|-------------------------------------|
| CPU | 6 cores / 12 threads        | 16 cores / 32 threads or more       |
| RAM | 24&nbsp;GB                  | 32&nbsp;GB                          |
| Storage | SATA SSD, 50&nbsp;GB free | NVMe SSD, about 140&nbsp;GB free for a full Windows tree |
| OS | Windows 10 x64              | Windows 11 x64                      |

An Unreal Engine 4.27 source tree with dependencies, intermediates and a built editor is very large &mdash;
budget well over a hundred gigabytes, and more again if you produce an installed build alongside it, since
that writes a second copy into `LocalBuilds\Engine\Windows\`. A mechanical hard drive will work but makes
every step painful; use an SSD.

Compile time scales almost linearly with core count. A full build on a Ryzen 9 9950X3D takes roughly
15 minutes. You can reclaim a meaningful amount of both time and disk space by excluding platforms you do
not target and stripping optional content &mdash; see [Debloat Guide](Debloat-Guide.md) and the setup
presets described in [Building from Source](Build-From-Source.md).

You also need a specific compiler and SDK. This is not optional and is covered separately in
[Toolchain Requirements](Toolchain-Requirements.md).

## See also

- [Toolchain Requirements](Toolchain-Requirements.md)
- [Building from Source](Build-From-Source.md)
- [Platform Support](Platforms.md)
- [Performance Targets](Performance-Targets.md)
