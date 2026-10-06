# ueVite25-LTS

<tldr>
<p>
The LTS transition establishes the new ueVite foundation on NvRTX Caustics 4.27 plus updated Epic 4.27-plus tooling and selected Vite backports.
</p>
</tldr>

| Release window | Status | Captured commits | Source branches |
|---|---|---:|---:|
| 1 November–31 December 2025 | LTS | 82 | 1 |

## Highlights

- Moves the active Vite base from NvRTX 5.0 to NvRTX Caustics 4.27 after matched RTXGI tests favored the 4.27 path.
- Restores the PhysX-oriented production foundation and begins cloth, capsule and target cleanup.
- Adds SMAA/filmic filtering and stylized Blinn–Phong and Guilty Gear-style shading work.
- Re-enables Live Coding while keeping corruption-prone reinstancing disabled and updates build/setup guidance.

## Scope and sources

The requested LTS audit window is 1 November through 31 December 2025. The branch snapshot currently ends on 26 November, so the record contains no December-dated commits; the full requested window remains explicit.

| Source | Branch |
|---|---|
| LTS branch | [`ue5Vite-release`](https://github.com/ViteStudio-Tech/ueVite-Internal/tree/ue5Vite-release) |

- [Base transition decision record](https://docs.google.com/document/d/1gA0MGkzeWWzKkgwBDOP5xRPouSKaOIW6xlPZ2q6BXO0/edit)

<note>
<p>
The requested LTS window extends through 31 December 2025, but the current <code>ue5Vite-release</code> branch tip is dated 26 November 2025. The table therefore contains no December-dated commits.
</p>
</note>

## Commit record

### LTS branch

Branch: [`ue5Vite-release`](https://github.com/ViteStudio-Tech/ueVite-Internal/tree/ue5Vite-release)

| Date | Commit | Change |
|---|---|---|
| 2025-11-26 | [`05ed0a7d6f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/05ed0a7d6f9f2d565b072e447eaa9329cb0b005c) | -.md |
| 2025-11-25 | [`458676ef5f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/458676ef5febd6e93551fd7212543146481d9e27) | Merge pull request #88 from deeplightgamedev/ue5vite-toonshading |
| 2025-11-24 | [`f9db75623c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/f9db75623c745541f8a872b1d9a65678e8250211) | Implemented a Guilty Gear style shading model |
| 2025-11-14 | [`6ff73ee342`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/6ff73ee342a7c593b70379a4d5b162f886b1bb59) | Merge pull request #65 from Aman-k346/ue5Vite-release |
| 2025-11-15 | [`0517974da2`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/0517974da2f67113ed95edc674c3eaaa1dc4cb6f) | Camera phake previewer plugin - Allow camera shake enabled by default |
| 2025-11-14 | [`bbc78bc971`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/bbc78bc9712ed23260c953bc49d6e2c50a559739) | Merge branch 'ue5Vite-release' of https://github.com/GapingPixel/UE5-PhysX-Vite into ue5Vite-release |
| 2025-11-14 | [`d96d5d7b01`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/d96d5d7b01b183fef06145e2b154231ab1eebb4f) | Live conding re enabled, Reinstancing is disabled because its always been corruption prone |
| 2025-11-14 | [`1d68db7de8`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/1d68db7de871834e856f180ba6c914e4af4ce5c9) | SMAA 1x + Filmic Filter |
| 2025-11-14 | [`e10edae2c8`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e10edae2c81cb4f8c9446f0f35f25562e1abccac) | BPs no longer get default nodes added /Begin Play Tick Overlap |
| 2025-11-14 | [`495f154b36`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/495f154b36eac403051b6c1c67bba8da03d7e960) | CMC Small cleanup |
| 2025-11-13 | [`c55da0cd57`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/c55da0cd578af03eb5aa1551098b324f8dca649f) | Turned off tick for StaticMesh Actor |
| 2025-11-13 | [`8ab0f56350`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/8ab0f56350c08bec7a15a11873bf4efed6a797b3) | Switch uncommented |
| 2025-11-13 | [`c12c0319fd`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/c12c0319fde6516ce3ecfb297e49455be4a08283) | PhongBlinn SImplification and Specular Color Blend |
| 2025-11-13 | [`9fda43cb6c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/9fda43cb6cc463756a5d22b4e21f33e4564f13f0) | Reflection fix |
| 2025-11-13 | [`be17169750`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/be171697503e3ac9d8474a184690771d53e8fc9e) | Blinn - Phong |
| 2025-11-13 | [`586d47a560`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/586d47a56001f374d18d1e733dc79fcd9f89117b) | Prepare code to be merged into release. Removed Debug, updated for UE5 calls |
| 2025-11-13 | [`33be8abc65`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/33be8abc65071d0b88f05cb9d6c0097ed513bd40) | Merge branch 'ue5Vite-release' into Capsule-Work |
| 2025-11-13 | [`55c6e70433`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/55c6e70433f204b253acfdc85d1f33daf101e2c1) | Update README Removed Target variables as they are not needed anymore.md |
| 2025-11-13 | [`b6c037df8e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/b6c037df8ed16021dd49c1cc64b681d398f0255f) | Revert "Add bUseChaos = false; &amp; bCompilePhysX = true; to all templates' .build.cs files" |
| 2025-11-13 | [`dbdc1a5896`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/dbdc1a5896e684f52a6e3635aec79034a7d308f2) | Merge remote-tracking branch 'origin/ueVite-PhysXCloth' into ue5Vite-release |
| 2025-11-13 | [`06cd40d216`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/06cd40d216a94056f28012a09dae1c6e080f4d36) | Updates to Targets |
| 2025-11-12 | [`6524e64a15`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/6524e64a152e73c12cfd644d595743d7197a862e) | Update README Clang 13.0.1 download link.md |
| 2025-11-12 | [`e2f080f232`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e2f080f232413d3a6abd1e8388ac4847e998b4f7) | PhysX Header Change, Cloth fixes Test 1 |
| 2025-11-12 | [`e96f6a6c83`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e96f6a6c8314d7fe79be8e98814976ada7a00aee) | debug update |
| 2025-11-12 | [`e7bccc5b42`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e7bccc5b424cf7166c71e6cd6192e4c0d028107a) | Clothing sim update |
| 2025-11-12 | [`b6cfa23ef0`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/b6cfa23ef0605b21e786dd65e4739bdc799119a3) | Update to collision conversions |
| 2025-11-11 | [`fd4faabd2d`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/fd4faabd2d79c2b7f60aeb09c2cf583653b9d957) | Merge branch 'ue5Vite-release' of https://github.com/GapingPixel/UE5-PhysX-Vite into ue5Vite-release |
| 2025-11-11 | [`dc35475c49`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/dc35475c490078b2826a9533ae156025f3f8d6ad) | Add bUseChaos = false; &amp; bCompilePhysX = true; to all templates' .build.cs files |
| 2025-11-11 | [`c61dfb0643`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/c61dfb0643d7f9482473da09d057f9ef8e6e9d9e) | Volumetric Cloud Improvement |
| 2025-11-11 | [`b73a9fecfc`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/b73a9fecfcc89a25b9d71c5eca0aadc1d4711d36) | SQ Accelerator first batch |
| 2025-11-11 | [`cab008777f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/cab008777fd0f084ee95c07df13dd8e537925bb8) | Merge branch 'ue5Vite-release' of https://github.com/GapingPixel/UE5-PhysX-Vite into ue5Vite-release |
| 2025-11-11 | [`b3de7265e6`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/b3de7265e64ff20f2b4d984e75d47b7cf9e4150e) | Macro Fix |
| 2025-11-11 | [`79510561f3`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/79510561f30f314f56b1b851b133e1d67943ebf3) | Update backup |
| 2025-11-11 | [`9879ec242e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/9879ec242e59471305e164e01cef5f0ad2e49103) | SMAA fix. |
| 2025-11-11 | [`927d1f63d4`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/927d1f63d48bda61ee26f215cd0899daa97fd10b) | Replaced UE5 CMC by UE4 |
| 2025-11-11 | [`5081f8cb9a`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/5081f8cb9a0996605d8fbc332a7857b8e7ef8232) | SMAA fix. |
| 2025-11-09 | [`c1635f9bdb`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/c1635f9bdb592f5242157516df521b6b4cff4e01) | Enabled live coding by default |
| 2025-11-09 | [`242b8d5c28`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/242b8d5c28636b66a52acf588a8a6c73cc722cca) | Color Space Conversion values Update |
| 2025-11-08 | [`eb58b5469e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/eb58b5469e763f0b95b26aa9824e49fb37737405) | Reapply "Merge branch 'ue5Vite-release' of https://github.com/GapingPixel/UE5-PhysX-Vite into ue5Vite-release" |
| 2025-11-08 | [`337945e577`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/337945e577c29949c4599ea0d20ea22102d37330) | Revert "Merge branch 'ue5Vite-release' of https://github.com/GapingPixel/UE5-PhysX-Vite into ue5Vite-release" |
| 2025-11-08 | [`b8f339993b`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/b8f339993b7e345b7a2ce2a4803f5c5346c51677) | Merge branch 'ue5Vite-release' of https://github.com/GapingPixel/UE5-PhysX-Vite into ue5Vite-release |
| 2025-11-07 | [`d0d1072745`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/d0d1072745b686b762c78d666cc663a45f042d4d) | Doesnt fix default AA as TSR but doesnt hurt. |
| 2025-11-07 | [`3ec0a8d2ca`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/3ec0a8d2ca68095f863d115d85fc3f2ebfec83c9) | Merge branch 'ue5Vite-release' of https://github.com/GapingPixel/UE5-PhysX-Vite into ue5Vite-release |
| 2025-11-07 | [`281017f526`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/281017f526b3ec490729aca763acd23e95e6e7d0) | Update PostProcessTonemap.cpp |
| 2025-11-07 | [`3aca8bf647`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/3aca8bf6476283850483f81fcc4fc6cb680361ee) | Revert "Add Max Shadow Draw Distance &amp; Max Shadow Draw Distance Fade Range settings to lights" |
| 2025-11-07 | [`294d534e7d`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/294d534e7ddd97ff56a334a339f3e277d2048288) | Update README.md |
| 2025-11-07 | [`235109c944`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/235109c944ff27a3d3d698d180c722dc843cb071) | Update README.md |
| 2025-11-07 | [`7e488125ce`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7e488125ce885ceb8a59e5ab5b35ac03ea7896fc) | BaseUtilityUpdate |
| 2025-11-07 | [`f4080307f7`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/f4080307f791646392d88e827692477756f867f9) | Fully removed PhysicsField Component |
| 2025-11-07 | [`812c001ff2`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/812c001ff290da347f824c1f6abee906e5beffeb) | Engine Tick Performance Improvement: Disabled Physics Field Component Tick by Default, same way as 4.27 default |
| 2025-11-06 | [`a136483d7f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/a136483d7f085f025d19e72457028875828f409d) | NET instruction update README.md |
| 2025-11-05 | [`5bc8371e2e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/5bc8371e2e80622deee0700f5c808634d305fdf4) | Add Max Shadow Draw Distance &amp; Max Shadow Draw Distance Fade Range settings to lights |
| 2025-11-05 | [`736b22e463`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/736b22e4633292c764b5cdbe5c2fb825c3e1d1d7) | PhysX Cooker Upgrade |
| 2025-11-05 | [`0002e47c84`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/0002e47c84de14f1358184af5b292e6452f2090c) | Tonemapper default to Epic one |
| 2025-11-05 | [`b2d949f62d`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/b2d949f62d6bbd36ca26ef67b611711769f8cebd) | Merge pull request #38 from KonstantinosLeriou01/SMAA+Tonemapper |
| 2025-11-05 | [`7562ab3df9`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7562ab3df9656f89bec160d3cc2ef39d82ee3862) | Merge pull request #39 from KonstantinosLeriou01/ISM-Performance-increase-AI-Nav |
| 2025-11-05 | [`c3ea85f67e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/c3ea85f67eb064cf3d28780a4d040c324e024b00) | ISM performance increase ai nav |
| 2025-11-05 | [`daad778e6d`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/daad778e6de81527baa80c0a0bd29d7183f83262) | SMAA + Tonemapper tweaks |
| 2025-11-04 | [`6e7e26a343`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/6e7e26a3436b8abf7cdf4ec169fb0a73579b90b2) | Merge pull request #34 from KonstantinosLeriou01/Shader-Compiler-Improvement |
| 2025-11-04 | [`01ae761af6`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/01ae761af615b3d59f8b78b67401ec2206a224e6) | https://github.com/EpicGames/UnrealEngine/commit/3a678f0547fd9d3cc2e375b6b0a2bd5726e062ec |
| 2025-11-04 | [`af376fe608`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/af376fe608028b482ef048e3fdb17960db7556a4) | Merge pull request #30 from KonstantinosLeriou01/MaterialFunctionsUpdate |
| 2025-11-04 | [`86e5690bc9`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/86e5690bc9d77140b5921f7f8fe81e38f00c12b0) | https://github.com/EpicGames/UnrealEngine/commit/c84c968904b1fbeec758297ea72824419d5a83dd |
| 2025-11-04 | [`7de94bc8f2`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7de94bc8f2db7b82ac7d96dfcaf367ab39b711f0) | Fixed AA Console setup, updated defaults |
| 2025-11-03 | [`699f8fb45c`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/699f8fb45cc0103e354f0c8739a7c006ab290289) | Merge pull request #26 from KonstantinosLeriou01/Commit-f574680 |
| 2025-11-03 | [`5b660ad535`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/5b660ad535bc5e1a7c3cef2c45a1fc3a04dcec57) | https://github.com/EpicGames/UnrealEngine/commit/f5746803ec74f99173d588098506ab7d565597f6 |
| 2025-11-02 | [`d321f2b453`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/d321f2b45358b0fb4a989645cc39363023c68bea) | Update README.md |
| 2025-11-02 | [`bd05437664`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/bd0543766440313cf648c0b119f223f680b1553a) | Default Settings Update: RTXGI is now enabled by defualt |
| 2025-11-01 | [`7d81c1b295`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7d81c1b2958280ebc2b5b698808cda7d35cca518) | Disabled Chaos Plugins By Default |
| 2025-11-01 | [`e140b6b1be`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e140b6b1bee0749da7496a2a9f099cc245bc5cb0) | Disabling More Default Plugins / Enabling RTXGI by default |
| 2025-11-01 | [`7edb71d17e`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/7edb71d17ea52988507b4a39b160c52dce4c43f9) | Tweaked  Recent Plugins Default Push |
| 2025-11-01 | [`dcfa69e676`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/dcfa69e676feace17dcebc684eaec4ce66de9177) | Merge pull request #18 from Solessfir/disable-notifications |
| 2025-11-01 | [`bb5706391a`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/bb5706391aeae2877256ec15c707097c7d270c4e) | Merge pull request #23 from Solessfir/default-plugins |
| 2025-11-01 | [`5f43db4542`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/5f43db45423e2a71191aa967cde884ab33836649) | Merge pull request #21 from Solessfir/batch-file |
| 2025-11-01 | [`ac67269ba9`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/ac67269ba9896cfa3aa9a0bde6dc44a8f57641aa) | Merge pull request #19 from Solessfir/gitignore-update |
| 2025-11-01 | [`e0c01fa6a8`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/e0c01fa6a8159fc13d5d95ada1d70acbce5a1171) | Revert added new lines |
| 2025-11-01 | [`39a45a0981`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/39a45a0981829acbb21d2e649a44305f354ef7d9) | Set enabled plugins by default |
| 2025-11-01 | [`38c1ce490f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/38c1ce490fc63dbc6ea819b0354722cea1049c7c) | Set disabled by default |
| 2025-11-01 | [`b2c3d94d9f`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/b2c3d94d9f47d155c225fcbc9c5d61cdaaf2990d) | Bakport GetMsBuildPath.bat from 5.6 |
| 2025-11-01 | [`95a6810c5d`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/95a6810c5dd868cead3f64c9160fcaa2d5b95bb2) | Add bShowLaunchTips and bShowNewPluginsPopup to have an option to disable notifications (default behavior preserved by default) |
| 2025-11-01 | [`2dfa991c82`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/2dfa991c82b2229569a06d501715318d441916e0) | gitignore AutomationToolLauncher folder |
| 2025-11-01 | [`0087ef49ed`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/0087ef49edfa3231f5fca80df12dc5976a40f88e) | Merge branch 'GapingPixel:ue5Vite-release' into disable-notifications |
| 2025-11-01 | [`604c2c6c12`](https://github.com/ViteStudio-Tech/ueVite-Internal/commit/604c2c6c12583a2b84e324e54e92387dd2e16a9b) | Update README.md |

## See also

- [All Release Notes](Release-Notes.md)
- [Engine Overview](Engine-Overview.md)

