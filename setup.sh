#!/bin/bash
# Carbon XRD Structure Tool - Quick Setup Script
# このスクリプトで環境を自動セットアップできます

echo "========================================="
echo "Carbon XRD Structure Tool Setup"
echo "========================================="
echo ""

# Python バージョン確認
echo "[CHECK] Verifying Python installation..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "  Python version: $python_version"

# 依存パッケージをインストール
echo ""
echo "[INSTALL] Installing dependencies..."
pip install -r requirements.txt

# テストを実行
echo ""
echo "[TEST] Running test suite..."
export PYTHONPATH="${PWD}/src"
python -m pytest tests/test_carbon_xrd.py -v

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Try the CLI:"
    echo "   export PYTHONPATH=\"\${PWD}/src\""
    echo "   python -m carbon_xrd.cli generate-pattern --cif tests/graphene.cif --output results/"
    echo ""
    echo "2. Start the API server:"
    echo "   python -m carbon_xrd.api_server"
    echo ""
    echo "3. Deploy to M365 Copilot:"
    echo "   atk provision --env local"
    echo ""
else
    echo ""
    echo "✗ Setup failed. Please check the error messages above."
    exit 1
fi
