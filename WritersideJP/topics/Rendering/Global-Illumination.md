# グローバルイルミネーション

<tldr>
<p>
Vite が推奨する GI の構成は <b>動的 DDGI と SSGI の併用</b> です。DDGI はワールド規模のバウンスをノイズなしで解決し、
SSGI はプローブボリュームでは粗すぎて捉えられない高周波の接触ディテールを補います。DDGI は既定で有効です
（<code>r.GlobalIllumination.ExperimentalPlugin 1</code>）。<code>r.SSGI.Enable 1</code> を追加してください。
</p>
</tldr>

<img src="StylizedRTDemo.png" alt="動的 DDGI でライティングされたスタイライズドシーン。フレームカウンターは 811 FPS を示している" border-effect="line"/>

*811 FPS、RTX 4080 Super、1440p ネイティブ、動的 DDGI。同じシーンを 5.7 の Lumen で描画すると 324 FPS です。*

グローバルイルミネーションは、Vite が独立したフォークとして存在する最大の理由です。このページでは選択肢とその選び方を
説明します。個々の手法にはそれぞれ専用のページがあります。

## 選択肢

| ソリューション | コスト | DXR が必要 | 動的ライティング | 適した用途 |
|---|---|---|---|---|
| [動的 DDGI](DDGI-Dynamic.md) | 低 | はい | 完全に動的 | ほぼすべて |
| [静的 DDGI](DDGI-Static.md) | 実行時はほぼゼロ | いいえ | ベイク | ローエンドと DXR 非対応のハードウェア |
| [SSGI](SSGI.md) | 低 | いいえ | 完全に動的 | 高周波のディテール。DDGI と併用する前提 |
| [ピクセル単位の RT GI](Ray-Tracing.md) | 高 | はい | 完全に動的 | PS5 より大幅に速い GPU、リファレンス画像 |
| [パストレーシング](Path-Tracing.md) | 非常に高 | はい | 完全に動的 | RTX 5080 以上、真値のリファレンス |
| ベイクしたライトマップ | 実行時はゼロ | いいえ | 静的のみ | 完全に静的なシーン。最高品質には CPU 版 Lightmass を使用 |

<note>
Vite には、距離フィールドによるバウンスや Vite 独自のローカライズド IBL キャプチャなど、補助的な間接バウンスの手法も
含まれています。特定のターゲットプラットフォームや特殊な構成を除けば、上記のソリューションより優先して選ばれることは
ほとんどありません。
</note>

## Lumen ではなく DDGI を選ぶ理由

Dynamic Diffuse Global Illumination は、イラディアンスをプローブのグリッドに保存し、球面調和関数でフィルタリングします。
表現が原理的に滑らかなため、デノイザーなしでもノイズのない結果が得られます。これが Lumen に対する利点の大半の根本的な
理由です。

ソフトウェア Lumen と比べると、DDGI はより高品質なバウンスと少ない光漏れを実現します。ハードウェア Lumen と比べると、
バウンスの品質は同等で、一般におよそ 2 倍の速度で動作します。これは GI 単体のコストではなく、シーン全体の
フレームレートで測った値です。RTX 4080 Super、1440p ネイティブの代表的なテストシーンでは、DDGI が 811 FPS、
Lumen 5.7 が 324 FPS でした。AMD のハードウェアでも良好で、同じ種類のテストシーンが RX 6600 で 1080p ネイティブ
245 FPS で動作します。

DDGI は実験的な技術でもありません。その実装は Metro Exodus、Overwatch 2、The Finals、Control、The Witcher 3、
Warhammer 40,000: Darktide、DOOM: The Dark Ages、Indiana Jones and the Great Circle、007 First Light、Ghost of Yotei、
そして Switch 2 版を含む Star Wars Outlaws で出荷されています。Anvil や Snowdrop といった AAA エンジンも、
レイトレーシング GI のパイプラインの一部として DDGI のプローブを使っています。この手法は幅広いハードウェアに対応する
よう設計されており、静的モードは Xbox One S の GPU から、動的な RT モードは GTX 1060 クラスの GPU から動作します。

