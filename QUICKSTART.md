# Carbon XRD Structure Tool - Quick Start Guide（5分で使い始める）

## 🚀 3ステップでスタート

### ステップ1️⃣: インストール（2分）

#### Windows

```powershell
# PowerShellを開いて実行
cd Carbon_xrd
setup.bat
```

#### macOS / Linux

```bash
cd Carbon_xrd
chmod +x setup.sh
./setup.sh
```

**期待される結果:** `✓ Setup completed successfully!` メッセージが表示される

---

### ステップ2️⃣: CLI で試す（1分）

**Windows:**

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m carbon_xrd.cli generate-pattern --cif tests/graphene.cif --output results/
```

**macOS/Linux:**

```bash
export PYTHONPATH="${PWD}/src"
python -m carbon_xrd.cli generate-pattern --cif tests/graphene.cif --output results/
```

**出力:**
```
[LOAD] Loading CIF: tests/graphene.cif
[OK] Structure loaded successfully
[CALC] Calculating XRD pattern...
[PEAKS] Extracting peaks...
[OK] Found 2 peaks
[OK] XRD pattern saved: results/xrd_pattern.png
[SUCCESS] Pattern generation completed successfully!
```

**生成されたファイル:**
- `results/xrd_pattern.png` - XRD パターングラフ
- `results/xrd_pattern.csv` - XRD データ（スプレッドシート可）

---

### ステップ3️⃣: APIサーバーを起動（1分）

**Windows:**

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m carbon_xrd.api_server
```

**macOS/Linux:**

```bash
export PYTHONPATH="${PWD}/src"
python -m carbon_xrd.api_server
```

**出力:**

```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

**テスト実行（別のターミナルで）:**

```bash
curl -X POST http://localhost:5000/api/v1/generate-pattern \
  -H "Content-Type: application/json" \
  -d '{"cif_content": "graphene", "include_pdf": false}'
```

---

## 📚 基本的な3つの使い方

### 使い方1️⃣: CLI（コマンドライン）- 最も簡単

```bash
export PYTHONPATH="${PWD}/src"
python -m carbon_xrd.cli generate-pattern --cif structure.cif --output results/
```

**こんな時に:**
- スタンドアロン実行
- バッチ処理
- スクリプト組み込み

---

### 使い方2️⃣: APIサーバー - 柔軟性が高い

```bash
# サーバー起動
python -m carbon_xrd.api_server

# 別ターミナルで利用
curl -X POST http://localhost:5000/api/v1/generate-pattern \
  -H "Content-Type: application/json" \
  -d '{"cif_content": "graphene"}'
```

**こんな時に:**
- Webアプリから使いたい
- 複数の処理を並列実行
- ローカルネットワーク共有

---

### 使い方3️⃣: M365 Copilot Agent - 最も簡単（マウスで操作）

```bash
# デプロイ
npm install -g @microsoft/m365agentstoolkit-cli
atk provision --env local

# M365 Copilot を開く
# https://m365.cloud.microsoft/chat/?titleId=<YOUR_ID>

# Copilot Chat でこう入力:
# "グラフェンのXRDパターンを見たいです"
```

**こんな時に:**
- 非技術者でも使いたい
- 自然言語で指示したい
- GUI で結果を見たい

---

## 💡 よくあるユースケース

### ケース1: 新しい構造のXRDを確認したい

```bash
export PYTHONPATH="${PWD}/src"
python -m carbon_xrd.cli generate-pattern \
  --cif my_structure.cif \
  --output results/ \
  --include-pdf
```

**出力:**
- `xrd_pattern.png` - XRD グラフを画像で確認
- `pdf_pattern.png` - PDF グラフを画像で確認
- `xrd_peaks.csv` - ピークを数値で確認（Excelで開ける）

---

### ケース2: 複数の構造を比較したい

**Excelデータとしてまとめる:**

```bash
export PYTHONPATH="${PWD}/src"

# グラフェン
python -m carbon_xrd.cli generate-pattern \
  --cif tests/graphene.cif --output results/graphene/

# グラファイト
python -m carbon_xrd.cli generate-pattern \
  --cif tests/graphite.cif --output results/graphite/

# 結果を ExcelPower Query で読み込み
# graphene/xrd_peaks.csv と graphite/xrd_peaks.csv を比較
```

---

### ケース3: X線源を変更したい（Mo Kα, Ag Kα等）

```bash
export PYTHONPATH="${PWD}/src"

