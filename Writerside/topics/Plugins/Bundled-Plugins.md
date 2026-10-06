# Bundled Plugins

<tldr>
<p>
Everything Vite adds on top of stock UE 4.27, with versions and default enablement. Stock 4.27 plugins are
not listed &mdash; only Vite's additions and the vendor integrations. Three are on by default: RTXGI, ACL
and the custom splash screen.
</p>
</tldr>

Versions and defaults are read from the `.uplugin` files of the
[September Major](ueVite26-SeptemberMajor.md) release. Check the `.uplugin` file for the authoritative value
in your tree. **Off** means the engine does not load the plugin until a project enables it; that includes
plugins whose descriptor leaves `EnabledByDefault` unset, which Unreal treats as off for engine plugins.

<img src="VitePlugins.png" alt="Contents of Engine/Plugins/Runtime/VitePlugins in Explorer" border-effect="line"/>

*Vite's own additions live under `Engine\Plugins\Runtime\VitePlugins`. Vendor integrations from NVIDIA sit
separately under `Engine\Plugins\Runtime\Nvidia`.*

<warning>
<p>
<a href="ViteSetup.md">ViteSetup</a>'s Express path moves every plugin under
<code>Runtime\VitePlugins</code> except ACL and MotionSymphony to <code>ViteDebloat_Moved</code>. If a plugin
in that folder is missing from your tree, that is the usual reason. See the
<a href="Debloat-Guide.md">Debloat Guide</a>.
</p>
</warning>

## Upscaling and frame generation

| Plugin | Version | Default | Path |
|---|---|---|---|
| NVIDIA DLSS Super Resolution / Ray Reconstruction / DLAA | 8.7.0 (NGX 310.7.0) | Off | `Runtime\Nvidia\DLSS` |
| NVIDIA DLSS Frame Generation | 1.3.0 (Streamline SDK 2.12.0) | Off | `Runtime\Nvidia\Streamline` |
| NVIDIA NIS | 1.2.1 | Off | `Runtime\Nvidia\NIS` |
| NVIDIA RTX Dynamic Vibrance (DeepDVC) | 1.3.0 (Streamline) | Off | `Runtime\Nvidia\StreamlineDeepDVC` |
| NVIDIA Reflex | 1.6 | Off | `Runtime\Nvidia\Reflex` |
| Movie Render Queue DLSS/DLAA support | 2.3.3 | Off | `Runtime\Nvidia\DLSSMoviePipelineSupport` |
| AMD FSR 4 | 4.1.1 | Off | `Runtime\VitePlugins\FSR4-427\FSR4` |
| AMD Anti-Lag 2 | 2.0.4 | Off | `Runtime\VitePlugins\AntiLag2.0.4` |
| Intel XeSS | 3.1.0 | Off | `Runtime\VitePlugins\XeSS_UE4.27_Plugin_v3.1.0` |

FSR 4 uses the native ffx-api and is DX12-only. It was backported to 4.27 specifically for Vite. The older
FSR 2 plugin remains in `Runtime\VitePlugins\FSR2-427` with its descriptors renamed `.uplugin.disabled`, so
it never loads. Full detail in [Upscalers](Upscalers.md).

## Ray tracing and rendering

| Plugin | Version | Default | Path |
|---|---|---|---|
| NVIDIA RTX Global Illumination (RTXGI) | 1.1.50 | **On** | `Runtime\Nvidia\RTXGI` |
| NVIDIA Real-Time Denoiser (NRD/ReLAX) | 2.10.00-relax | Off | `Runtime\Nvidia\NRD` |
| NVIDIA Ansel | 4251 | Off | `Runtime\Nvidia\Ansel` |
| Graphics Card Info Utilities | 1.0 | Off | `Runtime\Nvidia\GraphicsCardInfoUtils` |

RTXGI provides the DDGI implementation that is Vite's recommended dynamic GI solution, which is why it is on
by default. NRD/ReLAX denoises ray-traced output; enable it when you use the ray-traced effects that rely on
it. See [Global Illumination](Global-Illumination.md) and [Dynamic DDGI](DDGI-Dynamic.md).

## Hair

| Plugin | Version | Default | Path |
|---|---|---|---|
| TressFX 5.0 | 5.0 | Off | `Runtime\TressFX` |
| Groom (HairStrands) | 1.0 | Off | `Runtime\HairStrands` |

Two independent hair systems with different authoring pipelines. TressFX also needs the engine built with
`VITE_TRESSFX=1`. See [Hair Rendering](Hair-Rendering.md).

## Physics and destruction

| Plugin | Version | Default | Path |
|---|---|---|---|
| Blast (runtime) | 1.0 | Off | `GameWorks\Blast` |
| Blast Plugin (authoring) | 0.1 | Off | `Experimental\BlastPlugin` |
| PhysX Instanced Subsystem | 1.11 | Off | `Runtime\VitePlugins\PhysXInstancedSubsystem` |
| Kawaii Physics | 1.18.0 | Off | `Runtime\VitePlugins\KawaiiPhysics` |

