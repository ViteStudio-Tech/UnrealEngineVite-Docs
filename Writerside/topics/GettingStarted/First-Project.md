# Creating Your First Project

<tldr>
<p>
Create a project as you normally would. <a href="DDGI-Dynamic.md">Dynamic DDGI</a> is already on
(<code>r.GlobalIllumination.ExperimentalPlugin 1</code>); pair it with <code>r.SSGI.Enable 1</code>, then
enable only the ray-traced effects your performance target needs &mdash; they start disabled.
</p>
</tldr>

Project creation in Vite works exactly as it does in stock Unreal Engine 4.27. What differs is the default
rendering configuration, so this page focuses on what to do immediately after the project opens.

<note>
This manual documents what Vite changes, not Unreal Engine itself. For the parts that are unchanged
&mdash; project structure, templates, content browser, Blueprints, materials, packaging &mdash; Epic's
4.27 documentation applies directly and remains the reference:
<a href="https://dev.epicgames.com/documentation/unreal-engine/working-with-unreal-projects-and-templates?application_version=4.27">Working with Unreal Projects and Templates (4.27)</a>.
</note>

## Create the project

<procedure title="Create a new Vite project" id="create-project">
    <step>Launch the editor from your desktop shortcut or <code>Engine\Binaries\Win64\UE4Editor.exe</code>.</step>
    <step>Choose a template. The Third Person template is the one kept by the debloat presets and is the safest starting point.</step>
    <step>Pick C++ rather than Blueprint if you intend to drive rendering features from code, which most of the examples in this manual assume.</step>
    <step>Create the project and wait for the initial shader compile. On a first run this takes a while, because the engine is building its shader cache from scratch.</step>
</procedure>

If you are opening an existing project instead, right-click the `.uproject`, choose
**Switch Unreal Engine version**, and select `UE_ViteFork`.

## Understand the defaults before you build content

> New projects start with ray tracing support and Dynamic DDGI enabled. Ray-traced reflections, shadows,
> ambient occlusion and translucency are off by default and are enabled per project or per post-process
> volume, so you decide what each effect costs your frame.
>
{style="note"}

Decide early which effects your project actually needs, because the answer shapes your entire art and
performance budget. A stylised competitive title targeting 4K120 will typically run DDGI alone. A fidelity
title targeting 4K60 might add ray-traced reflections and tessellation. See
[Performance Targets](Performance-Targets.md) for the four reference configurations Vite is tuned around.

The other set of defaults worth reading before you build much content is
[Engine Default Changes](Engine-Defaults.md). Several of them change behaviour rather than just cost &mdash;
most notably, overlap events are disabled by default on primitive components, and lightmap UV generation is
off by default on import.

## Turning features on from code

The conventional place to set these up in a sample project is the character class constructor or
`BeginPlay`. This is what the Vite sample projects do.

```c++
// Global illumination
IConsoleManager::Get().FindConsoleVariable(TEXT("r.GlobalIllumination.ExperimentalPlugin"))->Set(1);
IConsoleManager::Get().FindConsoleVariable(TEXT("r.SSGI.Enable"))->Set(1);

// Ray tracing effects available in a default build (they start disabled)
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.AmbientOcclusion"))->Set(1);
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.Reflections"))->Set(1);
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.Shadows"))->Set(1);

// Compiled out unless the engine is rebuilt with VITE_RT_PSO_DEBLOAT=0
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.Translucency"))->Set(1);
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.SampledDirectLighting"))->Set(1);
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.MeshCaustics.Enable"))->Set(1);
```

`r.GlobalIllumination.ExperimentalPlugin 1` enables DDGI; it is already set in `BaseEngine.ini`, so the
line is only needed if a project turned it off. Running SSGI alongside it is recommended rather than
optional: DDGI resolves world-scale bounce, SSGI fills in high-frequency contact detail that probe
volumes are too coarse to capture. See [DDGI and SSGI Together](SSGI.md).

For production, prefer setting these in configuration files rather than code, so they participate in
scalability and can be overridden per platform:

```ini
; Config/DefaultEngine.ini
[/Script/Engine.RendererSettings]
r.GlobalIllumination.ExperimentalPlugin=1
r.SSGI.Enable=1
r.RayTracing.Reflections=1
```

`r.RayTracing.ForceAllRayTracingEffects 1` turns everything on at once. It is useful for a quick look at
what the engine can do, and a poor idea in a shipping configuration.

## Verify it is working

Open the console with the tilde key and check a few things:

- `stat unit` &mdash; frame, game, draw and GPU times. If GPU time dominates after enabling RT effects, that
  is expected; start turning effects off from there.
- `stat gpu` &mdash; per-pass GPU cost, which is how you find out whether reflections or GI is the expensive
  one.
- `r.RayTracing.Reflections 0` &mdash; toggle an effect at runtime and watch the delta.

Vite also bundles ImGui-based benchmarking tools for in-editor and in-game profiling. See
[Profiling and Benchmarking](Profiling.md).

## Sample projects worth opening

Rather than building a test scene from scratch, start from one that already demonstrates the features:

- [Tech Demo Project](Tech-Demo-Project.md) &mdash; DDGI Cornell Box, Apex Destruction test bed, Apex Cloth
  sample and a high-end DDGI plus SSGI cave scene.
- [Abandoned Apartment](Abandone-Apartment.md) and [Attic Scene](Attic-Scene.md) &mdash; NVIDIA's original
  RTGI showcase scenes.
- [Physics Cube Bench](Physics-Cube-Bench.md) and [400 Characters CMC Bench](400-Characters-CMC-Bench.md)
  &mdash; the benchmark scenes behind the numbers quoted in this manual.

The full list is in [Projects and Demos](ProjectsAndDemos.md).

## See also

- [Global Illumination](Global-Illumination.md)
- [Ray Tracing](Ray-Tracing.md)
- [Engine Default Changes](Engine-Defaults.md)
- [Console Variable Reference](Console-Variables.md)
- [Migrating from Unreal Engine 5](Migrating-From-UE5.md)
