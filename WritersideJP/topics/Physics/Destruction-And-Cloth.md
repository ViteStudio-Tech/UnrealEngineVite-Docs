# 破壊とクロス

<tldr>
<p>
Vite は Unreal Engine 5 で削除された <b>Apex Destruction</b> と <b>Apex Cloth</b> を維持し、最新の破砕のために
NVIDIA <b>Blast</b> を追加しています。既存の 4.27 の破壊可能アセットと衣服アセットは引き続き動作します。
</p>
</tldr>

<img src="ApexDestructionTest.jpg" alt="Vite の物理テストレベルで、破壊可能な壁が銃撃を受けてチャンクと破片に砕ける様子" border-effect="line"/>

*Vite の物理テストレベルでの Apex Destruction。壁は作成済みのチャンク階層に沿って砕け、破片は PhysX でシミュレーションされます。*

破壊とクロスは、[PhysX という選択](PhysX.md) がコンテンツに最も目に見える影響を与える 2 つの分野です。どちらの Apex のシステムも PhysX に結び付いており、PhysX の削除はそれらの削除を意味しました。

## Apex Destruction

Apex Destruction は、メッシュを衝撃で砕けるチャンクの階層に分割します。アセットは Destructible Mesh として作成し、エディタ内でボロノイ分割によって破砕するか、外部ツールからインポートします。

| 項目 | 値 |
|---|---|
| プラグイン | `Engine/Plugins/Runtime/ApexDestruction` |
| アセットの種類 | Destructible Mesh |
| コンポーネント | `UDestructibleComponent` |
| UE5 での状況 | 削除 |

成熟しよく理解されたシステムで、コストのモデルも単純です。すべてはチャンク数で決まります。2 階層でチャンク数が控えめな破壊可能アセットは軽く、深い階層と数百のチャンクを持つものは重くなります。

主な設定は Destructible Mesh アセットにあります。

- **Depth** は破砕の階層数を制御します。階層が増えるたびにチャンク数が掛け算で増えます。
- **Damage Threshold** と **Damage Spread** は、チャンクの壊れやすさとダメージの伝播範囲を制御します。
- **Support Depth** は、構造的な支持の計算に参加する階層を決めます。
- **Debris Timeout** と **Debris Max Separation** は、落ち着いたチャンクを片付けます。必ず設定してください。消えないチャンクはフレームタイムが崩壊するまで蓄積し続けます。

