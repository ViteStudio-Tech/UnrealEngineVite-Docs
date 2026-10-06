# コンパイル時スイッチ

<tldr>
<p>
<code>Engine/Source/Runtime/Core/Public/Misc/CoreDefines.h</code> にある 14 の <code>VITE_*</code> マクロが、コンソール変数ではなくコンパイル時に決まる機能を制御します。<b><code>VITE_RT_PSO_DEBLOAT</code> は既定で
<code>1</code> で、いくつかのレイトレーシングのエフェクトを完全にコンパイル対象から外します</b>。機能が壊れていると判断する前に、そのセクションを読んでください。
</p>
</tldr>

Vite の機能の中には、コンソール変数にできないものがあります。シェーダーのパーミュテーションの集合を変える（これはシェーダーのコンパイル時に決まります）か、実行時の分岐のほうが機能による節約より高くつくホットなコードパスを変えるためです。

## スイッチの一覧

以下の既定値は [ueVite26 September Major](ueVite26-SeptemberMajor.md) のリリースのものです。「導入」は、そのスイッチを含む `CoreDefines.h` が初めて入ったメジャーリリースです。

### レンダリングとレイトレーシング

| マクロ | 既定値 | 有効にしたときの効果 | 導入 |
|---|---|---|---|
| `VITE_RT_PSO_DEBLOAT` | `1` | パストレーシングと、Vite の主要な経路以外の重いレイトレーシングのパーミュテーションをコンパイル対象から外す | [June](ueVite26-JuneMajor.md) |
| `VITE_O_RT_REFLECTIONS` | `1` | ディファードのレイトレーシング反射の最適化。ペイロードは 64 バイトのまま | [August](ueVite26-AugustMajor.md) |
| `VITE_O_SSAO` | `1` | テクスチャサンプラーを使わない、Vite の最適化された SSAO のメモリアクセスの経路 | [June](ueVite26-JuneMajor.md) |
| `VITE_O_SSD_SAFE_SAMPLE_TRACK` | `1` | スクリーンスペースのデノイザーが `SampleTrackId` を VGPR に保持する（AMD で安全）。`0` で UE 5.0/5.1 の NVIDIA の占有率重視の経路に戻る | [August](ueVite26-AugustMajor.md) |
| `VITE_SPECULAR_OCCLUSION` | `0` | UE4 の Karis の項の代わりに、Jimenez 2016 のベントノーマルによるスペキュラーオクルージョンを使う | [August](ueVite26-AugustMajor.md) |
| `VITE_UE5_POSTPROCESSING` | `1` | UE 5.0 のローカル露出とポストプロセスのヒストグラムの経路 | [August](ueVite26-AugustMajor.md) |
| `VITE_NVRTX_TRANSLUCENCY_DEPTH` | `0` | NvRTX のブランチ由来の、独立した半透明の深度テクスチャ | [July](ueVite26-JulyMajor.md) |
| `VITE_DLSS_PATCH` | `0` | アップスケーリング時に、半透明とボリュメトリックフォグを出力解像度で処理する | [July](ueVite26-JulyMajor.md) |
| `VITE_FSR2_REACTIVE_MASK` | `0` | エンジン側での FSR 2 のリアクティブマスクのサポート | [July](ueVite26-JulyMajor.md) |

### シェーディングモデルとヘア

| マクロ | 既定値 | 有効にしたときの効果 | 導入 |
|---|---|---|---|
| `VITE_SHADINGMODEL_CALLISTO` | `0` | Callisto BRDF のシェーディングモデルをコンパイルに含める | [July](ueVite26-JulyMajor.md) |
| `VITE_SHADINGMODEL_TOON` | `0` | Toon のシェーディングモデルをコンパイルに含める | [July](ueVite26-JulyMajor.md) |
| `VITE_TRESSFX` | `0` | TressFX のストランドのヘアをコンパイルに含める | [July](ueVite26-JulyMajor.md) |

シェーディングモデルのスイッチは [July Major](ueVite26-JulyMajor.md) で追加されました。追加のモデルを既定でオフにしたことで、基準シーンは 235.56 FPS から 264.44 FPS（+12.3%）に向上しました。プロジェクトで使うモデルだけを有効にしてください。[シェーディングモデル](Shading-Models.md) と [ヘアレンダリング](Hair-Rendering.md) を参照してください。

### 物理とエディタ

| マクロ | 既定値 | 有効にしたときの効果 | 導入 |
|---|---|---|---|
| `VITE_PHYSX_FIXED_TIMESTEP` | `0` | 描画の補間を伴う、決定的な固定ステップの PhysX | [June](ueVite26-JuneMajor.md) |
| `VITE_UE4_ICON_BADGES` | `1` | アウトライナーのアイコンに UE4 スタイルのモビリティとスポーン可能のバッジを戻す。`0` で UE5 のラベルスタイル | [August](ueVite26-AugustMajor.md) |

それぞれ `#ifndef` のガードで定義されているため、ヘッダーを編集せずにビルドシステムからどれでも上書きできます。

## スイッチを上書きする

