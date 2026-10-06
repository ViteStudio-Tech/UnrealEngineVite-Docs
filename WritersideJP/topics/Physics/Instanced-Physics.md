# インスタンス化物理

<tldr>
<p>
Instanced Static Mesh コンポーネントの個々のインスタンスに専用の PhysX 剛体を与え、安定した数値ハンドルで制御する
Vite のプラグインです。オブジェクトごとに 1 つのアクターを使うのでは負担しきれない、数千個のオブジェクトのシミュレーションのために作られています。
</p>
</tldr>

<img src="PhysXInstancedSubsystem.png" alt="PhysX Instanced Subsystem でシミュレーションされた大量のインスタンス化剛体" border-effect="line"/>

*インスタンスごとに本物の PhysX ボディを持つインスタンス描画。1 つの Instanced Static Mesh コンポーネントがすべてのオブジェクトを描画し、まだ動いているものについてはサブシステムがそれぞれの PhysX ボディを所有します。*

Unreal で多数のオブジェクトをシミュレーションする標準的な方法は、オブジェクトごとに 1 つのアクターを用意し、それぞれにプリミティブコンポーネントとボディインスタンスを持たせることです。これは数百個までは機能しますが、そこを超えると破綻します。アクターのオーバーヘッド、コンポーネントの Tick、トランスフォームの伝播、シーングラフの更新のコストが、物理そのものより大きくなるのです。

PhysX Instanced Subsystem は、この 2 つの関心事を分離します。描画は 1 つの Instanced Static Mesh コンポーネントで行い、物理はサブシステムが直接所有する PhysX のボディで行います。オブジェクトごとのアクターもコンポーネントもありません。

| 項目 | 値 |
|---|---|
| プラグイン | `Engine/Plugins/Runtime/VitePlugins/PhysXInstancedSubsystem` |
| バージョン | 1.11（[March Major](ueVite26-MarchMajor.md) 以降） |
| モジュール | `PhysXInstancedSubsystem` |
| サブシステム | `UPhysXInstancedWorldSubsystem`（Tick 可能なワールドサブシステム） |
| アクター | `APhysXInstancedMeshActor` |
| コンポーネント | `UPhysXInstancedStaticMeshComponent` |
| 作者 | NordVader Inc. |

動作するプロジェクトは [PhysX インスタンスサブシステムのデモ](PhysX-Instanced-Subsystem.md) を参照してください。

## 基本概念

**インスタンスはポインターではなくハンドルで指定します。** `FPhysXInstanceID` は `uint32` をラップしたもので、`0` は無効を意味します。ハンドルはインスタンスがアクター間を移動しても変わりません。ISM のインスタンスのインデックスはインスタンスを削除するとずれるため、これは重要です。ゲームプレイのコードはハンドルを保持し、サブシステムがハンドルからコンポーネントとインデックスへの対応を管理します。

**動的インスタンスと格納インスタンスは、同じインスタンスの異なる状態です。** 動的インスタンスは PhysX のボディを持ち、シミュレーションされます。格納インスタンスは PhysX のボディを一切持たず、別の格納用アクターに置かれます。両者の間で変換してもハンドルは保たれます。これが性能の中心となる仕組みです。静止した破片は格納インスタンスに変換され、シミュレーションのコストはゼロになり、表示はそのまま残ります。

**処理はフレームごとに予算が決められています。** PhysX のボディの生成、力の適用、ライフタイムの期限切れの処理はすべてキューに入り、フレームごとの上限に従って処理されます。そのため、1 フレームで 1 万個のインスタンスを生成しても、1 万個のボディ分のヒッチは起きません。

## アクターのセットアップ

レベルに `APhysXInstancedMeshActor` を配置し、詳細パネルの **Phys X Instance** で設定します。

<procedure title="インスタンス化物理のアクターを設定する" id="setup-instanced-actor">
    <step><b>Static Mesh</b> を設定し、必要であればマテリアルを上書きします。</step>
    <step>
        <b>Spawn Mode</b> を選びます。<b>Manual</b> は <b>Instance Relative Transforms</b> の配列を使い、
        <b>Grid</b> は間隔の設定から 行 &times; 列 &times; 層 のグリッドを生成します。後者はベンチマークやテストシーンに便利です。
    </step>
    <step>
        <b>Instance Shape Type</b> を設定します。Box、Sphere、Capsule が最も軽く、<b>Convex Mesh</b> は正確で中程度のコスト、<b>Triangle Mesh</b> はスタティックまたはキネマティック専用です。
    </step>
    <step>
        <b>Simulate Instances</b> と <b>Instances Use Gravity</b> を設定し、既定値がオブジェクトに合わない場合は質量の上書きと減衰も設定します。
    </step>
    <step>
        描画コンポーネントがサブシステムのボディとは別に独自のコリジョンを作らないよう、<b>Disable ISM Physics</b>
        は有効のままにしておきます。
    </step>
    <step>
        <b>Auto Register On Begin Play</b> を有効にするか、エディタからも呼び出せる
        <code>BuildAndRegisterInstances</code> を呼び出します。
    </step>
