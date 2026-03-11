"""
Simple Advanced Build Script
Builds the advanced NGXSMK GameNet Optimizer without Unicode issues
"""

import os
import sys
import subprocess
import shutil

def build_advanced_executable():
    """Build the advanced executable with all features"""
    
    print("Building Advanced NGXSMK GameNet Optimizer...")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"PyInstaller found: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Clean previous builds
    print("Cleaning previous builds...")
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   Removed {folder}/")
    
    # PyInstaller command with advanced options
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name=NGXSMK_GameNet_Optimizer_Advanced",  # Executable name
        "--add-data=modules;modules",   # Include modules directory
        "--hidden-import=psutil",       # Hidden imports
        "--hidden-import=pywin32",
        "--hidden-import=ping3",
        "--hidden-import=threading",
        "--hidden-import=json",
        "--hidden-import=datetime",
        "--hidden-import=subprocess",
        "--hidden-import=platform",
        "--hidden-import=os",
        "--hidden-import=time",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.scrolledtext",
        "--exclude-module=speedtest",    # Exclude problematic modules
        "--exclude-module=matplotlib",
        "--exclude-module=numpy",
        "--exclude-module=netifaces",
        "--exclude-module=wmi",
        "--clean",                      # Clean build
        "--noconfirm",                  # Don't ask for confirmation
        "main.py"                       # Main script
    ]
    
    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("Build completed successfully!")
        print("\nOutput files:")
        
        # Check if executable was created
        exe_path = "dist/NGXSMK_GameNet_Optimizer_Advanced.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"   Executable: {exe_path} ({size_mb:.1f} MB)")
        else:
            print("   Executable not found!")
        
        # List all files in dist directory
        if os.path.exists("dist"):
            print("\nAll files in dist/:")
            for root, dirs, files in os.walk("dist"):
                for file in files:
                    file_path = os.path.join(root, file)
                    size_kb = os.path.getsize(file_path) / 1024
                    print(f"   {file_path} ({size_kb:.1f} KB)")
        
        print("\nAdvanced build completed successfully!")
        print("You can now run the executable from the dist/ folder")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        print(f"   Return code: {e.returncode}")
        if e.stdout:
            print(f"   stdout: {e.stdout}")
        if e.stderr:
            print(f"   stderr: {e.stderr}")
        return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("NGXSMK GameNet Optimizer - Advanced Builder")
    print("=" * 50)
    
    # Build the executable
    success = build_advanced_executable()
    
    if success:
        print("\nAdvanced build completed successfully!")
        print("Check the dist/ folder for your executable")
    else:
        print("\nBuild failed. Check the error messages above.")
        sys.exit(1)
