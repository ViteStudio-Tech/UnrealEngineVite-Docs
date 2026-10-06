# デブロートガイド

<tldr>
<p>
<code>devops\</code> にあるスクリプトが、1 つの <code>config.txt</code> に従って不要なエンジンのコンテンツを取り除きます。
既定はすべて <b>ドライラン</b> で、<b>削除ではなく移動</b> です。July Major 以降は、取り除いた後のツリーが引き続き
ビルドできることを参照チェックで確認します。<a href="ViteSetup.md">ViteSetup</a> の Express の経路は、同じスクリプトを
自動で実行します。
</p>
</tldr>

Unreal Engine 4.27 のソースツリー全体には、Epic が提供するすべてのプラットフォーム、すべてのワークフロー、すべての
テンプレートへの対応が含まれています。Win64 専用のプロジェクトが使うのはそのごく一部です。ViteSetup は、Windows 向けの
ソースツリー全体をビルド後で約 137&nbsp;GB と見積もっています。デブロートでその多くを取り戻し、ビルド時間も短縮できます。

Vite のオリジナルのデブロートスクリプトは Bikouz によるものです。

## スクリプトの一覧

| スクリプト | 用途 |
|---|---|
| `ueVite-debloat-SetupSlim.bat` | Win64 に絞ってエンジンの依存関係のセットアップを実行し、不要なプラットフォームの依存関係を一切ダウンロードしない |
| `ueVite-debloat-StripExecute.bat` | プラットフォームのバイナリ、Windows 以外のツール、テンプレート、サンプルコンテンツ、必要に応じてプラグインを取り除く |
| `ueVite-debloat-StripDebugSymbols.bat` | `ExcludedPdbs.txt` に従ってデバッグシンボルを取り除く |
| `ueVite-debloat-ValidateRefs.ps1` | ツリーに残ったモジュールが、移動したモジュールを参照していないかを確認し、欠けたものを戻すこともできる。[July Major](ueVite26-JulyMajor.md) 以降。 |
| `ViteSpaceReport.ps1` | セットアップ前に依存関係のマニフェストからダウンロード量を見積もり、セットアップ後にツリーを計測する。ViteSetup が使用。July Major 以降。 |
| `ueVite-ApplyVitePluginDefaults.bat` | Vite のエンジンのプラグインプロファイルを適用または元に戻す。[エンジンの既定値の変更](Engine-Defaults.md#disabled-plugins) を参照。July Major 以降。 |

いずれもエンジンのルートの `devops\` にあります。取り除くスクリプトは `devops\config.txt` を読みます。最初の引数として
別の設定ファイルのパスを渡すこともできます。

## 安全のための仕組み

スクリプトは意図的に慎重に作られています。実行する前に、その仕組みを理解しておく価値があります。

**既定はドライラン。** `DRYRUN=1` では、ファイルに一切触れずにすべての操作を表示します。変更する前に出力を確認して
ください。

**既定は削除ではなく移動。** `MODE=move` は、対象のファイルを相対的な配置を保ったまま `MOVE_DIR` に移すため、コピーし直す
だけで元に戻せます。`MODE=delete` は元に戻せません。

**移動先はエンジンのツリーの中にできない。** ツリーの中に移動先があると後続のパスで再び対象になってしまうため、
スクリプトは拒否します。

**ドライブのルートは拒否される。** エンジンのルートと移動先の両方が確認されます。

**エンジンのルートが検証される。** スクリプトは何かを行う前に `Engine\Binaries\` が存在することを確認します。

**実行後に参照が確認される。** 既定の `VALIDATE_REFERENCES=1` では、取り除く処理の最後に、ツリーに残った `.Build.cs` と
`.uplugin` のファイルを走査し、`MOVE_DIR` に移ったモジュールへの参照がないかを調べます。問題がなければ「No dangling
references in the editor build」と表示され、そうでなければ欠けているモジュールとそれを必要とするものが一覧表示されます。

## 設定

`devops\config.txt` は `KEY=VALUE` の行で構成されます。行を `#` でコメントアウトすると対象を **残し**、コメントを外すと
任意の対象を **有効** にします。この逆転は覚えておく価値があります。コメントアウトされていない `STRIP` の行は、それが
取り除かれることを意味します。

### 基本設定

```
MODE=move
MOVE_DIR=..\ViteDebloat_Moved
DRYRUN=1
VALIDATE_REFERENCES=1
```

`MOVE_DIR` はエンジンのルートを基準に解決されるため、既定ではエンジンと同じ階層のフォルダーになります。

### プラットフォーム

Win64 は常に残ります。`SetupSlim` の実行中に依存関係もダウンロードして残したいプラットフォームは、コメントを外して
ください。

```
#KEEP_PLATFORM=Android
#KEEP_PLATFORM=IOS
#KEEP_PLATFORM=Linux
#KEEP_PLATFORM=Mac
#KEEP_PLATFORM=HTML5
```

これはセットアップの **前に** 行ってください。依存関係をダウンロードしないほうが、ダウンロードしてから削除するより
安上がりです。

### テンプレート

```
STRIP_OTHER_TEMPLATES=1
KEEP_TEMPLATE=TP_ThirdPerson
KEEP_TEMPLATE=TP_ThirdPersonBP
KEEP_TEMPLATE=TemplateResources
```

`Templates\` 以下の、`KEEP_TEMPLATE` の行で指定されていないフォルダーはすべて対象になります。`TemplateResources` は
すべてのテンプレートが共有するため、テンプレートを 1 つでも残すなら残す必要があります。

### 取り除く対象

既定の対象の一覧を、カテゴリーごとに示します。

**Win64 に不要なプラットフォームのバイナリ**

```
STRIP=Engine\Binaries\Win64\Android
STRIP=Engine\Binaries\Win64\IOS
STRIP=Engine\Binaries\Win64\Lumin
STRIP=Engine\Binaries\DotNET\IOS
```

**Windows 以外のデプロイと開発のツール**

```
STRIP=Engine\Extras\Android
STRIP=Engine\Extras\iTunes
STRIP=Engine\Extras\Xcode
STRIP=Engine\Extras\Instruments
STRIP=Engine\Extras\GDBPrinters
STRIP=Engine\Extras\LLDBDataFormatters
STRIP=Engine\Extras\Maya_AnimationRiggingTools
STRIP=Engine\Extras\MayaVelocityGridExporter
```

3ds Max は Windows の DCC ツールなので、3ds Max のスクリプトは既定で残ります。

**UnrealFileServer**

```
STRIP=Engine\Binaries\Win64\UnrealFileServer.exe
#STRIP=Engine\Source\Programs\UnrealFileServer
```

UnrealFileServer は、クックしてステージングしたファイルをリモートのデバイスに提供し、ネットワーク経由の
Cook-on-the-Fly を支えています。ローカルの Win64 向けにだけ開発・パッケージ化し、リモートのデバイスにデプロイせず、
ネットワーク経由の Cook-on-the-Fly を使わず、ファイルサーバーのワークフローでコンソールやモバイルを対象としないので
あれば、取り除いても安全です。

既定ではビルド済みのバイナリが対象で、後でツールを再ビルドできるようにソースのフォルダーは残ります。

**エンジンのコンテンツ**

```
STRIP=Samples\StarterContent
STRIP=Samples\MobileStarterContent
STRIP=FeaturePacks\StarterContent.upack
STRIP=FeaturePacks\MobileStarterContent.upack
STRIP=Samples\NGXTest
STRIP=Samples\RTXGI_Test
#STRIP=Samples\PixelStreaming
```

Starter Content はデブロートの方針に従って取り除かれます。NVIDIA のテストサンプルはデモ用のコンテンツなので、既定で
取り除かれます。残したい場合は該当する行をコメントアウトしてください。特に `RTXGI_Test` は [DDGI](DDGI-Dynamic.md) を
検証するときに役立ちます。Pixel Streaming はデモではなく実際に使う機能なので残ります。

ツリーに存在しない項目は通知とともにスキップされます。これは問題ありません。

## プラグインのパス

プラグインの要件はプロジェクトごとに異なるため、既定では無効です。

```
#PLUGIN_LIST=ExcludedPlugins.txt
```

エンジンのルートにある `ExcludedPlugins.txt` には、約 200 のエンジンのプラグインのパスが並んでいます。モバイルと XR の
プラットフォーム、使っていないソース管理のプロバイダー、Chaos のプラグイン（Vite は [PhysX](PhysX.md) を使うため不要）、
エンタープライズとバーチャルプロダクションのツール、そして多数の実験的なプラグインです。

このファイルは、まずスクリプトと同じ場所で、次にエンジンのルートで探されます。

<warning>
このパスを有効にする前に <code>ExcludedPlugins.txt</code> を読んでください。プロジェクトが必要とするかもしれない項目が
含まれています。<code>Engine/Plugins/Runtime/GameplayAbilities/</code>、
<code>Engine/Plugins/Runtime/ApexDestruction/</code>、<code>Engine/Plugins/Runtime/HairStrands/</code>、
<code>Engine/Plugins/Runtime/Nvidia/</code>（<a href="Upscalers.md">DLSS と Streamline のプラグイン</a> を含む）、そして
<code>Engine/Plugins/Runtime/PhysXVehicles/</code> がすべて一覧に入っています。
<p>
パスを実行する前に、使っているものの行をコメントアウトしてください。
</p>
</warning>

## 実行する

最も簡単なのは [ViteSetup](ViteSetup.md) を使うことです。Express の経路はビルドの後に決まった選択でこれらのスクリプトを
実行し、Custom の経路とメニューのオプション 9 は同じ対象に対する選択画面を開きます。`config.txt` を自分で管理したい
場合は、スクリプトを直接実行してください。

<procedure title="エンジンのインストールをデブロートする" id="run-debloat">
    <step>
        <code>devops\config.txt</code> を開き、コメントアウトされていない <code>STRIP</code> の行をすべて確認します。
        必要なものはコメントアウトします。
    </step>
    <step><code>DRYRUN=1</code> と <code>MODE=move</code> であることを確認します。</step>
    <step>
        <code>ueVite-debloat-StripExecute.bat</code> を実行し、出力をすべて読みます。多くの人がこの手順を飛ばして
        後悔します。
    </step>
    <step><code>DRYRUN=0</code> にしてもう一度実行します。最後の参照チェックの結果を読みます。</step>
    <step>
        エンジンをビルドしてエディタを開きます。プロジェクトが引き続き読み込めること、必要なプラグインがあることを
        確認します。
    </step>
    <step>
        確信が持てたら、<code>MOVE_DIR</code> を削除して実際に容量を取り戻します。そうするまでは、ファイルはディスク上に
        残っています。
    </step>
</procedure>

新しくクローンした場合は、`Setup.bat` の代わりに `ueVite-debloat-SetupSlim.bat` を実行してください。そもそも不要な
プラットフォームの依存関係がダウンロードされなくなります。

## Express の経路が取り除くもの

ViteSetup の Express の経路は、ドライランの確認以外の確認なしに次のものを移動します。

- Win64 以外のすべてのプラットフォームのフォルダー
- デバッグシンボル（`.pdb`）
- Starter Content と Mobile Starter Content
- NVIDIA のサンプルプロジェクト `NGXTest` と `RTXGI_Test`
- Third Person（C++ と Blueprint）以外のすべてのテンプレート
- **`Engine\Plugins\Runtime\VitePlugins` 以下の、ACL と MotionSymphony を除くすべてのプラグイン**

確認すべきは最後の項目です。FSR 4、Anti-Lag 2、XeSS、PhysX Instanced Subsystem、KawaiiPhysics、ImGui、GPA、Automatron、
SplashAbilities が移動されます。プロジェクトでいずれかを使う場合は、Custom の経路を選ぶか、`ViteDebloat_Moved` から
フォルダーを戻してください。その後 Express は、プラグインの一覧、UnrealFileServer、Windows 以外のツール、プラットフォームの
バイナリを対象とした、任意の 2 回目のパスを提案します。

## デバッグシンボル

`ueVite-debloat-StripDebugSymbols.bat` は、`ExcludedPdbs.txt` に従って PDB ファイルを取り除きます。デバッグシンボルは、
ソースビルドのディスク容量の大きな割合を占めます。

デバッグする可能性のあるものはシンボルを残してください。ステップインすることのないエンジンのモジュールのシンボルを
取り除けば大きな節約になりますが、ステップインするモジュールのシンボルを取り除くと、読めるはずのコールスタックが
16 進数の羅列になります。

## 元に戻す

`move` モードでは、`MOVE_DIR` はエンジンのツリーの相対的な配置をそのまま再現しています。中身をエンジンのルートに
コピーし直せば、すべて元に戻ります。

ビルドに必要なものだけを戻すには、検証ツールを使います。

```
powershell -NoProfile -ExecutionPolicy Bypass -File devops\ueVite-debloat-ValidateRefs.ps1 -Restore
```

`-Restore` は、エディタのビルドが参照しているモジュールを戻します。`-RestoreAll` は、プログラム、テンプレート、ゲームの
ターゲットが必要とするものも戻します。

`delete` モードを使った場合、元に戻すにはクローンし直すか `Setup.bat` を再実行する必要があります。

## これが行わないこと

デブロートはディスク容量を減らし、プラグインのパスを通じてビルド時間も短縮します。実行時の性能は **改善しません**。
存在していても無効なプラグインは、実行時に一切コストがかかりません。

実行時の性能については [プロファイリング](Profiling.md) と [エンジンの既定値の変更](Engine-Defaults.md) を参照してください。
ビルド時間については、追加された Vite のプラグインを取り除くと、15 分のフルビルドのうち約 3 分を節約できます。
[シェーダーコンパイルと PSO](Shader-Compilation-And-PSO.md) を参照してください。

## 関連項目

- [ViteSetup](ViteSetup.md)
- [ソースからのビルド](Build-From-Source.md)
- [エンジンの既定値の変更](Engine-Defaults.md)
- [同梱プラグイン](Bundled-Plugins.md)
- [キャッシュ管理](Cache-Management.md)
