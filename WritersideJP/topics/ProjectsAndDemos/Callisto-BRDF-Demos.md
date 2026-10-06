# Callisto BRDF デモ

<tldr>
<p>
Vite 独自の Callisto BRDF のシェーディングモデルを示す 2 つのキャラクターのシーンです。このモデルは、標準のマテリアルの
ピンを流用して、再帰反射、ディフューズのフレネル、ターミネーターを制御します。
</p>
</tldr>

## ダウンロード

| デモ | リンク |
|---|---|
| 男性キャラクター | [ダウンロード](https://drive.google.com/file/d/133RwxvHT9jELgXWn338hieiAJUUeIoVq/view?usp=sharing) |
| 女性キャラクター | [ダウンロード](https://mega.nz/file/5I1STApA#zmKqFu_8X1bYZPakb2VvAbCF-GPQhmR98Iot3QVJtRM) |

<img src="CallistoMale.png" alt="Callisto BRDF のシェーディングモデルで描画した男性キャラクター" border-effect="line"/>

*男性のデモキャラクター。かすめる角度では、再帰反射とディフューズのフレネルが効いています。*

<img src="CallistoFemale.png" alt="Callisto BRDF のシェーディングモデルで描画した女性キャラクター" border-effect="line"/>

*女性のデモキャラクター。Smooth Terminator が、顔と腕の曲面にかかる影の境界を和らげています。*

## Callisto BRDF の役割

Unreal の既定の Lit モデルは汎用の BRDF としては優れていますが、肌やキャラクターのモデルとしては平凡です。Callisto BRDF は
Vite が追加したもので、新しいピンを加えるのではなく既存のマテリアルのピンを流用して、キャラクターの描画で重要な項を直接
制御できるようにします。

| 標準のピン | 置き換わる役割 |
|---|---|
| Opacity | Retroreflection |
| Anisotropy | Diffuse Fresnel |
| Custom Data 0 | Smooth Terminator |
| Custom Data 1 | Diffuse Fresnel Falloff |
| Ambient Occlusion | Retroreflection Falloff |

まず見るべきは Smooth Terminator です。曲面上の硬いシャドウのターミネーターは、リアルタイムのキャラクターであることが最も
よく分かる特徴の 1 つで、それを直接制御するほうが、ノーマルマップやライティングの工夫で回避するより安価で予測しやすく
なります。

ピンの完全な一覧と作成時の注意点は [シェーディングモデル](Shading-Models.md) にあります。

## デモの使い方

キャラクターのマテリアルを開き、ピンを 1 つずつ変えてみてください。流用したピンは互いに影響し合うため、出荷時の組み合わせ
よりも、1 つずつ切り離したほうが効果がはるかに分かりやすくなります。

かすめる光に対するモデルの反応に注目してください。再帰反射とディフューズのフレネルはどちらもそこで最も強く働き、既定の
Lit モデルとの違いが最もよく見える場所です。

## 設定を移植する

これらのデモで役に立つのはマテリアルのグラフです。Callisto BRDF はシェーディングモデルの選択なので、採用するにはモデルを
切り替えて、影響するピンをつなぎ直すだけで、有効にするプラグインはありません。[July Major](ueVite26-JulyMajor.md) 以降、
このモデルは既定でコンパイル対象から外れているため、先にエンジンを `VITE_SHADINGMODEL_CALLISTO=1` でビルドしてください。
[コンパイル時スイッチ](Compile-Time-Switches.md) を参照してください。

<note>
使用するシェーディングモデルが増えるごとに、シェーダーのパーミュテーションが増えます。Callisto がキャラクターにだけ必要
なら、キャラクターにだけ使ってください。<a href="Shader-Compilation-And-PSO.md">シェーダーコンパイルと PSO</a>
を参照してください。
</note>

## 関連項目

- [シェーディングモデル](Shading-Models.md)
- [カラーマネジメント](Color-Management.md)
- [ヘアレンダリング](Hair-Rendering.md)
