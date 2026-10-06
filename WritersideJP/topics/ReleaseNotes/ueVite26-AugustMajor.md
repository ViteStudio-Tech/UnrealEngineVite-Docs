# ueVite26 August Major

<tldr>
<p>
Vite 史上最大のリリースで、<b>438 件の変更</b> を含みます。エディタの応答性、メモリ、D3D12 の安定性に関する大規模な
UE5 バックポート、レイトレーシング反射とスペキュラーオクルージョンの新機能、Gameplay Ability System の更新、
Intel XeSS 3.1、そして Visual Studio 2026（MSVC 14.51）への対応です。リリース後には macOS / Xcode 26 への移植と、
DLSS と XeSS のランタイムの更新が加わりました。
</p>
<p>
ブランチ <code>ueVite26-AugustMajor-release</code> &middot; リリース日: 2026 年 8 月 24 日 &middot; ベース:
<a href="ueVite26-JulyMajor.md">ueVite26 July Major</a>
</p>
</tldr>

| 状態 | 開発期間 | ベース | コミット数 |
|---|---|---|---:|
| メジャー | 2026 年 7 月 25 日〜8 月 24 日（10 月 2 日までメンテナンス） | [ueVite26 July Major](ueVite26-JulyMajor.md) | 438（ステージング 420 件 + リリースブランチ 18 件） |

## ハイライト

<deflist>
<def title="エディタとメモリのバックポート">
4.27 の API に合わせて適応させた大規模な UE5 バックポートにより、日々のイテレーションのコストを削減しました。
ツールチップとプロパティのウィジェットは必要時に生成されるようになり（選択の切り替え時に最大約 400 ms 短縮）、
ウィンドウメニューのヒッチは 1〜5 秒から約 15 ms に減り、アセットのサムネイルがアセット全体を読み込まなくなり、
Windows の既定のアロケーターは、メモリ使用量が少なく割り当ても速い <b>mimalloc</b> になりました。
</def>
<def title="レイトレーシング反射とオクルージョン">
ディファードの RT 反射は、ミス時にスカイのキューブマップをサンプリングし、フォリッジ、サブサーフェス、スキンへの
ヒットに追加のディフューズを加え、既定値も最適化されました。<code>VITE_SPECULAR_OCCLUSION</code> の下で新しい
<b>ベントノーマルによるスペキュラーオクルージョン</b>（Jimenez 2016）が使えるようになり、RT シャドウは光源の長さ
（Source Length）に対応しました。
</def>
<def title="D3D12 と Vulkan の安定性">
フェンスとレジデンシーの修正、コア数の少ない PC でのデッドロックの修正、UAV バリアの復元、バッファのアップロード時の
SRV ステートキャッシュの正しい無効化、そして Vulkan のパイプラインキャッシュに関するセキュリティ修正です。シェーダー
バインディングテーブルの更新は、ワーカースレッド間の偽共有を避けるようになりました。
</def>
<def title="Gameplay Ability System の更新">
UE 5.1 からの約 40 件の GAS の修正と機能です。<code>WaitGameplayTagQuery</code>、ブループリント向けの
<code>AddLooseGameplayTags</code> / <code>RemoveLooseGameplayTags</code>、<code>PostAttributeChange</code> コールバック、
アクティブなエフェクトの SetByCaller マグニチュード、レプリケーションの修正、<code>ShowDebug AbilitySystem</code> を
含みます。
</def>
<def title="アップスケーリングとフレーム生成">
Intel XeSS を 3.1.0 に更新し、UE 4.27 で XeFG のフレーム生成を再び有効にしました。リリース後、DLSS のランタイムは
NGX 310.7.129 に更新されました。<a href="Upscalers.md">アップスケーラー</a> を参照してください。
</def>
<def title="ツールチェーン">
Visual Studio 2026 18.9.1（MSVC 14.51、<code>_MSC_VER</code> 1951）と Windows SDK 10.0.26100 でコンパイルでき、
Clang 11 のツールチェーンに対応し、特に遅い翻訳単位のコンパイル時間を短縮しました（例:
<code>ShowFlags.cpp</code> は 17 秒から 5 秒）。
</def>
</deflist>

## 新機能と変更点

### レンダリング

- **スペキュラーオクルージョン:** DFAO/SSAO のベントノーマルを使う Jimenez 2016 のコーンベースのスペキュラー
  オクルージョン。`VITE_SPECULAR_OCCLUSION=1` でコンパイル時に有効にします。既定は引き続き Karis の項です。
- **ローカル露出:** UE 5.0 のローカル露出のパスとポストプロセス設定を `VITE_UE5_POSTPROCESSING`（既定で有効）の下に
  バックポート。
- **アンチエイリアシング:** SMAA を Epic の UE 5.7 のパイプラインの移植に置き換え。エッジ検出、ステンシルで限定した
  ブレンドの重み、近傍ブレンドで構成され、4 段階の品質（`r.SMAA.Quality`）と、色または輝度によるエッジ検出
  （`r.SMAA.EdgeMode`）を備えます。`r.Vite.SMAA.Mode` は廃止されました。
- **ボリュメトリクス:** ボリュメトリッククラウドにトレースの最大距離モードを追加。シャドウ品質が `0` のときの
  レイトレーシングによるボリュメトリックフォグのライトパスを復元。
- **シャドウ:** 半透明のシャドウ、*Cast Shadow as Masked* を使うマテリアルインスタンスからの影の欠落、シャドウ
  フィルタリングの Gather4 のオフセットを修正。*Cast Shadow* が無効なオブジェクトは距離フィールドシャドウに寄与しなく
  なりました。
- **ライティング:** `r.AllowStaticLighting` が無効でもステーショナリーライトが正しく動作。リフレクション
  キャプチャでライト関数を使用可能に。ステーショナリーのスカイライトの表示フラグを修正。
- **ポストプロセス:** シーンキャプチャでトーンマッパーとポストプロセスマテリアルを表示可能に。すべてのピクセルが
  ステンシルテストに失敗する場合はポストプロセスマテリアルのパスをスキップ。GTAO がカメラカットに対応。
- **メッシュの描画:** HISM の動的描画のセットアップを軽量化。MinLOD をストリーミング済みの LOD に制限。描画距離や
  カリング距離が変わってもレンダーステートを再構築しなくなりました。

### レイトレーシング

- **RT ディファード反射:** ミス時のスカイキューブマップ、フォリッジ・サブサーフェス・スキンへのヒットでの追加
  ディフューズ、最適化された既定値。[レイトレーシング反射](RT-Reflections.md) を参照してください。
- **RT シャドウと RTAO:** 既定値を調整。RT シャドウが光源の長さに対応。無効なシャドウレイをトレースしなくなりました。
- **シーン管理:** ランドスケープのグラスを既定で RT シーンから除外。新しい
  `r.RayTracing.Geometry.InstancedStaticMeshes.MinLOD`。`r.RayTracing.ParallelMeshBatchSize` を 128 から 1024 に
  引き上げ。反射の RTPSO のゲーティングを完了。
- **デノイズ:** ReGIR の計算方法と ReLAX の履歴の既定値に関する NvRTX 5.0 の更新、そしてデノイズが破綻するシーンの
  修正。NVIDIA 向けのパスをコンパイル時スイッチで残したまま、AMD の GPU でスクリーンスペースのデノイズを修正。
- **D3D12 の SBT:** シェーダーバインディングテーブルを埋める処理の細かな最適化と偽共有の防止。

### アップスケーリングとフレーム生成

- Intel XeSS 3.1.0。UE 4.27 で XeFG のフレーム生成を再適用。
- リリース後: DLSS の NGX ランタイム 310.7.129、DLSS Ray Reconstruction のプリセット F を DLSS 4.5 のモデルとして
  明記、UE 4.27 での XeSS 3.1.0 のインストールと待機のガードを修正。

### ゲームプレイフレームワーク

- UE 5.1 からの Gameplay Ability System のバックポート。`WaitGameplayTagQuery`、ルースタグのブループリント関数、
  `PostAttributeChange` / `PostAttributeBaseChange`、SetByCaller マグニチュードの動的変更、ローカルでのアビリティ終了、
  そして多数のレプリケーションと安定性の修正を含みます。
- ブループリントで UFunction、変数、変換、Kismet の数学関数の double に対応。*Print String* に *Key* パラメーターを
  追加。関数グラフで開発専用ノードをバイパス可能に。
- ナビゲーションと AI: EQS のメモリチェック、Recast のタイル生成でのメモリ破壊の修正、`RunNavProjection` の高速化。

### アニメーション

- PUMA プラグインにアニムワーピングのノードを導入（第 1 段階）。
- `ComputeRequiredBones` の高速化、スケルタルメッシュのリダクションでの属性補間の改善、非同期アニメーション圧縮中の
  ゲームスレッドのスタッターの削減。

### エディタとワークフロー

- ツールチップとプロパティのウィジェットを必要時に生成、コンテンツソースの更新の高速化、コンテキストメニューの
  高速化、ウィンドウメニューのヒッチの解消、アセットのサムネイルがアセット全体を読み込まないように、起動時に
  カルチャーデータを事前読み込みしないように変更。
- 出力ログのコンソール向けの手動オートコンプリートコマンド。カラーテーマビューアー、アウトライナー、UMG の修正。
- PIE 中のエディタワールドのシーンのパージを UE5 から導入。

### コア、メモリ、読み込み

- Windows の既定のアロケーターを mimalloc に変更。
- アセットレジストリ、リンカー、パッケージ読み込みの最適化。`TSet` / `TMap` が縮小時にメモリを解放。メッシュ描画
  コマンドの余剰領域を回収。`FUObjectHashTables` のアウター用ハッシュを圧縮。
- 本物の `FXxHash64` の実装。DDC からミップを取得する際にテクスチャストリーミングがゲームスレッドを止めなくなり、
  非同期テクスチャコンパイルを既定で有効化。

### 物理

- クロスアクターの生成を高速化（平均 8.5 ms から 5.6 ms）、複雑なスイープがバックフェースカリングを考慮、AABB ツリーの
  ブロードフェーズでソート済み挿入、コリジョンメッシュ生成時の割り当てを削減。

### ツールチェーンとプラットフォーム

- Visual Studio 2026 18.9.1（MSVC 14.51）と Windows SDK 10.0.26100、Clang 11 のツールチェーン対応、Windows での
  Clang 静的解析。
- 特に遅いコンパイル単位の時間短縮と、最適化なしで 2 GB に達していた共有 PCH の削除。
- TressFX プラグインと `UnrealTargetPlatform` から HTML5 を削除。`TraceDataFilters` を既定で無効化。
- リリース後: Windows に影響を与えない macOS / Xcode 26 への移植、Xcode 26 の診断の引き下げ、TressFX のジオメトリ
  シェーダー対応チェックのガード、Linux 専用サーバー向けプラグインの更新、そして VS 2026 / MSVC 14.51 向けの
  セットアップスクリプトとソースビルドのストリップオプション。

## リリース後のメンテナンス

公開ブランチには 8 月 24 日以降も修正が加えられました。

| 日付 | 変更内容 |
|---|---|
| 8 月 25 日 | DOF のわずかなピンボケ（SOF）の履歴棄却を任意に。`r.DOF.TAA.CoCBilateralFilterStrength` を追加 |
| 8 月 25 日 | UE4 スタイルの UI アイコンバッジをオプトインで復元 |
| 8 月 26 日 | TressFX と SSGI の改善、VS 2026 / MSVC 14.51 向けセットアップスクリプト、Linux 専用サーバー向けプラグイン |
| 8 月 27〜28 日 | ソースビルドのストリップオプション、ランドスケープのチェックの更新 |
| 8 月 29 日 | DLSS NGX 310.7.129、XeSS 3.1.0 のガードの修正、macOS / Xcode 26 への移植 |
| 9 月 9 日 | GAS デバッガーとエンジンのマテリアルの更新 |
| 10 月 2 日 | 上流の Epic `4.27-plus` をマージ: Xcode 27 対応、Clang 21 の警告の修正、macOS エディタの修正 |

