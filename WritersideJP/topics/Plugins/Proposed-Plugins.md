# 提案中のプラグイン

<tldr>
<p>
エンジンへの同梱の候補と、プロジェクトが自分で追加すべき推奨プラグインです。ここにあるものはすべて UE 4.21&ndash;4.27 と互換である必要があり、UE5 専用のプラグインは対象外です。
</p>
</tldr>

役に立つものがすべてエンジンのリポジトリに入るべきとは限りません。Vite に同梱したプラグインは、すべてのクローンのサイズ、すべてのビルドの時間、すべての統合の対象範囲を増やします。このページでは、何が提案され、どの階層に属するかを記録します。

<img src="Plugins1.png" alt="統合済みのプラグインのフォルダーを示す Engine/Plugins/Runtime/VitePlugins のエクスプローラー表示" border-effect="line"/>

*すでに統合されたプラグインは `Engine\Plugins\Runtime\VitePlugins` にあります。*

## 階層

<deflist>
<def title="エンジンのリポジトリ">
中核の機能とネイティブのランタイム。小さく、コンパイルが速く、ほぼ全員の役に立つもの。これらは同梱されます。
<a href="Bundled-Plugins.md">同梱プラグイン</a> を参照してください。
</def>
<def title="定番">
一般的なゲーム制作に関係し、AAA で頻繁に使われ、主要な機能を担うもの。ライセンスとサイズが許せば同梱する価値があり、そうでなければチームが追加できるように文書化します。
</def>
<def title="一般的な用途">
必須ではないもの、または高レベルのツール。多くはブループリントの拡張です。プロジェクトが自分で追加します。
</def>
</deflist>

## 定番のプラグイン

### PhysX Instanced Subsystem &mdash; 統合済み、無料

大量の PhysX ベースのインスタンス化ボディを管理するための、ワールドサブシステムとインスタンス化アクターのワークフローです。何千もの個別の `AActor` / `UPrimitiveComponent` を生成する代わりに、描画用には 1 つまたは少数のインスタンス化メッシュのアクターを保ち、サブシステムがインスタンスごとの PhysX の剛体を作成・更新して、そのポーズを ISM/HISM のインスタンスのトランスフォームに書き戻します。

バージョン 1.11 で統合されました。[インスタンス化物理](Instanced-Physics.md) を参照してください。

