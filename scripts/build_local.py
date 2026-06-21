#!/usr/bin/env python3
"""
Local Build Script for NGXSMK GameNet Optimizer
Builds the executable locally for development and testing
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent


def print_banner():
    """Print build banner"""
    print("=" * 60)
    print("NGXSMK GameNet Optimizer - Local Builder")
    print("=" * 60)
    print()


def check_requirements():
    """Check if all requirements are met"""
    print("Checking requirements...")

    if sys.version_info < (3, 8):
        print("[ERROR] Python 3.8+ required")
        return False

    print(f"[OK] Python {sys.version_info.major}.{sys.version_info.minor} detected")

    try:
        import PyInstaller
        print(f"[OK] PyInstaller {PyInstaller.__version__} available")
    except ImportError:
        print("[ERROR] PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("[OK] PyInstaller installed")

    api_path = PROJECT_ROOT / "src" / "ngx_optimizer" / "api.py"
    if not api_path.exists():
        print(f"[ERROR] {api_path} not found")
        return False
    print(f"[OK] {api_path} found")

    modules_dir = PROJECT_ROOT / "src" / "ngx_optimizer" / "modules"
    if not modules_dir.is_dir():
        print(f"[ERROR] {modules_dir} not found")
        return False
    print(f"[OK] {modules_dir} found")

    return True


def clean_build():
    """Clean previous build artifacts"""
    print("Cleaning previous builds...")

    for dir_name in ["build", "dist", "__pycache__"]:
        dir_path = PROJECT_ROOT / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"[OK] Cleaned {dir_name}")

    for root, dirs, files in os.walk(str(PROJECT_ROOT)):
        for file in files:
            if file.endswith(".pyc"):
                os.remove(os.path.join(root, file))

    print("[OK] Build cleanup completed")


def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")

    req_file = PROJECT_ROOT / "requirements.txt"
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_file)],
                       check=True, capture_output=True, text=True)
        print("[OK] Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install dependencies: {e}")
        print("Trying minimal installation...")
        try:
            minimal_deps = ["psutil", "pywin32", "ping3", "pyinstaller"]
            for dep in minimal_deps:
                subprocess.run([sys.executable, "-m", "pip", "install", dep],
                               check=True, capture_output=True, text=True)
            print("[OK] Minimal dependencies installed")
            return True
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to install minimal dependencies")
            return False


def build_executable():
    """Build the executable"""
    print("Building executable...")

    build_script = SCRIPT_DIR / "build_advanced_exe.py"
    if not build_script.exists():
        print(f"[ERROR] {build_script} not found")
        return False

    try:
        subprocess.run([sys.executable, str(build_script)],
                       cwd=str(SCRIPT_DIR), check=True)
        print("[OK] Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed: {e}")
        return False


def test_executable():
    """Test the built executable"""
    print("Testing executable...")

    exe_path = SCRIPT_DIR / "dist" / "NGXSMK_GameNet_Optimizer_Advanced.exe"
    if not exe_path.exists():
        print(f"[ERROR] Executable not found at {exe_path}")
        return False

    file_size = os.path.getsize(exe_path)
    print(f"Executable size: {file_size / (1024*1024):.1f} MB")

    if file_size < 5 * 1024 * 1024:
        print("[WARN]  Warning: Executable size seems small")
    else:
        print("[OK] Executable size is reasonable")

    print("[OK] Executable test completed")
    return True


def create_build_info():
    """Create build information file"""
    print("Creating build information...")

    exe_path = SCRIPT_DIR / "dist" / "NGXSMK_GameNet_Optimizer_Advanced.exe"
    exe_size = os.path.getsize(exe_path) / (1024 * 1024) if exe_path.exists() else 0

    build_info = f"""# NGXSMK GameNet Optimizer - Build Information

## Build Details
- **Build Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **Python Version**: {sys.version}
- **Platform**: {sys.platform}
- **Build Type**: Local Development

## Files
- **Executable**: {exe_path}
- **Size**: {exe_size:.1f} MB

## Usage
1. Run the executable: `NGXSMK_GameNet_Optimizer_Advanced.exe`
2. The application will start in fullscreen mode by default
3. Use F11 to toggle fullscreen mode
4. Use the sidebar for quick actions

## Features
- FPS Boost & Game Optimization
- Network Analysis & Multi-Internet
- Traffic Shaping & RAM Cleaning
- League of Legends Server Testing
- Advanced System Monitoring
- Real-time Performance Tracking

## Support
- **GitHub**: https://github.com/NGXSMK/ngxsmk-gamenet-optimizer
- **Email**: sachindilshan040@gmail.com
- **Maintainer**: @NGXSMK

---
**Made for the gaming community**
"""

    with open(PROJECT_ROOT / "BUILD_INFO.md", "w", encoding="utf-8") as f:
        f.write(build_info)

    print("[OK] Build information created")


def main():
    """Main build process"""
    print_banner()

    if not check_requirements():
        print("[ERROR] Requirements check failed")
        return 1

    clean_build()

    if not install_dependencies():
        print("[ERROR] Dependency installation failed")
        return 1

    if not build_executable():
        print("[ERROR] Build failed")
        return 1

    if not test_executable():
        print("[ERROR] Executable test failed")
        return 1

    create_build_info()

    print("\n" + "=" * 60)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Executable: scripts/dist/NGXSMK_GameNet_Optimizer_Advanced.exe")
    exe_path = SCRIPT_DIR / "dist" / "NGXSMK_GameNet_Optimizer_Advanced.exe"
    if exe_path.exists():
        print(f"Size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
    print("Build Info: BUILD_INFO.md")
    print("\nReady to optimize your gaming experience!")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
