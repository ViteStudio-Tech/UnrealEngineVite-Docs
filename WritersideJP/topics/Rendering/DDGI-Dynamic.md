# 動的 DDGI

<tldr>
<p>
リアルタイムのレイトレーシングによるイラディアンスプローブボリュームです。既定で有効になっており（June Major 以降 <code>r.GlobalIllumination.ExperimentalPlugin 1</code>）、レベルに DDGI ボリュームを配置するとライティングされます。原理的にノイズが発生せず、完全に動的で、同等のシーンではハードウェア Lumen のおよそ 2 倍のフレームレートで動作します。
</p>
</tldr>

Dynamic Diffuse Global Illumination は Vite の主要なグローバルイルミネーションのソリューションであり、このフォークを最もよく知られたものにしている機能です。このページでは、その仕組み、セットアップ、調整方法を説明します。

<img src="DDGIDirectOnly.png" alt="直接光のみの屋根裏の室内。日差しの当たらない部分はすべて黒く見える" border-effect="line"/>

*直接光のみ。太陽が直接届かない部分は、部屋の中で光を運ぶものがないため、すべて黒くなります。*

<img src="DDGIDirectPlusGI.png" alt="同じ屋根裏の室内で動的 DDGI を有効にし、間接光のバウンスが部屋を満たしている様子" border-effect="line"/>

*同じフレームで動的 DDGI を有効にしたもの。天井、左側の箱、屋根の線の下の空間はすべてバウンス光だけで照らされています。プローブのイラディアンスは原理的に滑らかなため、デノイズすべきノイズもありません。*

## 仕組み

DDGI はボリューム全体に 3 次元のプローブのグリッドを配置します。毎フレーム、各プローブからシーンに向けて予算内の数のレイを飛ばし、得られたラディアンスをプローブごとのイラディアンスと深度のテクスチャに蓄積し、球面調和関数で保存します。

この表現から 2 つの性質が導かれ、それが DDGI の挙動のほぼすべてを説明します。

**ノイズが発生しません。** イラディアンスはピクセル単位・フレーム単位でサンプリングされるのではなく、多数のフレームにわたって蓄積され、滑らかな基底にフィルタリングされるため、出力に確率的なノイズはなく、デノイザーも不要です。DDGI に、デノイズしたレイトレーシング GI に見られるうねり、ゴースト、時間的な不安定さが現れないのはこのためです。

**粗い表現です。** 空間的な解像度はプローブの間隔で決まります。プローブのグリッドより細かいライティングのディテールは、表現の中に存在しません。[SSGI](SSGI.md) の併用を推奨する理由がここにあります。

プローブごとの深度情報が、薄いジオメトリを通した光漏れを防ぎます。プローブは各方向で最も近いサーフェスまでの距離を知っているため、壁を通り抜けなければならない寄与を除外できます。DDGI の光漏れがソフトウェア Lumen より少ないのはこのためです。

<img src="DDGIProbeVisualisation.png" alt="室内全体に DDGI のプローブの球体を表示したエディタのビューポート" border-effect="line"/>

*エディタでのプローブの可視化。各球体は保存されたイラディアンスを表示する 1 つのプローブで、プローブの間隔や位置の誤りがすぐに分かります。*

## Vite での統合

Vite の DDGI は、標準の 4.27 向けランチャー版プラグインではありません。NvRTX のエンジン側の統合を受け継いでおり、レイトレーシングパイプラインの横に置かれるのではなく、その内部にまで及んでいます。実際の違いは次のとおりです。

- **プローブを使ったレイトレーシング反射。** 反射レイは二次バウンスで黒を返したりキューブマップにフォールバックしたりする代わりに、プローブのイラディアンスをサンプリングできます。これにより RT 反射の品質が大きく向上し、このフォークで最も大きな見た目の改善の 1 つになっています。[レイトレーシング反射](RT-Reflections.md) を参照してください。
- 各リリースの一環として、DDGI の更新パスの最適化を継続しています。
- 他の RT エフェクト一式と組み合わせられるため、DDGI、RTXDI、RT 反射をすべて同時に有効にできます。