</procedure>

Convex や Triangle の形状でコリジョンメッシュを指定しない場合は、描画用メッシュが使われます。質量はコリジョンメッシュ上の物理マテリアルの密度から計算され、g/cm³ から kg/m³ に変換されたうえで、コンポーネントの質量スケールが掛けられます。

## 自動停止

大規模なシミュレーションを負担可能にしているのが自動停止です。実質的に動きを止めたインスタンスを検出し、より安価な状態に移します。

**Phys X Instance > Runtime > Auto Stop Config** で設定します。

| 設定 | 既定値 | 用途 |
|---|---|---|
| Enable Auto Stop | `false` | 全体の有効化 |
| Condition | PhysX のスリープフラグ | 「停止」の判定方法 |
| Linear Speed Threshold | `5.0` cm/s | 速度ベースの条件で使用 |
| Angular Speed Threshold | `5.0` deg/s | 速度ベースの条件で使用 |
| Min Stopped Time | `0.5` s | 処理を行う前に条件が成立し続けるべき時間 |
| Action | Destroy Body | 条件が成立したときの処理 |

条件は **PhysX のスリープフラグのみ**、**速度のしきい値のみ**、**スリープまたは速度**、**スリープかつ速度** から選びます。スリープフラグが最も軽く、通常はそれで十分です。速度のしきい値は、見た目には止まっているもののスリープしていない、ゆっくり漂っているボディを捕捉します。

処理は、影響の小さい順に次のとおりです。

| 処理 | 効果 |
|---|---|
| 何もしない | 状態の追跡のみ |
| シミュレーションを無効化（ボディは保持） | ボディは残るがシミュレーションを停止 |
| ボディを破棄（インスタンスは保持） | PhysX のボディを解放し、表示上のインスタンスはその場に残る |
| ボディとインスタンスを削除 | 両方を解放。ISM のインデックスがずれるため、インデックスではなくハンドルを使うこと |
| 格納に変換 | インスタンスを格納用アクターに移し、ボディを解放し、ハンドルを保持 |

表示を残したい破片には、通常 **格納に変換** が適切です。オブジェクトを残しつつ二度と動かさない場合は **ボディを破棄** が適しています。

### 安全のためのルール

自然には止まらないインスタンスを捕捉するルールが 2 つあります。

- **Max Fall Time** は、インスタンスがしきい値より長く落下し続けた後に停止の処理を実行します。ワールドのジオメトリをすり抜けて落ちたオブジェクトを捕捉します。
- **Max Distance From Actor** は、インスタンスが所有者からしきい値より遠くへ移動したときに実行されます。誤ったインパルスで吹き飛ばされたオブジェクトを捕捉します。

これとは別に、**Use Custom Kill Z** と **Custom Kill Z** の高さ、**Lost Instance Action** で、ワールドの Z のしきい値より下に落ちたインスタンスを処理します。

## ライフタイム

インスタンスはタイマーで期限切れにできます。アクターで **Enable Lifetime**、**Default Life Time Seconds**、**Default Lifetime Action** を設定するか、生成リクエストで生成ごとに上書きします。

期限切れは期限の時刻をキーとする最小ヒープで管理されるため、フレームごとのコストはインスタンスの総数ではなく、実際に期限切れになるインスタンスの数に比例します。

## 連続衝突検出

CCD は高速なボディが薄いジオメトリをすり抜けるのを防ぎますが、無料ではありません。**CCD Config** には 4 つのモードがあります。

| モード | 挙動 |
|---|---|
| Off | 使用しない |
| Simulating bodies only | 実際に動的なボディのみ |
| Auto (by velocity) | **Min CCD Velocity**（既定値 2000 cm/s）を超えたときに有効。**Max CCD Velocity** で上限を設定可能 |
| All bodies | 常に使用 |

破片の既定には速度による自動判定が適しています。ゆっくり動くチャンクは CCD を完全にスキップし、速いものだけがコストを支払います。

## 実行時の API

すべてブループリントから呼び出せます。ワールドからサブシステムを取得し、ハンドルを通じて操作します。

### 生成

```c++
FPhysXSpawnInstanceRequest Request;
Request.ActorMode = EPhysXInstanceActorMode::FindOrCreateByMeshAndMats;
Request.StaticMesh = DebrisMesh;
Request.InstanceWorldTransform = SpawnTransform;
Request.bStartSimulating = true;
Request.InitialLinearVelocity = LaunchVelocity;
Request.bOverrideLifetime = true;
Request.LifeTimeSeconds = 15.0f;
Request.LifetimeAction = EPhysXInstanceStopAction::ConvertToStorage;

const FPhysXSpawnInstanceResult Result = Subsystem->SpawnPhysicsInstance(Request);
```

