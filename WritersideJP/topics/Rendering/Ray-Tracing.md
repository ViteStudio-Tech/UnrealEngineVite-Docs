# レイトレーシング

<tldr>
<p>
Vite には NvRTX 4.27 Caustics と NvRTX 5.0 のレイトレーシング一式が含まれています。既定のビルドでは
<b>反射、シャドウ、アンビエントオクルージョン、スカイライトが利用でき、それ以外は <code>VITE_RT_PSO_DEBLOAT</code> によってコンパイル対象から外れています</b>。何も起きないように見えるコンソール変数をデバッグする前に、下の利用可否の表を確認してください。
</p>
</tldr>

<img src="AtticRTGIV2.jpg" alt="レイトレーシング GI でライティングされた屋根裏の室内。窓から差し込む光の筋と、木の床に広がる柔らかなバウンス光" border-effect="line"/>

*レイトレーシング GI を使った屋根裏シーン。プロジェクトは [屋根裏シーン](Attic-Scene.md) を参照してください。*

Vite のレイトレーシングは、特定の手法に依存しないパイプラインです。アクセラレーション構造は特定のライティング手法とは独立して管理されるため、各エフェクトを個別に有効・無効にできます。これは UE 4.27 にはあり、UE 5.1 以降で失われた構成です。[なぜ NvRTX 4.27 なのか](Why-NvRTX-427.md) を参照してください。

## 利用可否

コンパイル時スイッチ `VITE_RT_PSO_DEBLOAT` は既定で `1` で、Vite の推奨構成に含まれないエフェクトのシェーダーパーミュテーションを取り除きます。レイトレーシングの PSO はコンソール変数の設定に関係なくコンパイルとバインドが必要なため、使わないエフェクトをコンパイルに含めておくと、シェーダーのビルド時間、パッケージサイズ、パイプラインの生成時間を無駄に消費します。

実際の影響は次のとおりです。**コンパイル対象から外れたエフェクトのコンソール変数を設定すると、成功したように見えて何も描画されません。**

| エフェクト | コンソール変数 | 既定のビルド | ページ |
|---|---|---|---|
| 反射 | `r.RayTracing.Reflections` | 利用可能 | [レイトレーシング反射](RT-Reflections.md) |
| シャドウ | `r.RayTracing.Shadows` | 利用可能 | [RT シャドウと AO](RT-Shadows-And-Ambient-Occlusion.md) |
| アンビエントオクルージョン | `r.RayTracing.AmbientOcclusion` | 利用可能 | [RT シャドウと AO](RT-Shadows-And-Ambient-Occlusion.md) |
| スカイライト | `r.RayTracing.SkyLight` | 利用可能 | このページ |
| 半透明 | `r.RayTracing.Translucency` | コンパイル対象外 | [RT 半透明とコースティクス](RT-Translucency-And-Caustics.md) |
| メッシュコースティクス | `r.RayTracing.MeshCaustics.Enable` | コンパイル対象外 | [RT 半透明とコースティクス](RT-Translucency-And-Caustics.md) |
| ウォーターコースティクス | `r.RayTracing.WaterCaustics.Type` | コンパイル対象外 | [RT 半透明とコースティクス](RT-Translucency-And-Caustics.md) |
| サンプリングによる直接光（RTXDI） | `r.RayTracing.SampledDirectLighting` | コンパイル対象外 | [RTXDI](RTXDI.md) |
| ピクセル単位のグローバルイルミネーション | `r.RayTracing.GlobalIllumination` | コンパイル対象外 | このページ |
| リフレクションキャプチャとプローブ | `r.RayTracing.Reflections.RayTraceEnvironmentCaptures` | コンパイル対象外 | [レイトレーシング反射](RT-Reflections.md) |
| パストレーシング | `ShowFlag.PathTracing`（ビューモード） | コンパイル対象外 | [パストレーシング](Path-Tracing.md) |

コンパイル対象外のものを使うには、`VITE_RT_PSO_DEBLOAT=0` で再ビルドしてください。[コンパイル時スイッチ](Compile-Time-Switches.md) を参照してください。

**利用可能であることと有効であることは別です。** 現行のリリースでは、`r.RayTracing.Reflections`、`r.RayTracing.Shadows`、`r.RayTracing.AmbientOcclusion`、`r.RayTracing.Translucency` の既定値はすべて `0` です。これらのエフェクトはコンパイルに含まれていても無効の状態で始まり、プロジェクトやポストプロセスボリュームで有効にします。例外は動的 DDGI で、`BaseEngine.ini` の `r.GlobalIllumination.ExperimentalPlugin=True` により既定で有効です。

反射には、利用可能な場合でももう 1 つ注意点があります。デブロートのスイッチは、ソート済みのディファード反射のアルゴリズムを強制し、古い非ディファードのパスをコンパイル対象から外します。

