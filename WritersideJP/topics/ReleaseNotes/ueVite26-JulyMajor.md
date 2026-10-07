# ueVite26 July Major

<tldr>
<p>
July はパフォーマンスのゲーティングと製品化への備えに重点を置いたリリースです。オプションのシェーダーモデルを既定でコンパイル対象から外して <b>12.3% のフレームレート向上</b> を得たほか、TressFX をオプトインにし、<b>NVIDIA Blast</b>
の SDK を更新し、9 つのエンジンプラグインを UE5 からバックポートし、<b>ViteSetup</b> アシスタントをガイド付きのインストール手順を中心に作り直しました。
</p>
<p>
ブランチ <code>ueVite26-JulyMajor-release</code> &middot; ベース:
<a href="ueVite26-JuneMajor.md">ueVite26 June Major</a>
</p>
</tldr>

| 状態 | 開発期間 | ベース | コミット数 |
|---|---|---|---:|
| メジャー | 2026 年 7 月 29 日〜8 月 23 日 | [ueVite26 June Major](ueVite26-JuneMajor.md) | 78 |

## ハイライト

<deflist>
<def title="既定で 12.3% 高速化">
Toon、Callisto、FSR 2 のリアクティブのシェーディングパスは、それぞれのスイッチを有効にしてエンジンをビルドしない限りコンパイルされなくなりました。RTX 4080 Super、1440p の Unreal Tournament Vite シーンでは、フレームレートが 235.56 FPS から
264.44 FPS に向上します。<a href="Shading-Models.md">シェーディングモデル</a> を参照してください。
</def>
<def title="NVIDIA Blast の更新">
Blast の SDK を更新し、スキンキャッシュの再構築に対応し、破砕エディタが DDC のデータを正しく無効化してボーンのインデックスを検証するようになりました。<a href="Destruction-And-Cloth.md">破壊とクロス</a> を参照してください。
</def>
<def title="UE5 プラグインのバックポート">
Cable Component（レンダリングのオーバーヘッドを避ける UE 5.8 のパスを含む）、RenderDoc、Visual Studio Code、Platform Crypto、Animation Budget Allocator、Chunk Downloader、Significance Manager、Sun Position を 4.27 向けに適応させました。
</def>
<def title="ViteSetup の刷新">
2 つの主要な手順からなるガイド付きフロー、Visual Studio 2022 と 2026 のプロファイル、全プラットフォームのデブロート、サンプルの整理、ストリップ後のモジュール参照の検証、そして標準の 4.27 に合わせたプラグインの既定値です。
<a href="ViteSetup.md">ViteSetup</a> を参照してください。
</def>
</deflist>

## 新機能と変更点

### レンダリングとゲーティング

- 追加のシェーディングモデル（Toon、Callisto、FSR 2 リアクティブ）を既定で無効化: 基準シーンで FPS が 12.3% 向上。
- **TressFX** を `VITE_TRESSFX` によるオプトインに変更し、モバイルと ES 3.1 のシェーダープラットフォームから除外。デバッグとフォワードライティングのパスに null チェックを追加。
- DLSS とレイトレーシングの半透明をコンパイル時にゲーティング。
- **プロジェクト設定 &gt; レンダリング** にレイトレーシング機能の切り替えを追加（レイトレーシングが実際に利用可能な場合のみ表示）。
- レイトレーシングのシェーダーをコンパイルする際は、常にパストレーシングのスカイライトシェーダーもコンパイル。セパレートトランスルーセンシーのロードアクションを修正。ローカライズド IBL をインスタンスステレオ（VR）に対応。
- *Max Shadow Draw Distance* によって生じたローカルライトのシャドウのカリングの不具合と、フォワードシェーディングでローカルライトの影が欠ける問題を修正。

### 物理

- NVIDIA Blast の SDK を更新し、スキンキャッシュの再構築に対応、破砕エディタを修正。

### プラグイン

