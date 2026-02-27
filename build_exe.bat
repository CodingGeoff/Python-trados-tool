@echo off
chcp 65001 >nul
echo ==========================================
echo   全能术语转换中心 - 打包工具
echo ==========================================
echo.

:: 检查是否在虚拟环境中
if "%VIRTUAL_ENV%"=="" (
    echo [提示] 正在激活虚拟环境...
    call venv\Scripts\activate.bat
)

echo [步骤 1/3] 清理旧构建文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /f /q "*.spec"

echo [步骤 2/3] 正在打包 EXE (这可能需要几分钟)...
echo.

pyinstaller ^
    --name "TermConverter" ^
    --onefile ^
    --windowed ^
    --icon NONE ^
    --add-data "venv\Lib\site-packages\pandas;pandas" ^
    --add-data "venv\Lib\site-packages\openpyxl;openpyxl" ^
    --collect-all pandas ^
    --collect-all openpyxl ^
    --collect-all numpy ^
    --hidden-import pandas ^
    --hidden-import openpyxl ^
    --hidden-import numpy ^
    --hidden-import xml.etree.ElementTree ^
    --hidden-import tkinter ^
    --hidden-import tkinter.filedialog ^
    --hidden-import tkinter.messagebox ^
    --hidden-import tkinter.ttk ^
    --clean ^
    --noconfirm ^
    multiterm-convert.py

if %errorlevel% neq 0 (
    echo.
    echo [错误] 打包失败！请检查错误信息。
    pause
    exit /b 1
)

echo.
echo [步骤 3/3] 打包完成！
echo ==========================================
echo 输出文件: dist\TermConverter.exe
echo ==========================================
echo.
echo 提示: 将此 EXE 文件复制到任意 Windows 电脑即可直接运行，无需安装 Python。
echo.
pause
