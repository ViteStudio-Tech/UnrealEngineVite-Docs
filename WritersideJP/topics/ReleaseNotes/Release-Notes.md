# リリースノート

<tldr>
<p>
Unreal Engine Vite のすべての公開リリースを、新しい順にまとめています。最新は
<a href="ueVite26-SeptemberMajor.md"><b>ueVite26 September Major</b></a> です。各ページはハイライトとアップグレード時の注意点から始まり、最後にリリースブランチの全コミット履歴を掲載しています。
</p>
</tldr>

## リリース一覧

| リリース | 種別 | 開発期間 | 主な変更点 | コミット数 |
|---|---|---|---|---:|
| [ueVite26 September Major](ueVite26-SeptemberMajor.md) | **最新** | 2026 年 8〜9 月 | C++20 と .NET のアップグレード、Lightmass の Embree 4.4.1 化、SSGI の高速化 | 11 |
| [ueVite26 August Major](ueVite26-AugustMajor.md) | メジャー | 2026 年 7〜8 月 | UE5 からのエディタ・メモリ関連バックポート、RT 反射、スペキュラーオクルージョン、GAS、XeSS 3.1、macOS 移植 | 438 |
| [ueVite26 July Major](ueVite26-JulyMajor.md) | メジャー | 2026 年 7〜8 月 | ゲーティングによる 12.3% の FPS 向上、Blast SDK の更新、UE5 プラグインのバックポート、ViteSetup | 78 |
| [ueVite26 June Major](ueVite26-JuneMajor.md) | メジャー | 2026 年 3〜7 月 | FSR 4、DLSS 4、XeSS 3、フレーム生成、HBAO+、アニメーションのバックポート、固定タイムステップの PhysX | 170 |
| [ueVite26 March Major](ueVite26-MarchMajor.md) | メジャー | 2025 年 12 月〜2026 年 3 月 | トゥーンシェーディング、コンピュート SMAA、ローカライズド IBL、ネイティブ PhysX アクター、NDK 29 | 79 |
| [ueVite25 LTS](ueVite25-LTS.md) | **LTS** | 2025 年 11〜12 月 | NvRTX Caustics 4.27 ベース、パフォーマンス重視の既定値、VS 2026 | 174 |
| [初代 Vite](Original-Vite.md) | アーカイブ | 2025 年 11 月以前 | NvRTX 5.0（UE5）系列。LTS に置き換え | &mdash; |

## リリースの系列

<deflist>
<def title="LTS">
<code>ueVite25-LTS</code> は、すべてのメジャーリリースの土台となる長期サポートのベースです。NvRTX Caustics 4.27 と
Epic の 4.27-plus をマージし、Vite の既定値の変更を加えています。最も保守的なブランチが必要な場合に選んでください。
</def>
<def title="メジャーリリース">
<code>ueVite26-&lt;Month&gt;Major-release</code> の各ブランチです。それぞれが前のリリースの上に構築されるため、複数のメジャーリリースをまたいでアップグレードする場合は、その間のすべてのページを読んでください。メジャーブランチはリリース後も修正を受け続けており、各ページの「リリース後のメンテナンス」に記載しています。
</def>
<def title="最新">
最も新しいメジャーリリースです。LTS が必要な場合を除き、新規プロジェクトはここから始めてください。
</def>
</deflist>

## リリースページの読み方

各ページは同じ構成になっています。

1. **概要とリリース情報** &mdash; ブランチ、開発期間、ベースとなるリリース、コミット数。
2. **ハイライト** &mdash; 多くのチームが気付く変更点。
3. **新機能と変更点** &mdash; レンダリング、レイトレーシング、アップスケーリング、物理、アニメーション、ツール、プラットフォームなどの領域別。
4. **アップグレード時の注意点** &mdash; プロジェクトの挙動を変えうる既定値の変更や要件。
5. **全コミット履歴** &mdash; リリースブランチから生成し、領域別に集計したうえで、既定では折りたたんで表示します。マージコミットは表から除外しています。

## ソースの所在

すべてのリリースブランチは
[Unreal Engine Vite リポジトリ](https://github.com/GapingPixel/UnrealEngineVite-PhysX) で公開しています。

<note>
<p>
すべての Unreal Engine ソースのフォークと同様に、このリポジトリは Epic Games と連携した GitHub アカウントにしか表示されません。ブランチやコミットのリンクが <i>404</i> になる場合は、Epic Games のアカウント設定で GitHub アカウントを連携し、EpicGames 組織への招待を承認してください。
</p>
</note>

August Major は内部のステージングブランチで開発され、1 つのリリースコミットとして公開されました。そのため、同ページではステージングのコミットをリンクなしで掲載しています。それ以外はすべて公開コミットに直接リンクしています。

## 関連リソース

- [バックポート](Backporting.md)
- [コミット規約](Commit-Conventions.md)
- [ツールチェーン要件](Toolchain-Requirements.md)
- [エンジン概要](Engine-Overview.md)
