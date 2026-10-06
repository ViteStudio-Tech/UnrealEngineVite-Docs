# アップスケーラー

<tldr>
<p>
Vite には、Ray Reconstruction とマルチフレーム生成に対応した NVIDIA DLSS 4.5、FSR 3.1 へのフォールバックとベンダーを問わないフレーム生成を備えた AMD FSR 4、XeFG に対応した Intel XeSS 3.1、NVIDIA NIS、そして Reflex と Anti-Lag 2 のレイテンシー SDK が同梱されています。これらは <b>任意の余力</b> であり、レンダリングの前提ではありません。Vite の
<a href="Performance-Targets.md">パフォーマンス目標</a> は、どれも使わずにネイティブ解像度で達成しています。
</p>
</tldr>

[UpscalerTest サンプルプロジェクト](https://github.com/ViteStudio-Tech/ueVite-UpscalerTest) もご覧ください。

Unreal Engine 5 はアップスケーリングを必須として扱います。レンダラーは出力解像度の一部で描画し、残りを再構成する前提で設計されています。Vite は逆の立場を取ります。目標はネイティブであり、アップスケーラーは余力を別のことに使いたいユーザーのために用意しています。

この違いによって、このページのプラグインの使い方が変わります。DLSS のパフォーマンスモードを有効にしないとフレームの目標に届かないプロジェクトは、予算を超えています。まずそれを直し、そのうえで追加のオプションとしてアップスケーリングを提供してください。

## 同梱プラグイン

以下はすべてエンジンのリポジトリの `Engine/Plugins/Runtime` に含まれています。既定で有効なものはありません。プロジェクトで提供するものを **編集 > プラグイン** から有効にしてください。バージョンは
[September Major](ueVite26-SeptemberMajor.md) のものです。

| プラグイン | バージョン | 提供するもの | 場所 |
|---|---|---|---|
| NVIDIA DLSS | 8.7.0-NGX310.7.0（DLSS 4.5 のプリセット） | Super Resolution、Ray Reconstruction、DLAA | `Nvidia/DLSS` |
| NVIDIA DLSS Frame Generation | Streamline SDK 2.12.0 上の 1.3.0 プラグイン | マルチフレーム生成を含むフレーム生成 | `Nvidia/Streamline` |
| NVIDIA Reflex | 1.6 | レイテンシーの削減 | `Nvidia/Reflex` |
| NVIDIA RTX Dynamic Vibrance | 1.3.0（Streamline） | ディープラーニングによる動的な鮮やかさの調整 | `Nvidia/StreamlineDeepDVC` |
| NVIDIA NIS | 1.2.1 | Image Scaling: 空間アップスケーリングとシャープニング | `Nvidia/NIS` |
| Movie Render Queue DLSS/DLAA Support | 2.3.3 | Movie Render Queue への DLSS の統合 | `Nvidia/DLSSMoviePipelineSupport` |
| AMD FSR 4 | 4.1.1 | FSR 3.1 へのフォールバック付きの FSR 4 の ML アップスケーリング、ネイティブ AA、どのアップスケーラーとも組み合わせられるフレーム生成。DirectX 12 | `VitePlugins/FSR4-427/FSR4` |
| AMD Anti-Lag 2 | 2.0.4 | AMD の GPU でのレイテンシーの削減 | `VitePlugins/AntiLag2.0.4` |
| Intel XeSS | 3.1.0 | Xe Super Sampling と XeFG のフレーム生成 | `VitePlugins/XeSS_UE4.27_Plugin_v3.1.0` |

FSR 4 と XeSS 3 は特筆に値します。どちらも標準の 4.27 には存在しないバックポートです。FSR 4 はネイティブの `ffx-api` を使い、DirectX 12 が必要です。このセットの大部分は [June Major](ueVite26-JuneMajor.md) で導入され、[August Major](ueVite26-AugustMajor.md) で XeSS が 3.1.0 に、DLSS のランタイムが NGX 310.7.129 に更新されました。

以前のリリースの FSR 2 のプラグインは `VitePlugins/FSR2-427` としてツリーに残っていますが、記述子が `.uplugin.disabled` に名前を変えてあるため、エンジンは読み込みません。FSR 2 が対象としていたハードウェアは、FSR 4 に組み込まれた FSR 3.1 の経路でカバーされます。

<warning>
<p>
<a href="ViteSetup.md">ViteSetup</a> の Express の経路は、<code>Engine\Plugins\Runtime\VitePlugins</code> 以下のプラグインを ACL と MotionSymphony を除いてすべて <code>ViteDebloat_Moved</code> に移動します。FSR 4、Anti-Lag 2、XeSS もその中に含まれます。必要な場合は Custom の経路を選ぶか、<code>ViteDebloat_Moved</code> からフォルダーを戻してください。NVIDIA のプラグインは影響を受けません。
</p>
</warning>

### 任意のレンダー解像度

`r.Upscaler.ScreenPercentageOverride` を使うと、FSR、DLSS、XeSS が固定の品質モードだけでなく任意の内部レンダー解像度を受け取れます。これらのプラグインはスクリーンパーセンテージを自ら管理して `r.ScreenPercentage` を無視するため、これが設定する方法です。`0`（既定）では品質モードのプリセットが解像度を決め、`1`&ndash;`100` ではそのスクリーンパーセンテージを強制します。値は使用中のアップスケーラーが対応する範囲に制限されます。ベンチマークや解像度スライダーの提供に使ってください。

## 何を出荷するか

すべてを使う必要はありません。有効にしたアップスケーラーごとに、シェーダー、バイナリ、パッケージサイズ、そしてテストが必要な設定メニューの項目が増えます。

| 状況 | 推奨 |
|---|---|
| PC 版で幅広いハードウェアに対応 | DLSS と FSR 4。NVIDIA と AMD をカバーし、Intel Arc が重要なら XeSS も。 |
| NVIDIA 中心でレイトレーシングを多用 | Ray Reconstruction 付きの DLSS |
| ネイティブ解像度でのアンチエイリアシングの品質 | DLAA（DLSS プラグインの一部）、FSR 4 のネイティブ AA、または Vite の [SMAA](Anti-Aliasing.md) |
| アップスケーリングなし、ネイティブのみ | このページのものは何も出荷しません。これは正当でサポートされた構成です。 |

DLAA は特に取り上げる価値があります。DLSS のニューラルネットワークをアップスケーラーとしてではなくネイティブ解像度で適用するもので、SMAA を補うのではなく SMAA と競合します。一般に SMAA より細かいディテールを解像しますが、時間的な蓄積を再び持ち込むため、SMAA が避けているアーティファクトの一部も戻ってきます。両方を提供し、プレイヤーに選ばせてください。

## Ray Reconstruction

Ray Reconstruction は、レイトレーシングのエフェクト向けの手作業で調整したデノイザーを、ニューラルデノイザーに置き換えます。Vite のプロジェクトでは、これは [レイトレーシング](Ray-Tracing.md) の構成と直接関係します。

- 手作業で調整したデノイザーが苦手とする動きの中で、[RT 反射](RT-Reflections.md) と [RTXDI](RTXDI.md) の品質を大きく改善できます。
- 原理的にノイズがなくデノイズするものがない [DDGI](DDGI-Dynamic.md) には効果がありません。

Ray Reconstruction には、Super Resolution のプリセットとは別に専用のプリセットのコンソール変数があります。プリセット F が
DLSS 4.5 のモデルです。

レイトレーシングの構成が DDGI 中心であれば、Ray Reconstruction の効果は Lumen ベースのプロジェクトより小さくなります。出荷する前に計測してください。

## フレーム生成

エンジンには 3 種類のフレーム生成が同梱されています。

- Streamline による **DLSS Frame Generation**。DLSS-G のマルチフレーム生成の倍率指定も含みます。
- 表示時にスワップチェーンから駆動する **FSR のフレーム生成**。アップスケーラーに依存せず、FSR だけでなく DLSS、XeSS、ネイティブ描画とも組み合わせられます。いずれかのフレーム生成を選ぶと完全なベロシティ出力が強制されるため、生成されたフレームにゴーストが生じません。
- XeSS 3 によって UE 4.27 で有効にした、Intel のフレーム生成である **XeFG**。

フレーム生成は表示上のフレームレートを上げますが、入力遅延は減らしません。むしろわずかに悪化させることがあります。フレーム生成を有効にするときは、NVIDIA のハードウェアでは **Reflex**、AMD のハードウェアでは **Anti-Lag 2** を必ず併用してください。

> フレーム生成は、元のフレームレートがすでに高いときに最もよく機能します。30&nbsp;fps から 60&nbsp;fps を生成すると、
> 速く動く UI や細いジオメトリの周りに目に見えるアーティファクトが生じますが、60&nbsp;fps から 120&nbsp;fps を生成する
> 場合ははるかに自然です。Vite はもともと高いネイティブフレームレートを目標としているため、フレーム生成とは相性が
> 良く、30&nbsp;fps を救う手段ではなく、4K60 の目標を高リフレッシュレートのディスプレイに向けて押し上げる手段として
> 位置付けられます。
>
{style="note"}

## DLSS の半透明パッチ

Vite には、アップスケーリングに特有の品質の問題に対処する、任意のコンパイル時パッチが含まれています。セパレートトランスルーセンシーとボリュメトリックフォグが内部のレンダー解像度で描画されてからアップスケールされるため、それ以外は鮮明に再構成された画像の中で、パーティクル、ガラス、フォグがぼやけてしまう問題です。

| スイッチ | 既定値 | 効果 |
|---|---|---|
| `VITE_DLSS_PATCH` | `0` | アップスケール後の解像度での半透明のパスと、ネイティブ解像度のボリュメトリックフォグを追加 |

有効にすると、レンダラーに `TranslucencyAfterDOFUpscaledRT` と `TranslucencyAfterDOFModulateUpscaledRT` の 2 つの半透明のパスが追加され、選択した半透明のプリミティブをアップスケール後に出力解像度で描画します。プリミティブは
`bRenderInTranslucencyUpscaledRTPass` のレリバンスフラグでオプトインし、これらのパスは時間的アップスケーラーが実際に動作しているときにだけ使われます。

さらに次のものも追加されます。

| CVar | 既定値 | 効果 |
|---|---|---|
| `r.VolumetricFog.UseUpScaledSizeVolumetricFog` | `0` | ボリュメトリックフォグのグリッドを、内部のレンダー解像度ではなく出力解像度から計算 |

このスイッチは `Engine/Source/Runtime/Core/Public/Misc/CoreDefines.h` で定義され、フレームタイムを消費し、アップスケーリングを有効にして出荷するプロジェクトにしか関係しないため、既定では無効です。変更方法は
[コンパイル時スイッチ](Compile-Time-Switches.md) を参照してください。

## アップスケーラーを有効にする

<procedure title="プロジェクトに DLSS を追加する" id="enable-dlss">
    <step><b>編集 &gt; プラグイン</b> を開き、<b>NVIDIA DLSS Super Resolution/Ray Reconstruction/DLAA</b> を探して有効にし、エディタを再起動します。</step>
    <step>フレーム生成には <b>NVIDIA DLSS Frame Generation</b> も、レイテンシー対策には <b>Reflex</b> も有効にします。</step>
    <step>
        設定メニューにオプションを表示する前に、DLSS のブループリントライブラリで実行時に対応状況を確認します。ハードウェアとドライバーの対応はさまざまで、黙って何もしないオプションはオプションがないより悪い結果になります。
    </step>
    <step>品質モードは固定せず、プレイヤーの設定として公開します。オフの状態も含めてください。</step>
    <step>
        <a href="Anti-Aliasing.md">アンチエイリアシング</a> の設定との組み合わせをテストします。DLSS はアンチエイリアシングのパスを置き換えるため、SMAA を一緒に有効にしたままだとフレームタイムを無駄にします。
    </step>
</procedure>

## 関連項目

- [アンチエイリアシング](Anti-Aliasing.md)
- [パフォーマンス目標](Performance-Targets.md)
- [レイトレーシング](Ray-Tracing.md)
- [同梱プラグイン](Bundled-Plugins.md)
- [コンパイル時スイッチ](Compile-Time-Switches.md)
