#!/usr/bin/env python3
"""
Fixed build script for Windows executable
Excludes problematic modules for PyInstaller compatibility
"""

import subprocess
import sys
import os

def main():
    """Fixed build process"""
    print("🚀 Building NGXSMK GameNet Optimizer Executable (Fixed)")
    print("=" * 60)
    
    # Install PyInstaller if needed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    # Build command with exclusions for problematic modules
    build_cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                    # Single executable file
        '--windowed',                   # No console window
        '--name=NGXSMK_GameNet_Optimizer',
        '--add-data=modules;modules',   # Include modules folder
        '--hidden-import=psutil',
        '--hidden-import=tkinter',
        '--hidden-import=ping3',
        '--exclude-module=speedtest',   # Exclude problematic speedtest
        '--exclude-module=matplotlib',  # Exclude matplotlib for smaller size
        '--exclude-module=numpy',       # Exclude numpy for smaller size
        '--exclude-module=netifaces',   # Exclude netifaces
        '--clean',                      # Clean build
        'main.py'
    ]
    
    print("🔨 Building executable (excluding problematic modules)...")
    print("Command:", ' '.join(build_cmd))
    
    try:
        subprocess.check_call(build_cmd)
        print("\n✅ Build completed successfully!")
        print("\n📁 Output: dist/NGXSMK_GameNet_Optimizer.exe")
        print("\n🚀 To run: Navigate to 'dist' folder and run the .exe file")
        print("\n💡 Note: Some advanced features may be limited in the executable version")
        print("   - Speedtest functionality will use alternative methods")
        print("   - Some network analysis features may be simplified")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        print("\n💡 Try running: pip install pyinstaller")
        print("   Then run this script again")

if __name__ == "__main__":
    main()
