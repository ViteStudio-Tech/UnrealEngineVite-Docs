# ツールチェーン要件

<tldr>
<p>
現在の Vite のツールチェーンは、<b>Visual Studio 2026</b>、<b>MSVC 14.51</b>（14.50 以降を許容）、
<b>Windows SDK 10.0.26100</b> です。Visual Studio 2022 と MSVC 14.44 の組み合わせも引き続きサポートしています。
それ以外の MSVC ツールセットはすべてアンインストールするか選択を外してください。ツールチェーンが合っていないと
明確なエラーにはならず、<code>C4668: '__has_feature' is not defined</code> のような分かりにくいエラーが出ます。
</p>
</tldr>

Unreal Engine Vite をソースからコンパイルするには、バージョンを固定した特定のビルドツール一式が必要です。
Unreal Build Tool はインストール済みのものを走査してツールチェーンを選ぶため、複数の MSVC が共存していることが
ビルド失敗の最も一般的な原因です。このページに記載したものだけをインストールし、それ以外は削除してください。

## サポートされるツールチェーン

Vite は次の組み合わせで検証しています。1 行目が現在の推奨です。

| ツールチェーン | MSVC | Windows SDK | 状態 |
|---|---|---|---|
| Visual Studio 2026（18.9 以降） | 14.51 | 10.0.26100 | **現行。** [August](ueVite26-AugustMajor.md) と [September](ueVite26-SeptemberMajor.md) Major で検証済み。コンパイラ性能が最も高い構成です。 |
| Visual Studio 2026（18.8） | 14.50 | 10.0.26100 | サポート対象。[July Major](ueVite26-JulyMajor.md) で検証済みで、ViteSetup が VS 2026 で受け付ける最小バージョンです。 |
| Visual Studio 2022（最新） | 14.44 | 10.0.26100 | サポート対象。Epic の UE 4.27 Plus ブランチが最後に検証したツールチェーンと一致します。 |
| Visual Studio 2019 / 2022 | 14.29 | 10.0.18362 | 最大の安定性。サポートする最も古い組み合わせで、オリジナルのツールチェーンが必要なプロジェクト向けです。 |

> `ViteSetup.bat` は 2 つのツールチェーンを認識します。MSVC 14.44 以降の Visual Studio 2022 と、MSVC 14.50 以降の
> Visual Studio 2026 です。両方がインストールされている場合はどちらでビルドするかを尋ね、片方だけの場合は自動的に
> 選択します。どちらの場合も、Windows SDK 10.0.26100 のサブバージョン .7705 以降が必要です。
> [ViteSetup アシスタント](ViteSetup.md) を参照してください。
>
{style="note"}

## 必要なコンポーネント

Visual Studio Installer の **個別のコンポーネント** から、以下をインストールします。

- 「C++ によるデスクトップ開発」ワークロード
- MSVC v14.51 &ndash; VS 2026 C++ x64/x86 ビルドツール（または上の表で選んだ行に対応するバージョン）
- Windows 11 SDK（10.0.26100）
- .NET Framework 4.6.2 Targeting Pack &mdash; UnrealBuildTool と AutomationTool に必要
- .NET Framework 4.5 Targeting Pack &mdash; SwarmAgent、SwarmCoordinator、NetworkProfiler、UnrealControls に必要

