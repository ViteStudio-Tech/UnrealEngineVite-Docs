# UE5 からの移行

<tldr>
<p>
アセットは <a href="Proposed-Plugins.md">UE Downgrader</a> プラグインでダウングレードします。このプラグインは
UE 5.8 以前から 4.27 への変換に対応しています。Vite は UE5 のコンテナ、ゲームフレームワーク、GAS の API を多数バックポートしているため、コードの移行は標準の 4.27 よりも容易です。Nanite、Lumen、VSM、World Partition など
4.27 に存在しない機能には対応するものがなく、変換ではなく設計上の判断が必要です。
</p>
</tldr>

Unreal Engine 5 から Vite へのプロジェクトの移行は、単なるバージョン変更ではなく本格的な移行作業です。このページでは、そのまま移せるもの、置き換えが必要なもの、そして作業の順序を説明します。

## 移行できるものとできないもの

| UE5 の機能 | Vite での状況 | 対応方法 |
|---|---|---|
| スタティックメッシュ、テクスチャ、マテリアル、アニメーション | 移行可能 | UE Downgrader プラグインでダウングレード |
| ブループリント | 移行可能 | ダウングレード後、ノード単位で再テスト。UE5 専用ノードの一部は対応先がない |
| C++ のゲームプレイコード | 移行可能 | Vite は多くの UE5 API をバックポート済み。後述 |
| Gameplay Ability System | 移行可能 | Vite には UE5 からバックポートした GAS の更新が含まれる |
| Nanite | 対応なし | 従来の LOD を作成し、表面のディテールには [テッセレーション](Tessellation.md) を使用 |
| Lumen | 置き換え | [DDGI](DDGI-Dynamic.md) を使用し、必要に応じて [SSGI](SSGI.md) と併用 |
| 仮想シャドウマップ | 対応なし | カスケードシャドウマップ、または [レイトレーシングシャドウ](RT-Shadows-And-Ambient-Occlusion.md) |
| TSR | 置き換え | [DLSS、FSR、XeSS](Upscalers.md)、またはネイティブ解像度と [SMAA](Anti-Aliasing.md) |
| MegaLights | 置き換え | [RTXDI](RTXDI.md) |
| Chaos 物理 | 置き換え | [PhysX](PhysX.md) |
| Chaos Destruction | 置き換え | [Apex Destruction](Destruction-And-Cloth.md) と [Blast](Destruction-And-Cloth.md) |
| Chaos Cloth | 置き換え | [Apex Cloth](Destruction-And-Cloth.md) |
| Substrate | 対応なし | 標準のマテリアルモデルと [Callisto BRDF](Shading-Models.md) |
| World Partition | 置き換え | World Composition とレベルストリーミング |
| Niagara | 移行可能 | 利用可能。より高速な代替として [PopcornFX](Proposed-Plugins.md) がある |
| MetaSounds | 対応なし | Sound Cue、または [Wwise](Proposed-Plugins.md) |

## アセットのダウングレード

UE Downgrader プラグインは、UE 5.8 以前のアセットを 4.27 や 4.26 に変換します。まずアセットをプラグインのソースバージョン（通常は最新の UE5）にアップグレードし、その後 `.uasset` ファイルにパッチを当てて、古い形式で表現できないデータを除いたうえで対象バージョンから読めるようにします。たとえば、4.27 へのダウングレードでは Nanite のデータが取り除かれます。

このプラグインにできないのは、4.27 に存在しない機能の代わりを作り出すことです。マスクマテリアルでの Nanite、新しいマテリアルノード、新しい Niagara モジュールは移行できません。それらの作り直しを予算に組み込んでください。

