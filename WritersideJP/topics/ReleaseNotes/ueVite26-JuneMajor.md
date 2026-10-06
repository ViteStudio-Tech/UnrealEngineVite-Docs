# ueVite26 June Major

<tldr>
<p>
June is the upscaling and animation release: <b>FSR 4</b> with vendor-agnostic frame generation,
<b>DLSS 4</b> with Ray Reconstruction and multi-frame generation, <b>XeSS 3</b> with XeFG, and
<b>HBAO+</b> on D3D12 &mdash; alongside a full set of BlendSpace and blend-profile animation backports,
opt-in <b>fixed-timestep PhysX</b>, the <b>NVIDIA Blast</b> plugin, and DDGI enabled by default.
</p>
<p>
Branch <code>ueVite26-JuneMajor-release</code> &middot; builds on
<a href="ueVite26-MarchMajor.md">ueVite26 March Major</a>.
</p>
</tldr>

| Status | Development window | Builds on | Commits |
|---|---|---|---:|
| Major | 13 March &ndash; 28 July 2026 | [ueVite26 March Major](ueVite26-MarchMajor.md) | 170 |

## Highlights

<deflist>
<def title="Every current upscaler">
AMD FSR 4 (FidelityFX SDK 4.1.1) with ML upscaling and an FSR 3.1 fallback, including the native-AA mode;
NVIDIA DLSS 4 (NGX 310.7) with selectable transformer presets and Ray Reconstruction; Streamline 2.12 with
DLSS multi-frame generation; Intel XeSS 3.0.5 with XeFG; and AMD FSR 3.1.4. See
<a href="Upscalers.md">Upscalers</a>.
</def>
<def title="Vendor-agnostic frame generation">
FSR frame generation is driven from the swapchain and works with any upscaler, not only FSR. Motion
vectors are converted to FSR conventions, and full velocity output is forced whenever any frame generator
is selected, removing ghosting.
</def>
<def title="Animation backports">
BlendSpace smoothing modes (spring-damper, ease in/out, exponential), per-bone smoothing fixes, time-based
blend profiles in montages and blend nodes, pose snapshots, and per-call montage blend-in/out overrides.
</def>
<def title="Physics">
Opt-in fixed-timestep PhysX with render interpolation (<code>VITE_PHYSX_FIXED_TIMESTEP</code>) and the
NVIDIA Blast plugin with the engine-side changes it needs to render correctly. See
<a href="Fixed-Timestep.md">Fixed Timestep</a>.
</def>
</deflist>

## What's new

### Upscaling, frame generation and latency

- **FSR 4:** new plugin on the FidelityFX API; ML upscaling with FSR 3.1 fallback and provider logging;
  native AA (1.0×) mode restored; runtime switching of upscaler and frame-generation vendor.
- **FSR frame generation:** present-time, swapchain-driven, upscaler-agnostic, with project settings and a
  guard for odd back-buffer sizes.
- **DLSS 4:** NGX 310.7 (DLSS 4.5 presets named), selectable transformer presets, Ray Reconstruction with
  its own preset CVar and runtime staging, and DLSS-G multi-frame generation multipliers via Streamline
  2.12.0.
- **XeSS 3.0.5** with **XeFG** frame generation on UE 4.27; **AMD FSR 3.1.4**; **AMD Anti-Lag 2.0.4**.
- `r.Upscaler.ScreenPercentageOverride` lets FSR, DLSS and XeSS take an arbitrary render resolution.
- **Lit Reactive** shading model with static-WPO velocity for the FSR reactive mask.

### Rendering

- **HBAO+** backported to 4.27, with a new D3D12 back end and packaged DLL staging. See
  [Ambient Occlusion](Ambient-Occlusion.md).
- **DDGI enabled by default** through the GI plugin console variable; **NRD ReLAX** denoiser on by default.
- Ray tracing: RT shadow encoding fix, capsule indirect shadows without static lighting, ray-tracing
  instance gathering no longer stalls, raygen shaders excluded from RTPSOs unless their feature is enabled,
  NaNs removed from HWRT reflections, back-face culling for material-gather rays.
- Scene proxies skip redundant transform updates (about 4 ms GPU, 2.2 ms game thread and 4.8 ms render
  thread saved in the upstream "golem" test scene, with shadow-depth time roughly halved).
- TAA: explicit loop unroll (about 0.5 ms on some DXC platforms) and a history-drift fix with
  `r.TemporalAA.R11G11B10History=1`.
- Forward renderer: MSAA fixes for decals, explicit-fmask resolve alpha, and velocity output.
- Updated SSAO optimisation path; GTAO input-order fix; rect-light micro-occlusion; ISR translucency
  compositing; virtual-texture feedback from deferred decals.
- Shadow and SSGI defaults revised.

### Animation

- BlendSpace: smoothing modes, current and target preview positions, filters only allocated when used
  (~2.6 MB peak saved), crash fix for duplicated or retargeted BlendSpaces.
- Blend profiles: time-based profiles, mode selection, use inside montages and blend nodes.
- `UAnimInstance::AddPoseSnapshot` / `GetPoseSnapshot`; montage blend-in/out overrides on play and stop;
  improved Blueprint spring interpolation; lazily initialised rigid-body anim nodes.

### Physics

- Opt-in fixed-timestep PhysX with an accumulator, sub-stepping caps and render interpolation, guarded so
  the regular path pays nothing when disabled.
