# PS5 CPU の FPU

<tldr>
<p>
PS5 の Zen 2 は <code>FP3</code> を削除し、<code>FP2</code> をストア専用のポートにして、<b>256 ビットの FMA パイプを
1 本だけ</b> 残しています。AVX2 と FMA のレイテンシーはそのままです。Series X の Zen 2 にはこの削減はありません。Vite は FPU に依存する処理、とりわけ <b>PhysX 3.4</b> の近代化を <b>AMD 4700S</b> で検証します。その CPU は、デスクトップの
Matisse の FPU でも Series X でもない、さらに削減された Zen 2 です。
</p>
</tldr>

4700S はラボに GPU ではなく CPU のために置かれています。その Zen 2 は、Series X の Zen 2 に比べてさらに削減された FPU
です。実際の用途は、PhysX 3.4 のライブラリにおける FPU 側の変更が PS5 クラスのコアでどう振る舞うかを確認することです。アイランドの解決、コンタクトの生成、コンストレイントの準備、積分は FMA のスループットに依存する処理であり、Vite が近代化を進めているのはまさにその負荷です。

デスクトップの Ryzen 3000 の FPU では、その処理を過大評価してしまいます。Series X でも過大評価になります。4700S ならそうはなりません。

## Series X が CPU の代替として不適切な理由

Scarlett（Series X）は **153 億** トランジスター、Oberon（PS5）は **106 億** トランジスターです。トランジスター数で約
**1.4 倍** で、よく 50% 多いと丸められます。追加のシリコンは大きな GPU（52 CU 対 36 CU）だけではありません。Series X は
CPU にもより多くのトランジスターを使っており、その中にはより完全な Zen 2 の FPU が含まれます。

PS5 の Zen 2 は、Matisse の整数、ロード／ストア、アウトオブオーダーの部分をほぼ標準のまま残し、FPU で面積を節約しています。

| ポート | デスクトップの Zen 2 / Series X クラス | PS5 / 4700S クラス |
|---|---|---|
| `FP0` | 256 ビットの FMA / FMUL | **256 ビットの FMA / FMUL（残された FMA パイプ）** |
| `FP1` | 256 ビットの FMA / FMUL | FMA 以外の浮動小数点演算（FADD など） |
| `FP2` | FADD + ベクトルストア | **ベクトルストアのみ** |
| `FP3` | FADD | **削除** |
| AVX2 | 256 ビット | 256 ビット（AVX を 2 ビートで実行する 128 ビットの FPU ではない） |
| FMA のレイテンシー | 約 5 サイクル | 約 5 サイクル |
| 浮動小数点の物理レジスタファイル | 160 × 256 ビット | 160 × 256 ビット |

同じクロックの Matisse コアと比べた定常状態の発行数:

| 演算 | デスクトップの Zen 2 | PS5 / 4700S |
|---|---|---|
| パックド FMA（`vfmadd` / `a*b+c`） | **256 ビット × 2 / サイクル** | **256 ビット × 1 / サイクル** |
| 個別の演算としてのパックド FADD / FMUL | それぞれ 256 ビット × 2 / サイクル | それぞれ 256 ビット × 1 / サイクル |
| ベクトルストア | 浮動小数点クラスターを共有 | 引き続き `FP2` 上。FMA パイプを奪わない |
| パックド整数の MUL | 1 パイプ | 変化なし |
| パックド整数の ADD | 3 パイプ | 約 2 パイプ |

独立した FMA は、Series X と 3700X では 2 つ同時に発行されます。PS5 と 4700S では **1 本のパイプに並びます**。FMA と
FADD を組み合わせても、`FP2`/`FP3` で隠すことはもうできません。2 つのアキュムレーターで 5 サイクルの FMA のレイテンシーは引き続き隠せますが、2 本目の FMA ユニットが戻るわけではありません。

<warning>
PhysX をはじめとする FPU に依存するカーネルの計測は 4700S で行ってください。3700X、5800X3D、13700K、または Series X のシリコンは、PS5 のコアにはできない FMA の 2 命令同時発行を行います。それらのチップは「コンパイラの出力が悪化したか」を確認する目的にだけ使ってください。
</warning>

## テスト機とそれぞれの用途