<procedure title="コンパイル時スイッチを変更する" id="override-switch">
    <step>
        プロジェクトの <code>Source/&lt;Project&gt;.Target.cs</code> を開きます。エンジン全体で変更する場合は、エンジンのターゲットファイルを開きます。
    </step>
    <step>
        <code>GlobalDefinitions</code> に定義を追加します。
        <code-block lang="c#">
public MyGameTarget(TargetInfo Target) : base(Target)
{
    Type = TargetType.Game;
    DefaultBuildSettings = BuildSettingsVersion.V2;
    ExtraModuleNames.Add("MyGame");

    GlobalDefinitions.Add("VITE_RT_PSO_DEBLOAT=0");
}
        </code-block>
    </step>
    <step>プロジェクトファイルを再生成します。</step>
    <step>
        エンジンを再ビルドします。<code>VITE_RT_PSO_DEBLOAT</code> など、シェーダーのパーミュテーションに影響するスイッチを変更した場合は、シェーダーキャッシュを消去してください。<a href="Cache-Management.md">キャッシュ管理</a>
        を参照してください。
    </step>
</procedure>

`CoreDefines.h` を編集するより、ターゲットファイルの `GlobalDefinitions` を使うほうを優先してください。ヘッダーを編集するとすべてのターゲットで値が変わり、エンジンのリポジトリとの差分が生まれて、マージのたびにそれを持ち越さなければならなくなります。

## VITE_RT_PSO_DEBLOAT

これは多くの人を驚かせるスイッチなので、最も詳しく説明します。

レイトレーシングのパイプラインステートオブジェクトは、見落としやすい形で高価です。使われる *可能性のある* レイ生成シェーダーのパーミュテーションはすべて、そのエフェクトが実行時にコンソール変数で無効になっていても、コンパイルされ、パッケージに含まれ、レイトレーシングのパイプラインにバインドされなければなりません。CVar を `0` にしても、そのシェーダーがなくなるわけではありません。その結果、シェーダーのコンパイル時間が長くなり、パッケージ化したビルドが大きくなり、PSO の数が増え、実行時のレイトレーシングのパイプラインの作成が遅くなります。

`VITE_RT_PSO_DEBLOAT` は、それ以外のすべてについて `ShouldCompilePermutation` から `false` を返すことで、パーミュテーションの集合を Vite が実際に出荷するエフェクトに絞り込みます。

### 既定値でコンパイル対象から外れるもの

`VITE_RT_PSO_DEBLOAT=1` では、次のエフェクトは **コンソール変数に関係なく利用できません**。

| エフェクト | 通常の制御 |
|---|---|
| ピクセルごとのレイトレーシングのグローバルイルミネーション | `r.RayTracing.GlobalIllumination` |
| RTXDI のサンプリングによる直接光 | `r.RayTracing.SampledDirectLighting` |
| パストレーシング | `r.PathTracing`、パストレーシングのビューモード |
| レイトレーシングの半透明 | `r.RayTracing.Translucency` |
| メッシュのコースティクス | NvRTX のコースティクスの CVar |
| 水のコースティクス | NvRTX の水のコースティクスの CVar |
| Single Layer Water のレイトレーシング反射 | `r.Water.SingleLayer.RTR` |
| レイトレーシングのリフレクションキャプチャとリフレクションプローブ | `r.RayTracing.Reflections.RayTraceEnvironmentCaptures` |

コンソール変数の設定は成功したように見えますが、エフェクトは描画されません。

### 引き続き動作するもの

| エフェクト | 備考 |
|---|---|
| レイトレーシング反射 | ソートされたディファードのアルゴリズムに固定されます。古いディファードではない経路はコンパイル対象から外れます。 |
| レイトレーシングシャドウ | 影響なし |
| レイトレーシングのアンビエントオクルージョン | 影響なし |
| レイトレーシングのスカイライト | 影響なし |
| DDGI | 影響なし。DDGI はプラグインであり、これらのパーミュテーションを通りません。 |

残る集合は、まさに Vite の推奨構成です。間接光には [DDGI](DDGI-Dynamic.md)、ディファードの経路による
[レイトレーシング反射](RT-Reflections.md)、そして [レイトレーシングシャドウと AO](RT-Shadows-And-Ambient-Occlusion.md)
です。そもそもなぜピクセルごとのレイトレーシング GI より DDGI を優先するのかは
[グローバルイルミネーション](Global-Illumination.md) を参照してください。デブロートのスイッチは、その推奨をビルドに組み込んだものです。

### 無効にする

[リファレンス画像](Path-Tracing.md) のためのパストレーシング、多数のライトがあるシーンのための RTXDI、あるいはレイトレーシングの半透明とコースティクスが必要な場合は、`VITE_RT_PSO_DEBLOAT=0` にして再ビルドしてください。

<warning>
これを無効にすると、シェーダーのコンパイル時間、パッケージ化したビルドのサイズ、レイトレーシングの PSO の数が大幅に増えます。全体で無効にするのではなく、別のターゲット構成を維持することを検討してください。社内のリファレンス描画用ビルドではデブロートを無効に、出荷ビルドでは有効にします。
</warning>

