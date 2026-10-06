# ドキュメントへの貢献

<tldr>
<p>
このドキュメントは JetBrains Writerside のプロジェクトで、英語の <code>Writerside\</code> と日本語の
<code>WritersideJP\</code> の 2 つのモジュールがあります。Markdown のファイルを両方に追加し、両方のツリーに登録して
<code>main</code> にプッシュすると、GitHub Actions が両言語と Vite Technology のサイトをビルドし、GitHub Pages に
デプロイします。
</p>
</tldr>

エンジンに遅れたドキュメントは、ドキュメントがないより悪いものです。人はそれを信頼するからです。既定値を変える、
コンソール変数を追加する、機能をコンパイル対象から外す、といった変更をしたら、それを説明するページも同じ作業の中で変える
必要があります。

## リポジトリの構成

| パス | 内容 |
|---|---|
| `Writerside\topics\` | 英語のトピックの Markdown ファイル。セクションごとにサブフォルダーで整理 |
| `Writerside\images\` | 両言語の画像。ファイル名だけで参照 |
| `Writerside\hi.tree` | 英語のナビゲーションツリー（インスタンス `hi`）。ここにないトピックは公開されない |
| `Writerside\cfg\vite-theme.html` | 共通のテーマ。ヘッダー、ナビゲーション、ランディングページのスタイル |
| `WritersideJP\topics\` | 日本語のトピック。英語と同じファイル名とフォルダー |
| `WritersideJP\jp.tree` | 日本語のナビゲーションツリー（インスタンス `jp`）。同じ順序で、タイトルは日本語 |
| `Tools\ReleaseNotes\generate_release_notes.py` | リリースノートのページのコミットの記録を再生成する |
| `ViteTech\` | Vite Technology のサイト。`src\pages\en` と `src\pages\ja` を `build.py` でビルド |
| `.github\workflows\DocsBuild.yml` | ビルドとデプロイのパイプライン |

## トピックを追加する

<procedure title="ドキュメントのページを追加する" id="add-topic">
    <step>
        適切な <code>Writerside\topics\</code> のサブフォルダーに Markdown のファイルを作成します。名前は
        <code>Title-Case-With-Hyphens.md</code> の形にします。
    </step>
    <step>
        <code>Writerside\hi.tree</code> の適切なセクションに <code>&lt;toc-element topic="Your-File.md"/&gt;</code>
        のエントリを追加します。
    </step>
    <step>
        相互にリンクします。親のセクションのページのトピックの表と、関連するページの <b>関連項目</b> の一覧に追加します。
    </step>
    <step>
        <code>WritersideJP\topics\</code> の同じパスに日本語のページを作成し、<code>WritersideJP\jp.tree</code> の同じ
        位置に日本語の <code>toc-title</code> とともに追加します。まだ翻訳できない場合は、2 つのツリーが一致するように
        英語のページをコピーしておきます。
    </step>
    <step><code>main</code> にプッシュします。ワークフローが自動でビルドしてデプロイします。</step>
</procedure>

<note>
画像と <code>vite-theme.html</code> は英語のモジュールにだけ置きます。ワークフローは日本語のビルドの前にそれらを
<code>WritersideJP</code> にコピーし、そのコピーは Git で無視されます。<code>WritersideJP\images\</code> に画像を
コミットしないでください。
</note>

<note>
Writerside はトピックのリンクをパスではなくファイル名で解決するため、<code>[Ray Tracing](Ray-Tracing.md)</code> は
どちらのファイルがどのフォルダーにあっても機能します。そのため、ファイル名はモジュール全体で一意でなければなりません。
</note>

## 執筆の決まり

### 構成

ほとんどのページは同じ形をしています。

1. `# タイトル`
2. 答えを 2、3 文で示す `<tldr>` のブロック
3. 本文のセクション
4. `## 関連項目` の一覧

内容のあるページでは `<tldr>` は必須です。検索から来た読者は、正しい場所にいるかを 1 文で知る必要があります。

### Writerside の要素

| 要素 | 用途 |
|---|---|
| `<tldr>` | 冒頭の要約 |
| `<note>` | 危険ではないが役に立つ補足 |
| `<warning>` | 読者の時間を奪う、またはビルドを壊すもの |
| `<procedure>` | `id` 属性を持つ番号付きの手順 |
| `<deflist>` / `<def>` | 用語と説明の一覧 |
| `<code-block lang="ini">` | フェンスで囲んだブロックが使えない、HTML 風の要素の中のコード |

`<tldr>`、`<note>`、`<warning>`、`<def>` の中では、Markdown ではなく HTML（`<b>`、`<code>`、`<a href="Page.md">`、
`<p>`）を使ってください。そこでは Markdown の構文は処理されません。

