# Unreal Engine Vite マニュアル

<tldr>
<p>
Unreal Engine Vite は、NvRTX ブランチと Plus ブランチをベースに構築された、パフォーマンスを最優先とする
Unreal Engine 4.27 のフォークです。PhysX を維持したまま DDGI、RTXDI、テッセレーション、SMAA、HBAO+ を追加し、
コンシューマー機クラスのハードウェアでネイティブ解像度かつ高フレームレートの描画を目標としています。
</p>
<p>
初めての方は <a href="Introduction-to-Vite.md">Vite の概要</a> を読み、続いて
<a href="Build-From-Source.md">ソースからのビルド</a> に進んでください。
</p>
</tldr>

Unreal Engine Vite マニュアルへようこそ。このサイトでは、エンジンフォークそのものについて解説します。ビルド方法、
標準の Unreal Engine 4.27 からの変更点、追加されたレンダリングおよび物理システム、そしてプロジェクトを出荷まで
導く方法を扱います。

Vite は実際に開発を進めているチームを対象としています。研究用ブランチでも技術デモでもありません。本書で解説する
すべての機能は、クック、パッケージング、実機での出荷に耐えることを前提としており、マニュアル全体もその前提で
書かれています。

<img src="StylizedRTDemo.png" alt="動的 DDGI でライティングされたスタイライズドシーン。フレームカウンターは 811 FPS を示している" border-effect="line"/>

*完全に動的なレイトレーシング GI だけでライティングしたスタイライズドデモ。RTX 4080 Super、1440p ネイティブで
811 FPS。同じシーンを Unreal Engine 5.7 の Lumen で描画すると 324 FPS です。*

## Vite の目的

Unreal Engine 5.7 と 5.8 は、Lumen、Nanite、仮想シャドウマップ、TSR、Chaos を用いて、PlayStation 5 上で
720p〜1080p の動的内部解像度により約 60 FPS を目標としています。このスタックは仮想化と時間的再構成によって
品質を得ていますが、その代償として処理・ストリーミング・メモリのオーバーヘッド、ノイズ・ゴースト・ブラー、
そしてプロジェクトが何も作っていない段階から高い基本コストを抱えるレンダラーを支払っています。

Nintendo Switch 2 の発売、Steam Deck のような携帯機の定着、そしてハードウェア価格の上昇により、このトレードオフは
ゲームが実際に動作すべきマシンと噛み合わなくなりつつあります。Vite は逆の立場を取ります。厳格なフレームタイム
予算と高いネイティブ解像度を守りながら、高いビジュアル品質を維持することです。

具体的な主張は、UE 5.7 が想定する機能構成に対して実ゲームの FPS で最大 2.5 倍の基本性能向上であり、これは
主張ではなく測定に裏付けられています。詳しくは
[UE4 と UE5 のコスト分析](UE4-Versus-UE5-Cost-Analysis.md) と
[プロジェクトとデモ](ProjectsAndDemos.md) を参照してください。

