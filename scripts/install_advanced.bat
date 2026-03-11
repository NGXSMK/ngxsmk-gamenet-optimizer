@echo off
echo NGXSMK GameNet Optimizer - Advanced Installer
echo ================================================
echo.

echo Installing advanced requirements...
pip install -r requirements_advanced.txt

echo.
echo Building advanced executable...
python build_advanced_exe.py

echo.
echo Advanced installation completed!
echo You can now run the advanced optimizer!
echo.
pause
