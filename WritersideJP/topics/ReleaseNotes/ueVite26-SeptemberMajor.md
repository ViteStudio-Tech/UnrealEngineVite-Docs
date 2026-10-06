# ueVite26 September Major

<tldr>
<p>
最新のメジャーリリースです。September では、コードベースを最新の言語とツールの基盤に移行しました。<b>C++20</b> への初期アップグレード、エンジンの C# プログラム向けの <b>.NET</b> の初期アップグレード、そして Lightmass の
<b>Embree 4.4.1</b> 化です。あわせて、August Major をベースに SSGI と TressFX を改善しています。
</p>
<p>
ブランチ <code>ueVite26-SeptemberMajor-release</code> &middot; ベース:
<a href="ueVite26-AugustMajor.md">ueVite26 August Major</a>
</p>
</tldr>

| 状態 | 開発期間 | ベース | コミット数 |
|---|---|---|---:|
| **最新** | 2026 年 8 月 26 日〜9 月 30 日 | [ueVite26 August Major](ueVite26-AugustMajor.md) | 11 |

## ハイライト

<deflist>
<def title="C++20 の基盤">
C++20 への初期アップグレードにより、コードベースを UE 5.0 が導入した言語モデルに合わせました。C++20 はモジュール単位またはターゲット単位で有効にでき、エンジン本体は引き続き C++17 でビルドされます。エンジンのヘッダーは C++20 の翻訳単位からも正しく解析できるよう保たれているため、エンジンをフォークすることなくプロジェクトのコードで C++20 を採用できます。
</def>
<def title=".NET のアップグレード">
.NET の初期アップグレードにより、エンジンの C# プログラム（ビルドと自動化のツール）を最新の .NET ランタイムに移行しました。Visual Studio 2026 対応から始まったツールチェーンの近代化の続きです。
</def>
<def title="Lightmass の Embree 4.4.1 化">
Lightmass の CPU レイトレーシングが Embree 4.4.1 を使うようになりました。Windows での配置も修正されており、パッケージ化した Lightmass が新しいランタイムを正しく読み込みます。コミュニティからの貢献です。
</def>
<def title="SSGI の高速化">
SSGI が確実に実行され、アンビエントオクルージョンのマスクを置き換える場合は SSAO をスキップするようになりました。推奨構成である <a href="Global-Illumination.md">DDGI と SSGI の併用</a> から冗長なパスが 1 つ減ります。
</def>
</deflist>

## 新機能と変更点

### レンダリング

- **SSGI の性能:** SSGI が確実に実行され、オクルージョン項を提供する場合は SSAO をスキップします。
- **TressFX:** August 系列から引き継いだ統合の更新。[ヘアレンダリング](Hair-Rendering.md) を参照してください。

### ツールチェーンとプラットフォーム

- **C++20:** 初期アップグレード。ターゲットまたはモジュールで `CppStandard = CppStandardVersion.Cpp20` を指定して有効にします。
- **.NET:** エンジンの C# プログラムの初期アップグレード。
- **Lightmass:** Embree 4.4.1 に更新し、Windows での Embree ランタイムの配置を修正。
- **Linux:** Unix のプラットフォームファイル層で発生していた `TScopeLock` の問題を修正（RAII によるロック）。

## アップグレード時の注意点

- このブランチに切り替えたら、`Setup.bat` を実行してプロジェクトファイルを再生成してください。C++20 と .NET の変更はビルドツールに関わります。[ViteSetup](ViteSetup.md) を参照してください。
- C++20 はオプトインです。`CppStandard` を設定しないプロジェクトは引き続き C++17 でビルドされるため、アップグレードにソースの変更は不要です。
- Lightmass を自分でビルドしている場合は、Embree 4.4.1 とリンクされるよう、更新後に再ビルドしてください。

## コミュニティからの貢献

Lightmass の Embree 4.4.1 への更新と、Linux の `TScopeLock` の修正は、コミュニティからのプルリクエスト（#166 と #167）によるものです。貢献を歓迎します。[コントリビュート](Contributing.md) を参照してください。

<!-- BEGIN GENERATED COMMIT RECORD -->

## 全コミット履歴 {id="commit-history"}

ブランチ: [`ueVite26-SeptemberMajor-release`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/tree/ueVite26-SeptemberMajor-release)

### 領域別のコミット数

| 領域 | コミット数 |
|---|---:|
| ツールチェーンとプラットフォーム | 9 |
| レンダリング | 1 |
| ヘア | 1 |

### 公開リリースブランチ — 11 件 {collapsible="true" default-state="collapsed"}

11 件のコミット（マージコミット 5 件は表から除外）。

| 日付 | コミット | 作成者 | 変更内容 |
|---|---|---|---|
| 2026-09-28 | [`3827a62413`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/3827a62413cbdb30c514467669a2028044f5f8fd) | Michael Taulli | Fix Windows Embree 4.4.1 Lightmass deployment |
| 2026-09-28 | [`714417496d`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/714417496df642be8493ce0c7c03bca5b1ffb01a) | Michael Taulli | Fix Windows Embree 4.4.1 Lightmass deploymentclear |
| 2026-09-28 | [`b93b5d402a`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/b93b5d402a1438ace93bf0b3929f94c807053155) | unknown | Restore dotnet files(sorry) |
| 2026-09-28 | [`f364b63345`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/f364b63345f3484af9419b068b21612cefa0a659) | unknown | Remove accidentally committed DotNet setup files |
| 2026-09-28 | [`8eb537d9e5`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8eb537d9e5359a2a585b67a3f2f1107c46127080) | unknown | Remove accidentally committed dotnet binaries |
| 2026-09-28 | [`725a6893d9`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/725a6893d9b37fb5d3818541e4f137531f82d56c) | unknown | Update lightmass to Embree 4.4.1 |
| 2026-09-27 | [`8855719c60`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8855719c60ab2c9c2cd66ca62b25f3b7978e8eea) | unknown | Fix TScopeLock issue on linux |
| 2026-08-30 | [`1115b3e822`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/1115b3e822dc2c6af240e7538cc8d213d107b7a8) | RedPixel | Initial CPP 20 Upgrade |
| 2026-08-30 | [`ec3ebdef2f`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/ec3ebdef2f1138a4549e7abec390111fa462e07d) | RedPixel | Initial NET Upgrade |
| 2026-08-26 | [`940af70a05`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/940af70a0551904442adde2c560a24fe1e3242a9) | RedPixel | \[Rendering\] SSGI Performance improvement |
| 2026-08-26 | [`bacc4aaaa2`](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/bacc4aaaa22eeabcce8189a0e66240105aae673d) | RedPixel | \[Rendering\] TressFX Update |

<!-- END GENERATED COMMIT RECORD -->

## 関連項目

- [すべてのリリースノート](Release-Notes.md)
- [ueVite26 August Major](ueVite26-AugustMajor.md)
- [ツールチェーン要件](Toolchain-Requirements.md)
- [ソースからのビルド](Build-From-Source.md)
