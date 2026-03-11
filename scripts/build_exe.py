#!/usr/bin/env python3
"""
Build script for creating Windows executable
Converts NGXSMK GameNet Optimizer to standalone .exe file
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False

def create_spec_file():
    """Create PyInstaller spec file for the application"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('modules', 'modules'),
        ('README.md', '.'),
        ('LICENSE', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'psutil',
        'tkinter',
        'threading',
        'socket',
        'time',
        'json',
        'subprocess',
        'platform',
        'ping3',
        'speedtest',
        'netifaces',
        'matplotlib',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NGXSMK_GameNet_Optimizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('ngxsmk_gamenet_optimizer.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ PyInstaller spec file created")

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...")
    
    try:
        # Build using the spec file
        subprocess.check_call([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            'ngxsmk_gamenet_optimizer.spec'
        ])
        
        print("✅ Executable built successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def create_installer_script():
    """Create a simple installer script"""
    installer_content = '''@echo off
echo NGXSMK GameNet Optimizer - Installer
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Installation complete!
echo You can now run: NGXSMK_GameNet_Optimizer.exe
echo.
pause
'''
    
    with open('install.bat', 'w') as f:
        f.write(installer_content)
    
    print("✅ Installer script created")

def create_icon():
    """Create a simple icon file (placeholder)"""
    # This is a placeholder - you can replace with a real icon
    icon_content = '''# This is a placeholder for an icon file
# To add a real icon:
# 1. Create or find a .ico file
# 2. Save it as 'icon.ico' in the project root
# 3. The build script will automatically use it
'''
    
    with open('icon_placeholder.txt', 'w') as f:
        f.write(icon_content)
    
    print("ℹ️  Icon placeholder created (replace with real icon.ico for custom icon)")

def main():
    """Main build process"""
    print("🚀 NGXSMK GameNet Optimizer - Windows Executable Builder")
    print("=" * 60)
    
    # Check if we're on Windows
    if sys.platform != 'win32':
        print("⚠️  This script is designed for Windows")
        print("   For other platforms, use: python main.py")
        return
    
    # Install PyInstaller
    if not install_pyinstaller():
        return
    
    # Create spec file
    create_spec_file()
    
    # Create installer script
    create_installer_script()
    
    # Create icon placeholder
    create_icon()
    
    # Build executable
    if build_executable():
        print("\n🎉 Build completed successfully!")
        print("\n📁 Output files:")
        print("   - dist/NGXSMK_GameNet_Optimizer.exe (Main executable)")
        print("   - install.bat (Installer script)")
        print("\n🚀 To run the executable:")
        print("   1. Navigate to the 'dist' folder")
        print("   2. Run 'NGXSMK_GameNet_Optimizer.exe'")
        print("\n💡 For distribution:")
        print("   - Copy the entire 'dist' folder")
        print("   - Include 'install.bat' for dependency installation")
    else:
        print("\n❌ Build failed. Check the error messages above.")

if __name__ == "__main__":
    main()