Apex Destruction, Apex Cloth and PhysX Vehicles are stock 4.27 plugins that Vite retains &mdash; they were
removed in UE5 when Chaos replaced PhysX. The Vite plugin profile applied by
`ueVite-ApplyVitePluginDefaults.bat` turns the Blast authoring plugin on; see
[Engine Default Changes](Engine-Defaults.md#disabled-plugins) and
[Destruction and Cloth](Destruction-And-Cloth.md).

Kawaii Physics is a UE5 secondary-motion bone solver backported to Vite. It gives hair, cloth and
accessories physical follow-through from a single animation node, far more cheaply than a full cloth
simulation.

The PhysX Instanced Subsystem manages large numbers of PhysX-backed instanced bodies through a world
subsystem, writing poses back into ISM/HISM instance transforms rather than spawning individual actors.
See [Instanced Physics](Instanced-Physics.md).

## Animation

| Plugin | Version | Default | Path |
|---|---|---|---|
| Animation Compression Library (ACL) | 2.1.0 | **On** | `Runtime\VitePlugins\ACLPlugin` |
| Motion Symphony | 1.09 | Off | `Runtime\VitePlugins\MotionSymphony` |

ACL replaces Unreal's built-in animation compression with a substantially better size/quality curve. On a
project with a large animation set the memory saving is significant, and it is one of the cheapest wins
available &mdash; see [Performance Targets](Performance-Targets.md).

Motion Symphony provides motion matching and pose matching, the Ubisoft-style approach to animation
synthesis. It is the closest 4.27 equivalent to UE5's Motion Matching.
[Documentation](https://www.wikiful.com/@AnimationUprising/motion-symphony/motion-matching) ·
[Sample project](https://github.com/Animation-Uprising/MotionSymphony_ExampleProject/tree/main)

## Gameplay

| Plugin | Version | Default | Path |
|---|---|---|---|
| Abilities (SplashAbilities) | 1.1 | Off | `Runtime\VitePlugins\SplashAbilities` |

Abilities is a lighter alternative to `GameplayAbilities` for projects that want an ability system without
GAS's complexity and replication model.

<note>
<p>
A Flecs ECS integration (world subsystem, Blueprint entity handles, an ISM rendering demo and optional Flecs
Explorer support) is in development on an internal branch. It is not part of any public release yet. See
<a href="Proposed-Plugins.md">Proposed Plugins</a>.
</p>
</note>

## Debug and profiling

| Plugin | Version | Default | Path |
|---|---|---|---|
| Dear ImGui | 0.1.0 | Off | `Runtime\VitePlugins\UnrealImGui` |
| ImGui Tools | 1.0 | Off | `Runtime\VitePlugins\ImGuiTools` |
| Intel GPA | 1.0 | Off | `Runtime\VitePlugins\GPAPlugin` |
| Automatron | 1.1a | Off | `Runtime\VitePlugins\Automatron` |

ImGui gives you immediate-mode debug UI that works in the viewport and in standalone builds, where Slate
debug widgets are awkward. ImGui Tools builds functional development tools on top of it.

The GPA plugin integrates Intel Graphics Performance Analyzers into the editor. Automatron improves
automated testing for C++ and Blueprints. See [Profiling](Profiling.md).

## Content and utilities

| Plugin | Version | Default | Path |
|---|---|---|---|
| Custom Splash Preload Screen | 1.0 | **On** | `Runtime\PostSplashScreen` |
| Impostor Baker | 1.0 | Off | `Experimental\ImpostorBaker` |
| Shallow Water | 1.0 | Off | `Experimental\ShallowWater` |

The splash screen plugin displays a custom screen after the system splash during engine preinit, covering
the gap before the first frame.

Impostor Baker generates impostors for use as distant mesh LODs &mdash; the standard technique for
rendering large numbers of distant trees or props cheaply, and worth reaching for before accepting a draw
call cost you cannot afford.

## Default enablement summary

Three bundled plugins are on by default:

| Plugin | Why |
|---|---|
| RTXGI | Provides DDGI, Vite's recommended dynamic GI |
| ACL | Better animation compression for every project, at no runtime cost |
| Custom Splash Preload Screen | Cosmetic, negligible cost |

Everything else is opt-in. If a feature appears not to work, check that its plugin is enabled before
debugging further &mdash; and for ray tracing features, check the
[compile-time switch availability table](Ray-Tracing.md) as well.

## See also

- [Plugins](Plugins.md)
- [Proposed Plugins](Proposed-Plugins.md)
- [Upscalers](Upscalers.md)
- [Hair Rendering](Hair-Rendering.md)
- [Instanced Physics](Instanced-Physics.md)
- [Debloat Guide](Debloat-Guide.md)
