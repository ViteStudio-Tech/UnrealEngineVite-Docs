# コンソール変数

<tldr>
<p>
Vite 固有のコンソール変数と、よく必要になる標準のものを、サブシステムごとにまとめています。これは選び抜いた一覧であり、すべてを網羅したものではありません。全体を確認するには <code>help</code> かコンソールの自動補完を使ってください。
</p>
</tldr>

<warning>
この一覧のレイトレーシングの変数のいくつかは、既定のビルドでは <b>コンパイル対象から外れています</b>。設定自体は成功しますが、何も描画されません。利用可否は変数ごとに示しています。<a href="Compile-Time-Switches.md">コンパイル時スイッチ</a>
を参照してください。
</warning>

変数は実行時にコンソールで設定するか、`Config\DefaultEngine.ini` で恒久的に設定します。

```ini
[/Script/Engine.RendererSettings]
r.SMAA.Quality=2
r.HBAO.Enable=1
```

## Vite 固有

これらは標準の UE 4.27 には存在しません。

| 変数 | 既定値 | 用途 |
|---|---|---|
| `r.SMAA.Quality` | 2 | SMAA の品質。0 = Low、1 = Medium、2 = High、3 = Ultra。August Major 以降。それ以前のリリースは `r.Vite.SMAA.Mode`（0 = Low、1 = High）。[アンチエイリアシング](Anti-Aliasing.md) を参照 |
| `r.SMAA.EdgeMode` | 0 | SMAA のエッジ検出。0 = 色、1 = 輝度。August Major 以降 |
| `r.SMAA.DebugVisualization` | 0 | SMAA のデバッグ表示（Shipping 以外のビルド）。1 = エッジ、2 = ブレンドの重み、3 = 強調した結果。それ以前のリリースは `r.AntiAliasing.SMAA.Debug` |
| `r.Vite.SSAO` | 1 | Vite の最適化された SSAO の経路。開発用のビルドのみで、Shipping と Test は `VITE_O_SSAO` に固定。[アンビエントオクルージョン](Ambient-Occlusion.md) を参照 |
| `p.VitePhysXFixedTimestep.Enabled` | 0 | 固定タイムステップの物理を有効にする |
| `p.VitePhysXFixedTimestep.DeltaTime` | 0.01667（1/60） | 固定ステップの長さ（秒） |
| `p.VitePhysXFixedTimestep.MaxTimesteps` | 16 | 1 回のゲームのティックあたりの固定ステップの最大数 |
| `p.VitePhysXFixedTimestep.MaxCumulativeExtraSteps` | 50 | 制限の方針が適用されるまでの過負荷の予算 |
| `p.VitePhysXFixedTimestep.LimitType` | 0 | 0 = 固定ステップを制限、1 = 可変のサブステップに切り替え |
| `p.VitePhysXFixedTimestep.InterpolationMode` | 1 | 0 = オフ、1 = コンポーネントごと、2 = 常に |

<note>
<code>p.VitePhysXFixedTimestep.*</code> の変数には、<code>VITE_PHYSX_FIXED_TIMESTEP=1</code> でビルドしたエンジンが必要です。
<a href="Fixed-Timestep.md">固定タイムステップ</a> を参照してください。
</note>

## レイトレーシング

| 変数 | 既定値 | 利用可否 | ページ |
|---|---|---|---|
| `r.RayTracing.Reflections` | 0 | 利用可 | [レイトレーシング反射](RT-Reflections.md) |
| `r.RayTracing.Shadows` | 0 | 利用可 | [レイトレーシングシャドウと AO](RT-Shadows-And-Ambient-Occlusion.md) |
| `r.RayTracing.AmbientOcclusion` | 0 | 利用可 | [アンビエントオクルージョン](Ambient-Occlusion.md) |
| `r.RayTracing.SkyLight` | &mdash; | 利用可 | [レイトレーシング](Ray-Tracing.md) |
| `r.RayTracing.GlobalIllumination` | -1 | **コンパイル対象外** | [グローバルイルミネーション](Global-Illumination.md) |
| `r.RayTracing.Translucency` | 0 | **コンパイル対象外** | [レイトレーシング半透明とコースティクス](RT-Translucency-And-Caustics.md) |
| `r.RayTracing.SampledDirectLighting` | 0 | **コンパイル対象外** | [RTXDI](RTXDI.md) |

値が `-1` の場合、その設定はコンソール変数ではなくポストプロセスボリュームによって決まります。

### カリングとシーンの設定