- UE 5.2/5.3/5.8 からの適応済みバックポート: Cable Component、RenderDoc、Visual Studio Code、Platform Crypto、Animation Budget Allocator、Chunk Downloader、Significance Manager、Sun Position。
- ImGui のベンチマークユーティリティが Shipping ビルドでもスレッドのレポートを出力。

### 既定値

- フレームペーシングを安定させるため、スタンドアロンとパッケージ化したビルドのフレームレート上限を 120 に設定。
- 関数経由で呼び出した場合の `SetGenerateOverlapEvents` の既定値を `false` に変更。
- 新しいアニメーションの既定の圧縮を ACL に変更。
- DDGI（RTXGI）プラグインを既定で有効化。
- June で既定で有効だった NRD（ReLAX）のデノイザーのプラグインを、既定で無効に変更。それを使うレイトレーシングのエフェクトとともに有効にしてください。
- リリース時点では、その他のプラグインの既定値は標準の 4.27 と同じです。Vite のデブロート済みプラグイン構成を適用するには `ueVite-ApplyVitePluginDefaults.bat` を実行してください。

### セットアップとツールチェーン

- ViteSetup: 2 つのガイド付き手順、VS 2022 / VS 2026 のプロファイル、全プラットフォームのデブロート、サンプルの整理（Third Person と Vehicle は残す）、重要度の低い Vite プラグインの任意削除、MSBuild のチェック、対話式の依存関係の同期、ソースターゲットと一緒に Unreal Insights をビルド、デブロートのストリップ後のモジュール参照の検証。
- `ueVite-ApplyVitePluginDefaults.bat` が Vite のデブロート済みプラグインの既定値を適用。
- Visual Studio 2026 18.8.2（MSVC 14.50、`_MSC_VER` 1950）と Windows SDK 10.0.26100 で検証。

## アップグレード時の注意点

- **TressFX** はビルド時に `VITE_TRESSFX=1` が必要になりました。ストランドヘアを使うプロジェクトは有効にしてください。[コンパイル時スイッチ](Compile-Time-Switches.md) と [ヘアレンダリング](Hair-Rendering.md) を参照してください。
- **シェーディングモデル:** Toon、Callisto BRDF、FSR 2 のリアクティブマスクは、既定で無効のコンパイル時スイッチになりました。これらを使うプロジェクトは、`VITE_SHADINGMODEL_TOON=1`、`VITE_SHADINGMODEL_CALLISTO=1`、`VITE_FSR2_REACTIVE_MASK=1` を指定してビルドする必要があります。
- **フレームレートの上限:** パッケージ化したビルドとスタンドアロンのビルドは、既定で 120 FPS が上限です。ベンチマークを取る際は上限を引き上げるか解除してください。

<!-- BEGIN GENERATED COMMIT RECORD -->

## 全コミット履歴 {id="commit-history"}

ブランチ: [`ueVite26-JulyMajor-release`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/tree/ueVite26-JulyMajor-release)

### 領域別のコミット数

| 領域 | コミット数 |
|---|---:|
| エディタとワークフロー | 23 |
| ツールチェーンとプラットフォーム | 22 |
| レンダリング | 9 |
| プラグインとメディア | 7 |
| 物理 | 5 |
| ヘア | 3 |
| レイトレーシングと GI | 3 |
| アニメーション | 2 |
| その他 | 2 |
| ゲームプレイフレームワーク | 1 |
| アップスケーリングとアンチエイリアシング | 1 |

### 公開リリースブランチ — 78 件 {collapsible="true" default-state="collapsed"}

78 件のコミット（マージコミット 8 件は表から除外）。

