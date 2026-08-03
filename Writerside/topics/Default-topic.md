# Unreal Engine Vite Manual

<tldr>
<p>
Unreal Engine Vite is a performance-first fork of Unreal Engine 4.27 built on the NvRTX Caustics branch.
It keeps PhysX, adds DDGI, RTXDI, tessellation, SMAA and HBAO+, and targets native-resolution,
high-frame-rate rendering on console-class hardware.
</p>
<p>
New here? Start with <a href="Introduction-to-Vite.md">Introduction to Vite</a>, then
<a href="Build-From-Source.md">Build the Engine from Source</a>.
</p>
</tldr>

Welcome to the Unreal Engine Vite manual. This site documents the engine fork itself: how to build it,
what it changes relative to stock Unreal Engine 4.27, which rendering and physics systems it adds, and
how to get a project shipping on it.

Vite is aimed at teams in active production. It is not a research branch or a demo. Every feature
documented here is expected to survive cooking, packaging and shipping on real hardware, and the
manual is written with that assumption throughout.

## Where to start

Pick the entry point that matches what you are doing right now.

| I want to&nbsp;&hellip; | Start here |
|---|---|
| Understand what Vite is and whether it fits my project | [Introduction to Vite](Introduction-to-Vite.md) |
| Get the engine running on my machine | [Getting Started](Getting-Started.md) |
| Compile the engine from source | [Building from Source](Build-From-Source.md) |
| Fix a compile or setup error | [Build Troubleshooting](Build-Troubleshooting.md) |
| Move an existing UE5 project onto Vite | [Migrating from Unreal Engine 5](Migrating-From-UE5.md) |
| Light a scene without Lumen | [Global Illumination](Global-Illumination.md) |
| Replace Chaos with PhysX in my gameplay code | [PhysX](PhysX.md) |
| Find a console variable | [Console Variables](Console-Variables.md) |
| Contribute a change to the fork | [Contributing](Contributing.md) |

## Manual sections

### [Getting Started](Getting-Started.md)

Installation, toolchain setup, building from source, creating your first project, and migrating an
existing project from Unreal Engine 5.

### [Engine Overview](Engine-Overview.md)

Why the fork is based on NvRTX 4.27, what performance targets it is designed around, and where the
measurable cost differences between UE4 and UE5 come from.

### [Rendering](Rendering.md)

Global illumination, ray tracing, shading models, anti-aliasing, upscaling, tessellation, ambient
occlusion and colour management. This is the largest section of the manual and where most of Vite's
divergence from stock 4.27 lives.

### [Physics](Physics.md)

PhysX 3.4 as the shipping physics backend: the fast path, fixed timestep, Apex Destruction, Apex
Cloth, Blast, and large-scale instanced rigid bodies.

### [Performance and Optimization](Performance.md)

Profiling tools, the engine defaults Vite changes out of the box, shader compilation and PSO
behaviour, scalability, and how to strip the engine down for faster iteration.

### [Platforms](Platforms.md)

What each target platform supports, which renderer paths are available, and the hardware Vite is
tuned against.

### [Plugins](Plugins.md)

Plugins bundled with the engine, and the vetting process for proposing new ones.

### [Tools and Automation](Tools.md)

The `ViteSetup.bat` assistant, installed engine builds, packaging and distribution scripts, and cache
management.

### [Contributing](Contributing.md)

Coding guidelines, commit and pull request conventions, and the backporting workflow used to bring
UE5 changes into the fork.

### [Projects and Demos](ProjectsAndDemos.md)

Downloadable sample projects and benchmark scenes, with the hardware numbers they were captured on.

### [Reference](Reference.md)

Console variable reference, compile-time switches, glossary and FAQ.

## Community and project links

| Resource | Link |
|---|---|
| Engine repository | [ViteStudio-Tech](https://github.com/ViteStudio-Tech) |
| Community Discord | [discord.gg/n9zQrYFhMb](https://discord.gg/n9zQrYFhMb) |
| Work plan (Trello) | [UE Vite PhysX Studio Fork](https://trello.com/b/JKyBFS5X/ue-vite-physx-vite-studio-fork) |
| Public asset drive | [Google Drive](https://drive.google.com/drive/folders/16FOkb5u6GSqHiWeAm50NaxZ19QFBwZeI?usp=sharing) |
| Support development | [ko-fi.com/vitestudio](https://ko-fi.com/vitestudio) |
| Media updates | [@theredpix](https://x.com/theredpix) |

> Vite is developed in the open by a small team of engine programmers. If you want to contribute,
> read [Contributing](Contributing.md) and request the Forker role on Discord.
>
{style="note"}