動的 DDGI は `r.RayTracing.*` のグループではなく `r.GlobalIllumination.ExperimentalPlugin` で有効にする別のシステムで、デブロートのスイッチの影響を **受けません**。[動的 DDGI](DDGI-Dynamic.md) を参照してください。

これは Black Myth: Wukong が出荷に使ったレンダリングスタックです。

[![Black Myth: Wukong のレイトレーシング比較](https://img.youtube.com/vi/A5boaueGopg/0.jpg)](https://www.youtube.com/watch?v=A5boaueGopg)

## 有効化と無効化

コードからは次のようにします。

```c++
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.AmbientOcclusion"))->Set(1);
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.Reflections"))->Set(1);
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.Shadows"))->Set(1);
```

出荷するプロジェクトでは、設定ファイルで指定します。

```ini
; Config/DefaultEngine.ini
[/Script/Engine.RendererSettings]
r.RayTracing.Reflections=1
r.RayTracing.Shadows=0
r.RayTracing.AmbientOcclusion=0
r.RayTracing.Translucency=0
```

`r.RayTracing.ForceAllRayTracingEffects 1` はすべてを一度に有効にします。上限を確認したり、シーンがどのエフェクトに反応するかを調べたりするための診断用として扱い、出荷用の設定にはしないでください。`r.RayTracing.ForceAllRayTracingEffects 0` はすべてを強制的に無効にし、フレームタイムのうちレイトレーシングが占める割合を最も早く把握できます。

## カリングとコストの制御

レイトレーシングのコストはアクセラレーション構造に含まれるジオメトリの量に比例するため、エフェクトの品質を下げる前にまずカリングを検討します。

```ini
; Config/DefaultEngine.ini
[SystemSettings]
r.RayTracing.Culling=1
r.RayTracing.Culling.Radius=10000
r.RayTracing.Culling.Angle=1
```

標準の 4.27 と同じく、カリングは既定で無効です。有効にすると、カメラの後ろにあるオブジェクトのうち、半径（ここでは
100&nbsp;m）より遠いもの、または角度のしきい値より小さいものがアクセラレーション構造から外れます。直接見える画面は影響を受けませんが、それらのオブジェクトの反射とレイトレーシングのシャドウは影響を受けるため、プレイヤーの後ろにある鏡や大きなシャドウの投影元を確認してください。[エンジンの既定値の変更](Engine-Defaults.md#ray-tracing-culling) を参照してください。

カリング以外の標準的な手段を、おおよそ効果の大きい順に示します。

1. 有効にするエフェクトの数を減らします。エフェクトを無効にするほうが、最適化するより常に安価です。
2. エフェクトの解像度を下げます。ほとんどのエフェクトは半分または 4 分の 1 の解像度のバッファに対応しています。
3. サンプル数と最大バウンス数を減らします。
4. レイトレーシングに参加するジオメトリをプリミティブ単位で減らします。

## AMD のハードウェア

Vite は AMD GPUOpen の RT 最適化と、コンソールを対象とした AMD RDNA 固有の独自 GPU 最適化を多数統合しています。PS5 クラスのパフォーマンス目標から直接導かれることとして、RDNA2 のハードウェアでのレイトレーシング性能は後回しではなく最優先の関心事です。

### RDNA ベースのコンソールと携帯機

| ハードウェア | GPU アーキテクチャ | GPU の構成 |
|---|---:|---|
| PlayStation 5 | RDNA 2 ベースのカスタム GPU | 36 CU、最大 10.28 TFLOPS |
| PlayStation 5 Pro | RDNA ベースのカスタム GPU* | 60 CU、16.7 TFLOPS |
| Xbox Series X | RDNA 2 | 52 CU、12 TFLOPS |
| Xbox Series S | RDNA 2 | 20 CU、4 TFLOPS |
| Steam Deck / Steam Deck OLED | RDNA 2 | 8 CU、最大 1.6 GHz |
| ASUS ROG Ally | RDNA 3 | Z1: 4 CU、Z1 Extreme: 12 CU |
| ASUS ROG Ally X | RDNA 3 | 12 CU（Ryzen Z1 Extreme） |
| ROG Xbox Ally | RDNA 3 | 8 CU（Ryzen Z2 A） |
| ROG Xbox Ally X | RDNA 3.5 | 16 CU（Ryzen AI Z2 Extreme） |
| Valve Steam Machine（2026 年） | RDNA 3 | セミカスタム GPU、28 CU、最大 2.45 GHz |

\*Sony は PS5 Pro の GPU を公式に「AMD Radeon RDNA ベース」としています。PC の RDNA 3.5 の仕様を超える機能を備え、RDNA 4 の特定の技術を受け継いでいます。

### 主要な Android フラッグシップ: Exynos Xclipse GPU を搭載した Samsung Galaxy

| Galaxy の機種 | SoC | Xclipse GPU | RDNA アーキテクチャ | 提供地域 |
|---|---|---|---|---|
| Galaxy S22 | Exynos 2200 | Xclipse 920 | RDNA 2 | 一部の地域 |
| Galaxy S22+ | Exynos 2200 | Xclipse 920 | RDNA 2 | 一部の地域 |
| Galaxy S22 Ultra | Exynos 2200 | Xclipse 920 | RDNA 2 | 一部の地域 |
| Galaxy S23 FE | Exynos 2200 | Xclipse 920 | RDNA 2 | 一部の地域 |
| Galaxy S24 | Exynos 2400 | Xclipse 940 | RDNA 3 | 一部の地域 |
| Galaxy S24+ | Exynos 2400 | Xclipse 940 | RDNA 3 | 一部の地域 |
| Galaxy S24 FE | Exynos 2400e | Xclipse 940 | RDNA 3 | 全世界 |
| Galaxy Z Flip7 | Exynos 2500 | Xclipse 950 | RDNA 3 ベース | 全世界 |
| Galaxy S25 FE | Exynos 2400 | Xclipse 940 | RDNA 3 | 全世界 |
| Galaxy S26 | Exynos 2600 | Xclipse 960 | Samsung の新アーキテクチャ* | 一部の地域 |
| Galaxy S26+ | Exynos 2600 | Xclipse 960 | Samsung の新アーキテクチャ* | 一部の地域 |

\*Samsung は Xclipse 960 を、公開された AMD RDNA のバージョンではなく新しいアーキテクチャとして説明しています。

標準の Vite は Android でのレイトレーシングに **対応していません**。この表は今後の Vite のメジャーリリースのための参考資料です。現在の RDNA 向けの最適化は、これらの GPU での将来のあらゆるレンダリングパスに引き継がれます。

## ピクセル単位のレイトレーシング GI

<note>
既定のビルドではコンパイル対象から外れています。<code>VITE_RT_PSO_DEBLOAT=0</code> が必要です。
<a href="Compile-Time-Switches.md">コンパイル時スイッチ</a> を参照してください。
</note>

DDGI とは別に、Vite はピクセル単位のレイトレーシング GI のパスを、NvRTX の ReSTIR GI の改良とともに維持しています。新しい SVGF ベースのデノイザー、リザーバーリサンプリングによるファイナルギャザー、エミッシブマテリアルへの対応、4 分の 1 と 8 分の 1 の解像度のモード、メタリックマテリアルへの対応、そして法線のディテールを改善する球面調和関数です。

ハードウェアレイトレーシングの Lumen より高い品質のリファレンス画像を、やや高いコストで生成できます。一方で DDGI よりはるかに重く、DDGI がそもそも避けるために存在するデノイズと時間的な安定性の問題を再び持ち込みます。このトレードオフこそが、デブロートのスイッチが既定でこれを取り除く理由です。このパスは
[Vite ReSTIR](https://vitestudio-tech.github.io/UnrealEngineVite-Docs/tech/jp/restir.html) の基盤であり、Vite ReSTIR はこれを製品向けの GI とリアルタイムパストレーシングのソリューションへと発展させます。

使う場合の主要な設定:

- `r.RayTracing.GlobalIllumination.FinalGather.UseReservoirResampling 0/1` &mdash; 新しいファイナルギャザーのサンプラーを切り替えます。サンプラーのノイズを大幅に減らし、デノイズ前の結果をはるかに安定させるため、ピクセルあたりのサンプル数を減らせます。
- `r.DiffuseIndirect.Denoiser 2` &mdash; 新しい SVGF デノイザーを選択します。
- `r.RayTracing.GlobalIllumination.EvalSkyLight 0/1` &mdash; スカイライトの寄与を含めます。スカイライトのアクターの
  **Affect Global Illumination** フラグも設定する必要があります。
- `r.DiffuseIndirect.ApplyAO` &mdash; 間接光の結果に AO を適用します。ライティングのディテールが大きく向上するため、このパスを使う場合は強く推奨します。

一般的な用途では、ピクセルあたり 4 サンプルと `r.RayTracing.GlobalIllumination.ScreenPercentage` 12.5 で妥当な結果が得られます。

## 関連項目

- [グローバルイルミネーション](Global-Illumination.md)
- [レイトレーシング反射](RT-Reflections.md)
- [RT シャドウとアンビエントオクルージョン](RT-Shadows-And-Ambient-Occlusion.md)
- [RT 半透明とコースティクス](RT-Translucency-And-Caustics.md)
- [RTXDI](RTXDI.md)
- [コンパイル時スイッチ](Compile-Time-Switches.md)
- [コンソール変数](Console-Variables.md)
