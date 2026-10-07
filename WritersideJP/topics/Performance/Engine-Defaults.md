# エンジンの既定値の変更

<tldr>
<p>
Vite は性能のために、標準の Unreal Engine 4.27 の既定値をいくつか変更しています。これらの変更はプロジェクトに直接影響し、一部はコストだけでなく実行時の挙動も変えます。何かが壊れていると判断する前に、このページを読んでください。
</p>
</tldr>

標準の Unreal の既定値は、すべてがそのまま動くように選ばれており、ほとんどのプロジェクトが使わない機能まで有効になっています。Vite は、必要な機能は「オフにし忘れるもの」ではなく「オンにするもの」であるべきだという原則に基づき、その一部を性能重視に変更しています。

その代わり、標準の 4.27 から Vite に移したプロジェクトは挙動が変わることがあります。このページはその一覧です。

## 実行時の挙動の変更

<warning>
これらは性能だけでなく挙動も変えます。ゲームプレイのロジックが標準の既定値に依存している場合は、対応が必要です。
</warning>

### オーバーラップイベントは既定で無効

プリミティブコンポーネントは、明示的に有効にしない限りオーバーラップイベントを生成しなくなりました。

オーバーラップイベントの生成は、イベントに何かがバインドされているかどうかに関係なく、それを持つすべてのコンポーネントでコストがかかります。標準のプロジェクトでは、大半のプリミティブが誰も受け取らないオーバーラップイベントを生成しています。

**影響:** オーバーラップイベントが必要なコンポーネントは、**Generate Overlap Events** を明示的に設定する必要があります。トリガーボリューム、ピックアップの検出、`OnComponentBeginOverlap` で動くものはすべて、このフラグを設定してください。プロジェクトを移行した後に「トリガーが動かなくなった」という問題の最も可能性の高い原因です。

例外は `ACharacter` です。[March Major](ueVite26-MarchMajor.md) 以降、キャラクターではオーバーラップイベントに頼るプロジェクトが多いため、そのカプセルコンポーネントはオーバーラップイベントを有効のまま保ちます。無効にしたい場合は、`Character.cpp` の該当行に印が付いています。

<img src="OverlapEventsDisabled.png" alt="PrimitiveComponent.cpp で SetGenerateOverlapEvents(true) を bGenerateOverlapEvents = false に置き換えるコミットの差分" border-effect="line"/>

*`UPrimitiveComponent` の 1 行が、あらゆるプロジェクトのあらゆるプリミティブに適用されます。*

[コミット](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/02d7c0ad0a7542b382a70dc3e37877d6ec052d76)

### 最適化されたアクターのランタイム

アクターのランタイムの既定値は、`AActor::InitializeDefaults` でのアクターごとのオーバーヘッドを減らすように変更されています。

| 既定値 | 標準の 4.27 | Vite | 理由 |
|---|---|---|---|
| `SetCanBeDamaged` | `true` | `false` | ダメージシステムを使うアクターだけが必要とするため |
| `bRelevantForNetworkReplays` | `true` | `false` | 必要な場合を除き、アクターをデモのネットワーク録画から除外するため |
| `bRelevantForLevelBounds` | `true` | `false` | 境界を定義しないアクターに対するレベル境界の反復処理を避けるため |

<img src="OptimizedActorRuntime.png" alt="Actor.cpp で SetCanBeDamaged、bRelevantForNetworkReplays、bRelevantForLevelBounds の既定値を変更するコミットの差分" border-effect="line"/>

*ワールドの境界を定義する必要がある大きなメッシュ、ブロッキングボリューム、フォリッジは、`bRelevantForLevelBounds` を
`true` に戻す必要があります。*

[コミット](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/970cbb989c3712f13be1fa370b778e769e5d864c)

### スケルタルメッシュの最適化された構成

スケルタルメッシュは、ほとんどのプロジェクトで CPU の主要な負荷要因の 1 つです。そのため `USkeletalMeshComponent` は、Epic の全機能を有効にした既定値ではなく、性能重視の既定値で出荷されます。ワールド内のアセットには多くのスケルタルメッシュが含まれることが多く、コンポーネントごとに最適化した設定を有効にするのは現実的ではありません。安価な経路を既定にし、必要な箇所でだけ高価なオプションを有効にするほうが、実際に運用できる順序です。

