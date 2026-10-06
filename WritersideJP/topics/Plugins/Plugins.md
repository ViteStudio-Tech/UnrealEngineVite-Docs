# プラグイン

<tldr>
<p>
Vite は、ベンダーの技術（NVIDIA、AMD、Intel）、バックポートした UE5 のプラグイン、サードパーティの追加機能を、エンジンのツリーに直接同梱しています。その多くは <code>Engine\Plugins\Runtime\VitePlugins</code> にあります。
</p>
</tldr>

標準の UE 4.27 には大量のプラグインが含まれており、Vite はその大部分を残しています。そのうえで Vite は、4.27 向けには上流に存在しないもの、UE5 向けにしか存在しないもの、通常は手作業で統合する必要があるベンダーの SDK を同梱しています。

## このセクションの内容

| トピック | 内容 |
|---|---|
| [同梱プラグイン](Bundled-Plugins.md) | Vite が標準の 4.27 に追加したすべてのもの。バージョンと既定の有効状態つき |
| [提案中のプラグイン](Proposed-Plugins.md) | 統合の候補と、推奨する外部のプラグイン |

## プラグインの場所

| ディレクトリ | 内容 |
|---|---|
| `Engine\Plugins\Runtime\VitePlugins` | Vite 独自の追加: FSR 4、XeSS、ACL、ImGui、Motion Symphony、Kawaii Physics、PhysX Instanced Subsystem など |
| `Engine\Plugins\Runtime\Nvidia` | DLSS、Streamline、NIS、NRD、RTXGI、DeepDVC、Reflex、Ansel |
| `Engine\Plugins\Runtime\TressFX` | AMD TressFX 5.0 のヘア |
| `Engine\Plugins\GameWorks\Blast` | NVIDIA Blast の破壊のランタイム |
| `Engine\Plugins\Experimental\BlastPlugin` | Blast の作成ツール |
| その他すべて | 標準の 4.27 のプラグイン |

[ViteSetup](ViteSetup.md) の Express の経路でセットアップした場合、`VitePlugins` には ACL と MotionSymphony だけが残り、それ以外はエンジンのフォルダーの隣の `ViteDebloat_Moved` にあり、いつでもコピーして戻せます。

## プラグインを有効にする

同梱プラグインの多くは `EnabledByDefault` が `false` の状態で出荷されるため、必要とするまでコストはかかりません。プロジェクトごとに有効にしてください。

<procedure title="同梱プラグインを有効にする" id="enable-plugin">
    <step>エディタで <b>編集 &gt; プラグイン</b> を開きます。</step>
    <step>プラグインを探して <b>Enabled</b> にチェックを入れます。</step>
    <step>求められたらエディタを再起動します。</step>
</procedure>

または `.uproject` に直接追加します。

```json
{
  "Plugins": [
    {
      "Name": "DLSS",
      "Enabled": true
    }
  ]
}
```

<note>
プラグインを有効にすると、そのシェーダーのパーミュテーション、モジュール、起動時のコストがすべてのビルドに加わります。使うものだけを有効にし、残りはオフのままにしてください。<a href="Shader-Compilation-And-PSO.md">シェーダーコンパイルと PSO</a>
を参照してください。
</note>

## プラグインとデブロート

[デブロートのスイート](Debloat-Guide.md) は、`ExcludedPlugins.txt` を使ってエンジンのツリーからプラグインを取り除けます。この一覧は積極的で、多くのプロジェクトが本当に必要とするプラグインも含まれています。`GameplayAbilities`、`ApexDestruction`、`HairStrands`、NVIDIA のプラグインなどです。

<warning>
プラグインを取り除く前に <code>ExcludedPlugins.txt</code> を読んでください。プロジェクトが依存しているプラグインを取り除くと、きれいには失敗しません。それを参照しているアセットが読み込めなくなります。
</warning>

同じ一覧は、`LocalBuilds\CompressBuildSeparate.bat` がプラグインを別のアーカイブに分割する際にも使われます。こちらは破壊的ではない代替手段です。[インストール済みビルド](Installed-Builds.md) を参照してください。

## 独自のプラグインを追加する

プロジェクトのプラグインは、標準の Unreal と同じく `<Project>\Plugins` に置きます。チーム全員が持つべきエンジンのプラグインは `Engine\Plugins\Runtime\VitePlugins` に置き、エンジンの再ビルドと再配布が必要です。

プラグインを Vite に同梱してほしい場合は、4.21&ndash;4.27 と互換である必要があります。UE5 専用のプラグインは対象外です。基準と現在の候補の一覧は [提案中のプラグイン](Proposed-Plugins.md) を参照してください。

## 関連項目

- [同梱プラグイン](Bundled-Plugins.md)
- [提案中のプラグイン](Proposed-Plugins.md)
- [デブロートガイド](Debloat-Guide.md)
- [アップスケーラー](Upscalers.md)