コンポーネントを手作業で選ぶ代わりに、
[Vite VSConfig](https://drive.google.com/file/d/1NwpPUiM_7yVI_kjhW94kYxvVP42ViV3Q/view?usp=sharing) ファイルを
ダウンロードし、Visual Studio 26 Installer の **構成のインポート** から読み込むこともできます。

### 競合するツールセットの削除

<procedure title="競合する MSVC バージョンを削除する" id="remove-conflicting-msvc">
    <step>Visual Studio Installer を開きます。</step>
    <step>使用している Visual Studio のインストールを探し、<b>変更</b> をクリックします。</step>
    <step><b>個別のコンポーネント</b> タブに切り替えます。</step>
    <step>選んだツールチェーンに必要なもの以外の、MSVC v14.x x64/x86 ビルドツールの項目をすべて外します。</step>
    <step>選んだツールチェーンに必要なもの以外の Windows SDK をすべて外します。</step>
    <step><b>変更</b> をクリックし、インストーラーが完了してからプロジェクトファイルを再生成します。</step>
</procedure>

Windows SDK が複数インストールされていても致命的ではありませんが、リンク時の予期しない問題の原因になりがちです。
1 つに絞れるなら絞ってください。

### .NET Framework 4.5 Targeting Pack

Visual Studio 2022 と 2026 のインストーラーには 4.5 の Targeting Pack が含まれなくなりましたが、エンジンの C# ツールは
今も必要とします。`C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.5` に XML
ファイルしかないフォルダーがある場合、それは .NET ランタイムが残したスタブであり、本物の Targeting Pack では
ありません。`v4.5\RedistList\FrameworkList.xml` の有無で見分けられます。

`ViteSetup.bat` は、Microsoft 公式の NuGet パッケージから自動的にインストールすることを提案します。手作業で行う
場合は次のとおりです。

<procedure title=".NET Framework 4.5 Targeting Pack を手動でインストールする" id="install-net45">
    <step><a href="https://www.nuget.org/api/v2/package/Microsoft.NETFramework.ReferenceAssemblies.net45/1.0.3">Microsoft.NETFramework.ReferenceAssemblies.net45 1.0.3</a> をダウンロードします。</step>
    <step><code>.nupkg</code> ファイルを ZIP アーカイブとして開きます。</step>
    <step><code>build\.NETFramework\v4.5</code> を <code>C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.5</code> にコピーします。管理者権限が必要です。</step>
    <step><code>v4.5\RedistList\FrameworkList.xml</code> が存在することを確認します。</step>
</procedure>

## BuildConfiguration.xml による SDK の固定

Unreal Build Tool は、ツールチェーンの自動検出を上書きするユーザーごとの設定ファイルを読み込みます。複数の
コンパイラや Windows SDK が存在する場合に、特定のものを確実に使わせる方法です。

編集するファイル（VS26）:

```
%APPDATA%\Unreal Engine\UnrealBuildTool\BuildConfiguration.xml
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
  <WindowsPlatform>
    <CompilerVersion>14.51</CompilerVersion> <!-- Current: VS 2026, validated for the August and September Majors -->
    <!--<CompilerVersion>14.50</CompilerVersion> VS 2026 18.8, validated for the July Major -->
    <!--<CompilerVersion>14.44</CompilerVersion> VS22 Option: Latest Epic's 4.27 compliance -->
    <!--<CompilerVersion>14.29</CompilerVersion> Original 4.27 Toolchain VS 2019 + W10 SDK 10.0.18362 / Clang 11.0.0 -->
    <!--<WindowsSdkVersion>10.0.18362.0</WindowsSdkVersion> -->
    <!-- <WindowsSdkVersion>10.0.22621.0</WindowsSdkVersion> -->
    <!-- <WindowsSdkVersion>10.0.26100.0</WindowsSdkVersion> Enable if specification would be needed -->
    <!-- <Compiler>VisualStudio2022</Compiler>  -->
  </WindowsPlatform>
</Configuration>
```

> `BuildConfiguration.xml` の変更は次回のビルドから反映されますが、IDE と UBT の認識を一致させるため、編集後に
> プロジェクトファイルを再生成してください。
>
{style="note"}

## C++ の言語規格

エンジン本体は C++17 でビルドされます。UnrealBuildTool の `CppStandardVersion` は LTS から `Cpp20` を提供しており、
[September Major](ueVite26-SeptemberMajor.md) の C++20 アップグレードによって実用的になりました。UE 5.0 が導入した
方式に従い、エンジンのヘッダーは C++20 の翻訳単位からも正しく解析できるよう保たれているため、エンジンのモジュールを
C++17 のままにしつつ、ゲームのモジュールで C++20 を採用できます。

```c#
// モジュールの .Build.cs に記述
CppStandard = CppStandardVersion.Cpp20;
```

`.Target.cs` でターゲット全体に `CppStandard` を設定する（または `-CppStd=Cpp20` を指定する）には独自の
ビルド環境が必要なため、ソースビルドでのみ有効です。インストール済みエンジンビルドでは、モジュール単位で
設定してください。

## ツールチェーンの確認

長時間のビルドを始める前に、実際に何がインストールされているかを確認してください。`ViteSetup.bat` はこの確認を
自動で行い、要件ごとに `[OK]` または `[FAIL]` を表示します。手作業で確認する場合は、次の場所を調べます。

- `C:\Program Files\Microsoft Visual Studio\<year>\<edition>\VC\Tools\MSVC\<version>\bin\Hostx64\x64\cl.exe`
  &mdash; インストール済みの MSVC ツールセットは、`VC\Tools\MSVC` の下のフォルダー名で分かります。
- `C:\Program Files (x86)\Windows Kits\10\Include\<version>` &mdash; インストール済みの Windows SDK です。

もう 1 つの有効な確認ポイントは、リンク段階が始まる直前のビルド出力を見て、UBT がどのツールチェーンを使っていると
報告しているかを確かめることです。不一致をそこで見つけるほうが、リンク時に見つけるよりはるかに安く済みます。

## 関連項目

- [ソースからのビルド](Build-From-Source.md)
- [ビルドのトラブルシューティング](Build-Troubleshooting.md)
- [ViteSetup アシスタント](ViteSetup.md)
- [動作環境](System-Requirements.md)
- [Compiler Explorer](Compiler-Explorer.md)
