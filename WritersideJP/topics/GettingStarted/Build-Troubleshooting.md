# ビルドのトラブルシューティング

<tldr>
<p>
Vite でのビルド失敗の大半は、別の姿をしたツールチェーンの問題です。ほかの調査を始める前に、
<a href="Toolchain-Requirements.md">ツールチェーン要件</a> に一致する MSVC ツールセットと Windows SDK が、
それぞれ 1 つだけインストールされていることを確認してください。
</p>
</tldr>

このページでは、よく発生するエラーについて、それが実際に何を意味し、どう解消するかをまとめています。

## ツールチェーンのエラー

### `error C4668: '__has_feature' is not defined as a preprocessor macro`

ツールチェーンの不一致を示す典型的なエラーです。Unreal Engine 4.27 はインストールされている MSVC より古く、
UBT がエンジンのヘッダーの想定と異なるプリプロセッサ挙動のツールセットを選んでいます。

**対処法。** サポート対象の MSVC をインストールして他のバージョンを削除し、`BuildConfiguration.xml` で SDK を固定します。
[ツールチェーン要件](Toolchain-Requirements.md) を参照してください。何かを変更したら、プロジェクトファイルを
再生成します。

### UnrealBuildTool が誤ったコンパイラや SDK を選ぶ

UBT はインストール済みのツールセットを走査して自動検出し、基本的に最新のものを優先します。複数インストール
されている場合、それが意図したものとは限りません。

**対処法。** `%APPDATA%\Unreal Engine\UnrealBuildTool\BuildConfiguration.xml` で両方を明示的に固定します。

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <WindowsPlatform>
        <Compiler>VisualStudio2022</Compiler>
        <WindowsSdkVersion>10.0.26100.0</WindowsSdkVersion>
    </WindowsPlatform>
</Configuration>
```

その後、`GenerateProjectFiles.bat` を再実行します。リンク直前のビルドログを確認し、UBT が報告するツールチェーンが
意図したものであることを確かめてください。

### `ViteSetup.bat` が `[FAIL]` の行を出して続行を拒否する

アシスタントはツールチェーンの要件を意図的に検証し、回避手段を用意していません。失敗した行に、不足している
コンポーネントの名前が表示されます。受け付けるのは、MSVC 14.44 以降の Visual Studio 2022、または MSVC 14.50 以降の
Visual Studio 2026 で、どちらの場合も Windows SDK 10.0.26100 のサブバージョン .7705 以降が必要です。原因はたいてい
MSVC ツールセットか SDK のサブバージョンが古いことなので、Visual Studio Installer で更新してください。
[ツールチェーン要件](Toolchain-Requirements.md) を参照してください。

### C# ツールのプロジェクトがビルドできない（SwarmAgent、NetworkProfiler、UnrealControls）

これらは .NET Framework 4.5 を対象としていますが、最近の Visual Studio インストーラーにはその Targeting Pack が
含まれていません。

**対処法。** [ツールチェーン要件](Toolchain-Requirements.md) の説明に従ってインストールします。XML ファイルしかない
`v4.5` フォルダーはランタイムのスタブであり、Targeting Pack ではありません。`v4.5\RedistList\FrameworkList.xml` の
有無を確認してください。

## 依存関係とセットアップのエラー

### `Setup.bat` が依存関係のダウンロードに失敗する

標準の Unreal Engine 4.27 では、GitDeps のエンドポイントが移転したためにこれが起こります。**Vite には修正が含まれて
いる** ので、このフォークでダウンロードに失敗する場合の原因は環境にあります。プロキシ、ファイアウォール、または
以前の実行が中断されてキャッシュが壊れていることが考えられます。

**対処法。** リポジトリのルートにある `UE4_Source_Cache` フォルダーを削除し、`Setup.bat` を再実行します。
`ViteSetup.bat` はセットアップが成功するとこのキャッシュを自動的に削除します。

### `Setup.bat` がローカルの変更を上書きするか尋ねてくる

`N` と答えてください。`Y` と答えるとフォーク固有のファイルが上流の状態に戻り、ビルドが壊れます。

### Win64 ビルドで `astcenc.exe` などのサードパーティ製ツールが見つからない

セットアップ時に Win32 のフォルダーを除外しています。Win64 のインストール済みビルドは、`ARM\Win32\astcenc.exe`
など、Win32 の下にあるツールに依存しています。

**対処法。** `-exclude=Win32` 引数を付けずに `Setup.bat` を再実行します。`ViteSetup.bat` のプリセットは、この理由から
Win32 を除外しません。

## コンパイルとリンクのエラー

### コンパイル中のメモリ不足またはヒープの枯渇

Unreal のユニティビルドは非常に大きな翻訳単位をコンパイルし、積極的に並列化します。コア数が多く RAM が控えめな
マシンでは、既定の並列度でメモリを使い切ることがあります。

**対処法。** `BuildConfiguration.xml` で並列実行数を制限します。

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ParallelExecutor>
        <MaxProcessorCount>12</MaxProcessorCount>
    </ParallelExecutor>
</Configuration>
```