- NVIDIA Blast plugin with engine-side rendering support and a
  [sample project](https://github.com/ViteStudio-Tech/ueVite-PhysX_Blast-ProjectSample).
- Fixed camera stutter when following a physics object during long frame hitches.

### Core, loading and memory

- Oodle texture-format backports (background priority, 16-bit BC4/BC5 input, no redundant image copies,
  shorter game-thread waits).
- Streaming avoids a 10 ms wait where possible; cook time reduced by skipping unnecessary object
  iteration; a lambda signature change removes ~17 million allocations.
- MallocBinned alignment-corruption fix, leaner container allocation policies, TaskGraph dispatch fix,
  material uniform expressions cached in editor.
- NEON math upgrades for mobile and Switch 2.

### Tools

- **ImGui** plugin with a benchmark tool that runs in Shipping builds.
- `stat unit` backported from UE 5.8: VRAM and render-resolution rows, always-on memory, measured render
  resolution under DPI scaling and upscalers.
- `LocalBuilds` and `RunUAT.bat` for binary (installed) builds; debloat and targeting packs for the setup
  scripts.
- Console command sorting, tooltips and history improvements.

## Upgrade notes

- **DDGI is on by default.** Projects that do not use ray-traced GI should disable
  `r.GlobalIllumination.ExperimentalPlugin` explicitly. See [Dynamic DDGI](DDGI-Dynamic.md).
- **Fixed timestep** requires `VITE_PHYSX_FIXED_TIMESTEP=1` at build time and is still runtime-disabled by
  default; enable it with `p.VitePhysXFixedTimestep.Enabled`.
- **XGE shader compilation** is disabled by default.
- The Houdini plugin is temporarily removed.

<!-- BEGIN GENERATED COMMIT RECORD -->

## Full commit history {id="commit-history"}

Branch: [`ueVite26-JuneMajor-release`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/tree/ueVite26-JuneMajor-release)

### Commits by area

| Area | Commits |
|---|---:|
| Upscaling and anti-aliasing | 52 |
| Rendering | 43 |
| Animation | 18 |
| Toolchain and platforms | 15 |
| Editor and workflow | 11 |
| Ray tracing and GI | 8 |
| Other | 6 |
| Core and performance | 6 |
| Physics | 4 |
| Plugins and media | 3 |
| Hair | 2 |
| Gameplay framework | 2 |

### Public release branch — 170 commits {collapsible="true" default-state="collapsed"}

170 commits (15 merge commits omitted from the table).

| Date | Commit | Author | Change |
|---|---|---|---|
| 2026-07-28 | [`42dbf9a28d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/42dbf9a28dc8a98e7c9de44cd3a5fb98f4a34a8a) | Tuhoiisa | fix(renderer): cache localized IBL CVar |
| 2026-07-28 | [`303d941785`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/303d9417852c196854cff449431230d4e26c79ed) | Tuhoiisa | \[Backport 5.3\] Unconditionally disable velocity output in base pass for Forward Desktop (UE-169988). #rb Robert.Srinivasiah, Jules.Blok \[REVIEW\] \[at\]Jules.Blok, \[at\]Robert.Srinivasiah #jira UE-169988… |
| 2026-07-28 | [`73517832e5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/73517832e51d2d9cf90d2e1c85ed7620389656ac) | Tuhoiisa | \[Backport 5.3\] Fix MSAA being broken in forward (UE-166561). |
| 2026-07-28 | [`961335bc19`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/961335bc1992086e6fb80a80c596c4e973e8e7d4) | RedPixel | \[Rendering\] Updated SSAO Vite Optimization mechanism |
| 2026-07-28 | [`6b02db435a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/6b02db435a9b8468c11725dbe71753b0dc283346) | Tuhoiisa | rt pso debloat |
| 2026-07-25 | [`f72ff015f5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f72ff015f5badbd152694d992be09bb26cef59ee) | RedPixel | \[Plugin\] PhysX Blast + Engine Side Changes for proper support |
| 2026-07-23 | [`8f2cce17b7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8f2cce17b751c56f21c4526be0f944fc5a22350f) | Carlo V. | ueVite26-June Major Release: Update README.md |
| 2026-07-23 | [`9832bc74ed`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/9832bc74ed94609693f49d67c67f2ba3f21a1bb8) | RedPixel | \[Defaults\] Changed to Shadow Defaults and SSGI |
| 2026-07-23 | [`8627dee606`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8627dee6065ec95f6525b995f139d7cc7a81f5d7) | RedPixel | \[PhysX\] Opt-In Fixed Timestep implementation |
| 2026-07-23 | [`1a79815259`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1a79815259e0012ee4c3ef054106aa4297f28839) | RedPixel | \[Rendering\]\[Shading Models\] Removed unnecesary branch for Toon Shading Model |
| 2026-07-23 | [`620795f3db`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/620795f3db323eecf789d897a587cfe64d5b8bfb) | RedPixel | \[Plugin\] Implementation of IMGUI with Benchmark Tool |
| 2026-07-23 | [`a79ca7e1c3`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a79ca7e1c36b4f9830f6fd3efa7f172adb2783cd) | RedPixel | \[Toolchain\] Updated VS2026 code entries |
| 2026-07-23 | [`614806f6f1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/614806f6f156ce8fc4516a68402ff8a1ec65e7c5) | RedPixel | \[Mobile\]\[ES3\_1\] Updated guards for TressFX |
| 2026-07-23 | [`afa556586a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/afa556586a4aa5ab00b4176b506e4eebb771a3fc) | RedPixel | \[Plugin\] Removal of Houdini (temporarily) |
| 2026-07-23 | [`191aaaa2e7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/191aaaa2e720f2e474e4e8bf9cdd572ca4a6b906) | RedPixel | \[Rendering\]\[Forward\]\[Backport 5.6\] MSAA resolve with explicit fmask produces incorrect alpha values |
| 2026-07-23 | [`76d76e6527`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/76d76e6527bb87b09be93165f53fdf5b932ba049) | RedPixel | \[Rendering\]\[RT\]\[Backport 5.3\] Remove NaN-s at the end of the HWRT reflection shader to prevent propagating errors to large areas of the screen via denoising, antialiasing, bloom, etc. |
| 2026-07-23 | [`58db18ed65`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/58db18ed650bc980af06c4f65a322b45205fae51) | RedPixel | \[Rendering\]\[RT\]\[Optimization\]\[Adapted Backport 5.3\] Exclude various raygen shaders from RTPSOs unless corresponding features are enabled (RTGI, RTReflections, etc). This significantly improves perfor… |
| 2026-07-23 | [`730130e659`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/730130e6598725f619d2a8e9d128346bb35612be) | RedPixel | \[Rendering\]\[RT\]\[Optimization\]\[Adapted Backport 5.0\] Use back face culling for material gather rays + Skip Procedural Primitives + PathTracing Utility |
| 2026-07-23 | [`0f34e9f8f6`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0f34e9f8f6aef5d7ea176bf02bfe16aa8a7361e9) | Tuhoiisa | SSAO/HBAO fix |
| 2026-07-23 | [`f2aa830239`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f2aa8302395d90e454e95fad6be3867fa2a32cb1) | RedPixel | Revert "\[ShaderCompiler\]\[Backport\] Backports the STB-based shader preprocessor path from UE5.7" |
| 2026-07-23 | [`fb79e01d54`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fb79e01d540c1f73a9386a4cd5c32ce72b3cedae) | Tuhoiisa | \[BAT Systems\] Adds debloats and corrected Targetings pack |
| 2026-07-22 | [`72ad652aa7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/72ad652aa7e8c3669443ea315ba976400dc9d671) | Tung Nguyen | DLSS-RR: stage nvngx\_dlssd.dll and log whether the RR runtime was found |
| 2026-07-22 | [`96b5f32dec`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/96b5f32dec69be59d3db17bfb45dd090f1b5b7b9) | Tung Nguyen | try to test fix crash |
| 2026-07-22 | [`06c270aef7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/06c270aef718ed69d057a1cd4878022804292471) | Tung Nguyen | DLSS-RR: fix all shadows disappearing when RR is enabled |
| 2026-07-22 | [`ff5cca008c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ff5cca008c312c69c20e0141d75b8272a7b62d49) | Tung Nguyen | DLSS-RR: take the 310.7 DLL from 0943c9ca instead of the 310.6 one |
| 2026-07-22 | [`d9941e5f4f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d9941e5f4fbc8653eb3202e0818df45f579c7b6c) | Tung Nguyen | DLSS: ship nvngx\_dlssd.dll so Ray Reconstruction can actually initialise |
| 2026-07-22 | [`58000160b5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/58000160b5cb86a65fe7e2b175d67abfb73c2d8d) | Tung Nguyen | Fix build: finish wiring DLSSRRPreset through both structs and the RDG lambda |
| 2026-07-22 | [`ccdb44d795`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ccdb44d79546300097a54dea9e2339376cc04cf0) | Tung Nguyen | Fix UHT build break: move the EDLSSPreset comment out of the enum body |
| 2026-07-22 | [`0e1cc539c6`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0e1cc539c68b0f280bc4e843018fbe138974ee48) | Tung Nguyen | DLSS-RR: adopt the RR preset guard already used on realtime-gi / 4.27-Soliz |
| 2026-07-22 | [`daaa7c36ec`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/daaa7c36ec3a7d0f633ed64ec8ed8c6e25d0a41f) | Tung Nguyen | DLSS: make the DLSS 4 transformer presets selectable, and add an RR preset cvar |
| 2026-07-22 | [`3829cd32b4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3829cd32b4de4576ee613a4515484f45b13ab372) | Tung Nguyen | Add r.Upscaler.ScreenPercentageOverride so FSR/DLSS/XeSS can take an arbitrary render resolution |
| 2026-07-22 | [`e326080a21`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e326080a21b3177d0a423aec570aad23ddf7294d) | Tung Nguyen | NGX: mark which preset annotations are ours, and record the CNN evidence + its limits |
| 2026-07-22 | [`5225b0e8e6`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/5225b0e8e68e6229e147c881d1a2e801e6fa5256) | Tung Nguyen | NGX: name the DLSS 4.5 (310.7) render presets these 3.7-level headers were missing |
| 2026-07-22 | [`f174910d50`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f174910d5017942865ede54c4a15d406a4234f42) | Tung Nguyen | FSR4: restore the Native AA (1.0x) quality mode the port clamped away |
| 2026-07-22 | [`102dfbd5ba`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/102dfbd5ba0fe9fb3e8d89aae47fe667495b5163) | TungNguyen | stat fps: align with stat unit's value column |
| 2026-07-22 | [`41261fee6e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/41261fee6eb5dfa1a1b3a1d061cd7ecd2840030f) | TungNguyen | stat unit: report the MEASURED render resolution (fixes DPI scaling + upscalers) |
| 2026-07-22 | [`aaa21fce68`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/aaa21fce68ad52db83d9126b19eb15da50541974) | TungNguyen | fix(engine): stat unit — nudge overlay block right ~6 chars for alignment |
| 2026-07-22 | [`efa62fe1f3`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/efa62fe1f37b4c61a402a91ae63e91a8bc33be4d) | TungNguyen | feat(engine): stat unit — add VRam/RenderRes rows + always-on Mem, backported from UE5.8 |
| 2026-07-22 | [`17c25f9379`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/17c25f9379e3e61d68d8fae4a6af6d21542b028a) | Tung Nguyen | DLSS: bump plugin metadata to 8.7.0-NGX310.7.0 (align with UE5.8 naming) |
| 2026-07-22 | [`75345cea30`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/75345cea3077948d2836ac282f87d3c9cc5e1cf1) | Tung Nguyen | FSR4 FG: guard against odd backbuffer dimensions (fall back to native swapchain) |
| 2026-07-22 | [`8aed65c7cd`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8aed65c7cd8a4e6f70b9f438f15a78711e3092bf) | Tung Nguyen | XeFG: enable frame-gen on UE4.27 via MIN path (0x1) |
| 2026-07-22 | [`71d3a833c6`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/71d3a833c6068f46325f81663e8d4af90eafc7e1) | TungNguyen | FSR4: classify provider by major version (fix FSR4 vs FSR3.1 detection) |
| 2026-07-22 | [`869eadb2f5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/869eadb2f53678ed8dbb9317a976f5602bcf4940) | TungNguyen | FSR4: log + expose active upscaler provider (FSR4 ML vs FSR3.1 fallback) |
| 2026-07-22 | [`05a07ccf61`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/05a07ccf613e85ff23c797b7865d8fa98be712b5) | TungNguyen | FSR4 FG: feed converted FSR-convention MVs, not raw GBuffer velocity |
| 2026-07-22 | [`0f7900563d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0f7900563d0073429dfd3984e06cc1a874023af7) | Tung Nguyen | FSR4 FG: force velocity for ANY frame-gen vendor, not just FSR-FG |
| 2026-07-22 | [`8c227f1a05`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8c227f1a054d65c2c0e4183b0411233c85896c64) | Tung Nguyen | FSR4 FG: fix ghosting by forcing full velocity output when FG is selected |
| 2026-07-22 | [`a41836b273`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a41836b27312460a740d5a0b49cb58f9cbcee990) | Tung Nguyen | FSR4/DLSS: upscaler-agnostic FSR frame-gen + fix XeSS switch crash |
| 2026-07-22 | [`d003781695`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d003781695ba541bcbc86ea962398d4dab13608e) | Tung Nguyen | update xess document |
| 2026-07-22 | [`2badbcda91`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2badbcda9163cf7058fa4403f6391bee96648db9) | Tung Nguyen | DLSS: update nvngx\_dlss.dll (Super Resolution) 3.7.0 -&gt; 310.7.0 (DLSS 4) |
| 2026-07-22 | [`7c3b3165a0`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7c3b3165a0702854836739e6f4631264c1ea4a24) | Tung Nguyen | FSR4: fix runtime upscaler + frame-gen vendor switching |
| 2026-07-22 | [`84254c9173`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/84254c91730a921fc6cc583cff43c392697657d9) | Tung Nguyen | fix missing dll when package |
| 2026-07-22 | [`ee6ecf58d2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ee6ecf58d2653c7d1d75811401c6bf067de74809) | Tung Nguyen | add dll xess |
| 2026-07-22 | [`04eafa10df`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/04eafa10dfb25eec5bd76b620facd8487c74ca07) | Tung Nguyen | Engine: add LitReactive shading model + WPO-static velocity for FSR reactive mask |
| 2026-07-22 | [`2cb0bcdcee`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2cb0bcdcee3412fee49a842147fe4b2050bf5619) | Tung Nguyen | feat(streamline): expose DLSS4 MFG multipliers + adaptive in DLSS-G enum |
| 2026-07-22 | [`dce9759bd9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/dce9759bd9436e2129737a9877b80458480cba21) | Tung Nguyen | FSR4: add Frame Generation Settings to the project settings page |
| 2026-07-22 | [`7fd2ed8315`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7fd2ed83154722b24f5e295fd783001d6d18e069) | Tung Nguyen | FSR4 FG: present-time swapchain-driven frame generation (FG-M4/M5) |
| 2026-07-22 | [`79b522345c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/79b522345c95b7b886831fe1ce6b41b3c7e4f93a) | Tung Nguyen | add dll file |
| 2026-07-22 | [`949884c2f4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/949884c2f4e54b915260d0f7e74f5595f6c8a251) | Tung Nguyen | FSR-FG M3b: hook frame generation into the upscaler pass |
| 2026-07-22 | [`0a58e91fac`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0a58e91fac0c80e43f0f6144d47a822205f0a15f) | Tung Nguyen | FSR-FG M3 (core): FrameGeneration context + per-frame dispatch |
| 2026-07-22 | [`7166559506`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/716655950660ee254bb9fd9e4cec2edd3fcf95e3) | Tung Nguyen | FSR-FG M2: build the real ffx frame-generation swapchain |
| 2026-07-22 | [`716c15776f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/716c15776fec3ad94212de58566db28e226c7bd0) | Tung Nguyen | FSR-FG M0: scaffold swapchain provider + multi-vendor arbiter |
| 2026-07-22 | [`1588e55a6b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1588e55a6b22410b86b282abcbcb3776e2ebdddb) | Tung Nguyen | DLSS4: upgrade Streamline 2.7.32 -&gt; 2.12.0 (latest) |
| 2026-07-22 | [`1a3a201ca0`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1a3a201ca0a18b823b4c2c71b34bfe33567b5a65) | Tung Nguyen | FSR4: upgrade FidelityFX SDK 4.0.3 -&gt; 4.1.1 (v2.3.0) |
| 2026-07-22 | [`ce76472393`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ce764723937268254437e9594590cd3f0b3d4a15) | Tung Nguyen | FSR4: remove temporary \[FSR4-DIAG\] logging |
| 2026-07-22 | [`1d54ce9b2e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1d54ce9b2e52202d4eb618281a15641b8599d859) | Tung Nguyen | FSR4: add temporary \[FSR4-DIAG\] logging to BeginRenderViewFamily |
| 2026-07-22 | [`c27d460ce3`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/c27d460ce35e5094fe7c143749d83bd2a554e86b) | Tung Nguyen | FSR4: fix startup crash - drop dead ffx-fsr4-api/shaders mapping |
| 2026-07-22 | [`62fdcd870a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/62fdcd870a64728bc708b4a445546193dc5ead40) | Tung Nguyen | FSR4: fix C2061 - include FSR4TemporalUpscalingD3D12.h |
| 2026-07-22 | [`db8e6d020b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/db8e6d020b3d7f0ab2dd50252873624d8a313483) | Tung Nguyen | FSR4: disable FSR2 stack while testing FSR4 |
| 2026-07-22 | [`c262fe6f95`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/c262fe6f9584ba7c4a3ef42d2a3f938ca5aaa8d0) | Tung Nguyen | FSR4: port upscaler backend to ffx-api (M3/M4) |
| 2026-07-22 | [`5d3645d226`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/5d3645d2268bd8a48be4d5c70294a2a1c4518b13) | Tung Nguyen | FSR4: scaffold plugin + ffx-api loader (M0-M2) |
| 2026-07-22 | [`414edfe8ec`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/414edfe8ec504ab068f29868069b4eb133da7309) | Tung Nguyen | fix build error |
| 2026-07-22 | [`6f96c760ea`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/6f96c760eaa405decba464b9ff847c6860037f7a) | Tung Nguyen | try to update DLSS4 |
| 2026-07-22 | [`18558cb7fb`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/18558cb7fbdda0bbfa3d0e2f1eabb9c612ff149f) | Tuhoiisa | SSAO/HBAO fix |
| 2026-07-22 | [`78819be982`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/78819be98205a69f98b7be50b74b4803553893bc) | RedPixel | \[Toolchain\] STD Infinity usage were needed 2 |
| 2026-07-22 | [`9e4fdb9e75`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/9e4fdb9e75c11d371ecf085fb137a02356cd2c9b) | RedPixel | \[Toolchain\] STD Infinity usage were needed |
| 2026-07-22 | [`077ff8254c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/077ff8254c71431e997e0407662502f23deddc99) | RedPixel | \[Mobile\]\[Fix\] Updated TressFX checks |
| 2026-07-22 | [`b4eb1f69c1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b4eb1f69c1106fdf29efc160777d67c7d8facb5e) | Tung Nguyen | Stage HBAO+ DLLs into packaged builds |
| 2026-07-22 | [`0465921824`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0465921824ba07d8df891d2aea461d73180bab27) | Tung Nguyen | add dll for HBAO+ |
| 2026-07-22 | [`328b8d56a0`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/328b8d56a092ef3a1bc542e961a960f829ea49fb) | Tung Nguyen | HBAO+ D3D12: revert unnecessary hardening from 056ace8 |
| 2026-07-22 | [`461772cba0`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/461772cba0c52f0fb598edf6793a6df074f8ae79) | Tung Nguyen | HBAO+ D3D12: fix 0xC06D007E crash — pre-load the D3D11 SSAO DLL too |
| 2026-07-22 | [`73f7904f21`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/73f7904f2197c59751a3e321e8c857c850cd67cb) | Tung Nguyen | HBAO+ D3D12: harden against fatal paths (graceful init + null-guards) |
| 2026-07-22 | [`c539d4fc7c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/c539d4fc7c020dc9cb30a161cb838fb9f1847184) | Tung Nguyen | HBAO+: add D3D12 back-end (GFSDK\_SSAO D3D12, dedicated descriptor heaps) |
| 2026-07-22 | [`52176f21a5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/52176f21a56e9877b65ba418cbc0f42e8c69833e) | Tung Nguyen | HBAO+: match proven RDG SkipRenderPass idiom (FRHICommandListImmediate&amp; lambda) |
| 2026-07-22 | [`fe474ee6e1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fe474ee6e1fe164e4d5c1b69c1aeb56a24657c35) | Tung Nguyen | HBAO+: backport NVIDIA GFSDK\_SSAO to 4.27 (DX11-only quick win) |
| 2026-07-22 | [`b31a0a9783`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b31a0a97835557366aad62ae8d2d99f3993941f0) | RedPixel | \[Toolchain\] Upgraded codebase toolchain compability |
| 2026-07-22 | [`bbc1e81b45`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bbc1e81b4581f79f0594baab5ad799ade9685f19) | RedPixel | Update README Technical specifics and added PhysX Clang upgrade README |
| 2026-07-22 | [`fd591b384b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fd591b384ba26e170afd2eb9c4b5a3ea4dabdff6) | RedPixel | gitignore Update |
| 2026-07-22 | [`6d4bca0c43`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/6d4bca0c437809b89756cb86dc4015b5cf692abf) | RedPixel | Updated .gitignore for XeSS libs |
| 2026-07-22 | [`fde83bf197`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fde83bf1975d0c6fd63c7d6939a7433233f9a6bc) | RedPixel | Updated README.md: Setup instructions, Changelogs and Technical explanations |
| 2026-07-22 | [`e810ad080c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e810ad080c59ef8b1b78abccf0939e692c24401f) | RedPixel | \[Defaults\] Plugin GI console variable is now enabled by default (DDGI) |
| 2026-07-22 | [`00b9265991`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/00b92659918bdd5342ce53138b68ba7ca2bbb0b7) | RedPixel | Revert "\[Rendering\] Backport tonemapper (GT, GT7, AgX)" |
| 2026-07-22 | [`8e83628ff3`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8e83628ff396fad861c28aaa0bea817a51b40867) | RedPixel | \[Defaults\] DDGI Enabled by default from BaseEngine.ini |
| 2026-07-22 | [`768ca2725b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/768ca2725b7755febfa1cf5e9cd9c7c6e6a128eb) | RedPixel | \[Plugin\] AMD AntiLag 2.0.4 Port |
| 2026-07-22 | [`5fcfd28c06`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/5fcfd28c06fe216fb1992e2de73d178a02dc7c34) | RedPixel | \[Config\] Engine Default Changes: Enabled NRD RELAX Denoiser by default, Deactivated XGE Shader Compilation |
| 2026-07-22 | [`5e897c48a1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/5e897c48a15c82c5f0fe06eb8368701ef3163767) | RedPixel | \[Oodle\]\[Optimization\]\[Backport\]\[5.0\] Fix long waits on the game thread when we're waiting on a specific texture to finish synchronously and the taskgraph is full of background tasks |
| 2026-07-22 | [`79b332e3b5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/79b332e3b55f2c0efeecbd2b3cd48922cf5fef69) | RedPixel | \[Oodle\]\[Backport\]\[5.0\] Avoid image copy when performing Oodle image compression and image format matches Oodle input format. |
| 2026-07-22 | [`08dc77dd78`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/08dc77dd78273bfe7bf2926fd64aebc64c303c43) | RedPixel | \[Oodle\]\[Backport\]\[5.0\] TextureFormatOodle: make log verbosity a config option |
| 2026-07-22 | [`363347715d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/363347715d8463cda14a9645817386d33dde0f8a) | RedPixel | \[Oodle\]\[Backport\]\[5.0\]rename TextureFormatOodle config group to TextureFormatOodleSettings so existing Saved/ values are ignored |
| 2026-07-22 | [`16fe0f287f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/16fe0f287f9e53bb1a17d2fe251be415973a4bfe) | RedPixel | \[Oodle\]\[Backport\]\[5.0\] TextureFormatOodle use AnyBackgroundThreadNormalTask priority |
| 2026-07-22 | [`d1fe4ec45e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d1fe4ec45e46e97c39b5a90cb114b29429ead539) | RedPixel | \[Oodle\]\[Backport\]\[5.0\]TextureFormatOodle use proper min for last fix |
| 2026-07-22 | [`118a738a0c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/118a738a0c237b646efc66233ef53ecb577b9588) | RedPixel | \[Optimization\]\[Streaming\]\[Backport\]\[5.0\]Avoid 10ms delay when waiting on streaming if possible |
| 2026-07-22 | [`ed124dc648`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ed124dc648f0f01b667f87cec6cb6b207709c3dc) | RedPixel | \[Oodle\]\[Backport\]\[5.0\] TextureFormatOodle use 16 bit input for BC4/5 |
| 2026-07-22 | [`83b2c6b78a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/83b2c6b78ac17bfab4f4066ef86016fd5173ac73) | RedPixel | \[Backport\]\[5.0\] UE\_CONSTEVAL macro. |
| 2026-07-22 | [`bf765a95f3`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bf765a95f3ad3b5b96a1c5a7b0c27b11fa049e9b) | RedPixel | \[Math\] Changed order of declaration: VectorSin |
| 2026-07-22 | [`754d9482f0`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/754d9482f0419c92724c0f13f79c248171fba0a3) | RedPixel | \[Optimization\]\[Mobile\]\[Switch 2\] Upgraded Neon Math for Faster Calculations |
| 2026-07-22 | [`61b1149ab9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/61b1149ab926f1b8a4d1efce6b2737b53a3a0962) | RedPixel | \[Optimization\]\[Backport\]\[5.1\] Fix for slow performance when applying a new material in a large scene. The function UWorld::PropagateLightingScenarioChange was calling PropagateLightingScenarioChange… |
| 2026-07-22 | [`151460444d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/151460444dc10ffbd5f9d29aab39454f2923e1b9) | RedPixel | \[Cook\]\[Backport\]\[5.0\]Reduce cook time by avoiding costly object iterator when unnecessary |
| 2026-07-22 | [`e1d371f930`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e1d371f930960d4fd1d6786bd7b5f5f3dd0c6104) | RedPixel | \[Optimization\]\[Backport\]\[5.1\] Swapping FPrimitiveOctreeSemantics::ElementAllocator from TInlineAllocator to FDefaultAllocator. |
| 2026-07-22 | [`c942ab2809`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/c942ab280953e288a8823dca916b1cb593145d8d) | RedPixel | \[Backport\]\[5.0\] Fix Min/Max alpha blend state settings |
| 2026-07-22 | [`4c346414ae`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/4c346414aec2d1d9b58c71ffed5a1a8c978de73d) | RedPixel | \[Backport\]\[5.1\] Fix rounding issue with FDateTime::ParseIso8601 |
| 2026-07-22 | [`8a4754deec`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8a4754deec4e5c9107c7a7f530cfc583cd563a56) | RedPixel | \[TaskGraph\]\[Backport\]\[5.1\] TaskGraph - Use a local scratch variable for tasks popped in DispatchSubsequents() instead of reusing a referenced one that's passed in. This was causing a crash because th… |
| 2026-07-22 | [`a887e5a4db`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a887e5a4db51256266fd2990b936f32f780eac11) | RedPixel | \[Rendering\]\[Backport\]\[5.1\] Initialize virtual texture feedback when rendering deferred decals. Without this only one VT can provide feedback. |
| 2026-07-22 | [`abe3645318`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/abe3645318d9d835c1e0d3fd453cfa5ce94e0f66) | RedPixel | \[Rendering\]\[Backport\]\[5.0\] Fix translucent rendering result not being composited in the scene color when ISR is enabled. |
| 2026-07-22 | [`4b5aef71f5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/4b5aef71f5f4d49ead956c1652daa4d1a5577d3f) | RedPixel | \[Backport\]\[5.0\] PostProcessMaterials should always sample velocity through GBuffer SceneVelocity texture. |
| 2026-07-22 | [`c1bf5e23b3`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/c1bf5e23b3406f318883db0bd3950cba65f2f005) | RedPixel | \[Backport\]\[5.0\] Fixes crash on r.BloomQuality=6 |
| 2026-07-22 | [`fd8cc27b5f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fd8cc27b5f80606d01cbf56382f1001a68e5b6d5) | RedPixel | \[Backport\]\[5.1\] Fix for FMaterialRenderProxy::EvaluateUniformExpressions() being called every frame (when in editor) and not caching the results. |
| 2026-07-22 | [`8a9885001c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8a9885001cafbcf826bb45d79975c301ed9af148) | RedPixel | \[Fix\]\[Backport\]\[5.0\] Fix for camera stutter when following a physics object when the frame rate is hitching longer than the physics max delta time setting. New flag for Let spring arm which forces it… |
| 2026-07-22 | [`97e8421d2c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/97e8421d2cc23ecb2cab8fbfd75720301e56e86b) | RedPixel | \[Rendering\]\[Backport\]\[5.0\] Fix missing micro-occlusion on rect. light specular component. |
| 2026-07-22 | [`fffc58a39b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fffc58a39b0ff5c594bd28c293f074a9876af607) | RedPixel | \[Fix\]\[Backport\]\[5.2\] Use IsPlayInEditor() instead of GIsPlayInEditorWorld in FDeferredDecalProxy construction. |
| 2026-07-22 | [`e09bf26666`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e09bf26666b99269b954494daeea0c4cf065f4a3) | RedPixel | \[Rendering\]\[Backport\]\[5.2\] Fix broken decals in the forward renderer when MSAA is enabled. |
| 2026-07-22 | [`3086e1f7cc`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3086e1f7cc2fdac676cf06ae3b20bcd79bf65bb3) | RedPixel | \[Rendering\]\[5.0\] fixes for velocity rendering with niagara meshes |
| 2026-07-22 | [`7ebcd4428d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7ebcd4428dade7fd8adcb111d93d9167f51bfe09) | RedPixel | \[Memory\]\[Backport\]\[5.0\] Malloc Upgrade: Fixed memory corruption in MallocBinned when allocating memory with alignment requirements higher than DEFAULT\_BINNED\_ALLOCATOR\_ALIGNMENT (16 bytes) |
| 2026-07-22 | [`a2967a0e61`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a2967a0e61d9f943d96db65614d5fcdd93c89984) | RedPixel | \[Optimization\]\[Backport\]\[5.0\] UE5: MEMORY: Adjustment to container allocation policy to save memory on arrays with optional inline elements. |
| 2026-07-22 | [`503a416e53`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/503a416e53f40508e241e1303a2d90e2b25d35ef) | RedPixel | \[Optimization\]\[Backport\]\[5.0\] Consolidate SoA into AoS in FAnimNode\_BlendListBase |
| 2026-07-22 | [`f18b5f4aa6`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f18b5f4aa6665905e57488148aacb98009ee57f5) | RedPixel | \[Rendering\]\[Backport\]\[5.1\] PR #9727: FIX: Custom culling query was being provided wrong VisibilityId value (Contributed by MilkyEngineer) |
| 2026-07-22 | [`0c4089779c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0c4089779cea923e000134d9117b62b583be81f6) | RedPixel | \[Backport\]\[Optimization\] Micro optimization in AudioMixerSourceManager |
| 2026-07-22 | [`93b5ddc75f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/93b5ddc75f644d076b5f859f42179c74714f888d) | RedPixel | \[Backport\] MGPU perf: micro-optimization of multi-GPU debug name initialization |
| 2026-07-22 | [`e059a60b19`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e059a60b190140b7f323cf66f5aa0d42bf29c9a3) | RedPixel | \[ShaderCompiler\]\[Backport\] Increase default r.ShaderCompiler.DistributedMinBatchSize from 20 to 50 |
| 2026-07-22 | [`a0d0be6574`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a0d0be6574d13a04f5b5a399c91117b84bc15fce) | RedPixel | \[Backport\] Lazy initialization of AnimNode\_RigidBody - Memory saving optimization. |
| 2026-07-22 | [`e86897b7a0`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e86897b7a0178a8fc53cb0f25564c318aa2d5ff4) | RedPixel | \[Plugin\] AMD FSR 3.1.4 |
| 2026-07-22 | [`67d5c1251f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/67d5c1251f6b8d7dc94efefab5fdd8d78ba54bd1) | RedPixel | \[Backport\] #UE Fix crash when passing in an empty list of points to a spline component |
| 2026-07-22 | [`67fc7beba6`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/67fc7beba69427e6ff2b59815be0cb3000710943) | RedPixel | \[Engine\]\[Backport\] \* Forced signature of lambda to return FString by const reference instead of value.. removes ~17 million memory allocations when starting game |
| 2026-07-22 | [`bcad0457a1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bcad0457a184421fe1670515f8fc84e21fb4981d) | RedPixel | \[Rendering\]\[Backport\] Fix bad scoped lock in texture streaming. |
| 2026-07-22 | [`ca2c934a0e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ca2c934a0e49ceb19cfbbf534867409f1098ddbb) | RedPixel | \[Plugin\] Added Intel XeSS 3.0.5 |
| 2026-07-22 | [`f4694725d0`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f4694725d0f2c851675c7c98c1bbfce02d6b4dd5) | RedPixel | \[Backport\]\[Rendering\] Fix for assertion on occlusion query batch overrun due to use of outer occlusion query |
| 2026-07-22 | [`7362df0c84`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7362df0c844134c001539c5ec9b71284b88fd146) | RedPixel | \[Backport\[Console\] Batch of Console Upgrades |
| 2026-07-22 | [`62f08151c0`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/62f08151c029191d3831914b85d90cdff14579cf) | RedPixel | \[Backport\] Console command sorting |
| 2026-07-22 | [`b34fd21a68`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b34fd21a6893b1df33f8e8535bfc58f71b4ee3d9) | RedPixel | \[Rendering\]\[Backport\] TAA Stability Improvement: Fixes history drift when using r.TemporalAA.R11G11B10History=1 |
| 2026-06-04 | [`3c524b5bf9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3c524b5bf9646237a7cee631285a3cbcc92295e4) | RedPixel | \[Rendering\]\[Backport\] Fix general RT shadow issue because of an unmatched sqaure for the encoding of the shadow |
| 2026-06-04 | [`fe283b990c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fe283b990c64eea95683525c593cbdad3a7a6118) | RedPixel | \[Rendering\]\[Backport\] Allow capsule indirect shadows in projects that don't support static lighting. |
| 2026-06-04 | [`52982fbb9a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/52982fbb9af09c6c298ca672ba6383918acf24e2) | RedPixel | \[Rendering\]\[Optimization\]\[Backport\] Optimization to remove stalling in FDeferredShadingSceneRenderer::GatherRayTracingWorldInstancesForView() |
| 2026-06-04 | [`96ee43fb96`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/96ee43fb9614c41ec60cd409c1bea5c5236789bd) | RedPixel | \[Optimization\]\[Backport\] Implemented redundant transform skipping for scene proxies, which saves ~4ms of GPU, ~2.17ms GT, and ~4.81ms of RT in the golem scene, and numerous other expensive locations… |
| 2026-06-04 | [`94a7034c9c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/94a7034c9c928b1e44afdd8a54bf378c6f75756b) | RedPixel | \[Rendering\]\[Optimization\]\[Backport\] Explicitly unroll loop in TAA shader to improve platform specific DXC performance. This improves TAA on certain platforms with DXC by roughly 0.5ms. |
| 2026-06-03 | [`bd2211b5e8`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bd2211b5e8c494b36a894204d163f5361a9c2963) | RedPixel | \[Animation\]\[Backport\] Added UAnimInstance::AddPoseSnapshot and GetPoseSnapshot |
| 2026-06-03 | [`eda868b42c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/eda868b42c489f7d1fefccc48c937d885bd62c83) | RedPixel | \[Animation\]\[Backport\] Improve the way the preview position etc are shown and used |
| 2026-06-03 | [`e266f0a1a7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e266f0a1a769da45ee4e5230dfbd33a3fdafeff1) | RedPixel | \[Animation\]\[Backport\] Show the current as well as target preview position in BlendSpaces |
| 2026-06-03 | [`0c939792d9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0c939792d9c969ea134170b5fc2bb92762468e3c) | RedPixel | \[Animation\]\[Backport\] Fix for crash in duplicate/retargeted blendspace from missing samples |
| 2026-06-03 | [`66f7fca1fd`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/66f7fca1fdf2fd88b83cb723fcc176787331b233) | RedPixel | \[Animation\]\[Backport\] Fixed BlendSpace filters being allocated even when they are not in use Saves ~2.6MB peak in synthetic tests |
| 2026-06-03 | [`1e7b07dc46`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1e7b07dc46530b4ad7277237285b2030ab2f4215) | RedPixel | \[Animation\]\[Backport\] Fixes for per-bone smoothing with blendspace graphs |
| 2026-06-03 | [`28d7add77d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/28d7add77d5eb8244c16792f64a8f80d06a53673) | RedPixel | \[Animation\]\[Backport\] Improve Blueprint Spring Interp behaviour |
| 2026-06-03 | [`977cba7649`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/977cba764905e3951408a7d20c7f1d42593bcc0f) | RedPixel | \[Animation\]\[Backport\] Improve BlendSpace Smoothing, adding options like SpringDamper, Ease In/Out and Exponential |
| 2026-06-03 | [`bf9b627493`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bf9b627493fc593979a07cc8dd8d059ea277b791) | RedPixel | \[Animation\]\[Backport\] Remove the sorting of the per bone BlendSpace smoothing overrides in the UI |
| 2026-06-03 | [`8fa2fcfeab`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8fa2fcfeab7df22e3136c6fbe3c80f315bfeacf2) | RedPixel | \[Animation\]\[Backport\] Ease in/out for the target weight interpolation in BlendSpace. |
| 2026-06-03 | [`90153d4240`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/90153d42400803479c4e1cab40d0d6bb4bbda20b) | RedPixel | \[Animation\]\[Backport\] CL 14798723 Part 2 |
| 2026-06-02 | [`51144c4bc9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/51144c4bc95be3c4cc3d6087fc6a31c75a509e43) | RedPixel | \[Animation\]\[Backport\] Move blend profile customization to its own PropertyTypeCustomization. |
| 2026-06-02 | [`e21ae16c1d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e21ae16c1dd21e1b4ac6b8d70edd0ef70712dddb) | RedPixel | \[Animation\]\[Backport\] Add support for blend profiles inside anim montages and blend nodes. |
| 2026-06-02 | [`59259bbc6e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/59259bbc6ef14b4d6498964da19eab66e2a2969d) | RedPixel | \[Animation\]\[Backport\] -Added Blend Profile mode selection to blend profile picker. |
| 2026-06-02 | [`7786d064bd`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7786d064bd2d16c88dc3b4c2a8293a808300c1ef) | RedPixel | \[Animation\]\[Backport\] Improve the Blend Profiles by allowing time based profiles. |
| 2026-06-02 | [`f04400ae9d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f04400ae9d119a48207993acf39f9ed528824deb) | RedPixel | \[Animation\] Adding the option to override BlendIn/BlendOut settings on Montage\_Play/Stop |
| 2026-06-02 | [`c0889790e8`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/c0889790e82cdf63c87ec3c2d3f832192e9476ca) | RedPixel | Add LocalBuilds files + RunUAT.bat (Binaries Build) |
| 2026-05-26 | [`e9558904e6`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e9558904e6ceea0cd0affa4de76e8dc992949c98) | RedPixel | Cleaning Tonemapper UAssets |
| 2026-05-14 | [`d34d309622`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d34d309622ec366e7cdd28094f66bce3e45e9d68) | RedPixel | Gitdeps: Removed Unreal Vainilla Splash |
| 2026-05-14 | [`40f0b0c918`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/40f0b0c9185475c0552de414620f4e0ca7268485) | RedPixel | \[ShaderCompiler\]\[Backport\] Backports the STB-based shader preprocessor path from UE5.7 |
| 2026-04-27 | [`abc0b9b9a1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/abc0b9b9a190372e7f6d25a1416c60986dd13a11) | RedPixel | \[Rendering\] Fix LPV GI not affecting landscape unless landscape is selected in editor |
| 2026-04-27 | [`50d09878e7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/50d09878e7ae7e4b26a0e69c84b00564bf934127) | RedPixel | \[Backport\]\[Shader Compiler\] Fix memory leak of shader code during shader compilation (during cooks, deployments, or editor). |
| 2026-04-14 | [`0ce2248bef`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0ce2248beff32610f6cd40bdbe2256152f841e25) | sellano | switch material graph node |
| 2026-04-10 | [`df37698b61`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/df37698b61554cb182be8e9da8b109c2bf1fa1fe) | RedPixel | \[Rendering\]\[Backport\] Fixed invalid order of GTAO input textures |
| 2026-03-27 | [`85402aff9a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/85402aff9a1be29e7e080f441d2cc54d5deb7e5f) | cryptosebek | \[Rendering\] Backport tonemapper (GT, GT7, AgX) |
| 2026-03-13 | [`9376133806`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/9376133806b0db68d59cf9af93f026605770c70b) | ThePhxRises | Added an animation editor option to force opening animation assets inside a new tab. |
| 2026-03-13 | [`d37c0148da`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d37c0148dacc9f05ff73b9d122aeae23aa6862f6) | ThePhxRises | Added console command tooltips when displaying the history |

<!-- END GENERATED COMMIT RECORD -->

## See also

- [All release notes](Release-Notes.md)
- [ueVite26 July Major](ueVite26-JulyMajor.md)
- [ueVite26 March Major](ueVite26-MarchMajor.md)
- [Upscalers](Upscalers.md)
