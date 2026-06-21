@echo off
setlocal enabledelayedexpansion
title NGXSMK GameNet Optimizer Installer
cd /d "%~dp0"

echo ================================================
echo   NGXSMK GameNet Optimizer - Setup
echo   Free ^| Open Source ^| Windows 10/11
echo ================================================
echo.

REM Detect architecture
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    set ARCH=x64
) else if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    set ARCH=x86
) else (
    set ARCH=x64
)
echo [INFO] Detected system: %ARCH%-bit Windows
echo.

REM Check if EXE already exists
set EXE_NAME=NGXSMK_GameNet_Optimizer_%ARCH%.exe
if exist "%EXE_NAME%" (
    echo [INFO] %EXE_NAME% already exists in this folder.
    echo   To re-download, delete the file first and run this again.
    echo.
    choice /C YN /M "Launch %EXE_NAME% now"
    if !errorlevel!==1 (
        start "" "%EXE_NAME%"
    )
    goto :eof
)

REM Download from GitHub releases
echo [STEP 1/2] Downloading GameNet Optimizer (%ARCH%-bit)...
set DOWNLOAD_URL=https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/releases/latest/download/%EXE_NAME%

echo   URL: %DOWNLOAD_URL%
echo.

REM Try PowerShell first (Windows 10+), fall back to curl
powershell -Command "& { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%EXE_NAME%' -UseBasicParsing -ErrorAction Stop; Write-Host '  Downloaded successfully' } catch { exit 1 } }"
if errorlevel 1 (
    echo   PowerShell download failed, trying curl...
    curl -L -o "%EXE_NAME%" "%DOWNLOAD_URL%" --fail --silent --show-error
    if errorlevel 1 (
        echo.
        echo [ERROR] Download failed. Check your internet connection or download manually:
        echo   https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/releases/latest
        pause
        exit /b 1
    )
)

REM Verify download
if not exist "%EXE_NAME%" (
    echo [ERROR] Downloaded file not found.
    pause
    exit /b 1
)
for %%I in ("%EXE_NAME%") do set FILE_SIZE=%%~zI
set /A SIZE_MB=!FILE_SIZE! / 1048576
echo [OK] Downloaded !SIZE_MB! MB
echo.

REM Unblock the file (removes SmartScreen warning for this file)
echo [STEP 2/2] Unblocking file...
powershell -Command "Unblock-File -Path '%EXE_NAME%' -ErrorAction SilentlyContinue; Write-Host '  Done'"
echo.

echo ================================================
echo   INSTALLATION COMPLETE
echo ================================================
echo.
echo   File: %EXE_NAME% (!SIZE_MB! MB)
echo   Location: %CD%
echo.
echo   Launching the optimizer now...
echo   Tip: Right-click the EXE ^> Properties ^> Unblock if SmartScreen appears.
echo.
start "" "%EXE_NAME%"
echo.
echo   If the application doesn't open automatically,
echo   double-click "%EXE_NAME%" in this folder.
echo.
pause
