# 用語集

<tldr>
<p>
このドキュメント全体で使う用語です。Vite 固有の用語はその旨を示しています。それ以外は、このドキュメントが前提とする
標準的な Unreal やグラフィックスの用語です。
</p>
</tldr>

## Vite とフォークの用語

<deflist>
<def title="Vite">
このエンジン。NVIDIA の NvRTX のブランチをベースにした Unreal Engine 4.27 のフォークで、性能と、上流の 4.27 には含まれない
レンダリング技術に重点を置いています。エンジン関連付けの識別子は <code>UE_ViteFork</code>。Unreal Engine 4.27 として
ライセンスされ、Vite 独自の作業の著作権は Vite Studio にあります。<a href="License-And-Copyright.md">ライセンスと著作権</a>
を参照してください。
</def>
<def title="NvRTX">
上流に先行して NVIDIA のレイトレーシング技術を取り込んだ、NVIDIA の公開 Unreal Engine のブランチ。Vite は
<b>NvRTX 4.27 Caustics</b> と <b>NvRTX 5.0</b> から取り入れています。
</def>
<def title="VITE_* スイッチ">
機能をそもそもエンジンにビルドするかどうかを制御する、コンパイル時のプリプロセッサのスイッチ。
<code>Engine\Source\Runtime\Core\Public\Misc\CoreDefines.h</code> で定義されています。変更にはエンジンの再ビルドが必要です。
<a href="Compile-Time-Switches.md">コンパイル時スイッチ</a> を参照してください。
</def>
<def title="コンパイル対象外">
コンパイル時のスイッチによって、シェーダーのパーミュテーションとコードパスがビルドから除外された機能。そのコンソール
変数は存在し、設定にも成功しますが、何も描画されません。Vite で「この設定が何もしない」の最もよくある原因です。
</def>
<def title="デブロート">
ディスク容量を減らすために、使わないプラットフォームのバイナリ、テンプレート、サンプル、プラグインをエンジンのツリーから
取り除く作業。<a href="Debloat-Guide.md">デブロートガイド</a> を参照してください。
</def>
<def title="インストール済みビルド">
ランチャーでインストールしたものと同じように動作する、ビルド済みで再配布可能なエンジン。エンジンの C++ はコンパイル
できません。<a href="Installed-Builds.md">インストール済みビルド</a> を参照してください。
</def>
</deflist>

## レンダリング

