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

def print_banner():
    """Print build banner"""
    print("=" * 60)
    print("🚀 NGXSMK GameNet Optimizer - Local Builder")
    print("=" * 60)
    print()

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 13):
        print("❌ Python 3.13+ required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check if PyInstaller is available
    try:
        import PyInstaller # type: ignore
        print(f"✅ PyInstaller {PyInstaller.__version__} available")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed")
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ main.py not found")
        return False
    print("✅ main.py found")
    
    # Check if modules directory exists
    if not os.path.exists("modules"):
        print("❌ modules directory not found")
        return False
    print("✅ modules directory found")
    
    return True

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous builds...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Cleaned {dir_name}")
    
    # Clean .pyc files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".pyc"):
                os.remove(os.path.join(root, file))
    
    print("✅ Build cleanup completed")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("Trying minimal installation...")
        try:
            minimal_deps = ["psutil", "pywin32", "ping3", "pyinstaller"]
            for dep in minimal_deps:
                subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                              check=True, capture_output=True, text=True)
            print("✅ Minimal dependencies installed")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install minimal dependencies")
            return False

def build_executable():
    """Build the executable"""
    print("🔨 Building executable...")
    
    try:
        # Use the existing build script
        subprocess.run([sys.executable, "build_simple_advanced.py"], 
                       capture_output=True, text=True, check=True)
        print("✅ Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def test_executable():
    """Test the built executable"""
    print("🧪 Testing executable...")
    
    exe_path = "dist/NGXSMK_GameNet_Optimizer_Advanced.exe"
    if not os.path.exists(exe_path):
        print("❌ Executable not found")
        return False
    
    # Check file size
    file_size = os.path.getsize(exe_path)
    print(f"📊 Executable size: {file_size / (1024*1024):.1f} MB")
    
    if file_size < 5 * 1024 * 1024:  # Less than 5MB
        print("⚠️  Warning: Executable size seems small")
    else:
        print("✅ Executable size is reasonable")
    
    print("✅ Executable test completed")
    return True

def create_build_info():
    """Create build information file"""
    print("📝 Creating build information...")
    
    build_info = f"""# NGXSMK GameNet Optimizer - Build Information

## Build Details
- **Build Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **Python Version**: {sys.version}
- **Platform**: {sys.platform}
- **Build Type**: Local Development

## Files
- **Executable**: dist/NGXSMK_GameNet_Optimizer_Advanced.exe
- **Size**: {os.path.getsize('dist/NGXSMK_GameNet_Optimizer_Advanced.exe') / (1024*1024):.1f} MB

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
**Made with ❤️ for the gaming community**
"""
    
    with open("BUILD_INFO.md", "w", encoding="utf-8") as f:
        f.write(build_info)
    
    print("✅ Build information created")

def main():
    """Main build process"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed")
        return 1
    
    # Clean previous builds
    clean_build()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed")
        return 1
    
    # Build executable
    if not build_executable():
        print("❌ Build failed")
        return 1
    
    # Test executable
    if not test_executable():
        print("❌ Executable test failed")
        return 1
    
    # Create build info
    create_build_info()
    
    print("\n" + "=" * 60)
    print("🎉 BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("📁 Executable: dist/NGXSMK_GameNet_Optimizer_Advanced.exe")
    print(f"📊 Size: {os.path.getsize('dist/NGXSMK_GameNet_Optimizer_Advanced.exe') / (1024*1024):.1f} MB")
    print("📝 Build Info: BUILD_INFO.md")
    print("\n🚀 Ready to optimize your gaming experience!")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
