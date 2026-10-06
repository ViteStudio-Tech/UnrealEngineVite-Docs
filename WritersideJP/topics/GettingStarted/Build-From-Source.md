# ソースからのビルド

<tldr>
<p>
<code>Setup.bat</code>（上書きを尋ねられたら <code>N</code>）&rarr; <code>GenerateProjectFiles.bat</code>
&rarr; <b>Development Editor</b> / <b>Win64</b> で <b>UE4</b> をビルドします。または <code>ViteSetup.bat</code> を
実行して、アシスタントにすべてを任せます。
</p>
</tldr>

このページでは、Windows でソースからエンジンをビルドする手順を説明します。先に
[ツールチェーン](Toolchain-Requirements.md) をインストールしてください。Vite で報告されるビルド失敗のほとんどは、
コードではなくツールチェーンの問題です。

Unreal Engine をソースからビルドしたことがない場合は、Epic の
[4.27 向け Visual Studio セットアップガイド](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-visual-studio-development-environment-for-cplusplus-projects-in-unreal-engine?application_version=4.27)
が今でも最良の予備知識になります。

## ViteSetup によるガイド付きビルド

リポジトリのルートには `ViteSetup.bat` が同梱されています。これは環境チェック、ツールチェーンの検証、
プラットフォームを選んでの依存関係のセットアップ、プロジェクトファイルの生成、ソースまたはバイナリのビルド、
エンジンの登録、デスクトップショートカットの作成、そして任意のデブロートまで、一連の流れを順に実行する
アシスタントです。

```batch
ViteSetup.bat
```

個々の手順を単独で実行できる上級者向けメニューは次のとおりです。

```batch
ViteSetup.bat menu
```

アシスタントは、20 分かけてコンパイルする前に不足している前提条件を検出してくれるため、初回のビルドには
推奨の方法です。画面とオプションの詳しい説明は [ViteSetup アシスタント](ViteSetup.md) を参照してください。

> アシスタントはツールチェーンの要件を回避手段なしに検証します。続行を拒否した場合は、どのコンポーネントが
> 不足しているかを正確に表示します。
>
{style="note"}

## 手動ビルド

自分で手順を進めたい場合は、アシスタントが行っている内容は次のとおりです。

### 1. 依存関係のダウンロード

```batch
Setup.bat
```

このフォークでは GitDeps が修正済みなので、手作業での編集は不要です。ローカルの変更を上書きするか尋ねられたら
`N` と答えてください。

`Setup.bat` は不要なプラットフォームやコンテンツを除外する `-exclude=` 引数を受け付け、ダウンロード量と
ディスク使用量を大幅に減らせます。Win64 のみのセットアップはおおよそ次のようになります。

```batch
Setup.bat -exclude=Android -exclude=IOS -exclude=TVOS -exclude=Mac -exclude=MacOSX ^
          -exclude=Linux -exclude=Linux64 -exclude=HTML5 -exclude=WinRT ^
          -exclude=PS4 -exclude=XboxOne -exclude=Switch -exclude=Dingo ^
          -exclude=Samples -exclude=Templates -exclude=FeaturePacks -exclude=Engine/Documentation
```

> Win32 のフォルダーは除外しないでください。Win64 のインストール済みビルドは、`ARM\Win32\astcenc.exe` など
> Win32 の下にあるサードパーティ製ツールに依存しています。
>
{style="warning"}

`ViteSetup.bat` はこれらを名前付きのプリセットとして提供しています。**Recommended Win64**、
**Win64 ultra compact**、**Win64 + templates / feature packs**、**Win64 + Android**、**Win64 + Linux**、
**Full setup** の 6 種類で、**Show setup profiles** メニューからそれぞれの `Setup.bat` のコマンドラインを
正確に表示できます。

### 2. プロジェクトファイルの生成

```batch
GenerateProjectFiles.bat
```

これにより、リポジトリのルートに `UE4.sln` が生成されます。

<img src="UE4SolutionFiles.jpg" alt="プロジェクトファイル生成後のリポジトリルートをエクスプローラーで表示したもの。UE4.sln がある" border-effect="line"/>

*生成に成功すると、セットアップスクリプトと並んで `UE4.sln` が作られます。見当たらない場合は生成に失敗しています。
Visual Studio を開く前に、出力を確認してください。*

### 3. ビルド

`UE4.sln` を開き、まだ設定されていなければ **UE4** をスタートアッププロジェクトに設定します。**Win64** の
**Development Editor** 構成をビルドします。

<img src="VSBuildUE4.jpg" alt="Visual Studio のソリューションエクスプローラーで UE4 プロジェクトを選択し、ビルドコマンドを開いた状態" border-effect="line"/>

*ソリューション全体ではなく、**Engine** の下の **UE4** をビルドしてください。ソリューション全体をビルドすると、
エディタのビルドに不要なプログラムターゲットまでコンパイルされます。*

コマンドラインでは次のように実行します。

```batch
Engine\Build\BatchFiles\Build.bat UE4Editor Win64 Development -WaitMutex
Engine\Build\BatchFiles\Build.bat ShaderCompileWorker Win64 Development -WaitMutex
Engine\Build\BatchFiles\Build.bat UnrealLightmass Win64 Development -WaitMutex
```

エディタを正しく動作させるには 3 つのターゲットすべてが必要です。`ViteSetup.bat` はこの順序でビルドします。

### 4. エンジンの登録

`.uproject` ファイルからこのビルドを見つけられるよう、現在のユーザーの Unreal Engine ビルドキーに登録します。

```batch
reg add "HKCU\Software\Epic Games\Unreal Engine\Builds" /v UE_ViteFork /t REG_SZ /d "<engine root>" /f
```

その後、プロジェクトの `.uproject` ファイルに `"EngineAssociation": "UE_ViteFork"` を設定します。アシスタントは
この手順を代行し、同じフォルダーを指している古い GUID キーのエントリも整理します。

## ビルド時間

コンパイル時間はコア数でほぼ決まります。参考として、Ryzen 9 9950X3D でリポジトリをフルビルドするとおよそ 15 分
かかり、同梱の Vite プラグインを外すとおよそ 12 分に短縮されます。この差の大部分は Houdini プラグインによる
もので、同プラグインは [June Major](ueVite26-JuneMajor.md) で既定のセットから外されました。プラグインの網羅性より
イテレーション速度を重視する場合は、[デブロートガイド](Debloat-Guide.md) を参照してください。

## インストール済みビルドの作成

ソースビルドが動作したら、チームの他のメンバー向けに再配布可能なインストール済みビルドに変換できます。リポジトリ
ルートの `RunUAT.bat` は BuildGraph の `Make Installed Build Win64` ターゲットを実行し、結果を
`LocalBuilds\Engine\Windows\` に書き出します。

```batch
RunUAT.bat
```

オプションの全一覧は [インストール済みビルド](Installed-Builds.md) を、圧縮スクリプトについては
[パッケージングと配布](Installed-Builds.md) を参照してください。

## 関連項目

- [ツールチェーン要件](Toolchain-Requirements.md)
- [ビルドのトラブルシューティング](Build-Troubleshooting.md)
- [ViteSetup アシスタント](ViteSetup.md)
- [インストール済みビルド](Installed-Builds.md)
- [キャッシュ管理](Cache-Management.md)
