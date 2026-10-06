# リファレンス

<tldr>
<p>
調べるための資料です。コンソール変数、用語、よくある質問をまとめています。探しているものが分かっている場合はここを、分からない場合は各機能のセクションを使ってください。
</p>
</tldr>

## このセクションの内容

| トピック | 内容 |
|---|---|
| [ライセンスと著作権](License-And-Copyright.md) | Unreal Engine の EULA と Vite Studio の著作権 |
| [コンソール変数](Console-Variables.md) | Vite 固有のものと、よく必要になるコンソール変数。サブシステムごとに整理 |
| [コンパイル時スイッチ](Compile-Time-Switches.md) | `VITE_*` のビルドスイッチと、それが変えるもの |
| [用語集](Glossary.md) | このドキュメント全体で使う用語 |
| [よくある質問](FAQ.md) | 繰り返し寄せられる質問 |

## すぐに分かる答え

<deflist>
<def title="設定したコンソール変数が何もしない">
最も可能性が高いのは、機能がコンパイル対象から外れていることです。<code>VITE_RT_PSO_DEBLOAT</code> は既定で
<code>1</code> で、RTXDI、パストレーシング、レイトレーシングの半透明、コースティクス、ピクセルごとのレイトレーシング GI のシェーダーのパーミュテーションを取り除きます。変数の設定はできますが、何も描画されません。
<a href="Compile-Time-Switches.md">コンパイル時スイッチ</a> を参照してください。
</def>
<def title="エディタに機能が見当たらない">
そのプラグインが有効になっているかを確認してください。同梱プラグインの多くは既定でオフです。
<a href="Bundled-Plugins.md">同梱プラグイン</a> を参照してください。
</def>
<def title="クローンしたばかりでビルドが失敗する">
通常はツールチェーンの不一致か、.NET Framework 4.5 のリファレンスアセンブリの欠落です。
<a href="Build-Troubleshooting.md">ビルドのトラブルシューティング</a> を参照してください。
</def>
<def title="変更が反映されていないかのようにシェーダーが振る舞う">
古いキャッシュです。<a href="Cache-Management.md">キャッシュ管理</a> を参照してください。
</def>
</deflist>

## 関連項目

- [はじめに](Getting-Started.md)
- [パフォーマンスと最適化](Performance.md)
- [コントリビュート](Contributing.md)
- [ライセンスと著作権](License-And-Copyright.md)
