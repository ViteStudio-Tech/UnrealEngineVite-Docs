# ueVite25 LTS

<tldr>
<p>
The long-term-support foundation of today's Vite. The LTS rebases the engine onto <b>NVIDIA's NvRTX
Caustics 4.27</b> and Epic's <b>4.27-plus</b>, merges DLSS 3 / Streamline and TressFX, and then reshapes the
defaults for performance: lighter Actors, opt-in overlap events, a debloated plugin set, faster shader and
cook pipelines, and modern Visual Studio 2026 support.
</p>
<p>
Branch <code>ueVite25-LTS</code> &middot; every later major release builds on it.
</p>
</tldr>

| Status | Development window | Base | Commits |
|---|---|---|---:|
| **LTS** | 15 November &ndash; 15 December 2025, maintained to 12 February 2026 | NvRTX Caustics 4.27 + Epic 4.27-plus | 174 |

## Why the LTS exists

Vite was originally built on NvRTX 5.0. Matched tests showed the 4.27-based NvRTX branch running ray-traced
GI faster, and PhysX integrating far more cleanly, so the active line moved to 4.27 in November 2025. The
reasoning is in [Why NvRTX 4.27](Why-NvRTX-427.md) and the
[base transition record](https://docs.google.com/document/d/1gA0MGkzeWWzKkgwBDOP5xRPouSKaOIW6xlPZ2q6BXO0/edit).
The earlier line is archived as [Original Vite](Original-Vite.md).

## Highlights

<deflist>
<def title="A new base">
NvRTX Caustics 4.27 and Epic's 4.27-plus merged into one line together with the DLSS 3 / Streamline plugin
and TressFX, giving Vite ray-traced GI, caustics, RTXDI and modern upscaling on a UE4 core.
</def>
<def title="Lighter runtime by default">
Actors no longer default to being damageable, replay-relevant or level-bounds-relevant; primitive components
no longer generate overlap events unless asked; new Blueprints are created without placeholder event nodes,
and empty Blueprint ticks are skipped. See <a href="Engine-Defaults.md">Engine Default Changes</a>.
</def>
<def title="Faster pipelines">
On-demand shader-map processing drops from ~27.5 ms to ~6.1 ms, cooking uses about 25% less memory, PSO
caches are picked up correctly, and shader-compile batching is tuned for many-core machines.
</def>
<def title="Rendering additions">
Callisto BRDF (experimental), ACES 1.3.1 gamut compression, per-light maximum shadow draw distance, RTXDI
light-material functions, and AMD ray-tracing patches.
</def>
</deflist>

## What's new

### Base and integration

- Merged NvRTX `NvRTX_Caustics-4.27`, Epic `4.27-plus` and the NVIDIA DLSS 3 / Streamline 4.27 plugin.
- TressFX integration update; working FSR 2.

### Rendering

- **Callisto BRDF** shading model (experimental). See [Shading Models](Shading-Models.md).
- **ACES 1.3.1** gamut compression. See [Color Management](Color-Management.md).
- **Max Shadow Draw Distance** and fade range on lights.
- Shadow quality presets revised: *Low* now keeps cascaded shadows instead of disabling shadows, and *Mid*
  uses quality level 4.
- Histogram exposure reduction moved to compute; fullscreen passes draw a single triangle; slow render
  target clears removed; AO shader memory access improved.
- FX-system distance-field checks skipped for views that do not use distance fields; a command forces the
  lowest LOD for shadow depth maps; parallel rendering skipped for incompatible non-whole-scene shadows.
- Mobile uses basic eye adaptation by default (about 0.7 ms saved on a Galaxy S10).

### Ray tracing

- **RTXDI:** light material functions supported in sampled lighting; ReGIR samples per cell default to 64.
- **AMD patches:** configurable face-cull direction for ray-traced shadows.
- Lower overhead gathering ray tracing instances; reduced memory pressure on the translucent-lighting
  volume.
- Several ray-traced effects, including RT shadows, are disabled by default.

### Runtime and gameplay

- Optimised Actor defaults: `CanBeDamaged`, `bRelevantForNetworkReplays` and `bRelevantForLevelBounds`
  off by default.
- Overlap events disabled by default on primitive components.
- Optimised skeletal mesh configuration as the default.
- Faster ISM handling for AI navigation; navmesh fixes for hierarchical instanced static meshes and
  landscape meshes (Epic PRs 9027 and 9028); faster geometry-collection navmesh generation.

### Core and pipeline performance

- On-demand shader compilation map processing from ~27.5 ms to ~6.1 ms on average.
- About 25% less total cook memory by releasing the read buffer cache; 1 MB saved by deferring the pak
  reader's streaming buffer.
- Sparse-array, hashing and Map/Set/Tuple compile-time optimisations; unity builds split by available
  processors; faster editor loading; parallel asset data gathering.
- PSO cache fix; larger shader job batches; UE 5.6 virtual-core count check backported.
- Slate text kerning no longer hashes strings on the critical path.

### Plugins

- **Added:** ACL animation compression (enabled by default), Motion Symphony motion matching, Houdini 20,
  Intel Graphics Performance Analyzers, Kawaii Physics.
- **Disabled or removed by default:** SteamVR, other VR plugins, Magic Leap (Lumin) and a broad set of
  rarely used plugins.

### Editor quality of life

- Launch tips, new-plugin pop-ups and tutorial alerts can be turned off; usage-data and unattended bug
  reports off by default; the Marketplace and tutorial buttons are removed and the editor no longer forces
  the Epic Games Launcher open.
- UE5 viewport grid colour scheme, log category colourisation and "always open animation assets in a new
  tab" backported; frame rate and memory shown by default.

### Platforms and toolchain

- Visual Studio 2026 support added; Visual Studio 2015 and 2017 removed; MSVC 14.50 compiler version bump.
- Clang 13.0.1 upgrade work and MSVC compile fixes; GitDependencies and MemoryProfiler moved from .NET 4.5
  to 4.8.
- Android packaging fixes, Meta Quest device profiles, Vulkan enabled through the Android device selector,
  and Android fixes for TressFX and the C++ standard alias.
- Magic Leap removed from the engine and UnrealBuildTool.

## Maintenance after release

| Date | Change |
|---|---|
| 12 February 2026 | Windows Movie Player re-enabled; forward-shading colour-write clear limited to separate translucency; feature packs enumerated with `IterateDirectory` |

## Upgrade notes

These defaults change behaviour for projects coming from stock 4.27 or UE5:

- **Overlap events** are off for primitive components. Enable *Generate Overlap Events* on anything that
  relies on overlaps. (The character capsule was re-enabled in March.)
- **Actors** are not damageable, replay-relevant or level-bounds-relevant by default. Re-enable these on
  Actors that need them, such as damage targets, kill-cam subjects or Actors that define world bounds.
- **Blueprints** are created without *Event Tick*, *Begin Play* and overlap nodes, and empty ticks are
  skipped.
- **Ray tracing:** RT shadows and several other RT effects start disabled.
- **Toolchain:** Visual Studio 2015 and 2017 are no longer supported.

<!-- BEGIN GENERATED COMMIT RECORD -->

## Full commit history {id="commit-history"}

Branch: [`ueVite25-LTS`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/tree/ueVite25-LTS)

### Commits by area

| Area | Commits |
|---|---:|
| Toolchain and platforms | 48 |
| Editor and workflow | 36 |
| Rendering | 27 |
| Core and performance | 15 |
| Plugins and media | 11 |
| Ray tracing and GI | 10 |
| Other | 10 |
| Animation | 6 |
| Gameplay framework | 5 |
| Hair | 3 |
| Physics | 2 |
| Upscaling and anti-aliasing | 1 |

### Public release branch — 174 commits {collapsible="true" default-state="collapsed"}

174 commits (45 merge commits omitted from the table).

| Date | Commit | Author | Change |
|---|---|---|---|
| 2026-02-12 | [`d0c5d8dbb8`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d0c5d8dbb88b2bba6c6dd395fa3b9fa99ced8232) | RedPixel | Re-enabled WindowsMoviePlayer Plugin for Movies to work without needing activate the plugin in projects |
| 2026-02-12 | [`9e078e144a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/9e078e144ab5f9c770cb088b91e5f7d6c2e456a9) | RedPixel | \[Rendering\]\[Forward\]\[translucency\] Patch over NvRTX, Color write Clear now only runs with SeparateTranslucency on Forward |
| 2026-02-12 | [`d9ee07ecdc`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d9ee07ecdc912682b8088e13a0dcaebc3488e192) | RedPixel | Feature Pack IterateDirectory instead of FindFilesRecursively |
| 2025-12-15 | [`68a4da0ba4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/68a4da0ba446485034017a7f9c7f8f71aba5ba4e) | RedPixel | \[Settings\] Disabled RT Shadows by default |
| 2025-12-14 | [`21fc208c43`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/21fc208c43cebab1d1ba7a161acbd5380e528493) | RedPixel | \[Settings\] Disabled several RT effects by default |
| 2025-12-13 | [`a6e3efaf89`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a6e3efaf89f6c923e6b35cfda4521ecdeec1b289) | Carlo V. | Update README Material Comparison.md |
| 2025-12-12 | [`723fb76f92`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/723fb76f92c03a54ebaf26bc0cbad767c052a459) | RedPixel | Updated GitIgnore for GPA |
| 2025-12-12 | [`1f2422df15`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1f2422df15a8acac7b67c4382355168457547b33) | RedPixel | GPA Update |
| 2025-12-11 | [`a648e9858e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a648e9858ec6a4392001c1a1c301b01dfbe9e3f5) | RedPixel | \[Plugin Add\] Intel Graphics Performance Analyzer |
| 2025-12-11 | [`68594bec0a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/68594bec0aa0e9415677e8d15cda004dbaf3df9b) | Carlo V. | Important README Update.md |
| 2025-12-11 | [`3b5794ff67`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3b5794ff67183f91fca14a5a44b8483546777b61) | RedPixel | \[Optimization\] Added command to Force Lowest LOD shadow Depth Maps |
| 2025-12-11 | [`a25cd5be4f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a25cd5be4fcd7abf014d8a087d131aae762baebb) | RedPixel | \[Optimization\] Engine now skips all FX system distance-field checks for views that do not use distance-field data, reducing unnecessary overhead. |
| 2025-12-11 | [`853fbf68fd`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/853fbf68fd8e00344302b5eb492071f5b4c1ad4c) | RedPixel | \[Plugin Add\] Houdini 20 |
| 2025-12-11 | [`ba9832b727`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ba9832b7271b266c2a2001214ab851bfaed64eb3) | RedPixel | Motion Symphony \[Ubisoft-Inspired Motion Matching\] |
| 2025-12-10 | [`e43d59000d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e43d59000d190a621235097002bf2f0630668b3a) | RedPixel | \[Rendering Feature\] Callisto BRDF -Experimental- |
| 2025-12-10 | [`ca6f576e06`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ca6f576e0645e4d6b44b8aef958c67e1125389e6) | Dmitrii Komarevtsev | Remove Magic Leap(aka Lumin) from engine and UBT |
| 2025-12-09 | [`78aac00bae`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/78aac00bae7d9ad4a315fd0d7e57eb400b22bf02) | RedPixel | Max Shadow Draw Distance for Lights |
| 2025-12-09 | [`f8efeebb41`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f8efeebb417fd4b19695ac31e58b31d4b560906c) | Dmitrii Komarevtsev | androiddeviceslector enabled by default to get rid problem with vulkan deactivated on android |
| 2025-12-09 | [`5d465a52ca`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/5d465a52cadd0bdaabff2d208009929b4b4a13ff) | RedPixel | Reapply "Merge pull request #89 from Solessfir/shadow-draw-distance" |
| 2025-12-08 | [`b32cf998bc`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b32cf998bc0fa6dfc2e8ed310f38debb59643670) | Dmitrii Komarevtsev | device profiles fixes for oculus quest |
| 2025-12-07 | [`a4d6c877b1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a4d6c877b161ff7a0b0b98e8249fe45c784cf126) | Dmitrii Komarevtsev | Added Oculus quests device profiles; |
| 2025-12-07 | [`5ad98c2887`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/5ad98c28876cdb2d6a5506c50679fc3d6aea3b86) | Dmitrii Komarevtsev | Some changes to make package for android works |
| 2025-12-06 | [`60ad73e535`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/60ad73e535c24995091e169450e54b200380aca2) | RedPixel | Default to DX11 to avoid long shader comp on Lower End Hardware |
| 2025-12-07 | [`be1abac13d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/be1abac13d9f68493d54664f5994d44d9cfd8559) | Dmitrii Komarevtsev | Fix TressFX compilation on Android (SceneRendering include + shader type) |
| 2025-12-07 | [`ba2d5b2d78`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ba2d5b2d78e664a54cfa04cfafcbe8df2d8b0a3c) | Dmitrii Komarevtsev | Fix CppStandard alias crash in AndroidToolChain.GetCppStandardCompileArgument |
| 2025-12-05 | [`1718cd66e0`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1718cd66e08a2b47222f895162e3be2b2c98ee6a) | RedPixel | Shadow Quality 4 is now in use for Mid Shadoe Setting |
| 2025-12-05 | [`f906162bb8`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f906162bb8d72bb746da129ed6bbe9a5060671b3) | RedPixel | Shadow Quality Low Updated to have cascaded shadows and Shadow Quality 2 as default isntead of 0 |
| 2025-12-05 | [`8cee40a55b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8cee40a55bf4eebef2d9a696dc1b3c7a92b53d63) | RedPixel | Updated Default Quality Settings, Low Shadows now sets to Quality 1, instead of no shadows at all |
| 2025-12-04 | [`0fe5afa18b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0fe5afa18b6ede0ec0b5ad58e52d804c2e6cfeec) | Dmitrii Komarevtsev | Fix landscape error to make it work with c++ 17 /2 |
| 2025-12-04 | [`395f68cbb4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/395f68cbb4b7f916f3b2b68b58eb83f46423b993) | Dmitrii Komarevtsev | Fix landscape error to make it work with c++ 17' |
| 2025-12-04 | [`515fc59e6d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/515fc59e6d3000fcaeac4cc9cf57256a31501c78) | TungNguyen | fix build for old CPU |
| 2025-12-04 | [`3349560ff4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3349560ff43d096347f8e53bb09ffae173ef7e7b) | Carlo V. | Update README.md |
| 2025-12-04 | [`ff13cfe023`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ff13cfe02350068181862edf9ac587fd570357da) | Carlo V. | Update README.md |
| 2025-12-04 | [`f5ab6ef36e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f5ab6ef36e3f6da4dbf860212c6ecb925ff321e8) | Carlo V. | README UPDATE: Link to sheets class size doc, updated list of DDGI titles |
| 2025-12-04 | [`bd150a64a0`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bd150a64a059879f9413908cc06d9d1524dcd27f) | Carlo V. | Updated Vite Readme |
| 2025-12-01 | [`666c19a820`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/666c19a820f0fd901292fd5818817a8d21230acd) | RedPixel | Revert "#92 from Solessfir/cpp-20 -TO STRESS TEST!" |
| 2025-12-01 | [`a6335e192c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a6335e192c2e8d42ce4c453549995b52db6f7238) | Solessfir | C++ 20 |
| 2025-11-29 | [`505f72efda`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/505f72efda3cbc3aa4500376d00be9d4c451b01e) | RedPixel | ACES 1.3.1 Gamut compression |
| 2025-11-28 | [`2cebe1b545`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2cebe1b545b3e1db00d41545e3c5509f0051f746) | Benjamin Goundry | Update TressFX shader buffer and add padding to help |
| 2025-11-27 | [`1be7dfa3cc`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1be7dfa3cce12da1b9231bdab6ec7e124dd48be0) | RedPixel | Revert "Error fix" |
| 2025-11-27 | [`bfa501fcda`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bfa501fcdac8156ec19c3bdf2dc695c12b345d42) | RedPixel | Revert "RaiseScriptError cook fix" |
| 2025-11-27 | [`718fcccfb9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/718fcccfb9178387b42a6a5b7db765723a2830e7) | RedPixel | Revert |
| 2025-11-27 | [`de1d519c6e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/de1d519c6e209993e64640fe4d2a2344b76f9139) | RedPixel | Revert "Merge pull request #89 from Solessfir/shadow-draw-distance" |
| 2025-11-26 | [`0bfafb8637`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0bfafb863768411a0200308986bde8a3307c143d) | Solessfir | Fixes |
| 2025-11-26 | [`0c3bed6c1e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0c3bed6c1e164f3f520e8c394e6b5eb7534259e1) | Solessfir | Add Max Shadow Draw Distance &amp; Max Shadow Draw Distance Fade Range |
| 2025-11-24 | [`ae6f94472c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ae6f94472c84c3bb7a7fdc91599a94bce59547a2) | RedPixel | prev Clean Motion Symphony |
| 2025-11-24 | [`df3a37f113`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/df3a37f113adb43f7b6bad2e19e19b50fae6c6ba) | RedPixel | Fix Attempt of Viewport Visual Bug from: "Fixed: Better Defaults" |
| 2025-11-24 | [`20fb8c8fce`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/20fb8c8fcee8463ca5fb00e6fbe012edaadf7c7a) | RedPixel | RDNA 3 Alt Fix |
| 2025-11-23 | [`810f27d0e2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/810f27d0e2871aa263f11032b4a2ffd49f777102) | RedPixel | MSVC 14.50: Bump MSVC Compiler version to avoid message warning |
| 2025-11-23 | [`e252fd7d92`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e252fd7d92d1dd68abe5f47f71fcf9b456c8ad45) | Carlo V. | GameGetsMousrControl to false |
| 2025-11-23 | [`132bdae755`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/132bdae755876299c157d0797fabcd98c10833a9) | Carlo V. | bGenerateMeshDistanceFields back to disable |
| 2025-11-23 | [`d326c296cb`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d326c296cb9b5291f007a857623e1098d6f70093) | Carlo V. | Update BlueprintEditorSettings.cpp |
| 2025-11-23 | [`f3c0a9c107`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f3c0a9c107b897d4e016b54c76242fcace3c7f61) | RedPixel | AMD Patch: RTXDI: Enable light material function support in sampled lighting |
| 2025-11-23 | [`66cd05ab1f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/66cd05ab1f975028d958353718f669bacc8cd91a) | RedPixel | Const Update |
| 2025-11-23 | [`e8828c8644`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e8828c86446639f982f2f2c963fbb1c78340d948) | RedPixel | IniChange: Improve Speed for ShaderCompiler |
| 2025-11-23 | [`d47ebd742e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d47ebd742eb6ea0fc1fbb33994508ef075f9f57a) | RedPixel | AMD Patch: For RT Integrate support for changing face cull direction in ray traced shadows |
| 2025-11-23 | [`24d2e50926`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/24d2e50926bf49bb48fcb4f5ce55ce84788a0b69) | Solessfir | Fixed: Better defaults |
| 2025-11-23 | [`42b3cf882f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/42b3cf882fb444ba1d722d6f6db14249c31d5ef3) | Solessfir | RaiseScriptError cook fix |
| 2025-11-23 | [`53bb4063e3`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/53bb4063e35b2f73c38b6f15e1640c3964bd20d4) | Solessfir | RaiseScriptError cook fix |
| 2025-11-23 | [`20875ace28`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/20875ace288747fb4dfbc62ad884d5218cbcd3e3) | RedPixel | Revert "Backport RaiseScriptError to KismetSystemLibrary" |
| 2025-11-23 | [`fc01f1f272`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fc01f1f2727a775bee705798e9ace87ab62a78a0) | RedPixel | Revert "Error fix" |
| 2025-11-23 | [`33fe7c6388`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/33fe7c638829b8120e8a02ecc639acda761df835) | RedPixel | Skeletal Meshes Optimized Config as Default |
| 2025-11-22 | [`970cbb989c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/970cbb989c3712f13be1fa370b778e769e5d864c) | RedPixel | Optimized Actor runtime, \*Important READ |
| 2025-11-22 | [`c2b4fa9c48`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/c2b4fa9c483119ecb2f6964c26e912638b471498) | RedPixel | RT: Integrate support for changing face cull direction in ray traced shadows |
| 2025-11-22 | [`e54fda5de2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e54fda5de2681e93e6f1c1ffd90e36dfada6c61e) | RedPixel | RTXDI: Enable light material function support in sampled lighting |
| 2025-11-22 | [`4597fbbe95`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/4597fbbe95cd86f1192bc52eac2cf1ba0ac69003) | RedPixel | RTXDI Optimization: Change default samples per cell for ReGIR to 64 |
| 2025-11-22 | [`8aae4b3231`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8aae4b3231de14f64b578b89d467a4065d6993e1) | RedPixel | Revert "Optimize/Fix frame rate limit in unreal" |
| 2025-11-22 | [`bfcbb7bdd1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bfcbb7bdd144c82601150315585ef527fb8b6d00) | RedPixel | Default RT Back to true, it was causing a compile issue |
| 2025-11-22 | [`9b1788f4ba`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/9b1788f4ba8f00c07cb712783e3b403479787e9b) | RedPixel | Raytracing disabled by default to avoid longer shader compile on test projects |
| 2025-11-22 | [`14cdadb203`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/14cdadb2031ab7dc61f0b20ae3dd77664505c37e) | RedPixel | Kawaii Physics Chan |
| 2025-11-22 | [`55d453c9e2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/55d453c9e2c2ab60ce4dbf83f6a86a8ba3312601) | RedPixel | Revert: Rework shader compilation thread allocation on higher core machines |
| 2025-11-22 | [`36719327b2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/36719327b20cdbd00682640c47fb3d8d98c5d542) | RedPixel | ShaderCompilerRemoved extra checks, back to 4.27 behavior |
| 2025-11-22 | [`30916743fc`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/30916743fc1256df581362fe344541ca9bcbe217) | RedPixel | Revert "Shader Compiler: Minor Optimization for path hashing" |
| 2025-11-22 | [`952f00ccfc`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/952f00ccfccd8d9519a60a3adfe46ba938db113e) | RedPixel | 5.6 Backport of NumOfVirtualCores Check |
| 2025-11-22 | [`f90fc02e36`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f90fc02e367536bffe61bf4180b31eddd9143d2e) | RedPixel | Revert "Reduce ShaderCompilingThread activity while waiting for compile results." |
| 2025-11-21 | [`41c14cd766`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/41c14cd7665c14e689f2ddfc65e83971cf9640e4) | RedPixel | Revert "Merge pull request #82 from Solessfir/better-defaults" |
| 2025-11-21 | [`25c8097ca5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/25c8097ca5bb17a20189cfe05612312c7b69856a) | RedPixel | Use Compute for Histogram-based reduction during Lens Exposure |
| 2025-11-21 | [`2f17a2233c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2f17a2233ce6d3ef13b5f6aecfd2a2cda82b84c4) | RedPixel | Reduce memory pressure on the RT volume during Translucent Lighting |
| 2025-11-21 | [`1ed2a77b75`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1ed2a77b75f76c39d436b9a24693e46e1c7ad3f3) | RedPixel | Eliminate unnecessary and slow RT clears |
| 2025-11-21 | [`101206b7b8`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/101206b7b8aa79f1a2672246078a2d0370003dea) | RedPixel | Improve-AO-Shader-memory-access-pattern: Batch 1 |
| 2025-11-21 | [`cc0a6cc577`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/cc0a6cc5774f3956fcb0a79707301cdb48657ef1) | RedPixel | Use one triangle for fullscreen draws |
| 2025-11-21 | [`ebafa67a2a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ebafa67a2ad0ea732eb7af70c18b6598473de0db) | Solessfir | Error fix |
| 2025-11-21 | [`122d2b8a84`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/122d2b8a846f3032133f09119199f2a266c68669) | Solessfir | Backport RaiseScriptError to KismetSystemLibrary |
| 2025-11-21 | [`f74c18edd2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f74c18edd25e17fe6352b4dea08332083103920d) | Solessfir | Added GridCenterThickness and backorted UE5 grid color scheme |
| 2025-11-21 | [`decd13d16e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/decd13d16eb1df9109a778188fef8950ef9be421) | Solessfir | LinesToAdd fixes |
| 2025-11-21 | [`c9b6e94c75`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/c9b6e94c7541fd1af1fe3f03d8e892fb46a67d73) | RedPixel | Xcode plugin back on |
| 2025-11-21 | [`894ed62afb`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/894ed62afb202c6f6a6c31a116e1cdecac9c7d11) | Solessfir | Error fix |
| 2025-11-21 | [`f46ff2414e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f46ff2414e2869de54ca6a91edcede16b226a9db) | Solessfir | Add Cpp20 to CppCompileEnvironment.cs -&gt; CppStandardVersion |
| 2025-11-21 | [`7e40af4aa9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7e40af4aa91eba1aebc2e02af6b10c7ca570c3bf) | Solessfir | Backport: LogCategoryColorizationMode |
| 2025-11-21 | [`8bdae919e6`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8bdae919e6eae61a27ef8d09d38027592a473d8c) | Solessfir | Backport: AlwaysOpenAnimationAssetsInNewTab |
| 2025-11-21 | [`acce6fbe43`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/acce6fbe432fe9fe5a2536f0979befd5dcd741d1) | Solessfir | Better defaults |
| 2025-11-21 | [`fe7a6f4d7c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fe7a6f4d7c54d8725d6308820d5b4fd546b9ff49) | Solessfir | Safe Backports |
| 2025-11-21 | [`67b51c65e9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/67b51c65e9d137728c3b09a39b6c6e762bdeb5f7) | Solessfir | bShowFrameRateAndMemory=True |
| 2025-11-21 | [`24c04b02b6`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/24c04b02b6619be67b02d09ba80e8cfb349373bc) | RedPixel | Removed Lumin Plugins |
| 2025-11-21 | [`37ce30ba9d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/37ce30ba9db925c36d3a771c092f069ee1ed5131) | RedPixel | Revert "Partial backport Shader Compilation Task Handling Improvement" |
| 2025-11-21 | [`353257fc77`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/353257fc772e650031a25ea70512875045252c8a) | RedPixel | Revert "Added FFMPEG media player plugin" |
| 2025-11-21 | [`f95f5cf610`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f95f5cf6101962b212abf9cd3f4d662fdb2dfb40) | RedPixel | Added FFMPEG media player plugin |
| 2025-11-21 | [`d0b0f43007`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d0b0f430077d54b327d3fc6cb589ec52fdf54d67) | RedPixel | Removed Magic Leap from default |
| 2025-11-21 | [`e9aebc2ef9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e9aebc2ef9f8acb7326a7e989f288ef68969342f) | RedPixel | Disabled More Plugins, VR needs to be enabled |
| 2025-11-20 | [`6c5948bf12`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/6c5948bf12ea61f82784193ccaa5d43c4f574ae9) | RedPixel | Disabled More Default Plugins |
| 2025-11-20 | [`20dc65e269`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/20dc65e269655a5948a76e22c48e636d5897ff2c) | RedPixel | Removed unnecesary constructor |
| 2025-11-20 | [`76554f4b8b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/76554f4b8b5a7c02e56e34af8d3e40447412f4ed) | RedPixel | Partial backport Shader Compilation Task Handling Improvement |
| 2025-11-20 | [`5fdcd5d800`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/5fdcd5d800a8203bc54bcc078e4a3a9d442e456c) | RedPixel | Rework shader compilation thread allocation on higher core machines (+12 logical cores) to reserve 50&#37; of the cores for non-shader compilation work. |
| 2025-11-20 | [`4d6aee57e9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/4d6aee57e9c2c223ff5411fe4cd6f920bffb8bef) | RedPixel | Reduce ShaderCompilingThread activity while waiting for compile results. |
| 2025-11-20 | [`1ae98e4545`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1ae98e454550ad1017f7bfb34e5e80eb58f64930) | RedPixel | Reduce overhead of gathering ray tracing instances |
| 2025-11-20 | [`2e8b11907a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2e8b11907a8747ac13ca6ed341a8087e39b5657e) | RedPixel | Added Motion Matching Plugin: Motion Symphony (based on Ubisoft's Implementation) |
| 2025-11-20 | [`ae9b69a921`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ae9b69a92102038013feb6fd0333d27d32ad01c9) | RedPixel | Revert "Updated Vector.isph with better performant uniform overloads" |
| 2025-11-20 | [`875e694693`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/875e69469337a7339271925b860c24ea5538054d) | RedPixel | Optimize/Fix frame rate limit in unreal |
| 2025-11-20 | [`f3aa602859`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f3aa602859f30aad99b4dcfec1813c46574f7e63) | RedPixel | Updated Vector.isph with better performant uniform overloads |
| 2025-11-20 | [`b298c37d2f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b298c37d2f77c91ce5ad7e0132cf1b5cc55acda1) | RedPixel | Adapted PR EpicGames#9027: Fix navmesh generation for hierarchical instanced static meshes (Contributed by MichaelBell) |
| 2025-11-20 | [`89f25599bb`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/89f25599bb343affb4be767f9872f23d990c6f5f) | RedPixel | PR EpicGames#9028: Fix navmesh generation for Landscape Mesh |
| 2025-11-20 | [`f1d17858fc`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f1d17858fcd3c9dcb28f5efca2d05d20a1d068d0) | RedPixel | Performance improvement to geometry collection for navmesh |
| 2025-11-20 | [`f4fba4b15f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f4fba4b15f91d75644395b5fa7df05a69c7c29c2) | RedPixel | Update KismetCompiler to use IsEmpty now that the array class is updated |
| 2025-11-21 | [`d5a417709c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d5a417709cc403afa01c787c661989e96c833806) | Solessfir | NewsFeedSettings category is not used in code at all |
| 2025-11-20 | [`83f0f997bf`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/83f0f997bf85ced144fa3b20fad68dd31fc6df4a) | RedPixel | Friend Optimization for Map,Set and Tuple: Compile time optimization |
| 2025-11-21 | [`09e671bb78`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/09e671bb7874764503cec5456af2e384a00ba61b) | Solessfir | SendUsageData=False and SendUnattendedBugReports=False |
| 2025-11-21 | [`9af0349c18`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/9af0349c1832b7094ceae7f47ba8ca5d261e0e69) | Solessfir | Add config var to disable ShowNewPluginsPopup |
| 2025-11-21 | [`d9fd593e11`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d9fd593e11581fd93d0ff60b2933794f150b4780) | Solessfir | bDisableAllTutorialAlerts=True |
| 2025-11-20 | [`02d7c0ad0a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/02d7c0ad0a7542b382a70dc3e37877d6ec052d76) | RedPixel | OverlapEvents disabled by default for Primitive Component |
| 2025-11-20 | [`c8d176b465`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/c8d176b465a3fb05b0dbe3b8d74d91d6e2df1ec1) | RedPixel | Added Array: IsEmpty function for compability |
| 2025-11-20 | [`ff10fda9eb`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ff10fda9ebe651b511d06ca402fc664ce3e59eb3) | RedPixel | Do lighter weight component update for RecompileShaders() |
| 2025-11-20 | [`971fa08fb3`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/971fa08fb315430ff2989c3464f2f2192b286429) | RedPixel | Speed up ODSC shader map processing from ~27.5 ms to ~6.1 ms on average. |
| 2025-11-20 | [`cc8e21377b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/cc8e21377b51a4737f3c87cfcb6888fcda77ecbd) | RedPixel | Save about 25&#37; of total cook memory usage by releasing the read buffer cache in FlushCache |
| 2025-11-20 | [`9a6b545ffd`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/9a6b545ffdf472c05b3ce76672c4b8939f224516) | RedPixel | MEMORY: Defer allocation of streaming buffer for Pakfile reader until it's actually used. Saves 1MB |
| 2025-11-20 | [`864acb077a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/864acb077aa69d41978d018b79c7e22ae6ed27f0) | RedPixel | Optimize slate text kerning by removing string hashing from critical path in CompositeFont |
| 2025-11-20 | [`ba21fb2de7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ba21fb2de76877f625c26a39b4025cecd03e7b22) | RedPixel | Fix PSO cache not being picked up. |
| 2025-11-20 | [`933dd97169`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/933dd971695477175c5943020e61187e741f61d2) | RedPixel | Default RHI set to DX12 |
| 2025-11-20 | [`6c3a7f6e77`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/6c3a7f6e777aaeae3cbd0a977e55909561fd4a99) | Solessfir | Add support for VS 2026; Remove support for VS 2015 and VS 2017 |
| 2025-11-20 | [`ed12dba09c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ed12dba09c83f682cef5399856ff4ce91f26ba6f) | Solessfir | Update GitDependencies and MemoryProfiler .NET from 4.5 to 4.8 |
| 2025-11-20 | [`3c115f99bb`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3c115f99bbf704dcf0fb66bd2b18df5bc91d808c) | RedPixel | Hash runtime Optimizations |
| 2025-11-20 | [`5953831a6e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/5953831a6e48c72d1c35114fad8156da03250043) | RedPixel | skip parallel rendering for incompatible non whole scene shadows |
| 2025-11-20 | [`6ad0124d73`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/6ad0124d7355f5ee681929d6e7e0c168e92a2abf) | RedPixel | Asset Data Gather: Added Lambda to improve contextual parallelism |
| 2025-11-20 | [`002a9bcb7d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/002a9bcb7d603a740dcd7dd034e93758a2ec39a3) | RedPixel | Shader Compiler: Increased MaxShaderJobBatchSize for improved compile times |
| 2025-11-20 | [`64c1111189`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/64c1111189f9dbeec8e010e6ee3253f249c8b78c) | RedPixel | Shader Compiler: Minor Optimization for path hashing |
| 2025-11-20 | [`a7c826d4c4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a7c826d4c4adff869f27fb48a8fefa00b98972f4) | RedPixel | Unity build optimization: split according to processors available |
| 2025-11-20 | [`3c5cede8c1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3c5cede8c1f65be2438dc9ea4c4af88dbcf8869a) | RedPixel | Fixed Tick Kismet PR |
| 2025-11-20 | [`b94e7b59f9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b94e7b59f9bc4914f00d2a19446060914c3912cc) | Solessfir | Backport: Raycast navmesh crash fix |
| 2025-11-20 | [`0e3d2b9315`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0e3d2b931573163242335fe176c1df7411484cbe) | Solessfir | Backport -clearPSODriverCache option |
| 2025-11-20 | [`aa765d8492`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/aa765d8492d1038dc5cce6a6f836de03fbfefb46) | Solessfir | Don't tick empty BP Tick func |
| 2025-11-20 | [`e48745550e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e48745550e74f83d8d89840958ae9cde649b059d) | Solessfir | Dynamic cast: Jump Target (Double Click) |
| 2025-11-19 | [`f29028ae85`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f29028ae85f367151005da598a001ae698fc6f07) | Carlo V. | Update ToolChain Instructions Readme.md |
| 2025-11-19 | [`53ef9e5799`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/53ef9e5799a6505d74b1dcded1d14b7ffe277db4) | RedPixel | BPs no longer get defaults nodes added: Tick/Overlap/Begin Play |
| 2025-11-19 | [`15b5961b46`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/15b5961b46c12760f2addbba4e3d7460a24b933c) | RedPixel | Sparse Array performance improvement |
| 2025-11-19 | [`e3fbd2dfd7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e3fbd2dfd78ce3ebc735387b8cad66257e3cb6fd) | RedPixel | Added ACL Plugin, enabled by default |
| 2025-11-20 | [`13f590a3b2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/13f590a3b2d275dd09c85df5baeb9ceb636e3e73) | Solessfir | Disable Tutorial button |
| 2025-11-20 | [`adfd6d678d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/adfd6d678d2e7045b5a1f081c5eb48d6a0718c0a) | Solessfir | Remove Marketplace button from Toolbar |
| 2025-11-20 | [`1b19f1b339`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1b19f1b3398a3a66f25fca31a53fe0a5b131a33e) | Solessfir | Do not force open Epic Games Launcher |
| 2025-11-20 | [`02642ec9ad`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/02642ec9ad197eb15062a19b9a0219405fba7e4c) | Solessfir | DDC Badge alignment fix |
| 2025-11-19 | [`fcc782f8e1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fcc782f8e11a53adbc71c17ef1056e9ff9e7fa78) | RedPixel | Revert "Clang 13.0.1 Upgrade: batch 1" |
| 2025-11-19 | [`2cac85a0c1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2cac85a0c14f7b1ffcb3d1a4afc96f3db7a18994) | RedPixel | UE Editor Loading Optimization |
| 2025-11-19 | [`7125b70ff2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7125b70ff25f8932260b6adba90708ebb01b27f4) | RedPixel | Use Basic Eye Adaptation on mobile by default. Saves 0.7ms on S10 |
| 2025-11-19 | [`190001a343`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/190001a34352d11f785c122999750ce35f289840) | RedPixel | Don't allocate shared serialization info until needed |
| 2025-11-19 | [`c71169a719`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/c71169a719d49cc6fe3b63412a4c4de8c83cd58e) | RedPixel | Potential fix for water sampling depth outside of valid UV range after gather4. |
| 2025-11-19 | [`d4578766bc`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d4578766bc94c1a2022ebd3ae1b887db1e8ab956) | RedPixel | Don't parse the commandline every frame to check if the movie player should be disabled |
| 2025-11-19 | [`b0d1dd4a26`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b0d1dd4a263e5429e7ac2c8bde4bda4ea793c4bb) | RedPixel | Disabled More plugins |
| 2025-11-19 | [`918aeffcca`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/918aeffcca410edc601554d1655861b4f72959b5) | RedPixel | ISM performance Increase for AI Navigation |
| 2025-11-19 | [`534a03083e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/534a03083e01140e7583568362971e9b6f9461f2) | RedPixel | Deactivated largely Unnecesary default plugins |
| 2025-11-19 | [`17d6667299`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/17d6667299e17ed912807cc7ddbd93a32b50cda6) | RedPixel | Fixed SLN generation issue |
| 2025-11-19 | [`3a18cce00d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3a18cce00d31a210f0e81ebbf30f5d662c9588ab) | Konstantinos Leriou | UE5 Vite Backport some of my commits |
| 2025-11-19 | [`64d2eec9a4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/64d2eec9a4c9ecccdb5f26a14c9ddc9ad2929fc8) | RedPixel | GitIgnore updated to ignore rider and added working FSR2 |
| 2025-11-18 | [`2fac6b3f35`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2fac6b3f350d8a3327daa8d2a8fa93017f96c9b0) | fletch | Disable SteamVR Plugin By Default |
| 2025-11-18 | [`cb9e2064d2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/cb9e2064d2f6773310e307f036310d5dc0a3d706) | RedPixel | Clang 13.0.1 Upgrade: batch 3 |
| 2025-11-18 | [`4df5d21d2b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/4df5d21d2b3a97e69a0c3321bf301a96446b5c9e) | Carlo V. | Update README.md |
| 2025-11-18 | [`98fd7f2ee1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/98fd7f2ee116ac5fd1c9b6c2b2a4c3e038fdbeca) | Carlo V. | Update README.md |
| 2025-11-18 | [`cc472975c3`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/cc472975c310c642572aacd9971dc35379974e6e) | TungNguyen | Revert this commit " \[rt\]\[translucency\] fix the issue that r.RayTracing.Translucency.GI doesn't work " |
| 2025-11-17 | [`b2c4b4cc51`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b2c4b4cc518ed05b27f9062318ee78933696c7e8) | Carlo V. | Update README.md |
| 2025-11-17 | [`ea2f6cbf8b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ea2f6cbf8b32736b610daf791037de3650815319) | TungNguyen | change gamedir cache |
| 2025-11-16 | [`214f5cd0ac`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/214f5cd0acdb9d0a45727fe149d6d267df9e0487) | RedPixel | Fixes compile with msvc |
| 2025-11-16 | [`eaa2202a00`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/eaa2202a0028766acbc3698d2c9009f7f66b4544) | RedPixel | Clang 13.0.1 Upgrade: batch 2 |
| 2025-11-17 | [`57641f73c2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/57641f73c2b687c06c913e87041081792564e2ee) | TungNguyen | update for tressFX |
| 2025-11-15 | [`cb1ffe31a6`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/cb1ffe31a6f2b077912114e070c909d423727ac2) | Carlo V. | Update README.md |
| 2025-11-15 | [`b349e756e8`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b349e756e8d64a1c8f54053cd09e2fcfab2c184b) | Carlo V. | Update README.md |
| 2025-11-15 | [`e4cf1d1f4b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e4cf1d1f4bbe0796b547bfe281b1459c12f69d26) | RedPixel | Clang 13.0.1 Upgrade: batch 1 |
| 2025-11-15 | [`07b2b666f1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/07b2b666f15b2921223610ad0446498bbe234eb1) | RedPixel | Fixed commit deps |

<!-- END GENERATED COMMIT RECORD -->

## See also

- [All release notes](Release-Notes.md)
- [ueVite26 March Major](ueVite26-MarchMajor.md)
- [Original Vite](Original-Vite.md)
- [Engine Default Changes](Engine-Defaults.md)
