@echo off
setlocal enabledelayedexpansion

echo NGXSMK GameNet Optimizer - Windows Executable Builder
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Detect Python architecture (32-bit or 64-bit)
for /f "tokens=*" %%a in ('python -c "import sys; print('x86' if sys.maxsize <= 2**32 else 'x64')"') do set ARCH=%%a
echo [INFO] Detected Python architecture: %ARCH%

REM Build the React frontend
echo.
echo [STEP 1/4] Building React frontend...
echo.
if exist "..\web-ui" (
    pushd "..\web-ui"
    echo   [1/2] Installing npm dependencies...
    call npm install
    if errorlevel 1 (
        echo   [WARN] npm install had issues, continuing...
    )
    echo   [2/2] Building React app...
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

REM Install PyInstaller
echo.
echo [STEP 2/4] Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller
    pause
    exit /b 1
)
echo [OK] PyInstaller ready

REM Build the executable
echo.
echo [STEP 3/4] Building executable (%ARCH%)...
echo.
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name=NGXSMK_GameNet_Optimizer ^
    --paths="..\src" ^
    --add-data="..\src\ngx_optimizer\modules;ngx_optimizer\modules" ^
    --hidden-import=psutil ^
    --hidden-import=flask ^
    --hidden-import=flask_cors ^
    --hidden-import=werkzeug ^
    --hidden-import=werkzeug.serving ^
    --hidden-import=werkzeug.routing ^
    --hidden-import=werkzeug.exceptions ^
    --hidden-import=click ^
    --hidden-import=jinja2 ^
    --hidden-import=itsdangerous ^
    --hidden-import=win32api ^
    --hidden-import=win32con ^
    --hidden-import=win32process ^
    --hidden-import=pywintypes ^
    --hidden-import=speedtest ^
    --hidden-import=ping3 ^
    --hidden-import=tkinter ^
    --hidden-import=netifaces ^
    --hidden-import=pkg_resources ^
    --hidden-import=ngx_optimizer ^
    --hidden-import=ngx_optimizer.modules ^
    --hidden-import=ngx_optimizer.modules.ram_cleaner ^
    --hidden-import=ngx_optimizer.modules.system_monitor ^
    --hidden-import=ngx_optimizer.modules.config_manager ^
    --hidden-import=ngx_optimizer.modules.fps_boost ^
    --hidden-import=ngx_optimizer.modules.network_optimizer ^
    --hidden-import=ngx_optimizer.modules.gaming_optimizer ^
    --hidden-import=ngx_optimizer.modules.network_analyzer ^
    --hidden-import=ngx_optimizer.modules.neural_intelligence ^
    --hidden-import=ngx_optimizer.modules.learning_core ^
    --hidden-import=ngx_optimizer.modules.hardware_controller ^
    --hidden-import=ngx_optimizer.modules.network_evolution ^
    --hidden-import=ngx_optimizer.modules.cloud_link ^
    --hidden-import=ngx_optimizer.modules.ecosystem_integration ^
    --hidden-import=ngx_optimizer.modules.traffic_shaper ^
    --hidden-import=ngx_optimizer.modules.multi_internet ^
    --hidden-import=ngx_optimizer.modules.lol_optimizer ^
    --hidden-import=ngx_optimizer.modules.advanced_optimizer ^
    --hidden-import=ngx_optimizer.modules.compat ^
    --hidden-import=ngx_optimizer.core_config ^
    --clean ^
    --noconfirm ^
    ..\src\ngx_optimizer\api.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed! Check the error messages above.
    pause
    exit /b 1
)

REM Add web-ui/dist if it exists
if exist "..\web-ui\dist" (
    echo [STEP 4/4] Including web frontend assets...
    xcopy /E /I /Y "..\web-ui\dist" "dist\web-ui\dist" >nul 2>&1
    echo [OK] Web frontend assets included
) else (
    echo [STEP 4/4] Skipped - no web frontend build to include
)

echo.
echo ====================================================
echo [OK] BUILD COMPLETED SUCCESSFULLY!
echo ====================================================
echo.
echo Output: dist\NGXSMK_GameNet_Optimizer.exe
echo Architecture: %ARCH%
echo.
echo To run the executable:
echo    1. Navigate to the 'dist' folder
echo    2. Run 'NGXSMK_GameNet_Optimizer.exe'
echo.
echo For distribution:
echo    - Copy the entire 'dist' folder
echo    - Users can run the .exe file directly
echo.
pause
