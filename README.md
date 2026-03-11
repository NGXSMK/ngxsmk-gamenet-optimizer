# NGXSMK Neural Optimizer

[![Version](https://img.shields.io/badge/Version-2.2.6-blue.svg)](https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/releases)
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/UI-React%2018-61dafb.svg)](https://reactjs.org/)
[![Electron](https://img.shields.io/badge/Desktop-Electron-47848f.svg)](https://www.electronjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-lightgrey.svg)](https://github.com)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/actions)


> **A powerful, open-source gaming optimization suite with modern UI that enhances your gaming experience through advanced network optimization, system tuning, and real-time performance monitoring.**

## 🚀 Quick Start

### Download Pre-built Executable (Recommended)
1. **Download** the latest release from [Releases](https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/releases)
2. **Extract** the zip file
3. **Run** `NGXSMK Neural Optimizer.exe` (The new Electron-based Neural Dashboard)
4. **Enjoy** vectorized, low-latency gaming!

### Build from Source
```bash
# Clone the repository
git clone https://github.com/NGXSMK/ngxsmk-gamenet-optimizer.git
cd ngxsmk-gamenet-optimizer

# Install dependencies
pip install -r requirements.txt

# Run the Neural Backend
python src/ngx_optimizer/api.py

# Run the UI (Dev Mode)
cd web-ui
npm run dev
```

## ✨ What is NGXSMK GameNet Optimizer?

NGXSMK GameNet Optimizer is a comprehensive, open-source gaming optimization tool with a modern dark theme UI designed to enhance your gaming experience. The architecture features a **Python 3.13 Core** engine serving a high-performance **React 19 Dashboard** via a bi-directional Neural Link API.

### 🎯 Key Benefits

- **🚀 Boost FPS** - Optimize system performance for higher frame rates
- **🌐 Reduce Latency** - Advanced network optimization for lower ping
- **🧠 Neural Dashboard** - Next-gen React/Electron UI with real-time telemetry
- **🍞 Toast Notification System** - Instant visual feedback for all neural tasks
- **🥇 Stability Elite Ranking** - AI-driven system health scoring and predictive bottlenecking
- **🧹 Clean Memory** - Intelligent RAM management via `RAMCleaner.py`
- **⚡ Smart Traffic** - Prioritize gaming traffic over background apps
- **🎮 Game-Specific** - Tailored optimizations for popular games
- **📊 Real-time Analytics** - Animated charts for live CPU/RAM monitoring


## 🌟 Features

### 🧠 Neural UI & User Experience
- **React 18 Dashboard** - High-performance web interface built with modern hooks
- **Electron Standalone** - Native Windows experience with frameless "Glass" design
- **Real-time Telemetry** - Animated `recharts` integration for live performance tracking
- **Glassmorphism 2.0** - Premium semi-transparent visuals with glowing mint/cyan accents
- **Cross-Process Bridge** - Seamless integration between React UI and Python backend logic


### 🎮 FPS Boost & Game Optimization
- **Intelligent Game Detection** - Automatically detects and optimizes running games
- **Process Priority Management** - Sets high priority for gaming applications
- **CPU & GPU Optimization** - Advanced system tuning for maximum performance
- **Real-time Monitoring** - Live FPS and system metrics display
- **Quick Action Buttons** - One-click optimization for common tasks

### 🌐 Network Analyzer
- **Multi-Server Testing** - Test latency to gaming servers worldwide
- **Bandwidth Analysis** - Comprehensive speed testing and analysis with realistic estimates
- **Gaming Server Optimization** - Specialized testing for popular games
- **Connection Quality Assessment** - Detailed network quality scoring
- **Real-time Network Monitoring** - Live connection status and performance metrics

### 🔄 Multi-Connection Manager
- **Load Balancing** - Distribute traffic across multiple connections
- **Automatic Failover** - Seamless switching to backup connections
- **Quality Monitoring** - Real-time connection performance tracking
- **Smart Routing** - Optimize traffic paths for gaming

### 🚦 Traffic Shaper
- **Bandwidth Control** - Set limits and prioritize gaming traffic
- **QoS Management** - Quality of Service for optimal gaming
- **Background App Limiting** - Reduce interference from other applications
- **Real-time Monitoring** - Live bandwidth usage tracking

### 🧹 Memory Optimizer
- **Smart RAM Cleaning** - Intelligent memory management with detailed feedback
- **Process Optimization** - Close unnecessary background applications
- **Auto-cleanup** - Automatic memory optimization
- **Gaming-Specific Tuning** - Optimized for gaming workloads
- **Real-time Memory Monitoring** - Live RAM usage with color-coded status indicators

### 🎯 League of Legends Optimizer
- **Dedicated LoL Support** - Specialized optimizations for League of Legends
- **Server Latency Testing** - Test ping to all major LoL servers (NA, EUW, EUNE, KR, BR, SG)
- **Best Server Selection** - Automatically find your optimal server
- **Real-time Performance** - Monitor LoL-specific metrics
- **Accurate Latency Results** - Fixed server testing with proper ping parsing

## 🎮 Supported Games

- **League of Legends** (with server testing)
- **Valorant**
- **Counter-Strike 2**
- **Fortnite**
- **Apex Legends**
- **Call of Duty**
- **Overwatch**
- **Dota 2**
- **PUBG**
- **Rust**
- **Minecraft**
- And many more!

## 🛠️ Installation

### Prerequisites
- Python 3.13+ (for building from source)
- Windows 10/11 (primary support)
- Administrator privileges (for full functionality)

### Automated Builds
This project uses GitHub Actions for automated building and testing:

- **🔄 Automatic Builds** - Every push triggers a new build
- **📦 Pre-built Executables** - Download ready-to-use executables
- **🧪 Automated Testing** - Continuous integration testing
- **📋 Build Status** - Real-time build status monitoring

### Download Latest Build
Visit the [Actions](https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/actions) page to download the latest automated build artifacts.

### Installation (From Source)
```bash
git clone https://github.com/NGXSMK/ngxsmk-gamenet-optimizer.git
cd ngxsmk-gamenet-optimizer
pip install -r requirements.txt
python run.py
```

### Build Executable
```bash
python scripts/build_simple_advanced.py
```

## 📖 Usage

### Basic Usage
1. **Launch** the application using `python run.py` or run the executable
2. **Use Quick Actions** for one-click optimization (Optimize All, Clean RAM, Test Network, Gaming Mode)
3. **Use individual tabs** to configure specific features
4. **Monitor performance** in real-time with live status indicators
5. **View results** with detailed popup modals after each action

### Advanced Configuration
- **FPS Boost**: Configure game-specific optimizations with real-time monitoring
- **Network Analyzer**: Test and optimize your connection with detailed analysis
- **Multi Internet**: Manage multiple connections with load balancing
- **Traffic Shaper**: Control bandwidth allocation and QoS settings
- **RAM Cleaner**: Optimize memory usage with detailed feedback
- **LoL Optimizer**: Specialized League of Legends features with server testing
- **Settings**: Configure theme, language, and system preferences
- **About**: View version information and project details

## 🏗️ Project Structure

```
ngxsmk-gamenet-optimizer/
├── run.py                     # Legacy Python GUI entry
├── web-ui/                    # New Neural Dashboard (React source)
│   ├── src/App.jsx            # Main UI Logic
│   ├── electron-main.cjs      # Desktop Shell configuration
│   └── package.json           # UI Dependencies & Scripts
├── src/                       # Backend Source
│   └── ngx_optimizer/         
│       ├── api.py             # Full-stack bridge API (Flask)
│       └── modules/           # Core optimization engines
├── docs/                      # Updated v2.2.6 documentation
├── assets/                    # Shared application assets
├── LICENSE                    # MIT License
└── README.md                  # This file

```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Development Setup
```bash
git clone https://github.com/NGXSMK/ngxsmk-gamenet-optimizer.git
cd ngxsmk-gamenet-optimizer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Local Building
```bash
# Quick local build
python build_local.py

# Or use the existing build script
python build_simple_advanced.py
```

## 🔄 CI/CD Pipeline

This project uses GitHub Actions for automated building, testing, and deployment:

### 🏗️ Build Workflows
- **Main Build** (`build.yml`) - Builds on push to main/develop branches
- **Development Build** (`dev-build.yml`) - Quick builds for feature branches
- **Release Build** (`release.yml`) - Creates releases with executables
- **Test Suite** (`test.yml`) - Automated testing and validation

### 📦 Automated Features
- **🔄 Auto Build** - Every push triggers a new build
- **🧪 Auto Test** - Comprehensive testing on multiple Python versions
- **📦 Auto Release** - Automatic release creation on version tags
- **📋 Build Status** - Real-time build status monitoring
- **🔍 Security Scan** - Basic security checks on builds

### 🚀 Release Process
1. **Tag Creation** - Create a version tag (e.g., `v2.0.0`)
2. **Auto Build** - GitHub Actions automatically builds the executable
3. **Auto Release** - Release is created with downloadable executables
4. **Artifact Upload** - Build artifacts are uploaded to releases

### 📊 Build Artifacts
- **Executable** - Ready-to-run Windows executable
- **Archive** - Complete package with documentation
- **Build Info** - Detailed build information and changelog

## 📊 Performance Benefits

- **Reduced Latency** - Optimize network routing for lower ping
- **Higher FPS** - System optimization for better frame rates
- **Less Lag** - Traffic shaping and priority management
- **Better Stability** - Memory optimization and process management
- **Optimal Server Selection** - Find the best gaming servers
- **Real-time Monitoring** - Live system status with color-coded indicators
- **Adaptive Performance** - Optimized for both low-end and high-end PCs
- **Quick Actions** - One-click optimization for common tasks

## 🔒 Privacy & Security

- **100% Local Processing** - No data sent to external servers
- **No Telemetry** - Complete privacy protection
- **Open Source** - Full transparency and auditability
- **No Ads** - Completely ad-free experience
- **No Data Collection** - Your data stays on your device

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: Dual-core processor (2.0 GHz+)
- **Storage**: 100MB free space
- **Network**: Active internet connection
- **Permissions**: Administrator privileges for full functionality

### Recommended Requirements
- **OS**: Windows 11 (latest updates)
- **RAM**: 16GB or more
- **CPU**: Quad-core processor (3.0 GHz+)
- **Storage**: 500MB free space (SSD recommended)
- **Network**: High-speed internet connection
- **GPU**: Dedicated graphics card for gaming

### Build Requirements (for developers)
- **Python**: 3.13+ with pip
- **PyInstaller**: For building executables
- **Git**: For version control
- **Visual Studio Build Tools**: For compiling dependencies (Windows)

## 🐛 Troubleshooting

### Common Issues
1. **Permission Errors**: Run as administrator
2. **Network Analysis Fails**: Check firewall settings
3. **Memory Cleanup Issues**: Ensure sufficient system resources

### Getting Help
- **GitHub Issues**: [Report bugs and request features](https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/issues)
- **Discussions**: [Community discussions](https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/discussions)
- **Email**: sachindilshan040@gmail.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the gaming community's need for accessible optimization tools
- Built with open source principles and community feedback
- Special thanks to all contributors and testers

## 🔮 Roadmap

- [x] Modern UI with dark theme
- [x] Real-time system monitoring
- [x] Adaptive window sizing for all PCs
- [x] Quick action buttons
- [x] Enhanced RAM cleaning with feedback
- [x] Improved network testing
- [x] Fixed LoL server latency testing
- [ ] macOS support
- [ ] Additional game support
- [ ] Advanced network protocols
- [ ] Machine learning optimization
- [ ] Plugin system
- [ ] Mobile companion app

## 📞 Support

- **GitHub Issues**: [Report bugs and request features](https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/issues)
- **Discussions**: [Community discussions](https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/discussions)
- **Email**: sachindilshan040@gmail.com
- **Maintainer**: [@NGXSMK](https://github.com/NGXSMK)

---

**Made with ❤️ for the gaming community**

*NGXSMK GameNet Optimizer - Optimize your gaming experience, open source and free!*
