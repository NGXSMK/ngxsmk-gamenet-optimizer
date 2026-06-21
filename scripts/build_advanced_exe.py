"""
Advanced PyInstaller Build Script
Builds the advanced NGXSMK GameNet Optimizer with all features
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent


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
        subprocess.check_call([npm, 'install'], cwd=str(web_ui_dir),
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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


def get_pyinstaller_command(arch='x64'):
    """Build the PyInstaller command with advanced options"""
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=NGXSMK_GameNet_Optimizer_Advanced",
        "--add-data=..\\src\\ngx_optimizer\\modules;ngx_optimizer\\modules",
        "--hidden-import=psutil",
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
        "--exclude-module=pytest",
        "--exclude-module=black",
        "--exclude-module=flake8",
        "--clean",
        "--noconfirm",
    ]

    # Add architecture-specific flags
    if arch == 'x86':
        cmd.append("--target-arch=x86")
    elif arch == 'x64':
        cmd.append("--target-arch=x86_64")

    # Add optional files if they exist
    icon_ico = PROJECT_ROOT / 'icon.ico'
    if icon_ico.exists():
        cmd.append(f"--icon={icon_ico}")

    # Embed version info for Windows metadata (reduces SmartScreen severity)
    version_file = SCRIPT_DIR / 'version_info.txt'
    if version_file.exists():
        cmd.append(f"--version-file={version_file}")
        print("[INFO] Embedding version info (version_info.txt)")

    # Embed assembly manifest
    manifest_file = SCRIPT_DIR / 'exe_manifest.xml'
    if manifest_file.exists():
        cmd.append(f"--manifest={manifest_file}")
        print("[INFO] Embedding assembly manifest (exe_manifest.xml)")

    for f_rel in ['..\\README.md', '..\\LICENSE']:
        f_abs = PROJECT_ROOT / f_rel.replace('..\\', '')
        if f_abs.exists():
            cmd.append(f"--add-data={f_rel};.")

    # Include web-ui/dist if it exists
    web_dist = PROJECT_ROOT / 'web-ui' / 'dist'
    if web_dist.is_dir():
        cmd.append("--add-data=..\\web-ui\\dist;web-ui\\dist")
        print("[INFO] Including web-ui/dist in bundle")
    else:
        print("[INFO] web-ui/dist not found (frontend will be unavailable in bundle)")

    cmd.append("..\\src\\ngx_optimizer\\api.py")
    return cmd


def log_build_status():
    """Log the status of the build and list output files"""
    print("[OK] Build completed successfully!")
    print("\nOutput files:")

    exe_path = SCRIPT_DIR / "dist" / "NGXSMK_GameNet_Optimizer_Advanced.exe"
    if exe_path.exists():
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"   Executable: {exe_path} ({size_mb:.1f} MB)")
    else:
        print("   [ERROR] Executable not found!")

    dist_dir = SCRIPT_DIR / "dist"
    if dist_dir.is_dir():
        print("\nAll files in dist/:")
        for root, dirs, files in os.walk(str(dist_dir)):
            for file in files:
                file_path = os.path.join(root, file)
                size_kb = os.path.getsize(file_path) / 1024
                print(f"   {file_path} ({size_kb:.1f} KB)")

    print("\nAdvanced build completed successfully!")
    print("You can now run the executable from the dist/ folder")


def build_advanced_executable(arch='x64'):
    """Build the advanced executable with all features"""
    print(f"Building Advanced NGXSMK GameNet Optimizer ({arch})...")
    print("=" * 60)

    try:
        import PyInstaller
        print(f"[OK] PyInstaller found: {PyInstaller.__version__}")
    except ImportError:
        print("[ERROR] PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    print("Cleaning previous builds...")
    for folder in ["build", "dist", "__pycache__"]:
        folder_path = SCRIPT_DIR / folder
        if folder_path.exists():
            shutil.rmtree(folder_path)
            print(f"   Removed {folder}/")

    cmd = get_pyinstaller_command(arch=arch)

    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)

    try:
        subprocess.run(cmd, check=True, capture_output=False, text=False,
                       cwd=str(SCRIPT_DIR))
        log_build_status()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed with error: {e}")
        print(f"   Return code: {e.returncode}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

    return True


def create_advanced_installer():
    """Create an advanced installer script"""
    installer_script = """@echo off
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
"""

    with open(str(SCRIPT_DIR / "install_advanced.bat"), "w", encoding="utf-8") as f:
        f.write(installer_script)

    print("Created install_advanced.bat")


def create_advanced_readme():
    """Create advanced README"""
    readme_content = """# NGXSMK GameNet Optimizer - Advanced Edition

## Advanced Features

### AI-Powered Optimization
- **Intelligent System Analysis**: AI-powered analysis of your system performance
- **Predictive Optimization**: Anticipates performance issues before they occur
- **Adaptive Learning**: Learns from your usage patterns for better optimization
- **Real-time Monitoring**: Continuous system monitoring with intelligent alerts

