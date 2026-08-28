@echo off
REM Carbon XRD Structure Tool - Quick Setup Script for Windows
REM このスクリプトで環境を自動セットアップできます

echo =========================================
echo Carbon XRD Structure Tool Setup
echo =========================================
echo.

REM Python バージョン確認
echo [CHECK] Verifying Python installation...
python --version
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from https://www.python.org
    pause
    exit /b 1
)

REM 依存パッケージをインストール
echo.
echo [INSTALL] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM 環境変数を設定
set PYTHONPATH=%CD%\src
set PYTHONIOENCODING=utf-8

REM テストを実行
echo.
echo [TEST] Running test suite...
python -m pytest tests/test_carbon_xrd.py -v
if errorlevel 1 (
    echo.
    echo ERROR: Tests failed
    pause
    exit /b 1
)

echo.
echo SETUP completed successfully!
echo.
echo Next steps:
echo.
echo 1. Try the CLI:
echo    python -m carbon_xrd.cli generate-pattern --cif tests/graphene.cif --output results/
echo.
echo 2. Start the API server:
echo    python -m carbon_xrd.api_server
echo.
echo 3. Deploy to M365 Copilot:
echo    atk provision --env local
echo.
pause
