# ViteSetup

<tldr>
<p>
エンジンのルートにある <code>ViteSetup.bat</code> は、クローンしたばかりのツリーから、エディタの起動までを 9 つのガイド付きのステップで進めます。推奨は <b>Express</b> の経路です。Win64 の依存関係だけを取得してソースからビルドし、取り除いたものをすべて回復用のフォルダーに移動する軽量化を行います。<code>ViteSetup.bat menu</code> では、個々の操作を選べます。このページは <a href="ueVite26-SeptemberMajor.md">September Major</a> の版について説明します。
</p>
</tldr>

このアシスタントが存在するのは、Unreal のソースビルドのセットアップには多くの手順があり、どれも間違えると分かりにくいエラーになるからです。最初に環境を確認するため、ツールチェーンの部品が欠けていれば、ステップ 5 のリンカーエラーではなく、ステップ 1 で明確なメッセージとともに失敗します。

## ガイドモード

`ViteSetup.bat` を引数なしで実行します。

| ステップ | ソースビルド（Express または Custom） | ビルド済みバイナリのビルド |
|---|---|---|
| 1 | 環境を確認し、ツールチェーンを強制 | 同じ |
| 2 | ビルド方法を選ぶ | 同じ |
| 3 | 依存関係をセットアップ | 依存関係をセットアップ |
| 4 | Visual Studio のプロジェクトファイルを生成 | Visual Studio のプロジェクトファイルを生成 |
| 5 | ソースからエンジンをビルド | インストール済みバイナリとそのアーカイブをビルド |
| 6 | エンジンを軽量化 | ビルドを登録 |
| 7 | ビルドを登録 | デスクトップのショートカットを作成 |
| 8 | デスクトップのショートカットを作成 | 完了（バイナリビルドは起動しない） |
| 9 | エディタを起動 | &mdash; |

各ステップは一時停止するので、続ける前に出力を読めます。失敗するとアシスタントはそこで止まり、先に進まずにエラーコードを報告します。セットアップの前と最後に、予想と実際のディスク使用量を報告します。Windows 向けのソースツリー全体はビルド後に約 137&nbsp;GB になり、Express の経路はそれを減らすためにあります。

## ステップ 1 &mdash; 環境の確認

アシスタントは 2 つのツールチェーンのどちらかを受け付け、どちらもなければ先に進みません。

| 要件 | 受け付けるもの |
|---|---|
| Visual Studio と MSVC | Visual Studio 2022 と MSVC 14.44 以上、**または** Visual Studio 2026 と MSVC 14.50 以上 |
| MSBuild | UnrealBuildTool と C# のツールが必要とします |
| Windows SDK | 10.0.26100、サブバージョン .7705 以上、メジャーは 26100 に固定 |
| .NET Framework のターゲットパック | 4.6.2（UnrealBuildTool、AutomationTool）と 4.5（SwarmAgent と C# のツール） |

両方の Visual Studio がインストールされている場合は、どちらでビルドするかを尋ね、すべてのビルドに `-2022` または `-2026` を渡します。SDK が最低バージョンに満たない場合や .NET 4.5 のターゲットパックがない場合は、インストールを提案し、その後ツールチェーン全体を再確認します。[ツールチェーン要件](Toolchain-Requirements.md) を参照してください。

最近の Visual Studio のインストーラーは既定で提供しなくなったため、最もよく欠けているのは .NET Framework 4.5 のターゲットパックです。[ビルドのトラブルシューティング](Build-Troubleshooting.md) を参照してください。

## ステップ 2 &mdash; ビルド方法を選ぶ

| オプション | 内容 |
|---|---|
| **1. ソースビルド &ndash; Express**（推奨） | 他のプラットフォームにチェックを入れない限り Win64 のみ。最小の依存関係をダウンロードしてコンパイルし、エンジンを軽量化します。 |
| 2. ソースビルド &ndash; Custom | 同じビルドですが、プラットフォーム、任意のコンテンツ、取り除く項目を自分で選びます |
| 3. ビルド済みバイナリのビルド | 使えるエンジンのソースを含まない、パッケージ化されたエンジン。推奨しません。 |

**ソースビルドを選んでください。** それがサポートされる構成です。デバッガーでエンジンのコードにステップインでき、フォークのパッチを適用でき、プルのたびに再ビルドでき、[コンパイル時スイッチ](Compile-Time-Switches.md) を変更できます。ビルド済みバイナリではそのどれもできず、元になるソースビルドより作成に時間がかかり、それに対する不具合報告はサポートできません。それでもバイナリが適している場面は [インストール済みビルド](Installed-Builds.md) を参照してください。

## ステップ 3 &mdash; 依存関係のセットアップ

Express の経路では、Win64、Win32 のサポートファイル、テンプレートは常にダウンロードされ、プラットフォームの選択画面で
Android、Linux、iOS/tvOS、Mac を追加できます。サンプル、フィーチャーパック、ドキュメント、GoogleVR、LeapMotion、WinRT、HTML5、コンソール、そしてチェックを入れなかったすべてのプラットフォームはダウンロードされません。容量の大部分はここで節約されます。

Custom の経路では、代わりにセットアッププロファイルを選べます。

| プロファイル | 内容 |
|---|---|
| Step-by-step assistant | プラットフォームと任意のコンテンツを個別に選び、確認する |
| Recommended Win64 | Win64 のみ。Windows 以外のプラットフォーム、サンプル、テンプレート、フィーチャーパック、ドキュメント、XR、コンソールを除外 |
| Win64 ultra compact | Recommended と同様で、任意のコンテンツを最小にしたもの |
| Win64 + templates / feature packs | プロジェクトのテンプレートとスターターコンテンツを残す |
| Win64 + Android | Android の依存関係を追加 |
| Win64 + Linux | Linux とクロスコンパイルの依存関係を追加 |
| Full setup | `Setup.bat` に `-exclude` 引数を渡さない |

