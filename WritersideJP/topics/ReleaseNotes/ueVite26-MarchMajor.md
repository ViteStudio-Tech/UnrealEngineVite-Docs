# ueVite26 March Major

<tldr>
<p>
2026 年最初のメジャーリリースです。March では <b>トゥーンシェーディングモデル</b>、品質レベルを選べる
<b>コンピュートベースの SMAA</b>、高速化したレイトレーシング反射、<b>ローカライズド IBL</b>、ネイティブ PhysX
アクターのための <b>PhysX Instanced Subsystem</b>、Android NDK 29 への対応を追加し、非推奨の XR プラットフォームのコードをおよそ 3 GB 削除しました。
</p>
<p>
ブランチ <code>ueVite26-MarchMajor-release</code> &middot; リリース日: 2026 年 3 月 12 日 &middot; ベース:
<a href="ueVite25-LTS.md">ueVite25 LTS</a>
</p>
</tldr>

| 状態 | 開発期間 | ベース | コミット数 |
|---|---|---|---:|
| メジャー | 2025 年 12 月 12 日〜2026 年 3 月 12 日（2026 年 8 月 21 日までメンテナンス） | [ueVite25 LTS](ueVite25-LTS.md) | 79 |

## ハイライト

<deflist>
<def title="トゥーンシェーディングモデル">
Guilty Gear に着想を得たセルシェーディングのモデルで、影色、シャドウバイアス、ソフトネス、スペキュラーを明示的に制御できます。<a href="Shading-Models.md">シェーディングモデル</a> を参照してください。
</def>
<def title="コンピュート SMAA と FXAA の改良">
SMAA を品質レベルを選べるコンピュートパスとして作り直し、性能も向上しました。FXAA も品質と速度が向上しています。
<a href="Anti-Aliasing.md">アンチエイリアシング</a> を参照してください。
</def>
<def title="レイトレーシング反射の高速化">
レイトレーシング反射のペイロードを 32 バイトに縮小し、設定を更新しました。DDGI のスカイライトの寄与とレイトレーシング半透明の GI を修正し、SSGI が DDGI と正しく併用できるようになりました。
</def>
<def title="ネイティブ PhysX アクター">
PhysX Instanced Subsystem プラグイン（1.11 に更新）により、多数のボディをネイティブの PhysX アクターとして扱えます。
<a href="Instanced-Physics.md">インスタンス化物理</a> を参照してください。
</def>
</deflist>

## 新機能と変更点

### レンダリング

- **トゥーン** シェーディングモデル。
- **SMAA:** 品質レベルと性能改善を備えたコンピュートベースの実装。
- **FXAA:** 品質と性能を改善し、RDG のパスフラグの検証の修正をバックポート。
- **レイトレーシング反射:** 32 バイトのペイロードと最適化された設定。
- **GI:** DDGI のスカイライトの寄与を改善。`r.RayTracing.Translucency.GI` を修正。DDGI と組み合わせた際の SSGI を修正。
- **ローカライズド IBL** を追加。
- 色再現を UE 5.7 のリファレンスに合わせて更新。分割画面でのスカイとクラウドを修正。
- SSAO の最適化と新しい最適化オプション。
- TressFX のステージングの統合（2 段階）と、arm32 を含む Android でのコンパイルの修正。
- フォワードシェーディング: カラー書き込みのクリアをセパレートトランスルーセンシーの場合のみ実行。

### 物理

- **PhysX Instanced Subsystem** プラグイン（ネイティブ PhysX アクター）を 1.10、続いて 1.11 に更新。
- PhysX のライブラリを Android NDK Clang 19 のツールチェーンに対応させ、ビルド手順を追加。
- Kawaii Physics を UE5 向け 1.18 の移植版に更新。

### プラグイン

- Splash Damage の Abilities プラグインと Automatron プラグインを移植。
- EOS SDK 1.19.0.3 のバイナリ。

### プラットフォームとツールチェーン

