# レイトレーシング半透明とコースティクス

<tldr>
<p>
ハイブリッド半透明により、ラスタライズとレイトレーシングの半透明を共存させられます。推奨する高品質な構成は
<code>r.RayTracing.Translucency 3</code> と吸収の組み合わせです。メッシュコースティクスとウォーターコースティクスは別のシステムで、それぞれ <code>r.RayTracing.MeshCaustics.Enable</code> と <code>r.RayTracing.WaterCaustics.Type</code>
で有効にします。
</p>
</tldr>

<img src="RTOfficeScene.jpg" alt="ボリュメトリックライト、半透明の球体、レイトレーシングの反射と屈折を組み合わせたオフィスシーン" border-effect="line"/>

*NVIDIA のサンプルコンテンツのオフィスシーンは、パーティクル、半透明の反射と屈折、メッシュコースティクス、レイトレーシング GI を 1 つのフレームで同時に使い、スタック全体を試すことができます。*

これらの機能は、Vite のベースである NVIDIA の NvRTX 4.27 Caustics ブランチから来ています。レンダラーの中で最もパラメーターの多い部分なので、このページは読み物ではなくリファレンスとして構成しています。

<warning>
<b>このページの内容はすべて、既定のビルドではコンパイル対象から外れています。</b> <code>VITE_RT_PSO_DEBLOAT</code> が既定値の <code>1</code> のとき、レイトレーシング半透明、メッシュコースティクス、ウォーターコースティクスのシェーダーパーミュテーションはすべて取り除かれます。コンソール変数の設定は成功しますが、何も描画されません。
<p>
使うには <code>VITE_RT_PSO_DEBLOAT=0</code> で再ビルドしてください。
<a href="Compile-Time-Switches.md">コンパイル時スイッチ</a> を参照してください。
</p>
</warning>

これらはレイトレーシングのエフェクトの中で最も重く、どれも 4K での Vite の [パフォーマンス目標](Performance-Targets.md)
には収まりません。NvRTX の系譜にこれらが含まれていて、シネマティクス、宣伝用のキャプチャ、特定の見せ場のために使いたいプロジェクトもあるため、ここで説明しています。