<deflist>
<def title="DDGI">
Dynamic Diffuse Global Illumination。RTXGI のプラグインが提供する、NVIDIA のプローブベースの GI の手法。プローブが放射照度と
深度を保持し、サーフェスは周囲のプローブから間接光をサンプリングします。Vite が推奨する動的 GI です。
<a href="DDGI-Dynamic.md">動的 DDGI</a> を参照してください。
</def>
<def title="SSGI">
Screen Space Global Illumination。描画されたフレームから間接光を導きます。安価で細かいものの、画面に映っているものに
限られます。単独で使うより、DDGI の下に重ねるのが普通です。<a href="SSGI.md">SSGI</a> を参照してください。
</def>
<def title="RTXDI">
RTX Direct Illumination。リザーバーの再サンプリングを使った、非常に多くのライトを持つシーン向けのレイトレーシングの
直接光。Vite にあるのは単体の版で、UE 5.1 以降の Lumen に統合された版ではありません。既定ではコンパイル対象外です。
<a href="RTXDI.md">RTXDI</a> を参照してください。
</def>
<def title="ReSTIR / リザーバーの再サンプリング">
RTXDI を支えるサンプリングの手法。各ピクセルがライトのサンプルのリザーバーを持ち、それを空間と時間の方向に洗練していく
ことで、少ない数のレイで、はるかに大きなライトの集合を近似します。
</def>
<def title="パストレーシング">
光の伝搬の完全なシミュレーション。リファレンスの品質であり、実行時の目標ではありません。既定ではコンパイル対象外です。
<a href="Path-Tracing.md">パストレーシング</a> を参照してください。
</def>
<def title="DXR">
DirectX Raytracing。Vite のレイトレーシングのすべての機能を支える API であり、それらがすべて DirectX 12 を必要とする理由
です。
</def>
<def title="PSO">
Pipeline State Object。シェーダーと固定機能のステートをコンパイルしてまとめたもの。レイトレーシングの PSO は大きく、
構築に時間がかかります。それを減らすために存在するのが <code>VITE_RT_PSO_DEBLOAT</code> です。
<a href="Shader-Compilation-And-PSO.md">シェーダーコンパイルと PSO</a> を参照してください。
</def>
<def title="シェーダーのパーミュテーション">
特定の機能の組み合わせに対してコンパイルされた、シェーダーの 1 つの派生。パーミュテーションの数は掛け算で増え、
シェーディングモデル、任意の機能、品質レベルのそれぞれが集合を広げます。シェーダーのコンパイル時間とパッケージのサイズを
左右する最大の要因です。
</def>
<def title="コースティクス">
透明なサーフェスやスペキュラーのサーフェスでの屈折や反射によって集められた光。Vite には NvRTX Caustics のブランチから
来たメッシュのコースティクスと水のコースティクスの両方があります。既定ではコンパイル対象外です。
<a href="RT-Translucency-And-Caustics.md">レイトレーシング半透明とコースティクス</a> を参照してください。
</def>
<def title="Callisto BRDF">
キャラクターと肌のための Vite 固有のシェーディングモデル。標準のマテリアルのピンを流用して、再帰反射、ディフューズの
フレネル、ターミネーターの平滑化を公開します。<a href="Shading-Models.md">シェーディングモデル</a> を参照してください。
</def>
<def title="シャドウターミネーター">
曲面上で光が当たっている領域と当たっていない領域の境界。その硬さは、リアルタイムレンダリングであることが最もよく分かる
特徴の 1 つで、Callisto BRDF はそれを直接制御できます。
</def>
<def title="SMAA">
Subpixel Morphological Anti-Aliasing。Vite が推奨するアンチエイリアシングの手法。時間的ではなく空間的な手法なので、
TAA のようなゴーストやにじみを生みません。<a href="Anti-Aliasing.md">アンチエイリアシング</a> を参照してください。
</def>
<def title="TAA">
Temporal Anti-Aliasing。Unreal の既定。フレームをまたいでサンプルを蓄積します。効果的ですが、動きの中でゴースト、にじみ、
ぼやけが生じます。
</def>
<def title="HBAO+">
NVIDIA の Horizon-Based Ambient Occlusion。標準の SSAO より高品質で、スクリーンスペースの AO のバッファに乗算します。
ヘルプの記述に反して、DX11 と D3D12 の両方で動作します。<a href="Ambient-Occlusion.md">アンビエントオクルージョン</a>
を参照してください。
</def>
<def title="テッセレーション">
GPU 上でのハードウェアによる三角形の分割で、ディスプレイスメントを駆動します。UE5 では Nanite のために取り除かれ、
Vite では残っています。<a href="Tessellation.md">テッセレーション</a> を参照してください。
</def>
<def title="TressFX">
AMD のストランドベースのヘアの描画とシミュレーションのシステム。バージョン 5.0 を同梱しています。Unreal の Groom の
代わりになるものです。<a href="Hair-Rendering.md">ヘアレンダリング</a> を参照してください。
</def>
<def title="NRD / ReLAX">
NVIDIA Real-Time Denoiser。サンプル数の少ないレイトレーシングに付きもののノイズを取り除きます。プラグインは既定でオフ
なので、それを使うレイトレーシングのエフェクトとともに有効にしてください。
</def>
</deflist>

## アップスケーリング

