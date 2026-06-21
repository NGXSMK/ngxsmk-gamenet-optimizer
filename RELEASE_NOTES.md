# NGXSMK GameNet Optimizer 2.3.0

## What's New

- **Complete UI Redesign** — Clean, modern, professional interface. Removed heavy cyberpunk aesthetic for a sleek, minimal design. Faster load times and lower GPU usage.
- **Real Network Speed Test** — Integrated `speedtest-cli` based speed test with ping/download/upload results. Click "Run Speed Test" on the Network tab.
- **Performance Benchmarking** — Quick Optimize now captures before/after snapshots (CPU, RAM, ping) and displays the delta in a benchmark card.
- **Auto Game Detection** — Background watcher detects running games and automatically applies optimization profiles. Detected games shown as a dashboard banner.
- **System Info Tab** — Detailed hardware information: CPU model/cores/threads, RAM total, GPU name/VRAM, disk usage. Uses WMI on Windows.
- **Profile Manager** — Save/load/delete named profiles for settings (aggressive mode, auto-optimize). Accessible from Settings tab.
- **Low Power Mode** — New toggle in sidebar for low-end PCs. Reduces polling frequency, disables heavy background modules, and lowers CPU overhead.
- **32-bit (x86) Support** — Build scripts now support `--arch x86` for 32-bit Windows. Both architectures can be built.
- **SEO-Optimized Website** — New React landing page at `website/` with Open Graph, JSON-LD structured data, sitemap, and GitHub Pages deployment workflow.

## Build System Improvements

- Build scripts accept `--arch` argument (x86, x64, both)
- Automated React frontend build before PyInstaller
- Fixed Python version check (3.8+ instead of 3.13+)
- Serve bundled frontend from Flask backend
- GitHub Actions workflow for automated EXE builds on release tags

## Bug Fixes

- `NeuralIntelligence.get_neural_status` AttributeError (stale `__pycache__`)
- Missing dependencies in `requirements.txt` and `setup.py`
- SQL injection vulnerability in config manager
- Electron security hardening (contextIsolation, nodeIntegration disabled)
- Chart not rendering due to ResponsiveContainer height issue
- Various subprocess timeout issues

## How to Download

Go to https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/releases/latest and download:

- `NGXSMK_GameNet_Optimizer_x64.exe` — for 64-bit Windows 10/11
- `NGXSMK_GameNet_Optimizer_x86.exe` — for 32-bit Windows 10/11

Both are standalone portable executables. No installation required.
