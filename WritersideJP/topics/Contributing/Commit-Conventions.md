# コミット規約

<tldr>
<p>
すべてのコミットの件名の先頭に、1 つ以上のカテゴリーのタグを付けます。広いものから具体的なものの順に重ねます。
バックポートとプラグインの追加では、元のコミットやリポジトリへのリンクが必須です。
</p>
</tldr>

上流のエンジンを追うフォークには、さまざまな出所からの長い変更の履歴が蓄積します。その履歴を眺めて、最適化、
レンダリングの機能、バックポートを区別できることが、将来のマージを扱えるものにします。

## プレフィックス

コミットの件名の先頭に、次のいずれかを付けます。

| プレフィックス | 用途 |
|---|---|
| `[Rendering]` | レンダラーの作業全般。ツリーで最も多く使われるタグ |
| `[Rendering Feature]` | 特にレンダリングの機能の追加や変更 |
| `[RT]` | レイトレーシング |
| `[Forward]` | フォワードレンダラーの経路 |
| `[Optimization]` | 挙動を変えない性能の作業 |
| `[Backport]` | 後のエンジンバージョンから取り込んだ変更 |
| `[Animation]` | アニメーションのシステム |
| `[GameplayFramework]` | カメラ、キャラクタームーブメント、AI などのゲームプレイフレームワーク |
| `[Memory]` | UObject のメモリのサブシステム |
| `[DOP]` | ECS を含むデータ指向の作業 |
| `[PhysX]` | 物理 |
| `[Plugin]` | プラグインの追加、更新、削除 |
| `[Lib]` | サードパーティのライブラリの更新 |
| `[Toolchain]` | コンパイラ、SDK、ビルド環境 |
| `[Defaults]` | 出荷するエンジンの既定値の変更 |
| `[Debloat]` | 既定のビルドからコストを取り除く、またはゲートする |
| `[Mobile]` | モバイル固有の作業 |
| `[VR]` | VR 固有の作業 |
| `[AMD]` | AMD 固有の作業 |
| `[NVIDIA]` | NVIDIA 固有の作業 |
| `[Fix]` | 不具合の修正 |

### プレフィックスを重ねる

自明でない変更の多くは、複数のタグを持ちます。広いものから具体的なものの順に並べ、変更の出所が最後に読めるように
バックポートの印は最後に置きます。

```
[Rendering][RT][Optimization][Adapted Backport 5.3] Exclude raygen shaders from RTPSOs
unless the corresponding feature is enabled
[Rendering][Forward][Backport 5.6] Fix incorrect alpha from MSAA resolve with explicit fmask
[Rendering][Shading Models] Remove unnecessary branch for the Toon shading model
```

`Backport` ではなく `Adapted Backport` とするのは、上流の変更がそのままでは適用できず、Vite のコードベースに合わせて
書き直したことを示すためです。後で、元のコミットに対する上流の修正がここにも当てはまるかを調べるときに、この区別が
重要になります。

変更が本当に 1 つのことなら、タグが 1 つのコミットでも問題ありません。

```
[Toolchain] Compiling on VS 18.8.2 (_MSC_VER 1950) and Windows SDK 10.0.26100
[Plugin] PhysX Blast + engine-side changes for proper support
[Gating] RT translucency guard
[Fix] Guard RTXDI CVar behind ShouldRenderRayTracingSampledLighting
```

変更が本当に無関係な領域にまたがる場合は、表のタグをすべて 1 つのコミットに重ねるのではなく、分割してください。

## 出典の明記

<warning>
バックポートやプラグインの追加では、コミットの本文に元のコミットやリポジトリへの正しいリンクを含めてください。
</warning>

これは礼儀ではなく、実際上の要件です。リンクがなければ、どのバージョンを統合したのか、その後上流で不具合が修正されたか、
ライセンスが再配布を認めているかを、誰も判断できません。

```
[Plugin] Add Kawaii Physics 1.18.0, backported from UE5

Source: https://github.com/pafuhana1213/KawaiiPhysics
Upstream tag: v1.18.0
Changes: UE5 API calls replaced with 4.27 equivalents in
KawaiiPhysicsEditMode.cpp and AnimNode_KawaiiPhysics.cpp
```

上流の個々のコミットのバックポートでは、リポジトリだけでなくコミットそのものにリンクしてください。
[バックポート](Backporting.md) を参照してください。

## コミットの本文

件名は何が変わったかを伝えます。本文は、なぜ変えたのか、そしてレビュアーが知るべきことを伝えます。

- その変更がどの問題を解決するか
- 最適化を主張するものなら、計測した効果
- 追加したコンソール変数や [コンパイル時スイッチ](Compile-Time-Switches.md) と、その既定値
- 意図的にやり残したこと

計測した効果は重要です。数値のない `[Optimization]` のコミットは、結果ではなく主張にすぎません。説得力のある変更前と
変更後の比較の作り方は [プロファイリング](Profiling.md) を参照してください。

## ブランチ

| ルール | |
|---|---|
| 作業途中のものは別のブランチに置く | 未完成の作業を共有のブランチにプッシュしない |
| 残っている作業を記す | ブランチかコミットの本文に簡単なコメントを残す |
| 一時的なブランチは削除する | マージしたとき、または放棄したとき |
| 他のフォークの作業者に知らせる | 並行した作業が無駄にならないように |

## コンソール変数とスイッチ

新しいコンソール変数は、エンジンの既存の命名に従います。Vite 固有のものは、サブシステムの後に `Vite` を付けます。

| 例 | サブシステム |
|---|---|
| `r.Vite.SSAO` | レンダラー |
| `p.VitePhysXFixedTimestep.Enabled` | 物理 |

コンパイル時スイッチには `VITE_` のプレフィックスを使い、`Engine\Source\Runtime\Core\Public\Misc\CoreDefines.h` で既定値と
ともに定義しなければなりません。

```c++
#ifndef VITE_MY_FEATURE
	#define VITE_MY_FEATURE 0
#endif
```

新しいスイッチは、同じ変更の中で [コンパイル時スイッチ](Compile-Time-Switches.md) に記載してください。記載されていない
スイッチは、何も通知せずに何もしないコンソール変数をデバッグしている誰かによって発見されることになります。それこそが、
記載される前の `VITE_RT_PSO_DEBLOAT` が引き起こした問題です。

## 関連項目

- [コントリビュート](Contributing.md)
- [コーディングガイドライン](Coding-Guidelines.md)
- [バックポート](Backporting.md)
- [コンパイル時スイッチ](Compile-Time-Switches.md)