## アップグレード時の注意点

- **ツールチェーン:** このリリースは Visual Studio 2026 18.9.1（MSVC 14.51）と Windows SDK 10.0.26100 で検証して
  います。リリースブランチの更新済みセットアップスクリプトを使用してください。
  [ツールチェーン要件](Toolchain-Requirements.md) を参照してください。
- **アロケーター:** Windows の既定のアロケーターが TBB から mimalloc に変わりました。独自のアロケーターを固定している
  プロジェクトは設定を見直してください。
- **コンパイル時の機能:** UE5 のローカル露出（`VITE_UE5_POSTPROCESSING`）は既定でコンパイルされます。ベントノーマル
  によるスペキュラーオクルージョン（`VITE_SPECULAR_OCCLUSION`）は、ビルド時に有効にしない限り無効です。
  [コンパイル時スイッチ](Compile-Time-Switches.md) を参照してください。
- **レイトレーシング:** ランドスケープのグラスは、既定ではレイトレーシングのシーンに含まれなくなりました。

<!-- BEGIN GENERATED COMMIT RECORD -->

## 全コミット履歴 {id="commit-history"}

ブランチ: [`ueVite26-AugustMajor-release`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/tree/ueVite26-AugustMajor-release)

### 領域別のコミット数

| 領域 | コミット数 |
|---|---:|
| レンダリング | 105 |
| エディタとワークフロー | 69 |
| コアとパフォーマンス | 69 |
| ゲームプレイフレームワーク | 48 |
| ツールチェーンとプラットフォーム | 45 |
| その他 | 28 |
| レイトレーシングと GI | 27 |
| アニメーション | 12 |
| アップスケーリングとアンチエイリアシング | 11 |
| 物理 | 11 |
| プラグインとメディア | 10 |
| ヘア | 3 |

### 公開リリースブランチ — 18 件 {collapsible="true" default-state="collapsed"}

18 件のコミット（マージコミット 2 件は表から除外）。

| 日付 | コミット | 作成者 | 変更内容 |
|---|---|---|---|
| 2026-09-09 | [`52ce867d8d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/52ce867d8d0d15244eb9e64ec05ba5ff0b31f6ba) | RedPixel | GAS Debugger, and Engine Mat updates |
| 2026-09-04 | [`14106a0cd7`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/14106a0cd70aa3f76cfac182d989bc458126cd8b) | Carlo V. | Update Bat Instructions README.md |
| 2026-08-29 | [`8a54a7e49e`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8a54a7e49e981cf755f687293d3c7a2ecffff924) | RedPixel | MacToolChain: apply the Xcode 26 diagnostic downgrades to every module |
| 2026-08-29 | [`428d4221da`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/428d4221dabd8ef6c468ecacec1499f595d28cc1) | RedPixel | TressFX: restore the geometry-shader capability guards the Mac port dropped |
| 2026-08-29 | [`21c996fae4`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/21c996fae40f39a62219837a1097579f5074dcff) | Tung Nguyen | Port macOS / Xcode 26 build to ueVite26-AugustMajor-release; Windows untouched |
| 2026-08-29 | [`979d793bbd`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/979d793bbde28da2e79a17a51ae6cb4d689939a8) | Tung Nguyen | DLSS RR: document preset F as the DLSS 4.5 model, not a dead slot |
| 2026-08-29 | [`1baa3d0232`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1baa3d023222121603254cf3c61b83aba121f931) | Tung Nguyen | XeSS 3.1.0: fix the temporal-upscale guard that never installs XeSS on UE4.27 |
| 2026-08-29 | [`7b2e56f81f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/7b2e56f81f105a1770796b8ed875071130145a78) | Tung Nguyen | XeSS 3.1.0: restore the UE4.27 XeFG/XeLL stand-down guards |
| 2026-08-29 | [`ee9a5e1781`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ee9a5e17812f6042e50e613257922b8dadcbac64) | Tung Nguyen | DLSS: update NGX runtime DLLs to 310.7.129 |
| 2026-08-28 | [`8b50fa6b36`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8b50fa6b36b74bc2d425e308f7e383132e70a876) | RedPixel | Landscape check Update |
| 2026-08-27 | [`69b64b9ff9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/69b64b9ff9fad3a4f4b0c9375e5a3d85743e3e54) | RedPixel | \[Setup\] Updated Bats: Added strip options to Source Build |
| 2026-08-26 | [`57b98cda3a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/57b98cda3a79b694f3d9118475b1832770aaf5e8) | RedPixel | \[Linux\] Plugins updated for Linux Dedicated Server Builds |
| 2026-08-26 | [`814021ef2b`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/814021ef2bce886532e55fd1cf60a97ee810d25f) | RedPixel | \[Setup\] Updated Vite Bats for VS26 and MSVC 14.51 |
| 2026-08-26 | [`50ca73f6ac`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/50ca73f6ace628242b98aeae804368ab199c29fe) | RedPixel | \[Rendering\] TressFX and SSGI improvements |
| 2026-08-25 | [`764a54cd8a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/764a54cd8a9195eaa4f8e2fe92654c7bf01cfd33) | RedPixel | \[Editor\] Opt In UE4 UI Icon Badges |
| 2026-08-25 | [`5ef2ad6b91`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/5ef2ad6b9101f7d90764351f0db20c95438f5634) | RedPixel | \[DOF\] Make the slight-out-of-focus (SOF) history rejection boost optional, as this introduces noise in areas with high variance (e.g. bright specular). |
| 2026-08-25 | [`bcef2e4bbf`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bcef2e4bbf3226a0ae025be89baac672b625cff4) | RedPixel | Added a cvar to turn off the TAA bilateral filter (r.DOF.TAA.CoCBilateralFilterStrength). |
| 2026-08-24 | [`e6c356946d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e6c356946d6d17631c05f53af5e2a7308f60a091) | RedPixel | \[Release\] August Major |

### 内部ステージング（1 コミットとして公開） — 420 件 {collapsible="true" default-state="collapsed"}

<note>
<p>
これらのコミットは内部ステージングブランチ <code>ueVite26-AugustMajor-staging-9</code> で開発・レビューされ、公開ブランチには 1 つのリリースコミットとして反映されました。記録として掲載していますが、短縮ハッシュは内部リポジトリのものであり、リンクはありません。
</p>
</note>

420 件のコミット（マージコミット 14 件は表から除外）。

