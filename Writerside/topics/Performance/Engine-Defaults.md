# Engine Default Changes

<tldr>
<p>
Vite changes a number of stock Unreal Engine 4.27 defaults for performance. These changes affect your
project directly &mdash; some of them change runtime behaviour, not just cost. Read this page before
concluding that something is broken.
</p>
</tldr>

Stock Unreal defaults are chosen to make everything work out of the box, which means they enable features
most projects never use. Vite changes several of them to favour performance, on the principle that a
feature you want should be something you turn on rather than something you forget to turn off.

The trade is that a project moved from stock 4.27 to Vite may behave differently. This page is the list.

## Runtime behaviour changes

<warning>
These change behaviour, not just performance. If gameplay logic depends on the stock default, it will need
attention.
</warning>

### Overlap events disabled by default

Primitive components no longer generate overlap events unless explicitly enabled.

Overlap event generation costs on every component that has it, whether or not anything is bound to the
event. In a stock project the majority of primitives generate overlap events that nothing listens to.

**What this means for you:** components that need overlap events must set **Generate Overlap Events**
explicitly. Trigger volumes, pickup detection and anything driven by `OnComponentBeginOverlap` need the
flag set. This is the most likely source of "my trigger stopped working" after migrating a project.

The exception is `ACharacter`: since the [March Major](ueVite26-MarchMajor.md) its capsule component keeps
overlap events on, because most projects rely on them for characters. The line is marked in
`Character.cpp` if you want to turn it off.

<img src="OverlapEventsDisabled.png" alt="Commit diff replacing SetGenerateOverlapEvents(true) with bGenerateOverlapEvents = false in PrimitiveComponent.cpp" border-effect="line"/>

*One line in `UPrimitiveComponent`, applied to every primitive in every project.*

[Commit](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/02d7c0ad0a7542b382a70dc3e37877d6ec052d76)

### Optimised actor runtime

Actor runtime defaults are changed to reduce per-actor overhead in `AActor::InitializeDefaults`:

| Default | Stock 4.27 | Vite | Why |
|---|---|---|---|
| `SetCanBeDamaged` | `true` | `false` | Only actors that use the damage system need it |
| `bRelevantForNetworkReplays` | `true` | `false` | Keeps actors out of demo net recording unless wanted |
| `bRelevantForLevelBounds` | `true` | `false` | Avoids level-bounds iteration over actors that do not define bounds |

<img src="OptimizedActorRuntime.png" alt="Commit diff in Actor.cpp changing SetCanBeDamaged, bRelevantForNetworkReplays and bRelevantForLevelBounds defaults" border-effect="line"/>

*Large meshes, blocking volumes and foliage that must define world bounds need `bRelevantForLevelBounds`
set back to `true`.*

[Commit](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/970cbb989c3712f13be1fa370b778e769e5d864c)

### Skeletal mesh optimised configuration

Skeletal meshes are among the top CPU offenders in most projects, so `USkeletalMeshComponent` ships with
performance-oriented defaults instead of Epic's fully featured ones. In-world assets often contain many
skeletal meshes, which makes enabling optimised settings per component impractical; configuring the cheap
path as the default and opting into the expensive options where they are needed is the workable order.

| Default | Stock 4.27 | Vite |
|---|---|---|
| `VisibilityBasedAnimTickOption` | `AlwaysTickPoseAndRefreshBones` | `OnlyTickPoseWhenRendered` |
| `bEnableUpdateRateOptimizations` | `false` | `true` |
| `bHasCustomNavigableGeometry` | `Yes` | `No` |
| `bDisablePostProcessBlueprint` | `false` | `true` |
| `bUpdateOverlapsOnAnimationFinalize` | `true` | `false` |
| `bSkipKinematicUpdateWhenInterpolating` | `false` | `true` |
| `bSkipBoundsUpdateWhenInterpolating` | `false` | `true` |

<img src="SkeletalMeshesOptimizedConfig.png" alt="Commit diff in SkeletalMeshComponent.cpp showing changed defaults with Epic's original values in trailing comments" border-effect="line"/>

*Each changed line keeps Epic's original value in a trailing comment, so the stock behaviour is recoverable
without consulting upstream.*