<img src="DDGIEmissiveSurfaces.png" alt="エミッシブサーフェスが DDGI に寄与してライティングされた室内" border-effect="line"/>

*エミッシブマテリアルは DDGI に直接寄与するため、ライトアクターを配置しなくてもエミッシブなジオメトリでシーンを
照らせます。*

## DDGI と SSGI を組み合わせる理由

プローブボリュームには空間的な解像度があります。椅子の脚が床に接する部分の暗がり、狭い隙間でのバウンス、机の下の
接触シャドウなど、プローブの間隔より小さいディテールは、それを表現するプローブがないため表現されません。

スクリーンスペース GI はピクセル単位の解像度で動作し、まさにそれを捉えます。2 つの手法の弱点は正反対です。SSGI は
画面外や遮蔽されたものの情報を持たず、DDGI はワールド全体の情報を粗い解像度で持ちます。両方を使えば、DDGI による
ワールド規模のバウンスと、SSGI による高周波の接触ディテールの両方が得られます。NVIDIA は Unreal Engine の DDGI に
関する発表でこの組み合わせを推奨しており、Vite の SSGI は標準で DDGI と併用できるよう設定されています。

これは UE5 では不可能です。SSGI は Lumen に統合された際に品質と性能の両方が低下し、別の GI ソリューションと併用できなく
なりました。Vite の SSGI は UE4 世代の実装で、きれいに組み合わせられます。

## 推奨構成を有効にする

```c++
IConsoleManager::Get().FindConsoleVariable(TEXT("r.GlobalIllumination.ExperimentalPlugin"))->Set(1);
IConsoleManager::Get().FindConsoleVariable(TEXT("r.SSGI.Enable"))->Set(1);
```

製品版では、スケーラビリティの仕組みに組み込まれる設定ファイルでの指定をお勧めします。

```ini
; Config/DefaultEngine.ini
[/Script/Engine.RendererSettings]
r.GlobalIllumination.ExperimentalPlugin=1
r.SSGI.Enable=1
```

その後、レベルに DDGI のボリュームを配置する必要があります。ボリュームの設定、プローブの密度、重要な設定については
[動的 DDGI](DDGI-Dynamic.md) を参照してください。

## 最低スペックに合わせて選ぶ

<procedure title="GI の構成を選ぶ" id="pick-gi">
    <step>
        最低スペックが DXR に対応しているなら、動的 DDGI と SSGI を併用します。これが既定の推奨で、
        GTX 1060 6&nbsp;GB 以上をカバーします。
    </step>
    <step>
        最低スペックが DXR に一切対応していないなら、<a href="DDGI-Static.md">静的 DDGI</a> を使います。ほぼ一瞬で
        ベイクでき、従来のベイクライティングより高精度なバウンスが得られ、プローブボリュームがサーフェスではなく
        空間をカバーするため、動くオブジェクトもより適切に扱えます。
    </step>
    <step>
        両方に対応する必要がある場合は、静的 DDGI をスケーラビリティのフォールバックとして出荷します。ボリュームと
        作成作業は 2 つのモードで共通なので、レベルのライティングをもう一度行うのではなく、スケーラビリティの設定に
        なります。
    </step>
    <step>
        ピクセル単位のレイトレーシング GI は、リファレンス画像やプリビジュアライゼーションを作る場合に限って使って
        ください。DDGI よりはるかに重く、フレームタイムの予算の中ではその利点が残りません。また既定のビルドでは
        コンパイル対象から外れており、<code>VITE_RT_PSO_DEBLOAT=0</code> で再ビルドする必要があります。
        <a href="Compile-Time-Switches.md">コンパイル時スイッチ</a> を参照してください。
    </step>
</procedure>

## 関連項目

- [動的 DDGI](DDGI-Dynamic.md)
- [静的 DDGI](DDGI-Static.md)
- [SSGI](SSGI.md)
- [レイトレーシング](Ray-Tracing.md)
- [パフォーマンス目標](Performance-Targets.md)
