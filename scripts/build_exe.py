#!/usr/bin/env python3
"""
Build script for creating Windows executable
Converts NGXSMK GameNet Optimizer to standalone .exe file
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("[OK] PyInstaller is already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("[OK] PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to install PyInstaller")
            return False

def build_frontend():
    """Build the React frontend"""
    web_ui_dir = PROJECT_ROOT / 'web-ui'
    if not web_ui_dir.is_dir():
        print("[WARN] web-ui directory not found, skipping frontend build")
        return False

    print("Building React frontend...")
    try:
        npm = 'npm.cmd' if sys.platform == 'win32' else 'npm'
        print("  [1/2] Installing npm dependencies...")
        subprocess.check_call([npm, 'install'], cwd=str(web_ui_dir), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("  [2/2] Building React app...")
        subprocess.check_call([npm, 'run', 'build'], cwd=str(web_ui_dir))
        print("[OK] React frontend built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[WARN] Frontend build failed (non-fatal): {e}")
        return False
    except FileNotFoundError:
        print("[WARN] npm not found, skipping frontend build")
        return False

def create_spec_file(arch='x64'):
    """Create PyInstaller spec file for the application"""
    datas = [
        ('../src/ngx_optimizer/modules', 'ngx_optimizer/modules'),
    ]

    for f_rel in ['../README.md', '../LICENSE']:
        f_abs = PROJECT_ROOT / f_rel.replace('../', '')
        if f_abs.exists():
            datas.append((f_rel, '.'))
        else:
            print(f"[WARN] {f_rel} not found, skipping")

    web_dist = PROJECT_ROOT / 'web-ui' / 'dist'
    if web_dist.is_dir():
        datas.append(('../web-ui/dist', 'web-ui/dist'))
        print("[INFO] Including web-ui/dist in bundle")
    else:
        print("[INFO] web-ui/dist not found (frontend will be unavailable in bundle)")

    datas_str = ',\n        '.join(repr(d) for d in datas)

    icon_ico = PROJECT_ROOT / 'icon.ico'
    if icon_ico.exists():
        icon_line = f"icon=r'{icon_ico}',"
    else:
        icon_line = 'icon=None,'

    if arch == 'x86':
        target_arch_line = "target_arch='x86',"
    else:
        target_arch_line = 'target_arch=None,'

    # Version info file
    version_file = SCRIPT_DIR / 'version_info.txt'
    manifest_file = SCRIPT_DIR / 'exe_manifest.xml'
    version_line = f"version='{version_file}'," if version_file.exists() else "version=None,"
    manifest_line = f"manifest='{manifest_file}'," if manifest_file.exists() else "manifest=None,"

    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../src/ngx_optimizer/api.py'],
    pathex=['../src'],
    binaries=[],
    datas=[
        {datas_str},
    ],
    hiddenimports=[
        'psutil',
        'flask',
        'flask_cors',
        'werkzeug',
        'werkzeug.serving',
        'werkzeug.routing',
        'werkzeug.exceptions',
        'click',
        'jinja2',
        'itsdangerous',
        'win32api',
        'win32con',
        'win32process',
        'pywintypes',
        'speedtest',
        'ping3',
        'tkinter',
        'netifaces',
        'pkg_resources',
        'threading',
        'socket',
        'time',
        'json',
        'subprocess',
        'platform',
        'ngx_optimizer',
        'ngx_optimizer.modules',
        'ngx_optimizer.modules.ram_cleaner',
        'ngx_optimizer.modules.system_monitor',
        'ngx_optimizer.modules.config_manager',
        'ngx_optimizer.modules.fps_boost',
        'ngx_optimizer.modules.network_optimizer',
        'ngx_optimizer.modules.gaming_optimizer',
        'ngx_optimizer.modules.network_analyzer',
        'ngx_optimizer.modules.neural_intelligence',
        'ngx_optimizer.modules.learning_core',
        'ngx_optimizer.modules.hardware_controller',
        'ngx_optimizer.modules.network_evolution',
        'ngx_optimizer.modules.cloud_link',
        'ngx_optimizer.modules.ecosystem_integration',
        'ngx_optimizer.modules.traffic_shaper',
        'ngx_optimizer.modules.multi_internet',
        'ngx_optimizer.modules.lol_optimizer',
        'ngx_optimizer.modules.advanced_optimizer',
        'ngx_optimizer.modules.compat',
        'ngx_optimizer.core_config',
    ],
    hookspath=[],
    hooksconfig={{}},
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
    {target_arch_line}
    {version_line}
    {manifest_line}
    codesign_identity=None,
    entitlements_file=None,
    {icon_line}
)
'''

    spec_path = SCRIPT_DIR / 'ngxsmk_gamenet_optimizer.spec'
    with open(spec_path, 'w') as f:
        f.write(spec_content)

    print("[OK] PyInstaller spec file created")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")

    try:
        subprocess.check_call([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            str(SCRIPT_DIR / 'ngxsmk_gamenet_optimizer.spec')
        ], cwd=str(SCRIPT_DIR))

        print("[OK] Executable built successfully!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed: {e}")
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
    echo Please install Python 3.8+ from https://python.org
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

    with open(SCRIPT_DIR / 'install.bat', 'w') as f:
        f.write(installer_content)

    print("[OK] Installer script created")

def create_icon():
    """Create a simple icon file (placeholder)"""
    with open(SCRIPT_DIR / 'icon_placeholder.txt', 'w') as f:
        f.write('''# This is a placeholder for an icon file
# To add a real icon:
# 1. Create or find a .ico file
# 2. Save it as 'icon.ico' in the project root
# 3. The build script will automatically use it
''')

    print("Icon placeholder created (replace with real icon.ico for custom icon)")

def main():
    """Main build process"""
    parser = argparse.ArgumentParser(description='Build NGXSMK GameNet Optimizer executable')
    parser.add_argument('--arch', choices=['x86', 'x64'], default='x64',
                        help='Target architecture (x86 for 32-bit, x64 for 64-bit, default: x64)')
    args = parser.parse_args()

    print("NGXSMK GameNet Optimizer - Windows Executable Builder")
    print("=" * 60)
    print(f"Target architecture: {args.arch}")

    if sys.platform != 'win32':
        print("[WARN] This script is designed for Windows")
        print("   For other platforms, use: python main.py")
        return

    build_frontend()

    if not install_pyinstaller():
        return

    create_spec_file(arch=args.arch)
    create_installer_script()
    create_icon()

    if build_executable():
        print("\nBuild completed successfully!")
        print(f"\nOutput file:")
        print(f"   scripts/dist/NGXSMK_GameNet_Optimizer.exe")
        print("\nTo run the executable:")
        print("   1. Navigate to the 'scripts/dist' folder")
        print("   2. Run 'NGXSMK_GameNet_Optimizer.exe'")
    else:
        print("\n[ERROR] Build failed. Check the error messages above.")

if __name__ == "__main__":
    main()
