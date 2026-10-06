# 最初のプロジェクト

<tldr>
<p>
通常どおりプロジェクトを作成します。<a href="DDGI-Dynamic.md">動的 DDGI</a> はすでに有効です（<code>r.GlobalIllumination.ExperimentalPlugin 1</code>）。<code>r.SSGI.Enable 1</code> と組み合わせ、パフォーマンス目標に必要なレイトレーシングエフェクトだけを有効にしてください。これらは無効の状態で始まります。
</p>
</tldr>

Vite でのプロジェクト作成は、標準の Unreal Engine 4.27 とまったく同じです。異なるのは既定のレンダリング設定なので、このページではプロジェクトを開いた直後に行うべきことに焦点を当てます。

<note>
このマニュアルが扱うのは Vite が変更した部分であり、Unreal Engine そのものではありません。変更していない部分、つまりプロジェクト構成、テンプレート、コンテンツブラウザ、ブループリント、マテリアル、パッケージングについては、Epic の 4.27 ドキュメントがそのまま適用され、引き続き参照先となります。
<a href="https://dev.epicgames.com/documentation/unreal-engine/working-with-unreal-projects-and-templates?application_version=4.27">Working with Unreal Projects and Templates (4.27)</a>
</note>

## プロジェクトを作成する

<procedure title="新しい Vite プロジェクトを作成する" id="create-project">
    <step>デスクトップのショートカットまたは <code>Engine\Binaries\Win64\UE4Editor.exe</code> からエディタを起動します。</step>
    <step>テンプレートを選びます。Third Person テンプレートはデブロートのプリセットでも残されるもので、最も安全な出発点です。</step>
    <step>レンダリング機能をコードから制御するつもりなら、ブループリントではなく C++ を選んでください。このマニュアルの例の多くはそれを前提としています。</step>
    <step>プロジェクトを作成し、最初のシェーダーコンパイルが終わるのを待ちます。初回はエンジンがシェーダーキャッシュを一から構築するため、時間がかかります。</step>
</procedure>

既存のプロジェクトを開く場合は、`.uproject` を右クリックして **Switch Unreal Engine version** を選び、`UE_ViteFork` を選択します。

## コンテンツを作る前に既定値を理解する

> 新規プロジェクトはレイトレーシングのサポートと動的 DDGI が有効な状態で始まります。レイトレーシングの反射、
> シャドウ、アンビエントオクルージョン、半透明は既定で無効で、プロジェクト単位またはポストプロセスボリューム単位で
> 有効にします。そのため、各エフェクトにフレームのどれだけを割くかを自分で決められます。
>
{style="note"}

プロジェクトに本当に必要なエフェクトを早めに決めてください。その答えが、アートとパフォーマンスの予算全体を左右します。4K120 を目標とするスタイライズドな対戦タイトルなら、通常は DDGI だけを使います。4K60 を目標とする品質重視のタイトルなら、レイトレーシング反射とテッセレーションを加えるかもしれません。Vite がチューニングの基準としている 4 つの構成は [パフォーマンス目標](Performance-Targets.md) を参照してください。

コンテンツを本格的に作り始める前に読んでおくべきもう 1 つの既定値群が、[エンジン既定値の変更](Engine-Defaults.md)
です。その中にはコストだけでなく挙動を変えるものがいくつかあります。特に、プリミティブコンポーネントのオーバーラップイベントは既定で無効で、インポート時のライトマップ UV の生成も既定で無効になっています。

## コードから機能を有効にする

サンプルプロジェクトでこれらを設定する一般的な場所は、キャラクタークラスのコンストラクタか `BeginPlay` です。Vite のサンプルプロジェクトもそうしています。

```c++
// Global illumination
IConsoleManager::Get().FindConsoleVariable(TEXT("r.GlobalIllumination.ExperimentalPlugin"))->Set(1);
IConsoleManager::Get().FindConsoleVariable(TEXT("r.SSGI.Enable"))->Set(1);

// Ray tracing effects available in a default build (they start disabled)
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.AmbientOcclusion"))->Set(1);
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.Reflections"))->Set(1);
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.Shadows"))->Set(1);

// Compiled out unless the engine is rebuilt with VITE_RT_PSO_DEBLOAT=0
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.Translucency"))->Set(1);
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.SampledDirectLighting"))->Set(1);
IConsoleManager::Get().FindConsoleVariable(TEXT("r.RayTracing.MeshCaustics.Enable"))->Set(1);
```

`r.GlobalIllumination.ExperimentalPlugin 1` は DDGI を有効にします。`BaseEngine.ini` ですでに設定されているため、この行が必要なのはプロジェクトで無効にした場合だけです。SSGI の併用は任意ではなく推奨です。DDGI はワールド規模のバウンスを解決し、SSGI はプローブボリュームでは粗すぎて捉えられない高周波の接触ディテールを補います。[DDGI と SSGI の併用](SSGI.md) を参照してください。

製品版では、コードではなく設定ファイルで指定することをお勧めします。そうすればスケーラビリティの仕組みに組み込まれ、プラットフォームごとに上書きできます。

```ini
; Config/DefaultEngine.ini
[/Script/Engine.RendererSettings]
r.GlobalIllumination.ExperimentalPlugin=1
r.SSGI.Enable=1
r.RayTracing.Reflections=1
```

`r.RayTracing.ForceAllRayTracingEffects 1` はすべてを一度に有効にします。エンジンの能力をざっと確認するには便利ですが、出荷用の設定としては不適切です。

## 動作を確認する

チルダキーでコンソールを開き、いくつかの項目を確認します。

- `stat unit` &mdash; フレーム、ゲーム、描画、GPU の各時間です。RT エフェクトを有効にした後に GPU 時間が支配的になるのは想定どおりなので、そこから順にエフェクトを無効にしていきます。
- `stat gpu` &mdash; パスごとの GPU コストです。反射と GI のどちらが重いかはこれで分かります。
- `r.RayTracing.Reflections 0` &mdash; 実行中にエフェクトを切り替えて差分を確認します。

Vite には、エディタ内とゲーム内でプロファイリングを行う ImGui ベースのベンチマークツールも同梱されています。[プロファイリング](Profiling.md) を参照してください。

## 開いてみる価値のあるサンプルプロジェクト

テストシーンを一から作るより、すでに機能を実演しているシーンから始めるほうが効率的です。

- [テックデモプロジェクト](Tech-Demo-Project.md) &mdash; DDGI のコーネルボックス、Apex Destruction のテスト環境、Apex Cloth のサンプル、DDGI と SSGI を組み合わせたハイエンドの洞窟シーン。
- [廃アパートメント](Abandone-Apartment.md) と [屋根裏シーン](Attic-Scene.md) &mdash; NVIDIA のオリジナルの
  RTGI ショーケースシーン。
- [物理キューブベンチマーク](Physics-Cube-Bench.md) と [400 キャラクター CMC ベンチマーク](400-Characters-CMC-Bench.md)
  &mdash; このマニュアルで引用している数値の元になったベンチマークシーン。

全一覧は [プロジェクトとデモ](ProjectsAndDemos.md) を参照してください。

## 関連項目

- [グローバルイルミネーション](Global-Illumination.md)
- [レイトレーシング](Ray-Tracing.md)
- [エンジン既定値の変更](Engine-Defaults.md)
- [コンソール変数](Console-Variables.md)
- [UE5 からの移行](Migrating-From-UE5.md)
