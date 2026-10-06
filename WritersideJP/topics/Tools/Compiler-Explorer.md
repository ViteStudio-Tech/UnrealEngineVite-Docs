# Compiler Explorer

<tldr>
<p>
<a href="https://gcc.godbolt.org/">Compiler Explorer</a> は、自己完結した C++ のコード片をコンパイルし、MSVC と Clang が出力するアセンブリを表示します。Clang 22 への準拠とコード生成の確認に使ってください。実行時間は <b>計測しません</b>。計測には <a href="https://quick-bench.com/">Quick Bench</a>（Linux 上の GCC または Clang）を使います。MSVC と clang-cl の比較は、今も自分のマシンで計測する必要があります。
</p>
</tldr>

Vite は、[MSVC と Clang](Coding-Guidelines.md) の両方で明確に定義されたコードを求めます。Compiler Explorer は、エンジンをフルビルドせずに同じカーネルを両方のコンパイラにかける最も早い方法です。プロファイラーではなく、実際のコンテンツでの
[stat unit](Profiling.md) の代わりにもなりません。

公開インスタンスは [https://gcc.godbolt.org/](https://gcc.godbolt.org/)（[godbolt.org](https://godbolt.org/) でも同じ）です。どちらも同じサイトです。

## 用途

| 問い | Compiler Explorer |
|---|---|
| このコード片は MSVC と Clang 22 で C++ としてコンパイルできるか | できる |
| `/O2` / `-O2` でどんなアセンブリが生成されるか | わかる |
| MSVC がスカラーのままにしたループを Clang はベクトル化したか、またはその逆か | わかる |
| MSVC と Clang でそれぞれ何ナノ秒かかるか | **わからない** |

カーネルを切り出してください。Unreal のヘッダー、`FORCEINLINE`、`TArray` などのエンジンの要素はサイト上では解決できません。ホットな関数を標準の C++ に書き直し、コンパイラが見ているのがインクルードの欠落ではなくアルゴリズムであるようにしてください。

## セッションを開く

<procedure title="Compiler Explorer でコード片を比較する" id="open-compiler-explorer">
    <step>
        <a href="https://gcc.godbolt.org/">https://gcc.godbolt.org/</a> を開きます。言語のドロップダウンを
        <b>C++</b> にします。
    </step>
    <step>
        自己完結した関数を貼り付けます。<code>main</code> は、後で <b>Execute the code</b> にチェックを入れる場合にだけ必要です。
    </step>
    <step>
        コンパイラのペインで最新の <b>x64 msvc</b> を選びます。コンパイラのオプションを
        <code>/O2 /std:c++17</code> にします。
    </step>
    <step>
        <b>Add new&hellip;</b> &rarr; <b>Compiler</b> で <b>clang-cl</b> 22（または <b>x86-64 clang</b> 22）を追加します。clang-cl では同じ MSVC 形式のフラグ（<code>/O2 /std:c++17</code>）を、Linux の clang では
        <code>-O2 -std=c++17</code> を使います。
    </step>
    <step>
        Clang のペインで <b>Intel asm syntax</b> を有効にし、両方で Intel の表記を使うようにします。MSVC は最初からそうなっています。<b>Unused labels</b> と <b>Directives</b> を除外して、ノイズを取り除きます。
    </step>
    <step>
        両方のペインがコンパイルできたら、アドレスバーの URL でセッションを共有します。レビューに貼るべきなのはそのリンクであり、片方のコンパイラのスクリーンショットではありません。
    </step>
</procedure>

Vite の Windows の Clang により近いのは clang-cl です。Linux の `x86-64 clang` も標準への準拠の確認には役立ちますが、Unreal Build Tool が Windows で使う ABI やオブジェクト形式ではありません。

貼り付けられる程度の小さなコード片の例:

```c++
float clampf(float x, float lo, float hi) {
    const float y = x < lo ? lo : x;
    return y > hi ? hi : y;
}
```

関数が使われていないと、コンパイラによっては何も出力しません。同じエディタ内の別の関数から呼ぶか、シンボルを生かしたまま `/O2` でコンパイルしてください（`clampf(x, 0.f, 1.f)` を返す 2 つ目の関数があれば十分です）。

## フラグをそろえる

同じ条件で比較してください。Release の MSVC のペインと最適化なしの Clang のペインを比べても、コンパイラの比較にはなりません。

| | MSVC / clang-cl | Linux の clang / GCC |
|---|---|---|
| 最適化 | `/O2` | `-O2` |
| 言語 | `/std:c++17` | `-std=c++17` |
| 高速な浮動小数点 / FMA（任意） | `/fp:fast` | `-ffast-math` または `-ffp-contract=on` |

MSVC の `/O2` は通常の Release の設定です。Clang の `-O3` はそれより積極的です。使う場合は、共有するリンクでそのことを明記してください。Vite が [PS5 クラスの Zen 2](PS5-CPU-FPU.md) で重視する FPU に依存するカーネルでは、アセンブリに現れる違いは C++ のソースではなく、`/fp:fast` と縮約された FMA の違いであることがよくあります。

## アセンブリから読み取ること

行数ではなく、制御フロー、スピル、ベクトル化の違いを見てください。

- 一覧が短いからといって、関数が速いわけではありません。MSVC と Clang はアセンブリの書式が異なります。
- `cmov` / `blend` と分岐の違いは、実際のコード生成の違いです。どちらが速いかは、対象の CPU で分岐がどれだけ予測しやすいかによります。
- 一方のコンパイラでは自動ベクトル化（`movaps`、`vfmadd`、`ymm`）され、もう一方ではスカラーのループになっている、という結果は、エンジンに持ち帰る価値のあるものです。
- ペインに表示されるコンパイル時間は、Godbolt のマシンがコード片をコンパイルするのにかかった時間です。エンジンのビルド時間でも実行時間でもありません。

**llvm-mca** のツール（Clang/LLVM のペインで Add tool）は、アセンブリからポートの負荷を見積もります。これは一覧の静的な解析であり、コンパイルしたバイナリを実行した計測ではありません。また、MSVC のオブジェクトコードに対しては実行されません。

## 実行時の性能: ここでは測れない

<warning>
Compiler Explorer は MSVC と Clang のベンチマークを行いません。<b>Execute the code</b> は、共有の VM でプログラムを実行してその出力を表示するためのものです。その環境での <code>chrono</code> のループは結果とは言えません。ウォームアップも統計的な枠組みもなく、他の利用者の影響があり、多くの場合 Vite が出荷する OS とも異なります。
</warning>

Compiler Explorer は、*何を* 計測するかを決めるために使ってください。計測は、実際にバイナリを実行する場所で行います。

## Quick Bench

コンパイラが Linux 上の GCC または Clang の場合、そのためのサイトが [Quick Bench](https://quick-bench.com/) です。[Google Benchmark](https://github.com/google/benchmark) を包み、登録した関数を繰り返し実行して、何もしない基準に対する
CPU 時間をグラフにします。

<procedure title="Quick Bench でカーネルを計測する" id="run-quick-bench">
    <step><a href="https://quick-bench.com/">https://quick-bench.com/</a> を開きます。</step>
    <step>
        それぞれの版を個別の <code>BENCHMARK</code> 関数に入れます。準備は計測するループの外に置き、
        <code>benchmark::DoNotOptimize</code> を使ってコンパイラが処理を削除できないようにします。
    </step>
    <step>
        <b>compiler</b> を最新の Clang か GCC に、<b>std</b> を C++17 に、<b>optim</b> を <code>O3</code>（Vite のフラグに合わせる場合は <code>O2</code>）にします。
    </step>
    <step>Run Benchmark を実行します。グラフは、<b>その 1 つのコンパイラ</b> で登録した関数どうしを比較します。</step>
    <step>
        GCC と Clang を比べるには、コンパイラのドロップダウンを変えてもう一度実行します。Quick Bench は 2 つのコンパイラを 1 つのグラフに並べません。
    </step>
</procedure>

Godbolt の UI 自体にも Quick Bench へのリンクがあります（CppInsights の隣の **Quick-bench** の操作）。これは同じコード片を
Google Benchmark の形式で渡すためのもので、MSVC が加わるわけではありません。

<note>
Quick Bench には MSVC がありません。libstdc++ または libc++ を使って、Linux 上で GCC と Clang を実行します。Clang が GCC に勝つグラフは MSVC と clang-cl の比較ではなく、PS5 や Windows の結果でもありません。
<a href="Performance-Targets.md">パフォーマンス目標</a> を参照してください。
</note>

## 自分のマシンでの MSVC と clang-cl の比較

これこそ Vite が実際に出荷するものの比較です。Godbolt も Quick Bench もこれは出せません。

1. 両方のツールチェーンでコンパイルできる、小さな Google Benchmark（または専用のテスト用バイナリ）にカーネルを切り出します。
2. それを 2 回ビルドします。MSVC 14.50 の Release と clang-cl 22 の Release で、`/O2` と浮動小数点のフラグをそろえます。
3. 他の処理を止め、コアを固定して、同じマシンで両方のバイナリを実行します。PhysX のような FPU に依存するカーネルでは、デスクトップの Zen 2 より [4700S / PS5 クラスの FPU](PS5-CPU-FPU.md) を優先してください。
4. エンジンレベルの問いは、10 行のコード片のマイクロベンチマークとしてではなく、[プロファイリング](Profiling.md) の問題（`stat unit`、Unreal Insights）として扱ってください。

Godbolt でのコード生成の改善がフレームのキャプチャに現れないなら、それは出荷の根拠にすべき改善ではありません。

## 関連項目

- [コーディングガイドライン](Coding-Guidelines.md)
- [ツールチェーン要件](Toolchain-Requirements.md)
- [プロファイリング](Profiling.md)
- [PS5 CPU の FPU](PS5-CPU-FPU.md)
- [パフォーマンス目標](Performance-Targets.md)
- [コントリビュート](Contributing.md)