### 文体

- 先に答えを、次に理由を述べる。逆にはしない。
- 何をするかだけでなく、何にコストがかかるかを書く。
- 既定で使えない機能は、脚注ではなくページの冒頭でそう書く。[RTXDI](RTXDI.md) と [パストレーシング](Path-Tracing.md)
  のページが手本です。
- 列挙できる事実は表に、説明は文章に。表のセルに説明を書かない。

日本語のページでは、英語のページと同じ見出しの構成と ID を保ってください。手順の `id` やアンカーを変えると、両言語の
リンクがずれます。

### 正確さ

主張はエンジンのソースに基づかせてください。コンソール変数の名前、既定値、ヘルプは、記憶に頼らず定義と照らし合わせて
確認します。

```
Engine\Source\Runtime\Renderer\Private\        renderer CVars
Engine\Source\Runtime\Engine\Classes\Engine\Scene.h    post-process settings
Engine\Source\Runtime\Core\Public\Misc\CoreDefines.h   VITE_* compile switches
```

<warning>
エンジンのコンソール変数のヘルプは古いことがあります。HBAO+ はヘルプで自らを DX11 専用と説明していますが、動作する
D3D12 の実装があります。ソースとヘルプが食い違う場合はソースを信頼し、その食い違いを記載してください。
</warning>

## ローカルでビルドする

JetBrains の IDE に Writerside のプラグインを入れるか、Writerside のスタンドアロン版を入れて、リポジトリのルートを開き
ます。インスタンスの ID は `hi`（英語）と `jp`（日本語）です。`jp` をプレビューする前に、ワークフローと同じように
`Writerside\images\` と `Writerside\cfg\vite-theme.html` を `WritersideJP\` にコピーしてください。

Vite Technology のサイトに必要なのは Python 3 だけです。

```
python ViteTech/build.py
```

`ViteTech\public\` に、英語はルートに、日本語は `jp\` の下にプレーンな HTML を書き出します。

Writerside 自身の検査は、壊れたトピックのリンク、参照されていないトピック、欠けた画像を検出します。デプロイの後で気づくより
早く済みます。

## ビルドのパイプライン

`.github\workflows\DocsBuild.yml` は、`main` へのプッシュのたびと、手動での実行時に動きます。Writerside の Docker の
ビルダーで `hi` と `jp` のインスタンスを並行してビルドし、1 つのサイトにまとめます。英語はルートに、日本語は `/jp/` の
下に、Vite Technology のサイトは `/tech/` の下に置かれます。

日本語のビルドが失敗しても英語のデプロイは止まりませんが、英語のビルドが失敗するとデプロイは止まり、古いサイトが公開
されることはありません。ビルドの失敗は通常、ツリーで参照しているトピックが存在しないか、トピックが存在するのに参照されて
いないことが原因です。どちらもワークフローのログに名前で報告されます。

## リリースノート

各リリースのページには、手で書いた要約と、`<!-- BEGIN GENERATED COMMIT RECORD -->` と
`<!-- END GENERATED COMMIT RECORD -->` の間の生成されたコミットの記録があります。記録は、公開リポジトリをリモート `pub`、
社内リポジトリをリモート `int` とするエンジンのクローンから再生成します（August の記録には社内のステージングのコミットが
含まれるため）。ツリーを持たないクローン（`--filter=tree:0`）で十分です。

```
python Tools/ReleaseNotes/generate_release_notes.py --git-dir <path to engine clone>
python Tools/ReleaseNotes/generate_release_notes.py --git-dir <path to engine clone> --locale ja
```

要約は手で編集し、生成されたブロックの中は決して編集しないでください。

## エンジンの変更を文書化する

エンジンの変更が次のいずれかに影響する場合は、同じプルリクエストの中でドキュメントを更新してください。

| 変更 | 更新するページ |
|---|---|
| コンソール変数の追加や変更 | 該当する機能のページ |
| 新しい `VITE_*` スイッチ | [コンパイル時スイッチ](Compile-Time-Switches.md) |
| エンジンの既定値の変更 | [エンジンの既定値の変更](Engine-Defaults.md) |
| プラグインの追加や更新 | [同梱プラグイン](Bundled-Plugins.md) |
| 新しいツールやスクリプト | [ツールと自動化](Tools.md) のセクション |
| 既定のビルドで使えなくなる機能 | その機能のページ。該当する場合は [レイトレーシング](Ray-Tracing.md) も |

## 関連項目

- [コントリビュート](Contributing.md)
- [コーディングガイドライン](Coding-Guidelines.md)
- [コミット規約](Commit-Conventions.md)
