# Phase 2: Copilot Agent 開発ガイド

## 1. エージェント概要

**名前**: Carbon XRD Structure Assistant  
**説明**: 炭素材料の構造をテキストで記述し、XRDと総散乱パターンを可視化するCopilot Agentエージェント  
**対象ユーザー**: 材料研究者、開発エンジニア

## 2. エージェント機能フロー

```
ユーザー: 「グラファイト系材料で層間距離0.35nm、欠陥率15%の構造を分析したい」
   ↓
[Copilot Agent]
1. テキスト入力の解析
2. LLMによるCIF自動生成
3. CLIプログラム実行指示
4. 結果の表示（PNG + CSV）
```

## 3. Manifest 構成（declarativeAgent.json）

```json
{
  "schema": "https://developer.microsoft.com/json-schemas/copilot/declarativeAgent/v1.0/schema.json",
  "version": "1.0",
  "name": "Carbon XRD Structure Assistant",
  "description": "Analyze carbon material structures and visualize XRD patterns",
  "instructions": "[See section 4]",
  "conversation": {
    "type": "GroupChat",
    "conversationStarters": [
      {
        "title": "Graphene Structure",
        "text": "Analyze a single-layer graphene structure with layer spacing 0.335 nm"
      },
      {
        "title": "Graphite with Defects",
        "text": "Generate a graphite structure with 20% stacking disorder and calculate XRD"
      },
      {
        "title": "Amorphous Carbon",
        "text": "Model amorphous carbon and show total scattering pattern"
      }
    ]
  },
  "capabilities": [
    {
      "name": "cif_generator",
      "description": "Convert text description to CIF crystallographic file"
    },
    {
      "name": "xrd_calculator",
      "description": "Calculate XRD patterns from CIF structures"
    },
    {
      "name": "total_scattering",
      "description": "Compute total scattering S(Q) and PDF"
    }
  ],
  "actions": [
    {
      "id": "generate_pattern",
      "description": "Run CLI to generate XRD and total scattering patterns",
      "operation": "GenerateXRDPattern"
    }
  ]
}
```

## 4. Instructions Design

### Purpose
ユーザーのテキスト記述から結晶構造を推定し、XRDパターンの変化を可視化する。

### Key Intents
1. **Structure Analysis** - ユーザーの記述から結晶パラメータを推定
2. **CIF Generation** - テキスト → CIF ファイル変換
3. **Pattern Calculation** - CIF → XRD/Total Scattering 計算
4. **Visualization** - 結果表果の解釈と説明

### Sample Instructions

```
You are the Carbon XRD Structure Assistant, specialized in helping researchers visualize how carbon material structures manifest in X-ray diffraction patterns.

## Your Role
1. **Listen** to the user's description of carbon material structure (e.g., "graphite with 10% stacking faults", "defective graphene")
2. **Interpret** the description into crystallographic parameters (lattice constants, atom positions, disorder)
3. **Generate** a CIF file that represents this structure
4. **Calculate** XRD pattern, total scattering, and pair distribution
5. **Show** visual plots (PNG) and numerical data (CSV)

## Structure Interpretation Rules

### Graphene-like materials
- Default: hexagonal, a=b≈2.46Å, c=10.0Å (single layer)
- Single-layer: 1-2 atoms per unit cell
- Multi-layer: stack along c-axis, adjust c parameter

### Graphite
- Hexagonal, a=b≈2.46Å, c≈6.71Å (ABA stacking)
- Fully ordered: sharp XRD peaks
- Turbostratic (random stacking): broadened peaks

### Defects
- Point defects: reduce peak intensity
- Stacking faults: create satellite peaks, peak broadening
- Disorder: smooths XRD pattern, increases total scattering intensity

## Workflow
1. Ask user to describe the structure (if not already provided)
2. Generate CIF based on the description
3. Call the CLI tool: `carbon-xrd generate-pattern --cif <file> --output results/`
4. Interpret the results:
   - Show PNG visualizations
   - Point out key features in XRD (peak positions, widths, intensities)
   - Compare with expected patterns (e.g., "This peak broadening indicates disorder")
5. Offer refinement options: "Would you like to adjust defect density? Parameters?"

## Key Knowledge
- **2θ angle**: X-ray scattering angle, related to d-spacing by Bragg's law
- **d-spacing**: Atomic layer separation, inversely related to 2θ
- **Peak broadening**: Indicates disorder, defects, or small crystallite size
- **S(Q) total scattering**: Reveals short-range order and pair correlations
- **PDF G(r)**: Shows atomic pair distances, useful for amorphous materials

## Constraints
- CIF must be physically reasonable (positive volume, sensible lattice constants)
- XRD calculation uses Cu Kα radiation (λ=1.54184 Å) by default
- PDF calculation is simplified (Debye approximation)
```

