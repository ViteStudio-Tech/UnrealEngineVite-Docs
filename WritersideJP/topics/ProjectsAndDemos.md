# プロジェクトとデモ

<tldr>
<p>
Vite の機能を示し、その性能の数値を裏付けるダウンロード可能なプロジェクトです。いくつかは、
<a href="Performance-Targets.md">パフォーマンス目標</a> の計測の基準となるベンチマークです。
</p>
</tldr>

これらは 2 つのグループに分かれます。エンジンが見た目の面で何をできるかを示す **ショーケース** と、それにかかるコストを示す **ベンチマーク** です。Vite がプロジェクトに合うかを判断するなら、役に立つのはベンチマークのほうです。

## ショーケース

| プロジェクト | 示すもの |
|---|---|
| [テックデモプロジェクト](Tech-Demo-Project.md) | DDGI、SSGI、Apex Destruction、Apex Cloth を 1 つのパッケージで |
| [スタイライズドレイトレーシングデモ](Stylized-Raytracing-Demo.md) | 非写実的なアートディレクションへのレイトレーシングの適用 |
| [Callisto BRDF デモ](Callisto-BRDF-Demos.md) | 肌とキャラクターのための独自のシェーディングモデル |
| [廃アパートメント](Abandone-Apartment.md) | 屋内のライティングのシーン |
| [屋根裏シーン](Attic-Scene.md) | 屋内のライティングのシーン |
| [Crash Bandicoot: Timetwister](Crash-Bandicoot.md) | UE4 で作られた完全なゲームプレイのレベル |

## ベンチマーク

| プロジェクト | 計測するもの |
|---|---|
| [400 キャラクター CMC ベンチマーク](400-Characters-CMC-Bench.md) | 大規模なキャラクタームーブメントコンポーネントのコスト |
| [物理キューブベンチマーク](Physics-Cube-Bench.md) | PhysX の剛体のスループット |
| [PhysX テスト](PhysXTest.md) | PhysX の全般的な挙動と安定性 |
| [PhysX インスタンスサブシステム](PhysX-Instanced-Subsystem.md) | 個別のアクターでは到達できない数のインスタンス化した剛体 |

## ベンチマークの使い方

ベンチマークは、フレームレートの数値から想像する以上に多くのことを教えてくれます。`stat unit` を表示して実行し、どのスレッドが上限になっているかを確認してください。それによって、似た負荷にどれだけのコストがかかり、Vite のどの最適化が効くかが分かります。[プロファイリング](Profiling.md) を参照してください。

<note>
これらのプロジェクトの数値は、それを計測したハードウェアを反映しています。Vite の
<a href="Coding-Guidelines.md">性能の基準</a> は ARM クラスの約 1 GHz の CPU で、開発用のデスクトップよりはるかに低いものです。手元のマシンで余裕のあるベンチマークでも、対象のハードウェアではそうとは限りません。
</note>

## 関連項目

- [パフォーマンス目標](Performance-Targets.md)
- [プロファイリング](Profiling.md)
- [UE4 と UE5 のコスト分析](UE4-Versus-UE5-Cost-Analysis.md)