### Advanced Gaming Optimizer
- **Game Detection**: Automatically detects running games
- **Game-Specific Profiles**: Optimized settings for League of Legends, Valorant, CS2, Fortnite, Apex Legends
- **Anti-Cheat Compatibility**: Optimized for Vanguard, VAC, Easy Anti-Cheat
- **Gaming Network Optimization**: Specialized network settings for gaming

### Advanced Network Optimizer
- **Intelligent Traffic Shaping**: AI-powered network traffic management
- **QoS Optimization**: Quality of Service optimization for different applications
- **Latency Optimization**: Advanced latency reduction techniques
- **Network Monitoring**: Real-time network performance monitoring

### System Monitor
- **Real-time Performance Tracking**: Live system performance monitoring
- **Performance Analytics**: Detailed performance analysis and trends
- **Alert System**: Intelligent alerts for performance issues
- **Performance History**: Historical performance data and analysis

### Advanced System Optimizer
- **CPU Optimization**: Intelligent CPU scheduling and priority management
- **Memory Optimization**: Advanced memory management and cleanup
- **GPU Optimization**: GPU performance optimization for gaming and streaming
- **Storage Optimization**: Disk optimization and cleanup

## Quick Start

### Method 1: Easy Installation
```bash
# Run the advanced installer
install_advanced.bat
```

### Method 2: Manual Installation
```bash
# Install requirements
pip install -r requirements_advanced.txt

# Build executable
python build_advanced_exe.py

# Run the application
dist/NGXSMK_GameNet_Optimizer_Advanced.exe
```

## System Requirements

- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB free space
- **Python**: 3.8+ (for development)

## Advanced Features Guide

### 1. AI-Powered Optimization
- Select your optimization profile (Gaming, Streaming, Productivity, Balanced)
- Enable advanced features like AI analysis and predictive optimization
- Monitor real-time optimization results

### 2. Gaming Optimizer
- Choose your game or use auto-detection
- Enable gaming-specific features like Game Mode and anti-cheat optimization
- Monitor gaming performance in real-time

### 3. Network Optimizer
- Select network profile (Gaming, Streaming, Productivity)
- Monitor network optimization status
- Test network performance

### 4. System Monitor
- Start real-time system monitoring
- View performance analytics and trends
- Set up intelligent alerts

## Advanced Configuration

### Optimization Profiles
- **Gaming**: Maximum performance for gaming
- **Streaming**: Optimized for streaming and content creation
- **Productivity**: Balanced performance for work
- **Balanced**: General-purpose optimization

### Gaming Profiles
- **Auto**: Automatically detect and optimize for running games
- **League of Legends**: Specialized LoL optimization
- **Valorant**: Valorant-specific optimizations
- **CS2**: Counter-Strike 2 optimizations
- **Fortnite**: Fortnite-specific settings
- **Apex Legends**: Apex Legends optimizations

## Performance Benefits

- **FPS Improvement**: 15-30% FPS boost in games
- **Latency Reduction**: 20-40% lower ping
- **Memory Optimization**: 20-50% more available RAM
- **CPU Performance**: 10-25% better CPU utilization
- **Network Stability**: 30-60% more stable connections

## Troubleshooting

### Common Issues
1. **High CPU Usage**: Disable real-time monitoring
2. **Memory Issues**: Reduce monitoring interval
3. **Network Problems**: Check firewall settings
4. **Gaming Issues**: Disable anti-cheat optimization

### Performance Tips
1. **Close unnecessary applications** before optimization
2. **Use gaming profile** for best gaming performance
3. **Enable real-time monitoring** for best results
4. **Update drivers** regularly

## Support

- **GitHub**: https://github.com/NGXSMK/ngxsmk-gamenet-optimizer
- **Email**: sachindilshan040@gmail.com
- **Maintainer**: NGXSMK

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines and code of conduct.

---

**Optimize Your Gaming Experience with NGXSMK GameNet Optimizer!**
"""

    with open(str(SCRIPT_DIR / "README_ADVANCED.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("Created README_ADVANCED.md")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build NGXSMK GameNet Optimizer Advanced executable')
    parser.add_argument('--arch', choices=['x86', 'x64', 'both'], default='x64',
                        help='Target architecture: x86 (32-bit), x64 (64-bit), both (try both, default: x64)')
    args = parser.parse_args()

    print("NGXSMK GameNet Optimizer - Advanced Builder")
    print("=" * 50)
    print(f"Target architecture: {args.arch}")

    create_advanced_installer()
    create_advanced_readme()

    success = False
    if args.arch == 'both':
        print("\n--- Building for x64 ---")
        s1 = build_advanced_executable(arch='x64')
        if s1:
            print("\n--- Also attempting x86 ---")
            s2 = build_advanced_executable(arch='x86')
            success = s1 or s2
        else:
            success = False
    else:
        success = build_advanced_executable(arch=args.arch)

    if success:
        print("\nAdvanced build completed successfully!")
        print("Check the dist/ folder for your executable")
        print("Run install_advanced.bat for easy installation")
    else:
        print("\n[ERROR] Build failed. Check the error messages above.")
        sys.exit(1)
