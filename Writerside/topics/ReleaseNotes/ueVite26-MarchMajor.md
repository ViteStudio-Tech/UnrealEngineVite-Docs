# ueVite26-MarchMajor

<tldr>
<p>
The first 2026 major release expands stylized shading, ray-tracing efficiency, anti-aliasing and platform compatibility.
</p>
</tldr>

| Release window | Status | Captured commits | Source branches |
|---|---|---:|---:|
| 1 January–31 March 2026 | Major | 48 | 1 |

## Highlights

- Adds the Toon Shading Model and completes the major-release integration.
- Reduces ray-traced reflection payload size, improves DDGI skylight contribution and updates SSAO optimization controls.
- Improves SMAA and FXAA quality/performance and fixes TressFX compilation on Android.
- Adds Android NDK 29 support, C++20 compatibility fixes and updated EOS SDK binaries.

## Scope and sources

Commits are captured by committer date from 1 January through 31 March. Later maintenance on the named branch is excluded.

| Source | Branch |
|---|---|
| Release branch | [`ueVite26-MarchMajorRelease`](https://github.com/ViteStudio-Tech/ueVite-Internal/tree/ueVite26-MarchMajorRelease) |

## Commit record

### Release branch

Branch: [`ueVite26-MarchMajorRelease`](https://github.com/ViteStudio-Tech/ueVite-Internal/tree/ueVite26-MarchMajorRelease)

| Date | Commit | Change |
|---|---|---|
| 2026-03-12 | [`d0cc9ff063`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/d0cc9ff0637c7eb1f571ffd94ad8a646432143da) | [Major Release] PR 123: Toon Shading Support |
| 2026-03-12 | [`a75fc9d521`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/a75fc9d521a137515cecd1d68618fdc66e8dad6b) | Add Toon Shading Model |
| 2026-03-11 | [`c1ef4b9026`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/c1ef4b9026b39451e90569b9e5c00adcc110ef1d) | Merge pull request #122 from tuhoiisa/ueVite26-release-staging |
| 2026-03-11 | [`9700dee4db`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/9700dee4db561fec7f13e59a657c72cebab16739) | Updated README for major Release |
| 2026-03-09 | [`3c5c8c5e04`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/3c5c8c5e0481dfb2630716a2160320ca3394474b) | Merge pull request #121 from tuhoiisa/ueVite26-release-staging |
| 2026-03-08 | [`01064dbf99`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/01064dbf99a66e24978ba70f3bd857610243f408) | Add files via upload |
| 2026-03-08 | [`ed8f6d79cd`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/ed8f6d79cd0e04274db17a9f166f4abd31026057) | Delete Engine/Content/Splash/1 |
| 2026-03-08 | [`358ca03a57`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/358ca03a57eff330d4a22a67d764a9f950ec9400) | Add files via upload |
| 2026-03-08 | [`27b7da9396`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/27b7da939645a9a68ec1e2170bca46fe8a9e8090) | Create 1 |
| 2026-03-07 | [`08d0a14116`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/08d0a141160b7e414c400d2b4d25c45667ed8eab) | Merge pull request #119 from cryptosebek/WinSetupFix |
| 2026-03-07 | [`54386fd3a2`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/54386fd3a26afb5965af3262a28655bc7c23b880) | Merge pull request #118 from EmptyBucket123/ImprovedFXAA |
| 2026-03-07 | [`466dd781d9`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/466dd781d9a90b546694951893dac13ecbfee370) | Merge pull request #120 from ViteStudio-Tech/ueVite26-release |
| 2026-03-07 | [`0baffd6866`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/0baffd68665211d6a6eae7743b6001f2cebb4f10) | Fixed funny issue on the original SMAA Comment that mentioned a header |
| 2026-03-07 | [`5aa3a30cef`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/5aa3a30cef1731ef4539502b2652dd16c67e2ef1) | [Rendering][RT] Optimizations to Raytraced Reflections |
| 2026-03-07 | [`a762eec480`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/a762eec480902d15bbb9e4d3d743515145f0cf78) | Fix TressFX compilation on Android |
| 2026-03-07 | [`2c7bbf91d3`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/2c7bbf91d32accc2906c0d78c81700b53d7a10dd) | [Rendering] Updated Optimizations Options for SSAO |
| 2026-03-07 | [`a581412e8c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/a581412e8cd078ec478ee902da4270adbb709297) | [Rendering] SMAA Improvements. Performance and added Quality Levels |
| 2026-03-07 | [`8941cf40c9`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/8941cf40c93a9b5cd45edbe49a3fa6e9f60e5429) | [Rendering][RT] DDGI SkyLightContribution improvement |
| 2026-03-06 | [`fa37fbb106`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/fa37fbb106dc95763e3876f9e5c998e5a0a56323) | [Rendering][RT] Optimization to Raytraced Reflections: Introduction of 32 Bytes Payload and Updated Settings |
| 2026-02-28 | [`02540a9075`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/02540a907509c0f9d753b77170a455babd8b6d24) | [Win] Fix GitDependencies cache path parsing with spaces in Setup.bat |
| 2026-02-23 | [`efd077cc29`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/efd077cc29296b66d5b1254d6059cf13710590df) | Merge branch 'ueVite26-TressFX-Staging' into ueVite26-release |
| 2026-02-22 | [`b38463a033`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/b38463a03354d38c26964aae5ac2bd83abe9fd64) | [Rendering] Improved FXAA quality and performance. Backport fix for RDG pass flags validation and ERHIAccess::IndirectArgs |
| 2026-02-18 | [`2d3b3eabc7`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/2d3b3eabc7618b64f5d8d13033151f940eb25f2a) | Support Android NDK 29. Fix a couple of C++20 compilation errors to support this. |
| 2026-02-18 | [`1e951b592f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/1e951b592f1a7ca57569a923a35db1e553a2b225) | EOSSDK Release 1.19.0.3 CL 49960398 Binary Only Update |
| 2026-02-13 | [`6b31a7518e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/6b31a7518edbc346e9f0f47586d0b324cb8ca996) | [Ini] Moving DerivedDataCache back to Engine Dir |
| 2026-02-11 | [`8c96426eb7`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/8c96426eb74908fb56cdf00466a0c48174d3158f) | [Plugin] Ported Splash Damage's Abilities and Automatron Plugins |
| 2026-02-11 | [`9a2c9565de`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/9a2c9565de73074e4119b946d2bd7f60bc5d559f) | [Defaults] OverlapEvent re-enabled for Character Capsule |
| 2026-02-11 | [`2d60650150`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/2d606501509e928d14ab0173b6af18f56f40c3a3) | Re-enabled WindowsMoviePlayer Plugin for Movies to work without needing activate the plugin in projects |
| 2026-02-11 | [`886a086526`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/886a086526bc67fb6d50679e7a28d4b6ca9d9443) | [Rendering][Forward][translucency] Patch over NvRTX, Color write Clear now only runs with SeparateTranslucency on Forward |
| 2026-02-10 | [`e8c5f313ec`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e8c5f313ec3b66893fe34976dcd715e7d857733d) | Feature Pack IterateDirectory instead of FindFilesRecursively |
| 2026-02-05 | [`310541083f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/310541083f4aaed970bc90139abaae8639192b52) | [Rendering] SSAO Optimization |
| 2026-02-05 | [`7546a4919e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7546a4919eacde07daf33bec8fd0ce1777317fc7) | Merge pull request #115 from KonstantinosLeriou01/LinuxToolChainFix |
| 2026-02-05 | [`4e74d06c6b`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/4e74d06c6b46f2662cebf43940e5966e17c3fcb1) | Fix Linux Toolchain Error when building linux server |
| 2026-02-05 | [`11e1b16822`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/11e1b168227d3b48c17f2fe73198d18e80150a0c) | Merge pull request #114 from KonstantinosLeriou01/LinuxToolChainFix |
| 2026-02-05 | [`38e696e2bf`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/38e696e2bf3f3064d53bc5bc98851f871f96cf49) | PythonFixes |
| 2026-01-29 | [`7f88fbb40b`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7f88fbb40b6cee9d1e77a1bc749088cdc5f58335) | [Rendering] TressFX Staging - Part 2 |
| 2026-01-28 | [`abce6475bc`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/abce6475bc2236cbdafd20fa93310f871d8e0818) | [Rendering] TressFX  Staging - Part 1 |
| 2026-01-20 | [`21a8e31232`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/21a8e312320f63932e6b193f0886fde51861bea7) |  Shader Compile Default config to use Windows Scheduler |
| 2026-01-19 | [`56fdef5d6d`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/56fdef5d6d2ba35083a7d37432515e4ce90dccaa) | [Rendering][rt][translucency][fix]  Patch over NvRTX 4.27 commit, fixes SSGI when used in tandem with DDGI |
| 2026-01-04 | [`bdeb57a3d2`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/bdeb57a3d2e63c03d66394b455ca099cac34a836) | [Rendering] [rt][translucency] fix the issue that r.RayTracing.Translucency.GI doesn't work. |
| 2026-01-04 | [`ed51ed1ec8`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/ed51ed1ec89417a66c6b58ed1b774cd56bdacaad) | Reapply "Reduce ShaderCompilingThread activity while waiting for compile results." |
| 2026-01-04 | [`d810809fca`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/d810809fca3ee10ad0ea13e67ca5069adf593b02) | Revert "Update Shader Compiler" |
| 2026-01-04 | [`1fcd08fec0`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/1fcd08fec08dc663db252aaccf4e72c63c91a412) | Update Shader Compiler |
| 2026-01-04 | [`9fbef43228`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/9fbef4322883779b370829dedf587aa347c8a620) | Reapply "Shader Compiler: Minor Optimization  for path hashing" |
| 2026-01-03 | [`ed4a6f1f1b`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/ed4a6f1f1b7609f935bf524dec9f8caf27a884a9) | [Plugin] Upgraded Kawaii Physics with a ported 1.18 UE5 version |
| 2026-01-03 | [`881262032a`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/881262032a0a71053f83c02eb6f0cc471df361d8) | Commit Fix, texture UAsset, add updated uassets |
| 2026-01-03 | [`413c6372e1`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/413c6372e116fa4bd093815220cfd8cff0da846a) | Commit FIX, Texture uasset |
| 2026-01-03 | [`d5ab7a6ae9`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/d5ab7a6ae998496cb6d0fcd3454e48325f885184) | [Rendering] Improved SMAA |

## See also

- [All Release Notes](Release-Notes.md)
- [Engine Overview](Engine-Overview.md)