このプラグインは有償です。作者の Ciprian Stanciu 氏は [Vite の Discord](https://discord.gg/n9zQrYFhMb) で活動しており、複数の Vite プロジェクトを直接サポートしてきました。作業の流れは
[解説動画](https://youtu.be/yXvJfDNfrSQ) で確認できます。

## コードの移行

ここは標準の 4.27 より Vite のほうが楽な部分です。このフォークは UE5 の API を意図的にバックポートしており、UE5 世代のコードを少ない変更でコンパイルできます。更新されたコンテナクラス、ゲームフレームワークの更新、Gameplay Ability System の機能がすべて含まれています。

それでも違いには遭遇します。次の順序で対処してください。

1. **物理。** `Chaos` 名前空間、`FChaosScene`、ジオメトリコレクション、Chaos のビークルに関わるものは、PhysX の相当機能に移す必要があります。通常、これが最大の作業になります。[PhysX](PhysX.md) を参照してください。
2. **レンダリング。** Lumen、Nanite、VSM のコンソール変数を参照・操作するコードには移行先がありません。[レンダリング](Rendering.md) にある Vite の相当機能に置き換えてください。
3. **コア API の差異。** UE5 の `FVector` は倍精度（`FVector3d`）ですが、4.27 では単精度です。ラージワールド座標の前提は成り立ちません。大きなワールドオフセットで精度に敏感な計算を行っているコードを点検してください。
4. **モジュールとビルドルール。** UE5 専用モジュールを参照している `.Build.cs` は、その依存関係を削除するか置き換える必要があります。

## 推奨する移行手順

<procedure title="UE5 プロジェクトを Vite に移行する" id="migration-order">
    <step>
        まず空の Vite プロジェクトを立ち上げ、ツールチェーンとエンジンのビルドが正常であることを確認します。2 つの問題を同時にデバッグしないでください。
    </step>
    <step>
        コンテンツを含まない状態で C++ のモジュールを移植します。アセットを移す前に、Vite に対してコンパイルが通るようにします。物理とレンダリングの API の不整合はここで確認します。
    </step>
    <step>
        小規模で代表的なコンテンツの一部（キャラクター 1 体、環境 1 つ、数個のマテリアル）をダウングレードしてインポートし、見た目と挙動が正しいことを検証します。
    </step>
    <step>
        ライティングの構成を置き換えます。Lumen には直接の変換先がありません。
        <a href="DDGI-Dynamic.md">DDGI</a> のボリュームを配置し、インポートしたコンテンツに合わせて調整します。
    </step>
    <step>
        物理の構成を作り直します。破壊は <a href="Destruction-And-Cloth.md">Apex Destruction</a>、クロスは
        <a href="Destruction-And-Cloth.md">Apex Cloth</a> で再作成します。
    </step>
    <step>
        一部で問題がないことを確認できたら、残りのコンテンツを一括で移行します。
    </step>
    <step>
        対象ハードウェアでプロファイリングし、スケーラビリティを設定します。
        <a href="Profiling.md">プロファイリング</a> を参照してください。
    </step>
</procedure>

## バージョンを混在させるワークフロー

全員を一度に移行する必要はありません。よくある構成は、プログラマーは Vite で作業し、アーティストやコンテンツ制作者は Epic Games Launcher でインストールした標準の 4.27 で作業を続け、コンテンツを一方向に流すというものです。これを機能させるには、ランチャー側のユーザーがスタンドアロンの
[DDGI 1.1.5 プラグイン](https://github.com/GapingPixel/UE4-RTXGI-1.1.5-Latest-Official) を使い、手元でもライティングがおおむね正しく見えるようにする必要があります。これは Vite Studio で実際に採用している方法で、これまでモデリング、アニメーション、サウンドデザインの作業で問題なく運用できています。

> ランチャー用の DDGI プラグインを Vite のプロジェクトにインストールしないでください。Vite にはエンジンの一部として
> DDGI がすでに含まれており、両者は競合します。また、エンジン側とプラグイン側の両方に変更を加えているため、Vite に
> 統合された DDGI のほうがランチャー用プラグインより良好に動作します。
>
{style="warning"}

## 関連項目

- [Vite の概要](Introduction-to-Vite.md)
- [PhysX](PhysX.md)
- [グローバルイルミネーション](Global-Illumination.md)
- [提案中のプラグイン](Proposed-Plugins.md)
- [UE4 と UE5 のコスト分析](UE4-Versus-UE5-Cost-Analysis.md)
