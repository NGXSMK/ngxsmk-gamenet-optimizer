#!/usr/bin/env python3
"""
Simple build script for Windows executable
One-command build for NGXSMK GameNet Optimizer
"""

import subprocess
import sys
import os

def main():
    """Simple build process"""
    print("🚀 Building NGXSMK GameNet Optimizer Executable")
    print("=" * 50)
    
    # Install PyInstaller if needed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    # Build command
    build_cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                    # Single executable file
        '--windowed',                   # No console window
        '--name=NGXSMK_GameNet_Optimizer',
        '--add-data=modules;modules',   # Include modules folder
        '--hidden-import=psutil',
        '--hidden-import=tkinter',
        '--hidden-import=ping3',
        '--hidden-import=speedtest',
        '--hidden-import=matplotlib',
        '--hidden-import=numpy',
        '--clean',                      # Clean build
        'main.py'
    ]
    
    print("🔨 Building executable...")
    print("Command:", ' '.join(build_cmd))
    
    try:
        subprocess.check_call(build_cmd)
        print("\n✅ Build completed successfully!")
        print("\n📁 Output: dist/NGXSMK_GameNet_Optimizer.exe")
        print("\n🚀 To run: Navigate to 'dist' folder and run the .exe file")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        print("\n💡 Try running: pip install pyinstaller")
        print("   Then run this script again")

if __name__ == "__main__":
    main()
