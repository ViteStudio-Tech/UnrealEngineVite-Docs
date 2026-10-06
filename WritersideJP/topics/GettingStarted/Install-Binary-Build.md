# バイナリビルドのインストール

<tldr>
<p>
ビルドのアーカイブ（<code>UE_ViteFork.rar</code>、7-Zip で圧縮した場合は <code>UE_ViteFork.7z</code>）を展開し、<code>RegistryAdd.bat</code> でエンジンを登録し、
<code>MakeShortcut.bat</code> でデスクトップ用のランチャーを作成してから、<code>.uproject</code> に
<code>"EngineAssociation": "UE_ViteFork"</code> を設定します。
</p>
</tldr>

インストール済みビルドは、コンパイル済みで再配布可能なエディタ一式です。Epic Games Launcher でインストールした
エンジンと同じように振る舞い、プロジェクトを開いたりクックしたりはできますが、エンジンのソースを変更したり
デバッグしたりはできません。アーティスト、デザイナー、そしてフォークを評価する方に適した選択肢です。

インストール済みビルドは、チームがソースビルドから作成しています。自分で作成する必要がある場合は
[インストール済みビルド](Installed-Builds.md) を参照してください。

## ビルドアーカイブの内容

パッケージ化された Vite のビルドを展開すると、次の内容を含むフォルダーができます。

| 項目 | 用途 |
|---|---|
| `Engine\` | エンジン本体（`Engine\Binaries\Win64\UE4Editor.exe` を含む） |
| `MakeShortcut.bat` | エディタの実行ファイルを指す `UEViteFork.lnk` を作成 |
| `RegistryAdd.bat` | フォルダーを `UE_ViteFork` のエンジン関連付けとして登録 |
| `RegistryRemove.bat` | その登録を削除 |
| `Templates\` | プロジェクトテンプレート（ビルドに含めた場合） |
| `FeaturePacks\` | フィーチャーパック（ビルドに含めた場合） |
| `Samples\` | サンプルコンテンツ（ビルドに含めた場合） |

軽量版のビルドでは、テンプレート、フィーチャーパック、サンプル、デバッグシンボルを省いています。メインの
アーカイブを小さく保つためにプラグインを分離した `ExcludedPlugins.7z` が付属するビルドもあります。それらの
プラグインが必要な場合は、同じフォルダーに上書きで展開してください。

## インストール

<procedure title="インストール済みビルドをインストールして登録する" id="install-binary">
    <step>
        アーカイブを、スペースや非 ASCII 文字を含まないパス（例:
        <code>D:\Engines\UE_ViteFork</code>）に展開します。<code>Program Files</code> は避けてください。
        エディタは自身のディレクトリに書き込むため、権限の確認ダイアログに悩まされます。
    </step>
    <step>
        ビルドに <code>ExcludedPlugins.7z</code> が別途付属していて、そのプラグインが必要な場合は、
        ここで同じフォルダーに展開します。
    </step>
    <step>
        <code>RegistryAdd.bat</code> を実行します。これはエンジンのパスを
        <code>HKCU\Software\Epic Games\Unreal Engine\Builds</code> に <code>UE_ViteFork</code> という名前で書き込み、
        同じフォルダーを指していた古い GUID キーのエントリを削除します。
    </step>
    <step>
        <code>MakeShortcut.bat</code> を実行し、エンジンフォルダーの隣に <code>UEViteFork.lnk</code> を作成します。
    </step>
    <step>
        ショートカットから、または <code>Engine\Binaries\Win64\UE4Editor.exe</code> を直接実行してエディタを
        起動します。
    </step>
</procedure>

> 登録はユーザー単位で、`HKCU` に書き込まれます。エンジンを使う Windows のユーザーアカウントごとに、一度
> `RegistryAdd.bat` を実行する必要があります。
>
{style="note"}

## プロジェクトをビルドに関連付ける

`.uproject` ファイルをテキストエディタで開き、エンジンの関連付けを設定します。

```json
{
    "FileVersion": 3,
    "EngineAssociation": "UE_ViteFork",
    "Category": "",
    "Description": ""
}
```

インストール済みビルドのアーカイブに同梱されたプロジェクトには、すでにこの設定が入っています。ビルドを登録すると、
`.uproject` を右クリックして **Switch Unreal Engine version** を選んだときの一覧に `UE_ViteFork` が表示されます。

## ビルドの移動と削除

レジストリのエントリは絶対パスを保存しているため、エンジンフォルダーを移動すると関連付けが壊れます。ビルドを
移動する場合は次のようにします。

1. 移動前の場所で `RegistryRemove.bat` を実行するか、`UE_ViteFork` の値を手作業で削除します。
2. フォルダーを移動します。
3. 移動後の場所で `RegistryAdd.bat` を実行します。

完全にアンインストールするには、`RegistryRemove.bat` を実行してからフォルダーを削除します。エンジンディレクトリと
`HKCU` の 1 つのレジストリ値以外には、`%LOCALAPPDATA%\UnrealEngine` と `%APPDATA%\Unreal Engine` の通常の
ユーザー別 Unreal ディレクトリを除いて何も書き込まれません。

## ソースビルドとバイナリビルドの併用

両方をインストールしておくこともできます。異なる名前で登録すれば別々のエンジン関連付けになるので、ソースビルドと
インストール済みビルドを同時に使いたい場合は、登録前にどちらかの `ENGINE_ASSOCIATION` の値を変更してください。
ただし、両方のビルドはユーザー別の Unreal ディレクトリを共有するため、エディタのレイアウトや一部の設定は共通に
なります。

## 関連項目

- [はじめに](Getting-Started.md)
- [インストール済みビルド](Installed-Builds.md)
- [パッケージングと配布](Installed-Builds.md)
- [最初のプロジェクト](First-Project.md)