- Android NDK 29 に対応し、C++20 でのコンパイルの問題を修正。エディタでの Android Vulkan プレビュー。Clang 向けに
  NEON のスプラットヘルパーを修正。
- Linux サーバーのツールチェーンの修正、Python の修正。
- Windows: `Setup.bat` がスペースを含む GitDependencies のキャッシュパスに対応。シェーダーコンパイルの既定を
  Windows のスケジューラーに変更。
- .NET 4.5.x を対象とするプロジェクトを 4.6.2 に引き上げ。インストール済みエンジンビルドの既定を VS 2026 に変更（VS 2022 を優先するオプションあり）。

### エンジンのデブロート

- HoloLens と Windows Mixed Reality への対応を削除（エンジンソースが約 3 GB 減少）。
- Google VR / Daydream、Azure Spatial Anchors、古い Steam Audio の統合を削除。

### 既定値

- キャラクターのカプセルのオーバーラップイベントを再び有効化。
- 派生データキャッシュをエンジンディレクトリに戻しました。
- Windows Movie Player プラグインを再び有効にし、プロジェクトごとの設定なしで動画を再生できるようにしました。

## リリース後のメンテナンス

| 日付 | 変更内容 |
|---|---|
| 2026 年 7 月 7 日 | モバイル向け TressFX のチェック、必要な箇所での `std::numeric_limits` の infinity の使用を復元 |
| 2026 年 8 月 21 日 | Visual Studio 2026 18.8.2（`_MSC_VER` 1950）と Windows SDK 10.0.26100 で検証、VS 2026 向けのコード項目を更新 |

## アップグレード時の注意点

- **キャラクターのオーバーラップ:** キャラクターのカプセルは再びオーバーラップイベントを生成します。その他のプリミティブコンポーネントは、LTS での設定どおりオプトインのままです。
- **DDC の場所:** 派生データキャッシュがエンジンディレクトリに戻ったため、アップグレード後の最初のエディタ起動時にそこへキャッシュデータが再構築されます。[キャッシュ管理](Cache-Management.md) を参照してください。

<!-- BEGIN GENERATED COMMIT RECORD -->

## 全コミット履歴 {id="commit-history"}

ブランチ: [`ueVite26-MarchMajor-release`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/tree/ueVite26-MarchMajor-release)

### 領域別のコミット数

| 領域 | コミット数 |
|---|---:|
| ツールチェーンとプラットフォーム | 21 |
| レンダリング | 9 |
| その他 | 9 |
| 物理 | 9 |
| アップスケーリングとアンチエイリアシング | 8 |
| エディタとワークフロー | 6 |
| ヘア | 5 |
| レイトレーシングと GI | 5 |
| プラグインとメディア | 5 |
| ゲームプレイフレームワーク | 2 |

### 公開リリースブランチ — 79 件 {collapsible="true" default-state="collapsed"}

79 件のコミット（マージコミット 21 件は表から除外）。

