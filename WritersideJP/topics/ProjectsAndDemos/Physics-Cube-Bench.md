# 物理キューブベンチマーク

<tldr>
<p>
従来の PhysX のアクターを使った剛体のスループットのテストです。<a href="Instanced-Physics.md">インスタンス化サブシステム</a>
の比較の基準になります。
</p>
</tldr>

<img src="PhysicsCubeBench.png" alt="1400 個のキューブのシミュレーションで、Chaos の 75.45 FPS と PhysX 3.4 の 148.44 FPS を並べたキャプチャ" border-effect="line"/>

*同じシーンで 1400 個のキューブをシミュレーション。Chaos（左）は 13.25 ms のフレームで 75.45 FPS、PhysX 3.4（右）は
6.74 ms のフレームで 148.44 FPS。*

## ダウンロード

[物理キューブベンチマーク](https://drive.google.com/file/d/1WVsC8cp2fx8eiM56Ueek-mJbO_EdPKOR/view?usp=sharing)

## 計測するもの

従来の方法でシミュレーションした単純な剛体です。ボディごとに 1 つのアクターがあり、それぞれが独自のコンポーネント、トランスフォーム、ティックを持ちます。標準のワークフローで、フレームの予算が尽きるまでにいくつの PhysX のボディをシミュレーションできるかを確かめます。

面白いのは数値そのものではなく、どこでスケールしなくなり、それがなぜかです。ボディの数とともに増えるコストは 2 つあり、増え方が異なります。

| コスト | 増える要因 |
|---|---|
| PhysX のソルバー | 実際に接触していて起きているボディ |
| アクターとコンポーネントのオーバーヘッド | 何かが動いているかどうかに関係なく、ボディの総数 |

2 つ目を取り除くのが [PhysX Instanced Subsystem](Instanced-Physics.md) です。このベンチマークと
[インスタンス化サブシステムのデモ](PhysX-Instanced-Subsystem.md) を比べると、その違いが直接分かります。

## 実行する

まず `stat unit`、次に:

| コマンド | 表示されるもの |
|---|---|
| `stat physics` | ソルバーの時間 |
| `stat game` | アクターのティックとコンポーネントのオーバーヘッド |
| `show Collision` | ソルバーが実際にシミュレーションしている形を確かめるための、コリジョンの形状 |

**Game** が **Physics** を大きく上回っていれば、上限はソルバーではなくアクターのオーバーヘッドであり、答えはインスタンス化の経路です。

## PhysX と Chaos

Vite は Chaos に移行せず PhysX を維持しています。この種の負荷では PhysX のほうが速く予測しやすいソルバーであることが、その理由の一部です。[PhysX](PhysX.md) を参照してください。

この種のシミュレーションでフレームレートに依存しない決定性が必要なら、Vite の任意の
[固定タイムステップ](Fixed-Timestep.md) が使えます。`VITE_PHYSX_FIXED_TIMESTEP=1` での再ビルドが必要です。

## 関連項目

- [PhysX](PhysX.md)
- [インスタンス化物理](Instanced-Physics.md)
- [固定タイムステップ](Fixed-Timestep.md)
- [プロファイリング](Profiling.md)