依存関係は一時的な `UE4_Source_Cache` フォルダーを通じて 20 スレッドで取得されます。セットアップが成功するとアシスタントがこのフォルダーを削除するため、その後ディスクに残ることはありません。

## ステップ 5 &mdash; ビルド

ソースビルドは、ソースツリー内で `UE4Editor`、`ShaderCompileWorker`、`UnrealLightmass`、`UnrealInsights` を Win64 の
Development でコンパイルします。

バイナリビルドは、Development と Shipping のゲーム構成で BuildGraph の `Make Installed Build Win64` ターゲットを実行し、その結果をパッケージ化します。WinRAR がインストールされていれば `UE_ViteFork.rar` にアーカイブし、なければ WinRAR の試用版のダウンロードを提案し、それもなければ 7-Zip で `UE_ViteFork.7z` を作成します。

## ステップ 6 &mdash; エンジンの軽量化

Express の経路は、ドライランの確認の後で次のものを移動します。

- Win64 以外のすべてのプラットフォームのフォルダー
- デバッグシンボル（`.pdb`）
- Starter Content と Mobile Starter Content
- NVIDIA のサンプルプロジェクト `NGXTest` と `RTXGI_Test`
- Third Person（C++ と Blueprint）以外のすべてのテンプレート
- `Engine\Plugins\Runtime\VitePlugins` 以下の、ACL と MotionSymphony を除くすべてのプラグイン

<warning>
<p>
最後の項目は、FSR 4、Anti-Lag 2、XeSS、PhysX Instanced Subsystem、KawaiiPhysics、ImGui、GPA、Automatron、SplashAbilities を移動します。プロジェクトでいずれかを使う場合は、Custom の経路を選ぶか、
<code>ViteDebloat_Moved</code> からフォルダーを戻してください。
</p>
</warning>

何も削除はされません。すべてがエンジンのフォルダーの隣の `ViteDebloat_Moved` に配置を保ったまま移動され、参照チェックで残ったツリーが引き続きビルドできることを確認します。その後 Express は、プラグインの除外リスト、UnrealFileServer、Windows 以外のツール、プラットフォームのバイナリを対象とした、任意の 2 回目のパスを提案します。Custom の経路では、同じ選択画面が直接開きます。詳しくは [デブロートガイド](Debloat-Guide.md) を参照してください。

## 登録とショートカット

登録では、エンジンのパスを `HKCU\Software\Epic Games\Unreal Engine\Builds` に `UE_ViteFork` という名前で書き込みます。これにより、`.uproject` ファイルのエンジン関連付けでこのビルドを選べるようになります。その前に、同じフォルダーを指す自動生成の GUID のエントリを削除するため、バージョンの切り替え画面にエンジンが二重に表示されることはありません。

ショートカットのステップでは、`UE4Editor.exe` を指す `UEViteFork.lnk` をデスクトップに作成します。

<note>
<p>
単体の <code>LocalBuilds\RegistryAdd.bat</code> と <code>RegistryRemove.bat</code> は、今も古い名前
<code>UEViteFork</code> を使います。プロジェクトのエンジン関連付けは登録名と完全に一致する必要があるため、1 つのエンジンは
1 つの経路だけで登録してください。ViteSetup がバイナリのパッケージに書き出すスクリプトは <code>UE_ViteFork</code>
を使います。
</p>
</note>

## メニューモード

`ViteSetup.bat menu` はガイド付きの流れを飛ばし、操作を個別に表示します。

| オプション | 操作 |
|---|---|
| 1 | 環境とツールチェーンを確認 |
| 2 | 依存関係をセットアップ（アシスタント） |
| 3 | Visual Studio のファイルを生成 |
| 4 | Unreal Engine のソースをビルド |
| 5 | 依存関係をセットアップしてから Visual Studio のファイルを生成 |
| 6 | `UE4.sln` を開く |
| 7 | セットアッププロファイルを表示 |
| 8 | ビルド済みバイナリをビルド（推奨しません） |
| 9 | エンジンを軽量化（選択画面） |
| 0 | 終了 |

日々の作業にはメニューモードが適しています。モジュールを追加した後のプロジェクトファイルの再生成や、プル後の再ビルドに、ガイド付きの流れ全体は必要ありません。

`ViteSetup.bat --sync-only` はメニューを飛ばし、`Setup.bat` と同じ処理を行います。依存関係の同期、Git のフックの登録、前提ソフトウェアの静かなインストール、エンジンの登録です。残りの引数は GitDependencies に渡されます。ビルドマシンでは、ローカルで変更したファイルを確認なしに上書きするよう `--force` を付けてください。

## 主なパス

| 項目 | パス |
|---|---|
| エディタの実行ファイル | `Engine\Binaries\Win64\UE4Editor.exe` |
| インストール済みビルドのステージング | `LocalBuilds\Engine\Windows` |
| インストール済みビルドのアーカイブ | `LocalBuilds\Engine\UE_ViteFork.rar`（7-Zip の場合は `.7z`） |
| 一時的なダウンロードのキャッシュ | `UE4_Source_Cache`（セットアップの成功後に削除） |
| 軽量化の回復用フォルダー | `..\ViteDebloat_Moved` |
| エンジン関連付け | `UE_ViteFork` |

## 関連項目

- [ソースからのビルド](Build-From-Source.md)
- [ツールチェーン要件](Toolchain-Requirements.md)
- [インストール済みビルド](Installed-Builds.md)
- [ビルドのトラブルシューティング](Build-Troubleshooting.md)
- [デブロートガイド](Debloat-Guide.md)
