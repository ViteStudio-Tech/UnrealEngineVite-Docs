# ツールと自動化

<tldr>
<p>
Vite は、エンジンのライフサイクル全体をカバーするバッチツールを同梱しています。セットアップとビルドには
<code>ViteSetup.bat</code>、インストール済みビルドには <code>RunUAT.bat</code>、パッケージ化と登録には
<code>LocalBuilds\</code> のスクリプト、キャッシュが古くなったときには <code>WipeShaderCache.bat</code> を使います。
</p>
</tldr>

Unreal をソースからビルドするには長い一連の手順が必要で、それぞれに固有の失敗のしかたがあります。Vite はその手順を
ツールで包み、よく使う経路では正確なコマンドラインを覚えておかなくて済むようにしています。

## このセクションの内容

| トピック | 内容 |
|---|---|
| [ViteSetup](ViteSetup.md) | ガイド付きのセットアップとビルドのアシスタント、そのメニューモード |
| [インストール済みビルド](Installed-Builds.md) | 再配布可能なバイナリのエンジンの作成とパッケージ化 |
| [キャッシュ管理](Cache-Management.md) | 問題が起きたときのシェーダーと DDC のキャッシュの消去 |
| [Compiler Explorer](Compiler-Explorer.md) | Godbolt での MSVC と Clang のアセンブリの比較。計測は Quick Bench かローカルのベンチマークで |

## ツールの一覧

| ツール | 場所 | 用途 |
|---|---|---|
| `ViteSetup.bat` | エンジンのルート | Express の経路を備えた 9 ステップのガイド付きセットアップ、または個々の操作のメニュー |
| `ViteDefaults.bat` | エンジンのルート | オーバーラップとスケルタルメッシュの既定値を Vite と標準の 4.27 の間で切り替える。[エンジンの既定値の変更](Engine-Defaults.md) を参照 |
| `RunUAT.bat` | エンジンのルート | BuildGraph によるインストール済みエンジンのビルド |
| `WipeShaderCache.bat` | エンジンのルート | エンジンレベルのシェーダーと DDC のキャッシュを消去 |
| `LocalBuilds\CompressBuild*.bat` | `LocalBuilds\` | ステージングしたインストール済みビルドを 7z のアーカイブにパッケージ化 |
| `LocalBuilds\RegistryAdd.bat` | `LocalBuilds\` | ビルドを `UEViteFork` として登録（ViteSetup は `UE_ViteFork` を使用） |
| `LocalBuilds\RegistryRemove.bat` | `LocalBuilds\` | 登録を解除 |
| `LocalBuilds\MakeShortcut.bat` | `LocalBuilds\` | `UEViteFork.lnk` を作成 |
| `devops\ueVite-debloat-*.bat` | `devops\` | エンジンのデブロートのスイート。[デブロートガイド](Debloat-Guide.md) を参照 |
| `devops\ueVite-ApplyVitePluginDefaults.bat` | `devops\` | Vite のエンジンのプラグインプロファイルを適用または元に戻す。[エンジンの既定値の変更](Engine-Defaults.md#disabled-plugins) を参照 |

## 目的別の選び方

<deflist>
<def title="リポジトリをクローンしたばかり">
<code>ViteSetup.bat</code> を実行し、Express の経路を選んでください。環境のチェックからエディタの起動まで、一連の手順を
すべて案内します。<a href="ViteSetup.md">ViteSetup</a> を参照してください。
</def>
<def title="アーティストに渡すバイナリのエンジンが欲しい">
<code>ViteSetup.bat</code> を実行してステップ 2 でビルド済みバイナリのオプションを選ぶか、<code>RunUAT.bat</code> と
<code>LocalBuilds\</code> のスクリプトを直接使ってください。<a href="Installed-Builds.md">インストール済みビルド</a>
を参照してください。
</def>
<def title="変更後にシェーダーの挙動がおかしい">
<code>WipeShaderCache.bat</code> を実行してください。<a href="Cache-Management.md">キャッシュ管理</a> を参照してください。
</def>
<def title="エンジンがディスクを使いすぎている">
<code>ViteSetup.bat menu</code> でオプション 9 を選ぶか、<code>devops\</code> のデブロートのスイートを直接実行して
ください。<a href="Debloat-Guide.md">デブロートガイド</a> を参照してください。
</def>
<def title="プロジェクトファイルを再生成したいだけ">
<code>ViteSetup.bat menu</code> でオプション 3 を選ぶか、<code>GenerateProjectFiles.bat</code> を直接実行してください。
</def>
<def title="MSVC と Clang のコード生成を比べたい">
<a href="https://gcc.godbolt.org/">Compiler Explorer</a> を開いてください。表示されるのはアセンブリであり、実行時間では
ありません。<a href="Compiler-Explorer.md">Compiler Explorer</a> を参照してください。
</def>
</deflist>

## 関連項目

- [ソースからのビルド](Build-From-Source.md)
- [ツールチェーン要件](Toolchain-Requirements.md)
- [ビルドのトラブルシューティング](Build-Troubleshooting.md)
- [デブロートガイド](Debloat-Guide.md)
- [Compiler Explorer](Compiler-Explorer.md)
