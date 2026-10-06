# 初代 Vite

<tldr>
<p>
<b>NVIDIA の NvRTX 5.0</b>（Unreal Engine 5）をベースとした最初の Vite の系列です。PhysX とレイトレーシングという方向性を実証しましたが、同条件のテストで 4.27 ベースの NvRTX ブランチのほうが高速だと分かったため、2025 年 11 月に役目を終えました。現在はアーカイブされておりサポート対象外で、公開リポジトリの履歴は残っていません。
</p>
</tldr>

| 状態 | ベース | 後継 |
|---|---|---|
| アーカイブ | NvRTX 5.0（Unreal Engine 5） | [ueVite25 LTS](ueVite25-LTS.md)（2025 年 11 月） |

## この系列が確立したもの

- **最新エンジンでの PhysX。** 初代の系列は PhysX を UE5 世代のコードベースに移植しました。Chaos に対する Vite の立場はここから始まっています。
- **Lumen に頼らないレイトレーシング。** 主要な GI ソリューションとして、Lumen ではなく NvRTX の RTXGI/DDGI のパスを採用しました。
- **測定に基づく判断。** この系列で行った比較（レイトレーシング GI のフレームレートと、UE5 に PhysX を統合するコスト）が、4.27 ベースへの移行を決める根拠になりました。

## 置き換えられた理由

同条件のレイトレーシングのテストでは NvRTX 5.0 ベースのほうが NvRTX Caustics 4.27 より遅く、UE5 の物理アーキテクチャに対して PhysX を動かし続けるコストもかかり続けていました。詳しい理由は
[なぜ NvRTX 4.27 なのか](Why-NvRTX-427.md) と
[ベース移行の記録](https://docs.google.com/document/d/1gA0MGkzeWWzKkgwBDOP5xRPouSKaOIW6xlPZ2q6BXO0/edit) を参照してください。

## コミット記録

この系列については検証可能な公開コミット履歴が残っていないため、このページにはコミットの表はありません。上記の移行の記録が正式な経緯の説明です。

## 関連項目

- [すべてのリリースノート](Release-Notes.md)
- [ueVite25 LTS](ueVite25-LTS.md)
- [UE4 と UE5 のコスト分析](UE4-Versus-UE5-Cost-Analysis.md)
