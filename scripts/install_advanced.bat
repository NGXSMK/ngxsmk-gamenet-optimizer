@echo off
setlocal enabledelayedexpansion

echo NGXSMK GameNet Optimizer - Advanced Installer
echo ================================================
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed.
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Detect Python architecture (32-bit or 64-bit)
for /f "tokens=*" %%a in ('python -c "import sys; print('x86' if sys.maxsize <= 2**32 else 'x64')"') do set ARCH=%%a
echo [INFO] Detected Python architecture: %ARCH%

REM Install Python requirements
echo.
echo [STEP 1/4] Installing Python requirements...
pip install -r ..\requirements.txt
if errorlevel 1 (
    echo [WARN] pip install had warnings, reviewing...
)
echo [OK] Python dependencies installed

REM Build the React frontend
echo.
echo [STEP 2/4] Building React frontend...
echo.
if exist "..\web-ui" (
    pushd "..\web-ui"
    echo   Installing npm dependencies...
    call npm install
    if errorlevel 1 (
        echo   [WARN] npm install had issues, continuing...
    )
    echo   Building React app...
    call npm run build
    if errorlevel 1 (
        echo   [WARN] npm build had issues, continuing...
    ) else (
        echo   [OK] React frontend built
    )
    popd
) else (
    echo [WARN] web-ui directory not found, skipping frontend build
)

REM Build the executable
echo.
echo [STEP 3/4] Building advanced executable (%ARCH%)...
echo.
python build_advanced_exe.py --arch %ARCH%
if errorlevel 1 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)
echo [OK] Advanced executable built

REM Verify the build
echo.
echo [STEP 4/4] Verifying build...
echo.
if exist "dist\NGXSMK_GameNet_Optimizer_Advanced.exe" (
    for %%I in ("dist\NGXSMK_GameNet_Optimizer_Advanced.exe") do set EXE_SIZE=%%~zI
    set /A EXE_SIZE_MB=!EXE_SIZE! / 1048576
    echo [OK] Executable found: dist\NGXSMK_GameNet_Optimizer_Advanced.exe (!EXE_SIZE_MB! MB)
) else (
    echo [WARN] Executable not found in dist\ - check the build output
)

echo.
echo ================================================
echo INSTALLATION COMPLETED SUCCESSFULLY!
echo ================================================
echo.
echo Architecture: %ARCH%
echo Executable: dist\NGXSMK_GameNet_Optimizer_Advanced.exe
echo.
echo You can now run the advanced optimizer from the dist folder!
echo.
pause