Apex Destruction の解説動画 [![MeanLemur による解説動画](https://img.youtube.com/vi/Stn7eL1TFBg/hqdefault.jpg)](https://youtu.be/Stn7eL1TFBg)

## Apex Cloth

Apex Cloth は PhysX 時代の衣服システムで、エディタ内の Clothing Tool で作成するか、外部の DCC ツールで作成した APEX の衣服アセットをインポートします。4.27 で内部のソルバーとして動いているのは、APEX Clothing の後継である NVIDIA NvCloth（`ClothingSystemRuntimeNv`）です。インポートした APEX のアセットは同じ衣服データに変換されます。

| 項目 | 値 |
|---|---|
| アセットの種類 | APEX の衣服アセット、またはスケルタルメッシュ上のエディタ内の衣服データ |
| UE5 での状況 | Chaos Cloth に置き換えられて削除 |

エディタ内のワークフローでは、クロスのパラメーター（最大距離、バックストップの半径、バックストップの距離）をスケルタルメッシュに直接ペイントします。最大距離が主な制御で、各頂点がスキニングされた位置からどれだけ動けるかを定めます。0 にペイントするとその領域が固定され、値を大きくするとクロスが自由に揺れます。

実践上の注意点:

- クロスのコストはシミュレーションする頂点数に比例します。描画用メッシュを直接シミュレーションするのではなく、低解像度のシミュレーション用メッシュをペイントし、描画用メッシュをそれにスキニングしてください。
- クロスはスケルタルメッシュコンポーネントごとにシミュレーションされます。クロスを着たキャラクター 10 体は、1 体の
  10 倍のコストがかかります。
- クロスはシーンの他の部分と一緒にはサブステップされません。キャラクターの速い動きによって、どれだけパラメーターを調整しても直らない伸びが生じることがあります。通常の解決策は、取り付け点の移動速度を下げることです。

## NVIDIA Blast

Blast は Apex Destruction の後継となる NVIDIA の技術で、2 つの破砕システムのうちより高機能なものです。

[公式の Blast プラグインのドキュメント](https://archive.docs.nvidia.com/gameworks/content/gameworkslibrary/blast/1.1/authoring_docs/BlastUe4_QuickStart.html)

| 項目 | 値 |
|---|---|
| プラグイン | `Engine/Plugins/GameWorks/Blast`（バージョン 1.0） |
| プラットフォーム | Win64、Linux |
| 既定で有効 | いいえ。Vite のプラグインプロファイル（`ueVite-ApplyVitePluginDefaults.bat`）は Blast の作成用プラグインを有効にします。[エンジンの既定値の変更](Engine-Defaults.md#disabled-plugins) を参照 |
| モジュール | `BlastLoader`、`BlastRuntime`、`BlastEditor`、`BlastMeshEditor`、`BlastLoaderEditor` |

Blast は破壊のグラフを物理シミュレーションから切り離します。Blast のアセットはチャンクとその間の結合を記述し、ダメージは結合のグラフを通じて伝播し、チャンクは実際に分離したときに初めて物理ボディになります。Blast が大きな構造物を
Apex Destruction よりうまく扱えるのはこのためです。無傷の建物は、スリープ中の 1,000 個の剛体ではなく 1 つのグラフなのです。

Blast は実行時の破砕にも対応しているため、破砕のパターンを作成時にすべてベイクするのではなく、オブジェクトがどこをどのように撃たれたかに応じて変えられます。

**編集 > プラグイン > GameWorks** からプラグインを有効にし、Blast Mesh Editor でアセットを作成します。

### Vite での Blast の取り組み

| リリース | 変更内容 |
|---|---|
| [June Major](ueVite26-JuneMajor.md) | Blast を正しく描画するためのエンジン側の変更を含む PhysX Blast プラグインの統合と、[Blast のサンプルプロジェクト](https://github.com/ViteStudio-Tech/ueVite-PhysX_Blast-ProjectSample) |
| [July Major](ueVite26-JulyMajor.md) | Blast SDK の更新、スキンキャッシュの再構築への対応、破砕時に破砕エディタが DDC のデータを無効化しボーンのインデックスを検証 |

独自のアセットを作る前に、サンプルプロジェクトで Vite における Blast の動作する構成を確認してください。

> Blast は Apex Destruction の単純な置き換えではありません。アセットの種類、作成のワークフロー、実行時の API がすべて
> 異なります。混在させずにプロジェクトごとにどちらかを選び、新規の作業では Blast を優先してください。
>
{style="note"}

## 選び方

| 必要なもの | システム |
|---|---|
| 既存の 4.27 の破壊可能メッシュ | Apex Destruction &mdash; そのまま動作するので、理由なく移植しないでください |
| 新規の破壊、大きな構造物 | Blast |
| 新規の破壊、小さなプロップ | どちらでも可。Apex Destruction は単純で、Blast はスケールに強い |
| 実行時に変わる破砕パターン | Blast |
| 既存の APEX の衣服アセット | Apex Cloth |
| 新規の衣服 | エディタ内の Clothing Tool による Apex Cloth |

## パフォーマンス

破壊は、何かが壊れるまでコストが見えず、壊れた瞬間に一度に押し寄せるため、フレーム予算を最も簡単に壊す要因の 1 つです。

- **同時に存在する破片に上限を設けてください。** すべての破壊可能アセットに、破片のタイムアウトと最大分離距離を設定します。
- **チャンク数の予算は典型的なケースではなく最悪のケースで見積もってください。** 破壊可能なものだらけの部屋での手榴弾が、乗り切らなければならないフレームです。
- **破片には [インスタンス化物理サブシステム](Instanced-Physics.md) を検討してください。** 落ち着いて個別のアクターが不要になったチャンクは、インスタンスとしてはるかに安く扱えます。
- **静止しているときではなく、物を壊しているときに `stat physics` でプロファイリングしてください。**

## ライセンス

Apex Destruction、Apex Cloth、Blast は、PhysX と NvRTX の系譜から引き継いだ NVIDIA GameWorks の技術です。出荷するタイトルにはそれらのライセンス条項が適用されます。[GameWorks source SDK EULA](https://developer.nvidia.com/gameworks-source-sdk-eula) を参照してください。

## 関連項目

- [PhysX](PhysX.md)
- [インスタンス化物理](Instanced-Physics.md)
- [同梱プラグイン](Bundled-Plugins.md)
- [プロファイリング](Profiling.md)
