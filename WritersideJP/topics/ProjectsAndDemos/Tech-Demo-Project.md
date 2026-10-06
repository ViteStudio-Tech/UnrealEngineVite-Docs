# テックデモプロジェクト

<tldr>
<p>
Vite の主要なショーケースのパッケージです。動的なグローバルイルミネーション、Apex Destruction、Apex Cloth をカバーする
4 つのシーンを含みます。ビルドが正しく動作するかを確認するための基準のプロジェクトです。
</p>
</tldr>

<img src="TechDemo.png" alt="Unreal Engine Vite で描画したテックデモプロジェクトのシーン" border-effect="line"/>

*テックデモのパッケージは、新しいビルドが正しく描画・シミュレーションできるかを確認するための基準のプロジェクトです。*

## 内容

| シーン | 示すもの |
|---|---|
| NVIDIA DDGI の Cornell Box のオフィスのサンプル | 制御された基準の環境での [動的 DDGI](DDGI-Dynamic.md) |
| PhysX Apex Destruction のテストベッド | [Apex Destruction](Destruction-And-Cloth.md) |
| PhysX Apex Cloth のサンプル | [Apex Cloth](Destruction-And-Cloth.md) |
| 「High End」DDGI + SSGI の Deep Elder Caves | 本番規模のコンテンツでの [DDGI](DDGI-Dynamic.md) と [SSGI](SSGI.md) の組み合わせ |

DDGI を理解するのに役立つのは Cornell Box です。正解が分かっているからこそ標準的なグローバルイルミネーションの基準のシーンになっており、プローブの配置、光漏れ、応答の速さのすべてを、正解と比べて見ることができます。

Deep Elder Caves のシーンはその逆のケースで、DDGI と SSGI を重ねた本番規模のジオメトリです。DDGI が低周波のバウンスを担い、SSGI が DDGI のプローブのグリッドでは解像できない接触スケールのディテールを加えます。両方を一緒に使う理由は
[グローバルイルミネーション](Global-Illumination.md) を参照してください。

## ダウンロード

[テックデモプロジェクト](https://drive.google.com/file/d/1SuHlT4KC3nTQrB2rwVcwBpNgWa_r6yKh/view)

## 検証用のプロジェクトとして使う

Vite の [コントリビュートのガイドライン](Coding-Guidelines.md) は、このプロジェクトを名指ししています。エンジンの変更は、起動時、終了時、そして Tech Showcase のプロジェクトでクラッシュを起こしてはなりません。エンジンを変更する場合は、プルリクエストを出す前にこれを実行してください。

動的 GI、レイトレーシング、PhysX の破壊とクロスという、役に立つ範囲を一通り動かします。それらのどれかを壊す変更は、ここで問題になる傾向があります。

## 要件

動的 DDGI には、DirectX 12 で DXR に対応した GPU が必要です。Apex Destruction と Apex Cloth にはそれぞれのプラグインが必要で、これは Vite が残している標準の 4.27 のプラグインです。[対応プラットフォーム](Platforms.md) と
[動作環境](System-Requirements.md) を参照してください。

## 関連項目

- [動的 DDGI](DDGI-Dynamic.md)
- [グローバルイルミネーション](Global-Illumination.md)
- [破壊とクロス](Destruction-And-Cloth.md)
- [プロジェクトとデモ](ProjectsAndDemos.md)