`VisibilityBasedAnimTickOption` is the one to watch. `OnlyTickPoseWhenRendered` means an off-screen
character stops evaluating its pose entirely; gameplay that reads bone transforms or sockets on unrendered
characters &mdash; weapon muzzle positions, IK targets, attach points on a distant actor &mdash; must set
the component back to `AlwaysTickPose` or `AlwaysTickPoseAndRefreshBones`.

`bDisablePostProcessBlueprint = true` is the second: post-process anim Blueprints, commonly used for IK
and bone corrections, no longer run unless re-enabled per component.

The two `bSkip...WhenInterpolating` flags only matter with update rate optimisations, which Vite also turns
on: on frames where the animation is interpolated rather than evaluated, kinematic physics bodies and bounds
are not updated, and catch up on the next evaluated tick. Turn them off on a component whose kinematic bodies
must track the pose every frame, such as one used for hit detection at close range.

<img src="SkeletalMeshDefault.png" alt="SkeletalMeshComponent.cpp constructor block with Epic's original default values" border-effect="line"/>

*The same constructor block with Epic's original values (`bEnableUpdateRateOptimizations = false` and so
on), for context on where these defaults are set.*

[Commit](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/33fe7c638829b8120e8a02ecc639acda761df835)

### Generate Lightmap UVs disabled {id="generate-lightmap-uvs-disabled"}

Static mesh import no longer generates lightmap UVs by default.

Most Vite projects use [DDGI](DDGI-Dynamic.md) rather than baked lighting, so generating lightmap UVs for
every imported mesh is wasted import time and wasted UV channels. If your project bakes lighting, enable
the setting in the static mesh import options.

[Commit](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/acce6fbe432fe9fe5a2536f0979befd5dcd741d1)

### Animations compress with ACL by default

`BaseEngine.ini` points the default bone and curve compression settings at the
[Animation Compression Library](Bundled-Plugins.md) (`/ACLPlugin/ACLAnimBoneCompressionSettings` and
`ACLAnimCurveCompressionSettings`), so newly imported animations use ACL. This is why the ACL plugin is on by
default and why the [ViteSetup](ViteSetup.md) Express strip-down keeps it. Existing animations keep the
compression settings they were saved with.

### Frame rate capped at 120 in standalone and packaged builds

`FrameRateLimit=120.0` in `Engine/Config/BaseGameUserSettings.ini` caps standalone and packaged games at
120&nbsp;FPS, for consistent frame pacing (since the [July Major](ueVite26-JulyMajor.md)).

**What this means for you:** benchmarks that run faster than 120&nbsp;FPS, including several of the
[demo projects](ProjectsAndDemos.md), report 120 until you lift the cap. Use `t.MaxFPS 0` at runtime for an
uncapped frame rate, or set `FrameRateLimit` in your project's `DefaultGameUserSettings.ini`.

## Scalability

Vite rebalances the shadow scalability groups in `Engine/Config/BaseScalability.ini`. Stock 4.27 spreads
them from almost no shadows at Low to very expensive ones at Epic and Cinematic. Vite narrows that spread:
Low gets usable shadows, High and Epic become cheaper, and Medium is unchanged.

| Group | `r.ShadowQuality` (stock &rarr; Vite) | Other changes from stock |
|---|---|---|
| Low (`@0`) | 0 &rarr; **2** | Four cascades instead of one, 1024 maximum shadow resolution, distance field and capsule shadows on, light functions on, lights keep their full draw distance |
| Medium (`@1`) | 3 &rarr; 3 | None |
| High (`@2`) | 5 &rarr; **4** | Shadow distance scale 0.85 &rarr; 0.75, cascade transition 0.8 &rarr; 0.7 |
| Epic (`@3`) | 5 &rarr; 5 | At most 8 cascades instead of 10, radius threshold 0.01 &rarr; 0.02, distance scale 1.0 &rarr; 0.85, volumetric fog grid 16&nbsp;px &times; 64 slices instead of 8&nbsp;px &times; 128 |
| Cinematic | 5 &rarr; 5 | Maximum shadow resolution 4096 &rarr; 2048, volumetric fog grid 8&nbsp;px instead of 4&nbsp;px, 4 history-miss supersamples instead of 16 |

