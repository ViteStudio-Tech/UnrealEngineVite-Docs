# インストール済みビルド

<tldr>
<p>
インストール済みビルドは、Epic Games Launcher でインストールしたものと同じように動作する、ビルド済みで再配布可能なエンジンです。<code>RunUAT.bat</code> で作成し、<code>LocalBuilds\</code> のスクリプトでパッケージ化して登録します。
</p>
</tldr>

ソースビルドには、完全なツールチェーン、長いコンパイル、大量のディスク容量が必要です。インストール済みビルドには必要ありません。アーティスト、デザイナー、エンジンの C++ を変更しない人は誰でも、そのまま使えます。

## ビルド

エンジンのルートにある `RunUAT.bat` が、BuildGraph のインストール済みビルドのターゲットを実行します。

```
Engine\Build\BatchFiles\RunUAT.bat BuildGraph
    -script="Engine\Build\InstalledEngineBuild.xml"
    -target="Make Installed Build Win64"
    -nosign
    -set:GameConfigurations=Development;Shipping
    -set:WithWin64=true
    -set:WithWin32=false
    -set:WithMac=false
    -set:WithAndroid=false
    -set:WithIOS=false
    -set:WithTVOS=false
    -set:WithLinux=false
    -set:WithLinuxAArch64=false
    -set:WithDDC=false
    -clean
```

構成は Win64 のみで、ゲームの構成は Development と Shipping です。これは Vite の
[プラットフォームの方針](Platforms.md) に合わせたものです。`WithDDC=false` は Derived Data Cache の生成を省略するため、ビルドが大幅に短くなりますが、その代わりにエンドユーザーの初回起動時にシェーダーのコンパイルが発生します。

[ViteSetup](ViteSetup.md) から実行することもできます（ステップ 2 のオプション 3、またはメニューのオプション 8）。ViteSetup の経路はインクリメンタルで、チェックを入れれば Linux を追加し、結果のパッケージ化まで行います。同梱の
`RunUAT.bat` は `-clean` を渡し、パッケージ化は下記のスクリプトに任せます。

<note>
<p>
ViteSetup は、ビルド済みの経路を推奨しないものとして示しています。ソースビルドはデバッグ、パッチの適用、再ビルドができ、そこから作るバイナリより短い時間で作成できます。インストール済みビルドは、エンジンを一切コンパイルしない人が必要とする場合に使い、ソースビルドと同じコミットから作成してください。
</p>
</note>

<note>
これは長いビルドです。数分ではなく数時間を見込み、十分な空きディスク容量を用意してください。中間出力と最終出力のどちらも大きくなります。
</note>

出力は `LocalBuilds\Engine\Windows` に置かれます。

## パッケージ化

ViteSetup は、自身でビルドしたバイナリのパッケージ化も行います。WinRAR がインストールされていれば
`LocalBuilds\Engine\UE_ViteFork.rar` を作成し、なければ WinRAR の試用版のダウンロードを提案し、それもなければ 7-Zip で
`UE_ViteFork.7z` を作成します。パッケージのルートには、`UE_ViteFork` の関連付け用に書かれた `RegistryAdd.bat`、`RegistryRemove.bat`、`MakeShortcut.bat` が含まれます。