[![Vite のレイトレーシング GI とレイトレーシング反射](https://img.youtube.com/vi/2vfG3W-Gy5E/maxresdefault.jpg)](https://youtu.be/2vfG3W-Gy5E)

## 約束ではなく測定値

以下の数値はすべて同一シーンでの同条件比較で、速度の倍率として示しています。各測定の方法はリンク先のページに
記載しています。

| 測定項目 | Vite | 比較対象 | 結果 |
|---|---:|---:|---:|
| [動的 DDGI シーン](Global-Illumination.md)、RTX 4080 Super、1440p ネイティブ | 811 FPS | 324 FPS（UE 5.7 の Lumen） | **2.5&times;** |
| [エンジン内でシミュレーションする 3,000 個のキューブ](Physics.md) | 157.88 FPS | 33.26 FPS（UE 5.7 の Chaos） | **4.75&times;** |
| [10,005 ボディのソルバーベンチマーク](Physics.md)、6 スレッド | 11.76 ms | 791.97 ms（Chaos） | **67&times;** |
| [同ベンチマークを標準 PhysX 3.4 と比較](Physics.md)、1〜6 スレッド | 11.76〜35.60 ms | 15.82〜49.61 ms（NVIDIA PhysX 3.4） | **1.34〜1.39&times;** |
| [シェーディングモデルのゲーティング](ueVite26-JulyMajor.md)、UT Vite シーン、1440p | 264.44 FPS | ゲーティング前 235.56 FPS | **+12.3%** |

## 最新リリース

<deflist>
<def title="ueVite26 September Major">
現行リリースです。C++20 への初期アップグレード、エンジンの C# ツール向け .NET アップグレード、Lightmass の
Embree 4.4.1 化、そして SSGI の高速化を含みます。詳しくは
<a href="ueVite26-SeptemberMajor.md">ueVite26 September Major</a> を参照してください。
</def>
<def title="ueVite26 August Major">
これまでで最大のリリースで、438 件の変更を含みます。UE5 からのエディタ・メモリ関連バックポート、レイトレーシング
反射とスペキュラーオクルージョンの改良、Gameplay Ability System の更新、macOS への移植などです。詳しくは
<a href="ueVite26-AugustMajor.md">ueVite26 August Major</a> を参照してください。
</def>
<def title="すべてのリリース">
LTS ベースから毎月のメジャーリリースまで、アップグレード時の注意点と全コミット履歴をまとめています。
<a href="Release-Notes.md">リリースノート</a> を参照してください。
</def>
</deflist>

## どこから始めるか

いま取り組んでいる作業に合った入口を選んでください。

| やりたいこと | 参照先 |
|---|---|
| Vite とは何か、自分のプロジェクトに合うかを知りたい | [Vite の概要](Introduction-to-Vite.md) |
| 自分のマシンでエンジンを動かしたい | [はじめに](Getting-Started.md) |
| ソースからエンジンをコンパイルしたい | [ソースからのビルド](Build-From-Source.md) |
| コンパイルやセットアップのエラーを解決したい | [ビルドのトラブルシューティング](Build-Troubleshooting.md) |
| 既存の UE5 プロジェクトを Vite に移行したい | [UE5 からの移行](Migrating-From-UE5.md) |
| リリースでの変更点を確認したい | [リリースノート](Release-Notes.md) |
| Lumen を使わずにシーンをライティングしたい | [グローバルイルミネーション](Global-Illumination.md) |
| ゲームプレイコードの Chaos を PhysX に置き換えたい | [PhysX](PhysX.md) |
| コンソール変数を探したい | [コンソール変数](Console-Variables.md) |
| フォークに変更を貢献したい | [コントリビュート](Contributing.md) |

## Vite の中核となる機能

<deflist>
<def title="動的 DDGI">
レイトレーシングによるイラディアンスプローブボリュームです。原理的にノイズが発生せず、完全に動的で、同等の
シーンではハードウェア Lumen のおよそ 2 倍のフレームレートで動作します。詳しくは
<a href="DDGI-Dynamic.md">動的 DDGI</a> を参照してください。
</def>
<def title="静的 DDGI">
同じプローブ表現を、ほぼ一瞬で終わるベイクで利用します。従来のベイクライティングより高精度なバウンスと、
動くオブジェクトへのより良いカバレッジが得られます。レイトレーシング非対応の GPU でも利用できます。詳しくは
<a href="DDGI-Static.md">静的 DDGI</a> を参照してください。
</def>
<def title="最適化されたレイトレーシング反射">
PS5 クラスの GPU で 4K ネイティブ 60 FPS を実現できます。DDGI が有効な場合、反射レイは二次バウンスで黒を返す
代わりにプローブのイラディアンスをサンプリングします。詳しくは
<a href="RT-Reflections.md">レイトレーシング反射</a> を参照してください。
</def>
<def title="UE4 世代の SSGI">
SSGI は UE5 で Lumen に統合された際に品質と性能が低下し、別の GI ソリューションと併用できなくなりました。
Vite では DDGI ときれいに組み合わせられます。詳しくは <a href="SSGI.md">SSGI</a> を参照してください。
</def>
<def title="PhysX 3.4">
新しい Clang 向けにライブラリを再ビルドし、Blast に対応し、ベンダーを問わず動作する GPU パーティクルを
備えています。同じワークロードで Chaos より測定可能なほど高速です。詳しくは <a href="PhysX.md">PhysX</a> を
参照してください。
</def>
<def title="Apex Destruction と Cloth">
どちらも UE5 で非推奨となった後に削除され、既存アセットの移行手段はありませんでした。Vite では引き続き
動作します。詳しくは <a href="Destruction-And-Cloth.md">破壊とクロス</a> を参照してください。
</def>
<def title="RTXDI">
MegaLights よりノイズの少ない代替手段です。5.1 以降の Lumen 統合版ではなく、スタンドアロン版を採用しています。
詳しくは <a href="RTXDI.md">RTXDI</a> を参照してください。
</def>
<def title="テッセレーション">
距離とディスプレイスメントに基づくジオメトリディテールです。Nanite のオーバーヘッドなしに、より滑らかな表面、
より良いシルエット、実行時の高周波ディテールを実現します。詳しくは <a href="Tessellation.md">テッセレーション</a>
を参照してください。
</def>
</deflist>

## パフォーマンス目標

以下の目標はすべてレイトレーシングを含みます。詳細と測定条件は
[パフォーマンス目標](Performance-Targets.md) を参照してください。

| PS5 クラスの目標 | 内容 |
|---|---|
| **スタイライズド、4K 120 FPS** | スタイライズドデモで示した RT DDGI。競技性の高いマルチプレイヤー向け。 |
| **パフォーマンス（ハイエンド）、4K 60 FPS** | Unreal Tournament Vite デモで示した DDGI、RT 反射、テッセレーション。 |
| **フィデリティ（ハイエンド）、4K 30 FPS** | 同じ構成を、ジオメトリ密度の高い大規模オープンワールド向けに拡張。 |
| **フィデリティ（フル RT）、1440p 30 FPS** | DDGI と RT 反射に加えて RTAO と RT シャドウを使用。 |

## マニュアルの構成

<deflist>
<def title="はじめに">
インストール、ツールチェーンの準備、ソースからのビルド、最初のプロジェクトの作成、そして既存の
Unreal Engine 5 プロジェクトの移行を扱います。<a href="Getting-Started.md">はじめに</a> を参照してください。
</def>
<def title="エンジン概要">
このフォークが NvRTX 4.27 をベースとする理由、設計の基準となるパフォーマンス目標、そして UE4 と UE5 の間の
測定可能なコスト差がどこから生じるかを説明します。<a href="Engine-Overview.md">エンジン概要</a> を参照してください。
</def>
<def title="レンダリング">
グローバルイルミネーション、レイトレーシング、シェーディングモデル、アンチエイリアシング、アップスケーリング、
テッセレーション、アンビエントオクルージョン、カラーマネジメントを扱います。マニュアル最大のセクションであり、
標準 4.27 からの差分の大半がここにあります。<a href="Rendering.md">レンダリング</a> を参照してください。
</def>
<def title="物理">
出荷用の物理バックエンドである PhysX 3.4、高速パス、固定タイムステップ、Apex Destruction、Apex Cloth、Blast、
そして大規模なインスタンス化剛体を扱います。<a href="Physics.md">物理</a> を参照してください。
</def>
<def title="パフォーマンスと最適化">
プロファイリングツール、Vite が標準で変更しているエンジン既定値、シェーダーコンパイルと PSO の挙動、
スケーラビリティ、そしてイテレーションを速めるためのエンジンの軽量化方法を扱います。
<a href="Performance.md">パフォーマンスと最適化</a> を参照してください。
</def>
<def title="対応プラットフォーム">
各ターゲットプラットフォームの対応状況、利用可能なレンダラーパス、そして Vite がチューニングの基準とする
ハードウェアを説明します。<a href="Platforms.md">対応プラットフォーム</a> を参照してください。
</def>
<def title="プラグイン">
エンジンに同梱されるプラグインと、新しいプラグインを提案する際の審査プロセスを扱います。
<a href="Plugins.md">プラグイン</a> を参照してください。
</def>
<def title="ツールと自動化">
<code>ViteSetup.bat</code> アシスタント、インストール済みエンジンビルド、パッケージングと配布用スクリプト、
キャッシュ管理、そして MSVC と Clang のコード生成を比較する Compiler Explorer を扱います。
<a href="Tools.md">ツールと自動化</a> を参照してください。
</def>
<def title="プロジェクトとデモ">
ダウンロード可能なサンプルプロジェクトとベンチマークシーンを、計測に使ったハードウェアの数値とともに紹介します。
<a href="ProjectsAndDemos.md">プロジェクトとデモ</a> を参照してください。
</def>
<def title="リリースノート">
LTS ベース以降のすべての公開リリースについて、ハイライト、アップグレード時の注意点、各リリースブランチの
全コミット履歴をまとめています。<a href="Release-Notes.md">リリースノート</a> を参照してください。
</def>
<def title="コントリビュート">
コーディングガイドライン、コミットとプルリクエストの規約、そして UE5 の変更をフォークに取り込むための
バックポートの手順を扱います。<a href="Contributing.md">コントリビュート</a> を参照してください。
</def>
<def title="リファレンス">
コンソール変数のリファレンス、コンパイル時スイッチ、ライセンスと著作権、用語集、よくある質問をまとめています。
<a href="Reference.md">リファレンス</a> を参照してください。
</def>
</deflist>

## Vite テクノロジー

エンジンを支えるレンダリング、物理、ジオメトリの研究開発は、
[Vite テクノロジー](https://vitestudio-tech.github.io/UnrealEngineVite-Docs/tech/jp/) サイトで製品群として紹介して
います。リアルタイムのグローバルイルミネーションとパストレーシングを担う **Vite ReSTIR**、**ViteX Physics**、
**Vite BRDF**、ジオメトリ技術の **Vite Vertis**、そして **Vite Hair FX** です。ライセンスや提携を検討している
スタジオの方は、まずこちらをご覧ください。

## コミュニティとプロジェクトのリンク

| リソース | リンク |
|---|---|
| エンジンリポジトリ | [ViteStudio-Tech](https://github.com/ViteStudio-Tech) |
| コミュニティ Discord | [discord.gg/n9zQrYFhMb](https://discord.gg/n9zQrYFhMb) |
| 作業計画（Trello） | [UE Vite PhysX Studio Fork](https://trello.com/b/JKyBFS5X/ue-vite-physx-vite-studio-fork) |
| 公開アセットドライブ | [Google ドライブ](https://drive.google.com/drive/folders/16FOkb5u6GSqHiWeAm50NaxZ19QFBwZeI?usp=sharing) |
| 開発の支援 | [ko-fi.com/vitestudio](https://ko-fi.com/vitestudio) |
| 最新情報 | [@theredpix](https://x.com/theredpix) |

> Vite は少人数のエンジンプログラマーチームによってオープンに開発されています。貢献を希望する方は
> [コントリビュート](Contributing.md) を読み、Discord で Forker ロールを申請してください。
>
{style="note"}
