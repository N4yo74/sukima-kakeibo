# Sukima 家計簿 💴

シンプルで速い、スマホ向けの家計簿アプリ（PWA）。
**3タップで記録**・**データは端末内に保存**・**オフラインでも動く**。インストール不要、依存ゼロ。

<img src="icons/icon-192.png" width="96" alt="app icon">

## ✨ 特徴
- **速い入力** — 大きな電卓キーパッドで金額を入れて3タップで記録完了
- **見やすい可視化** — 支出内訳のドーナツグラフ、月別推移、カテゴリ別ランキング
- **オフライン対応** — Service Worker でネットが無くても起動（PWA）
- **プライバシー第一** — データは端末内（localStorage）のみ。サーバー送信なし
- **ダーク / ライト自動切替**
- **依存ゼロ** — 単一HTML + Vanilla JS。ビルド不要

## 📱 使い方
1. `index.html` をブラウザで開く
2. スマホでアプリ化するには、配信URLを開いて **「ホーム画面に追加」**
   - iPhone（Safari）: 共有 → ホーム画面に追加
   - Android（Chrome）: メニュー → アプリをインストール

## 🛠 開発
- アイコン再生成: `python make_icons.py`（標準ライブラリのみ・外部依存なし）
- ローカル確認: `python -m http.server 8000` → <http://localhost:8000>
  - ※ Service Worker / インストールは https か localhost でのみ有効

## 🧩 構成
| ファイル | 役割 |
|---|---|
| `index.html` | アプリ本体（UI + ロジック） |
| `manifest.json` | PWA アプリ情報 |
| `sw.js` | オフライン用 Service Worker |
| `icons/` | アプリアイコン（PNG・自前生成） |
| `make_icons.py` | アイコン生成スクリプト |

## 🗺 ロードmap
- [x] ① PWA 化（ホーム画面アプリ・オフライン）
- [ ] ② Capacitor でラップして App Store / Google Play 配信

## 📄 ライセンス
© 2026 syuto. All rights reserved.