If a project relies on the stock Epic or Cinematic shadow budget for trailers or offline captures, override
those values in the project's `DefaultScalability.ini` rather than editing the engine file.

## Switching gameplay defaults back

The overlap and skeletal mesh defaults above are the ones most likely to break a migrated project. Since the
[August Major](ueVite26-AugustMajor.md), `ViteDefaults.bat` at the engine root switches each of them between
Vite and stock UE 4.27 without hand-editing engine source:

```
ViteDefaults.bat                                  :: interactive menu showing the current state
ViteDefaults.bat -DetectOnly                      :: report the current state only
ViteDefaults.bat -SetOverlap ue427 -SetSkm vite   :: stock overlap, Vite skeletal mesh defaults
```

It rewrites the defaults in `PrimitiveComponent.cpp` and `SkeletalMeshComponent.cpp`, so rebuild the editor
afterwards. Prefer fixing the affected components in your project where you can; switching an engine
default back puts its cost back on every primitive or skeletal mesh in every level.

## Disabled plugins {id="disabled-plugins"}

Vite's plugin profile turns off engine plugins that most Win64 projects never load, which reduces editor
startup time, module load count and packaged build size. How the profile reaches your tree depends on the
release:

| Release | How the profile is applied |
|---|---|
| [LTS](ueVite25-LTS.md) to [June Major](ueVite26-JuneMajor.md) | Built into the source tree: the plugins ship with `EnabledByDefault` set to `false` |
| [July Major](ueVite26-JulyMajor.md) onwards | The tree ships the stock 4.27 values for compatibility. Run `devops\ueVite-ApplyVitePluginDefaults.bat` to apply the profile |

The profile is the list in `devops\ViteEnginePluginDefaults.txt`. It disables 39 engine plugins and enables
one:

- **Disabled:** Paper2D; the CLion, CodeLite and KDevelop source code accessors; Plastic SCM and Subversion
  source control; Chaos Cloth, Chaos Editor, Chaos Niagara and the Chaos solver plugin; the Alembic importer;
  Facial Animation; Crypto Keys; Android, Apple and WMF media playback; OpenXR, Oculus VR and SteamVR; and
  mobile services such as Google Cloud Messaging, Google PAD, Chunk Downloader and Mobile Patching Utils.
- **Enabled:** Blast, Vite's [destruction](Destruction-And-Cloth.md) path.

```
devops\ueVite-ApplyVitePluginDefaults.bat            :: apply the Vite profile
devops\ueVite-ApplyVitePluginDefaults.bat --dryrun   :: report what would change
devops\ueVite-ApplyVitePluginDefaults.bat --stock    :: restore the stock 4.27 values
```

`--yes` skips the confirmation prompt. The script edits `.uplugin` files only, so a project that names a
plugin explicitly in its `.uproject` keeps it either way.

**VR plugins in particular must be re-enabled if you need them**, and so must WMF Media if your project
plays video through Media Framework on Windows.

[Commit 1](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e9aebc2ef9f8acb7326a7e989f288ef68969342f) &middot;
[Commit 2](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/6c5948bf12ea61f82784193ccaa5d43c4f574ae9)

## Ticking you can turn off

### Niagara

Niagara ticks whenever the plugin is enabled. Disable the Niagara plugin at project level if you do not use
it; Cascade remains available in 4.27.

## Ray-traced effects start off {id="ray-traced-effects-off"}

Stock 4.27 lets post-process volumes decide whether ray-traced reflections, translucency and ambient
occlusion run (`-1`), and turns ray-traced shadows on (`1`). Every Vite release since the
[LTS](ueVite25-LTS.md) sets all four to `0`:

| CVar | Stock 4.27 | Vite |
|---|---|---|
| `r.RayTracing.Reflections` | `-1` (post-process volume decides) | `0` |
| `r.RayTracing.Translucency` | `-1` (post-process volume decides) | `0` |
| `r.RayTracing.AmbientOcclusion` | `-1` (post-process volume decides) | `0` |
| `r.RayTracing.Shadows` | `1` | `0` |

At `0` the post-process volume settings for these effects are ignored, so a project that enabled them in
its volumes gets none of them after moving to Vite. Set the CVar to `-1` to restore the stock behaviour, or to
`1` to force the effect on:

