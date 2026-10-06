# ヘアレンダリング

<tldr>
<p>
Vite には 2 つのストランドベースのヘアシステムが同梱されています。AMD の <b>TressFX 5.0</b> と、Epic の
<b>Groom</b>（HairStrands）です。TressFX は Vite が追加したもので、Groom は標準の 4.27 のシステムです。どちらも既定では
無効です。
</p>
</tldr>

髪は、説得力のある描画が最も難しいサーフェスの 1 つです。カードベースの髪は安価で予測しやすいものの、動きの中や
かすめる角度からは決して正しく見えません。ストランドベースの髪は個々の繊維をシミュレーション・描画するため、見た目は
劇的に良くなりますが、コストも劇的に高くなります。

## 利用できるシステム

| システム | プラグイン | 提供元 | 備考 |
|---|---|---|---|
| TressFX 5.0 | `Engine/Plugins/Runtime/TressFX` | AMD | Vite が追加。シミュレーション、描画、エディタツール。 |
| Groom（HairStrands） | `Engine/Plugins/Runtime/HairStrands` | Epic | 標準の 4.27。Alembic ベースで、`Hair` シェーディングモデルで動作。 |
| Alembic Hair Importer | `Engine/Plugins/Importers/AlembicHairImporter` | Epic | Groom のアセットのインポート手段 |

どちらのヘアシステムも既定では有効ではありません。**編集 > プラグイン** からどちらかを有効にしてください。同じ
プロジェクトで両方を有効にする理由はほとんどありません。

<note>
<p>
<a href="ueVite26-JulyMajor.md">July Major</a> 以降、TressFX はコンパイル時の機能でもあります。プラグインを有効にする前に、
<code>VITE_TRESSFX=1</code> でエンジンをビルドしてください。TressFX のシェーダーはモバイルと ES 3.1 のプラットフォーム
から除外されます。<a href="Compile-Time-Switches.md">コンパイル時スイッチ</a> を参照してください。
</p>
</note>

## TressFX 5.0

TressFX は AMD のオープンなヘアとファーのシステムです。Vite の統合には 3 つのモジュールがあります。実行時の
シミュレーションと描画の `TressFXCore`、アセットのインポートの `TressFXImportTranslator`、作成ツールの `TressFXEditor`
です。

シミュレーション（頭の動き、風、コリジョンにストランドが反応）と描画（順序に依存しない透明度、自己シャドウ、髪に必要な
異方性スペキュラー）を 1 つのシステムとして扱います。

### コンソール変数

| CVar | 既定値 | 用途 |
|---|---|---|
| `r.TressFX.StrandsMode` | `0` | デバッグ表示。`0` はオフ、`1` はシミュレーション用ストランド、`2` はシミュレーションの影響度で色分けした描画用ストランド、`3` は髪の UV、`4` は髪の根元の UV、`5` は髪のシード、`6` は寸法 |
| `r.TressFX.Interoplation.FrustumCulling` | `1` | ストランドの補間中の視錐台カリング。実験的。 |
| `r.TressFX.MorphTargetMeshVisualization` | `0` | 正確な透過のパス。小さなスケールの TressFX の描画を改善 |

<note>
<code>r.TressFX.Interoplation.FrustumCulling</code> は、「Interpolation」の文字の入れ替わりも含めて、ソースに記述された
とおりの綴りです。文字列はそのまま使ってください。
</note>

デバッグモードは、髪の問題を診断する最も早い方法です。特にモード `2`（シミュレーションの影響度で色分けした描画用
ストランド）は、ガイドストランドの分布が妥当か、少なすぎるガイドで描画用ストランドの広い領域を動かしていないかを
すぐに示してくれます。

### コスト

ストランドの髪は、コストがシミュレーション（コンピュート）、描画（半透明による大量のオーバードロー）、シャドウに分散する
ため、過小評価しやすい形で高価です。TressFX の髪をフルに使ったキャラクター 1 体で、
[4K60 のフレーム予算](Performance-Targets.md) のかなりの部分を消費することがあります。

実践的な指針:

- ストランドの髪の予算はヒーローキャラクターだけに割り当ててください。群衆や背景のキャラクターにはカードを使います。
- LOD を積極的に使ってください。ストランドの数は距離に応じて大きく減らすべきで、中距離でカードに切り替えるのは普通の
  ことです。
- 実際の [アンチエイリアシング](Anti-Aliasing.md) の設定でテストしてください。細いジオメトリはまさに AA の手法が最も
  影響するケースで、TAA では許容できる髪も SMAA ではちらつくことがあります。

## Groom

Groom は標準の 4.27 にある Epic のストランドシステムです。Maya、Houdini、Blender から Alembic Hair Importer で Alembic の
グルームキャッシュをインポートし、`Hair` シェーディングモデルで描画します。**Scatter**（Metallic ピン）と **Backlit**
（Custom Data 0）のパラメーター、そして Normal ピンの **Tangent** を使います。

Groom は標準の Unreal なので、ドキュメントがより充実しており、サードパーティのツールも多くあります。AMD 系のパイプラインから
来た場合や、TressFX 特有のシミュレーションの挙動が必要な場合は、TressFX のほうが適しています。

## レイトレーシングとの関係

髪とレイトレーシングは、既定ではうまく噛み合いません。ストランドのジオメトリはアクセラレーション構造に膨大な数の
小さなプリミティブを生成し、髪に対するレイトレーシングの [シャドウ](RT-Shadows-And-Ambient-Occlusion.md) と
[反射](RT-Reflections.md) はどちらも高価でノイズが多くなります。

髪をレイトレーシングから除外し（プリミティブの **Visible in Ray Tracing** フラグ）、代わりにラスタライズのシャドウを
受けるようにすることを検討してください。見た目の違いは通常わずかですが、性能の違いはわずかではありません。

## 関連項目

- [シェーディングモデル](Shading-Models.md)
- [アンチエイリアシング](Anti-Aliasing.md)
- [同梱プラグイン](Bundled-Plugins.md)
- [パフォーマンス目標](Performance-Targets.md)
