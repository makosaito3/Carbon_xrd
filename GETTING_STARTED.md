# Carbon XRD Structure Tool - 本番利用ガイド

炭素材料開発者向けの構造-XRD相互可視化ツール。このガイドでは、3つの利用方法を説明します。

---

## 📋 目次

1. [インストール](#インストール)
2. [方法1: CLIで直接使用](#方法1-cliで直接使用)
3. [方法2: REST APIサーバーで使用](#方法2-rest-apiサーバーで使用)
4. [方法3: GitHub Copilot Agentで使用](#方法3-github-copilot-agentで使用)
5. [よくある質問（FAQ）](#よくある質問faq)
6. [トラブルシューティング](#トラブルシューティング)

---

## インストール

### 前提条件

- Python 3.9 以上
- pip（Pythonパッケージマネージャー）
- Git

### ステップ1: リポジトリをクローン

```bash
git clone https://github.com/makosaito3/Carbon_xrd.git
cd Carbon_xrd
```

### ステップ2: 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

**インストール内容:**
- `pymatgen` - 結晶構造計算
- `matplotlib` - グラフ描画
- `pandas` - データ処理
- `numpy` - 数値計算
- `scipy` - 科学計算
- `flask` - REST API サーバー

### ステップ3: インストール確認

```bash
python -m pytest tests/test_carbon_xrd.py
```

**期待される結果:** `9 passed`

---

## 方法1: CLIで直接使用

### 最も簡単な使用方法です。コマンドラインから直接実行できます。

#### 基本的な使用方法

```bash
# Windows/macOS/Linux 共通（Linux/macOSの場合）
export PYTHONPATH="${PWD}/src"
python -m carbon_xrd.cli generate-pattern --cif <CIFファイル> --output <出力ディレクトリ>
```

**Windows PowerShellの場合:**

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m carbon_xrd.cli generate-pattern --cif <CIFファイル> --output <出力ディレクトリ>
```

#### 実行例

```bash
# グラフェンのXRDパターンを生成
export PYTHONPATH="${PWD}/src"
python -m carbon_xrd.cli generate-pattern --cif tests/graphene.cif --output results/

# PDF（ペア分布関数）も含める
python -m carbon_xrd.cli generate-pattern --cif tests/graphene.cif --output results/ --include-pdf

# X線波長をカスタマイズ（Mo Kα = 0.71 Å）
python -m carbon_xrd.cli generate-pattern --cif tests/graphite.cif --output results/ --wavelength 0.71

# ピーク抽出の感度を調整（デフォルト1.0%）
python -m carbon_xrd.cli generate-pattern --cif my_structure.cif --output results/ --peak-threshold 2.0
```

#### 利用可能なオプション

```
--cif CIF                  入力CIFファイルパス（必須）
--output OUTPUT            出力ディレクトリ（デフォルト: results/）
--wavelength WAVELENGTH    X線波長 Å（デフォルト: 1.54184 Cu Kα）
--xrd-range XRD_RANGE      XRD測定範囲 2θ度（デフォルト: 10-100）
--peak-threshold VALUE     ピーク抽出の感度 %（デフォルト: 1.0）
--include-pdf              PDF計算を含める（デフォルト: 無効）
--formats FORMATS          出力形式（デフォルト: png,csv）
--dpi DPI                  PNG解像度（デフォルト: 300）
```

#### 出力ファイル

実行後、以下のファイルが生成されます:

| ファイル名 | 説明 |
|-----------|------|
| `xrd_pattern.png` | XRD回折パターン図（300dpi） |
| `xrd_pattern.csv` | XRD 全データ（2θ, 強度） |
| `xrd_peaks.csv` | 抽出されたピーク情報（2θ, d-spacing, 強度%） |
| `total_scattering.png` | Total Scattering S(Q) グラフ |
| `total_scattering.csv` | S(Q) データ |
| `pdf_pattern.png` | PDF G(r) グラフ（--include-pdf 時のみ） |

---

## 方法2: REST APIサーバーで使用

### PythonやNode.jsなど、他のプログラムから利用したい場合に便利です。

#### ステップ1: APIサーバーを起動

```bash
export PYTHONPATH="${PWD}/src"
python -m carbon_xrd.api_server
```

**Windows PowerShellの場合:**

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m carbon_xrd.api_server
```

**出力例:**

```
 * Running on http://127.0.0.1:5000
```

#### ステップ2: APIを呼び出す

APIサーバーは以下のエンドポイントを提供します:

### エンドポイント1: `/api/v1/generate-pattern` (POST)

**構造を指定してXRDパターンを生成します。**

```bash
curl -X POST http://localhost:5000/api/v1/generate-pattern \
  -H "Content-Type: application/json" \
  -d '{
    "cif_content": "graphene",
    "include_pdf": false,
    "peak_threshold": 1.0
  }'
```

**リクエストボディ:**

```json
{
  "cif_content": "graphene",           // 構造テンプレート または CIF内容
  "include_pdf": false,                // PDF計算を含めるか
  "peak_threshold": 1.0,               // ピーク感度（%）
  "wavelength": 1.54184,               // X線波長（Å）（オプション）
  "xrd_range": "10-100"                // 測定範囲 2θ度（オプション）
}
```

**サポートされるテンプレート:**
- `"graphene"` - グラフェン
- `"graphite"` - グラファイト

**レスポンス（200 OK）:**

```json
{
  "success": true,
  "formula": "C2",
  "atoms": 2,
  "peaks_found": 2,
  "xrd_plot": "data:image/png;base64,...",
  "total_scattering_plot": "data:image/png;base64,...",
  "pdf_plot": null,
  "peak_data": [
    {
      "two_theta": 43.46,
      "d_spacing": 2.0824,
      "intensity": 1.53
    },
    ...
  ],
  "message": "Successfully generated patterns for C2 with 2 peaks detected."
}
```

### エンドポイント2: `/api/v1/structures` (GET)

**利用可能なテンプレートを取得します。**

```bash
curl http://localhost:5000/api/v1/structures
```

**レスポンス:**

```json
{
  "structures": [
    {
      "name": "graphene",
      "description": "Single-layer hexagonal carbon",
      "formula": "C"
    },
    {
      "name": "graphite",
      "description": "Layered structure with ABA stacking",
      "formula": "C"
    }
  ]
}
```

### エンドポイント3: `/health` (GET)

**サーバーの状態確認:**

```bash
curl http://localhost:5000/health
```

**レスポンス:**

```json
{
  "status": "healthy"
}
```

#### Pythonクライアント例

```python
import requests
import json
from base64 import b64decode

# APIサーバーに接続
response = requests.post(
    'http://localhost:5000/api/v1/generate-pattern',
    json={
        'cif_content': 'graphene',
        'include_pdf': True,
        'peak_threshold': 1.0
    }
)

data = response.json()

# 画像を保存
if data['success']:
    # XRDパターン画像
    xrd_data = data['xrd_plot'].replace('data:image/png;base64,', '')
    with open('xrd.png', 'wb') as f:
        f.write(b64decode(xrd_data))
    
    # ピークデータを表示
    for peak in data['peak_data']:
        print(f"2θ={peak['two_theta']:.2f}°, d={peak['d_spacing']:.4f}Å, I={peak['intensity']:.2f}%")
```

---

## 方法3: GitHub Copilot Agentで使用

### 最も簡単。自然言語で構造を説明するだけで、自動的にXRDが生成されます。

#### セットアップ手順

##### ステップ1: ATK CLIをインストール

```bash
npm install -g @microsoft/m365agentstoolkit-cli
```

##### ステップ2: Agentプロジェクトを初期化（必要な場合）

```bash
atk new
```

##### ステップ3: Agent マニフェストをコピー

```bash
# このリポジトリの Agent マニフェストを使用
cp copilot_agent/declarativeAgent.json appPackage/
cp copilot_agent/openapi.yaml appPackage/
```

##### ステップ4: M365 Copilotにデプロイ

```bash
atk provision --env local --interactive false
```

##### ステップ5: テスト リンクを開く

デプロイ後、`env/.env.local`から`TEAMS_APP_ID`を取得します：

```bash
cat env/.env.local | grep TEAMS_APP_ID
```

以下のURLでテスト:
```
https://m365.cloud.microsoft/chat/?titleId=<YOUR_TEAMS_APP_ID>
```

#### Copilot Agentの使用例

Copilot Chatで以下のように入力:

```
"グラフェンのXRDパターンを見たいです。
単層で、格子定数 a=2.46Å のきれいな構造をお願いします。"
```

Agent は以下を自動的に実行:
1. ✓ テキスト説明を解析
2. ✓ CIFファイルを生成
3. ✓ APIを呼び出し
4. ✓ XRDパターン画像を表示
5. ✓ ピーク情報を説明

#### Agentの会話スターター例

- 「グラフェンのXRDパターンを見たいです」
- 「グラファイトの秩序と無秩序の状態でXRDパターンを比較してください」
- 「30%の点欠陥を持つアモルファスカーボンのXRDは？」
- 「層間隔 0.34nm で15%のスタッキング欠陥があるカーボンのXRDを予測してください」

---

## よくある質問（FAQ）

### Q1: 自分の構造CIFファイルを使いたいのですが？

CIFファイルの形式が標準的なら、そのまま使用可能です：

```bash
export PYTHONPATH="${PWD}/src"
python -m carbon_xrd.cli generate-pattern --cif my_structure.cif --output results/
```

CIFファイルの作成方法:
- **Materials Studio, VESTA等の結晶構造ソフト** - エクスポート機能で CIF 形式で保存
- **ICSD, Materials Project** - CIFダウンロード可能
- **pymatgen** - Pythonで生成

### Q2: 異なるX線源（Mo Kα, Ag Kα等）を使いたい

波長を指定してください：

```bash
# Cu Kα (デフォルト)
python -m carbon_xrd.cli generate-pattern --cif structure.cif --output results/

# Mo Kα (0.71 Å)
python -m carbon_xrd.cli generate-pattern --cif structure.cif --output results/ --wavelength 0.71

# Ag Kα (0.56 Å)
python -m carbon_xrd.cli generate-pattern --cif structure.cif --output results/ --wavelength 0.56
```

### Q3: ピークの感度を変更したい

`--peak-threshold`で調整：

```bash
# デフォルト (1.0%)
python -m carbon_xrd.cli generate-pattern --cif structure.cif --output results/

# より多くのピークを検出 (0.5%)
python -m carbon_xrd.cli generate-pattern --cif structure.cif --output results/ --peak-threshold 0.5

# 強いピークのみ (5.0%)
python -m carbon_xrd.cli generate-pattern --cif structure.cif --output results/ --peak-threshold 5.0
```

### Q4: APIサーバーをどのくらい起動したままにしておけばいい？

常時運用する場合:
- **ローカル開発:** Ctrl+Cで終了するまで
- **本番運用:** Process Manager (`pm2`, `systemd`) で自動再起動
- **クラウド:** Azure App Service, AWS Lambda等にデプロイ

### Q5: 複数の構造を一括処理したい

Bashスクリプト例:

```bash
#!/bin/bash
export PYTHONPATH="${PWD}/src"

for cif_file in structures/*.cif; do
    base_name=$(basename "$cif_file" .cif)
    python -m carbon_xrd.cli generate-pattern \
        --cif "$cif_file" \
        --output "results/$base_name"
done
```

### Q6: APIサーバーのタイムアウトは？

現在のデフォルト: 30秒

大きな構造の場合、以下でタイムアウトを延長:

```python
# api_server.py の先頭に追加
import os
os.environ['WERKZEUG_RUN_MAIN'] = 'true'
app.config['PROPAGATE_EXCEPTIONS'] = True
```

---

## トラブルシューティング

### エラー: `ModuleNotFoundError: No module named 'carbon_xrd'`

**原因:** PYTHONPATH が設定されていない

**解決方法:**

```bash
# Linux/macOS
export PYTHONPATH="${PWD}/src"

# Windows PowerShell
$env:PYTHONPATH = "$PWD\src"

# 確認
echo $PYTHONPATH
```

### エラー: `UnicodeEncodeError: 'cp932' codec can't encode...`

**原因:** Windows でのエンコーディング問題

**解決方法:**

```bash
# Windows PowerShell
$env:PYTHONIOENCODING = "utf-8"
python -m carbon_xrd.cli generate-pattern --cif tests/graphene.cif --output results/
```

### エラー: `OSError: [Errno 2] No such file or directory`

**原因:** CIFファイルが見つからない

**解決方法:**
1. CIFファイルのパスが正しいか確認
2. 絶対パスで指定

```bash
python -m carbon_xrd.cli generate-pattern --cif /full/path/to/structure.cif --output results/
```

### APIサーバーが起動しない

**原因:** ポート 5000 が使用されている

**解決方法:**

別のポートで起動:

```python
# api_server.py を修正
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```

### 画像が生成されない

**原因:** matplotlib のバックエンド問題

**解決方法:**

```bash
pip install --upgrade matplotlib
```

### 計算が遅い

**原因:** 大きな構造の計算には時間がかかる

**最適化:**
- ピーク感度を上げる: `--peak-threshold 5.0`
- PDF計算を省略: `--include-pdf` を使わない
- XRD範囲を狭める: `--xrd-range 20-80`

---

## システム要件

| 項目 | 要件 |
|-----|------|
| OS | Windows, macOS, Linux |
| Python | 3.9 以上 |
| メモリ | 2GB 以上（推奨 4GB以上） |
| ディスク | 500MB（依存パッケージ含む） |
| ネット | インストール時のみ必要 |

---

## サポート

問題が解決しない場合:

1. **GitHub Issues** - バグレポート、質問
2. **ドキュメント** - `README.md`, `DESIGN.md` 参照
3. **テスト実行** - `pytest tests/` で診断

---

## ライセンス

MIT License - 自由に使用、修正、配布可能

---

## 次のステップ

- [ ] セットアップ完了
- [ ] CLI で簡単な構造をテスト
- [ ] APIサーバーを起動してブラウザでテスト
- [ ] 独自の CIF ファイルで実行
- [ ] Copilot Agent をデプロイ（本番環境）
- [ ] チームで共有開始

楽しい材料研究を！🔬