**Actor Mode** はインスタンスの配置先を決めます。`AlwaysCreateNew` は新しいアクターを生成し、`FindOrCreateByMeshAndMats` はメッシュとマテリアルが一致する既存のアクターを再利用し、`UseExplicitActor` は指定したアクターを対象にします。通常は `FindOrCreateByMeshAndMats` を選びます。インスタンスをできるだけ少ない ISM
コンポーネントにまとめられるため、描画側が効率的になります。

コンポーネント上にすでに存在するインスタンスをまとめて登録するには、`RegisterInstancesBatch` が処理を複数のフレームに分散させます。

### 力とクエリ

力とインパルスの関数には、通常版と Advanced 版があります。Advanced 版は `bIncludeStorage` と
`bConvertStorageToDynamic` を受け取り、その呼び出しで格納インスタンスを動的なボディに戻すかどうかを制御します。静止した破片の山が後の爆発に反応するのは、この仕組みによるものです。

```c++
Subsystem->AddRadialImpulse(
    ExplosionOrigin, /*Radius=*/500.0f, /*Strength=*/80000.0f,
    /*bVelChange=*/false,
    /*bIncludeStorage=*/true,
    /*bConvertStorageToDynamic=*/true,
    /*bLinearFalloff=*/true);
```

空間クエリはヒット結果ではなくハンドルを返します。`RaycastInstanceID`、`SweepSphereInstanceID`、`OverlapSphereInstanceIDs`、`FindNearestInstance`、`FindNearestInstanceAdvanced` です。それぞれ任意のデバッグモード（`None`、`Basic`、`Detailed`）と描画時間を受け取り、クエリが期待どおりに当たらない理由を理解する最も早い方法になります。

### イベント

`APhysXInstancedMeshActor` は 6 つのマルチキャストデリゲートを公開しています。`OnInstancePreRemove`、`OnInstancePostRemove`、`OnInstancePreConvert`、`OnInstancePostConvert`、`OnInstancePrePhysics`、`OnInstancePostPhysics` です。

イベントはアクターの **Instance Event Mask** のビットマスクで制御されます。実際にバインドしない限りマスクは空のままにしてください。何も受け取らないのに数千のインスタンスにブロードキャストするのは無駄な処理です。削除と変換のイベントは、理由（`Explicit`、`Expired`、`AutoStop`、`KillZ`、`Lost`）とその時点のワールドトランスフォームを伝えます。破片が落ち着いたときにパーティクルエフェクトを出したりサウンドを鳴らしたりするのに必要な情報です。

## パフォーマンスの調整

| 設定 | 既定値 | 効果 |
|---|---|---|
| `MaxAddActorsPerFrame` | `64` | フレームごとに PhysX シーンに追加するボディの数。`0` は無制限。 |
| `MaxInstanceTasksPerFrame` | `4096` | フレームごとの、キューに入った力・インパルス・スリープ・ウェイクの操作の数。`0` は無制限。 |
| `MaxLifetimeExpirationsPerTick` | `4096` | Tick ごとに処理するライフタイムの期限切れの数。`0` は無制限。 |

3 つともサブシステムの設定プロパティなので、`DefaultGame.ini` で設定し、プラットフォームごとに調整できます。

最初に調整すべきは `MaxAddActorsPerFrame` です。PhysX のボディをシーンに追加するのは軽い処理ではなく、生成の集中はヒッチの最も起こりやすい原因です。値を下げるとコストが分散し、上げると新しく生成した破片が動き出すまでの遅れが短くなります。

サブシステムは可能な範囲でインスタンスを並列に評価します。ワーカースレッドは PhysX の状態とアクターの設定をコピーしたスナップショットを通じて読み取り、UObject には一切触れません。ゲームスレッドが、コンポーネントごとにまとめたトランスフォームの更新として結果を反映します。

## 指針

**使うべき対象:** 破片、薬莢、分離した後の破壊の欠片、倒れたプロップ、散らばった小物など、数百から数千のオブジェクトをシミュレーションしたいもの全般。

**使うべきでない対象:** 独自のゲームプレイロジック、コンポーネント、レプリケーション、ブループリントの振る舞いを必要とするオブジェクト。それらはアクターであり、アクターのままにしておくべきです。

**注意点:** ISM のインデックスのずれ。表示上のインスタンスを削除すると、それより後ろのインスタンスのインデックスが変わります。サブシステムは自身の対応関係を修正しますが、自分のコードでキャッシュしたインデックスは不正になります。ハンドルをキャッシュしてください。

## 関連項目

- [PhysX](PhysX.md)
- [PhysX インスタンスサブシステムのデモ](PhysX-Instanced-Subsystem.md)
- [破壊とクロス](Destruction-And-Cloth.md)
- [物理キューブベンチマーク](Physics-Cube-Bench.md)
- [プロファイリング](Profiling.md)