| 日付 | コミット | 作成者 | 変更内容 |
|---|---|---|---|
| 2026-08-23 | [`739e04e84a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/739e04e84a68ae317ad92b49add9cd494e446718) | Carlo V. | Update README.md |
| 2026-08-22 | [`fcc2aa0d77`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fcc2aa0d77c6b6e69276c4bad6c45167d3512085) | RedPixel | \[Blast\] Added support for SkinCache Rebuild |
| 2026-08-22 | [`60948cda75`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/60948cda75298a70b03809f03a4703277c4fe2ad) | RedPixel | \[Bats\]\[Plugins\] Upgraded Bats for Engine Installation and plugins defaults now mirror 4.27, debloat default plugins with ueVite-ApplyVitePluginDefaults.bat |
| 2026-08-22 | [`ca9da2fd16`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ca9da2fd1689233895ab5f749bd4d71f34264d87) | RedPixel | \[VR\] Adapted IBL for Instanced Stereo |
| 2026-08-19 | [`049efa3dd5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/049efa3dd5dfaf1eea610b8d6efc8071b2bab03a) | Carlo V. | Update README.md |
| 2026-08-19 | [`3c3e219a99`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3c3e219a99ce41f7aa40e25a6ce84d9e57b2b03b) | RedPixel | \[Setup\] Original Setup.bat |
| 2026-08-19 | [`55ec41a1d9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/55ec41a1d906b70af7d5421e1cf1079b90e7751b) | tuhoiisa | \[Setup\] Validate module references after a debloat strip and unexclude MovieScene |
| 2026-08-19 | [`b48b29190d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b48b29190d3c7aa156206c2d0a9566c6bce46174) | tuhoiisa | \[Rendering\] Fix local light shadow culling regressions from Max Shadow Draw Distance |
| 2026-08-19 | [`6224421c4a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/6224421c4ad783152d0827ea77f9a95b4c7342e1) | tuhoiisa | \[Rendering\] Fix missing local light shadows in Forward Shading |
| 2026-08-19 | [`3d00c45d33`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3d00c45d33d0cdb20ead487ae4488c8bff1d7008) | tuhoiisa | \[Setup\] Swap the setup entry point names, make dependency sync interactive |
| 2026-08-18 | [`fbaa45af28`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fbaa45af28da8091fcefc43ffa4e152a0f404fb1) | RedPixel | \[Optimization\]\[Gating\] Disabled the extra Shading Models by Default to save on performance: yields a 12.3&#37; FPS increase |
| 2026-08-17 | [`b64b7c2e86`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b64b7c2e86a53bb26617be557a3c6a1e0669ac8d) | tuhoiisa | \[Setup\] Gate MSBuild in the environment check |
| 2026-08-14 | [`64741e129f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/64741e129f62c8f5586085b8410f74926b70251a) | Carlo V. | Update README.md |
| 2026-08-12 | [`d9edf40915`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d9edf40915d60b1cba00396626e11d0a24a27228) | RedPixel | \[Defaults\] Default FrameRateLimit for Standalone and Builds set to 120 in order to keep Frame Consistency |
| 2026-08-12 | [`d9d22b4bbc`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d9d22b4bbcad7a8ae6fff081060b44b192f42460) | RedPixel | \[IMGUI\]\[Benchmarking\] Added Threading Reports for Shipping Builds with ImGUI Utility |
| 2026-08-12 | [`457da6a277`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/457da6a2770cf16b76173b998e4422ff2b349bb7) | Carlo V. | Update README.md |
| 2026-08-12 | [`40cab583df`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/40cab583df60afe829b406b57a7cfb59376be5d0) | Carlo V. | Update README Hardware Reference.md |
| 2026-08-12 | [`6c06073595`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/6c0607359588d472d12515da03ce94abc09d24d7) | Carlo V. | Update README.md |
| 2026-08-11 | [`65f603d428`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/65f603d428d15cb0b6d3c69eda3a1bd56ea6dbe6) | Carlo V. | Update README.md |
| 2026-08-11 | [`dbcac43450`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/dbcac43450c9d4de94f91a50aa35478411d5f63a) | Carlo V. | Update README.md |
| 2026-08-11 | [`ab0859b8d6`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ab0859b8d663440d2b682ea88a549043cbe331c6) | Carlo V. | Update README.md |
| 2026-08-11 | [`2834897775`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/28348977755992a8dfc18ed6f77f753d36d7c1b1) | Carlo V. | Update README.md |
| 2026-08-11 | [`77cb3e8068`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/77cb3e806839ed80f8b0e1955b648732802493da) | Carlo V. | Update README links to other READMEs and Documentation Links.md |
| 2026-08-11 | [`2dae10eae4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2dae10eae45bdd3a0b1dda173e5e208b728c59f9) | Carlo V. | Update README UE4 Titles Reference.md |
| 2026-08-11 | [`8de4bc40d8`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8de4bc40d86a26f7187438a2f5e11d63d791f963) | Carlo V. | Update README Build Configuration.md |
| 2026-08-11 | [`910b435e80`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/910b435e80da7a4eb7fbf8f8430c829f1e0edb21) | Carlo V. | Update README.md |
| 2026-08-11 | [`0b0104f7db`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0b0104f7dba35d940c1b5716580105ad1dcb7e5a) | Carlo V. | Update README Performance Analysis.md |
| 2026-08-11 | [`80a5292936`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/80a5292936ee50735d9fb0308e4c90e568d3dc0d) | Carlo V. | Update README.md |
| 2026-08-11 | [`25659dabd4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/25659dabd47cb528d5d3352bb4c881703bdf5af2) | Carlo V. | Update README.md |
| 2026-08-11 | [`0e9915fe22`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0e9915fe22339e017c58b66e025173df5702aa3c) | RedPixel | \[Defaults\] SetGenerateOverlapEvents by function to false |
| 2026-08-11 | [`4b6868fe12`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/4b6868fe1208d4c9df26480fd8cc687e2a18da93) | Carlo V. | Update README Feature Section.md |
| 2026-08-11 | [`4ff38ead9f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/4ff38ead9f2f7ad8037c7ed3403680429356caea) | Carlo V. | Update README feature specification.md |
| 2026-08-11 | [`d73bb1d820`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d73bb1d8204b0971b8be3e6c01bad5f47de7ab96) | RedPixel | Update Setup README |
| 2026-08-10 | [`cabd6e8e55`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/cabd6e8e55c0548b163fcf2ba3f4424549a76468) | RedPixel | Blast Enabled By Default |
| 2026-08-10 | [`3a81672fdf`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3a81672fdf09554384f6f1d42ddca72a0b86f293) | tuhoiisa | \[Rendering\]\[TressFX\] Null-guard the debug and forward lighting passes |
| 2026-08-10 | [`0f30811b6b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/0f30811b6b6a3f970702d4d124b954ca17369ff8) | tuhoiisa | \[Rendering\]\[TressFX\] Make TressFX an opt-in feature behind VITE\_TRESSFX |
| 2026-08-10 | [`73fb8e5ce9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/73fb8e5ce950b74585b61bb2bc7b679f2726c623) | tuhoiisa | \[Rendering\]\[TressFX\] Exclude TressFX shaders from mobile and ES3.1 platforms |
| 2026-08-10 | [`544c2e1b6d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/544c2e1b6de82c5f9aa76b924b9c575bdc3eda54) | tuhoiisa | \[Editor\] Gate the Raytracing project settings on actual RT availability |
| 2026-08-10 | [`7742958773`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/77429587737b62084120e8d96bbc572e0e074f7f) | tuhoiisa | \[Anim\] Default new animations to ACL compression |
| 2026-08-10 | [`f3da6f857e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f3da6f857e9f7c1d258995911f82eb55c6148ba7) | RedPixel | \[Defaults\] Disabled Chaos Solver |
| 2026-08-10 | [`20e657755e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/20e657755e9d24de02dc4160a6cd7f92c8b3f1c0) | RedPixel | \[Defaults\] Disabled plugins, enabled DDGI Plugin by default |
| 2026-08-10 | [`41c98ea1b4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/41c98ea1b43cdaceda81978f41e1f0388ec960b9) | Carlo V. | Update NvRTX Documentation README.md |
| 2026-08-10 | [`4af2864089`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/4af286408912cdfcdc7a75cffac76dd20cfd2262) | Carlo V. | Update NvRTX Documentation README.md |
| 2026-08-09 | [`b928545da2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b928545da207a24f20d655e594ee8b6c28c9c225) | RedPixel | Removed AOCheckFXSystem |
| 2026-08-09 | [`e8dc4d53e5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e8dc4d53e59d78604c2b7534bcb828493897a18c) | RedPixel | \[Backport 5.8\]\[Plugin\] Manual Backport of Engine Plugin: Cable Component Part #2 (Avoids Rendering Overhead) |
| 2026-08-08 | [`6054f22695`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/6054f22695c7892e375354ecd5751643a85987e6) | RedPixel | \[PhysX\] Blast Plugin Upgrade SDK |
| 2026-08-08 | [`2288d72c6a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2288d72c6ac6fb4b43c9e3f290a75efe4e99666f) | RedPixel | Separate Translucency Load Action |
| 2026-08-08 | [`a317ad0e02`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a317ad0e02a80a89e34ce9918273d4878bd18c85) | RedPixel | Compile the path tracing skylight shaders whenever ray tracing shaders are compiled |
| 2026-08-08 | [`eb9e56ad76`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/eb9e56ad7612d3b81e732ec61b7753828dcd026a) | tuhoiisa | Add includes the BlastMeshEditor module relies on unity for |
| 2026-08-08 | [`cd760ba50b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/cd760ba50bbd689d48f1720dc921b1f05c778500) | tuhoiisa | Register static mesh attributes before RetrieveMesh |
| 2026-08-08 | [`fdf3eb29b6`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fdf3eb29b6ac7a381609d1d7d2147c3c16f0aefa) | tuhoiisa | Invalidate the DDC GUID on fracture, guard bone indices |
| 2026-08-07 | [`019fb6ab24`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/019fb6ab2496bd45f0e04652af1ab957f34db2c9) | RedPixel | Asign RValue to SkelMeshRenderData before Branch |
| 2026-08-06 | [`fc6d5ee931`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/fc6d5ee9316d960eee4af209c77f0725b2ec5dd8) | RedPixel | \[Backport 5.3\]\[Plugin\] Adapted Backport of Engine Plugin Cable Component |
| 2026-08-06 | [`840ee170e0`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/840ee170e069f38d48b78b0882e875d8b3bfc110) | RedPixel | \[Backport 5.2\]\[Plugin\] Adapted Backport of Engine Plugin RenderDoc |
| 2026-08-06 | [`705a2f091a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/705a2f091ab0f53cad6099bc257ed172c4f79d00) | RedPixel | \[Backport 5.2\]\[Plugin\] Adapted Backport of Engine Plugin Visual Studio Code |
| 2026-08-06 | [`441d9dad16`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/441d9dad16ff3fa88f76963ff1b36b346676670f) | RedPixel | \[Backport 5.2\]\[Plugin\] Adapted Backport of Engine Plugin Platform Crypto |
| 2026-08-06 | [`e6b98f472c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e6b98f472c2bd730e1c621c15a58aa22f4ec9bee) | RedPixel | \[Backport 5.2\]\[Plugin\] Adapted Backport of Engine Plugin Animation Budget Allocator |
| 2026-08-06 | [`31534a4e33`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/31534a4e33174db704302dd3c1002d6598832918) | RedPixel | \[Backport 5.2\]\[Plugin\] Adapted Backport of Engine Plugin Cable Component |
| 2026-08-06 | [`8607b0e90e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8607b0e90e4ffe72fb317beffd51d3d7f89decf5) | RedPixel | \[Backport 5.2\]\[Plugin\] Adapted Backport of Engine Plugin Chunk Downloader |
| 2026-08-06 | [`5562ed4bf4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/5562ed4bf45bdef933c7d5e25e1a6654a626dda9) | RedPixel | \[Backport 5.2\]\[Plugin\] Adapted Backport of Engine Plugin Significance Manager |
| 2026-08-06 | [`a27e4364b1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a27e4364b19add534758cb0284ec0ccf1ac817bd) | RedPixel | \[Backport 5.2\]\[Plugin\] Adapted Backport of Engine Plugin SunPosition |
| 2026-08-03 | [`b3a66c4df9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b3a66c4df95f2b7ca27b946964d6bc6859eb6165) | tuhoiisa | \[Setup\] Skip iPhonePackager when iOS is excluded |
| 2026-08-03 | [`ff2a01ec4d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ff2a01ec4d5f552fe7cdfe0a8b83bf7434d3caf1) | tuhoiisa | \[Setup\] Add option to remove less important Vite plugins |
| 2026-08-03 | [`2ae1d25524`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/2ae1d255242ebc8f0d0e6ea726a93f4aff95147d) | tuhoiisa | \[Setup\] Split the guided flow into two core paths |
| 2026-08-03 | [`6c56f8baeb`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/6c56f8baeba092fe754ba9044d0f805e749e2b7b) | tuhoiisa | \[Setup\] Build UnrealInsights with the source targets |
| 2026-08-03 | [`d663ddd92c`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/d663ddd92c69a2671a9720656d9afbfa5cf9878e) | tuhoiisa | \[Setup\] Prune sample projects except Third Person and Vehicle |
| 2026-08-03 | [`f32749cbad`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f32749cbad5b9e77fef8b6c418c4451dc041e598) | tuhoiisa | \[Setup\] Add all-platform debloat option |
| 2026-08-03 | [`5d7493eb7b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/5d7493eb7bd4f81e0bd1aeaa4e334bc219a248ab) | tuhoiisa | \[Setup\] Add VS2022 and VS2026 toolchain profiles |
| 2026-08-03 | [`27a5919670`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/27a591967041b81af48830124c47cea42340e932) | tuhoiisa | \[Setup\] Prefer WinRAR over 7-Zip for binary archives |
| 2026-08-03 | [`059251bca8`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/059251bca818e69597d7425ec887efb99134bcfb) | tuhoiisa | \[Setup\] Add 4.5 download stats |
| 2026-08-01 | [`f934b45b7b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f934b45b7bdac0c022752accc2505f541ce78235) | RedPixel | Cached localized IBL CVar |
| 2026-07-31 | [`7def2d7051`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7def2d7051cfc466c98c3857ba1c9bbbddc8f3a2) | RedPixel | \[gitignore\] Updated to include PhysX-Blast Plugin content Folder |
| 2026-07-31 | [`74d9dea475`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/74d9dea475d0170f2380398c19603f33189c79b6) | RedPixel | \[Toolchain\] Compiling on VS 18.8.2 (\_MSC\_VER 1950) and Windows SDK (10.0.26100) for Windows 11 |
| 2026-07-31 | [`70827df2f2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/70827df2f2a41b40ffdc000227391af0c7456b05) | tuhoiisa | \[Editor\] Added Raytracing feature toogles to Rendering Project Settings |
| 2026-07-30 | [`a0855402e0`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/a0855402e0efb285c5d9e97ac4dbcf874571d678) | tuhoiisa | \[Rendering\] AmbientOcclusion Macro Update |
| 2026-07-30 | [`f4830395a1`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f4830395a1b40eae4f8777369115849b2fe5982f) | tuhoiisa | \[Plugin\] Replacing PlatformAllowList with WhitelistPlatforms |
| 2026-07-29 | [`7ba848ec89`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7ba848ec89d290299ef572f676017a8aad3fb23e) | Tuhoiisa | \[Gating\] RT Translucency Guard |
| 2026-07-29 | [`051cde6cd7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/051cde6cd72edb8338bc9f0f91bf9ce488885469) | Tuhoiisa | \[Gating\] DLSS |

<!-- END GENERATED COMMIT RECORD -->

## 関連項目

- [すべてのリリースノート](Release-Notes.md)
- [ueVite26 August Major](ueVite26-AugustMajor.md)
- [ueVite26 June Major](ueVite26-JuneMajor.md)
- [ViteSetup](ViteSetup.md)