<deflist>
<def title="DLSS">
NVIDIA Deep Learning Super Sampling。低い解像度で描画し、AI のモデルで再構築します。NVIDIA のハードウェア専用です。Vite は
4.5 を同梱しています。<a href="Upscalers.md">アップスケーラー</a> を参照してください。
</def>
<def title="DLAA">
Deep Learning Anti-Aliasing。DLSS の再構築をネイティブ解像度で適用するもので、性能ではなく品質のためのものです。
</def>
<def title="Ray Reconstruction">
手作業で調整したレイトレーシングのデノイザーを、学習によるものに置き換える DLSS の機能。
</def>
<def title="FSR">
AMD FidelityFX Super Resolution。ベンダーを問わないアップスケーリング。Vite は DX12 専用の FSR 4.1.1 を同梱しています。
</def>
<def title="XeSS">
Intel Xe Super Sampling。ベンダーを問わず、Intel Arc のハードウェアではより高速な経路があります。Vite は XeFG の
フレーム生成を含む 3.1.0 を同梱しています。
</def>
<def title="NIS">
NVIDIA Image Scaling。時間方向の処理を持たない空間的なアップスケーリング。最も安価で品質も最も低い選択肢ですが、どこでも
動作します。
</def>
<def title="Streamline">
DLSS Frame Generation と RTX Dynamic Vibrance のための NVIDIA の SDK の層。Vite のプラグインは Streamline SDK 2.12 の上に
構築されています。Reflex は独立したプラグインとして同梱されています。
</def>
<def title="フレーム生成">
描画したフレームの間に中間のフレームを合成すること。表示されるフレームレートは上がりますが、入力の遅延は減らず、
わずかに増えます。
</def>
<def title="Reflex">
NVIDIA の入力遅延を減らす技術。フレーム生成を使うようになると、より重要になります。
</def>
</deflist>

## 物理

<deflist>
<def title="PhysX">
NVIDIA の物理エンジンで、4.27 までの Unreal の既定。Vite は Chaos に移行せずにこれを維持しています。
<a href="PhysX.md">PhysX</a> を参照してください。
</def>
<def title="Chaos">
UE5 で PhysX を置き換えた Epic の物理エンジン。Vite は使いません。
</def>
<def title="Apex Destruction">
PhysX の破壊可能なメッシュのシステム。UE5 では取り除かれ、Vite では残っています。
<a href="Destruction-And-Cloth.md">破壊とクロス</a> を参照してください。
</def>
<def title="Apex Cloth">
PhysX のクロスシミュレーション。UE5 では取り除かれ、Vite では残っています。
</def>
<def title="Blast">
Apex Destruction より柔軟な、NVIDIA の新しい破壊のライブラリ。ランタイムと作成用の別々のプラグインで同梱されています。
</def>
<def title="固定タイムステップ">
フレームの時間に関係なく一定の差分で物理を進め、フレームレートに依存しない決定性を得ること。Vite では
<code>VITE_PHYSX_FIXED_TIMESTEP</code> の背後にある任意の機能です。<a href="Fixed-Timestep.md">固定タイムステップ</a>
を参照してください。
</def>
<def title="サブステップ">
安定性のために、1 フレームの物理の更新をより小さなステップに分割すること。ステップの大きさをフレームをまたいで固定する
固定タイムステップとは異なります。
</def>
<def title="CCD">
Continuous Collision Detection。端点だけを調べるのではなく、フレーム間のボディの動きをスイープし、速いオブジェクトが
薄いジオメトリをすり抜けるのを防ぎます。離散的な検出より高価です。
</def>
<def title="CMC">
Character Movement Component。Unreal の標準的なキャラクターの移動コンポーネントで、群衆のシーンでインスタンスあたりの
コストが最も高いものの 1 つです。<a href="400-Characters-CMC-Bench.md">400 キャラクター CMC ベンチマーク</a> を参照して
ください。
</def>
</deflist>

## エンジンとビルド

