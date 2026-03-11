@echo off
echo NGXSMK GameNet Optimizer - Fixed Windows Executable Builder
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable (excluding problematic modules)...
echo.

REM Build the executable with exclusions
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name=NGXSMK_GameNet_Optimizer ^
    --add-data="modules;modules" ^
    --hidden-import=psutil ^
    --hidden-import=tkinter ^
    --hidden-import=ping3 ^
    --exclude-module=speedtest ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    --exclude-module=netifaces ^
    --clean ^
    main.py

if errorlevel 1 (
    echo.
    echo Build failed! Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo.
echo 📁 Output: dist\NGXSMK_GameNet_Optimizer.exe
echo.
echo 🚀 To run the executable:
echo    1. Navigate to the 'dist' folder
echo    2. Run 'NGXSMK_GameNet_Optimizer.exe'
echo.
echo 💡 Note: Some advanced features may be limited in the executable version
echo    - Speedtest functionality will use alternative methods
echo    - Some network analysis features may be simplified
echo.
pause