| 変数 | 用途 |
|---|---|
| `r.RayTracing.Culling` | `0`（既定）はオフ、`1` はカメラの後ろのオブジェクトを距離と立体角でカリング |
| `r.RayTracing.Culling.Radius` | カメラの後ろのオブジェクトをカリングする距離。既定は 10000（100&nbsp;m） |
| `r.RayTracing.Culling.Angle` | カメラの後ろのオブジェクトをカリングする、投影された角度のしきい値。既定は 1 |
| `r.RayTracing.SceneCaptures` | シーンキャプチャがレイトレーシングのシーンを構築するかどうか |
| `r.RayTracing.PreGather` | 事前収集のパスの制御 |

カリングの設定は、レイトレーシングの性能を左右する最も効果的な手段の 1 つです。Vite はこれらを標準の 4.27 の値のまま、カリングを無効にしています。有効にすべき場面は [エンジンの既定値の変更](Engine-Defaults.md#ray-tracing-culling) を参照してください。

### スカイライト

| 変数 | 用途 |
|---|---|
| `r.RayTracing.SkyLight.SamplesPerPixel` | サンプル数 |
| `r.RayTracing.SkyLight.MaxRayDistance` | レイの長さの上限 |
| `r.RayTracing.SkyLight.ScreenPercentage` | スカイライトのパスの解像度のスケール |
| `r.RayTracing.SkyLight.Denoiser` | デノイザーの選択 |
| `r.RayTracing.SkyLight.EnableMaterials` | ヒット時にマテリアルを評価する |
| `r.RayTracing.SkyLight.EnableTwoSidedGeometry` | 両面のジオメトリの扱い |

スカイライトのパスが高価すぎる場合は、`ScreenPercentage` と `SamplesPerPixel` の 2 つから調整してください。

### 半透明

既定ではコンパイル対象外です。

| 変数 | 用途 |
|---|---|
| `r.RayTracing.Translucency.HalfRes` | 半分の解像度の半透明 |
| `r.RayTracing.Translucency.HybridDepthThreshold` | ハイブリッドな半透明の深度のしきい値 |
| `r.RayTracing.Translucency.HybridDepthBias` | ハイブリッドな半透明の深度のバイアス |
| `r.RayTracing.PrimaryRays.IncludeDOF` | プライマリレイに被写界深度を含める |

### RTXDI（サンプリングによるライティング）

既定ではコンパイル対象外です。`r.RayTracing.SampledDirectLighting` が全体のスイッチで、`r.RayTracing.SampledLighting.*`
の系統（リザーバーの数、空間と時間の再サンプリング、ReGIR のセルの構成、ライトの種類ごとの切り替えなど、60 を超える変数）で調整します。

まず知っておく価値があるもの:

| 変数 | 既定値 | 用途 |
|---|---|---|
| `r.RayTracing.SampledLighting.Mode` | 1 | サンプリングのモード |
| `r.RayTracing.SampledLighting.InitialSamples` | 8 | 最初の候補のサンプル数 |
| `r.RayTracing.SampledLighting.Spatial` | 1 | 空間の再サンプリング |
| `r.RayTracing.SampledLighting.Temporal` | 1 | 時間の再サンプリング |
| `r.RayTracing.SampledLighting.NumReservoirs` | -1 | リザーバーの数。-1 で自動 |
| `r.RayTracing.SampledLighting.Denoiser` | &mdash; | デノイザーの選択 |
| `r.RayTracing.SampledLighting.DebugMode` | &mdash; | デバッグ表示 |

[RTXDI](RTXDI.md) を参照してください。

### コースティクス

メッシュと水のコースティクスは、主にコンソール変数ではなくポストプロセスボリュームの設定で制御され、どちらも既定ではコンパイル対象外です。関連する変数:

| 変数 | 用途 |
|---|---|
| `r.RayTracing.BuildRayTracingMeshForCaustics` | コースティクスに対応したレイトレーシングのジオメトリを構築する |
| `r.ParallelCausticsMap` | コースティクスマップの並列描画 |
| `r.PathTracing.ApproximateCaustics` | パストレーサーでのコースティクスの近似 |

[レイトレーシング半透明とコースティクス](RT-Translucency-And-Caustics.md) を参照してください。

## グローバルイルミネーション

| 変数 | 用途 |
|---|---|
| `r.RTXGI.DDGI` | DDGI 全体の切り替え |
| `r.RTXGI.DDGI.LightingPass.Scale` | ライティングのパスの解像度のスケール |
| `r.RTXGI.DDGI.LightingPass.RelativeDistanceThreshold` | 距離による除外のしきい値 |
| `r.RTXGI.DDGI.LightingPass.NormalPower` | 法線による重み付け |
| `r.RTXGI.DDGI.ProbesTextureVis` | プローブのテクスチャの可視化 |
| `r.RTXGI.DDGI.ProbesTextureVis.IrradianceScalar` | 可視化のスケール |
| `r.RTXGI.DDGI.StatVolume` | ボリュームごとの統計 |
| `r.RTXGI.MemoryUsed` | DDGI のメモリ使用量を報告する |

RTXGI のプラグインは既定で有効です。[動的 DDGI](DDGI-Dynamic.md) と [グローバルイルミネーション](Global-Illumination.md)
を参照してください。

## アンビエントオクルージョン

| 変数 | 既定値 | 用途 |
|---|---|---|
| `r.HBAO.Enable` | 0 | HBAO+ を有効にする。スクリーンスペースの AO のバッファに乗算します。 |
| `r.HBAO.HighPrecisionDepth` | 0 | 0 = 内部の深度を FP16、1 = FP32。遠くのオブジェクトの自己遮蔽によるバンディングを避けるには FP32 を使います。 |
| `r.HBAO.GBufferNormals` | 1 | 0 = 深度から法線を再構築、1 = GBuffer の法線を取得 |

HBAO+ には、ポストプロセスボリュームにボリュームごとの追加の設定があります。べき指数（既定 2.0）、半径（2.0）、バイアス（0.1）、小スケールの AO（1.0）、ブラーの半径（2 ピクセル）、ブラーのシャープネス（16.0）、最大の視距離（9500）、深度のシャープネス（50.0）、そして前景と背景の AO の距離です。

<note>
<code>r.HBAO.Enable</code> のヘルプは HBAO+ を DX11 専用と説明していますが、これは古い記述です。動作する D3D12 の実装があります。<a href="Ambient-Occlusion.md">アンビエントオクルージョン</a> を参照してください。
</note>

## テッセレーション

| 変数 | 既定値 | 用途 |
|---|---|---|
| `r.TessellationAdaptivePixelsPerTriangle` | 48.0 | テッセレーションの係数の全体の倍率。小さいほど三角形が増えます。 |

[テッセレーション](Tessellation.md) を参照してください。

## ヘア

| 変数 | 用途 |
|---|---|
| `r.TressFX.StrandsMode` | デバッグ描画のモード。0 = オフ、1 = シミュレーション用ストランド、2 = シミュレーションの影響度で色分けした描画用ストランド、3 = 髪の UV、4 = 根元の UV、5 = シード、6 = 寸法 |
| `r.TressFX.Interoplation.FrustumCulling` | 補間時の視錐台カリング。既定は 1 |
| `r.TressFX.MorphTargetMeshVisualization` | モーフターゲットのメッシュの可視化 |

[ヘアレンダリング](Hair-Rendering.md) を参照してください。

## ボリュメトリックフォグ

| 変数 | 用途 |
|---|---|
| `r.RayTracing.VolumeFogMode` | シャドウをレイトレーシングする際に、ボリュメトリックフォグでライトをどう扱うか |
| `r.VolumetricFog.UseUpScaledSizeVolumetricFog` | ボリュメトリックフォグを内部解像度ではなく出力解像度で描画する |

<note>
<code>r.VolumetricFog.UseUpScaledSizeVolumetricFog</code> は、<code>VITE_DLSS_PATCH=1</code> のビルドにだけ存在します。アップスケーリング時のボリュメトリックフォグの解像度を修正するためのものです。<a href="Upscalers.md">アップスケーラー</a>
を参照してください。
</note>

## プロファイリング

標準の Unreal のものですが、1 か所にまとめておく価値があります。

| コマンド | 表示されるもの |
|---|---|
| `stat unit` | Frame、Game、Draw、GPU、RHIT の時間。まずここから。 |
| `stat unitgraph` | 同じものの時間変化 |
| `stat game` | ゲームスレッドの内訳 |
| `stat scenerendering` | レンダースレッドの内訳 |
| `stat gpu` | GPU のパスの内訳 |
| `stat physics` | 物理ソルバーの時間 |
| `stat rhi` | RHI のリソースの統計 |
| `stat memory` | メモリ使用量 |
| `profilegpu` | 1 フレームの GPU のキャプチャ |
| `recompileshaders changed` | 変更したシェーダーを再コンパイル |
| `recompileshaders global` | グローバルシェーダーを再コンパイル |

[プロファイリング](Profiling.md) を参照してください。

## 変数を自分で探す

| コマンド | 効果 |
|---|---|
| `help` | すべてのコンソール変数とコマンドをログに出力する |
| 名前の一部を入力して Tab | コンソールでの自動補完 |
| 値なしで `<変数>` | 現在の値とヘルプを表示する |
| `DumpConsoleCommands` | コマンドの一覧を表示する |

<warning>
エンジンのヘルプは古いことがあります。HBAO+ の DX11 専用という記述はその一例です。挙動とヘルプが食い違う場合は、ソースが正しい情報源です。
</warning>

## 関連項目

- [コンパイル時スイッチ](Compile-Time-Switches.md)
- [エンジンの既定値の変更](Engine-Defaults.md)
- [プロファイリング](Profiling.md)
- [用語集](Glossary.md)