<deflist>
<def title="Compiler Explorer / Godbolt">
MSVC、Clang、GCC が出力するアセンブリを表示するオンラインの C++ コンパイラ。
<a href="https://gcc.godbolt.org/">gcc.godbolt.org</a>。実行時間は計測しません。
<a href="Compiler-Explorer.md">Compiler Explorer</a> を参照してください。
</def>
<def title="Quick Bench">
Linux 上の GCC と Clang のための、オンラインの Google Benchmark の実行環境。
<a href="https://quick-bench.com/">quick-bench.com</a>。MSVC はありません。<a href="Compiler-Explorer.md">Compiler Explorer</a>
を参照してください。
</def>
<def title="DDC">
Derived Data Cache。コンパイル済みのシェーダー、クックしたテクスチャなどの派生データが保存される場所。
<a href="Cache-Management.md">キャッシュ管理</a> を参照してください。
</def>
<def title="UAT / UBT">
Unreal Automation Tool と Unreal Build Tool。UAT はインストール済みビルドやパッケージ化などの高レベルの操作を、UBT は
コンパイルを担います。
</def>
<def title="BuildGraph">
インストール済みビルドの作成に使われる、UAT の XML で記述するビルドの統括システム。
</def>
<def title="ISM / HISM">
Instanced Static Mesh と Hierarchical Instanced Static Mesh のコンポーネント。1 つのメッシュの多数のコピーを、少数の
ドローコールで描画します。<a href="Instanced-Physics.md">PhysX Instanced Subsystem</a> の描画側を担います。
</def>
<def title="ABI">
Application Binary Interface。Vite の文脈では、CPU と GPU で共有する構造体のバイナリのレイアウト。変更すると PSO の
キャッシュ、シリアライズ、レイトレーシングの安定性が壊れ、コントリビュートは即座に却下されます。
<a href="Coding-Guidelines.md">コーディングガイドライン</a> を参照してください。
</def>
<def title="ACL">
Animation Compression Library。Unreal に組み込みのアニメーション圧縮を、サイズと品質の関係がはるかに優れたものに
置き換えます。
</def>
<def title="モーションマッチング">
ステートマシンに従うのではなく、現在のポーズと軌跡をデータベースと照合して、実行時にアニメーションのフレームを選ぶこと。
Motion Symphony のプラグインが提供します。
</def>
<def title="FPU">
浮動小数点演算ユニット。PS5 の Zen 2 は <code>FP3</code> を削除し、<code>FP2</code> をストア専用にし、256 ビットの FMA
パイプを 1 本残しています。AVX2 と FMA のレイテンシーはそのままです。Series X の Zen 2 にはこの削減はありません。
<a href="PS5-CPU-FPU.md">PS5 CPU の FPU</a> を参照してください。
</def>
<def title="4700S">
さらに削減された Zen 2 のコア（Series X に比べて FPU を縮小）を 8 基持ち、内蔵 GPU が無効化された AMD のデスクトップ
キット。PhysX 3.4 の書き直しを含む、PS5 の CPU の FPU に関する作業の Windows 上での代替です。GPU のテスト機ではありません。
<a href="PS5-CPU-FPU.md">PS5 CPU の FPU</a> を参照してください。
</def>
</deflist>

## Vite Technology

Vite の次世代のシステムに使う製品名です。いずれも、すでにエンジンに含まれているものの上に築かれています。状況と詳細は
[Vite Technology](https://vitestudio-tech.github.io/UnrealEngineVite-Docs/tech/jp/) のサイトにあります。

<deflist>
<def title="Vite ReSTIR">
リアルタイムのグローバルイルミネーションのための、リザーバーによる時空間の再サンプリング。同じパイプライン上に
リアルタイムのパストレーサーを備えます。動的 DDGI、RTXDI、ReSTIR のファイナルギャザーを伴うピクセルごとの
レイトレーシング GI の上に築かれています。開発中です。
</def>
<def title="ViteX Physics">
Unreal Engine 4 と互換の物理 SDK。ゲーム向けに調整した PhysX 4 と 5 のソルバーの進歩と、Flex と Flow による GPU の高速化を
組み合わせます。Vite の PhysX 3.4、APEX、Blast、固定タイムステップ、インスタンス化ボディの上に築かれています。開発中です。
</def>
<def title="Vite BRDF">
Callisto に基づく、キャラクター向けの品質の BRDF。現在は実験的な Callisto BRDF のシェーディングモデルとして利用できます。
</def>
<def title="Vite Vertis">
標準のメッシュのパイプライン上での連続的な LOD。ゲームが出荷されるハードウェアで、Nanite 級のジオメトリの密度を目指して
います。開発中です。
</def>
<def title="Vite Hair FX">
TressFX 5.0 の上に築いたストランドのヘアで、新しいヘアの BRDF と、より低いフレームのコストを備えます。開発中です。
</def>
</deflist>

## 関連項目

- [コンソール変数](Console-Variables.md)
- [コンパイル時スイッチ](Compile-Time-Switches.md)
- [よくある質問](FAQ.md)