[リポジトリ](https://github.com/Dragomirson/PhysXInstancedSubsystem) ·
[デモプロジェクト](https://drive.google.com/file/d/1NulunBP2Qre5vLyYnkiqywovsycNuWdQ/view)

### Houdini Engine &mdash; 以前は同梱、商用／無料利用

[LTS](ueVite25-LTS.md) から [March Major](ueVite26-MarchMajor.md) までは同梱されていましたが、[June Major](ueVite26-JuneMajor.md) で一時的に外されました。戻るまでは、SideFX の 4.27 のブランチからプロジェクトごとに追加してください。

Houdini Digital Assets によるプロシージャルなワークフローです。アーティストはエディタ上でアセットのパラメーターを対話的に調整し、Unreal のアセットを入力として使えます。Houdini のプロシージャルエンジンがアセットをクックし、その結果がベイクなしでエディタに表示されます。

[HoudiniEngineForUnreal、Houdini 20.0 / Unreal 4.27 のブランチ](https://github.com/sideeffects/HoudiniEngineForUnreal/tree/Houdini20.0-Unreal4.27)

### Motion Symphony &mdash; 統合済み

Ubisoft 方式のモーションマッチングとポーズマッチング。1.09 で同梱されています。[同梱プラグイン](Bundled-Plugins.md) を参照してください。

### Flecs ECS &mdash; 開発中

[Flecs](https://github.com/SanderMertens/flecs) のエンティティコンポーネントシステムのエンジンレベルの統合です。ワールドサブシステム、ブループリントのエンティティハンドル、ISM による描画のデモ、任意の Flecs Explorer 対応を備えます。アクターをエンティティごとに持つオーバーヘッドがボトルネックになる場合を対象としています。コアクラスの基本コストについては
[UE4 と UE5 のコスト分析](UE4-Versus-UE5-Cost-Analysis.md) を参照してください。社内のブランチにあり、まだ公開リリースには含まれていません。

### PopcornFX &mdash; 商用／無料利用

Blizzard のゲームやレースゲームなど、いくつもの AAA タイトルで使われている独自のパーティクルシステムです。バージョン
2.18.6 が、4.27 と完全に互換な最新のリリースです。Niagara より GPU の性能に優れます。

[リポジトリ](https://github.com/PopcornFX/UnrealEnginePopcornFXPlugin) ·
[v2.18.6 のダウンロード](https://github.com/PopcornFX/UnrealEnginePopcornFXPlugin/archive/refs/tags/v2.18.6.zip)

bunnyofficial による修正版のビルドで、コンパイルエラーが直されています:
[修正版](https://drive.google.com/file/d/1hckpY_1zSLsW6mBqBlDeEgPVSijg9Z_y/view?usp=drive_link)。

### Azure PlayFab &mdash; 商用／無料利用

ライブゲーム向けのバックエンドプラットフォームです。プレイヤーの認証、データの保存、マッチメイキング、マルチプレイヤーのネットワーク、分析、そしてイベントや A/B テストといった LiveOps を、Azure のインフラ上で提供します。

<img src="Plugins2.png" alt="Azure PlayFab のバックエンドサービスの概要" border-effect="line"/>

[PlayFab Unreal Marketplace Plugin](https://github.com/PlayFab/UnrealMarketplacePlugin)

### Wwise &mdash; 商用／無料利用

ゲームのオーディオミドルウェアの事実上の標準で、数百の出荷タイトルがあります。

[Wwise の Unreal 統合](https://www.audiokinetic.com/en/public-library/2025.1.3_9039/?source=UE4&id=index.html)

### Asset Downgrader &mdash; 有料

アセットを 5.6.1、5.5.4、5.4.4、5.3.2、5.2.1、5.1.1、5.0.3、4.27、4.26 にダウングレードします。まずアセットを元のバージョン（5.6）にアップグレードし、その後 `.uasset` ファイルにパッチを当てて、新しいデータを除いたうえで対象のバージョンと互換にします。たとえば 4.27 へのダウングレードでは Nanite のデータが取り除かれます。

<warning>
古いバージョンに存在しない機能は移植できません。マスクマテリアルでの Nanite、新しいマテリアルノード、新しい Niagara のモジュールなどです。ダウングレーダーが移すのはデータであって、機能ではありません。
</warning>

<img src="AssetDwongrader.png" alt="対象のバージョンの選択を示す Asset Downgrader のプラグインの画面" border-effect="line"/>

*ダウングレーダーが対応する対象のバージョン（5.6.1 から 4.26 まで）。*

これは、UE5 のマーケットプレイスのコンテンツを Vite で使うための実用的な方法です。[UE5 からの移行](Migrating-From-UE5.md)
を参照してください。作者の Ciprian Stanciu は Vite の Discord で活動しており、いくつもの Vite のプロジェクトを直接支援してきました。

<img src="CiprianStanciu.png" alt="Vite の Discord での Asset Downgrader の作者" border-effect="line"/>

### HTN Planner &mdash; FAB／有料

Unreal 向けの階層型タスクネットワーク（HTN）の AI フレームワークです。*何を* するかと *どう* するかを分けることで、目標駆動の戦略を構築します。バージョン 1.18.3 が最近 4.27 にバックポートされました。

<img src="HTN.png" alt="Unreal エディタでの HTN Planner のタスクネットワーク" border-effect="line"/>

*階層型タスクネットワークは目標とそれを達成する方法を分けます。これにより、計画をエージェントをまたいで組み合わせられるようになります。*

[Unreal Engine 向けの HTN プラグイン](https://maksmaisak.github.io/htn/front.html)

## 一般的な用途のプラグイン

推奨はしますが、同梱はしていません。プロジェクトごとに追加してください。

### FFMPEG Media Player

標準のメディアフレームワークより多くの動画形式とアルファ付きの動画に対応します。

[bakjos/FFMPEGMedia](https://github.com/bakjos/FFMPEGMedia)

### UI Navigation

ゲームパッドとキーボードでメニューを移動するための、ブループリントで駆動する UI のナビゲーションです。

[goncasmage1/UINavigation、4.27 のブランチ](https://github.com/goncasmage1/UINavigation/tree/4.27_3.0)

### Multiplayer Movement（SMN2）

ブループリントのマルチプレイヤーの移動です。公式には 4.26 まで対応ですが、4.27 でもコンパイルでき動作し、さらに拡張もできます。上流では非推奨になっています。

[Reddy-dev/SMN2](https://github.com/Reddy-dev/SMN2)

### Root Motion Source

4.26 と 4.27 で完全に機能し、実質的に UE5 の Motion Warping に相当する 4.x のものです。標準の UE4 では、ルートモーションソースは GAS を通じてしか正しくネットワーク同期されません。このプラグインはそれを上書きし、ルートモーションソースの機能すべてをブループリントで直接使えるようにします。

遅延の大きいネットワークでの実地テストでは、通常の CMC のロジックに従えば、ルートモーションのアニメーション中にもジッターやサーバー側の補正のないきれいな結果が得られると報告されています。

<img src="Plugins3.png" alt="Root Motion Source のブループリントのノード" border-effect="line"/>

[VJien/RootMotionSource](https://github.com/VJien/RootMotionSource) ·
[解説記事](https://supervj.top/2022/03/24/RootMotionSource/?highlight=root+motion+source)

## プラグインを提案する

提案する前に、次を確認してください。

| 基準 | 要件 |
|---|---|
| エンジンのバージョン | 4.21&ndash;4.27 と互換であること。UE5 専用は対象外 |
| ライセンス | 再配布できること、またはユーザーが自分で入手するものとして明確に文書化されていること |
| サイズ | 同梱したプラグインは全員がクローンします。大きなバイナリの依存関係には正当な理由が必要です |
| コンパイルのコスト | すべてのエンジンのビルドに加わります。[シェーダーコンパイルと PSO](Shader-Compilation-And-PSO.md) を参照 |
| 重複 | すでに同梱されているもの、または標準のものと重複していないか |

そのうえで、どの階層に属すると考えるか、その理由を添えてください。

## 関連項目

- [同梱プラグイン](Bundled-Plugins.md)
- [プラグイン](Plugins.md)
- [UE5 からの移行](Migrating-From-UE5.md)
- [コントリビュート](Contributing.md)