| 日付 | コミット | 作成者 | 変更内容 |
|---|---|---|---|
| 2026-08-24 | `cb6e64c2f9` | RedPixel | \[Re-Apply\] XeFG: enable frame-gen on UE4.27 via MIN path (0x1) |
| 2026-08-24 | `70db0cef55` | RedPixel | \[Plugin\] Intel XeSS Updated to 3.1.0 |
| 2026-08-24 | `9807723f25` | RedPixel | Subpixel Morphological Anti-Aliasing |
| 2026-08-24 | `2afb3c7b18` | sebastien hillaire | Fixed skylight show flag not working properly for stationary skylight. |
| 2026-08-24 | `d940240fee` | Kenzo Terelst | Make sure buffer SRV is removed from state cache when performing upload buffer copy to make sure it's gets transitioned to SRV again on next usage. If a resource is updated while still being bound, a… |
| 2026-08-24 | `7c2f6e8851` | Kenzo Terelst | Restore UAV barriers on every transition to UAV when using internal transitions because UAV-&gt;SRV and then SRV-&gt;UAV would skip the UAV barrier and have zero synchronization because UAV-&gt;SRV was just s… |
| 2026-08-24 | `2cfa9fc7e7` | RedPixel | Cast Fix to HierarchicalInstancedStaticMesh.cpp after UE5.3 backport 1b37162 |
| 2026-08-24 | `49d030c6ba` | RedPixel | \[Toolchain\] UE Vite26 August compiling on VS 18.9.1 (\_MSC\_VER 1951) and Windows SDK (10.0.26100) for Windows 11 |
| 2026-08-24 | `7e7304d81b` | RedPixel | \[Plugins\] Removed HTML5 platform from TressFX and TraceDataFilters is now disabled by default |
| 2026-08-23 | `0794d42b5d` | RedPixel | Implement a real FXxHash64, backported from ueVite-Internal@5.4 (scoped) |
| 2026-08-23 | `e4f62bbbc2` | RedPixel | Fix: revert SBT hashing from FXxHash64 back to CityHash64 (xxHash is a non-functional stub in this fork) |
| 2026-08-23 | `083966429a` | RedPixel | Fix: restore ray-traced volumetric fog light path when shadow quality is 0 |
| 2026-08-23 | `d7e233bbbd` | RedPixel | \[Rendering\] Added Jimenez 2016 bent-normal specular occlusion gated by VITE\_SPECULAR\_OCCLUSION |
| 2026-08-23 | `f49f9e45d7` | chris kulla | RHI: Avoid re-allocating the OutData array in RHIRead\*SurfaceData when possible |
| 2026-08-23 | `633f08c658` | jian ru | Do not report materials supporting dithered LOD transition as masked for non-shadow passes unless stencil dithering is disabled or the VF doesn't support null pixel shader. |
| 2026-08-23 | `7be6a75433` | kenzo terelst | - Clamp MinLOD to GetCurrentFirstLODIdx\_RenderThread during setup of dynamic draw elements to take mesh streaming into account as well - Add cvar to force end cull distance for HISM instances (defaul… |
| 2026-08-23 | `072f266a93` | jason hoerner | Slack memory savings for FCachedMeshDrawCommandInfo. Do an explicit "Shrink" instead of "bAllowShrinking" which shrinks conditionally. Arrays with 32 or 64 reserved elements weren't ever being shrunk… |
| 2026-08-23 | `25fc80a913` | Yuriy ODonnell | Several micro-optimizations for D3D12 shader binding table management |
| 2026-08-23 | `3c9bb80861` | tiago costa | Prevent false sharing when filling SBT on D3D12 RHI. - all worker threads were updating bIsDirty. - instead update bIsDirty once after bindings are written. |
| 2026-08-23 | `014b5debbb` | zach bethel | HISM - GDME improvement - No need to create unfirom buffer if we have empty LOD array. - No need to allocate mesh batch if we have empty section. |
| 2026-08-23 | `ceecd77c05` | dmitriy dyomin | Avoid re-creating whole rendering state for a primitive when MaxDrawDistance or InstanceCullDistance has changed |
| 2026-08-23 | `24bd497904` | RedPixel | \[Backport\] f6d95da Match Original Indentation |
| 2024-06-12 | `7914da4f62` | RedPixel | \[UE 5.1\] Port safe Gameplay Ability System fixes and WaitGameplayTagQuery |
| 2024-06-12 | `ce8cc8166b` | RedPixel | \[UE 5.2\] Port Trace Data Filtering Insights fixes without AllowList rename |
| 2024-06-12 | `ab26271ce7` | Ivan Belyavtsev | \[NvRTX 5.0\] Changed Get LatencyInMs methods to fetch meaningful values from LatencyMarkerModule |
| 2024-06-12 | `e9d89a659e` | Evan Hart | \[NvRTX 5.0\] Fix sampled lighting to obey disabling shadows |
| 2024-06-12 | `4bae6c66ff` | Evan Hart | \[NvRTX 5.0\] Change ReLAX diffuse fast history default from 0 to 8 |
| 2024-06-12 | `601002eaa7` | Evan Hart | \[NvRTX 5.0\] Change ReGIR computation method |
| 2024-06-12 | `5b2600678b` | Evan Hart | \[NvRTX 5.0\] Fix some scenes with corrupted denoising |
| 2025-06-12 | `dce0f0c572` | tiago costa | \[Auto Exposure\] Fix exposure compensation being incorrectly evaluated when Method = Histogram and AutoExposureMinBrightness &gt;= AutoExposureMaxBrightness. - always need to generate histogram to calcul… |
| 2025-06-02 | `7263d5453a` | tiago costa | \[Eye Adaptation\] Fix incorrect eye adaptation when sequence ends. - View.bCameraCut is not set in this case so also need to check View.bPrevTransformsReset. |
| 2025-03-11 | `abe27d1e60` | tiago costa | Modified FMaterialResource::IsDitherMasked() to also check IsMasked(). - fixes issues with codepaths checking IsDitherMasked() without explictly checking IsMasked() (eg: BlendModeToRayTracingInstance… |
| 2024-12-16 | `6d619b22dc` | tiago costa | Fix AddVisualizeBufferPass(...) not taking OutputViewport.Rect.Min into account. |
| 2024-09-02 | `8ce43808a2` | tiago costa | Fix multiple definitions of asfloat(...) due to non-static definition in HaltonUtilities.cpp |
| 2023-04-26 | `276e693cce` | tiago costa | Modified check in FUniqueNetIdRepl::ImportTextItem to prevent cooking errors in some projects. |
| 2022-11-17 | `707d53bdbc` | eric renaudhoude | Post-processing: Reconnect r.LUT.Size with the combined LUT/tonemapping texture size. |
| 2024-03-26 | `fc541b3568` | arciel rekman | Fix leaking shader code preloading entries. |
| 2024-06-12 | `71cc2b9192` | jimmy smith | Fix for rare condition with SoundWave GC and playing Wave. #rb phil.popp #jira UE-214884 |
| 2023-02-23 | `8c50729355` | Aris Theophanidis | Fix memory corruption from FRecastTileGenerator::MarkDynamicAreas #rb Yoan.StAmant #rb Mieszko.Zielinski #preflight 63f7a96e9009dd70d73fe364 |
| 2023-08-14 | `9cecb0fd6d` | mickael gilabert | Fix GOcclusionRandomStream OOB due to CurrentSample access not being thread safe |
| 2024-06-12 | `1b1a31a6fd` | chris tchou | Fix for the landscape bounds calculation, that can cause perf regressions and/or very fast visibility flashing (i.e. landscape draws every other frame). |
| 2026-08-22 | `bb273719e7` | RedPixel | \[Adapted to Keep NVIDIA OP on Compile Time Switch\] Fix screen space denoising shaders on AMD GPUs by removing CONFIG\_VGPR\_FREE\_SAMPLE\_TRACK\_ID optimization |
| 2026-08-22 | `a798e16828` | RedPixel | \[RT\] Adjusted RT Shadows Defaults |
| 2026-08-22 | `bf5bce35e0` | RedPixel | \[RT\] Adjusted RTAO Defaults |
| 2026-08-22 | `df090b4fa1` | RedPixel | \[RT\] RT Deferred Reflections: Added Sky cubemap on gather miss, plus foliage/SSS/skin extra diffuse on hits |
| 2026-08-22 | `daa619f5f2` | RedPixel | \[RT\] Updated RT Deferred Reflections Optimization setup and updated default settings |
| 2026-08-22 | `f0789972d9` | Lars Thießen | Removed pre-loading of all culture data from editor start |
| 2026-08-22 | `cca18205d4` | Lars Thießen | Changed FMessageLogListingViewModel to only refresh list when it's actually required |
| 2026-08-22 | `b012fec634` | Lars Thießen | Fixed widgets not being available for explicit navigation |
| 2026-08-22 | `8aa50ae5e9` | phillip kavan | \[UE\] Blueprint "enable/disable" node submenu options moved out of experimental. |
| 2026-08-22 | `f13162c9bf` | Marvelius | PR #14371: Removed redundant function call, speeding up the automatic asset reimporter by 2x |
| 2026-08-22 | `c6e2fd23c2` | daren cheng | Only create property &amp; text tooltip widgets on demand to speed up editor startups. Saves up to ~400ms when switching between states in state centric view. - Add SDeferredToolTip to wrap any previous… |
| 2026-08-22 | `f9c389bb7e` | Marvelius | PR #13849: Changed refresh of content sources to only happen if needed to speed up editor launch |
| 2026-08-22 | `93be99dc2f` | sebastien hillaire | Fixed translucent material using alpha to coverage when it is in fact disabled on the material. MATERIAL\_USE\_ALPHA\_TO\_COVERAGE was not used to check for usage. |
| 2026-08-22 | `250fa8b3fc` | chris kulla | Ray Traced Shadows: Implement support for Source Length |
| 2026-08-22 | `1888b6a7f7` | marcussvensson92 | PR #9905: Option to disable reflections and sky contribution in reflection captures (Contributed by marcussvensson92) |
| 2026-08-22 | `b2ad6078cb` | kevin ortegren | Moving debug declaration to work in all AO\_SAMPLE\_QUALITY cases |
| 2026-08-22 | `4dd16420fc` | tiago costa | Don't include objects with "Cast Shadow" disabled in Distance Field Shadows - Added bCastShadow flag to FDFObjectBounds - Filter objects in CullObjectsForShadowCS |
| 2026-08-22 | `9bf9c4eb2a` | RedPixel | Fix newlines in ConsoleSettings.cpp smashed by PowerShell string conversion. |
| 2026-08-22 | `3b4b39626c` | ben hoffman | Add ConsoleSettings.cpp for manual auto-complete commands. |
| 2026-08-22 | `2e1773e1ce` | ben hoffman | Add support for manual auto-complete commands in the Output Log console |
| 2026-08-23 | `07c2a5fd21` | tuhoiisa | Clang 11 toolchain support and compatibility fixes |
| 2026-08-22 | `0b7c944f00` | Phillip Kavan | Allow script execution to bypass development-only nodes in a Blueprint function graph when a project is configured to compile them out at cook time. |
| 2026-08-22 | `1745bf6e17` | guillaume abadie | Fixes SSR alignment issues |
| 2026-08-22 | `992b026c15` | zahra nikbakht | UMG: ensure we do the widget rename operation from the details panel name textbox if the name actually changed. |
| 2026-08-22 | `2ff495f505` | eric renaudhoude | SceneCapture: Added tonemapper and post-process materials to visible scene capture show flags. |
| 2026-08-22 | `4b850fe4ea` | steve robb | Improved Clamp() codegen. |
| 2026-08-22 | `60caa55de4` | tiago costa | Fix issues with stationary light when r.AllowStaticLighting is disabled. - Renderer will treat stationary lights as movable in projects with static lighting disabled. - Don't render "Preview" indicat… |
| 2026-08-22 | `16cc2f84ff` | tiago costa | Fix bug in GTAO when there's a camera cut. |
| 2026-08-22 | `7f7c1c6649` | geoff evans | Windows Splash Updates |
| 2026-08-22 | `cdddb0b10f` | Ola Olsson | Fix missing shadow casting from material instance when setting Cast Shadow As Masked flag on parent material. - Superset of changes in PR #6863 |
| 2026-08-22 | `36b4b7391d` | Sebastien Hillaire | Fixed bad translucent shadow on translucent surfaces. UDN https://epicgames.lightning.force.com/lightning/r/Case/5004z00001dnA8jAAE/view #rb Ola.Olsson #preflight none |
| 2026-08-22 | `f18b1c034d` | stu mckenna | - Fix for translucent shadows not being rendered |
| 2026-08-22 | `aac4376b6b` | stefan-zimecki | PR #8796: Implemented Key parameter for PrintString and PrintText nodes (Contributed by stefan-zimecki) |
| 2026-08-22 | `c5bc981b0b` | matt peters | FReferenceFinder: Optimize searching of objects that have 100k references. |
| 2026-08-22 | `56da326e82` | aris theophanidis | Fix editor performance issue caused by navigation building even if there is nowhere to build navigation |
| 2026-08-22 | `d332ca29da` | Andriy Tylychko | UTexture::UpdateResource(): combined 3 RT tasks into one to reduce the number of tasks spike during loading, both for perf and memory usage |
| 2026-08-22 | `a5bb15dccd` | dan oconnor | Optimize UUserDefinedStruct::InitializeStruct by avoiding redundant operations for STRUCT\_IsPlainOldData instances |
| 2026-08-22 | `f7f5cae805` | andriy tylychko | minor optim to avoid needless copies of TRefCountPtr in IoDispatcher |
| 2026-08-22 | `1d93bd7f00` | yuriy odonnell | Add r.RayTracing.Geometry.InstancedStaticMeshes.MinLOD CVar |
| 2026-08-22 | `2c47cf7488` | aleksander netzel | Make r.RayTracing.Shadows.EnableMaterials render thread safe |
| 2026-08-22 | `81ef2ba229` | aris theophanidis | Optimization to UHierarchicalInstancedStaticMeshComponent::GetOverlappingBoxTransforms() |
| 2026-08-22 | `b64c8c15fb` | mickael gilabert | Skip D3D12 drawcall in RHIDrawIndexedPrimitive and RHIDrawIndexedPrimitiveIndirect if IB is empty or underlying resource is null |
| 2026-08-22 | `b6c6d17b64` | yohann dossantos | Fixed Tooltips appearing over foreground programs |
| 2026-08-22 | `06ac37b11e` | graham wihlidal | Significant optimization to CheckMaterialUsage\_Concurrent - keep track of cache misses on the render/worker threads, and only send a single check packet back to the game thread when a miss for a mate… |
| 2026-08-22 | `682252066d` | Andriy Tylychko | added defaulted move constructor/operator= for TMulticastDelegate for a minor optimisation, as otherwise copy constructor/operator= are used and allocate memory |
| 2026-08-22 | `9a52beb3f7` | mihnea balta | PR #10117: Remove unnecessary copying of FRayTracingDynamicGeometryUpdateParams |
| 2026-08-22 | `ae898658a3` | chris kulla | RayTracing: Objects casting hidden shadows or affecting indirect while hidden were not visible to ray tracing |
| 2026-08-22 | `5147d1cc4f` | Nick Darnell | Editor Performance - Fixing a long standing issue with asset thumbnails, they've been loading the assets for a pretty long time now, because of the thumbnail editing mode. Note that thumbnail editing… |
| 2026-08-22 | `1130e89739` | aleksander netzel | InstancedStaticMesh - handle hidden materials for ray tracing in the same way as for StaticMesh |
| 2026-08-22 | `b7141da084` | chris kulla | Ray Tracing: Fix potential preformance issue with invalid shadow rays being traced |
| 2026-08-22 | `4ba1f6f8f7` | logan buchy | Performance improvement to opening Context Menu and other operations looking up AssetTypeActions |
| 2026-08-22 | `5d1289f228` | yohann dossantos | Optimize UpdateTooltip |
| 2026-08-22 | `7c87973ff3` | yuriy odonnell | Immediately release static mesh offline ray tracing data if ray tracing is known to be disabled at run-time due to user settings |
| 2026-08-22 | `a2794edde0` | mateo egey | Added bool attribute to SDropTarget to stop AllowDrop function call from executing every frame for overlay visibility |
| 2026-08-22 | `a8287eaf32` | yuriy odonnell | Use a RW lock to protect GShaderHashCache instead of a critical section to reduce lock contention |
| 2026-08-21 | `02a361f61c` | Patrick Laflamme | Prevent loading all debug symbols when resolving callstacks around module changes |
| 2026-08-21 | `49f2dcf83f` | Benn Gallagher | Fixed performance issues in camera rig rail actor and made spline mesh component skip unchanged updates |
| 2026-08-21 | `511797bb12` | krzysztof narkowicz | Ray tracing - disable adding Landscape Grass to ray tracing scene by default |
| 2026-08-21 | `3fa569edef` | Patrick Laflamme | Prevent loading all debug symbols when resolving callstacks around module changes |
| 2026-08-21 | `e656fac2bb` | Benn Gallagher | Fixed performance issues in camera rig rail actor and made spline mesh component skip unchanged updates |
| 2026-08-21 | `c71d57bfe8` | bob tellez | #UE AssembleTokenStreams optimization. When ProcessNewlyLoadedUObjects, only assemble token streams for the new classes that showed up duing the process |
| 2026-08-21 | `706bc68faa` | kenzo terelst | Check for nullptr before trying to destroy buddy allocator during shutdown |
| 2026-08-21 | `cd921a832b` | sebastien hillaire | Volumetric cloud - added tracing max distance mode |
| 2026-08-21 | `f7f52a01b5` | pj kack | TSet &amp; TMap: release dynamic hash allocations when shrinking |
| 2026-08-21 | `873008003a` | tim doerries | Fix for vulnerability caused by possible integer overflow in UVolumeTexture::UpdateSourceFromSourceTexture(). |
| 2026-08-21 | `517aeffb8d` | vincent robert | Broad Phase AABBTree optimization: Simple sorted insertion in AABBTree |
| 2026-08-21 | `1d60bfc708` | tyler staples | Only set SImage MouseDown and DoubleClick event if bound. |
| 2026-08-21 | `56a39a9fdd` | thomas ross | Prevent our PipelineCaches directories from being trimmed in pak memory optimization |
| 2026-08-21 | `b68fd5595d` | Ethan | Fixed SSAO with forward rendering and static skylight |
| 2026-08-21 | `98e57b9ea4` | Tiantian Xie | Allow light functions in reflection captures |
| 2026-08-21 | `f0bd718663` | jeanfrancois dube | Avoid flushing async loads for visibility-only streaming flushes |
| 2026-08-21 | `30108dbddb` | richard malo | Respect cumulative level streaming frame-time limits |
| 2026-08-21 | `3631c72731` | sebastien lussier | Hide full-visibility streaming levels atomically |
| 2026-08-21 | `277ce5b044` | aurel cordonnier | Skip the scene light loop when shadows are disabled |
| 2026-08-21 | `2fa6fe695b` | Krzysztof Narkowicz | Require cast shadow for cast hidden shadow |
| 2026-08-21 | `3604ebdc6a` | Josie Yang | Provide custom context menu search criteria for material editor |
| 2026-08-21 | `5eeeef4637` | ben hoffman | Prefer context-menu actions with matching container types |
| 2026-08-21 | `e1042e4ea7` | ben zeigler | Tweaks to blueprint editor context menu |
| 2026-08-21 | `3ff830b94f` | Yuriy ODonnell | Complete ray tracing reflection RTPSO gating |
| 2026-08-21 | `68314a76fa` | Devin Doucette | Fixed non-deterministic texture cubes from the reflection capture component |
| 2026-08-21 | `c992b764b8` | Ola Olsson | Fix Gather4 offsets in shadow map filtering (off-by half error) |
| 2026-08-21 | `3292901efa` | Michal Valient | Backport of extra utility functions to Vector.h and Box.h from 5.0 Early Access |
| 2026-08-21 | `5884cc9f55` | tuhoiisa | Backport UE5.0 local exposure renderer passes and post process settings |
| 2026-08-21 | `f5a91a1fdb` | tuhoiisa | Backport UE5.0 local exposure shaders behind VITE\_UE5\_POSTPROCESSING |
| 2026-08-21 | `d182e37dc0` | tuhoiisa | Modified UWorld::PurgeScene to internally flush Slate scene ptr cache instead of SetPlayInEditorWorld to avoid repeated calls per frame in some cases. |
| 2026-08-21 | `8a4bdc1045` | tuhoiisa | Purge editor world scene during PIE |
| 2026-08-21 | `db87265851` | tuhoiisa | Backport editor world scene purge from UE5 |
| 2026-08-21 | `ed06c71943` | Tony Wong | MediaCompositing: Fixed media cache display being offset when track is offset from the start. #JIRA: UE-112192 #review-18333345 @max.chen #rb max.chen #rnx |
| 2026-08-21 | `b187c06d8b` | Max Chen | Media: Fix timing issues when evaluating with sequences with different underlying tick resolutions. Convert FFrameTime to seconds and then to ticks per second. |
| 2026-08-21 | `12ccd2522d` | aaron mcleran | Allowing procedural sound waves (and synth components) have more than 2 channels |
| 2026-08-21 | `8d0c4807fe` | Frank Gigliotti | 'UAttributeSet::PostAttributeChange' is no longer const. This allows the ability set to update internal state and it matches the call to 'PreAttributeChange'. |
| 2026-08-21 | `839a6b378c` | brian bekich | Fix for compiler dependent deprecation warnings |
| 2026-08-20 | `361ed9f420` | Frank Gigliotti | ShowDebug AbilitySystem options; |
| 2026-08-20 | `01d65fd0f2` | Frank Gigliotti | Added PostAttributeChange() and PostAttributeBaseChange() callbacks to UAttributeSet. These callbacks mirror the existing pre-change callbacks. |
| 2026-08-20 | `1e400cf6cb` | Mieszko Zielinski | Added AddLooseGameplayTags and RemoveLooseGameplayTags functions to UAbilitySystemBlueprintLibrary |
| 2026-08-20 | `bf20189b44` | Frank Gigliotti | Updated FGameplayTagBlueprintPropertyMap to not initialize again if the owner and ability system hasn't changed. |
| 2026-08-20 | `f122f975ba` | ben zeigler | Fix ensure in abilities system if an ASC is registered and unregistered without being initialized, which can happen during level streaming #rb none |
| 2026-08-20 | `98548b646b` | ben zeigler | Add safety checks for FGameplayTagBlueprintPropertyMap to avoid crashing on trashed memory if it was unable to unregister or was copied incorrectly Add ApplyCurrentTags to apply any changes that happ… |
| 2026-08-20 | `65bd3c8ba9` | ben zeigler | #jira UE-115636 Static analysis fix #rb none |
| 2026-08-20 | `1f2a40ce9e` | BillEliot | PR #7991: Bugfix GameplayAbilityTargetActor\_Trace.cpp - \[The replicated location of AGameplayAbilityTargetActor\_GroundTrace in the simulated proxy is incorrect\] (Contributed by BillEliot) |
| 2026-08-20 | `61d25feb90` | brian bekich | Removing direct package map reference from FPredictionKey to avoid holding references to old connections |
| 2026-08-20 | `cd969ea616` | michael noland | Guarded a potential crash in UGameplayAbility::GetAbilityLevel if the ASC pointed to by the actor info has been destroyed \[CODEREVIEW\] fred.kimberley #jira UE-118411 |
| 2026-08-20 | `d9acb7c1e5` | fred kimberley | Fix a bug where ability tasks do not broadcast their end task delegates when the ability ends. |
| 2026-08-20 | `c27358aa16` | justin hare | Ability system component cleanup: removed no-longer-used actor info field |
| 2026-08-20 | `a5e1a6a8fc` | max chen | Sequencer: Missing transactionals, which could cause null sections on undo. These haven't caused any specific problems but there was one in Media Track that was missing recently that caused a crash f… |
| 2026-08-20 | `2591d90128` | justin hare | Fixed issue where global ability task count tracking was double-counting, resulting in errors when we were only halfway to the limit |
| 2026-08-20 | `9aaf3f4d1f` | david ratti | Ability System Fix GE GCs playing when bRequireModifierSuccessToTriggerCues=true but all execution modifiers fail to apply. Previously this flag was only honored for GE modifiers and not modifiers th… |
| 2026-08-20 | `9f9a75bd7b` | david ratti | Ability System -Remove unnecessary call to AddActors in FGameplayEffectContext::Duplicate which was causing duplicate entries of the actors to be created (heh) |
| 2026-08-20 | `166fdea4a3` | Michael Noland | Ability System: Made an access violation crash when replicating an attribute set on an improperly set up ability system component more explicit (e.g., when the target actor doesn't implement GetAbili… |
| 2026-08-20 | `ab3848a1fd` | aziogroup | Fix for ASC montage playback not being fully replicated on simulated proxies under certain circumstances. This could happen if multple montages are played in rapid succession before replicated animti… |
| 2026-08-20 | `b482ddab5e` | taylor driggs | Force replication after a gameplay cue is removed from the AbilitySystemComponent. This ensures GC removals are replicated to clients during Mixed and Minimal replication modes. |
| 2026-08-20 | `7cc477cc59` | billy bramer | Ability System - Fix bug wherein DynamicAssetTags would never be included in aggregator calculations; Deprecate public access to DynamicAssetTags &amp; have API that auto-includes them within source capt… |
| 2026-08-20 | `5ff5b97ccf` | justin hare | Fixes issue where property redirector was not respected on an Gameplay Abilities AttributeSet class on BP graph pins, causing saved data to show as the type's default value. |
| 2026-08-20 | `3a88dba947` | billy bramer | Ability System - Make UAbilitySystemComponent::GetAggregatedStackCount const |
| 2026-08-20 | `24ffd4ffe8` | justin hare | Disallowed function calls on non-instanced abilities no longer halt the program. Converted checks to ensures where reasonable and improved messaging. Pulled macro from sample game into Gameplay Abili… |
| 2026-08-20 | `5ce5ac2eab` | charles lefebvre | FScalableFloatDetails: Dynamic preview levels based on the time range of the curve #rb ben.zeigler #rnx |
| 2026-08-20 | `c190e71e40` | ben zeigler | Add End Ability Locally function to the generic gameplay ability, this is needed for predicted abilities with animations where you don't want the server ability to end early and miss a callback Also… |
| 2026-08-20 | `b291c2488a` | justin hare | Fixing crash when showing 'AbilitySystem' debug info from the command line when a not-fully-initialized ASC is in play |
| 2026-08-20 | `0bdf473524` | ben hoffman | Allow game feature plugins to modify the gameplay cue paths |
| 2026-08-20 | `62d63c7e3e` | Michael Noland | Removed some log spam about updating the gameplay tag tree #jira UE-142878 #preflight 620c8fe36202a22eedd389b0 |
| 2026-08-20 | `05223e2b6e` | Michael Noland | Fix for ensures when adding duplicate OnEndPlayDelegates |
| 2026-08-20 | `8efdf775e3` | tuhoiisa | Fix duplicated if keyword in velocity pass gating |
| 2026-08-19 | `7be1e11b02` | tuhoiisa | Adapt 5.1 optimizations to 4.27 Core APIs |
| 2026-08-19 | `fe157e2e04` | matt peters | Optimize FCoreRedirects::GetMatchingRedirects since it is showing up as a moderately high cost in cooks (38s out of 870s in CitySample). #rb Stefan.Boberg #rnx #preflight 621e42cbca28c556342bd1d9 |
| 2026-08-19 | `2f5596f91f` | daniel broder | Exposed functions for fetching a scalar material parameter index and then setting the parameters by index to blueprint in order to be able to optimize cases with extreme amounts of material parameter… |
| 2026-08-19 | `7222d4d432` | sarah noonan | Optimisation - Add option to not update the position of widgets within the SWorldWidgetScreenLayer if they are not visible. Prevents invalidating all the widgets in the layer to update widgets that a… |
| 2026-08-19 | `8f0d474904` | johan torp | Kill FGenericWidePlatformString::Strncmp, which reads one character out of bounds for unterminated strings, and fallback to my faster FGenericPlatform::Strncmp algorithm |
| 2026-08-19 | `8f00fc7323` | johan torp | AssetRegistry loading optimization, zero out less memory |
| 2026-08-19 | `3cbc1761e7` | ilya loshchinin | Optimized StaticDuplicateObject by pooling its temporary memory block allocation. Added FPooledLargeMemoryData that allows lockless access to temporary memory blocks. |
| 2026-08-19 | `9c79522f2f` | max chen | Anim: Remove stray PRAGMA\_DISABLE\_OPTIMIZATION |
| 2026-08-19 | `2952fef70d` | phillip kavan | Remove unnecessary overhead from FEdGraphPinReference::GetTypeHash(). |
| 2026-08-19 | `8453f35a34` | matt peters | AssetRegistryState: fix EnumerateAssets to handle duplicates in Filter.ObjectPaths, and optimize the handling of duplicates using a bit for each filters rather than counting the number of passed filt… |
| 2026-08-19 | `291cfdd610` | ben zeigler | Fix ActorComponent to call PostEditChangeOwner on AssetData from PostEditChange instead of PostInitProperties. This will correctly update when making editor changes and is also a small performance im… |
| 2026-08-19 | `322fe051f2` | martin sevigny | Optimize code to avoid converting a White vertex color (ie no vertex color). Was making a significant difference in test on the Twinmotion stream. #rb: Richard.TalbotWatkin #preflight none |
| 2026-08-19 | `4e50d1010d` | jordan cristiano | Optimized BuildingFoundationPostSignificanceUnloadsFirst. Saves half the cost (25us on high end pc). |
| 2026-08-19 | `7ff1a1b02e` | benn gallagher | Chaos: Fix use-after-move in implicit unions. When building unions the object storage array was reserved by Objects.Num() however Objects had just been moved from. Due to ArrayNum getting set to zero… |
| 2026-08-19 | `f9ed187fd0` | louisphilippe seguin | CurlHttp \* Slightly optimized DebugCallback function \* Remove extra FString allocations by directly converting from ANSICHAR to TCHAR in the final FString. \* Don't create FStrings in CURLINFO\_HEADER\_… |
| 2026-08-19 | `8c7f1ea5db` | bryan sefcik | Removed "OptimizeCode = CodeOptimization.Never" from SoundFields. This setting created a 2.03 GB shared PCH file that was only used by this module. #preflight 62fe72073f75602b2f093732 |
| 2026-08-19 | `08e07ffeb3` | bryan sefcik | Updated OSCModulationMixing to not compile with optimizations off so it matches other modules that use Shared PCHs. This speeds up compile times and removes the need to have a 2.03 GB shared Engine P… |
| 2026-08-19 | `83b3e7c016` | bryan sefcik | Updated SoundCueTemplates to not compile with optimizations off so it matches other modules that use Shared PCHs. This speeds up compile times and removes the need to have a 2.03 GB shared Engine PCH. |
| 2026-08-19 | `2864a0b3e9` | bryan sefcik | Updated Spatialization to not compile with optimizations off so it matches other modules that use Shared PCHs. This speeds up compile times and removes the need to have a 2.03 GB shared Engine PCH. |
| 2026-08-19 | `96287eb9bd` | jordan cristiano | Removed csv stat for Exclusive/GameThread/ReplicateActor and added Exclusive/GameThread/ReplayReplicateActors. ReplayReplicateActors and ServerReplicateActors should add up to the total ReplicateActo… |
| 2026-08-19 | `08f685214d` | joe pribele | \[Engine\] added IsDefaultAsString to optimize and compare to default value |
| 2026-08-19 | `a2284ab1fc` | christopher waters | Allowing global constant buffer updates to be more dynamic. Removes the shadow data overhead from stages that aren't used in a context and also allows for global constant buffers larger than 4kb. |
| 2026-08-19 | `e2bc1e6443` | jeremy moore | Optimization for FVirtualTextureProducer::Release Accelerate lookup of tiles per producer in ForceUnlockAllTiles #rb jeanfrancois.dube #preflight 6179b6d14c74960001ea6bca #lockdown michal.valient |
| 2026-08-19 | `a9f4f35065` | danny couture | Optimize cook time and fix indeterminism in niagara curve generated textures by using content based guid |
| 2026-08-19 | `17f040154f` | Patrick Laflamme | Prevented adding non-existing directories to Python 'sys.path' - This makes Python a bit faster at startup (according to my benchmark) and reduce noise looking at the sys.path. |
| 2026-08-19 | `77198e7038` | Michael Galetzka | Build time optimization |
| 2026-08-19 | `b1e97026a5` | Anousack Kitisa | Added an additional topology check when importing GeometryCache without "Apply Constant Topology Optimizations" instead of assuming it changes every 64 frames. |
| 2026-08-19 | `4ee3bcbd8a` | rex hill | Optimize Window menu being opened incurring 1-5 second hitch. Reduced to 0.015 seconds. #jira UE-132066 #rb dave.belanger |
| 2026-08-19 | `bbdc4cf3ba` | Flo Schar | TakesCore now uses the SAVE\_Async flag to save its assets, leading to significantly faster saving times |
| 2026-08-19 | `a0de3c8ce6` | ggsharkmob | PR #8013: Optimization of USkeletalMeshComponent::ComputeRequiredBones() (Contributed by ggsharkmob) |
| 2026-08-19 | `3cb155f04a` | andrew ladenberger | Added GetHitchTimePercent(), mirroring HitchTimePercent in the csv report tool. |
| 2026-08-19 | `36f582bbdc` | matt peters | FAsyncPackage::FlushObjectLinkerCache: Optimize by calling FlushCache once per linker instead of once per object. #rb PJ.Kack #rnx |
| 2026-08-19 | `36d562f622` | gabriel pereyra | Exposure Post Processing: Made it so that if either AutoExposureSpeedUp and AutoExposureSpeedDown parameters are negative, then the speeds are considered invalid and we force ourselves to hit the tar… |
| 2026-08-19 | `f8a3da6dd8` | uriel doyon | Asset streaming : - New computation for the load order priority when LODs are streamed out. - Cleaned up MemoryUsed and TempMemoryUsed being passed along different functions (not required anymore) -… |
| 2026-08-19 | `8a9e83e538` | dan phillips | Optimization, don't empty and grow this array multiple times |
| 2026-08-19 | `4ef783ee16` | danny couture | Do not setup viewport for movie streaming if it is disabled - Prevent an unneeded render thread suspension from happening - Saves 1s when starting PIE and removes some hitches each time BlockTillLeve… |
| 2026-08-19 | `ec3d0d118c` | daniel lamb | Added support for generating optimized deltas for new online bpt enabled pc builds. |
| 2026-08-19 | `6e284426f4` | steve robb | Fix for optimized map and set properties serialization when there are no defaults and the container is already populated. |
| 2026-08-19 | `ec8fe73273` | jeanfrancois dube | Optimize FAssetRenameDataWithReferencers by changing an array with a set. Results for breaking a Level Instance with ~10K actors: ~810s down to ~256s. |
| 2026-08-19 | `f54bf5e655` | danny couture | Compilation time optimization - Disable codegen optims on extremely long function with lots of FORCEINLINE calls in it - 1m14s -&gt; 28.09s for NiagaraDataInterfaceHairStrands.cpp - 1m03s -&gt; 20.12s for… |
| 2026-08-19 | `fd89fe497b` | Jimmy Andrews | more direct / faster implementation of HasAttribute and RemoveAttribute in ManagedArrayCollection (directly use key in map, rather than linear searching for key) |
| 2026-08-19 | `11734914cf` | evgenii babinets | Optimized FTickTaskManager::RunTickGroup by ~45&#37; when the new tick set is empty. Constructing TSet::TIterator doesn't seem to be a trivial operation, as the object is 48 bytes and has nested bit-iter… |
| 2026-08-19 | `1ff21f58ae` | Ryan Schmidt | GeometryProcessing: optimize SweepingMeshSDF make\_level\_set3\_parallel\_floodfill() function. Replaced single full-grid lock with per-chunk locks to reduce lock contention. Also made per-chunk queues t… |
| 2026-08-19 | `40db80c9f7` | rob krajcarski | Ensure that we don't worry about trying to optimize the Niagara bytecode unless it is valid. Out of date code could have gotten to the VM (for standalone scripts during cooking) which can result in c… |
| 2026-08-19 | `5724cc25ea` | Yuriy ODonnell | Optimized FRichCurve::RemoveRedundantKeysInternal by adding an explicit FKeyHandleMap::Initialize method instead of a loop over Add(). Reduces complexity from O(n^2) to O(n). |
| 2026-08-19 | `6e16de5c03` | Yuriy ODonnell | Increase default r.RayTracing.ParallelMeshBatchSize from 128 to 1024 to avoid some of the task overhead and resource contention. |
| 2026-08-19 | `aeedfec2a0` | Yuriy ODonnell | Speed up FEQSHelpers::RunNavProjection by removing elements from Points array after the workload result processing loop. |
| 2026-08-19 | `f64e2c56b3` | Jimmy Andrews | Optimize FDynamicMesh3 to do less wasteful allocating/better copying |
| 2026-08-19 | `1ec483f094` | jeanfrancois dube | Set Chaos::MaxDirtyElements to MAX\_int32 in editor builds to avoid costly ReoptimizeTree calls during various operations. |
| 2026-08-19 | `1009c5951c` | Arne Schober | U5 - remove forcenoinline as otherwise the compiler will generate the call to the empty function in optimized builds. |
| 2026-08-19 | `d7de37fc6a` | Helge Mathee | RigVM: Literal consolidation optimization |
| 2026-08-19 | `121aedc99e` | Sebastien Lussier | Optimized HLOD merged mesh generation \* Avoid recreating render states for all primitives in the world #rb jeanfrancois.dube |
| 2026-08-19 | `dcb12708c6` | Sebastien Lussier | Optimized HLOD proxy mesh generation \* Avoid recreating render states for all primitives in the world #rb jeanfrancois.dube |
| 2026-08-18 | `3ede24be54` | tuhoiisa | Drop shader stats call unavailable in 4.27 |
| 2026-08-18 | `2ef6193ec7` | tuhoiisa | Backport IntFitsIn template from UE5 |
| 2026-08-18 | `d8d4b6a1c9` | tuhoiisa | Adapt occlusion history trim to 4.27 view family time |
| 2026-08-18 | `2ddce9f0a0` | tuhoiisa | Adapt SScaleBox prepass invalidation to 4.27 SWidget API |
| 2026-08-18 | `039978fa12` | tuhoiisa | Backport Misc/MTAccessDetector.h from UE5 |
| 2026-08-18 | `8a37cb5e9d` | Kevin Ortegren | Skip post process material pass when all the pixels will fail the stencil test of the material. Corrects certain stencil test operations from executing full screen when not needed. Saves performance… |
| 2026-08-18 | `b7bf2982ed` | sebastien lussier | Shader Compilation - Prevent job cancellation from leaving unscheduled duplicated jobs behind, which could cause a hang - Not merging to main as code was refactored there and a slightly different fix… |
| 2026-08-18 | `3278a418b8` | mickael gilabert | Fix FOcclusionRandomStream OOB |
| 2026-08-18 | `d37fe1b584` | stu mckenna | - Reset SKM data interface if the source component is unregistered - Reading from an unregistered skeletal mesh will have no ComponentSpaceTransforms and hit an ensure |
| 2026-08-18 | `c1ee965d46` | christopher waters | Make sure we flush occlusion queries out of memory if we've turned them off. |
| 2026-08-18 | `8c16c65b44` | Kevin Ortegren | Guard against integer overflow under allocation in Custom Instance Data by not allocating. Access to this buffer is not occurring when NumCustomDataFloats is 0. |
| 2026-08-18 | `58bbfbcd46` | erin wasik | SScaleBox Prepass: scale box is getting old data and passing it along to children, mark prepass dirty so we get a new desiredsize from the child |
| 2026-08-18 | `3d4077a0ed` | yoan stamant | \[DebugDrawService\] added synchronization object for delegate registration since it can happen from multiple threads from primitives added in batch through ParallelFor(AddPrimitiveBatches.Num(), \[&amp;\](i… |
| 2026-08-12 | `0862c9c67e` | tuhoiisa | Upgrade legacy boolean ray tracing feature mode settings when loading config |
| 2026-08-12 | `e68e9941d1` | ben hoffman | Add FWildcardNodeUtils with some commonly used logic to create/compare wildcard pins in blueprints |
| 2026-08-12 | `095ca04e70` | Matt Kuhlenschmidt | Fixed fixed size array properties defined by enums not showing their display names |
| 2026-08-12 | `c26a61d8d7` | brooke hubert | Fix a crash when editor viewport layouts destruct, and their viewport clients use the level editor global mode tools. |
| 2026-08-12 | `33b23eb07b` | Chad Garyet | Change the name of the zip file to EditorTarget rather than just "Editor" #jira none #rb none #rnx |
| 2026-08-12 | `71080ad6c6` | Louise Rasmussen | Fix to AthenaScoreAlert error. Added EnumRedirect for ETextTransformPolicy |
| 2026-08-12 | `1f0121779e` | Matt Kuhlenschmidt | Remove broken drop shadow from content browser list view |
| 2026-08-12 | `1cc504e959` | Louise Rasmussen | CIS Fix for TextLayout |
| 2026-08-12 | `44d5143887` | danny couture | Properly name the game thread on Windows |
| 2026-08-12 | `76c66377c1` | aditya ravichandran | Fixed some of the color theme viewer text not fitting in the button and the list moving off screen if too many items were added to it |
| 2026-08-12 | `5bb36e8482` | jimmy smith | Audio Codecs V1 Hello World and Unit tests #rb ethan.geller, aaron.mcleran,phill.Popp #jira UEAU-503 #jira UEAU-504 #jira UEAU-505 |
| 2026-08-12 | `b89041c3f9` | Jeff Farris | Merging using RigLogic\_CharacterTech\_to\_UE5Main 13925048 (inconsequential change, but to keep integrations happy) |
| 2026-08-12 | `a9ef85ff28` | Josh Adams | \[CIS\] Redoing change 13925048 (disabling Mac, Linux RigLogicLibTest module since it fails to link) |
| 2026-08-12 | `4a5cf7b1fa` | Matt Kuhlenschmidt | Missing edit to last file |
| 2026-08-12 | `c78e12e71a` | Matt Kuhlenschmidt | Fix the "New Plugins Available" prompt not dismissing immediately when clicking the dismiss button |
| 2026-08-12 | `c0056a39e1` | halfdan ingvarsson | Build fix for a missing argument to NotifyPostChange. |
| 2026-08-12 | `2007c6f90c` | Lauren Barnes | Removing unneeded function call #rb trivial #jira cis |
| 2026-08-12 | `98ca144630` | daren cheng | Fix save file dialog clipping. |
| 2026-08-12 | `23b6b55553` | Matt Kuhlenschmidt | Remove window drop shadows again. Causes too many artifacts |
| 2026-08-12 | `264e82cfa1` | danny couture | Fix infinite wait on cleared cooked platform data in case an UpdateResource clears them |
| 2026-08-12 | `bff7399d05` | Josh Adams | - Non-unity CIS fix |
| 2026-08-12 | `9cb06b3244` | Josh Adams | - Removed unnecessary MobileDeviceInterface reference from AutomationTool project |
| 2026-08-12 | `1b91362c0f` | halfdan ingvarsson | Remove unused function and nix dependency on Engine. |
| 2026-08-12 | `77bcca3bda` | Jeff Farris | Debug draw utilities in KismetTraceUtils.h are now tagged with ENGINE\_API |
| 2026-08-12 | `8969dd257f` | Matt Kuhlenschmidt | Trying out drop shadows on top level windows |
| 2026-08-12 | `8173f7155e` | aditya ravichandran | Added a details panel to the bulk property editor |
| 2026-08-12 | `978cf37c84` | Matt Kuhlenschmidt | Back out padding change to SWindow. Causes too many issues with UI elements being on the edge of the screen |
| 2026-08-12 | `e2810c3b23` | Matt Kuhlenschmidt | Remove padding from SWindow when maximized |
| 2026-08-12 | `9e1a0d67e9` | Marc Audy | Fix missing forward declares #rnx |
| 2026-08-12 | `314ce2bf34` | Patrick Laflamme | #jira UE-94499 - Crash Reporter application name shows Unreal Engine 4 Crash Reporter - Fixed the application title, getting it from the engine version rather than hardcoding it. |
| 2026-08-12 | `c284933b06` | Matt Kuhlenschmidt | Fix table header rows not clipping text when they get too small |
| 2026-08-12 | `44c6d7e99c` | danny couture | Enable Async Texture Compilation by default |
| 2026-08-12 | `20b8d8c76d` | Ryan Durand | Adding UGS ini. |
| 2026-08-12 | `ebd6b76e23` | ben hoffman | Add Insights traces to the Kismet Compiler |
| 2026-08-12 | `15aacdfd9d` | aditya ravichandran | Removed the "clear" action from material properties in actor details. |
| 2026-08-12 | `08975bacf8` | Josh Adams | - Removed HTML5 from UnrealTargetPlatform (it's a PlatformExtension, and that should add the UTP) |
| 2026-08-12 | `c910633aca` | Matt Kuhlenschmidt | Avoid rogue slow task dialog appearing for a few frames due to concert checking connection. Now we wait until the connection takes longer than a second before showing |
| 2026-08-12 | `e0b56f1993` | Louise Rasmussen | Scene Outliner - Adjusts Temp Actor display |
| 2026-08-12 | `0db42ebcda` | ben hoffman | Add asserts compatabile with doubles for Functional Tests |
| 2026-08-12 | `8ad4905222` | ben hoffman | Fix spelling mistake in comment on K2Node\_Tunnel |
| 2026-08-12 | `0ed76cef6e` | aditya ravichandran | EditorUtilityActor and EditorUtilityObject now show up as common classes when you create an EditorUtilityBlueprint |
| 2026-08-12 | `58256e7467` | aditya ravichandran | Reverting CL 13601508 because it showed some UI options that shouldn't be displayed (on the toolbar specifically). |
| 2026-08-12 | `ca4eb77d1d` | aditya ravichandran | Made the Set and Get Actor label functions more easily searchable in blueprints |
| 2026-08-12 | `827eb6dd67` | ben hoffman | Add kismet math functions for double support |
| 2026-08-12 | `dbe03026eb` | Louise Rasmussen | Scene Outliner Mobility - moved Mobility to an optional info column, removed icon badges |
| 2026-08-12 | `7e66a0b4cb` | ben hoffman | Double property support in blueprint for UFunctions, BP Variables, and conversions to floats |
| 2026-08-12 | `db1e0b8f34` | Louise Rasmussen | SLinkedBox - provides a way for widgets unrelated in the widget hierarchy to share a size |
| 2026-08-12 | `ba4aa18aa3` | Andrew Marre | #Animation PUMA Plugin setup with Anim Warping Nodes first pass #rb Jaren.Peterson |
| 2026-08-12 | `cc9e5f002b` | Josh Adams | - Moved UAT project commandline parsing up to BuildCommand to be usable by scripts other than BuildCookRun |
| 2026-08-12 | `6224b7be2d` | aditya ravichandran | Added functionality in the material editor to rename parameters by pressing F2. |
| 2026-08-12 | `99e8d39863` | phil popp | Metasound plugin initial checkin of data sharing reference graph. #rb Aaron.McLeran Ethan.Geller Jimmy.Smith Rob.Gay Maxwell.Hayes #jira UEAU-445 |
| 2026-08-12 | `29c3dc1d8d` | Matt Kuhlenschmidt | Do not allow the console command window to absorb and enter a key when the content browser drawer key is pressed |
| 2026-08-12 | `8a5e082baf` | Matt Kuhlenschmidt | Remove unused border from UMG designer view which is causing a huge gray block to appear in the new style |
| 2026-08-12 | `ebfedc11bf` | Matt Kuhlenschmidt | Renamed Brush Wireframe to Wireframe in menus to avoid confusion. We dont differentiate between wireframe and brush wireframe anymore |
| 2026-08-12 | `c5c0480173` | Ryan Durand | Adding support in CopyUAT to write out a copied file list for debugging purposes. |
| 2026-08-12 | `f9c9793e77` | Matt Kuhlenschmidt | Complex gradients now take in a desired size override so every one of them does not have to be wrapped in a box to specify size |
| 2026-08-12 | `6fc8247600` | Matt Kuhlenschmidt | Move gradient widgets out of AppFramework and into Slate. They are neeed for slate core styling |
| 2026-08-12 | `9e19fa62d8` | Matt Kuhlenschmidt | Fix perforce connection icon not appering correctly if a server and credentials are specified but the server cannot be contacted. |
| 2026-08-12 | `2020d95ccc` | Matt Kuhlenschmidt | Fix multi-user toolbar button not appearing in new toolbar if enabled. |
| 2026-08-12 | `9467d0a96c` | RedPixel | \[Config\] Engine Default Changes: Enabled NRD RELAX Denoiser by default, Deactivated XGE Shader Compilation |
| 2026-08-12 | `66f3d67891` | RedPixel | \[Math\] Changed order of declaration: VectorSin |
| 2026-08-12 | `e67a090a9f` | RedPixel | \[Optimization\]\[Mobile\]\[Switch 2\] Upgraded Neon Math for Faster Calculations |
| 2026-08-12 | `3e187a8caa` | RedPixel | \[Backport\] Lazy initialization of AnimNode\_RigidBody - Memory saving optimization. |
| 2026-08-12 | `005360822e` | RedPixel | \[Plugin\] AMD FSR 3.1.4 |
| 2026-08-11 | `4c91f03cdc` | halfdan ingvarsson | Add an IsEmpty() method to the standard containers for consistency and readability |
| 2026-08-11 | `c678deebe8` | ben hoffman | Fix incorrect CompactNodeTitle on FFrameNumber Divide\_FrameNumberInteger |
| 2026-08-11 | `d0d1d70ac4` | ben woodhouse | Fix for filesystem memory leak #jira UE-117562 #preflight 60f2bd3a35476b00013cbfaf |
| 2026-08-11 | `babadd1fb1` | ben zeigler | Change default OSS polling interval to 20ms, this matches the faster value required by all internal games and several platforms #rb rob.cannaday #jira none |
| 2026-08-11 | `8cc5c80134` | ben woodhouse | Log the hitch threshold when the hitch detector is enabled or the hitch threshold changes at runtime |
| 2026-08-11 | `d372deef6f` | wei liu | Fix a bug of missing mobile shaders when using Performance mode. |
| 2026-08-11 | `a7d5f56f5b` | david harvey | Adding optional platform-specific MfMedia initialization, allowing per-platform video decoding optimizations. |
| 2026-08-11 | `00184505d7` | cody albert | Fixed potential issue where transaction buffer could hold a reference to the dummy world created in UWidgetBlueprint::DetectSlateWidgetLeaks See UDN: https://epicgames.lightning.force.com/lightning/r… |
| 2026-08-11 | `a475c01357` | johan torp | Set/map property loading optimization |
| 2026-08-11 | `a4f3e6c473` | guillaume abadie | Adds CFLAG\_ForceOptimization on FDiffuseIndirectCompositeCS |
| 2026-08-11 | `9e1462c447` | matt peters | Cooker leak diagnostics: FReferenceChainSearch calls made from the cooker should use the new EReferenceChainSearchMode::FullChain flag, because RF\_Standalone objects are GC'd during cooking invocatio… |
| 2026-08-11 | `778d4013a3` | pj kack | Optimize FPropertyValueIterator to alleviate the GC performance regression from 16048941. Add separate stack entries instead of inserting elements in one single array to minimize mem copying. Minimiz… |
| 2026-08-11 | `33356edbca` | danny couture | Compilation time optimization - Disable codegen optims on extremely long function with lots of FORCEINLINE calls in it - 36.23s -&gt; 19.24s for FbxAutomationTests.cpp - 37.33s -&gt; 19.89 for Module.Edito… |
| 2026-08-11 | `d37726f66c` | danny couture | Compilation time optimization - Split extremely long function into multiple parts to improve codegen time - 22.04s -&gt; 11.14s for LowLevelMemTracker.cpp - 20.40s -&gt; 13.62s for Module.Core.4\_of\_17.cpp |
| 2026-08-11 | `9a54bfe827` | danny couture | Compilation time optimization - Reduce codegen time for huge switch case - 17.03s -&gt; 5.34s for ShowFlags.cpp - 24.59s -&gt; 13.73s for Module.Engine.45\_of\_56.cpp |
| 2026-08-11 | `031cb08acf` | brandon dawson | Allow for time-sliced unhashing of uobjects when in the editor. All unhashing will still occur before streaming is continued, but async loading will provide additional time to the unhashing, allowing… |
| 2026-08-11 | `8142f76fed` | Emil Persson | Fix DredSettings leaking |
| 2026-08-11 | `3e94bde151` | Johan Torp | Optimize asset registry UpdateTemporaryCaches() |
| 2026-08-11 | `83ff311ab2` | brandon dawson | Prevent memory leaks when caching mesh draw commands in parallel thread. \[REVIEW\] \[at\]Graham.Wihlidal,\[at\]Nick.Whiting |
| 2026-08-11 | `bb7fafa5e2` | Francis Hurteau | undo commented blacklist from cl 15714549 until other content browser filtering optimization are merged in UE5 |
| 2026-08-11 | `ad53f9c5e0` | Thomas Sarkanen | Revert optimization for layered bone per blend |
| 2026-08-11 | `5ab9d55aee` | Matt Peters | AssetManager's BulkDataScanning: keep the AssetRegistry's temporary caching optimization going when we detect that it is invalidated; use the AssetRegistry's internal invalidation functionality rathe… |
| 2026-08-11 | `c8fe4e4f51` | brandon dawson | Remove the InlineAllocator from the FPassDrawCommandArray and FPassDrawCommandBuildRequestArray typedefs. The size of these arrays was causing the the Virtual Allocator to get used when allocating us… |
| 2026-08-11 | `cb9bd048ee` | Jason Nadro | Fix memory leak in FPreloadFile. |
| 2026-08-11 | `968ba7f49e` | Jason Nadro | Removing file info caching from StreamingNetworkPlatformFile. |
| 2026-08-11 | `7c0ec1f439` | Tim Smith | Minor changes to stablize UHT code generation in preperation for more extensive performance changes. |
| 2026-08-11 | `cb51bad362` | danny couture | Switch default allocator on Windows from tbb to mimalloc because of both performance and memory usage improvements - See CL 15887498 description for benchmarks and motivation |
| 2026-08-11 | `7bdefff901` | brett miller | GeometryCollection -- Removed vertex visibility test from CalcBounds as it was having the opposite performance effect than intended. |
| 2026-08-11 | `84cbfd4c56` | Patrick Boutot | Slate: Remove deprecated invalidation flag. Remove unwanted pragma disable optimization. #rb none |
| 2026-08-11 | `f0d03326f8` | Tim Smith | UE-10688 - UE4 Static Analysis Win64 (PVS-Studio) - chunkdownloader.cpp - Visibility scope of the 'MultiCallback' pointer was exited without releasing the memory. A memory leak is possible |
| 2026-08-11 | `23fad7f6ab` | danny couture | Disable loading of asset at Persona module startup because of major performance regression this code introduce |
| 2026-08-11 | `b908181995` | zach bethel | Improved slate D3D vertex / index buffer growing algorithm to reduce hitches. |
| 2026-08-11 | `514277a5ed` | jimmy smith | Optimization to Audio::FastSin3 #jira none #rm miles.flanagan aaron.mcleran |
| 2026-08-11 | `1012f7acf0` | Tim Smith | Fixing PVS 7.7 Issues: |
| 2026-08-11 | `71c81bf930` | Ryan Schmidt | ModelingComponents: Add UMeshWireframeComponent, this is a component that renders mesh edges as lines, with line color/thickness varying depending on line type. Accesses mesh via an API so client doe… |
| 2026-08-11 | `29b76fc1b8` | halfdan ingvarsson | Add support for enabling the clang static analyzer on Windows when using the clang compiler. |
| 2026-08-11 | `a09295525a` | danny couture | Add performance tags on compression and report back error message on ZLIB errors |
| 2026-08-11 | `2473aa454c` | Jamie Dale | Clear asset selection on shutdown |
| 2026-08-11 | `69abd3850d` | danny couture | Reduce game-thread stutters during async animation compression |
| 2026-08-11 | `882c4af4d7` | ionut matasaru | \[Insights\] - Improved performance of flat grouping for very large generic tables. - Added debug code in STableTreeView to measure peak times spent in sorting, filtering and grouping. - Added FInt64Va… |
| 2026-08-11 | `3a3ef7c882` | danny couture | Fix stutters in the game-thread while streaming texture mips from DDC. |
| 2026-08-10 | `b1055db38f` | tuhoiisa | Re-integrate UrlEncode rewrite and DX11 HDR detection from e9073796065d |
| 2026-08-10 | `a5a9911da3` | Steve Robb | FPlatformString support for UTF8CHAR. |
| 2026-08-10 | `3b6c274ad0` | Steve Robb | Some extra support for UTF8CHAR and related compile time checks for char encodings. |
| 2026-08-08 | `6786cbc8c4` | tuhoiisa | Revert "fix for HDR in editor (scRGB): we were applying AP1-&gt;sRGB color space conversion twice in case of scRGB: once during the LUT computation, and once during the tonemapping through ST2084ToScRGB… |
| 2026-08-07 | `6a5d0be2d0` | tuhoiisa | Revert "Landscape edit layers : " |
| 2026-08-07 | `d71f2e0504` | tuhoiisa | Revert "Immediately release static mesh offline ray tracing data if ray tracing is known to be disabled at run-time due to user settings. " |
| 2026-08-07 | `5b40d8b52a` | tuhoiisa | Revert "Remove TagAtLastTest from SoftObjectPtr (and LazyObjectPtr) as it was only used for edge cases involving stale weak pointers and caused bugs when objects are created without calling Invalidat… |
| 2026-08-07 | `4e44e443ee` | tuhoiisa | Revert "Optimization for UBlueprintGameplayTagLibrary::HasAllMatchingGameplayTags and DoesTagAssetInterfaceHaveTag. " |
| 2026-08-07 | `d3a246cf06` | tuhoiisa | Revert "- Merging fix for wrong descriptor passed to d3d12Resource constructor. Shared buffers were causing asserts when getting resource allocation info. " |
| 2026-08-07 | `8128c066f3` | tuhoiisa | Revert "Manual cherry-picks and fixes for UE5.2/5.3 Backport" |
| 2026-08-07 | `7a924b2a8b` | tuhoiisa | Revert "\[Backport\] Adapt UE5.2/5.3 backports to 4.27 APIs" |
| 2026-07-25 | `318563e96e` | Tuhoiisa | \[Backport\] Adapt UE5.2/5.3 backports to 4.27 APIs |
| 2026-07-25 | `e907379606` | tuhoiisa | Manual cherry-picks and fixes for UE5.2/5.3 Backport |
| 2026-07-25 | `ff943563e3` | sebastien lussier | HLOD: Optimized HLOD cluster generation \* Leverage the fact that if a cluster becomes invalid it will never become valid again and saves all valid merged clusters in a separate array to speed up proc… |
| 2026-07-25 | `a7f762cd11` | jeremy moore | Use DrawsVelocity instead of IsMovable to check whether primitive can draw velocity. This fixes case where static primitives were not rendering velocity, even with WPO. Might need to follow up with f… |
| 2026-07-25 | `9d8a38f69c` | Jeremy Moore | Take into account whether primitive is set to always write velocity when building GPU Scene primitive flags. Primitives that use world position offset use this to ensure that they write velocity duri… |
| 2026-07-25 | `10c780212d` | john vanderburg | Optimization in the LinkerLoad, when it has many bulk data loaders. This could do like a linear search through the large array thousands of times, which got very slow. Turned the TArray into a TSet.… |
| 2026-07-25 | `958c3ccf49` | Kevin Ortegren | Skip post process material pass when all the pixels will fail the stencil test of the material. Corrects certain stencil test operations from executing full screen when not needed. Saves performance… |
| 2026-07-25 | `04eadf49b9` | jason hoerner | DisplayCluster perf: made it so scene occlusion queries are added to a queue based on the UniqueID of the first View in the ViewState, so in scenarios where there are multiple view families rendering… |
| 2026-07-25 | `cdee86d00e` | danny couture | Reduce allocations during collision mesh creation - 201.3ms to 146.7ms total from engine start to end of skydiving section in replayrun |
| 2026-07-25 | `dacb9ccb2e` | cedric caillaud | Chaos - Heightfield raycast perf improvement - Make sure VisitRaycast returns relevant value if a triangle has been hit - Shorten the raylength to the exit time from the test against the heightfield… |
| 2026-07-25 | `ed7cea1cb2` | robert manuszewski | Locking the entire hash maps instead of individual hash buckets when iterating UObject maps to prevent memory stomps when creating / renaming / destroying objects mid iteration |
| 2026-07-25 | `b00d7a5e23` | robert manuszewski | Locking the entire hash map instead of individual buckets when iterating UObject hash maps with ForEachObjectWith\* functions to fix a loophole that allowed new UObjects to be created while iterating… |
| 2026-07-25 | `cca47acc71` | kenzo terelst | Increase max residency set count to 128 to fix possible OOM on machines with lots of cores and worker threads for texture streaming after editor level load. Increase CPU memory size with around 1MB f… |
| 2026-07-25 | `6e1e56ae01` | jonathan bard | Fixed missing resource transitions for GPU particle simulation resources (failing RHI validation) |
| 2026-07-25 | `58bf4302d3` | christopher waters | RHI stall improvements - When trying to stall the RHI thread, use TryLock+YieldThread to avoid the scenario where the OS scheduler doesn't yield the RHI thread fast enough. - When calling StallRHIThr… |
| 2026-07-25 | `4490966137` | mihnea balta | Disallow async compute in mGPU mode because it causes CPU hangs (likely due to command lists being submitted in the wrong order). |
| 2026-07-25 | `8cc1ebd63a` | David Hill | Skeletal Mesh Reduction. Improve attribute interpolation during simplification. |
| 2026-07-25 | `2514ef5d64` | joe bestrotheray | Add option to log stack when GC is forced #rb none |
| 2026-07-25 | `a0c4798c20` | bruno ferreira1 | Added AActor::FindComponentByTag to avoid allocating and copying arrays of components around |
| 2026-07-25 | `2bb4312f33` | simon therriault | - Merging fix for wrong descriptor passed to d3d12Resource constructor. Shared buffers were causing asserts when getting resource allocation info. |
| 2026-07-25 | `2257fe1cad` | dan oconnor | Destroy the skeleton class before clearing the UBlueprint's generated class. This allows UBlueprintGeneratedClass::PostLoad (called during duplication) to correctly identify that it is not the author… |
| 2026-07-25 | `014df0abac` | christopher fiala | Fix ScreenPosition material expression not rendering correctly in secondary views with Instanced Stereo Rendering enabled. |
| 2026-07-25 | `e0db06d191` | jordan cristiano | Optimization for UBlueprintGameplayTagLibrary::HasAllMatchingGameplayTags and DoesTagAssetInterfaceHaveTag. |
| 2026-07-25 | `e1643f2829` | dmytro vovk | Fixed FPerThreadFreeBlockLists leak in MB3 #rb Johan.Torp |
| 2026-07-25 | `dcc5e007a6` | Mieszko Zielinski | Added checks to EQS item types to ensure the correct amount of memory gets allocated. |
| 2026-07-25 | `46d062de42` | ben zeigler | Remove TagAtLastTest from SoftObjectPtr (and LazyObjectPtr) as it was only used for edge cases involving stale weak pointers and caused bugs when objects are created without calling InvalidateTag Rem… |
| 2026-07-25 | `dcd9f5e12c` | Benn Gallagher | Fixed ensure condition when required bones are requested from a skeletal mesh component that hasn't yet allocated transforms. #rb Thomas.Sarkanen #jira UE-174332 #preflight 63fce713ae54ee4ce92c26bb |
| 2026-07-25 | `7a0edeaab0` | james singer | Fix for race condition in Linux FileMapCache |
| 2026-07-25 | `52897338b2` | dan oconnor | Make sure we use authoritative class, in case a literal object is being reinstanced on load |
| 2026-07-25 | `e06ae3c1a9` | elizabeth baumel | Fix redundant file writes and overwrites when saving high-res screenshots. GIsHighResScreenshot was being set to true too early, so images would be repeatedly generated, saved, and overwritten. Somet… |
| 2026-07-25 | `2276a14858` | Jurre deBaare | Nothing occurs when compressing an animation on a skeleton with no bones |
| 2026-07-25 | `e3849c533b` | massimo tristano | Fix in LandscapeRender to read whether WorldPositionOffset is enabled in the material from the correct source (shader map) instead of the old, approximate source (asking the material if the property… |
| 2026-07-25 | `43aec4227c` | jeannoe morissette | VulkanRHI: Match other RHI and skip shader check when the SRV/UAV being set is null (the RHI will do nothing anyhow). |
| 2026-07-25 | `1cdf21c73c` | danny couture | Fix potential race on FSelfRegisteringExec during ALT loading |
| 2026-07-25 | `d044bb99f7` | yuriy odonnell | Immediately release static mesh offline ray tracing data if ray tracing is known to be disabled at run-time due to user settings. |
| 2026-07-25 | `2291e9e0c5` | jeannoe morissette | VulkanRHI: Fix security issue regarding loading of vulkan pipeline cache. |
| 2026-07-25 | `48330641b1` | eric mcdaniel | Allow for stack reserve and commit size control on all Microsoft platforms (expanded from Windows only previously) |
| 2026-07-25 | `b44435520a` | dominik peacock | Fix crash resetting property when IPropertyTypeCustomization::CustomizeChildren used on instanced TArray&lt;UObject\*&gt; called AddExternalObjects on array elements and supplied a OverrideResetToDefault im… |
| 2026-07-25 | `bfda7de771` | pj kack | Change ArchetypeAnnotation to use FUObjectAnnotationChunked instead of FUObjectAnnotationDense (originally implemented in 18810065). Reduces memory from 3.2 MB to 2.2 MB for an internal project with… |
| 2026-07-25 | `d133b315f1` | massimo tristano | Fixed crash caused by renaming material graph node to name 1024 character or more long. |
| 2026-07-25 | `6553dfa391` | jeanfrancois dube | Foliage optim: use a static name instead of looking it up for every call to FFoliageHelper::IsOwnedByFoliage. This happens when we rename actors during cooks for partitioned world, for every actor. |
| 2026-07-25 | `3b395ad6c2` | jaime cifuentes | AnimInstance display debug fix to avoid a crash when a montage ends while blending physical animation (Montage pointer inside MontageInstance is null) |
| 2026-07-25 | `fc24dbdfc4` | danny couture | Fix PostSerialize to support async loading thread |
| 2026-07-25 | `3698616ea0` | devin doucette | DDC: Fixed the file system cache EditorOverrideSetting not handling paths with \\ in them |
| 2026-07-25 | `cd2921918c` | jeanluc corenthin | Fixed crash when commiting a HSIM with null material overrides |
| 2026-07-25 | `a67eb513cf` | jonathan bard | Landscape edit layers : \* Fixed missing barrier \* Added some GPU tags to improve readability of render captures |
| 2026-07-25 | `9659ba0c9a` | benjamin fox | Don't trigger replicated gameplaycues from gameplayeffects that no longer exist if the gameplayeffect no longer exists |
| 2026-07-25 | `919eeadb27` | vivien wei | Refine TargetTags lacking problem in UAbilitySystemComponent::ApplyGameplayEffectSpecToSelf - Previously was simply populating the tags from owner ability system component when UGameplayAbility::BP\_A… |
| 2026-07-25 | `fcf976b34f` | vivien wei | Fix Removal Tag requirment not working for apply cooldown GE - GE with removal tag requirement specified would be removed unexpectedly - the chain of UGameplayAbility::ApplyGameplayEffectToOwner neve… |
| 2026-07-25 | `0b6f7e03c1` | Stals | PR #9519: Fix: GAS Ability getting stuck if EndAbility was called during the lock inside ApplyGameplayEffectSpecToTarget (Contributed by Stals) |
| 2026-07-25 | `0def0cd302` | danny couture | Protect AllEnumNames which can be accessed from multiple threads at the same time (i.e. async loading thread and game-thread) |
| 2026-07-25 | `65d391d21c` | mic rooney | Manual merge of 21006616 - Converting FGameplayAbilitySpec/Def::SourceObject to be a weak reference. \* Includes update to lyra SourceObject references. |
| 2026-07-25 | `fc6c0ea116` | angela wu | Move AbilityCount++ to CallActivateAbility at the end of PreActivate to prevent an ability from accidentally cancelling itself and running EndAbility before ActivateAbility |
| 2026-07-25 | `63a35f0d8c` | benjamin rouveyrol | fix selection outline for HDR editor: ScRGB can generate negative values |
| 2026-07-25 | `00561b6cda` | ben woodhouse | D3D12 RHI fence logic fixes: - Stop the RHI thread holiding a critical section in FD3D12CommandListData::WaitForCompletion while we're waiting on the GPU. This has a very bad effect on RHI thread per… |
| 2026-07-25 | `43c41bacdd` | ionut matasaru | \[Insights\] Added LLM\_SCOPE(ELLMTag::UI); in FSlateApplication::OnSizeChanged() in effort to reduce untagged allocations. It captures ~10000 untagged allocations (~10 MiB) in a short Editor run sessio… |
| 2026-07-25 | `7ef3e151ff` | benjamin rouveyrol | fix for HDR in editor (scRGB): we were applying AP1-&gt;sRGB color space conversion twice in case of scRGB: once during the LUT computation, and once during the tonemapping through ST2084ToScRGB. Since… |
| 2026-07-25 | `ce94ee7a6a` | andrew thayer | Fixed an issue when a gameplay ability listening to activate based on a tag would fail to be activated. This would happen if there were more than one GA listening to this tag, and the first one in th… |
| 2026-07-25 | `5c24b93e31` | nicholas howe | Fix a bug where a widget disappears for a frame when it changes from volatile to non-volatile, by adding the NeedsRepaint update flag in SWidget::UpdateFastPathVolatility when the widget is not volat… |
| 2026-07-25 | `499d5849c3` | robert millar | Reset UniqueTables instead of emptying it to reduce allocator churn. Reset FCommandListResourceState::ResourceStates instead of emptying it to reduce allocator churn. |
| 2026-07-25 | `f8a6d65646` | jeannoe morissette | Make sure RHI resources are flushed even when nothing is rendered to prevent leak in RHI (D3D12/Vulkan) when Realtime is turned off in Editor. |
| 2026-07-25 | `ca0832e1e7` | christopher waters | Fixing deadlocks on lower core count PCs running DX12. |
| 2026-07-25 | `41008c67fa` | billy bramer | Ability System - Add methods to dynamically alter set-by-caller magnitudes on already active gameplay effects (one for a single tag and one for multiple at once) - Fix typo of "Get Activate" to "Get… |
| 2026-07-25 | `74d931dd0f` | Jon Nabozny | Move the call to FlushNetDormancy earlier when removing active gameplay effects. This prevents issues where changes to ActiveGameplayEffects aren't tracked properly on Dormant actors. |
| 2026-07-25 | `722caed076` | Daniel Wright | Suppressed D3D12RHI log spam "Force flushing command list to GPU because too many commands have been enqueued already" #preflight none trivial |
| 2026-07-25 | `c4b71b218d` | Fred Kimberley | Fix a bug where effects were being removed based on the source data of a new effect being applied instead of the target data. |
| 2026-07-25 | `67f4916a00` | Robert Manuszewski | Keeping track of AbilitySystemComponent's references to other actors and releasing them to prevent levels from leaking |
| 2026-07-25 | `e8387b7033` | arciel rekman | Allocate RHI shader cache on demand (UE-136845). |
| 2026-07-25 | `a472dcf641` | arciel rekman | Allow D3D12 and Vulkan to preload only shaders needed by PSOs. |
| 2026-07-25 | `1c5f683d97` | richard malo | Optimized FClothingSimulation::CreateActor inclusive avg 8.5ms down to 5.6ms (Reduce allocations done in FGraphColoring::ComputeGraphColoring). #rb jeanfrancois.dube, michael.lentine #preflight 615c4… |
| 2026-07-25 | `6106c08892` | kenzo terelst | Implement LockTexture2DArray\_RenderThread &amp; UnlockTexture2DArray\_RenderThread in d3d12 and agc rhi to remove the unrequired RHI thread flush which isn't required on these platforms |
| 2026-07-25 | `ea81c141c6` | danny couture | Reduce reallocs due to auto shrinkage of RemoveSwap causing bouncing between 0 element and 1 element very often - Gets rid of 572K reallocs from process start to end of skydiving for a replayrun |
| 2026-07-25 | `bffc060721` | Ori Cohen | Fix missing backface culling on complex sweeps. Improves perf and is consistent with raytrace behavior |
| 2026-07-25 | `45c7a8104c` | Ola Olsson | Inline allocate the dummy element in the RobinHoodHashTable, saves a lot of redundant allocations in the shadow setup (FViewInfo::CreateSnapShot -&gt; FGraphicsMinimalPipelineStateSet). - also fixes mis… |
| 2026-07-25 | `27399eb330` | james doverspike | Compress FUObjectHashTables::HashOuter |

<!-- END GENERATED COMMIT RECORD -->

## 関連項目

- [すべてのリリースノート](Release-Notes.md)
- [ueVite26 September Major](ueVite26-SeptemberMajor.md)
- [ueVite26 July Major](ueVite26-JulyMajor.md)
- [バックポート](Backporting.md)