```ini
; Config/DefaultEngine.ini
[/Script/Engine.RendererSettings]
r.RayTracing.Reflections=-1
r.RayTracing.AmbientOcclusion=-1
```

Ray-traced translucency is also compiled out by default (`VITE_RT_PSO_DEBLOAT`), so its CVar only matters in
a build with that switch off. Its help text still labels `-1` as the default; the value in the code is `0`.

## Ray tracing culling: unchanged, worth enabling {id="ray-tracing-culling"}

Vite keeps the stock 4.27 behaviour here: `r.RayTracing.Culling` defaults to `0`, so every ray-traced
primitive stays in the acceleration structure wherever it is relative to the camera. In large scenes,
turning it on is one of the cheapest ray tracing savings available:

```ini
; Config/DefaultEngine.ini
[SystemSettings]
r.RayTracing.Culling=1
r.RayTracing.Culling.Radius=10000
r.RayTracing.Culling.Angle=1
```

With culling on, objects **behind the camera** are dropped when they are further than
`r.RayTracing.Culling.Radius` (default 10000, 100&nbsp;m) or their projected angle is below
`r.RayTracing.Culling.Angle`. What is in front of the camera is never culled, so the direct view does not
change, but culled objects disappear from reflections and ray-traced shadows. Check mirrors and large shadow
casters behind the player after enabling it.

<note>
UE5's <code>r.RayTracing.Culling.UseMinDrawDistance</code> does not exist in 4.27 or in Vite.
</note>

## Editor defaults

These do not affect runtime performance but change editor behaviour. They are set in
`Engine/Config/BaseEditorSettings.ini` and `BaseEditorPerProjectUserSettings.ini`:

| Setting | Vite default | Effect |
|---|---|---|
| `bDisableAllTutorialAlerts` | `True` | No tutorial prompts in the editor |
| `bShowNewPluginsPopup` | `True` | Set to `False` to stop the "new plugins available" popup |
| `bSendUsageData`, `bSendUnattendedBugReports` | `False` | The editor does not send usage data or unattended crash reports |
| `bEnableAsyncTextureCompilation` | `True` | Textures compile in the background instead of blocking the editor |
| `bCopyStarterContentPreference` | `False` | New projects start without Starter Content |
| `bGenerateLightmapUVs` | `False` | See [Generate Lightmap UVs disabled](#generate-lightmap-uvs-disabled) |

The editor news feed is also removed, and animation assets always open in a new editor tab, a UE5
behaviour backported to Vite
([commit](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8bdae919e6eae61a27ef8d09d38027592a473d8c)).

## Optional debloat you can do yourself

These cannot be disabled in the fork release branch for compatibility reasons, but are available to
individual projects.

**Vite plugin removal.** Removing the added Vite plugins improves compile times. Measured on a Ryzen 9
9950X3D while Houdini Engine was still bundled: full repository 15 minutes, without Vite plugins 12 minutes,
with Houdini the largest single contributor. The [June Major](ueVite26-JuneMajor.md) removed Houdini, so the
gap is smaller in current releases.

See the [Debloat Guide](Debloat-Guide.md) for the tooling.

## Migrating an existing project

<procedure title="Check a migrated project against Vite defaults" id="check-defaults">
    <step>
        Test every trigger volume and overlap-driven interaction. Overlap events are the most common
        breakage.
    </step>
    <step>
        Check characters using leader/follower skeletal mesh setups for missing curve propagation.
    </step>
    <step>
        If the project bakes lighting, re-enable lightmap UV generation and confirm existing meshes still
        have valid lightmap UVs.
    </step>
    <step>Re-enable any plugins your project needs, VR and WMF Media in particular.</step>
    <step>Review scalability settings, since Low, High, Epic and Cinematic shadows now differ from stock.</step>
    <step>
        If the project relies on post-process volumes for ray-traced reflections, translucency or AO, set
        those CVars to <code>-1</code>; see <a href="#ray-traced-effects-off">Ray-traced effects start off</a>.
    </step>
</procedure>

## See also

- [Migrating from UE5](Migrating-From-UE5.md)
- [Debloat Guide](Debloat-Guide.md)
- [Profiling](Profiling.md)
- [Compile-Time Switches](Compile-Time-Switches.md)
