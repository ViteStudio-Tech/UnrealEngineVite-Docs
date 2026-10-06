# レンダリング

<tldr>
<p>
Vite のレンダラーは、特定のライティング手法に依存しない DXR レイトレーシングパイプラインを備えた、SM5 のディファードレンダラーです。グローバルイルミネーションは Lumen ではなく <a href="DDGI-Dynamic.md">DDGI</a>、ジオメトリのディテールは Nanite ではなく <a href="Tessellation.md">テッセレーション</a>、アンチエイリアシングは時間的再構成ではなくネイティブ解像度と <a href="Anti-Aliasing.md">SMAA</a> を基本とします。
</p>
</tldr>

レンダリングは、Vite が標準の Unreal Engine 4.27 と UE5 の両方から最も大きく異なる部分であるため、このマニュアルで最大のセクションになっています。

## レンダラーの構成

パイプラインは Unreal Engine 4.27 のディファードレンダラーで、NvRTX Caustics の DirectX 12 と DXR の改良を受け継ぎ、その上に Vite 独自の追加機能を重ねています。構造上の重要な特性は、レイトレーシングパイプラインが *手法に依存しない*
ことです。アクセラレーション構造は特定のライティング手法とは無関係に構築・更新されるため、DDGI、RTXDI、各種 RT
エフェクトが共存でき、それぞれを独立して有効にできます。

これは、レイトレーシングのシーン構築が Lumen、Nanite、GPU Scene と結合している UE 5.1 以降の構成とは正反対です。[なぜ NvRTX 4.27 なのか](Why-NvRTX-427.md) を参照してください。

> 新規プロジェクトはレイトレーシングのサポートと動的 DDGI が有効な状態で始まります。レイトレーシングの反射、
> シャドウ、アンビエントオクルージョンはオプトインで、半透明、コースティクス、RTXDI、パストレーシングは既定で
> コンパイル対象から外れています。どのエフェクトを有効にするかは意識的に決めてください。
> [レイトレーシング](Ray-Tracing.md) を参照してください。
>
{style="note"}

## セクションの内容

### グローバルイルミネーション

- [グローバルイルミネーション](Global-Illumination.md) &mdash; 利用できる GI ソリューションの選び方
- [動的 DDGI](DDGI-Dynamic.md) &mdash; リアルタイムのレイトレーシングによるイラディアンスプローブボリューム
- [静的 DDGI](DDGI-Static.md) &mdash; ほぼ一瞬でベイクできるプローブボリューム
- [SSGI](SSGI.md) &mdash; スクリーンスペース GI と、それを DDGI と併用すべき理由

### レイトレーシング

- [レイトレーシング](Ray-Tracing.md) &mdash; 概要と主要なスイッチ
- [レイトレーシング反射](RT-Reflections.md)
- [レイトレーシングシャドウとアンビエントオクルージョン](RT-Shadows-And-Ambient-Occlusion.md)
- [レイトレーシング半透明とコースティクス](RT-Translucency-And-Caustics.md)
- [RTXDI](RTXDI.md) &mdash; 多数のライトがあるシーンのためのレイトレーシングによる直接光
- [パストレーシング](Path-Tracing.md)

### サーフェスとジオメトリ

- [シェーディングモデル](Shading-Models.md) &mdash; Callisto BRDF とトゥーンを含む
- [テッセレーション](Tessellation.md)
- [ヘアレンダリング](Hair-Rendering.md) &mdash; TressFX

### 画質

- [アンチエイリアシング](Anti-Aliasing.md) &mdash; SMAA、FXAA、TAA、MSAA
- [アップスケーラー](Upscalers.md) &mdash; DLSS、FSR、XeSS、NIS
- [アンビエントオクルージョン](Ambient-Occlusion.md) &mdash; SSAO の高速パスと HBAO+
- [カラーマネジメント](Color-Management.md) &mdash; ACES、トーンマッピング、HDR 出力

## レンダリング構成の選び方

適切な出発点はパフォーマンス目標によって決まります。以下は [パフォーマンス目標](Performance-Targets.md) にある
4 つの目標の背後にある構成です。

| 目標 | GI | 反射 | シャドウ | AO | ジオメトリ | AA |
|---|---|---|---|---|---|---|
| スタイライズド 4K120 | 動的 DDGI | ラスター / SSR | カスケード | SSAO の高速パス | LOD | SMAA / TAA |
| パフォーマンス 4K60 | DDGI + SSGI | レイトレーシング | カスケード | SSAO / HBAO+ | テッセレーション | TAA / SMAA |
| フィデリティ 4K30 | DDGI + SSGI | レイトレーシング | カスケード | HBAO+ | テッセレーション | TAA |
| フル RT 1440p30 | DDGI + SSGI | レイトレーシング | レイトレーシング | RTAO | テッセレーション | TAA |
| RT 非対応のハードウェア | 静的 DDGI | SSR | カスケード | SSAO | LOD | TAA / SMAA / FXAA |

どれも処方箋ではなく出発点です。各構成のコンソール変数は対応するページで説明しており、[コンソール変数](Console-Variables.md) にもまとめています。

## 関連項目

- [パフォーマンス目標](Performance-Targets.md)
- [プロファイリング](Profiling.md)
- [シェーダーコンパイルと PSO](Shader-Compilation-And-PSO.md)
- [コンソール変数](Console-Variables.md)