| マシン | 役割 | 向かない用途 |
|---|---|---|
| **AMD 4700S** | Windows + PS5 クラスの CPU の FPU。PhysX 3.4、アニメーションの SIMD、オーディオ。 | GPU。内蔵 GPU は無効化されています。 |
| **AMD 4800S** | Xbox Series X の APU をベースにし、GPU は無効化。Series X の CPU の代替であり、コンソールのクロックでの完全な FPU との比較用。 | PS5 の FPU の数値、および GPU。どちらの FPU のクラスとして扱う前にも、下の FMA のプローブを実行してください。 |
| **RX 6700 RDNA2** | デスクトップの RDNA2 のコンパイラとスループットの代替。シェーダーコンパイラの挙動を捉えるのに十分なほど、性能とアーキテクチャが近い。 | サイクル単位で正確な PS5 の GPU。PS5 の RDNA2 は異なる点があります（キャッシュ、RB+、エクスポート、プリミティブシェーダー、RT の ISA）。そのため、6700 のキャプチャをコンソールの GPU としてどこまで信頼できるかには限界があります。 |
| **AMD BC-250** | Oberon クラスの選別品の APU。FPU は同じ系統で、GPU は **動作します**。 | Vite の Windows / D3D12 の経路。使える Windows 用の GPU ドライバーがないため、エディタや Shipping の実用的なテスト機にはなりません。 |

