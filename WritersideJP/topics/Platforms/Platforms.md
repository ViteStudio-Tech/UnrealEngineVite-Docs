# 対応プラットフォーム

<tldr>
<p>
Vite の主な対象は DirectX 12 の 64 ビット Windows で、すべての機能がそこでビルドされ、計測されます。Android と Linux には対象を絞った修正が入り、その他のプラットフォームは標準の 4.27 の対応を引き継ぎます。コンソールの作業は非公開です。
</p>
</tldr>

Vite は目的を絞ったフォークです。Vite を特徴づける機能（NvRTX のレイトレーシング一式、DDGI、RTXDI、DLSS とその代替、HBAO+、ハードウェアテッセレーション）は、デスクトップ PC と現世代のコンソールを対象とした、ディファードレンダラーの
GPU 機能です。Windows 以外のプラットフォームの作業は、そこでプロジェクトを出荷し続けるために必要なもの、つまりツールチェーン、コンパイルの修正、フォワード（モバイル）レンダラーに集中しています。

## 対応レベル

| プラットフォーム | レベル | 備考 |
|---|---|---|
| Windows 64 ビット | **主要** | すべてのビルドと計測の基準 |
| Windows 32 ビット | サポートファイルのみ | Win64 のツールが必要とするもので、出荷の対象ではない |
| Android | 保守対象 | C++20 の修正を伴う Android NDK 29、arm32 の修正、エディタでの Android Vulkan のプレビュー（[March Major](ueVite26-MarchMajor.md)）。Meta Quest のデバイスプロファイルとパッケージ化の修正（[LTS](ueVite25-LTS.md)）。NEON の演算の改良（[June Major](ueVite26-JuneMajor.md)） |
| Linux | サーバー向けに保守 | サーバーのツールチェーンの修正（March）、専用サーバーのプラグインの更新（[August Major](ueVite26-AugustMajor.md)）、Unix のファイル層のロックの修正（[September Major](ueVite26-SeptemberMajor.md)）。レイトレーシング一式は未テスト |
| Mac | 継承 | 標準の 4.27 の対応。DXR がないため、レイトレーシング一式は対象外 |
| iOS / tvOS | 継承 | 標準の 4.27 の対応と、共通のフォワードレンダラーの変更 |
| HTML5 | 利用不可 | Epic は 4.24 で HTML5 をエンジンから切り離し、コミュニティが保守する拡張に移しました。この名前は、セットアップのスクリプトで依存関係を絞り込む条件としてだけ残っています。 |
| コンソール | 非公開 | コンソールの SDK は NDA の対象であり、コンソール固有の変更はこのリポジトリで公開できません |

「継承」とは、標準の 4.27 のコードが存在し、意図的に壊されてはいないものの、Vite がテストしておらず、フォークのレンダリング機能が使えないか未検証であることを意味します。「保守対象」とは、レンダリング機能一式を約束するものではないものの、Vite がそのプラットフォームのツールチェーンとビルドを修正・更新していることを意味します。

## 他のプラットフォームを有効にする

プラットフォームの依存関係は、セットアップ時に選んで追加します。

[ViteSetup](ViteSetup.md) では、Express の経路のプラットフォームの選択画面でチェックを入れるか、Custom の経路で
**Win64 + Android** または **Win64 + Linux** のプロファイルを選ぶか、step-by-step assistant でプラットフォームを個別に切り替えます。**Full setup** は `Setup.bat` に `-exclude` 引数を渡さず、すべてをダウンロードします。

デブロートのスクリプトでは、`devops\config.txt` の該当する行のコメントを外します。

```ini
# Win64 is always kept. Uncomment a platform to ALSO download and keep
# its dependencies during setup.
#KEEP_PLATFORM=Android
#KEEP_PLATFORM=IOS
#KEEP_PLATFORM=Linux
#KEEP_PLATFORM=Mac
```

<warning>
後からプラットフォームを追加するには、依存関係のセットアップの再実行と再ビルドが必要です。できれば最初のビルドの前に決めてください。
</warning>

## グラフィックス API

| API | 状況 | 備考 |
|---|---|---|
| DirectX 12 | **主要** | DXR に必要で、したがってレイトレーシングのすべてに必要 |
| DirectX 11 | 対応 | ラスターの機能は動作し、レイトレーシングは動作しない |
| Vulkan | 継承 | 標準の 4.27 の対応に、Vite の安定性の修正（August Major）を加えたもの。Vite のレイトレーシング一式は DXR ベース |
| Metal | 継承 | Mac と iOS |
| OpenGL ES / モバイルの Vulkan | 保守対象 | Android |

### DX12 が必要なもの

レイトレーシングはすべて DXR を必要とし、Vite ではそれは DirectX 12 を意味します。

- [レイトレーシング反射](RT-Reflections.md)、シャドウ、アンビエントオクルージョン、スカイライト
- [動的 DDGI](DDGI-Dynamic.md)
- ピクセルごとのレイトレーシング GI、[RTXDI](RTXDI.md)、[パストレーシング](Path-Tracing.md)、[半透明とコースティクス](RT-Translucency-And-Caustics.md)（`VITE_RT_PSO_DEBLOAT=0` で再ビルドした場合）

[FSR 4](Upscalers.md) も、レイトレーシングとは無関係に DX12 専用です。

### DX11 で動作するもの

- [HBAO+](Ambient-Occlusion.md)。コンソール変数のヘルプの記述に反して、June Major 以降は D3D12 のバックエンドもあります
- [SMAA](Anti-Aliasing.md)
- [SSGI](SSGI.md)
- [ハードウェアテッセレーション](Tessellation.md)
- [Callisto BRDF と Toon のシェーディングモデル](Shading-Models.md)（コンパイルに含めた場合）

レイトレーシングを諦めてよいなら、DX11 を対象にすることも十分に可能です。[パフォーマンス目標](Performance-Targets.md)
に DXR の予算の余地がないプロジェクトには、それが適した選択です。

## ハードウェア

開発用と実行用のハードウェアについては [動作環境](System-Requirements.md) を参照してください。

PS5 クラスの CPU の作業、とりわけ PhysX 3.4 の近代化は、Series X より FPU がさらに削減された Zen 2（`FP3` がなく、`FP2` はストア専用、FMA パイプは 1 本）を持つ AMD 4700S で計測します。GPU のコンパイラの確認にはディスクリートの RX 6700 を使います。4700S と 4800S の GPU は無効化されており、BC-250 には使える Windows の D3D12 のドライバーがないためです。詳しくは
[PS5 CPU の FPU](PS5-CPU-FPU.md) を参照してください。

## パッケージ化

[インストール済みビルド](Installed-Builds.md) は、Win64 向けに Development と Shipping のゲーム構成で作成されます。ViteSetup では、チェックを入れれば Linux も追加されます。他の構成やプラットフォームが必要な場合は、`RunUAT.bat` の
BuildGraph の引数を編集してください。

```
-set:WithLinux=true
-set:GameConfigurations=Development;Test;Shipping
```

プラットフォームや構成を追加するごとに、もともと長いビルドがさらに大幅に長くなります。

## 関連項目

- [動作環境](System-Requirements.md)
- [インストール済みビルド](Installed-Builds.md)
- [ViteSetup](ViteSetup.md)
- [レイトレーシング](Ray-Tracing.md)
- [デブロートガイド](Debloat-Guide.md)