## VITE_O_SSAO

スクリーンスペースのアンビエントオクルージョンのパスで、Vite が書き直したメモリアクセスのパターンを有効にします。見た目は標準と同じで、コストは低くなります。

これらのスイッチの中では珍しく、実行時の CVar もあります。ただし開発用のビルドでのみです。

```
r.Vite.SSAO 0   // 標準の UE の経路
r.Vite.SSAO 1   // 最適化された経路
```

Shipping と Test のビルドはコンパイル時の値に固定され、そこには CVar が存在しません。実行時の切り替えは、開発中に
2 つの経路を A/B 比較するためにあり、最適化の検証もその方法で行いました。コンパイル時のスイッチをオフにする理由はありません。[アンビエントオクルージョン](Ambient-Occlusion.md) を参照してください。

## VITE_PHYSX_FIXED_TIMESTEP

既定ではオフです。描画の補間を伴う、決定的な固定ステップの PhysX のシミュレーションと、`p.VitePhysXFixedTimestep.*`
のコンソール変数を有効にします。

この機能は、物理シーン、サブステップのタスク、アニメーションの物理ブレンドに分岐とダブルバッファのトランスフォームの保存領域を追加するため、コンパイル時のゲートがあります。決定性を必要としないプロジェクトが、そのコストを払うべきではありません。詳しくは [固定タイムステップ](Fixed-Timestep.md) を参照してください。

## VITE_DLSS_PATCH

既定ではオフです。`TranslucencyAfterDOFUpscaledRT` と `TranslucencyAfterDOFModulateUpscaledRT` のメッシュパスを追加し、選択した半透明のプリミティブがアップスケーリングの後に出力解像度で描画されるようにします。また
`r.VolumetricFog.UseUpScaledSizeVolumetricFog` を追加し、フォグのグリッドを出力解像度から計算できるようにします。

アップスケーラーを有効にして出荷するプロジェクトにだけ関係します。[アップスケーラー](Upscalers.md) を参照してください。

## VITE_NVRTX_TRANSLUCENCY_DEPTH

既定ではオフです。NvRTX のブランチから受け継いだもので、独立した半透明の色と並んで、独立した半透明の深度テクスチャを確保して書き込みます。半透明の深度を必要とする一部の NvRTX のエフェクトに必要で、有効にするとレンダーターゲットが
1 つ増えます。

## VITE_SPECULAR_OCCLUSION

既定ではオフです。UE4 のスペキュラーオクルージョンの項（Karis の `GetSpecularOcclusion(NoV, RoughnessSq, AO)`）を、DFAO または SSAO のベントノーマルによる Jimenez ら 2016 のコーンとコーンのスペキュラーオクルージョンに置き換えます。くぼみの中やオブジェクトの下での反射の光漏れを減らします。

この定義は、イメージベースドライティングとレイトレーシング反射のシェーダーだけに対するコンパイル時の定数です。シェーダーのパーミュテーションでもグローバルなシェーダーの定義でもないため、PSO は増えません。変更するとそれらのシェーダーが再コンパイルされます。

## VITE_UE5_POSTPROCESSING

既定でオンです。UE 5.0 のローカル露出のパスと、それに対応するポストプロセスのヒストグラムとトーンマッパーの変更をコンパイルに含め、プロジェクトを UE5 に移さずに UE5 に匹敵するローカル露出の制御を提供します。

## シェーディングモデルと TressFX のスイッチ

`VITE_SHADINGMODEL_CALLISTO`、`VITE_SHADINGMODEL_TOON`、`VITE_FSR2_REACTIVE_MASK`、`VITE_TRESSFX` は既定でオフです。追加のシェーディングモデルはそれぞれ、共有のライティングのシェーダーに分岐を、それを使える可能性のあるすべてのマテリアルにパーミュテーションを追加します。そのため、プロジェクトはそれで何かを描画するかどうかに関係なくコストを払います。アートディレクションに必要なものだけを有効にしてください。TressFX は、スイッチに関係なく、モバイルと ES 3.1
のシェーダープラットフォームからも除外されます。

## ビルドに含まれているものを確認する

コンパイル時スイッチは実行時には見えないため、デバッグ時には「この機能はそもそもコンパイルされているのか」が現実的な問いになります。

最も確実な確認方法は、該当する CVar を設定してエフェクトが現れるかを見ることです。数百のライトがあるシーンで
`r.RayTracing.SampledDirectLighting 1` にしても何も変わらなければ、`VITE_RT_PSO_DEBLOAT` が有効です。

実行時の CVar を持つスイッチでは、CVar が存在するかどうかを確認するのが直接的なテストです。Shipping や Test のビルドでは、`r.Vite.SSAO` はコンパイル対象から外れているため見つかりません。

## 関連項目

- [シェーダーコンパイルと PSO](Shader-Compilation-And-PSO.md)
- [レイトレーシング](Ray-Tracing.md)
- [固定タイムステップ](Fixed-Timestep.md)
- [キャッシュ管理](Cache-Management.md)
- [ソースからのビルド](Build-From-Source.md)