BC-250 は、公開されたマイクロベンチマーク（特に [Chips and Cheese](https://chipsandcheese.com/p/the-nerfed-fpu-in-ps5s-zen-2-cores)）が
PS5 の FPU を解明するのに使ったものです。Vite のエディタは動かせません。4700S なら、ディスクリート GPU に RHI を任せたうえで、削減された FPU で Vite のエディタを動かせます。

<note>
コンソールのプラットフォームのコードは非公開のままです。このページは移植可能な SIMD、PhysX 3.4、そして Windows 上の
CPU の代替について説明するもので、PS5 の SDK のドキュメントではありません。<a href="Platforms.md">対応プラットフォーム</a>
を参照してください。
</note>

## FPU の負荷は PhysX 3.4

Vite は、PS5 の CPU を最適化の目標として、**PhysX 3.4** のライブラリを近代化しています（新しい Clang/MSVC、FMA への縮約、バッチ化した浮動小数点カーネル）。この SDK は `physx::shdfnd::aos`（`Vec3V`、`FloatV`、`V3ScaleAdd`、`V3MulAdd`）で
`float` を扱う SSE2/SSE4 です。ナローフェーズ、コンストレイントの準備、PGS ソルバー、積分はパックド FMA です。まさに
2 本目の FMA パイプを失うカーネルです。

Chaos の ISPC の AVX2 の経路は、このコアが持つより多くの FPU の発行帯域を前提としています。この作業の参考としては不適切です。ステップ全体での占有率は、実行されることのない見事なカーネルに今も勝ります（[物理](Physics.md) を参照）。しかし、SDK の書き直しが達成すべき予算は、残された 1 本の FMA パイプです。

書き直しのルール:

1. **縮小したのは発行数に制約されるパックド FMA です。** 3700X が 2 つ同時に発行する独立した `V3ScaleAdd` / `fmadd` は、今は 1 本のパイプを待ちます。独立したアイランドとコンタクトのバッチを維持し、1 つの依存チェーンの中で 1 サイクルに
   2 FMA を期待しないでください。
2. **乗算と加算を FMA に縮約します。** `V3ScaleAdd(a, s, b)`（`a * s + b`）は 1 uop です。`V3Scale` の後に `V3Add` では
   2 uop になり、残った演算ポートを奪い合います。デスクトップでは加算を `FP2`/`FP3` で隠せましたが、PS5 では隠せません。
3. **SoA / `Vec3V` のバッチと、アラインされたロード。** 内側のループでスカラーの `PxVec3` を使うと、挿入とスカラーのストアに発行枠を使ってしまいます。`FP2` は引き続きベクトルストアを完了できるので、活用してください。
4. **AVX2 は使ってよいが、2 本目の FMA は戻らない。** 256 ビットの FMA は SSE に比べて 1 命令あたりの浮動小数点数を
   2 倍にしますが、完了は 1 サイクルに 1 つのままです。古い「128 ビットの FPU」という噂を理由に AVX2 をやめないでください。Matisse はパイプの少ない 256 ビットの FPU であり、256 ビットと 128 ビットのベクトルの浮動小数点演算は
   Matisse に比べてほぼ同じ割合で低下します。
5. **AVX-512 を生成しない。** 存在しません。ホットな翻訳単位は `/arch:AVX2` または `-mavx2 -mfma` にします。カーネルが明示的に AVX2 でない限り、Unreal の `VectorRegister` は SSE のままにしてください。
6. **FP32 を維持する。** ソルバー、コンタクト、積分は `float` です。FP64 は SIMD の占有率をさらに半分にします。LWC の
   double はこの経路に入れるべきではありません。
7. **SMT を有効にして 4700S で検証する**（PS5 は SMT 有効で出荷されています）。比率は、クロックをそろえた
   `time_4700S / time_3700X` です。1.0 に近づけば FMA のトラフィックを減らせています。2 倍近くで止まっていれば、デスクトップの追加の FMA パイプが吸収していた ILP を増やしただけです。

### プローブ: FMA パイプが 1 本であることを確認する

独立した `_mm256_fmadd_ps` は、同じクロックで 4700S では **約 1 サイクル/uop**、デスクトップの Zen 2 では
**約 0.5 サイクル/uop** になるはずです。依存チェーン（同じアキュムレーター）では、**どちらも約 5 サイクル/uop** になるはずです。「改善」が依存チェーンのテストにしか現れない場合、隠したのはレイテンシーであり、PS5 の FPU のスループットを取り戻したわけではありません。

```cpp
#include <immintrin.h>
#include <stdint.h>

#if defined(_MSC_VER)
#include <intrin.h>
static uint64_t Ticks() { return __rdtsc(); }
#else
static uint64_t Ticks()
{
	uint32_t Lo, Hi;
	__asm__ volatile("rdtsc" : "=a"(Lo), "=d"(Hi));
	return (uint64_t(Hi) << 32) | Lo;
}
#endif

float ProbeFmaThroughput(uint32_t Iters)
{
	__m256 A = _mm256_set1_ps(1.0001f);
	__m256 B = _mm256_set1_ps(1.0002f);
	__m256 Acc0 = _mm256_set1_ps(1.0f);
	__m256 Acc1 = _mm256_set1_ps(1.0f);
	__m256 Acc2 = _mm256_set1_ps(1.0f);
	__m256 Acc3 = _mm256_set1_ps(1.0f);

	const uint64_t T0 = Ticks();
	for (uint32_t I = 0; I < Iters; ++I)
	{
		Acc0 = _mm256_fmadd_ps(Acc0, A, B);
		Acc1 = _mm256_fmadd_ps(Acc1, A, B);
		Acc2 = _mm256_fmadd_ps(Acc2, A, B);
		Acc3 = _mm256_fmadd_ps(Acc3, A, B);
	}
	const uint64_t Dt = Ticks() - T0;

	Acc0 = _mm256_add_ps(Acc0, Acc1);
	Acc0 = _mm256_add_ps(Acc0, Acc2);
	Acc0 = _mm256_add_ps(Acc0, Acc3);
	alignas(32) float Out[8];
	_mm256_store_ps(Out, Acc0);

	(void)Out;
	return float(Dt) / float(Iters * 4u); // 4700S で約 1.0、Matisse で約 0.5
}
```

この翻訳単位は `/arch:AVX2` または `-mavx2 -mfma` でコンパイルしてください。

### ソルバー型の FMA: スケールしてから加算ではなく `V3ScaleAdd`

PhysX 3.4 にはすでに融合した形があります。それを使ってください。バッチ化した法線方向のインパルスに対する PGS の差分は、レーンごとに 1 つの FMA です。分割すると、4700S に予備のないパイプを無駄にします。

```cpp
#include "PsVecMath.h"
using namespace physx::shdfnd::aos;

// deltaV = deltaV + n * (impulse * invMass)   — V3Scale + V3Add ではなく FMA 1 つ
inline void ApplyNormalImpulse(
	Vec3V& DeltaLin,
	const Vec3V N,
	const FloatV Impulse,
	const FloatV InvMass)
{
	const FloatV S = FMul(Impulse, InvMass);
	DeltaLin = V3ScaleAdd(N, S, DeltaLin);
}

// この FPU では悪い例: 演算の uop が 2 つになり、FADD を FP2/FP3 で隠せない
inline void ApplyNormalImpulseSplit(
	Vec3V& DeltaLin,
	const Vec3V N,
	const FloatV Impulse,
	const FloatV InvMass)
{
	const Vec3V Tmp = V3Scale(N, FMul(Impulse, InvMass));
	DeltaLin = V3Add(DeltaLin, Tmp);
}
```

積分も同じです。`x += v * dt` はスカラーの `PxVec3` のループではなく `V3ScaleAdd` です。ベクトルストアは引き続き `FP2` が受け持ちます。

```cpp
void IntegrateLinearSoA(
	PxF32* RESTRICT Px, PxF32* RESTRICT Py, PxF32* RESTRICT Pz,
	const PxF32* RESTRICT Vx, const PxF32* RESTRICT Vy, const PxF32* RESTRICT Vz,
	PxF32 Dt,
	PxU32 Count)
{
	const FloatV VDt = FLoad(Dt);
	const PxU32 Padded = Count & ~3u;
	PxU32 I = 0;

	for (; I < Padded; I += 4)
	{
		Vec3V P = V3LoadA(Px + I); // SoA: 4 つのボディの X を読み込む。実際のコードでは Y/Z も同様
		Vec3V V = V3LoadA(Vx + I);
		P = V3ScaleAdd(V, VDt, P);
		V3StoreA(P, Px + I);
		(void)Py; (void)Pz; (void)Vy; (void)Vz;
	}

	for (; I < Count; ++I)
	{
		Px[I] += Vx[I] * Dt;
		Py[I] += Vy[I] * Dt;
		Pz[I] += Vz[I] * Dt;
	}
}
```

上の SoA の例は 1 回の呼び出しで 1 つの成分を読み込みます。実際のカーネルは 3 つの `Vec3V` のレーン、または 4 つのボディの AoSoA ブロックを使います。重要なのは FMA とアラインされたベクトルストアであり、簡略化したレイアウトではありません。

### SDK のホットパスに入れてはいけないもの

```cpp
// ソルバーの内側のループでのスカラーの PxVec3 — 挿入／抽出とスカラーのストア
for (PxU32 I = 0; I < Count; ++I)
{
	PxVec3 V = Bodies[I].linearVelocity;
	V.z += gravityZ * dt;
	Bodies[I].linearVelocity = V;
}

// V3ScaleAdd があるのに乗算と加算を分ける
Vec3V Tmp = V3Scale(N, Impulse);
Delta = V3Add(Delta, Tmp);

// ボディごとのカーネルでの FP64
PxF64 X = PxF64(p.x) + PxF64(v.x) * dt;

// AVX2 で Series X / Matisse の FMA 2 本が戻ると想定する
// 独立した Acc0 と Acc1 の fmadd — デスクトップ/SX: 2/サイクル、PS5/4700S: 1/サイクル
```

## 4700S で PhysX の FPU の作業をテストする方法

<procedure title="PhysX 3.4 の FPU の変更を PS5 の CPU に対して検証する" id="fpu-4700s-physx">
    <step>
        コード生成全体に影響する変更はガードします。
        <a href="Compile-Time-Switches.md">コンパイル時スイッチ</a> を参照してください。
    </step>
    <step>
        近代化した PhysX 3.4 のライブラリと、エンジンの Test/Shipping ターゲットを、4700S とデスクトップの Zen 2 のマシンで同じ ISA のフラグでビルドします（カーネルの翻訳単位には <code>/arch:AVX2</code> または
        <code>-mavx2 -mfma</code>）。
    </step>
    <step>
        FMA のプローブを実行します。マシンを信頼する前に、4700S で独立した FMA が約 1 サイクルであることを確認します。
    </step>
    <step>
        実際の SDK の経路を計測します。<code>stat physics</code>、アイランド／コンタクト／ソルバーの内訳、ETW です。13700K の Insights のキャプチャを PS5 の数値として使わないでください。
    </step>
    <step>
        クロックをそろえ、SMT を有効にした状態の <code>time_4700S / time_3700X</code> を報告します。1.0 に近づけば FMA のトラフィックが減っています。2 倍近くで止まっていれば、デスクトップの 2 本目の FMA パイプだけが吸収していた ILP を増やしただけです。
    </step>
    <step>
        RX 6700 で GPU がボトルネックの状態でシーンを再実行します。フレームの時間が変わらなければ、そのシーンは CPU の
        FPU がボトルネックではありませんでした。SDK の変更は、4700S の物理のキャプチャがまだそれを必要とする場合にだけ残してください。
    </step>
</procedure>

キットがブーストする場合はクロックを固定してください。8 コア 16 スレッドの 4700S の数値を 16 コアのデスクトップと比べて、それを FPU の比較と呼ばないでください。

## GPU のテストは 6700 で

4700S と 4800S では GPU のコンパイラに関する問いには答えられません。GPU は完全に無効化されています。

RX 6700 は性能とアーキテクチャが PS5 の RDNA2 に近く、**GPU のコンパイラの挙動** を調べるには十分です。それでも
PS5 の RDNA2 は PC の RDNA2 と異なります（キャッシュ階層、RB+、エクスポートの経路、プリミティブシェーダー、RT の交差判定の
ISA、ラストレベルキャッシュ）。こうした違いにより、6700 のトレースがコンソールの GPU の代わりになれる範囲には限界があります。

BC-250 の GPU は Oberon クラスのシリコンで動作しますが、Windows の D3D12 では使えません。そのため Vite のエディタや
Shipping の実用的なテストができません。GPU の検証をこれに頼る計画は立てないでください。

## 関連項目

- [PhysX](PhysX.md)
- [物理](Physics.md)
- [動作環境](System-Requirements.md)
- [パフォーマンス目標](Performance-Targets.md)
- [プロファイリング](Profiling.md)
- [コーディングガイドライン](Coding-Guidelines.md)
- [対応プラットフォーム](Platforms.md)