## 5. プラグイン・アクション設定

### Action: GenerateXRDPattern

**入力スキーマ**:
```json
{
  "type": "object",
  "properties": {
    "cif_content": {
      "type": "string",
      "description": "CIF file content (structure definition)"
    },
    "include_pdf": {
      "type": "boolean",
      "description": "Include pair distribution function (default: false)"
    },
    "peak_threshold": {
      "type": "number",
      "description": "Peak detection threshold in % (default: 1.0)"
    }
  },
  "required": ["cif_content"]
}
```

**出力スキーマ**:
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean"
    },
    "xrd_plot": {
      "type": "string",
      "description": "Base64-encoded XRD pattern PNG"
    },
    "total_scattering_plot": {
      "type": "string",
      "description": "Base64-encoded S(Q) plot PNG"
    },
    "pdf_plot": {
      "type": "string",
      "description": "Base64-encoded G(r) plot PNG (if requested)"
    },
    "peaks_data": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "2theta": {"type": "number"},
          "d_spacing": {"type": "number"},
          "intensity": {"type": "number"}
        }
      }
    },
    "message": {
      "type": "string",
      "description": "Summary and interpretation of results"
    }
  }
}
```

## 6. Capabilities Configuration

### CIF Generator (LLM-based)
- **Input**: User's text description
- **Processing**: LLM generates CIF structure
- **Output**: CIF file string
- **Example**:
  - Input: "Graphite with 10% random stacking"
  - Output: CIF file with modified c-axis and atom positions

### XRD Calculator
- **Input**: CIF structure
- **Processing**: Bragg's law, intensity calculation
- **Output**: 2θ, intensity, d-spacing

### Total Scattering
- **Input**: CIF structure
- **Processing**: S(Q) calculation, G(r) derivation
- **Output**: Q vs S(Q), r vs G(r)

## 7. テスト用構造記述例

```
例1: 「完全グラファイト」
- Hexagonal crystal, a=2.46Å, c=6.71Å
- ABA stacking
- Expected: Sharp (002), (004), (100), (101) peaks

例2: 「欠陥あるグラフェン」
- Single layer, a=2.46Å, c=10Å
- 20% point defects on carbon atoms
- Expected: Broad (002) peak, reduced intensity

例3: 「乱層グラファイト」
- Multiple layers, random stacking
- a=2.46Å, variable c
- Expected: Broad (002), enhanced total scattering
```

## 8. 実装ステップ

1. **Manifest作成**: declarativeAgent.json with instructions
2. **Action実装**: CLI呼び出しロジック
3. **CIF生成プロンプト**: 正確な結晶パラメータ推定用
4. **UI/UX**: 結果表示、ダウンロード機能
5. **テスト**: 各構造タイプでの動作確認
6. **デプロイ**: Copilot App で公開

## 9. セキュリティ・制限事項

- **CIF検証**: 不正なCIFを拒否
- **実行タイムアウト**: 計算時間上限設定（デフォルト: 30秒）
- **出力サイズ**: PNG / CSV ファイルサイズ制限
- **ユーザー認証**: 必要に応じてログイン要求
