# ueVite26-JuneMajor

<tldr>
<p>
The June line concentrates on animation backports, renderer correctness and measurable CPU/GPU savings.
</p>
</tldr>

| Release window | Status | Captured commits | Source branches |
|---|---|---:|---:|
| 1 April–30 June 2026 | Major | 38 | 1 |

## Highlights

- Backports BlendSpace smoothing, spring-damper and easing modes, blend profiles, pose snapshots and montage blend overrides.
- Fixes ray-traced shadows and capsule indirect shadows and removes a ray-tracing world-instance stall.
- Skips redundant scene-proxy transforms and explicitly unrolls the TAA loop for platform-specific DXC gains.
- Adds installed-build helpers through LocalBuilds and RunUAT.

## Scope and sources

Commits are captured by committer date from 1 April through 30 June. Later maintenance on the named branch is excluded from this release window.

| Source | Branch |
|---|---|
| Release branch | [`ueVite26-JuneMajorRelease`](https://github.com/ViteStudio-Tech/ueVite-Internal/tree/ueVite26-JuneMajorRelease) |

## Commit record

### Release branch

Branch: [`ueVite26-JuneMajorRelease`](https://github.com/ViteStudio-Tech/ueVite-Internal/tree/ueVite26-JuneMajorRelease)

| Date | Commit | Change |
|---|---|---|
| 2026-06-04 | [`3c524b5bf9`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/3c524b5bf9646237a7cee631285a3cbcc92295e4) | [Rendering][Backport] Fix general RT shadow issue because of an unmatched sqaure for the encoding of the shadow |
| 2026-06-04 | [`fe283b990c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/fe283b990c64eea95683525c593cbdad3a7a6118) | [Rendering][Backport] Allow capsule indirect shadows in projects that don't support static lighting. |
| 2026-06-04 | [`52982fbb9a`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/52982fbb9af09c6c298ca672ba6383918acf24e2) | [Rendering][Optimization][Backport] Optimization to remove stalling in FDeferredShadingSceneRenderer::GatherRayTracingWorldInstancesForView() |
| 2026-06-04 | [`96ee43fb96`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/96ee43fb9614c41ec60cd409c1bea5c5236789bd) | [Optimization][Backport] Implemented redundant transform skipping for scene proxies, which saves ~4ms of GPU, ~2.17ms GT, and ~4.81ms of RT in the golem scene, and numerous other expensive locations (cuts shadow depth time in half, and cuts out time from GPUScene update). |
| 2026-06-04 | [`94a7034c9c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/94a7034c9c928b1e44afdd8a54bf378c6f75756b) | [Rendering][Optimization][Backport] Explicitly unroll loop in TAA shader to improve platform specific DXC performance. This improves TAA on certain platforms with DXC by roughly 0.5ms. |
| 2026-06-03 | [`bd2211b5e8`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/bd2211b5e8c494b36a894204d163f5361a9c2963) | [Animation][Backport] Added UAnimInstance::AddPoseSnapshot and GetPoseSnapshot |
| 2026-06-03 | [`eda868b42c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/eda868b42c489f7d1fefccc48c937d885bd62c83) | [Animation][Backport] Improve the way the preview position etc are shown and used |
| 2026-06-03 | [`e266f0a1a7`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e266f0a1a769da45ee4e5230dfbd33a3fdafeff1) | [Animation][Backport] Show the current as well as target preview position in BlendSpaces |
| 2026-06-03 | [`0c939792d9`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/0c939792d9c969ea134170b5fc2bb92762468e3c) | [Animation][Backport] Fix for crash in duplicate/retargeted blendspace from missing samples |
| 2026-06-03 | [`66f7fca1fd`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/66f7fca1fdf2fd88b83cb723fcc176787331b233) | [Animation][Backport] Fixed BlendSpace filters being allocated even when they are not in use Saves ~2.6MB peak in synthetic tests |
| 2026-06-03 | [`1e7b07dc46`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/1e7b07dc46530b4ad7277237285b2030ab2f4215) | [Animation][Backport] Fixes for per-bone smoothing with blendspace graphs |
| 2026-06-03 | [`28d7add77d`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/28d7add77d5eb8244c16792f64a8f80d06a53673) | [Animation][Backport] Improve Blueprint Spring Interp behaviour |
| 2026-06-03 | [`977cba7649`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/977cba764905e3951408a7d20c7f1d42593bcc0f) | [Animation][Backport] Improve BlendSpace Smoothing, adding options like SpringDamper, Ease In/Out and Exponential |
| 2026-06-03 | [`bf9b627493`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/bf9b627493fc593979a07cc8dd8d059ea277b791) | [Animation][Backport] Remove the sorting of the per bone BlendSpace smoothing overrides in the UI |
| 2026-06-03 | [`8fa2fcfeab`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/8fa2fcfeab7df22e3136c6fbe3c80f315bfeacf2) | [Animation][Backport] Ease in/out for the target weight interpolation in BlendSpace. |
| 2026-06-03 | [`90153d4240`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/90153d42400803479c4e1cab40d0d6bb4bbda20b) | [Animation][Backport] CL 14798723 Part 2 |
| 2026-06-02 | [`51144c4bc9`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/51144c4bc95be3c4cc3d6087fc6a31c75a509e43) | [Animation][Backport] Move blend profile customization to its own PropertyTypeCustomization. |
| 2026-06-02 | [`e21ae16c1d`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e21ae16c1dd21e1b4ac6b8d70edd0ef70712dddb) | [Animation][Backport] Add support for blend profiles inside anim montages and blend nodes. |
| 2026-06-02 | [`59259bbc6e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/59259bbc6ef14b4d6498964da19eab66e2a2969d) | [Animation][Backport] -Added Blend Profile mode selection to blend profile picker. |
| 2026-06-02 | [`7786d064bd`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7786d064bd2d16c88dc3b4c2a8293a808300c1ef) | [Animation][Backport] Improve the Blend Profiles by allowing time based profiles. |
| 2026-06-02 | [`f04400ae9d`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/f04400ae9d119a48207993acf39f9ed528824deb) | [Animation] Adding the option to override BlendIn/BlendOut settings on Montage_Play/Stop |
| 2026-06-02 | [`c0889790e8`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/c0889790e82cdf63c87ec3c2d3f832192e9476ca) | Add LocalBuilds files + RunUAT.bat (Binaries Build) |
| 2026-05-26 | [`e9558904e6`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e9558904e6ceea0cd0affa4de76e8dc992949c98) | Cleaning Tonemapper UAssets |
| 2026-05-14 | [`d34d309622`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/d34d309622ec366e7cdd28094f66bce3e45e9d68) | Gitdeps: Removed Unreal Vainilla Splash |
| 2026-05-14 | [`c2665fd06a`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/c2665fd06a8bfa6641d684be80e8ff80d6dffb49) | Merge branch 'ueVite26-release' of https://github.com/GapingPixel/UnrealEngineVite-PhysX into ueVite26-release |
| 2026-05-14 | [`dce9ee06ea`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/dce9ee06eabcb3476963d760433d51fa0f22603c) | Merge remote-tracking branch 'origin/4.27-plus' into ueVite26-release |
| 2026-05-14 | [`2f547b2695`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/2f547b2695f76355440957146db63e3eb7260dd1) | Merge pull request #132 from ViteStudio-Tech/ueVite26-release |
| 2026-05-14 | [`40f0b0c918`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/40f0b0c9185475c0552de414620f4e0ca7268485) | [ShaderCompiler][Backport] Backports the STB-based shader preprocessor path from UE5.7 |
| 2026-05-14 | [`e6afce3da0`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e6afce3da089d16ac37f1f6ac90ecf8fd33feb19) | Merge branch 'GapingPixel:ueVite26-release' into ueVite26-release |
| 2026-05-14 | [`f621b210c1`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/f621b210c12bbb77b403b9b9e52250ab9c31961b) | Merge remote-tracking branch 'origin/ueVite26-release-staging' into ueVite26-release |
| 2026-05-13 | [`5539207b01`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/5539207b0184700cb8bdaa4ce1f75218a46bd926) | Merge branch 'GapingPixel:ueVite26-release' into ueVite26-release |
| 2026-04-30 | [`dbbdc07df2`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/dbbdc07df2b5086beade988eaf4e46d8eea74d09) | EOSSDK Release 1.19.0.7 CL 52449437 Binary Only Update |
| 2026-04-27 | [`abc0b9b9a1`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/abc0b9b9a190372e7f6d25a1416c60986dd13a11) | [Rendering] Fix LPV GI not affecting landscape unless landscape is selected in editor |
| 2026-04-27 | [`a2cd3bbc52`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/a2cd3bbc52214e23c066feaf2e1cf3e57ae6b486) | Merge pull request #129 from sellano/ueVite26-release |
| 2026-04-27 | [`50d09878e7`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/50d09878e7ae7e4b26a0e69c84b00564bf934127) | [Backport][Shader Compiler]  Fix memory leak of shader code during shader compilation (during cooks, deployments, or editor). |
| 2026-04-14 | [`0ce2248bef`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/0ce2248beff32610f6cd40bdbe2256152f841e25) | switch material graph node |
| 2026-04-10 | [`93145d9f97`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/93145d9f97df1ce53701dd6b24e737bb4609cd06) | Merge pull request #127 from ViteStudio-Tech/ueVite26-release |
| 2026-04-10 | [`df37698b61`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/df37698b61554cb182be8e9da8b109c2bf1fa1fe) | [Rendering][Backport] Fixed invalid order of GTAO input textures |

## See also

- [All Release Notes](Release-Notes.md)
- [Engine Overview](Engine-Overview.md)