| 既定値 | 標準の 4.27 | Vite |
|---|---|---|
| `VisibilityBasedAnimTickOption` | `AlwaysTickPoseAndRefreshBones` | `OnlyTickPoseWhenRendered` |
| `bEnableUpdateRateOptimizations` | `false` | `true` |
| `bHasCustomNavigableGeometry` | `Yes` | `No` |
| `bDisablePostProcessBlueprint` | `false` | `true` |
| `bUpdateOverlapsOnAnimationFinalize` | `true` | `false` |
| `bSkipKinematicUpdateWhenInterpolating` | `false` | `true` |
| `bSkipBoundsUpdateWhenInterpolating` | `false` | `true` |

<img src="SkeletalMeshesOptimizedConfig.png" alt="SkeletalMeshComponent.cpp の既定値を変更し、Epic の元の値を末尾のコメントに残しているコミットの差分" border-effect="line"/>

*変更した各行には Epic の元の値が末尾のコメントとして残されているため、上流を参照しなくても標準の挙動に戻せます。*

注意すべきは `VisibilityBasedAnimTickOption` です。`OnlyTickPoseWhenRendered` では、画面外のキャラクターはポーズの評価を完全に止めます。描画されていないキャラクターのボーンのトランスフォームやソケットを読むゲームプレイ（武器の銃口の位置、IK のターゲット、遠くのアクターのアタッチポイントなど）では、コンポーネントを `AlwaysTickPose` または
`AlwaysTickPoseAndRefreshBones` に戻す必要があります。

2 つ目は `bDisablePostProcessBlueprint = true` です。IK やボーンの補正によく使われるポストプロセスのアニメーションブループリントは、コンポーネントごとに再び有効にしない限り実行されなくなります。

2 つの `bSkip...WhenInterpolating` フラグが効くのは、Vite が同じくオンにしている更新レートの最適化を使う場合だけです。アニメーションを評価せずに補間するフレームでは、キネマティックの物理ボディとバウンドが更新されず、次に評価する Tick で追いつきます。至近距離のヒット判定に使うものなど、キネマティックのボディが毎フレームポーズに追従しなければならないコンポーネントでは、これらをオフにしてください。

<img src="SkeletalMeshDefault.png" alt="Epic の元の既定値が入った SkeletalMeshComponent.cpp のコンストラクターのブロック" border-effect="line"/>

*Epic の元の値（`bEnableUpdateRateOptimizations = false` など）が入った同じコンストラクターのブロック。これらの既定値が設定されている場所の文脈として示します。*

[コミット](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/33fe7c638829b8120e8a02ecc639acda761df835)

### ライトマップ UV の生成は無効 {id="generate-lightmap-uvs-disabled"}

スタティックメッシュのインポートで、既定ではライトマップ UV を生成しなくなりました。

ほとんどの Vite のプロジェクトはベイクしたライティングではなく [DDGI](DDGI-Dynamic.md) を使うため、インポートするすべてのメッシュにライトマップ UV を生成するのは、インポート時間と UV チャンネルの無駄です。プロジェクトでライティングをベイクする場合は、スタティックメッシュのインポートオプションでこの設定を有効にしてください。

[コミット](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/acce6fbe432fe9fe5a2536f0979befd5dcd741d1)

### アニメーションは既定で ACL で圧縮

`BaseEngine.ini` は、既定のボーンとカーブの圧縮設定を [Animation Compression Library](Bundled-Plugins.md)（`/ACLPlugin/ACLAnimBoneCompressionSettings` と `ACLAnimCurveCompressionSettings`）に向けているため、新しくインポートしたアニメーションは ACL を使います。ACL のプラグインが既定で有効なのも、[ViteSetup](ViteSetup.md) の Express の軽量化がそれを残すのも、このためです。既存のアニメーションは、保存されたときの圧縮設定を保ちます。

### スタンドアロンとパッケージ化したビルドのフレームレートを 120 に制限

`Engine/Config/BaseGameUserSettings.ini` の `FrameRateLimit=120.0` により、フレームペーシングを安定させるため、スタンドアロンとパッケージ化したゲームは 120&nbsp;FPS に制限されます（[July Major](ueVite26-JulyMajor.md) 以降）。