# Cu Kα (1.54 Å) - デフォルト
python -m carbon_xrd.cli generate-pattern --cif structure.cif --output results/

# Mo Kα (0.71 Å)
python -m carbon_xrd.cli generate-pattern \
  --cif structure.cif --output results_mo/ --wavelength 0.71

# Ag Kα (0.56 Å)
python -m carbon_xrd.cli generate-pattern \
  --cif structure.cif --output results_ag/ --wavelength 0.56
```

**結果:** 波長による XRD パターン変化を確認可能

---

### ケース4: ピークを詳しく分析したい

```bash
export PYTHONPATH="${PWD}/src"

# より多くのピークを検出（感度を下げる）
python -m carbon_xrd.cli generate-pattern \
  --cif structure.cif \
  --output results/ \
  --peak-threshold 0.5

# 少ないピークのみ（感度を上げる）
python -m carbon_xrd.cli generate-pattern \
  --cif structure.cif \
  --output results/ \
  --peak-threshold 5.0
```

**出力:** `xrd_peaks.csv` を開いて、2θ と d-spacing を確認

---

## 🔧 環境変数の設定（Windows/macOS/Linux共通）

**毎回設定するのが面倒な場合:**

### Windows PowerShell（永続設定）

ファイル: `$PROFILE`を編集（デフォルト）

```powershell
# PowerShell を管理者で開く
notepad $PROFILE

# 以下を追加
$env:PYTHONPATH = "C:\Users\YourName\Carbon_xrd\src"
$env:PYTHONIOENCODING = "utf-8"
```

### macOS/Linux（永続設定）

```bash
# ~/.bashrc または ~/.zshrc に追加
export PYTHONPATH="${HOME}/Carbon_xrd/src"
export PYTHONIOENCODING="utf-8"

# 設定を反映
source ~/.bashrc
```

---

## 📊 出力ファイルの見方

### XRD パターン（xrd_pattern.csv）

| 2-theta | Intensity |
|---------|-----------|
| 10.0    | 0.5       |
| 43.46   | 1.53      |
| 46.35   | 1.18      |
| ...     | ...       |

**読み方:**
- `2-theta`: X線回折角度（度）
- `Intensity`: 回折強度（%）
- グラフが高いほどピークが強い

### ピークデータ（xrd_peaks.csv）

| 2θ (deg) | d-spacing (Å) | Intensity (%) |
|----------|---------------|---------------|
| 43.46    | 2.0824        | 1.53          |
| 46.35    | 1.9589        | 1.18          |

**読み方:**
- `d-spacing`: 結晶面の間隔（Bragg's law で計算）
- 小さい d は高角度
- 大きい d は低角度

---

## ❓ トラブル対応（即解決）

### トラブル1: Python コマンドが見つからない

```bash
# Python をインストール確認
python --version

# インストールされていない場合
# https://www.python.org から Python 3.9+ をインストール
```

### トラブル2: PYTHONPATH が設定されていない

```bash
# 毎回実行前に設定
export PYTHONPATH="${PWD}/src"  # macOS/Linux
$env:PYTHONPATH = "$PWD\src"   # Windows PowerShell
```

### トラブル3: CIF ファイルが見つからない

```bash
# 絶対パスで指定
python -m carbon_xrd.cli generate-pattern \
  --cif /full/path/to/my_structure.cif \
  --output results/
```

### トラブル4: 画像が生成されない

```bash
# matplotlib をアップグレード
pip install --upgrade matplotlib

# 再度実行
python -m carbon_xrd.cli generate-pattern --cif tests/graphene.cif --output results/
```

---

## 🎯 次のステップ

| 次にしたいこと | 手順書 |
|-------------|-------|
| 自分の CIF を使いたい | [GETTING_STARTED.md](#q1-自分の構造cifファイルを使いたいのですが) |
| APIを別の言語から呼び出したい | [GETTING_STARTED.md - 方法2](#方法2-rest-apiサーバーで使用) |
| M365 Copilot に登録したい | [GETTING_STARTED.md - 方法3](#方法3-github-copilot-agentで使用) |
| 大量の構造を処理したい | [GETTING_STARTED.md - Q5](#q5-複数の構造を一括処理したい) |

---

## 📞 サポート

- **ドキュメント:** このファイル
- **詳細ガイド:** `GETTING_STARTED.md`
- **API仕様:** `copilot_agent/openapi.yaml`
- **設計書:** `copilot_agent/DESIGN.md`

---

楽しい材料研究を！🔬