> NvRTX Caustics ブランチから受け継いだ RTX 機能のコードとアートアセットは、すべて
> [GameWorks のライセンス](https://developer.nvidia.com/gameworks-source-sdk-eula) の対象です。
>
{style="note"}

## 半透明のモード

標準の UE4 のレイトレーシング半透明は、*すべての* 半透明をレイトレーシングのパイプラインに通します。そのため、Cascade のパーティクルなど対応していないプリミティブの種類が消え、ラスタライズ向けに作成したコンテンツと直感に反する形で相互作用する屈折の挙動になります。ハイブリッド半透明はこれを解決します。

| `r.RayTracing.Translucency` | モード |
|---|---|
| `0` | 標準の UE4 のレイトレーシング半透明を無効 |
| `1` | 標準の UE4 のレイトレーシング半透明を有効 |
| `2` | ハイブリッド半透明 1 &mdash; レイトレーシングによる半透明の反射のみ |
| `3` | ハイブリッド半透明 2 &mdash; レイトレーシングによる半透明の反射と屈折 |

ハイブリッドのモードはベースの半透明シェーダーのパーミュテーションを増やすため、プロジェクト設定の
**Hybrid Translucency** のチェックボックスが必要です。対応するシェーダーのサポートのスイッチは
`r.RayTracing.HybridTranslucencySupport` です。

### モード 2 &mdash; 反射のみ

複数の半透明の層をオフスクリーンのサーフェスにトレースし、通常のラスタライズの半透明の一部として合成します。完全なレイトレーシング半透明と比べると順序に依存しない透明度と屈折は失われますが、それらの点ではラスタライズより悪くはならず、レイトレーシングによる反射とシェーディングが得られます。

| コンソール変数 | 用途 |
|---|---|
| `r.RayTracing.Translucency.HybridLayers` | 追跡する、重なり合うレイトレーシング半透明の層の数 |
| `r.RayTracing.Translucency.HybridDepthThreshold` | ジオメトリを別の半透明の層とみなすワールド空間での距離。小さすぎるとハイブリッド半透明が現れないか Z ファイティングのアーティファクトが生じ、大きすぎると重なった層が誤って統合されます。 |
| `r.RayTracing.Translucency.HalfRes` | 0 はフル解像度、1 は垂直方向に半分（インターリーブ）、2 は半分のチェッカーボード（4 タップ）、3 は半分のチェッカーボード（2 タップ垂直） |

### モード 3 &mdash; 反射と屈折

ラスタライズと *完全な* レイトレーシング半透明を組み合わせ、反射、屈折、OIT に対応します。Cascade のパーティクルも、レイトレーシング半透明の利点を損なわずに共存できます。このモードでは順序に依存しない透明度が自動的に適用されます。

半透明のメッシュには、吸収と組み合わせたこのモードを推奨します。

最高の画質のための推奨設定:

```
r.RayTracing.Translucency.Refraction 1
r.RayTracing.Translucency.HybridLayers 5
r.RayTracing.Translucency.MaxRefractionRays 5
```

4.27 では、モード 3 で RT 屈折を有効にすると、マテリアルごとの IOR は PBR ベースの屈折率の入力に結び付けられます。マテリアルの Refraction Mode の入力は **Index Of Refraction** に設定する必要があります。

モード 3 では、半透明のスタティックメッシュをレイトレーシングに参加させるかどうかをメッシュごとに選ぶこともできます。レイトレーシングから除外したメッシュはラスタライズで描画されるため、同じシーンでレイトレーシングとラスタライズの半透明を混在させられ、レイトレーシングのパイプラインの負荷を減らして性能を改善できます。

モード 3 についての追加の注意点:

- `r.RayTracing.Translucency.HybridDepthThreshold` は適用されません。層の順序を決める際の深度のバイアスには、代わりに
  `r.RayTracing.Translucency.PrimaryRayBias` を使ってください。
- 不透明なメッシュを生成する Cascade と Niagara のエミッターは、レイトレーシング半透明のメッシュに完全に遮蔽されると消えることがあります。一部のパーティクルの種類が、ハードウェアレイトレーシングに必要な BVH のデータを生成できないためです。これは標準の UE4 の既知の挙動で、ハイブリッドモード 2 でも変わりません。
- 半分の解像度の屈折は `r.RayTracing.Translucency.HalfRes` で利用できます。0 はフル解像度、1 は重み付きの色の再構成による半分のチェッカーボード、2 はフレーム間での半分のチェッカーボード、3 は平均色の再構成による半分のチェッカーボードです。これらの再構成の手法は TAA での使用を想定しており、ピクセル単位の再構成のアーティファクトを増幅しうる DLSS では慎重な調整が必要です。

## 半透明の吸収

吸収を有効にすると、同じマテリアルでできた厚いオブジェクトほど透明度が下がって見えます。これは物理的に正しい挙動で、ガラスや液体で大きな品質の向上になります。吸収はマテリアルごとのオプションなので、吸収を使うオブジェクトと使わないオブジェクトを一緒に描画できます。

<procedure title="半透明の吸収を有効にする" id="enable-absorption">
    <step>レイトレーシング半透明が有効であることを確認します。</step>
    <step><code>r.RayTracing.Translucency.EnableAbsorption 1</code> を設定するか、ポストプロセスボリュームで <b>Enable Absorption</b> にチェックを入れます。</step>
    <step>マテリアルエディタで、吸収を使うマテリアルごとに <b>Ray Traced Translucency Absorption</b> にチェックを入れます。</step>
</procedure>

スループットによるカリングで、寄与の小さいレイのパスを捨ててコストを減らせます。

| コンソール変数 | 用途 |
|---|---|
| `r.RayTracing.Translucency.MinRefractionThroughput` | 値を大きくするほど多くの屈折レイをカリングします。アーティファクトが出ることがあります。 |
| `r.RayTracing.Translucency.MinReflectionThroughput` | 値を大きくするほど多くの反射レイをカリングします。アーティファクトが出ることがあります。 |
| `r.RayTracing.PrimaryRays.AbsorptionForceShadingOnOpaqueObjects` | 1 に設定すると、アクターが背景を遮る透明な反射での二重シェーディングのアーティファクトを解消します。 |

## プライマリレイによる被写界深度

ラスタライズの被写界深度は、特に Cascade のパーティクルが半透明のガラスと交差する部分で、半透明の扱いが苦手です。レイトレーシングを使うと、正確なシネマティックの DOF を実現できます。

<procedure title="レイトレーシングによる被写界深度を有効にする" id="enable-rt-dof">
    <step>シネカメラを使い、通常どおり被写界深度を適用します。</step>
    <step>
        半透明のパーティクルを含め、カメラの視錐台に入るすべての半透明マテリアルを集めます。それぞれのルートマテリアルで
        <b>Output Translucency Depth</b> にチェックを入れ、<b>Translucency Depth Opacity Threshold</b> がマテリアルインスタンスの不透明度のパラメーターより小さいことを確認します。
    </step>
    <step><code>r.RayTracing.PrimaryRays.IncludeDOF 1</code> を設定します。</step>
</procedure>

RT DOF と併せて、強化された半透明のモード 3、RT による半透明の反射と屈折、半透明の吸収の使用を強く推奨します。DLSS には自動的に対応しています。

## メッシュコースティクス

半透明やメタリックのオブジェクトに対して、インタラクティブなコースティクスを描画します。UE4 の 4 種類のライトすべて、複数の光源、反射と屈折のコースティクス、分散、ソフトコースティクスに対応しています。

<img src="MeshCaustics.jpg" alt="タイルの表面に投影されたレイトレーシングの屈折コースティクスを示す POV-Ray の Glasses シーン" border-effect="line"/>

*POV-Ray の Glasses シーン。タイル上の明るい模様はすべて、作成したものではなくトレースした屈折のコースティクスです。*

<img src="CausticsDispersion.jpg" alt="レイトレーシングの分散によって白い光線をスペクトルに分けるプリズム" border-effect="line"/>

*分散。マテリアルのルートノードで **Ray Traced Caustics Dispersion Amount** を 0 より大きくし、`r.RayTracing.MeshCaustics.EnableDispersion 1` を設定する必要があります。*

<procedure title="メッシュコースティクスを有効にする" id="enable-mesh-caustics">
    <step>レイトレーシングを有効にします。</step>
    <step>ポストプロセスボリュームの <b>Ray Tracing Mesh Caustics</b> にある <b>Enabled</b> にチェックを入れるか、<code>r.RayTracing.MeshCaustics.Enable 1</code> を設定します。</step>
    <step>ライトのプロパティで <b>Cast Mesh Caustics</b> にチェックを入れます。</step>
    <step>
        メタリックのマテリアルでは <b>Cast Ray Traced Reflection Caustics</b> にチェックを入れます。半透明のオブジェクトでは、反射のコースティクスには <b>Cast Ray Traced Reflection Caustics</b>、屈折のコースティクスには
        <b>Cast Ray Traced Refraction Caustics</b> にチェックを入れます。
    </step>
</procedure>

### 機能の設定

コンソール変数を `-1` に設定した場合は、ポストプロセスボリュームが実際の値を決めます。

| コンソール変数 | 用途 |
|---|---|
| `r.RayTracing.MeshCaustics.EnableTranslucentReflection` | 透明なオブジェクトの反射のコースティクス |
| `r.RayTracing.MeshCaustics.TranslucentReflectionMode` | 0 は屈折のみ、1 は屈折と最初のバウンスでの反射、2 は任意のバウンス数での反射 |
| `r.RayTracing.MeshCaustics.EnableDispersion` | 分散を有効にします。マテリアルのルートノードで **Ray Traced Caustics Dispersion Amount** を 0 より大きくする必要があります。 |
| `r.RayTracing.MeshCaustics.DispersionSamples` | 分散に使う色のサンプル数 |
| `r.RayTracing.MeshCaustics.SoftCausticsSample` | ソフトコースティクスのサンプル数。ライトの設定で **Mesh Caustics Softness** を 0 より大きくする必要があります。 |
| `r.RayTracing.MeshCaustics.EnableAdvancedSoftCaustics` | より高品質なソフトコースティクスのアルゴリズム |

マテリアルインスタンスごとに分散の量を公開するには、**Ray Traced Caustics Use CustomData 0 As Dispersion Amount** にチェックを入れ、Custom Data 0 のチャンネルにスカラーを接続します。これで実行時にパラメーターを調整できます。

### 性能の調整

性能の鍵はフォトン数の制限です。ビューモードを **Ray Tracing Debug &rarr; Mesh Caustics Debug Data** に設定し、**Debug Light Data Type** を **Photon Count** にします。一般的なケースでは、約 10 万個のフォトンで十分な結果が得られます。多すぎる場合は、ポストプロセスボリュームで **Adaptive Photon Size** を大きくして **Adaptive Variance Gain** を小さくし、コースティクスが消え始めるまで **Final Cull Threshold** と **Mid Cull Threshold** を上げます。

| コンソール変数 | 用途 |
|---|---|
| `r.RayTracing.MeshCaustics.FinalCullColorThreshold` | 寄与の小さいレイをカリング |
| `r.RayTracing.MeshCaustics.MidCullColorThreshold` | 寄与の小さいレイをカリング |
| `r.RayTracing.MeshCaustics.BufferScale` | -1 はポストプロセスボリューム、0 はフル、1 は半分、2 は 4 分の 1 の解像度 |
| `r.RayTracing.MeshCaustics.AdaptivePhotonSize` | 目標とするスクリーン空間でのフォトンのサイズ。小さいほど詳細で高価になります。 |
| `r.RayTracing.MeshCaustics.AdaptiveVarianceGain` | 値を大きくするとちらつきを抑えます |
| `r.RayTracing.MeshCaustics.EnableTemporalFilter` | ちらつきを減らす時間方向のフィルタリング |
| `r.RayTracing.MeshCaustics.TemporalStrength` | 大きいほど安定しますが、遅れやゴーストが生じることがあります |
| `r.RayTracing.MeshCaustics.MaxTraceDepth` | バウンス数を制限し、半透明のオブジェクトでの性能を上げます |

## ウォーターコースティクス

池から外洋まで、水域のインタラクティブなコースティクスを描画します。4 種類すべてのライト、複数のライト、反射と屈折のコースティクス、分散、ソフトコースティクス、カスケードのコースティクスマップに対応しています。

<img src="WaterCaustics.jpg" alt="キャラクターが水面を乱し、レイトレーシングのウォーターコースティクスで照らされたプールの底" border-effect="line"/>

*1 つのディレクショナルライトでの Swimming Pool シーン。コースティクスは毎フレーム水面のメッシュに対してトレースされるため、水面の乱れに反応します。*

<procedure title="ウォーターコースティクスを有効にする" id="enable-water-caustics">
    <step>レイトレーシングを有効にします。</step>
    <step>ポストプロセスボリュームでウォーターコースティクスの種類を選ぶか、<code>r.RayTracing.WaterCaustics.Type</code> を 1 または 2 に設定します。</step>
    <step>ライトのプロパティで <b>Cast Water Caustics</b> にチェックを入れます。</step>
    <step>
        水面のスタティックメッシュアクターで、Ray Tracing タブの <b>Evaluate Ray Tracing Water Caustics</b> にチェックを入れます。水面のマテリアルは Translucent のブレンドモードでなければなりません。
    </step>
</procedure>

### アルゴリズムの選び方

**Photon Difference Scattering（タイプ 1）** は柔軟で、UE4 が対応するすべてのライトの種類で動作します。くっきりした模様を得るには比較的高解像度のコースティクスマップが必要なため、海や大きな湖のような広いサーフェスでは、カスケードのコースティクスマップを併用してください。カスケードによって、カメラの近くではコースティクスをくっきり保ちつつ、遠くではより安価に描画できます。

**Procedural Caustic Mesh（タイプ 2）** は、比較的低解像度のマップでも非常にくっきりしたコースティクスを生成します。カスケードのコースティクスマップを必要としないため、それとは組み合わせられません。通常は PDS より高速ですが、エリアライトには対応しておらず、コースティクスを受けるオブジェクトの縁にアーティファクトが残ることがあります。

### 設定

| コンソール変数 | 用途 |
|---|---|
| `r.RayTracing.WaterCaustics.MaxReflectionRayDistance` | 0 にすると反射のコースティクスを無効化 |
| `r.RayTracing.WaterCaustics.MaxRefractionRayDistance` | 0 にすると屈折のコースティクスを無効化 |
| `r.RayTracing.WaterCaustics.MapCascades` | カスケード数（最大 4 段階）。タイプ 1 のみ。 |
| `r.RayTracing.WaterCaustics.MapSizeX` / `MapSizeY` | コースティクスマップのサイズ。既定値 2048。小さな池なら 1024 で十分なことが多く、大幅に性能を節約できます。 |
| `r.RayTracing.WaterCaustics.NumDenoisePasses` | 既定値 2。0 にするとよりくっきりした結果になります。 |
| `r.RayTracing.WaterCaustics.UseSceneLightDir` | 0 にすると、ライトの方向ではなくカメラの上方からコースティクスマップをキャプチャします。ディレクショナルライトのみ。 |
| `r.RayTracing.WaterCaustics.BufferScale` | 1 はフル、2 は半分、4 は 4 分の 1 の解像度 |
| `r.RayTracing.WaterCaustics.PhotonScale` | PDS での初期のフォトンサイズ。既定値 3。 |
| `r.RayTracing.WaterCaustics.ShowPhoton` | デバッグ用: フォトンを点として描画 |
| `r.RayTracing.WaterCaustics.RefractBackFaceCullingThreshold` | -0.5 程度に設定すると、ひびや継ぎ目が現れる部分の面法線を無視します |
| `r.RayTracing.WaterCaustics.ReflectBackFaceCullingThreshold` | 上と同様、反射のコースティクス用 |

ウォーターコースティクスを 1 つの動的なライトに限定すると、大きく性能を節約できます。ライトの距離によるカリングと強度のフェードにも完全に対応しています。

コースティクスの焦点はメッシュと法線の強さに依存します。大きな波や強い法線マップの値は、より劇的なコースティクスを生みます。分散を有効にするには、ポストプロセスボリュームで **Dispersion Intensity** を上げ、**Dispersion Offset** を調整します。

## サンプルコンテンツ

NVIDIA は、これらの機能のプロジェクトファイルとパッケージ化したデモを提供しています。

- [すべてのプロジェクトファイル](https://drive.google.com/drive/folders/1MfJ1rLqwx8acdscFfQtaYOR2Cdm1WPz9?usp=sharing)
- [すべてのパッケージ化したデモ](https://drive.google.com/drive/folders/1yHFOtmZWVDof8GbfZJMeazfb927ahTDn?usp=sharing)

個別のシーン: 屈折の多い POV-Ray の Glasses シーン、プリズムによる分散のデモ、ウォーターコースティクスの
Swimming Pool シーン、そしてこのページの冒頭に示した、パーティクル、反射、屈折、メッシュコースティクス、RTGI を組み合わせたオフィスシーンです。このマニュアルの [廃アパートメント](Abandone-Apartment.md) と [屋根裏シーン](Attic-Scene.md) も参照してください。

## 関連項目

- [レイトレーシング](Ray-Tracing.md)
- [レイトレーシング反射](RT-Reflections.md)
- [アップスケーラー](Upscalers.md)
- [コンソール変数](Console-Variables.md)