`RunUAT.bat` で作成したビルドの場合は、`LocalBuilds\` にある 4 つのスクリプトが、ステージングしたビルドを 7-Zip で圧縮します。どれも `LocalBuilds\Engine\Windows` にステージングしたビルドがあることを前提とし、環境変数 `SEVEN_ZIP` で別の場所を指定しない限り、7-Zip を `C:\Program Files\7-Zip\7z.exe` から探します。

| スクリプト | デバッグシンボル | プラグイン |
|---|---|---|
| `CompressBuild.bat` | `ExcludedPdbs.txt` に従って除外 | 1 つのアーカイブ |
| `CompressBuildSeparate.bat` | `ExcludedPdbs.txt` に従って除外 | 2 つ目のアーカイブに分割 |
| `CompressBuildSymbols.bat` | `ExcludedPdbs.txt` に従って除外 | 1 つのアーカイブ |
| `CompressBuildSymbolsSeparate.bat` | **含める** | 2 つ目のアーカイブに分割 |

<note>
<code>CompressBuildSymbols.bat</code> は現在 <code>CompressBuild.bat</code> と同一で、どちらも PDB を除外します。アーカイブにシンボルが必要な場合は、<code>-x@ExcludedPdbs.txt</code> を渡さない唯一のスクリプトである
<code>CompressBuildSymbolsSeparate.bat</code> を使ってください。
</note>

4 つとも、メインのアーカイブから `FeaturePacks\`、`Samples\`、`Templates\` を除外します。

出力:

| ファイル | 内容 |
|---|---|
| `LocalBuilds\Engine\UE_ViteFork.7z` | エンジン |
| `LocalBuilds\Engine\ExcludedPlugins.7z` | プラグイン（`Separate` の版のみ） |

### 除外リスト

`ExcludedPdbs.txt` には、エンジンのモジュールとプラグインに対応する約 1,100 の PDB のパスが並んでいます。デバッグシンボルはソースビルドのサイズの非常に大きな割合を占めるため、それを除外することがパッケージ化で最も大きな節約になります。

`ExcludedPlugins.txt` は、[デブロートのスイート](Debloat-Guide.md) が使うものと同じ一覧です。`Separate` の版では、プラグインを取り除くのではなく別のアーカイブに分割します。ユーザーは基本のエンジンを展開し、必要な場合にだけプラグインのアーカイブを追加します。

### プラグインを分割する理由

ほとんどの人が基本のエンジンだけを必要とし、一部の人だけがプラグイン一式を必要とするチームでは、最初にダウンロードするものをずっと小さくできます。分割はアーカイブ単位であって削除ではないため、何も失われません。

## 対象のマシンにインストールする

<procedure title="パッケージ化した Vite のビルドをインストールする" id="install-binary">
    <step><code>UE_ViteFork.rar</code> または <code>UE_ViteFork.7z</code> を最終的な場所に展開します。後で移動すると再登録が必要になります。</step>
    <step><code>ExcludedPlugins.7z</code> を受け取っていて、そのプラグインが必要な場合は、同じフォルダーに上書きで展開します。</step>
    <step>
        展開したルートから <code>RegistryAdd.bat</code> を実行します。これはエンジンのパスを
        <code>HKCU\Software\Epic Games\Unreal Engine\Builds</code> に、ViteSetup のパッケージなら <code>UE_ViteFork</code>、単体の <code>LocalBuilds\</code> のスクリプトなら <code>UEViteFork</code> という名前で書き込みます。
    </step>
    <step><code>MakeShortcut.bat</code> を実行して、エディタを指す <code>UEViteFork.lnk</code> を作成します。</step>
    <step>
        <code>.uproject</code> を右クリックして <b>Switch Unreal Engine version</b> を選び、登録した名前を選択します。
    </step>
</procedure>

パッケージのアーカイブのルートには、`Engine\` と並んで `MakeShortcut.bat`、`RegistryAdd.bat`、`RegistryRemove.bat` が含まれます。ビルド時に含めた場合は、`FeaturePacks\`、`Templates\`、`Samples\` も含まれます。

## 移動と削除

登録には絶対パスが保存されるため、ビルドを移動すると登録が壊れます。

<procedure title="インストール済みビルドを移動する" id="move-binary">
    <step>現在の場所から <code>RegistryRemove.bat</code> を実行します。</step>
    <step>フォルダーを移動します。</step>
    <step>新しい場所から <code>RegistryAdd.bat</code> を実行します。</step>
    <step>古いショートカットは古いパスを指しているので、<code>MakeShortcut.bat</code> をもう一度実行します。</step>
</procedure>

完全に削除するには、`RegistryRemove.bat` を実行し、ショートカットとフォルダーを削除します。

## ソースビルドと併用する

両方を共存させることはできますが、ViteSetup とそのパッケージは同じ `UE_ViteFork` という名前で登録するため、一度に登録できるのは 1 つだけです。最後に登録したほうがプロジェクトから見つかります。単体の `LocalBuilds\RegistryAdd.bat` は古い名前 `UEViteFork` を使います。プロジェクトのエンジン関連付けは登録名と完全に一致する必要があるため、1 つのエンジンに
2 つの経路を混在させないでください。

頻繁に切り替える場合は、どちらが現在登録されているかを控えておくか、レジストリキーを手作業で編集して別々の名前を付けてください。

## 制限事項

インストール済みビルドではエンジンの C++ をコンパイルできません。それを使うプロジェクトも独自の C++ モジュールを持つことはでき、インストール済みエンジンのヘッダーとライブラリに対してコンパイルされますが、エンジンのソースの変更にはソースビルドが必要です。

これには [コンパイル時スイッチ](Compile-Time-Switches.md) も含まれます。プロジェクトでパストレーシングや RTXDI のために
`VITE_RT_PSO_DEBLOAT=0` が必要な場合は、インストール済みビルドを作成する時点でそれを組み込んでおく必要があります。

## 関連項目

- [ViteSetup](ViteSetup.md)
- [バイナリビルドのインストール](Install-Binary-Build.md)
- [ソースからのビルド](Build-From-Source.md)
- [デブロートガイド](Debloat-Guide.md)
- [コンパイル時スイッチ](Compile-Time-Switches.md)
