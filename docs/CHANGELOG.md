# Changelog

All notable changes to GameNet Optimizer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.6] - 2026-03-11

### Added
- **Neural UI Redesign**: Launched a completely new dashboard built with React 18, featuring a premium "Neural" aesthetic.
- **Electron Integration**: The application can now run as a standalone Windows desktop app with a custom frameless window.
- **Full-Stack Web Bridge**: Created a Flask-based API (`api.py`) to connect the React UI with legacy Python optimization modules.
- **Real-Time Telemetry**: Integrated animated Recharts for live-tracking of CPU, RAM, and Network performance.
- **Stand-alone Packaging**: Added `electron-builder` support for creating portable `.exe` distributions.

### Fixed
- **Prop Validation**: Resolved linting warnings across the React component tree.
- **Accessibility**: Replaced non-semantic interactive elements with native buttons for better screen reader and keyboard support.

## [2.1.0] - 2026-03-11

### Added
- **Premium UI Overhaul**: Implemented a state-of-the-art dark theme with vibrant accents and modern typography.
- **Glassmorphism Design**: Added modern semi-transparent elements for a depth-rich user experience.
- **System-Wide Stabilization**: Resolved critical syntax and runtime errors across all optimization modules.
- **Adaptive Sizing**: Improved UI scaling for both low-end and high-end PCs.
- **Enhanced Monitoring**: Refined real-time status indicators and system metrics tracking.
- **Modernized Dialogs**: Revamped About and Settings dialogs with premium branding and improved layout.

## [Unreleased]

### Added
- Initial open source release
- Comprehensive gaming optimization suite
- League of Legends specific optimizations
- Multi-platform support planning

## [1.0.0] - 2024-01-XX

### Added
- **FPS Boost Module**
  - Game process detection and optimization
  - CPU priority management
  - GPU optimization settings
  - System performance tuning
  - Real-time performance monitoring

- **Network Analyzer**
  - Multi-server latency testing
  - Bandwidth analysis with speedtest integration
  - Gaming server testing (Valorant, CS2, Fortnite, LoL, etc.)
  - Network quality scoring and recommendations
  - Continuous monitoring capabilities

- **Multi Internet Manager**
  - Multiple connection management
  - Load balancing across connections
  - Automatic failover support
  - Connection quality monitoring
  - Best connection selection

- **Traffic Shaper**
  - Bandwidth limiting and control
  - Gaming traffic prioritization
  - Background application limiting
  - Real-time traffic monitoring
  - Port-based traffic shaping

- **RAM Cleaner**
  - Memory optimization and cleanup
  - Process memory management
  - Auto-cleanup with configurable thresholds
  - Gaming-specific optimizations
  - Memory usage trending

- **League of Legends Optimizer**
  - Dedicated LoL process detection
  - Server latency testing (NA, EUW, EUNE, KR, BR, SG)
  - LoL-specific performance optimization
  - Best server selection
  - Real-time LoL performance monitoring

- **Configuration Management**
  - JSON-based settings with automatic saving
  - Module-specific configurations
  - Import/export functionality
  - Default configurations with sensible presets
  - Advanced debugging options

- **Modern GUI Application**
  - Dark theme interface with professional styling
  - Tabbed interface for each optimization module
  - Real-time status monitoring and progress indicators
  - One-click optimization with "Start Optimization" button
  - Individual module controls for fine-tuning

### Technical
- Cross-platform Python application
- Modular architecture for easy extension
- Comprehensive error handling
- Thread-safe operations
- Memory-efficient design
- Open source MIT license

### Documentation
- Comprehensive README with installation instructions
- Contributing guidelines
- Code of conduct
- Setup script for easy installation
- Git configuration for open source development

### Supported Games
- League of Legends (with server testing)
- Valorant
- Counter-Strike 2
- Fortnite
- Apex Legends
- Call of Duty
- Overwatch
- Dota 2
- PUBG
- Rust
- Minecraft
- And many more!

### Supported Platforms
- Windows 10/11 (primary support)
- Linux (partial support)
- Python 3.7+ compatibility

## [0.9.0] - 2024-01-XX (Pre-release)

### Added
- Initial project structure
- Core optimization modules
- Basic GUI framework
- Configuration system
- League of Legends support

### Changed
- Project renamed from "Network Optimizer Pro" to "GameNet Optimizer"
- Refactored for open source release
- Updated documentation for community use

---

## Legend
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes
