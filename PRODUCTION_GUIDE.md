# 📋 本番利用ガイド - 完全版

Carbon XRD Structure Tool は **完全に実装・テスト完了** し、本番利用可能な状態です。

---

## 🎯 このガイドについて

ユーザーが **実際に使い始める** ための完全な手順を提供します。

- 👶 **初心者向け**: 技術経験がなくても大丈夫
- ⚡ **すぐ始める**: 最短5分でツール利用開始
- 🔧 **詳細ガイド**: 専門的な設定も可能

---

## 📚 3つのドキュメント

### 1️⃣ **QUICKSTART.md** - 今すぐ試す（5分）

```
👉 最初に読むべき
✓ 3ステップのセットアップ
✓ 実行例付き
✓ よくある問題の対応
```

**こんな人向け:**
- 今すぐ試したい
- 細かい説明は不要
- 動かしてから理解したい

**内容:**
- Windows/macOS/Linuxでの最小セットアップ
- 3つの使い方（CLI / API / Copilot Agent）
- 5つの基本的なユースケース

---

### 2️⃣ **GETTING_STARTED.md** - 完全ガイド（30分）

```
👉 深く理解したい人向け
✓ 全機能の詳細説明
✓ 全APIエンドポイント
✓ トラブルシューティング
✓ FAQ
```

**こんな人向け:**
- 全機能を理解したい
- カスタマイズしたい
- チームに説明する必要がある

**内容:**
- インストール手順（詳細版）
- CLI 全オプション解説
- API 4エンドポイントの仕様
- Copilot Agent デプロイ方法
- 10個のFAQ
- 10個のトラブルシューティング

---

### 3️⃣ **README.md** - 概要

```
👉 プロジェクト全体の説明
✓ 何ができるか
✓ システムアーキテクチャ
✓ ファイル構成
```

**こんな人向け:**
- プロジェクト全体を把握したい
- 技術的な背景を知りたい

---

## 🚀 今すぐ始める（3ステップ）

### ステップ1: インストール

**Windows:**
```powershell
cd Carbon_xrd
setup.bat
```

**macOS/Linux:**
```bash
cd Carbon_xrd
chmod +x setup.sh
./setup.sh
```

### ステップ2: 試す

```bash
# PYTHONPATH を設定（毎回または永続設定）
export PYTHONPATH="${PWD}/src"

# 実行
python -m carbon_xrd.cli generate-pattern \
  --cif tests/graphene.cif \
  --output results/
```

**出力:**
- `results/xrd_pattern.png` - グラフを画像で確認
- `results/xrd_peaks.csv` - データを数値で確認

### ステップ3: 次に進む

| やりたいこと | 次のステップ |
|-----------|-----------|
| 自分の構造を試す | CIFファイルを用意して実行 |
| APIから利用 | `python -m carbon_xrd.api_server` で起動 |
| Copilot Agentで使う | GETTING_STARTED.md 方法3 を実行 |
| 詳しく知りたい | GETTING_STARTED.md を読む |

---

## 🎯 3つの使い方

### 使い方1️⃣: CLI（コマンドライン）

**最も簡単。スタンドアロン実行に最適。**

```bash
export PYTHONPATH="${PWD}/src"
python -m carbon_xrd.cli generate-pattern --cif my_structure.cif --output results/
```

**こんな時に:**
- 1つの構造を確認
- バッチ処理で複数実行
- スクリプトから呼び出し

**出力:** PNG画像 + CSVデータ

---

### 使い方2️⃣: API サーバー

**柔軟性が高い。Webアプリから利用可能。**

```bash
# サーバー起動
python -m carbon_xrd.api_server

# リクエスト（別ターミナル）
curl -X POST http://localhost:5000/api/v1/generate-pattern \
  -H "Content-Type: application/json" \
  -d '{
    "cif_content": "graphene",
    "include_pdf": false,
    "peak_threshold": 1.0
  }'
```

**こんな時に:**
- Webアプリから利用
- 複数ユーザーで同時利用
- ローカルネットワーク共有

**レスポンス:** JSON（Base64エンコード画像 + ピークデータ）

---

### 使い方3️⃣: Copilot Agent

**最も直感的。マウス操作で利用可能。**

```bash
# M365 Copilot に登録
npm install -g @microsoft/m365agentstoolkit-cli
atk provision --env local

# Copilot Chat を開く
# 自然言語で指示: "グラフェンのXRDを見せて"
```

**こんな時に:**
- 非技術者でも使いたい
- 自然言語で指示したい
- GUI で確認したい

**操作:** Copilot Chat で自然言語入力 → 画像とデータが自動生成

---

## 📊 出力の見方

### XRD パターン（PNG画像）

```
強度(%)
  │     ┌─╖
  │     │ ║      ╭──╖
  │  ╭──┤ ║  ┌───┤  ║
  └──┴──┴─╜──┴───┴──╜─→ 2θ(度)
  10   30   50   70  90
```

**読み方:**
- 縦軸: X線回折強度（高いほどピークが強い）
- 横軸: 回折角2θ（度）
- ピークの位置: 結晶構造の特徴
- ピークの幅: 結晶性（広い=無秩序、狭い=高結晶）

### ピークデータ（CSV）