**影響:** 120&nbsp;FPS を超えて動くベンチマークは、いくつかの [デモプロジェクト](ProjectsAndDemos.md) も含め、制限を外すまで 120 と表示されます。実行時に `t.MaxFPS 0` で制限を外すか、プロジェクトの `DefaultGameUserSettings.ini` で `FrameRateLimit` を設定してください。

## スケーラビリティ

Vite は `Engine/Config/BaseScalability.ini` のシャドウのスケーラビリティグループを調整し直しています。標準の 4.27 は、Low でほぼシャドウなし、Epic と Cinematic で非常に高価なシャドウという幅の広い構成です。Vite はその幅を狭め、Low で実用的なシャドウを出し、High と Epic を安価にし、Medium は変更していません。

| グループ | `r.ShadowQuality`（標準 &rarr; Vite） | 標準からのその他の変更 |
|---|---|---|
| Low（`@0`） | 0 &rarr; **2** | カスケードを 1 から 4 に、最大シャドウ解像度 1024、ディスタンスフィールドとカプセルのシャドウを有効、ライト関数を有効、ライトの描画距離を短縮しない |
| Medium（`@1`） | 3 &rarr; 3 | なし |
| High（`@2`） | 5 &rarr; **4** | シャドウの距離スケール 0.85 &rarr; 0.75、カスケードの遷移 0.8 &rarr; 0.7 |
| Epic（`@3`） | 5 &rarr; 5 | カスケードの上限を 10 から 8 に、半径のしきい値 0.01 &rarr; 0.02、距離スケール 1.0 &rarr; 0.85、ボリュメトリックフォグのグリッドを 8&nbsp;px &times; 128 スライスから 16&nbsp;px &times; 64 スライスに |
| Cinematic | 5 &rarr; 5 | 最大シャドウ解像度 4096 &rarr; 2048、ボリュメトリックフォグのグリッドを 4&nbsp;px から 8&nbsp;px に、履歴ミス時のスーパーサンプルを 16 から 4 に |

トレーラーやオフラインのキャプチャで標準の Epic や Cinematic のシャドウの予算に頼っている場合は、エンジンのファイルを編集するのではなく、プロジェクトの `DefaultScalability.ini` でそれらの値を上書きしてください。

## ゲームプレイの既定値を元に戻す

上記のオーバーラップとスケルタルメッシュの既定値は、移行したプロジェクトを最も壊しやすいものです。[August Major](ueVite26-AugustMajor.md) 以降、エンジンのルートにある `ViteDefaults.bat` で、エンジンのソースを手で編集せずにそれぞれを Vite と標準の UE 4.27 の間で切り替えられます。

```
ViteDefaults.bat                                  :: 現在の状態を表示する対話式メニュー
ViteDefaults.bat -DetectOnly                      :: 現在の状態を報告するだけ
ViteDefaults.bat -SetOverlap ue427 -SetSkm vite   :: オーバーラップは標準、スケルタルメッシュは Vite の既定値
```

このツールは `PrimitiveComponent.cpp` と `SkeletalMeshComponent.cpp` の既定値を書き換えるため、実行後にエディタを再ビルドしてください。可能であれば、影響を受けるコンポーネントをプロジェクト側で修正するほうを優先してください。エンジンの既定値を元に戻すと、そのコストがすべてのレベルのすべてのプリミティブやスケルタルメッシュに戻ってきます。

## 無効化されたプラグイン {id="disabled-plugins"}

Vite のプラグインプロファイルは、ほとんどの Win64 のプロジェクトが読み込まないエンジンのプラグインをオフにし、エディタの起動時間、読み込むモジュールの数、パッケージ化したビルドのサイズを減らします。プロファイルがツリーに適用される方法はリリースによって異なります。

| リリース | プロファイルの適用方法 |
|---|---|
| [LTS](ueVite25-LTS.md) から [June Major](ueVite26-JuneMajor.md) | ソースツリーに組み込み済み。プラグインは `EnabledByDefault` が `false` の状態で出荷 |
| [July Major](ueVite26-JulyMajor.md) 以降 | 互換性のため、ツリーは標準の 4.27 の値で出荷。`devops\ueVite-ApplyVitePluginDefaults.bat` を実行してプロファイルを適用 |

