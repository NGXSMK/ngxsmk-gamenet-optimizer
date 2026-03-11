#!/usr/bin/env python3
"""
Simple installation script for NGXSMK GameNet Optimizer
Handles dependency installation with fallbacks
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package with error handling"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        return True
    except subprocess.CalledProcessError:
        print(f"⚠️  Failed to install {package}")
        return False

def main():
    print("🚀 NGXSMK GameNet Optimizer - Simple Installer")
    print("=" * 50)
    
    # Core required packages
    core_packages = [
        'psutil',
        'pywin32'
    ]
    
    # Optional packages (will work without these)
    optional_packages = [
        'speedtest-cli',
        'ping3',
        'matplotlib',
        'numpy'
    ]
    
    print("📦 Installing core packages...")
    core_success: int = 0
    for package in core_packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed successfully")
            core_success = core_success + 1 # pyre-ignore[58]
        else:
            print(f"❌ {package} installation failed")
    
    print("\n📦 Installing optional packages...")
    optional_success: int = 0
    for package in optional_packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed successfully")
            optional_success = optional_success + 1 # pyre-ignore[58]
        else:
            print(f"⚠️  {package} installation failed (optional)")
    
    print("\n" + "=" * 50)
    print("📊 Installation Summary:")
    print(f"Core packages: {core_success}/{len(core_packages)}")
    print(f"Optional packages: {optional_success}/{len(optional_packages)}")
    
    if core_success == len(core_packages):
        print("\n✅ Core installation successful!")
        print("🎮 You can now run NGXSMK GameNet Optimizer with: python launcher.py")
    else:
        print("\n❌ Core installation failed!")
        print("Please check the error messages above.")
        return False
    
    if optional_success < len(optional_packages):
        print("\n⚠️  Some optional features may not be available")
        print("The application will work with reduced functionality.")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Installation interrupted by user")
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