| 日付 | コミット | 作成者 | 変更内容 |
|---|---|---|---|
| 2026-08-21 | [`89271b45b7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/89271b45b7830cc117ae8ca6d26066097e2c979f) | RedPixel | \[Toolchain\] Upgraded codebase toolchain compability |
| 2026-08-21 | [`9d40ecae32`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/9d40ecae323713b1fe04956dc2b92b628586eb8b) | RedPixel | \[Toolchain\] Compiling on VS 18.8.2 (\_MSC\_VER 1950) and Windows SDK (10.0.26100) for Windows 11 |
| 2026-08-21 | [`37433d6859`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/37433d6859272baff4344a1346443e5fbea2daa9) | RedPixel | \[Toolchain\] Updated VS2026 code entries |
| 2026-07-07 | [`d6648361a5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d6648361a54bbea9e95a3f9bee8f72108e74aab8) | RedPixel | \[Toolchain\] STD Infinity usage were needed 2 |
| 2026-07-07 | [`04e33fa783`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/04e33fa783f3b38ffb0733ad08a17b58755e5fa9) | RedPixel | \[Toolchain\] STD Infinity usage were needed |
| 2026-07-07 | [`07e3fc5a01`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/07e3fc5a01a139f35a567851e5ef49f0dedb4651) | RedPixel | \[Mobile\]\[Fix\] Updated TressFX checks |
| 2026-03-12 | [`a75fc9d521`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a75fc9d521a137515cecd1d68618fdc66e8dad6b) | fletch | Add Toon Shading Model |
| 2026-03-11 | [`9700dee4db`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/9700dee4db561fec7f13e59a657c72cebab16739) | Carlo V. | Updated README for major Release |
| 2026-03-08 | [`01064dbf99`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/01064dbf99a66e24978ba70f3bd857610243f408) | tuhoiisa | Add files via upload |
| 2026-03-08 | [`ed8f6d79cd`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ed8f6d79cd0e04274db17a9f166f4abd31026057) | tuhoiisa | Delete Engine/Content/Splash/1 |
| 2026-03-08 | [`358ca03a57`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/358ca03a57eff330d4a22a67d764a9f950ec9400) | tuhoiisa | Add files via upload |
| 2026-03-08 | [`27b7da9396`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/27b7da939645a9a68ec1e2170bca46fe8a9e8090) | tuhoiisa | Create 1 |
| 2026-03-07 | [`0baffd6866`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0baffd68665211d6a6eae7743b6001f2cebb4f10) | RedPixel | Fixed funny issue on the original SMAA Comment that mentioned a header |
| 2026-03-07 | [`5aa3a30cef`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/5aa3a30cef1731ef4539502b2652dd16c67e2ef1) | RedPixel | \[Rendering\]\[RT\] Optimizations to Raytraced Reflections |
| 2026-03-07 | [`a762eec480`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a762eec480902d15bbb9e4d3d743515145f0cf78) | RedPixel | Fix TressFX compilation on Android |
| 2026-03-07 | [`2c7bbf91d3`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2c7bbf91d32accc2906c0d78c81700b53d7a10dd) | RedPixel | \[Rendering\] Updated Optimizations Options for SSAO |
| 2026-03-07 | [`a581412e8c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a581412e8cd078ec478ee902da4270adbb709297) | RedPixel | \[Rendering\] SMAA Improvements. Performance and added Quality Levels |
| 2026-03-07 | [`8941cf40c9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8941cf40c93a9b5cd45edbe49a3fa6e9f60e5429) | RedPixel | \[Rendering\]\[RT\] DDGI SkyLightContribution improvement |
| 2026-03-06 | [`fa37fbb106`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fa37fbb106dc95763e3876f9e5c998e5a0a56323) | RedPixel | \[Rendering\]\[RT\] Optimization to Raytraced Reflections: Introduction of 32 Bytes Payload and Updated Settings |
| 2026-02-28 | [`02540a9075`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/02540a907509c0f9d753b77170a455babd8b6d24) | cryptosebek | \[Win\] Fix GitDependencies cache path parsing with spaces in Setup.bat |
| 2026-02-22 | [`b38463a033`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b38463a03354d38c26964aae5ac2bd83abe9fd64) | EmptyBucket123 | \[Rendering\] Improved FXAA quality and performance. Backport fix for RDG pass flags validation and ERHIAccess::IndirectArgs |
| 2026-02-18 | [`2d3b3eabc7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2d3b3eabc7618b64f5d8d13033151f940eb25f2a) | stephane jacoby | Support Android NDK 29. Fix a couple of C++20 compilation errors to support this. |
| 2026-02-18 | [`1e951b592f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1e951b592f1a7ca57569a923a35db1e553a2b225) | alejandro aguilar | EOSSDK Release 1.19.0.3 CL 49960398 Binary Only Update |
| 2026-02-13 | [`6b31a7518e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/6b31a7518edbc346e9f0f47586d0b324cb8ca996) | RedPixel | \[Ini\] Moving DerivedDataCache back to Engine Dir |
| 2026-02-11 | [`8c96426eb7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8c96426eb74908fb56cdf00466a0c48174d3158f) | RedPixel | \[Plugin\] Ported Splash Damage's Abilities and Automatron Plugins |
| 2026-02-11 | [`9a2c9565de`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/9a2c9565de73074e4119b946d2bd7f60bc5d559f) | RedPixel | \[Defaults\] OverlapEvent re-enabled for Character Capsule |
| 2026-02-11 | [`2d60650150`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2d606501509e928d14ab0173b6af18f56f40c3a3) | RedPixel | Re-enabled WindowsMoviePlayer Plugin for Movies to work without needing activate the plugin in projects |
| 2026-02-11 | [`886a086526`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/886a086526bc67fb6d50679e7a28d4b6ca9d9443) | RedPixel | \[Rendering\]\[Forward\]\[translucency\] Patch over NvRTX, Color write Clear now only runs with SeparateTranslucency on Forward |
| 2026-02-10 | [`e8c5f313ec`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e8c5f313ec3b66893fe34976dcd715e7d857733d) | RedPixel | Feature Pack IterateDirectory instead of FindFilesRecursively |
| 2026-02-05 | [`310541083f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/310541083f4aaed970bc90139abaae8639192b52) | RedPixel | \[Rendering\] SSAO Optimization |
| 2026-02-05 | [`4e74d06c6b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/4e74d06c6b46f2662cebf43940e5966e17c3fcb1) | DESKTOP-PUIKBNQ\\kostas | Fix Linux Toolchain Error when building linux server |
| 2026-02-05 | [`38e696e2bf`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/38e696e2bf3f3064d53bc5bc98851f871f96cf49) | DESKTOP-PUIKBNQ\\kostas | PythonFixes |
| 2026-01-29 | [`7f88fbb40b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7f88fbb40b6cee9d1e77a1bc749088cdc5f58335) | RedPixel | \[Rendering\] TressFX Staging - Part 2 |
| 2026-01-28 | [`abce6475bc`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/abce6475bc2236cbdafd20fa93310f871d8e0818) | RedPixel | \[Rendering\] TressFX Staging - Part 1 |
| 2026-01-20 | [`21a8e31232`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/21a8e312320f63932e6b193f0886fde51861bea7) | RedPixel | Shader Compile Default config to use Windows Scheduler |
| 2026-01-19 | [`56fdef5d6d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/56fdef5d6d2ba35083a7d37432515e4ce90dccaa) | RedPixel | \[Rendering\]\[rt\]\[translucency\]\[fix\] Patch over NvRTX 4.27 commit, fixes SSGI when used in tandem with DDGI |
| 2026-01-04 | [`bdeb57a3d2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bdeb57a3d2e63c03d66394b455ca099cac34a836) | RedPixel | \[Rendering\] \[rt\]\[translucency\] fix the issue that r.RayTracing.Translucency.GI doesn't work. |
| 2026-01-04 | [`ed51ed1ec8`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ed51ed1ec89417a66c6b58ed1b774cd56bdacaad) | RedPixel | Reapply "Reduce ShaderCompilingThread activity while waiting for compile results." |
| 2026-01-04 | [`d810809fca`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d810809fca3ee10ad0ea13e67ca5069adf593b02) | RedPixel | Revert "Update Shader Compiler" |
| 2026-01-04 | [`1fcd08fec0`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1fcd08fec08dc663db252aaccf4e72c63c91a412) | RedPixel | Update Shader Compiler |
| 2026-01-04 | [`9fbef43228`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/9fbef4322883779b370829dedf587aa347c8a620) | RedPixel | Reapply "Shader Compiler: Minor Optimization for path hashing" |
| 2026-01-03 | [`ed4a6f1f1b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ed4a6f1f1b7609f935bf524dec9f8caf27a884a9) | RedPixel | \[Plugin\] Upgraded Kawaii Physics with a ported 1.18 UE5 version |
| 2026-01-03 | [`881262032a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/881262032a0a71053f83c02eb6f0cc471df361d8) | RedPixel | Commit Fix, texture UAsset, add updated uassets |
| 2026-01-03 | [`413c6372e1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/413c6372e116fa4bd093815220cfd8cff0da846a) | RedPixel | Commit FIX, Texture uasset |
| 2026-01-03 | [`d5ab7a6ae9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d5ab7a6ae998496cb6d0fcd3454e48325f885184) | RedPixel | \[Rendering\] Improved SMAA |
| 2025-12-31 | [`60c0b264de`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/60c0b264de4dd2be219f39c76465a6c9fdcc1eba) | RedPixel | \[Plugin\] PhysXInstancedSubsystem Update to 1.11 |
| 2025-12-31 | [`9e50ed919a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/9e50ed919a4d3fa99320a8d056ffbb53cc5019ba) | RedPixel | \[Rendering\] Localized IBL |
| 2025-12-28 | [`134c3add99`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/134c3add99a5d137cac4983447279bac698d56b5) | RedPixel | \[Backport\] Fixed sky and cloud not working in split screen (again, I guess something got lost during a merge from UE4Main). |
| 2025-12-27 | [`c2e10eaee4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/c2e10eaee4d87cf785c0abf5635e496f4897f2dd) | RedPixel | Revert "PR #108 from tanger1n/chaos-debloat" |
| 2025-12-23 | [`bb1ff8d5ed`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bb1ff8d5ed78f945830cae11aed4f7b98d7dbf49) | RedPixel | Revert "PR #105 from tanger1n/ Removal of Virtual Production" |
| 2025-12-23 | [`fe063f3100`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fe063f3100992e32389644ce587a6e02cecb4d2c) | RedPixel | Revert "PR #101 from bennystarfighter/ueVite-Release" |
| 2025-12-23 | [`fea568a17d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fea568a17d28b161aa41da5d638d8b30e16ce04b) | tanger1n | deleted HPMotionController as part of wmr clean up |
| 2025-12-23 | [`b2f67a7ad6`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b2f67a7ad63b210ca30c1445e791d1161da51e00) | tanger1n | remove hololens and wmr support from the engine. reduced engine size for 3 gb |
| 2025-12-22 | [`a77a421bdf`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a77a421bdf217eb42578695fd133430bb391c54e) | RedPixel | \[Plugin\] PhysXInstancedSubsystem Update to 1.10 |
| 2025-12-22 | [`7d115b303b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7d115b303bba47af4d841549fefca6de9df7a1a3) | tanger1n | small chaos debloat |
| 2025-12-22 | [`7df71032af`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7df71032afefa22bbe30feab9f7246383d5e26e4) | RedPixel | \[Rendering\] Updated Colour Reproduction to Match UE-5.7 Reference |
| 2025-12-22 | [`8a14dd6271`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8a14dd6271847b9965c6bbe04455df5b8f114afd) | tanger1n | removal steamaudio due very old integartion in the engine |
| 2025-12-22 | [`83f0cbfdfc`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/83f0cbfdfc3d0b3e4ceee8bc2f2c6103140097fb) | tanger1n | removal virtual production related plugins to debloat engine and reduce disk size |
| 2025-12-21 | [`5ec49ceb2a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/5ec49ceb2a2814a1bf2fca7d71cdf940bb74fa57) | tanger1n | remove googleVr and google daydream due deprecation |
| 2025-12-20 | [`722cd507c7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/722cd507c7dca4546bb9f1c5d4d3f5cf9fa2297a) | Carlo V. | Update README.md |
| 2025-12-20 | [`53bda764c5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/53bda764c5023c32f98ca605225351af43cc4688) | tanger1n | removed AzureSpatialAnchors due backend deprecation |
| 2025-12-20 | [`da0ec92fff`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/da0ec92fff272716cb404b823d543264498153f9) | Benjamin L | Bump dotnet projects targeting v4.5.x up to v4.6.2 which is still available in newer visual studio versions |
| 2025-12-19 | [`bc4de9ab27`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bc4de9ab27d670f26d986f8e1ecff7e6b938f666) | RedPixel | \[Plugin\] PhysXInstancedSubsystem (Native PhysX actors usage) |
| 2025-12-19 | [`db0f9af647`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/db0f9af647367eead1899bf2585317dac413c025) | Benjamin L | Updated InstalledEngineBuild to use VS2026 by default with a option to prefer VS2022 |
| 2025-12-19 | [`b1782ead1c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b1782ead1c2ecf888efcc0c6112d8d8c89f8dbb5) | Carlo V. | Update .gitignore |
| 2025-12-18 | [`bf2bb46286`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bf2bb46286c27addc63cb9cc4c349caa6db41ff0) | tanger1n | Fix clang NEON splat helpers + changed cmake rule for c++ 17 |
| 2025-12-18 | [`e06c4b7318`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e06c4b73182034c1af325c94b2044b7473ee4d0e) | RedPixel | Removed STD Infinity usage |
| 2025-12-18 | [`2ceb9ff215`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2ceb9ff2153072a9ba5b6c6fc01df19da47a4486) | RedPixel | Revert "\[Engine Debloat\] Removal of HoloLens support to improve compile times and reduce engine size by ~3 GB" |
| 2025-12-18 | [`ec17b799a3`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ec17b799a35f1b51e411c522911591ee4ba6bbde) | RedPixel | \[Engine Debloat\] Removal of HoloLens support to improve compile times and reduce engine size by ~3 GB |
| 2025-12-18 | [`adaf7d45d4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/adaf7d45d4b93e721895f8cd6517d8647e4c2686) | Dmitrii Komarevtsev | extra protection for physx compatability with NDK Clang 19 |
| 2025-12-17 | [`fcbc45ed30`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fcbc45ed30465d564d2bf60864c804a7695a3443) | RedPixel | Compute Based SMAA |
| 2025-12-17 | [`830f0b590e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/830f0b590e9a42086e88d27b67a8458528d16afd) | RedPixel | CleanUp |
| 2025-12-17 | [`7194027f36`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7194027f3602a40ac57e1048d351af95596c95a1) | RedPixel | SMAA WIP 3 |
| 2025-12-17 | [`289ce24222`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/289ce24222b3784968d807aa6b386175abd50e48) | RedPixel | SMAA WIP 2 |
| 2025-12-17 | [`7bee7b0d06`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7bee7b0d0680510a31b780498dfe4eb638e83f57) | RedPixel | SMAA WIP 1 |
| 2025-12-16 | [`f4796b30a8`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f4796b30a8af33d391d23b3ddcbc06f317708579) | Dmitrii Komarevtsev | fix TressFX to compile for android (arm32) |
| 2025-12-16 | [`797fcfb765`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/797fcfb765922bf0e7f82be6c7c09e049b1427b0) | Dmitrii Komarevtsev | added readme build physx libs for Android |
| 2025-12-16 | [`eabae54d81`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/eabae54d811b6898598da010c42107ed5258b3b3) | Dmitrii Komarevtsev | make physX lib compatible with ndk clang 19 |
| 2025-12-12 | [`3b081dacba`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3b081dacba1ff5de431dfd985c2f301a2e5f1b71) | Dmitrii Komarevtsev | Make android vulkan preview works in editor |

<!-- END GENERATED COMMIT RECORD -->

## 関連項目

- [すべてのリリースノート](Release-Notes.md)
- [ueVite26 June Major](ueVite26-JuneMajor.md)
- [ueVite25 LTS](ueVite25-LTS.md)
- [シェーディングモデル](Shading-Models.md)
