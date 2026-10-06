# はじめに

<tldr>
<p>
最短の方法は、インストール済みバイナリビルドをダウンロードし、<code>RegistryAdd.bat</code> を実行して
エディタを開くことです。ソースからのビルドは、最新のデスクトップ CPU でおよそ 15〜30 分のコンパイル時間がかかり、
バージョンを固定したツールチェーンが必要です。
</p>
</tldr>

このセクションでは、何もインストールされていない状態から、Unreal Engine Vite のエディタを起動して最初の
プロジェクトを作るまでを案内します。このフォークが自分のプロジェクトに合うかまだ判断していない場合は、先に
[Vite の概要](Introduction-to-Vite.md) を読んでください。ソースビルドには標準の 4.27 と同じ Unreal Engine
ライセンスが適用されます。[ライセンスと著作権](License-And-Copyright.md) を参照してください。

## インストール方法を選ぶ

Vite は 2 つの形態で提供されます。機能的には同じエディタであり、違いはエンジンを自分でコンパイルするかどうか
だけです。

| | インストール済みバイナリビルド | ソースビルド |
|---|---|---|
| セットアップ時間 | 数分 | 15〜30 分のコンパイルと依存関係のダウンロード |
| ディスク使用量 | 小さい（中間ファイルなし） | 大きい（全ソースと中間ファイルを含む） |
| エンジンコードの変更 | 不可 | 可能 |
| エンジンコードのデバッグ | 同梱のシンボルがある場合のみ | 可能 |
| 推奨対象 | アーティスト、デザイナー、評価目的 | プログラマー、フォークへの貢献者 |

多くのチームは混在構成を採用しています。エンジニアはソースビルドを使い、それ以外のメンバーは同じコミットから
作成したインストール済みビルドを使います。作成方法は [インストール済みビルド](Installed-Builds.md) を参照してください。

## 手順

1. [動作環境](System-Requirements.md) を確認し、必要なハードウェアとディスク容量を把握します。
2. [ツールチェーン要件](Toolchain-Requirements.md) に従ってインストールします。この手順は必須で、融通が利きません。
   MSVC や Windows SDK のバージョンが違うと、明確なメッセージではなく分かりにくいコンパイルエラーが発生します。
3. [バイナリビルドをインストール](Install-Binary-Build.md) するか、[ソースからビルド](Build-From-Source.md) します。
4. [最初のプロジェクト](First-Project.md) を作成します。
5. 既存のコンテンツを持ち込む場合は、[UE5 からの移行](Migrating-From-UE5.md) を読みます。

途中で失敗した場合は、[ビルドのトラブルシューティング](Build-Troubleshooting.md) によくあるエラーをまとめています。
ツールチェーンの不一致を示す `C4668: '__has_feature' is not defined` エラーもここで扱っています。

## 標準の Unreal Engine 4.27 との違い

以前に Unreal Engine をソースからビルドしたことがあれば、驚く点が 3 つあります。

**GitDeps は修正済みです。** 標準の 4.27 は CDN のエンドポイントが移転したため、依存関係のダウンロードに失敗します。
Vite には修正が含まれているので、`Setup.bat` は手作業での編集なしに動作します。`Setup.bat` がローカルの変更を
上書きするか尋ねてきたら、`N` と答えてください。

**レイトレーシング GI は有効、個別の RT エフェクトはオプトインです。** レイトレーシングのサポートと動的 DDGI は
既定で有効なので、新規プロジェクトはすぐにレイトレーシングによるグローバルイルミネーションを使えます。
レイトレーシングの反射、シャドウ、アンビエントオクルージョン、半透明は無効の状態で始まり、プロジェクトごとに
有効にします。半透明、コースティクス、RTXDI、パストレーシングは、エンジンを `VITE_RT_PSO_DEBLOAT=0` で
再ビルドしない限りコンパイル対象からも除外されています。[レイトレーシング](Ray-Tracing.md) を参照してください。

**パフォーマンスのためにいくつかのエンジン既定値が変更されています。** オーバーラップイベント、スケルタルメッシュの
設定、ライトマップ UV の生成、一部のプラグインが標準と異なります。これらの変更はフレームタイムだけでなく
ゲームプレイの挙動にも影響するため、出荷前に [エンジン既定値の変更](Engine-Defaults.md) を読んでください。

## Unreal Engine の基礎

このマニュアルが扱うのはフォークであり、その下にあるエンジン全般ではありません。Vite が変更していない部分は
すべて Unreal Engine 4.27 と同じように動作し、Epic による 4.27 のドキュメントが正しい参照先になります。

| トピック | Epic の 4.27 ドキュメント |
|---|---|
| プロジェクト、テンプレート、ディレクトリ構成 | [Working with Unreal Projects and Templates](https://dev.epicgames.com/documentation/unreal-engine/working-with-unreal-projects-and-templates?application_version=4.27) |
| ソースビルド用の Visual Studio のセットアップ | [Setting Up Visual Studio](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-visual-studio-development-environment-for-cplusplus-projects-in-unreal-engine?application_version=4.27) |
| ブループリントとゲームプレイフレームワーク | [Unreal Engine 4.27 documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-4-27-documentation) |

バージョンセレクターは 4.27 のままにしておいてください。UE5 のドキュメントは Vite が意図的に持たないシステムを
説明しており、それに従うことは UE5 から移ってきた人が混乱する典型的な原因です。

## 関連項目

- [Vite の概要](Introduction-to-Vite.md)
- [ツールチェーン要件](Toolchain-Requirements.md)
- [ViteSetup アシスタント](ViteSetup.md)
- [エンジン既定値の変更](Engine-Defaults.md)
- [ライセンスと著作権](License-And-Copyright.md)
