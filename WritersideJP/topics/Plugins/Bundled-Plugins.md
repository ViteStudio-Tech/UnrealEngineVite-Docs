# 同梱プラグイン

<tldr>
<p>
Vite が標準の UE 4.27 に追加したすべてのものを、バージョンと既定の有効状態とともに示します。標準の 4.27 のプラグインは載せず、Vite の追加とベンダーの統合だけを扱います。既定で有効なのは RTXGI、ACL、カスタムのスプラッシュ画面の 3 つです。
</p>
</tldr>

バージョンと既定値は、[September Major](ueVite26-SeptemberMajor.md) のリリースの `.uplugin` ファイルから読み取ったものです。正確な値は、手元のツリーの `.uplugin` ファイルで確認してください。**オフ** は、プロジェクトが有効にするまでエンジンがプラグインを読み込まないことを意味します。記述子で `EnabledByDefault` が指定されていないプラグインも含まれ、Unreal はエンジンのプラグインではそれをオフとして扱います。

<img src="VitePlugins.png" alt="エクスプローラーで表示した Engine/Plugins/Runtime/VitePlugins の中身" border-effect="line"/>

*Vite 独自の追加は `Engine\Plugins\Runtime\VitePlugins` にあります。NVIDIA のベンダー統合は別に
`Engine\Plugins\Runtime\Nvidia` にあります。*

<warning>
<p>
<a href="ViteSetup.md">ViteSetup</a> の Express の経路は、<code>Runtime\VitePlugins</code> 以下のプラグインを ACL と
MotionSymphony を除いてすべて <code>ViteDebloat_Moved</code> に移動します。このフォルダーのプラグインがツリーにない場合、通常はそれが理由です。<a href="Debloat-Guide.md">デブロートガイド</a> を参照してください。
</p>
</warning>

## アップスケーリングとフレーム生成

| プラグイン | バージョン | 既定 | パス |
|---|---|---|---|
| NVIDIA DLSS Super Resolution / Ray Reconstruction / DLAA | 8.7.0（NGX 310.7.0） | オフ | `Runtime\Nvidia\DLSS` |
| NVIDIA DLSS Frame Generation | 1.3.0（Streamline SDK 2.12.0） | オフ | `Runtime\Nvidia\Streamline` |
| NVIDIA NIS | 1.2.1 | オフ | `Runtime\Nvidia\NIS` |
| NVIDIA RTX Dynamic Vibrance（DeepDVC） | 1.3.0（Streamline） | オフ | `Runtime\Nvidia\StreamlineDeepDVC` |
| NVIDIA Reflex | 1.6 | オフ | `Runtime\Nvidia\Reflex` |
| Movie Render Queue DLSS/DLAA Support | 2.3.3 | オフ | `Runtime\Nvidia\DLSSMoviePipelineSupport` |
| AMD FSR 4 | 4.1.1 | オフ | `Runtime\VitePlugins\FSR4-427\FSR4` |
| AMD Anti-Lag 2 | 2.0.4 | オフ | `Runtime\VitePlugins\AntiLag2.0.4` |
| Intel XeSS | 3.1.0 | オフ | `Runtime\VitePlugins\XeSS_UE4.27_Plugin_v3.1.0` |

FSR 4 はネイティブの ffx-api を使い、DX12 専用です。Vite のために 4.27 へバックポートされました。以前の FSR 2 のプラグインは `Runtime\VitePlugins\FSR2-427` に残っていますが、記述子が `.uplugin.disabled` に名前を変えてあるため、読み込まれることはありません。詳しくは [アップスケーラー](Upscalers.md) を参照してください。

## レイトレーシングとレンダリング

| プラグイン | バージョン | 既定 | パス |
|---|---|---|---|
| NVIDIA RTX Global Illumination（RTXGI） | 1.1.50 | **オン** | `Runtime\Nvidia\RTXGI` |
| NVIDIA Real-Time Denoiser（NRD/ReLAX） | 2.10.00-relax | オフ | `Runtime\Nvidia\NRD` |
| NVIDIA Ansel | 4251 | オフ | `Runtime\Nvidia\Ansel` |
| Graphics Card Info Utilities | 1.0 | オフ | `Runtime\Nvidia\GraphicsCardInfoUtils` |

RTXGI は、Vite が推奨する動的 GI である DDGI の実装を提供するため、既定で有効です。NRD/ReLAX はレイトレーシングの出力のノイズを除去します。それに依存するレイトレーシングのエフェクトを使う場合に有効にしてください。[グローバルイルミネーション](Global-Illumination.md) と [動的 DDGI](DDGI-Dynamic.md) を参照してください。

## ヘア

| プラグイン | バージョン | 既定 | パス |
|---|---|---|---|
| TressFX 5.0 | 5.0 | オフ | `Runtime\TressFX` |
| Groom（HairStrands） | 1.0 | オフ | `Runtime\HairStrands` |

作成のパイプラインが異なる、独立した 2 つのヘアシステムです。TressFX には、エンジンを `VITE_TRESSFX=1` でビルドすることも必要です。[ヘアレンダリング](Hair-Rendering.md) を参照してください。

## 物理と破壊

| プラグイン | バージョン | 既定 | パス |
|---|---|---|---|
| Blast（ランタイム） | 1.0 | オフ | `GameWorks\Blast` |
| Blast Plugin（作成） | 0.1 | オフ | `Experimental\BlastPlugin` |
| PhysX Instanced Subsystem | 1.11 | オフ | `Runtime\VitePlugins\PhysXInstancedSubsystem` |
| Kawaii Physics | 1.18.0 | オフ | `Runtime\VitePlugins\KawaiiPhysics` |