### エディタはビルドできたが起動しない

`UE4Editor`、`ShaderCompileWorker`、`UnrealLightmass` の 3 つのターゲットすべてをビルドしたか確認してください。
エディタのターゲットだけをビルドすると、起動はするものの、シェーダーのコンパイルが必要になった時点で失敗する
バイナリになります。

### エンジンの変更を取り込んだ後にシェーダーや派生データが古くなる

レンダリングの変更はシェーダーキャッシュを無効にします。プル後にシェーダーのコンパイルエラー、マテリアルの欠落、
表示の乱れが起きた場合は、エンジンレベルのキャッシュを消去します。

```batch
WipeShaderCache.bat
```

これにより `Engine\DerivedDataCache`、`Engine\Intermediate\Shaders`、`Engine\Saved\ShaderDebugInfo` が削除されます。
エンジンは次回起動時にこれらを再構築するため、時間がかかります。先にエディタと `ShaderCompileWorker` の
プロセスを終了しておかないと、削除に失敗します。[キャッシュ管理](Cache-Management.md) を参照してください。

## ビルド成功後の実行時の問題

### 新規プロジェクトが想定よりかなり遅い

新規プロジェクトではレイトレーシングのサポートと動的 DDGI が既定で有効なため、空のプロジェクトでも毎フレーム
レイを飛ばしています。ハードウェアレイトレーシング非対応の GPU やローエンドのハードウェアでは、まず DDGI を
確認してください。レイトレーシングの反射、シャドウ、アンビエントオクルージョンは既定で無効です。それらが動いて
いる場合は、プロジェクト設定かポストプロセスボリュームで有効にされています。

**対処法。** `stat gpu` でプロファイリングしてから、不要なものを無効にします。DDGI は
`r.GlobalIllumination.ExperimentalPlugin 0`、それ以外は個別の `r.RayTracing.*` 変数で無効にできます。
[レイトレーシング](Ray-Tracing.md) と [動的 DDGI](DDGI-Dynamic.md) を参照してください。

### ゲームプレイの挙動が標準の 4.27 と異なる

Vite はパフォーマンスのためにいくつかのエンジン既定値を変更しており、その一部はフレームタイムだけでなく挙動にも
影響します。たとえば、プリミティブコンポーネントのオーバーラップイベントは既定で無効です。

**対処法。** [エンジン既定値の変更](Engine-Defaults.md) を全体に目を通してください。変更されたすべての既定値が、
それを変更したコミットへのリンクとともに記載されています。

## サポートを受ける

上記のどれにも当てはまらない場合は、[コミュニティ Discord](https://discord.gg/n9zQrYFhMb) の `#support`
チャンネルが最も早い解決手段です。Visual Studio のバージョン、MSVC ツールセットのバージョン、Windows SDK の
バージョン、ビルドしているブランチ、そしてログの最後ではなく最初のエラーを添えてください。Unreal のビルド出力は
エラーが連鎖するため、最後のエラーが役に立つことはほとんどありません。

## 関連項目

- [ツールチェーン要件](Toolchain-Requirements.md)
- [ソースからのビルド](Build-From-Source.md)
- [キャッシュ管理](Cache-Management.md)
- [エンジン既定値の変更](Engine-Defaults.md)
