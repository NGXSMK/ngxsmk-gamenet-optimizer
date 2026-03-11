# Windows Executable Build Guide

This guide will help you create a Windows executable (.exe) file for NGXSMK GameNet Optimizer.

## 🚀 Quick Build (Recommended)

### Method 1: Simple Batch File
```bash
build_exe.bat
```

### Method 2: Python Script
```bash
python build_exe_simple.py
```

### Method 3: Advanced Build
```bash
python build_exe.py
```

## 📋 Prerequisites

- **Python 3.7+** installed
- **All dependencies** installed (`pip install -r requirements.txt`)
- **Windows OS** (for building Windows executables)

## 🛠️ Step-by-Step Build Process

### 1. Install PyInstaller
```bash
pip install pyinstaller
```

### 2. Build Executable
```bash
# Simple one-file executable
python -m PyInstaller --onefile --windowed --name=NGXSMK_GameNet_Optimizer main.py

# Advanced build with modules
python build_exe.py
```

### 3. Find Your Executable
After building, you'll find:
- **Location**: `dist/NGXSMK_GameNet_Optimizer.exe`
- **Size**: ~50-100 MB (includes all dependencies)
- **Type**: Standalone executable (no Python required)

## 🎯 Build Options

### Simple Build (One File)
```bash
python -m PyInstaller --onefile --windowed main.py
```

### Advanced Build (With Modules)
```bash
python -m PyInstaller --onefile --windowed --add-data="modules;modules" main.py
```

### Custom Build (With Icon)
```bash
python -m PyInstaller --onefile --windowed --icon=icon.ico main.py
```

## 📦 Distribution Options

### Option 1: Single Executable
- **File**: `NGXSMK_GameNet_Optimizer.exe`
- **Size**: ~50-100 MB
- **Requirements**: None (standalone)
- **Best for**: Simple distribution

### Option 2: Folder Distribution
- **Folder**: `dist/` (entire folder)
- **Size**: ~100-200 MB
- **Requirements**: None (standalone)
- **Best for**: Complete application

### Option 3: Installer Package
- **Tool**: NSIS, Inno Setup, or Advanced Installer
- **Size**: ~50-100 MB
- **Requirements**: None (standalone)
- **Best for**: Professional distribution

## 🔧 Troubleshooting

### Common Issues

1. **"PyInstaller not found"**
   ```bash
   pip install pyinstaller
   ```

2. **"Module not found" errors**
   ```bash
   pip install -r requirements.txt
   ```

3. **"Permission denied" errors**
   - Run as administrator
   - Check antivirus software

4. **Large file size**
   - Use `--exclude-module` to exclude unused modules
   - Use `--strip` to reduce size

### Build Optimization

```bash
# Smaller executable
python -m PyInstaller --onefile --windowed --strip --exclude-module=matplotlib main.py

# Faster startup
python -m PyInstaller --onefile --windowed --noupx main.py

# Debug version
python -m PyInstaller --onefile --console main.py
```

## 📁 File Structure After Build

```
project/
├── dist/
│   └── NGXSMK_GameNet_Optimizer.exe  # Your executable
├── build/                            # Build temporary files
├── main.py                           # Source code
├── modules/                          # Application modules
└── requirements.txt                  # Dependencies
```

## 🚀 Testing Your Executable

1. **Navigate to dist folder**
2. **Run the .exe file**
3. **Test all features**
4. **Check for errors**

## 📦 Distribution Checklist

- [ ] Executable runs without Python installed
- [ ] All features work correctly
- [ ] No missing dependencies
- [ ] File size is reasonable
- [ ] Antivirus doesn't flag it
- [ ] Test on different Windows versions

## 🎯 Advanced Build Options

### Custom Icon
1. Create or find a `.ico` file
2. Place it in project root as `icon.ico`
3. Build with: `--icon=icon.ico`

### Version Information
```bash
python -m PyInstaller --onefile --windowed --version-file=version.txt main.py
```

### Console Version (for debugging)
```bash
python -m PyInstaller --onefile --console main.py
```

## 💡 Tips for Success

1. **Test thoroughly** before distribution
2. **Use virtual environment** for clean builds
3. **Check file size** and optimize if needed
4. **Test on different Windows versions**
5. **Include installation instructions**

## 🔒 Security Considerations

- **Code signing** for trusted distribution
- **Antivirus whitelisting** may be needed
- **User permissions** for system optimization features
- **Firewall exceptions** for network features

## 📞 Support

If you encounter issues:
- Check the build logs
- Ensure all dependencies are installed
- Try the simple build method first
- Contact: sachindilshan040@gmail.com

---

**Your NGXSMK GameNet Optimizer executable is ready for distribution!** 🚀