| 2θ (°) | d-spacing (Å) | Intensity (%) |
|---------|--------------|---------------|
| 43.46   | 2.0824       | 1.53          |
| 46.35   | 1.9589       | 1.18          |

**読み方:**
- `2θ`: 回折角（大きいほど原子間距離が小さい）
- `d-spacing`: 結晶面の間隔（Å）
- `Intensity`: ピークの強さ（%）

Excelで開いてグラフ化・分析可能。

---

## 💡 本番運用のポイント

### ポイント1: PYTHONPATH 設定

毎回コマンドを打つのが面倒な場合、永続設定します。

**Windows（管理者 PowerShell）:**
```powershell
# $PROFILE を編集
notepad $PROFILE

# 以下を追加
$env:PYTHONPATH = "C:\Users\YourName\Carbon_xrd\src"
$env:PYTHONIOENCODING = "utf-8"

# 確認
. $PROFILE
```

**macOS/Linux:**
```bash
# ~/.bashrc または ~/.zshrc に追加
export PYTHONPATH="${HOME}/Carbon_xrd/src"
export PYTHONIOENCODING="utf-8"

# 確認
source ~/.bashrc
```

### ポイント2: バッチ処理

複数の構造を一括処理:

```bash
#!/bin/bash
export PYTHONPATH="${PWD}/src"

for cif_file in structures/*.cif; do
    base_name=$(basename "$cif_file" .cif)
    python -m carbon_xrd.cli generate-pattern \
        --cif "$cif_file" \
        --output "results/$base_name"
done

echo "処理完了！"
```

### ポイント3: 常時サーバー運用

API サーバーを常時起動:

**Windows（タスクスケジューラー）:**
1. `タスクスケジューラー` を開く
2. 「基本タスク」→「作成」
3. プログラム: `python`
4. 引数: `-m carbon_xrd.api_server`
5. トリガー: 「システム起動時」

**Linux/macOS（systemd）:**
```bash
# /etc/systemd/system/carbon-xrd.service を作成
[Unit]
Description=Carbon XRD API Server
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/Carbon_xrd
Environment="PYTHONPATH=/path/to/Carbon_xrd/src"
ExecStart=/usr/bin/python -m carbon_xrd.api_server
Restart=on-failure

[Install]
WantedBy=multi-user.target

# 有効化・起動
sudo systemctl enable carbon-xrd
sudo systemctl start carbon-xrd
```

---

## 🔍 動作確認チェックリスト

セットアップ後、以下で動作確認します:

- [ ] `python -m pytest tests/test_carbon_xrd.py` → 9/9 合格
- [ ] `python -m carbon_xrd.cli generate-pattern --cif tests/graphene.cif --output results/` → 画像 + CSV 生成
- [ ] `python -m carbon_xrd.api_server` → `http://127.0.0.1:5000` で起動
- [ ] API テスト: `curl http://localhost:5000/health` → `{"status": "healthy"}`

全て完了すれば、本番利用可能です。

---

## 📞 サポート

### ドキュメント

1. **QUICKSTART.md** - すぐ試す（おすすめ）
2. **GETTING_STARTED.md** - 完全ガイド
3. **copilot_agent/DESIGN.md** - 設計書
4. **copilot_agent/openapi.yaml** - API仕様

### よくある質問

**Q: 自分の CIF ファイルを使える？**
A: はい。標準形式なら直接利用可能。

**Q: インターネット接続が必要？**
A: インストール時のみ。実行時は不要。

**Q: クラウドにデプロイできる？**
A: はい。Azure App Service, AWS Lambda 等に対応可能。

**Q: 複数ユーザーで同時使用できる？**
A: APIサーバーモードなら可能。

**Q: オフラインで使える？**
A: はい。インストール後はオフライン環境でも利用可能。

---

## 🎓 次のステップ

### Level 1: 基本利用（今ここ）
- [ ] インストール完了
- [ ] CLI で実行確認
- [ ] 出力ファイル確認

### Level 2: 応用利用
- [ ] APIサーバーを起動
- [ ] 自分の CIF ファイルで実行
- [ ] 結果をExcelで分析

### Level 3: 高度な利用
- [ ] Copilot Agent をデプロイ
- [ ] チームで共有
- [ ] カスタマイズ

### Level 4: エンタープライズ運用
- [ ] クラウドにデプロイ
- [ ] 認証・ロールベースアクセス実装
- [ ] 監視・ログ設定

---

## 📝 ライセンス

MIT License - 自由に使用・修正・配布可能

---

## ✨ まとめ

このツールは **完全に完成** しており、以下が保証されています:

✅ **実装完了**
- Python CLI ✓
- REST API ✓
- Copilot Agent ✓
- テスト 9/9 合格 ✓

✅ **ドキュメント完備**
- セットアップガイド ✓
- 使用方法 ✓
- API仕様 ✓
- トラブルシューティング ✓

✅ **本番利用可能**
- 単体実行 ✓
- サーバー運用 ✓
- クラウドデプロイ対応 ✓

---

## 🚀 さあ、始めましょう！

```bash
# 1. インストール
setup.bat          # Windows
./setup.sh         # macOS/Linux

# 2. 試す
python -m carbon_xrd.cli generate-pattern --cif tests/graphene.cif --output results/

# 3. 詳しく知る
# → QUICKSTART.md or GETTING_STARTED.md
```

**楽しい材料研究を！🔬**