プロファイルの内容は `devops\ViteEnginePluginDefaults.txt` の一覧です。39 のエンジンのプラグインを無効にし、1 つを有効にします。

- **無効:** Paper2D、CLion・CodeLite・KDevelop のソースコードアクセス、Plastic SCM と Subversion のソース管理、Chaos Cloth・
  Chaos Editor・Chaos Niagara と Chaos のソルバーのプラグイン、Alembic のインポーター、Facial Animation、Crypto Keys、Android・Apple・WMF のメディア再生、OpenXR・Oculus VR・SteamVR、そして Google Cloud Messaging、Google PAD、Chunk Downloader、Mobile Patching Utils などのモバイル向けサービス。
- **有効:** Vite の [破壊](Destruction-And-Cloth.md) の経路である Blast。

```
devops\ueVite-ApplyVitePluginDefaults.bat            :: Vite のプロファイルを適用
devops\ueVite-ApplyVitePluginDefaults.bat --dryrun   :: 変更内容を報告するだけ
devops\ueVite-ApplyVitePluginDefaults.bat --stock    :: 標準の 4.27 の値に戻す
```

`--yes` を付けると確認のプロンプトを省略します。このスクリプトは `.uplugin` ファイルだけを編集するため、`.uproject` で明示的に指定したプラグインは、どちらの場合もそのまま残ります。

**特に VR のプラグインは、必要な場合は再び有効にする必要があります。** Windows で Media Framework を通じて動画を再生するプロジェクトでは、WMF Media も同様です。

[コミット 1](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/e9aebc2ef9f8acb7326a7e989f288ef68969342f) &middot;
[コミット 2](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/6c5948bf12ea61f82784193ccaa5d43c4f574ae9)

## 無効にできるティック

### Niagara

Niagara はプラグインが有効であれば常にティックします。使わない場合はプロジェクトレベルで Niagara のプラグインを無効にしてください。4.27 では Cascade も引き続き利用できます。

## レイトレーシングのエフェクトは無効で始まる {id="ray-traced-effects-off"}

標準の 4.27 では、レイトレーシングの反射、半透明、アンビエントオクルージョンを実行するかはポストプロセスボリュームが決め（`-1`）、レイトレーシングのシャドウは有効（`1`）です。[LTS](ueVite25-LTS.md) 以降のすべての Vite のリリースでは、4 つとも `0` です。

| CVar | 標準の 4.27 | Vite |
|---|---|---|
| `r.RayTracing.Reflections` | `-1`（ポストプロセスボリュームが決定） | `0` |
| `r.RayTracing.Translucency` | `-1`（ポストプロセスボリュームが決定） | `0` |
| `r.RayTracing.AmbientOcclusion` | `-1`（ポストプロセスボリュームが決定） | `0` |
| `r.RayTracing.Shadows` | `1` | `0` |

`0` のときは、これらのエフェクトに関するポストプロセスボリュームの設定は無視されます。そのため、ボリュームでこれらを有効にしていたプロジェクトは、Vite に移ると何も表示されなくなります。標準の挙動に戻すには CVar を `-1` に、エフェクトを強制的に有効にするには `1` に設定してください。

```ini
; Config/DefaultEngine.ini
[/Script/Engine.RendererSettings]
r.RayTracing.Reflections=-1
r.RayTracing.AmbientOcclusion=-1
```

レイトレーシングの半透明は既定でコンパイル対象からも外れている（`VITE_RT_PSO_DEBLOAT`）ため、その CVar が意味を持つのはこのスイッチを無効にしたビルドだけです。ヘルプテキストは今も `-1` を既定値と表示していますが、コード上の値は `0` です。

## レイトレーシングのカリング: 変更なし、有効にする価値あり {id="ray-tracing-culling"}

ここで Vite は標準の 4.27 の挙動を維持しています。`r.RayTracing.Culling` の既定値は `0` で、レイトレーシングの対象のプリミティブは、カメラとの位置関係に関係なくすべてアクセラレーション構造に残ります。大きなシーンでは、これを有効にすることが最も安価なレイトレーシングの節約の 1 つです。

```ini
; Config/DefaultEngine.ini
[SystemSettings]
r.RayTracing.Culling=1
r.RayTracing.Culling.Radius=10000
r.RayTracing.Culling.Angle=1
```