> ランチャー版の 4.27 用 DDGI プラグインを Vite のプロジェクトにインストールしないでください。エンジンにはすでに
> DDGI が含まれており、両者は競合します。スタンドアロンの
> [DDGI 1.1.5 プラグイン](https://github.com/GapingPixel/UE4-RTXGI-1.1.5-Latest-Official) は、Vite のプロジェクトと
> 並行して標準のランチャー版 4.27 で作業するチームメンバー専用です。
>
{style="warning"}

## セットアップ

<procedure title="レベルに動的 DDGI を設定する" id="setup-ddgi">
    <step>
        プロジェクトでレイトレーシングが有効になっていることを確認します。DDGI には DXR 対応が必要です。
    </step>
    <step>
        プラグインのパスが有効なことを確認します。June Major 以降は <code>BaseEngine.ini</code> で
        <code>r.GlobalIllumination.ExperimentalPlugin 1</code> が設定されているため、プロジェクトの設定やコードで無効にしていない限り対応は不要です。
    </step>
    <step>
        ライティングしたいプレイ可能な空間を囲むように DDGI ボリュームのアクターを配置します。ボリュームがカバーするのはサーフェスではなく空間です。壁の位置ではなく、プレイヤーや動的なオブジェクトが移動できる場所を考えてください。
    </step>
    <step>
        軸ごとのプローブ数を設定します。粗い設定から始め、違いが見える場所でだけ増やしてください。プローブ数はメモリとフレームごとのレイのコストの両方を左右します。
    </step>
    <step>
        プローブのグリッドでは表現できない接触ディテールを補うため、<code>r.SSGI.Enable 1</code> で
        <a href="SSGI.md">SSGI</a> を有効にします。
    </step>
    <step>
        静止画ではなく動きの中で確認します。DDGI の利点は時間方向にあり、スクリーンショットではデノイズを使う手法との安定性の差は分かりません。
    </step>
</procedure>

<img src="ProjectSettingsRHI.png" alt="既定の RHI を DirectX 12 に設定し、DirectX 11 と 12 の SM5 にチェックを入れたプロジェクト設定" border-effect="line"/>

*最初の手順であり、よく飛ばされる手順です。**プロジェクト設定 &rarr; プラットフォーム &rarr; Windows &rarr; Targeted RHIs**
は DirectX 12 でなければなりません。4.27 のレイトレーシングは DX12 専用です。*

<img src="DDGIEnablePlugin.png" alt="プラグインのダイアログで、Built-In の Rendering にある NVIDIA RTX Global Illumination プラグインが有効になっている" border-effect="line"/>

***Built-In &rarr; Rendering** にある GI プラグインのパス。Vite はこれをエンジン側に同梱しているため、これはエンジン内のプラグインであり、ランチャー版の 4.27 用プラグインではありません。後者を一緒にインストールしないでください。*

<img src="DDGIVolumeEditor.png" alt="エディタのビューポートでレベルに配置された DDGI ボリュームのアクター" border-effect="line"/>

*レベル内の DDGI ボリューム。ボリュームはサーフェスではなく空間をカバーします。カメラと動的なオブジェクトが実際に移動できる範囲に合わせてサイズを決めてください。*

### ボリュームの設定

<img src="DDGISettingsVolume.png" alt="DDGI ボリュームの設定パネル" border-effect="line"/>

<img src="DDGISettingsProbes.png" alt="軸ごとのプローブ数とプローブの間隔を設定する DDGI のプローブ設定パネル" border-effect="line"/>

<img src="DDGISettingsLighting.png" alt="DDGI のライティング設定パネル" border-effect="line"/>

*DDGI ボリュームのアクターのボリューム、プローブ、ライティングの設定。軸ごとのプローブ数が、メモリとフレームごとのレイのコストの両方を左右する設定です。*

## 調整

特に重要な設定を、おおよそ影響の大きい順に示します。

**プローブの密度**（ボリュームの `Probe Counts`、既定 8&times;8&times;8）。 コストと品質を支配する設定です。密なグリッドほど小さなライティングの特徴を解像できますが、トレースするレイの数とメモリの両方でそれに比例したコストがかかります。小部屋の多い屋内空間には、開けた屋外より多くのプローブが必要です。

<img src="DDGIProbeDensity.png" alt="プローブの間隔によってライティングのディテールがどう変わるかを示すプローブ密度の比較" border-effect="line"/>

*プローブの密度と解像されるライティングのディテールの関係。プローブの間隔より細かいディテールは、どの品質設定でも表現には存在しません。そのために [SSGI](SSGI.md) があります。*

**ボリュームの配置と数。** 大きく緩いボリュームを 1 つ使うより、ぴったり合わせた複数のボリュームを使うほうが通常は良い結果になります。レベル全体を低密度で覆うボリュームは、固体のジオメトリの中でプローブを無駄にし、重要な空間にプローブが足りなくなります。

**プローブあたりのレイ数**（`Rays Per Probe`、既定 288）。 収束の速さとフレームごとのコストのトレードオフです。少ないと収束が遅くなり、明るい屋外に面したドアが開くなど、ライティングが急に変わったときに遅れとして現れます。

**ヒステリシス / 更新レート**（`Probe History Weight`、既定 0.97）。 プローブが新しい情報をどれだけ速く受け入れるかです。応答を速くすると遅れは減りますが、時間的な揺らぎが増えます。

**法線とビューのバイアス**（`Normal Bias` 10、`View Bias` 40）。 光漏れと接触部の暗さのトレードオフを調整する標準的な設定です。薄い壁を通して光が漏れる場合はバイアスを上げ、接触部が浮いて見える場合は下げてください。

## 参考資料

手法そのものについては、NVIDIA のオリジナルのドキュメントと講演が今でも最良の詳しい参考資料です。

- [現行リリースの RTXGI プラグイン](https://github.com/GapingPixel/UnrealEngineVite-PhysX/tree/ueVite26-SeptemberMajor-release/Engine/Plugins/Runtime/Nvidia/RTXGI)
- [Dynamic Diffuse Global Illumination の GDC での発表](https://developer.download.nvidia.com/video/gputechconf/gtc/2019/presentation/s9900-irradiance-fields-rtx-diffuse-global-illumination-for-local-and-cloud-graphics.pdf)

Ray-Traced Irradiance Fields:

[![Ray-Traced Irradiance Fields](https://img.youtube.com/vi/KufJBCTdn_o/0.jpg)](https://www.youtube.com/watch?v=KufJBCTdn_o)

サンプルシーンのセットアップと SSGI との併用:

[![DLSS and RTXGI Unreal Engine 4 Plugin: Settings Deep Dive](https://img.youtube.com/vi/ZefvmV1pdP8/0.jpg)](https://www.youtube.com/watch?v=ZefvmV1pdP8&t=1210s)

プラグインの設定の詳細:

[![NVIDIA RTXGI Unreal Engine 4 Plugin: Settings Deep Dive](https://img.youtube.com/vi/U57_a3lGKOo/0.jpg)](https://www.youtube.com/watch?v=U57_a3lGKOo)

公式の再生リスト全体:

[![Getting Started with NVIDIA RTXGI Unreal Engine 4 Plugin](https://img.youtube.com/vi/bxEVMnyXxqw/0.jpg)](https://www.youtube.com/playlist?list=PL4FII4B-zM0f5h75klcOfiO1v_atlp8Ky)

チームが管理している内部の
[DDGI リファレンス文書](https://docs.google.com/document/d/1kdZGRV6bRNjNvec1OzzEJd64NtLBDZ8hzQvFVzB2GfI/edit?tab=t.0)
もあります。

## サンプルシーン

- [テックデモプロジェクト](Tech-Demo-Project.md) &mdash; NVIDIA 公式の DDGI のコーネルボックスのサンプルと、DDGI と
  SSGI を組み合わせたハイエンドの洞窟シーンを含みます。
- [スタイライズドレイトレーシングデモ](Stylized-Raytracing-Demo.md) &mdash; 4K120 のスタイライズドの目標。
- [廃アパートメント](Abandone-Apartment.md) と [屋根裏シーン](Attic-Scene.md) &mdash; NVIDIA の RTGI ショーケースシーン。

## 関連項目

- [グローバルイルミネーション](Global-Illumination.md)
- [静的 DDGI](DDGI-Static.md)
- [SSGI](SSGI.md)
- [レイトレーシング反射](RT-Reflections.md)
- [パフォーマンス目標](Performance-Targets.md)