Apex Destruction、Apex Cloth、PhysX Vehicles は、Vite が残している標準の 4.27 のプラグインです。UE5 では Chaos が PhysX を置き換えた際に取り除かれました。`ueVite-ApplyVitePluginDefaults.bat` で適用する Vite のプラグインプロファイルは、Blast の作成用プラグインを有効にします。[エンジンの既定値の変更](Engine-Defaults.md#disabled-plugins) と
[破壊とクロス](Destruction-And-Cloth.md) を参照してください。

Kawaii Physics は、Vite にバックポートした UE5 の二次モーション用のボーンソルバーです。1 つのアニメーションノードで、髪、布、アクセサリーに物理的な追従の動きを与え、完全なクロスシミュレーションよりはるかに安価です。

PhysX Instanced Subsystem は、ワールドサブシステムを通じて大量の PhysX ベースのインスタンス化ボディを管理し、個々のアクターを生成するのではなく、ISM/HISM のインスタンスのトランスフォームにポーズを書き戻します。[インスタンス化物理](Instanced-Physics.md) を参照してください。

## アニメーション

| プラグイン | バージョン | 既定 | パス |
|---|---|---|---|
| Animation Compression Library（ACL） | 2.1.0 | **オン** | `Runtime\VitePlugins\ACLPlugin` |
| Motion Symphony | 1.09 | オフ | `Runtime\VitePlugins\MotionSymphony` |

ACL は、Unreal に組み込みのアニメーション圧縮を、サイズと品質の関係がはるかに優れたものに置き換えます。大量のアニメーションを持つプロジェクトではメモリの節約が大きく、最も安価に得られる改善の 1 つです。[パフォーマンス目標](Performance-Targets.md) を参照してください。

Motion Symphony は、Ubisoft 方式のアニメーション合成の手法であるモーションマッチングとポーズマッチングを提供します。UE5 の Motion Matching に最も近い 4.27 の機能です。[ドキュメント](https://www.wikiful.com/@AnimationUprising/motion-symphony/motion-matching) ·
[サンプルプロジェクト](https://github.com/Animation-Uprising/MotionSymphony_ExampleProject/tree/main)

## ゲームプレイ

| プラグイン | バージョン | 既定 | パス |
|---|---|---|---|
| Abilities（SplashAbilities） | 1.1 | オフ | `Runtime\VitePlugins\SplashAbilities` |

Abilities は、GAS の複雑さやレプリケーションのモデルを持ち込まずにアビリティシステムが欲しいプロジェクト向けの、`GameplayAbilities` より軽い代替です。

<note>
<p>
Flecs ECS の統合（ワールドサブシステム、ブループリントのエンティティハンドル、ISM による描画のデモ、任意の Flecs Explorer
対応）は社内のブランチで開発中で、まだどの公開リリースにも含まれていません。
<a href="Proposed-Plugins.md">提案中のプラグイン</a> を参照してください。
</p>
</note>

## デバッグとプロファイリング

| プラグイン | バージョン | 既定 | パス |
|---|---|---|---|
| Dear ImGui | 0.1.0 | オフ | `Runtime\VitePlugins\UnrealImGui` |
| ImGui Tools | 1.0 | オフ | `Runtime\VitePlugins\ImGuiTools` |
| Intel GPA | 1.0 | オフ | `Runtime\VitePlugins\GPAPlugin` |
| Automatron | 1.1a | オフ | `Runtime\VitePlugins\Automatron` |

ImGui は、ビューポートでもスタンドアロンのビルドでも動作するイミディエイトモードのデバッグ UI を提供します。そうした場面では Slate のデバッグウィジェットは扱いにくいものです。ImGui Tools は、その上に実用的な開発用ツールを構築します。

GPA プラグインは Intel Graphics Performance Analyzers をエディタに統合します。Automatron は C++ とブループリントの自動テストを改善します。[プロファイリング](Profiling.md) を参照してください。

## コンテンツとユーティリティ

| プラグイン | バージョン | 既定 | パス |
|---|---|---|---|
| Custom Splash Preload Screen | 1.0 | **オン** | `Runtime\PostSplashScreen` |
| Impostor Baker | 1.0 | オフ | `Experimental\ImpostorBaker` |
| Shallow Water | 1.0 | オフ | `Experimental\ShallowWater` |

スプラッシュ画面のプラグインは、エンジンの事前初期化中にシステムのスプラッシュの後でカスタムの画面を表示し、最初のフレームまでの空白を埋めます。

Impostor Baker は、遠景のメッシュの LOD として使うインポスターを生成します。遠くの大量の木や小物を安価に描画するための標準的な手法で、払えないドローコールのコストを受け入れる前に検討する価値があります。

## 既定の有効状態のまとめ

既定で有効な同梱プラグインは 3 つです。

| プラグイン | 理由 |
|---|---|
| RTXGI | Vite が推奨する動的 GI である DDGI を提供する |
| ACL | 実行時のコストなしに、すべてのプロジェクトでアニメーションの圧縮を改善する |
| Custom Splash Preload Screen | 見た目のためのもので、コストはごくわずか |

それ以外はすべて任意で有効にするものです。機能が動作していないように見える場合は、さらにデバッグする前にプラグインが有効になっているかを確認してください。レイトレーシングの機能については、[コンパイル時スイッチの利用可否の表](Ray-Tracing.md) も確認してください。

## 関連項目

- [プラグイン](Plugins.md)
- [提案中のプラグイン](Proposed-Plugins.md)
- [アップスケーラー](Upscalers.md)
- [ヘアレンダリング](Hair-Rendering.md)
- [インスタンス化物理](Instanced-Physics.md)
- [デブロートガイド](Debloat-Guide.md)