カリングを有効にすると、**カメラの後ろ** にあるオブジェクトのうち、`r.RayTracing.Culling.Radius`（既定 10000、100&nbsp;m）より遠いもの、または投影された角度が `r.RayTracing.Culling.Angle` より小さいものが除外されます。カメラの前にあるものは決してカリングされないため直接見える画面は変わりませんが、カリングされたオブジェクトは反射とレイトレーシングのシャドウから消えます。有効にした後は、プレイヤーの後ろにある鏡や大きなシャドウの投影元を確認してください。

<note>
UE5 の <code>r.RayTracing.Culling.UseMinDrawDistance</code> は、4.27 にも Vite にも存在しません。
</note>

## エディタの既定値

これらは実行時の性能には影響しませんが、エディタの挙動を変えます。`Engine/Config/BaseEditorSettings.ini` と `BaseEditorPerProjectUserSettings.ini` で設定されています。

| 設定 | Vite の既定値 | 効果 |
|---|---|---|
| `bDisableAllTutorialAlerts` | `True` | エディタでチュートリアルの案内を表示しない |
| `bShowNewPluginsPopup` | `True` | `False` にすると「新しいプラグインがあります」のポップアップを止められる |
| `bSendUsageData`、`bSendUnattendedBugReports` | `False` | エディタは使用状況のデータも無人のクラッシュレポートも送信しない |
| `bEnableAsyncTextureCompilation` | `True` | テクスチャをエディタを止めずにバックグラウンドでコンパイルする |
| `bCopyStarterContentPreference` | `False` | 新しいプロジェクトは Starter Content なしで始まる |
| `bGenerateLightmapUVs` | `False` | [ライトマップ UV の生成は無効](#generate-lightmap-uvs-disabled) を参照 |

エディタのニュースフィードも取り除かれています。また、UE5 の挙動をバックポートし、アニメーションのアセットは常に新しいエディタのタブで開きます（[コミット](https://github.com/GapingPixel/UnrealEngineVite-PhysX/commit/8bdae919e6eae61a27ef8d09d38027592a473d8c)）。

## 自分で行える任意のデブロート

これらは互換性のためにフォークのリリースブランチでは無効にできませんが、個々のプロジェクトでは利用できます。

**Vite のプラグインの削除。** 追加された Vite のプラグインを取り除くと、コンパイル時間が短くなります。Houdini Engine がまだ同梱されていた時期の Ryzen 9 9950X3D での計測では、リポジトリ全体で 15 分、Vite のプラグインなしで 12 分で、単一で最も大きな要因は Houdini でした。[June Major](ueVite26-JuneMajor.md) で Houdini が外されたため、現在のリリースでは差はより小さくなっています。

ツールについては [デブロートガイド](Debloat-Guide.md) を参照してください。

## 既存のプロジェクトを移行する

<procedure title="移行したプロジェクトを Vite の既定値と照らし合わせて確認する" id="check-defaults">
    <step>
        すべてのトリガーボリュームとオーバーラップで動くインタラクションをテストします。オーバーラップイベントは最もよくある不具合の原因です。
    </step>
    <step>
        リーダー／フォロワーのスケルタルメッシュ構成を使うキャラクターで、カーブの伝播が欠けていないかを確認します。
    </step>
    <step>
        プロジェクトでライティングをベイクする場合は、ライトマップ UV の生成を再び有効にし、既存のメッシュに有効なライトマップ UV があることを確認します。
    </step>
    <step>プロジェクトに必要なプラグイン、特に VR と WMF Media を再び有効にします。</step>
    <step>Low、High、Epic、Cinematic のシャドウが標準と異なるため、スケーラビリティの設定を見直します。</step>
    <step>
        レイトレーシングの反射、半透明、AO をポストプロセスボリュームで制御している場合は、それらの CVar を <code>-1</code> に設定します。<a href="#ray-traced-effects-off">レイトレーシングのエフェクトは無効で始まる</a> を参照してください。
    </step>
</procedure>

## 関連項目

- [UE5 からの移行](Migrating-From-UE5.md)
- [デブロートガイド](Debloat-Guide.md)
- [プロファイリング](Profiling.md)
- [コンパイル時スイッチ](Compile-Time-Switches.md)
