# NGXSMK Neural Optimizer - Web Dashboard

## Redesign Overview
This is a modern React-based redesign of the NGXSMK GameNet Optimizer. It features a premium, dark glassmorphism aesthetic with real-time telemetry visualizations.

### Technologies
- **Framework**: React 18+ (Vite)
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Styling**: Vanilla CSS with Design Tokens

### Features
- **Modern Sidebar**: Smooth navigation between optimization modules.
- **Glassmorphic Cards**: Premium look and feel for system stats.
- **Dynamic Telemetry**: Animated Area charts for CPU and RAM monitoring.
- **Quick Optimize**: Unified action button with pulse animations.

### Full-Stack Integration
The project now uses a **Web Bridge Architecture**:
- **Frontend**: React (Vite) running on `http://localhost:5173`
- **Backend API**: Python (Flask) running on `http://localhost:5000`
- **Communication**: Axois with CORS enabled

The React frontend polls the Python backend every 2 seconds to fetch live system metrics directly from the `SystemMonitor` and `RAMCleaner` classes. Action buttons on the UI trigger real-world optimizations (like clearing RAM or flushing DNS) by calling methods in the original Python modules.

## Getting Started

### 1. Start the Python Backend
```bash
python src/ngx_optimizer/api.py
```

### 2. Start the React UI
```bash
cd web-ui
npm run dev
```

## Production Build
```bash
npm run build
```
