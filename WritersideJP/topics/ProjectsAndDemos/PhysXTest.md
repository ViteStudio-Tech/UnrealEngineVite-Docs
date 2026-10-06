# PhysX テスト

<tldr>
<p>
PhysX の全般的な挙動と安定性をテストするプロジェクトです。エンジンの変更後に、ビルドの物理の層が無事かを確認するのに役立ちます。
</p>
</tldr>

## ダウンロード

[PhysicsTest のリポジトリ](https://github.com/tanger1n/PhysicsTest)

## 対象

スループットのベンチマークではなく、PhysX の挙動を幅広く動かすものです。コリジョンの応答、コンストレイント、積み重ねの安定性、スリープと起床、そしてソルバーが本来あるべき振る舞いをするかという全般的な問いを扱います。

<img src="PhysXTest1.png" alt="PhysX テストのプロジェクト、コリジョンとコンストレイントのシナリオ" border-effect="line"/>

<img src="PhysXTest2.png" alt="PhysX テストのプロジェクト、積み重ねの安定性のシナリオ" border-effect="line"/>

<img src="PhysXTest3.png" alt="PhysX テストのプロジェクト、スリープと起床のシナリオ" border-effect="line"/>

*テストプロジェクトのシナリオ。それぞれが 1 つの挙動を切り離しているため、不具合は動いた数値としてではなく、目に見える違いとして現れます。*

物理に関わる何かを変更して、どれだけ速いかではなく、壊していないかを知りたいときに実行するのがこのプロジェクトです。

## Vite との関わり

Vite は Chaos に移行せず PhysX を維持しており、その選択は、エンジンの変更を経ても PhysX の層が正しく保たれて初めて正当化できます。次のものに触れる変更は:

- 物理シーンやサブステップ、特に [`VITE_PHYSX_FIXED_TIMESTEP`](Fixed-Timestep.md) を有効にした場合
- ボディのインスタンスのトランスフォームや補間
- キャラクタームーブメントコンポーネントが多用する、コリジョンのクエリの経路
- Apex Destruction や Cloth の統合

完了とみなす前に、ここで確認すべきです。確認の要件は [コーディングガイドライン](Coding-Guidelines.md) を参照してください。

## 固定タイムステップのテスト

[固定タイムステップの物理](Fixed-Timestep.md) を評価するなら、このプロジェクトは違いを観察するのに適した場所です。フレームレートを制限せずに実行し、次に `t.MaxFPS` をさまざまな値にして実行します。既定の可変タイムステップではシミュレーションの結果がフレームレートによって変わり、固定タイムステップでは変わらないはずです。

固定タイムステップはコンパイル時の機能であることを忘れないでください。ビルドに `VITE_PHYSX_FIXED_TIMESTEP=1` がなければ、`p.VitePhysXFixedTimestep.Enabled` は何もしません。

## 関連項目

- [PhysX](PhysX.md)
- [固定タイムステップ](Fixed-Timestep.md)
- [物理キューブベンチマーク](Physics-Cube-Bench.md)
- [コンパイル時スイッチ](Compile-Time-Switches.md)
