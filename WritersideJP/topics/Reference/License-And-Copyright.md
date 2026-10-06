# ライセンスと著作権

<tldr>
<p>
Vite は Unreal Engine 4.27 のフォークです。エンジンは Epic の
<a href="https://www.unrealengine.com/eula/unreal">Unreal Engine エンドユーザーライセンス契約</a> に基づいて使用されます。
Vite 独自の作業の著作権は Vite Studio にあります。
</p>
</tldr>

<note>
この日本語訳は参考のためのものです。法的な効力を持つのは、Epic の EULA の原文と、このページの英語版です。
</note>

Unreal Engine Vite は Unreal Engine 4.27 をベースにしています。使用の仕組みは、他の Unreal Engine のソースビルドを使う
場合と同じです。Epic のライセンスに同意し、既存の表示を残し、エンジンで作ったプロジェクトはあなたのものになります。

## Unreal Engine

Vite による変更を含むエンジンは、Epic の [Unreal Engine EULA](https://www.unrealengine.com/eula/unreal) における
**Licensed Technology** です。このバージョン（4.27）のソースとエディタのツールは、Unreal Engine のライセンシーが
利用できます。

Vite で作ったゲームやその他のプロジェクトは **Product** です。その Product は、中に含まれる Licensed Technology を除いて、
あなたが所有します。Licensed Technology は Epic が所有します。

ロイヤリティ、シートのサブスクリプション、出荷に関する Epic の通常の条件は引き続き適用されます。Vite Studio がそれらを
置き換えることはありません。

## 著作権

標準の Unreal Engine 4.27 の著作権は引き続き Epic Games, Inc. にあります。NvRTX のブランチ由来の NVIDIA の素材の著作権は
引き続き NVIDIA にあります。サードパーティのライブラリには、すでに付属している表示がそのまま残ります。

Vite 独自の作業の著作権は Vite Studio にあります。

```
Copyright 2026 Vite Studio. All rights reserved.
```

ソースでは次のように表記します。

```c++
// Copyright 2026 Vite Studio. All rights reserved.
```

エンジンのファイルには Epic の既存のヘッダーがそのまま残ります。Vite が独自の作業を加えた箇所では、Vite Studio の表示が
それと並んで記載されます。

## クレジット表記

出荷する Product にクレジットがある場合は、Epic の標準の Unreal Engine のクレジット（現在の年を記載）を含めてください。

```
[Product name] uses Unreal® Engine. Unreal® is a trademark or registered trademark of Epic Games, Inc. in the United States of America and elsewhere.

Unreal® Engine, Copyright 1998 – 2026, Epic Games, Inc. All rights reserved.
```

## 商標

Unreal® と Unreal Engine は Epic Games, Inc. の商標です。Vite と Unreal Engine Vite は、このフォークのために Vite Studio が
使用しています。

## サードパーティのコンポーネント

| コンポーネント | 条件 |
|---|---|
| NVIDIA NvRTX と関連する SDK | それらのブランチと SDK に対する NVIDIA のライセンス |
| PhysX、Apex Destruction、Apex Cloth | [GameWorks source SDK EULA](https://developer.nvidia.com/gameworks-source-sdk-eula) |
| その他の同梱ライブラリ | `Engine/Source/ThirdParty/Licenses` と `Engine/Extras/ThirdPartyNotUE/` |

## 関連項目

- [はじめに](Getting-Started.md)
- [よくある質問](FAQ.md)
- [Unreal Engine EULA](https://www.unrealengine.com/eula/unreal)
