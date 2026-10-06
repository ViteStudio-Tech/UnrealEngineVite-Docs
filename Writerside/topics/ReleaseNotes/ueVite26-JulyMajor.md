# ueVite26-JulyMajor

<tldr>
<p>
A dense integration release focused on PhysX Blast, fixed-step simulation, renderer gating, plugins and current Windows toolchains.
</p>
</tldr>

| Release window | Status | Captured commits | Source branches |
|---|---|---:|---:|
| 1 July–1 August 2026 | Major | 148 | 1 |

## Highlights

- Integrates the PhysX Blast plugin and engine-side support, plus an opt-in fixed-timestep PhysX path.
- Adds project-setting toggles and compile-time gating for ray tracing, DLSS, translucency and mobile/TressFX paths.
- Backports forward-renderer MSAA and velocity fixes and revises SSAO, shadow and SSGI defaults.
- Adds an ImGui benchmark tool and validates VS 2026/MSVC 19.50 with Windows SDK 10.0.26100.

## Scope and sources

Commits are captured by committer date from 1 July through the branch tip at 1:27 a.m. on 1 August, preserving the final release commit that landed just after midnight.

| Source | Branch |
|---|---|
| Release branch | [`ueVite26-JulyMajorRelease`](https://github.com/ViteStudio-Tech/ueVite-Internal/tree/ueVite26-JulyMajorRelease) |

## Commit record

### Release branch

Branch: [`ueVite26-JulyMajorRelease`](https://github.com/ViteStudio-Tech/ueVite-Internal/tree/ueVite26-JulyMajorRelease)

| Date | Commit | Change |
|---|---|---|
| 2026-08-01 | [`f934b45b7b`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/f934b45b7bdac0c022752accc2505f541ce78235) | Cached localized IBL CVar |
| 2026-07-31 | [`7def2d7051`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7def2d7051cfc466c98c3857ba1c9bbbddc8f3a2) | [gitignore] Updated to include PhysX-Blast Plugin content Folder |
| 2026-07-31 | [`74d9dea475`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/74d9dea475d0170f2380398c19603f33189c79b6) | [Toolchain] Compiling on VS 18.8.2 (_MSC_VER 1950) and Windows SDK (10.0.26100) for Windows 11 |
| 2026-07-31 | [`70827df2f2`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/70827df2f2a41b40ffdc000227391af0c7456b05) | [Editor] Added Raytracing feature toogles to Rendering Project Settings |
| 2026-07-30 | [`a0855402e0`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/a0855402e0efb285c5d9e97ac4dbcf874571d678) | [Rendering] AmbientOcclusion Macro Update |
| 2026-07-30 | [`f4830395a1`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/f4830395a1b40eae4f8777369115849b2fe5982f) | [Plugin] Replacing PlatformAllowList with WhitelistPlatforms |
| 2026-07-29 | [`7ba848ec89`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7ba848ec89d290299ef572f676017a8aad3fb23e) | [Gating] RT Translucency Guard |
| 2026-07-29 | [`051cde6cd7`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/051cde6cd72edb8338bc9f0f91bf9ce488885469) | [Gating] DLSS |
| 2026-07-28 | [`303d941785`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/303d9417852c196854cff449431230d4e26c79ed) | [Backport 5.3] Unconditionally disable velocity output in base pass for Forward Desktop (UE-169988).  #rb Robert.Srinivasiah, Jules.Blok [REVIEW] [at]Jules.Blok, [at]Robert.Srinivasiah #jira UE-169988 #rnx #preflight 6411d252924023147d96f7f6 |
| 2026-07-28 | [`73517832e5`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/73517832e51d2d9cf90d2e1c85ed7620389656ac) | [Backport 5.3] Fix MSAA being broken in forward (UE-166561). |
| 2026-07-28 | [`e8f1a55052`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e8f1a5505212c50ab8bae0b5411cc204d854b26b) | Merge pull request #156 from ViteStudio-Tech/ueVite26-JuneMajorRelease |
| 2026-07-28 | [`961335bc19`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/961335bc1992086e6fb80a80c596c4e973e8e7d4) | [Rendering] Updated SSAO Vite Optimization mechanism |
| 2026-07-28 | [`6b02db435a`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/6b02db435a9b8468c11725dbe71753b0dc283346) | rt pso debloat |
| 2026-07-25 | [`495dee40b9`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/495dee40b91b22586de739dc1a14a8f5a927e6cb) | Merge pull request #154 from ViteStudio-Tech/ueVite26-JuneMajorRelease |
| 2026-07-25 | [`f72ff015f5`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/f72ff015f5badbd152694d992be09bb26cef59ee) | [Plugin] PhysX Blast + Engine Side Changes for proper support |
| 2026-07-23 | [`8f2cce17b7`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/8f2cce17b751c56f21c4526be0f944fc5a22350f) | ueVite26-June Major Release: Update README.md |
| 2026-07-23 | [`9832bc74ed`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/9832bc74ed94609693f49d67c67f2ba3f21a1bb8) | [Defaults] Changed to Shadow Defaults and SSGI |
| 2026-07-23 | [`8627dee606`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/8627dee6065ec95f6525b995f139d7cc7a81f5d7) | [PhysX] Opt-In Fixed Timestep implementation |
| 2026-07-23 | [`1a79815259`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/1a79815259e0012ee4c3ef054106aa4297f28839) | [Rendering][Shading Models] Removed unnecesary branch for Toon Shading Model |
| 2026-07-23 | [`d1a07d2e6e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/d1a07d2e6ef07f6f34c7f197b6c08214e13cb469) | Merge branch 'ueVite26-June-Major-Release' of https://github.com/ViteStudio-Tech/ueVite-Internal into ueVite26-June-Major-Release |
| 2026-07-23 | [`620795f3db`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/620795f3db323eecf789d897a587cfe64d5b8bfb) | [Plugin] Implementation of IMGUI with Benchmark Tool |
| 2026-07-23 | [`a79ca7e1c3`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/a79ca7e1c36b4f9830f6fd3efa7f172adb2783cd) | [Toolchain] Updated VS2026 code entries |
| 2026-07-23 | [`614806f6f1`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/614806f6f156ce8fc4516a68402ff8a1ec65e7c5) | [Mobile][ES3_1] Updated guards for TressFX |
| 2026-07-23 | [`afa556586a`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/afa556586a4aa5ab00b4176b506e4eebb771a3fc) | [Plugin] Removal of Houdini (temporarily) |
| 2026-07-23 | [`191aaaa2e7`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/191aaaa2e720f2e474e4e8bf9cdd572ca4a6b906) | [Rendering][Forward][Backport 5.6] MSAA resolve with explicit fmask produces incorrect alpha values |
| 2026-07-23 | [`76d76e6527`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/76d76e6527bb87b09be93165f53fdf5b932ba049) | [Rendering][RT][Backport 5.3] Remove NaN-s at the end of the HWRT reflection shader to prevent propagating errors to large areas of the screen via denoising, antialiasing, bloom, etc. |
| 2026-07-23 | [`58db18ed65`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/58db18ed650bc980af06c4f65a322b45205fae51) | [Rendering][RT][Optimization][Adapted Backport 5.3] Exclude various raygen shaders from RTPSOs unless corresponding features are enabled (RTGI, RTReflections, etc). This significantly improves performance of certain ray tracing passes such as material gather by reducing overall RTPSO VGPR requirements and improving occupancy. |
| 2026-07-23 | [`730130e659`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/730130e6598725f619d2a8e9d128346bb35612be) | [Rendering][RT][Optimization][Adapted Backport 5.0] Use back face culling for material gather rays + Skip Procedural Primitives + PathTracing Utility |
| 2026-07-23 | [`0f34e9f8f6`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/0f34e9f8f6aef5d7ea176bf02bfe16aa8a7361e9) | SSAO/HBAO fix |
| 2026-07-23 | [`f2aa830239`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/f2aa8302395d90e454e95fad6be3867fa2a32cb1) | Revert "[ShaderCompiler][Backport] Backports the STB-based shader preprocessor path from UE5.7" |
| 2026-07-23 | [`fb79e01d54`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/fb79e01d540c1f73a9386a4cd5c32ce72b3cedae) | [BAT Systems] Adds debloats and corrected Targetings pack |
| 2026-07-22 | [`72ad652aa7`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/72ad652aa7e8c3669443ea315ba976400dc9d671) | DLSS-RR: stage nvngx_dlssd.dll and log whether the RR runtime was found |
| 2026-07-22 | [`96b5f32dec`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/96b5f32dec69be59d3db17bfb45dd090f1b5b7b9) | try to test fix crash |
| 2026-07-22 | [`06c270aef7`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/06c270aef718ed69d057a1cd4878022804292471) | DLSS-RR: fix all shadows disappearing when RR is enabled |
| 2026-07-22 | [`ff5cca008c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/ff5cca008c312c69c20e0141d75b8272a7b62d49) | DLSS-RR: take the 310.7 DLL from 0943c9ca instead of the 310.6 one |
| 2026-07-22 | [`d9941e5f4f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/d9941e5f4fbc8653eb3202e0818df45f579c7b6c) | DLSS: ship nvngx_dlssd.dll so Ray Reconstruction can actually initialise |
| 2026-07-22 | [`58000160b5`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/58000160b5cb86a65fe7e2b175d67abfb73c2d8d) | Fix build: finish wiring DLSSRRPreset through both structs and the RDG lambda |
| 2026-07-22 | [`ccdb44d795`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/ccdb44d79546300097a54dea9e2339376cc04cf0) | Fix UHT build break: move the EDLSSPreset comment out of the enum body |
| 2026-07-22 | [`0e1cc539c6`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/0e1cc539c68b0f280bc4e843018fbe138974ee48) | DLSS-RR: adopt the RR preset guard already used on realtime-gi / 4.27-Soliz |
| 2026-07-22 | [`daaa7c36ec`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/daaa7c36ec3a7d0f633ed64ec8ed8c6e25d0a41f) | DLSS: make the DLSS 4 transformer presets selectable, and add an RR preset cvar |
| 2026-07-22 | [`3829cd32b4`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/3829cd32b4de4576ee613a4515484f45b13ab372) | Add r.Upscaler.ScreenPercentageOverride so FSR/DLSS/XeSS can take an arbitrary render resolution |
| 2026-07-22 | [`e326080a21`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e326080a21b3177d0a423aec570aad23ddf7294d) | NGX: mark which preset annotations are ours, and record the CNN evidence + its limits |
| 2026-07-22 | [`5225b0e8e6`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/5225b0e8e68e6229e147c881d1a2e801e6fa5256) | NGX: name the DLSS 4.5 (310.7) render presets these 3.7-level headers were missing |
| 2026-07-22 | [`f174910d50`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/f174910d5017942865ede54c4a15d406a4234f42) | FSR4: restore the Native AA (1.0x) quality mode the port clamped away |
| 2026-07-22 | [`102dfbd5ba`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/102dfbd5ba0fe9fb3e8d89aae47fe667495b5163) | stat fps: align with stat unit's value column |
| 2026-07-22 | [`41261fee6e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/41261fee6eb5dfa1a1b3a1d061cd7ecd2840030f) | stat unit: report the MEASURED render resolution (fixes DPI scaling + upscalers) |
| 2026-07-22 | [`aaa21fce68`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/aaa21fce68ad52db83d9126b19eb15da50541974) | fix(engine): stat unit — nudge overlay block right ~6 chars for alignment |
| 2026-07-22 | [`efa62fe1f3`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/efa62fe1f37b4c61a402a91ae63e91a8bc33be4d) | feat(engine): stat unit — add VRam/RenderRes rows + always-on Mem, backported from UE5.8 |
| 2026-07-22 | [`17c25f9379`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/17c25f9379e3e61d68d8fae4a6af6d21542b028a) | DLSS: bump plugin metadata to 8.7.0-NGX310.7.0 (align with UE5.8 naming) |
| 2026-07-22 | [`75345cea30`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/75345cea3077948d2836ac282f87d3c9cc5e1cf1) | FSR4 FG: guard against odd backbuffer dimensions (fall back to native swapchain) |
| 2026-07-22 | [`8aed65c7cd`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/8aed65c7cd8a4e6f70b9f438f15a78711e3092bf) | XeFG: enable frame-gen on UE4.27 via MIN path (0x1) |
| 2026-07-22 | [`71d3a833c6`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/71d3a833c6068f46325f81663e8d4af90eafc7e1) | FSR4: classify provider by major version (fix FSR4 vs FSR3.1 detection) |
| 2026-07-22 | [`869eadb2f5`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/869eadb2f53678ed8dbb9317a976f5602bcf4940) | FSR4: log + expose active upscaler provider (FSR4 ML vs FSR3.1 fallback) |
| 2026-07-22 | [`05a07ccf61`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/05a07ccf613e85ff23c797b7865d8fa98be712b5) | FSR4 FG: feed converted FSR-convention MVs, not raw GBuffer velocity |
| 2026-07-22 | [`0f7900563d`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/0f7900563d0073429dfd3984e06cc1a874023af7) | FSR4 FG: force velocity for ANY frame-gen vendor, not just FSR-FG |
| 2026-07-22 | [`8c227f1a05`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/8c227f1a054d65c2c0e4183b0411233c85896c64) | FSR4 FG: fix ghosting by forcing full velocity output when FG is selected |
| 2026-07-22 | [`a41836b273`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/a41836b27312460a740d5a0b49cb58f9cbcee990) | FSR4/DLSS: upscaler-agnostic FSR frame-gen + fix XeSS switch crash |
| 2026-07-22 | [`d003781695`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/d003781695ba541bcbc86ea962398d4dab13608e) | update xess document |
| 2026-07-22 | [`2badbcda91`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/2badbcda9163cf7058fa4403f6391bee96648db9) | DLSS: update nvngx_dlss.dll (Super Resolution) 3.7.0 -&gt; 310.7.0 (DLSS 4) |
| 2026-07-22 | [`7c3b3165a0`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7c3b3165a0702854836739e6f4631264c1ea4a24) | FSR4: fix runtime upscaler + frame-gen vendor switching |
| 2026-07-22 | [`84254c9173`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/84254c91730a921fc6cc583cff43c392697657d9) | fix missing dll when package |
| 2026-07-22 | [`ee6ecf58d2`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/ee6ecf58d2653c7d1d75811401c6bf067de74809) | add dll xess |
| 2026-07-22 | [`04eafa10df`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/04eafa10dfb25eec5bd76b620facd8487c74ca07) | Engine: add LitReactive shading model + WPO-static velocity for FSR reactive mask |
| 2026-07-22 | [`2cb0bcdcee`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/2cb0bcdcee3412fee49a842147fe4b2050bf5619) | feat(streamline): expose DLSS4 MFG multipliers + adaptive in DLSS-G enum |
| 2026-07-22 | [`dce9759bd9`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/dce9759bd9436e2129737a9877b80458480cba21) | FSR4: add Frame Generation Settings to the project settings page |
| 2026-07-22 | [`7fd2ed8315`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7fd2ed83154722b24f5e295fd783001d6d18e069) | FSR4 FG: present-time swapchain-driven frame generation (FG-M4/M5) |
| 2026-07-22 | [`79b522345c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/79b522345c95b7b886831fe1ce6b41b3c7e4f93a) | add dll file |
| 2026-07-22 | [`949884c2f4`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/949884c2f4e54b915260d0f7e74f5595f6c8a251) | FSR-FG M3b: hook frame generation into the upscaler pass |
| 2026-07-22 | [`0a58e91fac`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/0a58e91fac0c80e43f0f6144d47a822205f0a15f) | FSR-FG M3 (core): FrameGeneration context + per-frame dispatch |
| 2026-07-22 | [`7166559506`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/716655950660ee254bb9fd9e4cec2edd3fcf95e3) | FSR-FG M2: build the real ffx frame-generation swapchain |
| 2026-07-22 | [`716c15776f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/716c15776fec3ad94212de58566db28e226c7bd0) | FSR-FG M0: scaffold swapchain provider + multi-vendor arbiter |
| 2026-07-22 | [`1588e55a6b`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/1588e55a6b22410b86b282abcbcb3776e2ebdddb) | DLSS4: upgrade Streamline 2.7.32 -&gt; 2.12.0 (latest) |
| 2026-07-22 | [`1a3a201ca0`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/1a3a201ca0a18b823b4c2c71b34bfe33567b5a65) | FSR4: upgrade FidelityFX SDK 4.0.3 -&gt; 4.1.1 (v2.3.0) |
| 2026-07-22 | [`ce76472393`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/ce764723937268254437e9594590cd3f0b3d4a15) | FSR4: remove temporary [FSR4-DIAG] logging |
| 2026-07-22 | [`1d54ce9b2e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/1d54ce9b2e52202d4eb618281a15641b8599d859) | FSR4: add temporary [FSR4-DIAG] logging to BeginRenderViewFamily |
| 2026-07-22 | [`c27d460ce3`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/c27d460ce35e5094fe7c143749d83bd2a554e86b) | FSR4: fix startup crash - drop dead ffx-fsr4-api/shaders mapping |
| 2026-07-22 | [`62fdcd870a`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/62fdcd870a64728bc708b4a445546193dc5ead40) | FSR4: fix C2061 - include FSR4TemporalUpscalingD3D12.h |
| 2026-07-22 | [`db8e6d020b`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/db8e6d020b3d7f0ab2dd50252873624d8a313483) | FSR4: disable FSR2 stack while testing FSR4 |
| 2026-07-22 | [`c262fe6f95`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/c262fe6f9584ba7c4a3ef42d2a3f938ca5aaa8d0) | FSR4: port upscaler backend to ffx-api (M3/M4) |
| 2026-07-22 | [`5d3645d226`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/5d3645d2268bd8a48be4d5c70294a2a1c4518b13) | FSR4: scaffold plugin + ffx-api loader (M0-M2) |
| 2026-07-22 | [`414edfe8ec`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/414edfe8ec504ab068f29868069b4eb133da7309) | fix build error |
| 2026-07-22 | [`6f96c760ea`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/6f96c760eaa405decba464b9ff847c6860037f7a) | try to update DLSS4 |
| 2026-07-22 | [`18558cb7fb`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/18558cb7fbdda0bbfa3d0e2f1eabb9c612ff149f) | SSAO/HBAO fix |
| 2026-07-22 | [`78819be982`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/78819be98205a69f98b7be50b74b4803553893bc) | [Toolchain] STD Infinity usage were needed 2 |
| 2026-07-22 | [`9e4fdb9e75`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/9e4fdb9e75c11d371ecf085fb137a02356cd2c9b) | [Toolchain] STD Infinity usage were needed |
| 2026-07-22 | [`077ff8254c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/077ff8254c71431e997e0407662502f23deddc99) | [Mobile][Fix] Updated TressFX checks |
| 2026-07-22 | [`b4eb1f69c1`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/b4eb1f69c1106fdf29efc160777d67c7d8facb5e) | Stage HBAO+ DLLs into packaged builds |
| 2026-07-22 | [`0465921824`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/0465921824ba07d8df891d2aea461d73180bab27) | add dll for HBAO+ |
| 2026-07-22 | [`328b8d56a0`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/328b8d56a092ef3a1bc542e961a960f829ea49fb) | HBAO+ D3D12: revert unnecessary hardening from 056ace8 |
| 2026-07-22 | [`461772cba0`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/461772cba0c52f0fb598edf6793a6df074f8ae79) | HBAO+ D3D12: fix 0xC06D007E crash — pre-load the D3D11 SSAO DLL too |
| 2026-07-22 | [`73f7904f21`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/73f7904f2197c59751a3e321e8c857c850cd67cb) | HBAO+ D3D12: harden against fatal paths (graceful init + null-guards) |
| 2026-07-22 | [`c539d4fc7c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/c539d4fc7c020dc9cb30a161cb838fb9f1847184) | HBAO+: add D3D12 back-end (GFSDK_SSAO D3D12, dedicated descriptor heaps) |
| 2026-07-22 | [`52176f21a5`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/52176f21a56e9877b65ba418cbc0f42e8c69833e) | HBAO+: match proven RDG SkipRenderPass idiom (FRHICommandListImmediate&amp; lambda) |
| 2026-07-22 | [`fe474ee6e1`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/fe474ee6e1fe164e4d5c1b69c1aeb56a24657c35) | HBAO+: backport NVIDIA GFSDK_SSAO to 4.27 (DX11-only quick win) |
| 2026-07-22 | [`b31a0a9783`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/b31a0a97835557366aad62ae8d2d99f3993941f0) | [Toolchain] Upgraded codebase toolchain compability |
| 2026-07-22 | [`bbc1e81b45`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/bbc1e81b4581f79f0594baab5ad799ade9685f19) | Update README Technical specifics and added PhysX Clang upgrade README |
| 2026-07-22 | [`fd591b384b`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/fd591b384ba26e170afd2eb9c4b5a3ea4dabdff6) | gitignore Update |
| 2026-07-22 | [`6d4bca0c43`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/6d4bca0c437809b89756cb86dc4015b5cf692abf) | Updated .gitignore for XeSS libs |
| 2026-07-22 | [`fde83bf197`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/fde83bf1975d0c6fd63c7d6939a7433233f9a6bc) | Updated README.md: Setup instructions, Changelogs and Technical explanations |
| 2026-07-22 | [`e810ad080c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e810ad080c59ef8b1b78abccf0939e692c24401f) | [Defaults] Plugin GI console variable is now enabled by default (DDGI) |
| 2026-07-22 | [`00b9265991`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/00b92659918bdd5342ce53138b68ba7ca2bbb0b7) | Revert "[Rendering] Backport tonemapper (GT, GT7, AgX)" |
| 2026-07-22 | [`8e83628ff3`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/8e83628ff396fad861c28aaa0bea817a51b40867) | [Defaults] DDGI Enabled by default from BaseEngine.ini |
| 2026-07-22 | [`768ca2725b`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/768ca2725b7755febfa1cf5e9cd9c7c6e6a128eb) | [Plugin] AMD AntiLag 2.0.4 Port |
| 2026-07-22 | [`5fcfd28c06`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/5fcfd28c06fe216fb1992e2de73d178a02dc7c34) | [Config] Engine Default Changes: Enabled NRD RELAX Denoiser by default, Deactivated XGE Shader Compilation |
| 2026-07-22 | [`5e897c48a1`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/5e897c48a15c82c5f0fe06eb8368701ef3163767) | [Oodle][Optimization][Backport][5.0] Fix long waits on the game thread when we're waiting on a specific texture to finish synchronously and the taskgraph is full of background tasks |
| 2026-07-22 | [`79b332e3b5`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/79b332e3b55f2c0efeecbd2b3cd48922cf5fef69) | [Oodle][Backport][5.0] Avoid image copy when performing Oodle image compression and image format matches Oodle input format. |
| 2026-07-22 | [`08dc77dd78`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/08dc77dd78273bfe7bf2926fd64aebc64c303c43) | [Oodle][Backport][5.0] TextureFormatOodle: make log verbosity a config option |
| 2026-07-22 | [`363347715d`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/363347715d8463cda14a9645817386d33dde0f8a) | [Oodle][Backport][5.0]rename TextureFormatOodle config group to TextureFormatOodleSettings so existing Saved/ values are ignored |
| 2026-07-22 | [`16fe0f287f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/16fe0f287f9e53bb1a17d2fe251be415973a4bfe) | [Oodle][Backport][5.0] TextureFormatOodle use AnyBackgroundThreadNormalTask priority |
| 2026-07-22 | [`d1fe4ec45e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/d1fe4ec45e46e97c39b5a90cb114b29429ead539) | [Oodle][Backport][5.0]TextureFormatOodle use proper min for last fix |
| 2026-07-22 | [`118a738a0c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/118a738a0c237b646efc66233ef53ecb577b9588) | [Optimization][Streaming][Backport][5.0]Avoid 10ms delay when waiting on streaming if possible |
| 2026-07-22 | [`ed124dc648`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/ed124dc648f0f01b667f87cec6cb6b207709c3dc) | [Oodle][Backport][5.0] TextureFormatOodle use 16 bit input for BC4/5 |
| 2026-07-22 | [`83b2c6b78a`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/83b2c6b78ac17bfab4f4066ef86016fd5173ac73) | [Backport][5.0] UE_CONSTEVAL macro. |
| 2026-07-22 | [`bf765a95f3`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/bf765a95f3ad3b5b96a1c5a7b0c27b11fa049e9b) | [Math] Changed order of declaration: VectorSin |
| 2026-07-22 | [`754d9482f0`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/754d9482f0419c92724c0f13f79c248171fba0a3) | [Optimization][Mobile][Switch 2] Upgraded Neon Math for Faster Calculations |
| 2026-07-22 | [`61b1149ab9`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/61b1149ab926f1b8a4d1efce6b2737b53a3a0962) | [Optimization][Backport][5.1] Fix for slow performance when applying a new material in a large scene.  The function UWorld::PropagateLightingScenarioChange was calling PropagateLightingScenarioChange on each component, and several types of components were in turn individually creating an FComponentRecreateRenderStateContext, which generates an UpdateAllPrimitiveSceneInfos command for the entire scene.  So it's more or less an O(N^2) operation on the number of primitives in the scene. |
| 2026-07-22 | [`151460444d`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/151460444dc10ffbd5f9d29aab39454f2923e1b9) | [Cook][Backport][5.0]Reduce cook time by avoiding costly object iterator when unnecessary |
| 2026-07-22 | [`e1d371f930`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e1d371f930960d4fd1d6786bd7b5f5f3dd0c6104) | [Optimization][Backport][5.1] Swapping FPrimitiveOctreeSemantics::ElementAllocator from TInlineAllocator to FDefaultAllocator. |
| 2026-07-22 | [`c942ab2809`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/c942ab280953e288a8823dca916b1cb593145d8d) | [Backport][5.0] Fix Min/Max alpha blend state settings |
| 2026-07-22 | [`4c346414ae`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/4c346414aec2d1d9b58c71ffed5a1a8c978de73d) | [Backport][5.1] Fix rounding issue with FDateTime::ParseIso8601 |
| 2026-07-22 | [`8a4754deec`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/8a4754deec4e5c9107c7a7f530cfc583cd563a56) | [TaskGraph][Backport][5.1] TaskGraph - Use a local scratch variable for tasks popped in DispatchSubsequents() instead of reusing a referenced one that's passed in. This was causing a crash because the passed in array was being cleared by another thread before we were finished using them. |
| 2026-07-22 | [`a887e5a4db`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/a887e5a4db51256266fd2990b936f32f780eac11) | [Rendering][Backport][5.1] Initialize virtual texture feedback when rendering deferred decals. Without this only one VT can provide feedback. |
| 2026-07-22 | [`abe3645318`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/abe3645318d9d835c1e0d3fd453cfa5ce94e0f66) | [Rendering][Backport][5.0] Fix translucent rendering result not being composited in the scene color when ISR is enabled. |
| 2026-07-22 | [`4b5aef71f5`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/4b5aef71f5f4d49ead956c1652daa4d1a5577d3f) | [Backport][5.0] PostProcessMaterials should always sample velocity through GBuffer SceneVelocity texture. |
| 2026-07-22 | [`c1bf5e23b3`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/c1bf5e23b3406f318883db0bd3950cba65f2f005) | [Backport][5.0] Fixes crash on r.BloomQuality=6 |
| 2026-07-22 | [`fd8cc27b5f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/fd8cc27b5f80606d01cbf56382f1001a68e5b6d5) | [Backport][5.1] Fix for FMaterialRenderProxy::EvaluateUniformExpressions() being called every frame (when in editor) and not caching the results. |
| 2026-07-22 | [`8a9885001c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/8a9885001cafbcf826bb45d79975c301ed9af148) | [Fix][Backport][5.0] Fix for camera stutter when following a physics object when the frame rate is hitching longer than the physics max delta time setting. New flag for Let spring arm which forces it to clam delta time to the same value as the physics system. |
| 2026-07-22 | [`97e8421d2c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/97e8421d2cc23ecb2cab8fbfd75720301e56e86b) | [Rendering][Backport][5.0] Fix missing micro-occlusion on rect. light specular component. |
| 2026-07-22 | [`fffc58a39b`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/fffc58a39b0ff5c594bd28c293f074a9876af607) | [Fix][Backport][5.2] Use IsPlayInEditor() instead of GIsPlayInEditorWorld in FDeferredDecalProxy construction. |
| 2026-07-22 | [`e09bf26666`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e09bf26666b99269b954494daeea0c4cf065f4a3) | [Rendering][Backport][5.2] Fix broken decals in the forward renderer when MSAA is enabled. |
| 2026-07-22 | [`3086e1f7cc`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/3086e1f7cc2fdac676cf06ae3b20bcd79bf65bb3) | [Rendering][5.0]  fixes for velocity rendering with niagara meshes |
| 2026-07-22 | [`7ebcd4428d`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7ebcd4428dade7fd8adcb111d93d9167f51bfe09) | [Memory][Backport][5.0] Malloc Upgrade: Fixed memory corruption in MallocBinned when allocating memory with alignment requirements higher than DEFAULT_BINNED_ALLOCATOR_ALIGNMENT (16 bytes) |
| 2026-07-22 | [`a2967a0e61`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/a2967a0e61d9f943d96db65614d5fcdd93c89984) | [Optimization][Backport][5.0] UE5:  MEMORY:  Adjustment to container allocation policy to save memory on arrays with optional inline elements. |
| 2026-07-22 | [`503a416e53`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/503a416e53f40508e241e1303a2d90e2b25d35ef) | [Optimization][Backport][5.0] Consolidate SoA into AoS in FAnimNode_BlendListBase |
| 2026-07-22 | [`f18b5f4aa6`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/f18b5f4aa6665905e57488148aacb98009ee57f5) | [Rendering][Backport][5.1] PR #9727: FIX: Custom culling query was being provided wrong VisibilityId value (Contributed by MilkyEngineer) |
| 2026-07-22 | [`0c4089779c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/0c4089779cea923e000134d9117b62b583be81f6) | [Backport][Optimization] Micro optimization in AudioMixerSourceManager |
| 2026-07-22 | [`93b5ddc75f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/93b5ddc75f644d076b5f859f42179c74714f888d) | [Backport] MGPU perf:  micro-optimization of multi-GPU debug name initialization |
| 2026-07-22 | [`e059a60b19`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e059a60b190140b7f323cf66f5aa0d42bf29c9a3) | [ShaderCompiler][Backport] Increase default r.ShaderCompiler.DistributedMinBatchSize from 20 to 50 |
| 2026-07-22 | [`a0d0be6574`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/a0d0be6574d13a04f5b5a399c91117b84bc15fce) | [Backport] Lazy initialization of AnimNode_RigidBody - Memory saving optimization. |
| 2026-07-22 | [`e86897b7a0`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e86897b7a0178a8fc53cb0f25564c318aa2d5ff4) | [Plugin] AMD FSR 3.1.4 |
| 2026-07-22 | [`67d5c1251f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/67d5c1251f6b8d7dc94efefab5fdd8d78ba54bd1) | [Backport] #UE Fix crash when passing in an empty list of points to a spline component |
| 2026-07-22 | [`67fc7beba6`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/67fc7beba69427e6ff2b59815be0cb3000710943) | [Engine][Backport] * Forced signature of lambda to return FString by const reference instead of value.. removes ~17 million memory allocations when starting game |
| 2026-07-22 | [`bcad0457a1`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/bcad0457a184421fe1670515f8fc84e21fb4981d) | [Rendering][Backport] Fix bad scoped lock in texture streaming. |
| 2026-07-22 | [`ca2c934a0e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/ca2c934a0e49ceb19cfbbf534867409f1098ddbb) | [Plugin] Added Intel XeSS 3.0.5 |
| 2026-07-22 | [`f4694725d0`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/f4694725d0f2c851675c7c98c1bbfce02d6b4dd5) | [Backport][Rendering]  Fix for assertion on occlusion query batch overrun due to use of outer occlusion query |
| 2026-07-22 | [`7362df0c84`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7362df0c844134c001539c5ec9b71284b88fd146) | [Backport[Console] Batch of Console Upgrades |
| 2026-07-22 | [`62f08151c0`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/62f08151c029191d3831914b85d90cdff14579cf) | [Backport] Console command sorting |
| 2026-07-22 | [`b34fd21a68`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/b34fd21a6893b1df33f8e8535bfc58f71b4ee3d9) | [Rendering][Backport] TAA Stability Improvement: Fixes history drift when using r.TemporalAA.R11G11B10History=1 |

## See also

- [All Release Notes](Release-Notes.md)
- [Engine Overview](Engine-Overview.md)

