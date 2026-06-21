import React, { useState, useEffect, useCallback, useRef } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import {
  Activity,
  Gamepad2,
  Network,
  Zap,
  Settings,
  BarChart3,
  ShieldCheck,
  HardDrive,
  Trash2,
  Share2,
  GitFork,
  Wifi,
  Radar,
  Cpu,
  ArrowRight,
  Monitor,
  Battery,
  Globe,
  Signal,
  Power,
  Layers,
  Clock,
  FileText,
  Library,
  Sliders,
  ToggleLeft,
  ToggleRight,
  Play,
  RefreshCw,
  Download,
  Eye,
  EyeOff,
  Rocket,
  Calendar
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip
} from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';
import toast, { Toaster } from 'react-hot-toast';

const API_BASE = 'http://localhost:5000/api';

const NeuralIntelligenceCard = ({ data }) => (
  <div className="card">
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
      <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Zap size={18} color="var(--primary)" />
        Stability Index
      </h3>
    </div>

    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>System Stability</span>
        <span style={{ fontSize: '18px', fontWeight: '700', color: (data?.stability_score || 0) > 80 ? 'var(--success)' : 'var(--warning)' }}>
          {data?.stability_score || 100}%
        </span>
      </div>

      <div className="progress-bar">
        <div className="progress-fill" style={{
          width: `${data?.stability_score || 100}%`,
          background: 'var(--secondary)'
        }}></div>
      </div>

      {data?.predicted_bottleneck && (
        <div style={{
          padding: '12px',
          background: '#fef2f2',
          borderRadius: '8px',
          border: '1px solid #fecaca',
          marginTop: '4px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--error)', fontWeight: '600', fontSize: '11px' }}>
            <Activity size={12} />
            Predicted Bottleneck
          </div>
          <div style={{ fontSize: '13px', fontWeight: '600', marginTop: '4px', color: 'var(--text)' }}>
            {data.predicted_bottleneck.replaceAll('_', ' ')}
          </div>
        </div>
      )}

      <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px', display: 'flex', justifyContent: 'space-between' }}>
        <span>Trend: {data?.trend || 'Analyzing...'}</span>
        <span>Sync: Active</span>
      </div>
    </div>
  </div>
);

const LearningCoreCard = ({ data }) => (
  <div className="card">
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
      <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <HardDrive size={18} color="var(--primary)" />
        Learning Progress
      </h3>
    </div>

    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Knowledge Progress</span>
        <span style={{ fontSize: '14px', fontWeight: '700', color: 'var(--primary)' }}>
          {data?.learning_progress?.toFixed(1) || 0}%
        </span>
      </div>

      <div className="progress-bar">
        <div className="progress-fill" style={{
          width: `${data?.learning_progress || 0}%`
        }}></div>
      </div>

      <div style={{ marginTop: '8px' }}>
        <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '8px', fontWeight: '600' }}>Background Processes:</div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
          {data?.candidates?.length > 0 ? data.candidates.map(c => (
            <span key={c} style={{ padding: '4px 8px', background: '#f3f4f6', borderRadius: '6px', fontSize: '10px', color: 'var(--text-secondary)', border: '1px solid var(--border)' }}>
              {c}
            </span>
          )) : (
            <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontStyle: 'italic' }}>Learning your patterns...</span>
          )}
        </div>
      </div>

      <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '8px', borderTop: '1px solid var(--border)', paddingTop: '8px' }}>
        Tracked Processes: {data?.total_procs_tracked || 0}
      </div>
    </div>
  </div>
);

const HardwareHubCard = ({ data, onRunTask }) => (
  <div className="card">
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
      <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Activity size={18} color="var(--primary)" />
        Hardware
      </h3>
    </div>

    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
      <div style={{ padding: '12px', background: '#f9fafb', borderRadius: '8px' }}>
        <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginBottom: '4px' }}>CPU TEMP</div>
        <div style={{ fontSize: '20px', fontWeight: '700', color: (data?.cpu_temp || 0) > 70 ? 'var(--error)' : 'var(--text)' }}>
          {data?.cpu_temp?.toFixed(1) || 0}°C
        </div>
      </div>
      <div style={{ padding: '12px', background: '#f9fafb', borderRadius: '8px' }}>
        <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginBottom: '4px' }}>GPU TEMP</div>
        <div style={{ fontSize: '20px', fontWeight: '700', color: (data?.gpu_temp || 0) > 70 ? 'var(--error)' : 'var(--text)' }}>
          {data?.gpu_temp?.toFixed(1) || 0}°C
        </div>
      </div>
    </div>

    <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div>
        <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>GPU PROFILE</div>
        <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--primary)' }}>{data?.gpu_mode || 'STANDARD'}</div>
      </div>
      <button className="btn" style={{ padding: '6px 14px', fontSize: '12px' }} onClick={() => onRunTask('/optimize/gpu', 'GPU P-State Shift')}>
        MAX POWER
      </button>
    </div>

    <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '12px', textAlign: 'center' }}>
      Status: <span style={{ color: data?.thermal_status === 'COOL' ? 'var(--success)' : 'var(--error)', fontWeight: '600' }}>{data?.thermal_status || 'OPTIMAL'}</span>
    </div>
  </div>
);

const NetworkEvolutionCard = ({ data, onRunTask }) => (
  <div className="card">
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
      <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Network size={18} color="var(--primary)" />
        Network
      </h3>
    </div>

    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Multi-Path Tunneling</span>
        <span style={{ fontSize: '12px', fontWeight: '600', color: data?.tunneling_active ? 'var(--success)' : 'var(--text-muted)' }}>
          {data?.tunneling_active ? 'Enabled' : 'Disabled'}
        </span>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Active Region</span>
        <span style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text)' }}>{data?.current_region || 'AUTO'}</span>
      </div>

      <div style={{ padding: '12px', background: '#f0fdf4', borderRadius: '8px', border: '1px solid #bbf7d0', marginTop: '4px' }}>
        <div style={{ fontSize: '11px', color: 'var(--success)', fontWeight: '600' }}>PERFORMANCE GAIN</div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginTop: '4px' }}>
          <span style={{ fontSize: '24px', fontWeight: '700', color: 'var(--text)' }}>{data?.ping_improvement || '-0ms'}</span>
          <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>LATENCY DROP</span>
        </div>
      </div>

      <div style={{ marginTop: '8px', display: 'flex', gap: '8px' }}>
        <button className="btn" style={{ flex: 1, padding: '8px', fontSize: '12px', background: data?.tunneling_active ? 'var(--success)' : undefined }} onClick={() => onRunTask('/optimize/network-tunnel', 'Neural Tunnel Shift', { active: !data?.tunneling_active })}>
          {data?.tunneling_active ? 'DISABLE TUNNEL' : 'ENABLE TUNNEL'}
        </button>
      </div>

      <div style={{ fontSize: '10px', color: 'var(--text-muted)', textAlign: 'center' }}>
        Packet Loss Protection: <span style={{ color: 'var(--success)', fontWeight: '600' }}>{data?.packet_loss_protection || 'ACTIVE'}</span>
      </div>
    </div>
  </div>
);

const CloudLinkCard = ({ data, onRunTask }) => (
  <div className="card">
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
      <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Share2 size={18} color="var(--primary)" />
        Cloud Sync
      </h3>
    </div>

    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Stability Rank</span>
        <span style={{ fontSize: '14px', fontWeight: '700', color: 'var(--primary)' }}>{data?.stability_rank || 'ELITE'}</span>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Score</span>
        <span style={{ fontSize: '18px', fontWeight: '700', color: 'var(--text)' }}>{data?.score || 9450} XP</span>
      </div>

      <div style={{ padding: '12px', background: '#eef2ff', borderRadius: '8px', border: '1px solid #c7d2fe', marginTop: '4px' }}>
        <div style={{ fontSize: '11px', color: 'var(--primary)', fontWeight: '600' }}>DISCORD PRESENCE</div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '6px' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>{data?.discord_presence || 'Disconnected'}</span>
          <button className="btn" style={{ padding: '4px 10px', fontSize: '11px' }} onClick={() => onRunTask('/cloud/discord', 'Discord RPC Shift', { active: data?.discord_presence === 'Disconnected' })}>
            SYNC
          </button>
        </div>
      </div>

      <div style={{ fontSize: '10px', color: 'var(--text-muted)', textAlign: 'center', marginTop: '8px' }}>
        Position: <span style={{ color: 'var(--primary)', fontWeight: '600' }}>{data?.global_position || '#124 GLOBAL'}</span>
      </div>
    </div>
  </div>
);

const EcosystemSyncCard = ({ data, onRunTask }) => (
  <div className="card">
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
      <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Gamepad2 size={18} color="var(--primary)" />
        Game Sync
      </h3>
    </div>

    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Detected Stores</span>
        <div style={{ display: 'flex', gap: '4px' }}>
          {data?.stores?.map(s => (
            <span key={s} style={{ padding: '2px 6px', background: '#f3f4f6', borderRadius: '4px', fontSize: '9px', fontWeight: '600' }}>{s.toUpperCase()}</span>
          ))}
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Auto-Boost</span>
        <span style={{ fontSize: '12px', fontWeight: '600', color: 'var(--success)' }}>Enabled</span>
      </div>

      <div style={{ padding: '12px', background: '#f3f4f6', borderRadius: '8px', marginTop: '4px' }}>
        <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginBottom: '4px' }}>LAST LAUNCH</div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '14px', fontWeight: '600' }}>{data?.last_boosted_launch || 'None'}</span>
          <Zap size={14} color="var(--primary)" />
        </div>
      </div>

      <button className="btn" style={{ marginTop: '8px', padding: '10px' }} onClick={() => onRunTask('/ecosystem/launch', 'Neural Launch Sequence', { game: 'Valorant', store: 'Steam' })}>
        QUICK LAUNCH & BOOST
      </button>

      <div style={{ fontSize: '10px', color: 'var(--text-muted)', textAlign: 'center', marginTop: '4px' }}>
        Sync: <span style={{ color: 'var(--success)', fontWeight: '600' }}>Secure</span>
      </div>
    </div>
  </div>
);

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isApiConnected, setIsApiConnected] = useState(true);
  const [hasShownConnectionToast, setHasShownConnectionToast] = useState(false);
  const [statusData, setStatusData] = useState(null);
  const [cpuHistory, setCpuHistory] = useState([]);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [taskStatus, setTaskStatus] = useState(null);
  const [benchmark, setBenchmark] = useState(null);
  const [lowPowerMode, setLowPowerMode] = useState(false);
  const [settings, setSettings] = useState({
    aggressive_mode: true,
    auto_optimize: true,
    start_on_boot: false
  });

  const fetchData = useCallback(async () => {
    try {
      const resp = await axios.get(`${API_BASE}/status`);
      setStatusData(resp.data);
      if (!isApiConnected || !hasShownConnectionToast) {
        toast.success("Connected to backend", { id: 'conn-success' });
        setHasShownConnectionToast(true);
      }
      setIsApiConnected(true);

      if (resp.data.neural?.history) {
        const backendHistory = resp.data.neural.history.map(m => ({
          time: new Date(m.timestamp * 1000).toLocaleTimeString(),
          cpu: m.cpu
        }));
        setCpuHistory(backendHistory);
      } else {
        const newPoint = {
          time: new Date().toLocaleTimeString(),
          cpu: resp.data.cpu?.usage || 0
        };
        setCpuHistory(prev => [...prev.slice(-29), newPoint]);
      }
    } catch (err) {
      if (isApiConnected) {
        toast.error("Connection lost: reconnecting...", { id: 'conn-error' });
      }
      setIsApiConnected(false);
      console.error("Fetch Error:", err);
    }
  }, [isApiConnected, hasShownConnectionToast]);

  const [detectedGames, setDetectedGames] = useState([]);
  const [systemInfo, setSystemInfo] = useState(null);
  const [profiles, setProfiles] = useState([]);

  // --- New feature state ---
  const [dnsStatus, setDnsStatus] = useState(null);
  const [pingHistory, setPingHistory] = useState({});
  const [startupEnabled, setStartupEnabled] = useState(false);
  const [adapterStatus, setAdapterStatus] = useState(null);
  const [visualStatus, setVisualStatus] = useState(null);
  const [gameLibrary, setGameLibrary] = useState({ games: [], total: 0, by_store: {} });
  const [scheduleJobs, setScheduleJobs] = useState([]);
  const [scheduleActions, setScheduleActions] = useState([]);
  const [scheduleForm, setScheduleForm] = useState({ action: 'quick_optimize', hour: '20', minute: '00', repeat: true });
  const [dnsCustomPrimary, setDnsCustomPrimary] = useState('');
  const [dnsCustomSecondary, setDnsCustomSecondary] = useState('');
  const [gameScanLoading, setGameScanLoading] = useState(false);

  const fetchDnsStatus = useCallback(async () => {
    try { const r = await axios.get(`${API_BASE}/dns/status`); setDnsStatus(r.data); } catch { /* silent */ }
  }, []);
  const fetchPingHistory = useCallback(async () => {
    try { const r = await axios.get(`${API_BASE}/ping/history`); setPingHistory(r.data); } catch { /* silent */ }
  }, []);
  const fetchStartupStatus = useCallback(async () => {
    try { const r = await axios.get(`${API_BASE}/startup/status`); setStartupEnabled(r.data.enabled || false); } catch { /* silent */ }
  }, []);
  const fetchAdapterStatus = useCallback(async () => {
    try { const r = await axios.get(`${API_BASE}/adapter/status`); setAdapterStatus(r.data); } catch { /* silent */ }
  }, []);
  const fetchVisualStatus = useCallback(async () => {
    try { const r = await axios.get(`${API_BASE}/visual/status`); setVisualStatus(r.data); } catch { /* silent */ }
  }, []);
  const fetchGameLibrary = useCallback(async () => {
    try { const r = await axios.get(`${API_BASE}/games/library`); setGameLibrary(r.data); } catch { /* silent */ }
  }, []);
  const fetchSchedule = useCallback(async () => {
    try { const r = await axios.get(`${API_BASE}/schedule/status`); setScheduleJobs(r.data.jobs || []); setScheduleActions(r.data.available_actions || []); } catch { /* silent */ }
  }, []);

  useEffect(() => {
    fetchDnsStatus();
    fetchStartupStatus();
    fetchAdapterStatus();
    fetchVisualStatus();
    fetchGameLibrary();
    fetchSchedule();
  }, [fetchDnsStatus, fetchStartupStatus, fetchAdapterStatus, fetchVisualStatus, fetchGameLibrary, fetchSchedule]);

  useEffect(() => {
    if (lowPowerMode) return;
    fetchPingHistory();
    const iv = setInterval(fetchPingHistory, 5000);
    return () => clearInterval(iv);
  }, [fetchPingHistory, lowPowerMode]);


  const fetchGames = useCallback(async () => {
    try {
      const resp = await axios.get(`${API_BASE}/detected-games`);
      setDetectedGames(resp.data.games || []);
    } catch { /* silent */ }
  }, []);

  useEffect(() => {
    if (lowPowerMode) return;
    fetchGames();
    const interval = setInterval(fetchGames, 5000);
    return () => clearInterval(interval);
  }, [fetchGames, lowPowerMode]);

  const fetchSystemInfo = useCallback(async () => {
    if (activeTab !== 'system') return;
    try {
      const resp = await axios.get(`${API_BASE}/system/info`);
      setSystemInfo(resp.data);
    } catch { /* silent */ }
  }, [activeTab]);
  useEffect(() => { fetchSystemInfo(); }, [fetchSystemInfo]);

  const fetchProfiles = useCallback(async () => {
    try {
      const resp = await axios.get(`${API_BASE}/profiles/list`);
      setProfiles(resp.data.profiles || []);
    } catch { /* silent */ }
  }, []);
  useEffect(() => { fetchProfiles(); }, [fetchProfiles]);

  useEffect(() => {
    if (lowPowerMode) return;
    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, [fetchData, lowPowerMode]);

  const closeApp = () => globalThis.electronAPI?.close() ?? globalThis.location.reload();
  const minimizeApp = () => globalThis.electronAPI?.minimize();
  const maximizeApp = () => globalThis.electronAPI?.maximize();

  const navItems = [
    { id: 'dashboard',    label: 'Dashboard',    icon: BarChart3  },
    { id: 'fps_boost',    label: 'FPS Boost',    icon: Zap        },
    { id: 'network',      label: 'Network',       icon: Network    },
    { id: 'traffic',      label: 'Traffic Shaper',icon: GitFork    },
    { id: 'multi_internet',label:'Multi Internet',icon: Wifi       },
    { id: 'lol',          label: 'LoL Optimizer', icon: Radar      },
    { id: 'advanced',     label: 'AI Optimizer',  icon: Cpu        },
    { id: 'dns',          label: 'DNS Switcher',  icon: Globe      },
    { id: 'ping_chart',   label: 'Live Ping',     icon: Signal     },
    { id: 'sys_tools',    label: 'System Tools',  icon: Sliders    },
    { id: 'game_library', label: 'Game Library',  icon: Library    },
    { id: 'scheduler',    label: 'Scheduler',     icon: Calendar   },
    { id: 'system',       label: 'System',        icon: Monitor    },
    { id: 'settings',     label: 'Settings',      icon: Settings   },
  ];

  const SUPPORTED_GAMES = [
    'Valorant', 'CS2', 'Fortnite', 'Apex Legends',
    'League of Legends', 'Dota 2', 'PUBG', 'Rust', 'Minecraft'
  ];

  const toggleSetting = async (key) => {
    const newVal = !settings[key];
    const updated = { ...settings, [key]: newVal };
    setSettings(updated);

    const toastId = toast.loading(`Updating ${key.replaceAll('_', ' ')}...`);

    try {
      await axios.post(`${API_BASE}/settings`, updated);
      toast.success(`${key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')} Updated`, { id: toastId });
    } catch (err) {
      toast.error("Failed to sync settings", { id: toastId });
      console.error("Failed to update settings:", err);
    }
  };

  const runTask = async (endpoint, label, data = {}) => {
    setTaskStatus(`Initializing ${label}...`);
    const toastId = toast.loading(`Executing ${label}...`);

    try {
      await axios.post(`${API_BASE}${endpoint}`, data);
      setTaskStatus(`${label} Complete!`);
      toast.success(`${label} Success`, { id: toastId });
      setTimeout(() => setTaskStatus(null), 3000);
    } catch (err) {
      console.error(`Task ${label} failed:`, err);
      setTaskStatus(`Error: ${label} Failed`);
      toast.error(`${label} Failed`, { id: toastId });
      setTimeout(() => setTaskStatus(null), 3000);
    }
  };

  const handleOptimize = async () => {
    setIsOptimizing(true);
    const toastId = toast.loading("Running optimization...");

    try {
      const resp = await axios.post(`${API_BASE}/optimize/quick`);
      setBenchmark(resp.data.benchmark);
      toast.success("Optimization complete!", { id: toastId, duration: 4000 });
      setTimeout(() => setIsOptimizing(false), 2000);
    } catch (err) {
      toast.error("Optimization failed", { id: toastId });
      console.error("Optimization failed:", err);
      setIsOptimizing(false);
    }
  };

  return (
    <div className="app-container">
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: '#fff',
            color: '#1f2937',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
            fontSize: '14px',
          },
          success: {
            iconTheme: { primary: '#10b981', secondary: '#fff' }
          },
          error: {
            iconTheme: { primary: '#ef4444', secondary: '#fff' }
          }
        }}
      />
      <div style={{
        height: '32px',
        background: '#111827',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '0 12px',
        WebkitAppRegion: 'drag',
        zIndex: 1000
      }}>
        <div style={{ fontSize: '11px', color: '#9ca3af', fontWeight: 600 }}>GameNet Optimizer</div>
        <div style={{ display: 'flex', WebkitAppRegion: 'no-drag' }}>
          <button onClick={minimizeApp} className="window-ctrl">─</button>
          <button onClick={maximizeApp} className="window-ctrl">☐</button>
          <button onClick={closeApp} className="window-ctrl close">✕</button>
        </div>
      </div>

      <div style={{ display: 'flex', height: 'calc(100vh - 32px)', overflow: 'hidden' }}>
        <motion.div
          initial={{ x: -60, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.4, ease: "easeOut" }}
          className="sidebar"
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '0 10px 32px' }}>
            <div style={{
              width: '36px',
              height: '36px',
              background: 'var(--primary)',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Activity size={18} color="white" />
            </div>
            <div>
              <div style={{ fontSize: '15px', fontWeight: 700 }}>NGXSMK</div>
              <div style={{ fontSize: '10px', color: '#9ca3af' }}>Optimizer</div>
            </div>
          </div>

          <nav style={{ flex: 1 }}>
            {navItems.map((item, index) => (
              <motion.button
                initial={{ x: -10, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.05 + index * 0.03, duration: 0.3 }}
                key={item.id}
                className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                onClick={() => setActiveTab(item.id)}
              >
                <item.icon size={16} style={{ opacity: activeTab === item.id ? 1 : 0.6 }} />
                <span>{item.label}</span>
              </motion.button>
            ))}
          </nav>

          <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div style={{ padding: '12px', borderRadius: '8px', background: 'rgba(255,255,255,0.05)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: isApiConnected ? 'var(--success)' : 'var(--error)' }}></div>
                <span style={{ fontSize: '12px', fontWeight: 600 }}>System {isApiConnected ? 'Online' : 'Offline'}</span>
              </div>
            </div>

            <button onClick={() => setLowPowerMode(!lowPowerMode)}
              style={{
                display: 'flex', alignItems: 'center', gap: '8px',
                padding: '10px 12px', borderRadius: '8px',
                background: lowPowerMode ? 'rgba(245,158,11,0.15)' : 'rgba(255,255,255,0.05)',
                border: 'none', width: '100%', cursor: 'pointer',
                color: lowPowerMode ? '#f59e0b' : '#9ca3af',
                fontSize: '12px', fontWeight: 500, fontFamily: 'inherit',
                transition: 'background 0.15s'
              }}>
              <Battery size={14} />
              Low Power Mode {lowPowerMode ? 'ON' : 'OFF'}
            </button>

            <div style={{ padding: '12px', borderRadius: '8px', background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.06)' }}>
              <div style={{ fontWeight: 600, fontSize: '12px', color: '#e5e7eb', marginBottom: '8px' }}>Speed Test</div>
              {statusData?.speedtest ? (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '8px', marginBottom: '8px' }}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '9px', color: '#6b7280', marginBottom: '2px' }}>PING</div>
                    <div style={{ fontSize: '14px', fontWeight: 700, color: '#e5e7eb' }}>{statusData.speedtest.ping_ms?.toFixed(1) || 0}ms</div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '9px', color: '#6b7280', marginBottom: '2px' }}>DOWN</div>
                    <div style={{ fontSize: '14px', fontWeight: 700, color: 'var(--success)' }}>{statusData.speedtest.download_mbps?.toFixed(1) || 0}</div>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '9px', color: '#6b7280', marginBottom: '2px' }}>UP</div>
                    <div style={{ fontSize: '14px', fontWeight: 700, color: 'var(--secondary)' }}>{statusData.speedtest.upload_mbps?.toFixed(1) || 0}</div>
                  </div>
                </div>
              ) : null}
              <button className="btn" style={{ width: '100%', padding: '8px', fontSize: '11px', justifyContent: 'center' }} onClick={async () => {
                const toastId = toast.loading('Running speed test...');
                try {
                  const resp = await axios.post(`${API_BASE}/network/speedtest`);
                  setStatusData(prev => prev ? { ...prev, speedtest: resp.data } : null);
                  toast.success('Speed test complete', { id: toastId });
                } catch (err) {
                  toast.error('Speed test failed', { id: toastId });
                }
              }}>
                Run Speed Test
              </button>
            </div>
          </div>
        </motion.div>

        <main className="main-content">
          <motion.header
            initial={{ y: -10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.1 }}
            style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}
          >
            <div>
              <h1>Command <span className="glow-text">Center</span></h1>
              <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
                {isApiConnected ? (
                  <>System <span style={{ color: 'var(--success)', fontWeight: 600 }}>synchronized</span>.</>
                ) : (
                  <span style={{ color: 'var(--error)', fontWeight: 600 }}>Backend Unreachable</span>
                )}
              </p>
            </div>
            {!isApiConnected && (
              <button className="btn" onClick={fetchData}>
                RECONNECT
              </button>
            )}
            {isApiConnected && (
              <button
                className="btn"
                onClick={handleOptimize}
                disabled={isOptimizing}
                style={{ background: isOptimizing ? 'var(--success)' : undefined }}
              >
                {isOptimizing ? 'OPTIMIZING...' : 'QUICK OPTIMIZE'}
              </button>
            )}
          </motion.header>

          <AnimatePresence mode="wait">
            {activeTab === 'dashboard' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                key="dashboard"
                style={{ display: 'flex', gap: '24px', flexDirection: 'column' }}
              >
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: '24px', alignItems: 'start' }}>
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="card"
                    style={{ height: '380px', display: 'flex', flexDirection: 'column' }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                      <div>
                        <h3>Performance Feed</h3>
                        <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Real-time CPU usage</div>
                      </div>
                      <div className="stats-badge">LIVE</div>
                    </div>
                    <div style={{ flex: 1, minHeight: 0 }}>
                      {cpuHistory.length > 0 ? (
                        <ResponsiveContainer width="100%" height="100%">
                          <AreaChart data={cpuHistory}>
                            <defs>
                              <linearGradient id="colorCpu" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="var(--primary)" stopOpacity={0} />
                              </linearGradient>
                            </defs>
                            <Area
                              type="monotone"
                              dataKey="cpu"
                              stroke="var(--primary)"
                              fillOpacity={1}
                              fill="url(#colorCpu)"
                              strokeWidth={2}
                              isAnimationActive={false}
                            />
                          </AreaChart>
                        </ResponsiveContainer>
                      ) : (
                        <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)', fontSize: '14px' }}>
                          Waiting for data...
                        </div>
                      )}
                    </div>
                  </motion.div>

                  {detectedGames.length > 0 && (
                    <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} style={{ gridColumn: '1 / -1' }}>
                      <div className="card" style={{ background: '#f0fdf4', border: '1px solid #bbf7d0' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
                          <Gamepad2 size={16} color="var(--success)" />
                          <span style={{ fontSize: '13px', fontWeight: 600 }}>Active Games Detected</span>
                          {detectedGames.map((g, i) => (
                            <span key={g.key || i} style={{ fontSize: '12px', background: '#dcfce7', padding: '4px 12px', borderRadius: '20px', color: '#15803d', fontWeight: 500 }}>
                              {g.name}
                            </span>
                          ))}
                          <span style={{ marginLeft: 'auto', fontSize: '10px', color: 'var(--text-muted)' }}>Auto-optimization active</span>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3 }}
                    style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}
                  >
                    <div className="card">
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                        <h3>Tasks</h3>
                        {taskStatus && (
                          <motion.div
                            initial={{ opacity: 0, x: 10 }}
                            animate={{ opacity: 1, x: 0 }}
                            style={{ fontSize: '11px', color: taskStatus.includes('Error') ? 'var(--error)' : 'var(--primary)', fontWeight: 600 }}
                          >
                            {taskStatus}
                          </motion.div>
                        )}
                      </div>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        <ActionItem icon={Trash2} label="Memory Purge" sub="Force RAM stabilization" onClick={() => runTask('/optimize/ram', 'RAM Flush')} />
                        <ActionItem icon={Network} label="Network Tuner" sub="Optimize routing tables" onClick={() => runTask('/optimize/network', 'Net Tuner')} />
                        <ActionItem icon={Zap} label="Core Boost" sub="Aggressive process priority" onClick={() => runTask('/optimize/fps', 'Core Boost')} />
                      </div>
                    </div>

                    <NeuralIntelligenceCard data={statusData?.neural} />
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.35 }}
                  >
                    <LearningCoreCard data={statusData?.learning} />
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.4 }}
                  >
                    <HardwareHubCard data={statusData?.hardware} onRunTask={runTask} />
                  </motion.div>

                  {benchmark && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.45 }}
                    >
                      <div className="card">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                          <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <Activity size={18} color="var(--success)" />
                            Benchmark Results
                          </h3>
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', gap: '8px', alignItems: 'center', fontSize: '13px' }}>
                          <div style={{ textAlign: 'center', color: 'var(--text-muted)' }}>CPU: {benchmark.before.cpu}%</div>
                          <ArrowRight size={14} color="var(--text-muted)" />
                          <div style={{ textAlign: 'center', color: benchmark.delta.cpu <= 0 ? 'var(--success)' : 'var(--error)' }}>{benchmark.after.cpu}% ({benchmark.delta.cpu > 0 ? '+' : ''}{benchmark.delta.cpu}%)</div>
                          <div style={{ textAlign: 'center', color: 'var(--text-muted)' }}>RAM: {benchmark.before.ram}%</div>
                          <ArrowRight size={14} color="var(--text-muted)" />
                          <div style={{ textAlign: 'center', color: benchmark.delta.ram <= 0 ? 'var(--success)' : 'var(--error)' }}>{benchmark.after.ram}% ({benchmark.delta.ram > 0 ? '+' : ''}{benchmark.delta.ram}%)</div>
                          <div style={{ textAlign: 'center', color: 'var(--text-muted)' }}>Ping: {benchmark.before.ping}ms</div>
                          <ArrowRight size={14} color="var(--text-muted)" />
                          <div style={{ textAlign: 'center', color: benchmark.delta.ping <= 0 ? 'var(--success)' : 'var(--error)' }}>{benchmark.after.ping}ms ({benchmark.delta.ping > 0 ? '+' : ''}{benchmark.delta.ping}ms)</div>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                  >
                    <NetworkEvolutionCard data={statusData?.net_evolution} onRunTask={runTask} />
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.55 }}
                  >
                    <CloudLinkCard data={statusData?.cloud} onRunTask={runTask} />
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.6 }}
                  >
                    <EcosystemSyncCard data={statusData?.ecosystem} onRunTask={runTask} />
                  </motion.div>
                </div>
              </motion.div>
            )}

            {activeTab === 'fps_boost' && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="fps" className="tab-view">
                <div className="stats-grid">
                  <StatCard icon={Zap} label="Optimized" value={statusData?.fps?.optimized_processes || 0} color="var(--primary)" progress={statusData?.fps?.optimized_processes * 10} />
                  <StatCard icon={ShieldCheck} label="Stability" value="Locked" color="var(--success)" progress={100} />
                </div>
                <div className="card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                    <h3>Process Monitor</h3>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 600 }}>SCANNING PROCESSES...</div>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '16px' }}>
                    {SUPPORTED_GAMES.map(g => {
                      const isOptimized = statusData?.fps?.optimized_details?.some(p => p.name.toLowerCase().includes(g.toLowerCase()));
                      return (
                        <div key={g} style={{
                          padding: '16px',
                          background: isOptimized ? '#eef2ff' : '#f9fafb',
                          borderRadius: '10px',
                          border: isOptimized ? '1px solid #c7d2fe' : '1px solid var(--border)',
                          textAlign: 'center'
                        }}>
                          <div style={{ fontWeight: 600, fontSize: '14px', color: isOptimized ? 'var(--primary)' : 'var(--text)' }}>{g}</div>
                          <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '4px' }}>
                            {isOptimized ? 'Optimized' : 'Not detected'}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div className="card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                    <h3>High Impact Processes</h3>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 600 }}>RESOURCE DRAINS</div>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {(statusData?.ram?.top_procs || []).map((p) => (
                      <div key={`${p.pid}-${p.name}`} style={{ display: 'flex', alignItems: 'center', gap: '16px', padding: '14px', background: '#f9fafb', borderRadius: '8px' }}>
                        <div style={{ width: '50px', padding: '6px', borderRadius: '6px', background: '#fef2f2', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--error)', fontSize: '9px', fontWeight: 600 }}>
                          PID {p.pid}
                        </div>
                        <div style={{ flex: 1 }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                            <span style={{ fontWeight: 600, fontSize: '14px' }}>{p.name}</span>
                            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{p.memory_mb?.toFixed(0) || 0} MB</span>
                          </div>
                          <div className="progress-bar" style={{ height: '4px', marginTop: '0' }}>
                            <div className="progress-fill" style={{ width: `${Math.min(100, (p.memory_mb / 1024) * 100)}%`, background: 'var(--error)' }}></div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'network' && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="network" className="tab-view">
                <div className="stats-grid">
                  <StatCard icon={Network} label="Network Load" value={`${statusData?.network?.load || 0}%`} color="var(--accent-cyan)" progress={statusData?.network?.load || 0} />
                  <StatCard icon={ShieldCheck} label="Geo Routing" value="Secure" color="var(--success)" progress={100} />
                </div>
                <div className="card">
                  <h3>Network Interface Analysis</h3>
                  <div style={{ marginTop: '24px' }}>
                    {(statusData?.network?.interfaces || []).map((iface) => (
                      <div key={`${iface.name}-${iface.ip}`} style={{ padding: '14px', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between' }}>
                        <div>
                          <div style={{ fontWeight: 600 }}>{iface.name}</div>
                          <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{iface.ip}</div>
                        </div>
                        <div style={{ textAlign: 'right' }}>
                          <div style={{ color: 'var(--success)', fontWeight: 600 }}>ACTIVE</div>
                          <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{iface.speed} Mbps</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'traffic' && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="traffic" className="tab-view">
                <div className="stats-grid">
                  <StatCard icon={GitFork} label="Traffic Shaping" value={statusData?.traffic?.is_shaping ? 'Active' : 'Inactive'} color="var(--accent-cyan)" progress={statusData?.traffic?.is_shaping ? 100 : 0} />
                  <StatCard icon={ShieldCheck} label="Gaming Priority" value={statusData?.traffic?.gaming_priority ? 'Enabled' : 'Disabled'} color="var(--success)" progress={statusData?.traffic?.gaming_priority ? 100 : 0} />
                </div>
                <div className="card">
                  <h3>Bandwidth Control</h3>
                  <div style={{ marginTop: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    <button className="btn" style={{ justifyContent: 'center' }} onClick={() => runTask('/traffic-shaper/start', 'Start Traffic Shaping')}>
                      Start Traffic Shaping
                    </button>
                    <button className="btn" style={{ justifyContent: 'center', background: '#6b7280' }} onClick={() => runTask('/traffic-shaper/stop', 'Stop Traffic Shaping')}>
                      Stop Traffic Shaping
                    </button>
                    <button className="btn" style={{ justifyContent: 'center' }} onClick={() => runTask('/traffic-shaper/priority', 'Toggle Gaming Priority', { enabled: !statusData?.traffic?.gaming_priority })}>
                      {statusData?.traffic?.gaming_priority ? 'Disable' : 'Enable'} Gaming Priority
                    </button>
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'multi_internet' && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="multi" className="tab-view">
                <div className="stats-grid">
                  <StatCard icon={Wifi} label="Connections" value={statusData?.multi_internet?.connections || 0} color="var(--primary)" progress={Math.min(100, (statusData?.multi_internet?.connections || 0) * 20)} />
                  <StatCard icon={Activity} label="Monitoring" value={statusData?.multi_internet?.is_monitoring ? 'Active' : 'Inactive'} color="var(--success)" progress={statusData?.multi_internet?.is_monitoring ? 100 : 0} />
                </div>
                <div className="card">
                  <h3>Available Connections</h3>
                  <div style={{ marginTop: '24px' }}>
                    {(statusData?.multi_internet?.interface_details || []).map((conn) => (
                      <div key={conn.name} style={{ padding: '14px', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between' }}>
                        <div style={{ fontWeight: 600 }}>{conn.name}</div>
                        <div style={{ color: conn.status === 'Connected' ? 'var(--success)' : 'var(--error)', fontWeight: 600 }}>{conn.status}</div>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="card">
                  <h3>Controls</h3>
                  <div style={{ marginTop: '24px', display: 'flex', gap: '12px' }}>
                    <button className="btn" onClick={() => runTask('/multi-internet/start', 'Start Multi Monitoring')}>Start Monitoring</button>
                    <button className="btn" style={{ background: '#6b7280' }} onClick={() => runTask('/multi-internet/stop', 'Stop Multi Monitoring')}>Stop Monitoring</button>
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'lol' && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="lol" className="tab-view">
                <div className="stats-grid">
                  <StatCard icon={Radar} label="LoL Processes" value={statusData?.lol?.running || 0} color="var(--secondary)" progress={(statusData?.lol?.running || 0) * 50} />
                  <StatCard icon={HardDrive} label="Memory Used" value={statusData?.lol?.mem_mb ? `${statusData.lol.mem_mb.toFixed(0)} MB` : '0 MB'} color="var(--accent-cyan)" progress={Math.min(100, (statusData?.lol?.mem_mb || 0) / 10)} />
                </div>
                <div className="card">
                  <h3>League of Legends Server Latency</h3>
                  <div style={{ marginTop: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {statusData?.lol_servers && Object.entries(statusData.lol_servers).map(([region, latency]) => (
                      <div key={region} style={{ padding: '14px', background: '#f9fafb', borderRadius: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span style={{ fontWeight: 600 }}>{region}</span>
                        <span style={{ fontSize: '16px', fontWeight: 700, color: latency < 50 ? 'var(--success)' : latency < 100 ? 'var(--warning)' : 'var(--error)' }}>
                          {latency}ms
                        </span>
                      </div>
                    ))}
                    <button className="btn" style={{ marginTop: '8px' }} onClick={() => runTask('/lol/servers', 'Testing LoL Servers')}>
                      Refresh Server Latency
                    </button>
                  </div>
                </div>
                <div className="card">
                  <h3>Quick Actions</h3>
                  <div style={{ marginTop: '24px', display: 'flex', gap: '12px' }}>
                    <button className="btn" onClick={() => runTask('/lol/optimize', 'LoL Optimization')}>Optimize LoL</button>
                    <button className="btn" style={{ background: '#6b7280' }} onClick={() => runTask('/lol/metrics', 'LoL Metrics Refresh')}>Refresh Metrics</button>
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'advanced' && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="advanced" className="tab-view">
                <div className="stats-grid">
                  <StatCard icon={Cpu} label="AI Engine" value={statusData?.advanced?.is_running ? 'Running' : 'Idle'} color="var(--secondary)" progress={statusData?.advanced?.is_running ? 100 : 0} />
                  <StatCard icon={BarChart3} label="Data Points" value={statusData?.advanced?.history_count || 0} color="var(--accent-cyan)" progress={Math.min(100, (statusData?.advanced?.history_count || 0) * 2)} />
                </div>
                <div className="card">
                  <h3>AI Optimization Engine</h3>
                  <div style={{ marginTop: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
                      Continuously monitors system performance and applies intelligent resource management in real-time.
                    </p>
                    <div style={{ display: 'flex', gap: '12px' }}>
                      <button className="btn" onClick={() => runTask('/advanced/start', 'Start AI Optimizer', { profile: 'gaming' })}>
                        Start AI Optimizer
                      </button>
                      <button className="btn" style={{ background: '#6b7280' }} onClick={() => runTask('/advanced/stop', 'Stop AI Optimizer')}>
                        Stop AI Optimizer
                      </button>
                    </div>
                    {statusData?.advanced?.real_time_stats && (
                      <div style={{ marginTop: '16px', padding: '16px', background: '#f3f4f6', borderRadius: '8px' }}>
                        <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--primary)', marginBottom: '8px' }}>REAL-TIME STATS</div>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                          <div>CPU: {statusData.advanced.real_time_stats.cpu_usage?.toFixed(1) || 'N/A'}%</div>
                          <div>RAM: {statusData.advanced.real_time_stats.memory_usage?.toFixed(1) || 'N/A'}%</div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'system' && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="system" className="tab-view" style={{ maxWidth: '700px', margin: '0 auto' }}>
                <div className="card">
                  <h3>System Information</h3>
                  <div style={{ marginTop: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {systemInfo ? (
                      <>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 0', borderBottom: '1px solid var(--border)' }}>
                          <span style={{ color: 'var(--text-muted)' }}>Operating System</span>
                          <span style={{ fontWeight: 600 }}>{systemInfo.os} — {systemInfo.hostname}</span>
                        </div>
                        <div style={{ fontSize: '14px', fontWeight: 700, color: 'var(--primary)', marginTop: '8px' }}>CPU</div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid var(--border)', fontSize: '13px' }}>
                          <span style={{ color: 'var(--text-muted)' }}>Model</span>
                          <span>{systemInfo.cpu.name}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid var(--border)', fontSize: '13px' }}>
                          <span style={{ color: 'var(--text-muted)' }}>Cores / Threads</span>
                          <span>{systemInfo.cpu.cores} / {systemInfo.cpu.threads}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid var(--border)', fontSize: '13px' }}>
                          <span style={{ color: 'var(--text-muted)' }}>Frequency</span>
                          <span>{systemInfo.cpu.frequency_mhz} MHz</span>
                        </div>
                        <div style={{ fontSize: '14px', fontWeight: 700, color: 'var(--success)', marginTop: '8px' }}>Memory</div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid var(--border)', fontSize: '13px' }}>
                          <span style={{ color: 'var(--text-muted)' }}>Total RAM</span>
                          <span>{systemInfo.ram.total_gb} GB</span>
                        </div>
                        <div style={{ fontSize: '14px', fontWeight: 700, color: 'var(--secondary)', marginTop: '8px' }}>Graphics</div>
                        {systemInfo.gpu.length === 0 && (
                          <div style={{ padding: '8px 0', fontSize: '13px', color: 'var(--text-muted)' }}>No GPU information available</div>
                        )}
                        {systemInfo.gpu.map((g, i) => (
                          <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid var(--border)', fontSize: '13px' }}>
                            <span style={{ color: 'var(--text-muted)' }}>{g.name}</span>
                            <span>{g.vram_gb} GB VRAM</span>
                          </div>
                        ))}
                        <div style={{ fontSize: '14px', fontWeight: 700, color: 'var(--warning)', marginTop: '8px' }}>Storage</div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', fontSize: '13px' }}>
                          <span style={{ color: 'var(--text-muted)' }}>Disk (OS)</span>
                          <span>{systemInfo.disk.free_gb} GB free / {systemInfo.disk.total_gb} GB total</span>
                        </div>
                      </>
                    ) : (
                      <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-muted)', fontSize: '13px' }}>Loading system information...</div>
                    )}
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'settings' && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="settings" className="tab-view" style={{ maxWidth: '600px', margin: '0 auto' }}>
                <div className="card">
                  <h3>General Configuration</h3>
                  <div style={{ marginTop: '32px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
                    <button
                      className="action-item"
                      style={{ justifyContent: 'space-between', padding: '20px' }}
                      onClick={() => toggleSetting('aggressive_mode')}
                    >
                      <div>
                        <div style={{ fontWeight: 700 }}>Aggressive Optimization</div>
                        <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Maximum performance for demanding games.</div>
                      </div>
                      <div style={{ width: '40px', height: '20px', background: settings.aggressive_mode ? 'var(--primary)' : 'var(--border)', borderRadius: '10px', position: 'relative', transition: '0.3s' }}>
                        <div style={{ width: '16px', height: '16px', background: 'white', borderRadius: '50%', position: 'absolute', right: settings.aggressive_mode ? '2px' : '22px', top: '2px', transition: '0.3s' }}></div>
                      </div>
                    </button>
                    <button
                      className="action-item"
                      style={{ justifyContent: 'space-between', padding: '20px' }}
                      onClick={() => toggleSetting('auto_optimize')}
                    >
                      <div>
                        <div style={{ fontWeight: 700 }}>Auto-Optimize</div>
                        <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Automatically optimize when games are detected.</div>
                      </div>
                      <div style={{ width: '40px', height: '20px', background: settings.auto_optimize ? 'var(--primary)' : 'var(--border)', borderRadius: '10px', position: 'relative', transition: '0.3s' }}>
                        <div style={{ width: '16px', height: '16px', background: 'white', borderRadius: '50%', position: 'absolute', right: settings.auto_optimize ? '2px' : '22px', top: '2px', transition: '0.3s' }}></div>
                      </div>
                    </button>
                    <button
                      className="action-item"
                      style={{ justifyContent: 'space-between', padding: '20px' }}
                      onClick={() => toggleSetting('start_on_boot')}
                    >
                      <div>
                        <div style={{ fontWeight: 700 }}>Start with Windows</div>
                        <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Launch on system startup.</div>
                      </div>
                      <div style={{ width: '40px', height: '20px', background: settings.start_on_boot ? 'var(--primary)' : 'var(--border)', borderRadius: '10px', position: 'relative', transition: '0.3s' }}>
                        <div style={{ width: '16px', height: '16px', background: 'white', borderRadius: '50%', position: 'absolute', right: settings.start_on_boot ? '2px' : '22px', top: '2px', transition: '0.3s' }}></div>
                      </div>
                    </button>
                    <div style={{ marginTop: '24px', padding: '20px', background: '#f3f4f6', borderRadius: '10px' }}>
                      <div style={{ fontSize: '12px', color: 'var(--primary)', fontWeight: 600, marginBottom: '8px' }}>BACKEND STATUS</div>
                      <code style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
                        Backend: Flask/3.0.0 • Python 3.11.2 • Bridge: Active
                      </code>
                    </div>
                    <div style={{ marginTop: '24px' }}>
                      <h3 style={{ fontSize: '16px', marginBottom: '16px' }}>Profile Manager</h3>
                      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
                        <input
                          id="profile-name-input"
                          type="text"
                          placeholder="Profile name..."
                          style={{ flex: 1, padding: '10px 14px', background: '#f9fafb', border: '1px solid var(--border)', borderRadius: '8px', color: 'var(--text)', fontSize: '13px', outline: 'none', fontFamily: 'inherit' }}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                              document.getElementById('save-profile-btn').click();
                            }
                          }}
                        />
                        <button id="save-profile-btn" className="btn" style={{ padding: '10px 20px', fontSize: '12px' }} onClick={async () => {
                          const input = document.getElementById('profile-name-input');
                          const name = input?.value?.trim();
                          if (!name) { toast.error('Enter a profile name'); return; }
                          try {
                            await axios.post(`${API_BASE}/profiles/save`, { name, ...settings });
                            input.value = '';
                            toast.success(`Profile "${name}" saved`);
                            fetchProfiles();
                          } catch { toast.error('Failed to save profile'); }
                        }}>
                          Save
                        </button>
                      </div>
                      {profiles.length === 0 && (
                        <div style={{ fontSize: '13px', color: 'var(--text-muted)', textAlign: 'center', padding: '12px' }}>
                          No saved profiles yet.
                        </div>
                      )}
                      {profiles.map((p, i) => (
                        <div key={p.name} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px', borderBottom: '1px solid var(--border)', fontSize: '13px' }}>
                          <div>
                            <div style={{ fontWeight: 600 }}>{p.name}</div>
                            <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                              Aggressive: {p.settings?.aggressive_mode ? 'ON' : 'OFF'} • Auto-Opt: {p.settings?.auto_optimize ? 'ON' : 'OFF'}
                            </div>
                          </div>
                          <div style={{ display: 'flex', gap: '8px' }}>
                            <button style={{ padding: '6px 14px', background: '#d1fae5', border: 'none', borderRadius: '6px', color: '#065f46', fontSize: '12px', fontWeight: 600, cursor: 'pointer', fontFamily: 'inherit' }} onClick={async () => {
                              try {
                                const resp = await axios.post(`${API_BASE}/profiles/apply`, { name: p.name });
                                setSettings(resp.data.settings);
                                toast.success(`Profile "${p.name}" applied`);
                              } catch { toast.error('Failed to apply profile'); }
                            }}>
                              Apply
                            </button>
                            <button style={{ padding: '6px 14px', background: '#fee2e2', border: 'none', borderRadius: '6px', color: '#991b1b', fontSize: '12px', fontWeight: 600, cursor: 'pointer', fontFamily: 'inherit' }} onClick={async () => {
                              try {
                                await axios.post(`${API_BASE}/profiles/delete`, { name: p.name });
                                toast.success(`Profile "${p.name}" deleted`);
                                fetchProfiles();
                              } catch { toast.error('Failed to delete profile'); }
                            }}>
                              Delete
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

          {/* ── DNS Switcher ── */}
          {activeTab === 'dns' && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="dns" className="tab-view" style={{ maxWidth: '680px', margin: '0 auto' }}>
              <div className="card">
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Globe size={18} color="var(--primary)" /> DNS Switcher</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '8px', marginBottom: '20px' }}>Switch DNS servers on all active adapters for lower latency gaming.</p>
                {dnsStatus?.current_preset && (
                  <div style={{ padding: '10px 14px', background: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: '8px', marginBottom: '16px', fontSize: '13px', fontWeight: 600, color: '#15803d' }}>
                    ✓ Active: {dnsStatus.current_preset}
                  </div>
                )}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '16px' }}>
                  {(dnsStatus?.available_presets || []).map(p => (
                    <button key={p.key} className="btn" style={{ justifyContent: 'flex-start', fontSize: '13px', padding: '12px 16px' }}
                      onClick={async () => { const t = toast.loading(`Switching to ${p.label}...`); try { await axios.post(`${API_BASE}/dns/switch`, { preset: p.key }); fetchDnsStatus(); toast.success(`DNS → ${p.label}`, { id: t }); } catch { toast.error('DNS switch failed', { id: t }); } }}>
                      <Globe size={14} style={{ marginRight: '8px' }} />{p.label}
                    </button>
                  ))}
                </div>
                <div style={{ borderTop: '1px solid var(--border)', paddingTop: '16px' }}>
                  <div style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '10px' }}>CUSTOM DNS</div>
                  <div style={{ display: 'flex', gap: '8px', marginBottom: '10px' }}>
                    <input placeholder="Primary (e.g. 1.1.1.1)" value={dnsCustomPrimary} onChange={e => setDnsCustomPrimary(e.target.value)}
                      style={{ flex: 1, padding: '10px 12px', border: '1px solid var(--border)', borderRadius: '8px', fontSize: '13px', outline: 'none', fontFamily: 'inherit' }} />
                    <input placeholder="Secondary (optional)" value={dnsCustomSecondary} onChange={e => setDnsCustomSecondary(e.target.value)}
                      style={{ flex: 1, padding: '10px 12px', border: '1px solid var(--border)', borderRadius: '8px', fontSize: '13px', outline: 'none', fontFamily: 'inherit' }} />
                  </div>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button className="btn" style={{ fontSize: '12px' }} onClick={async () => {
                      const t = toast.loading('Applying custom DNS...');
                      try { await axios.post(`${API_BASE}/dns/switch`, { preset: 'custom', custom_primary: dnsCustomPrimary, custom_secondary: dnsCustomSecondary }); fetchDnsStatus(); toast.success('Custom DNS applied', { id: t }); } catch { toast.error('Failed', { id: t }); }
                    }}>Apply Custom</button>
                    <button className="btn" style={{ background: '#6b7280', fontSize: '12px' }} onClick={async () => {
                      const t = toast.loading('Restoring DNS...');
                      try { await axios.post(`${API_BASE}/dns/restore`); fetchDnsStatus(); toast.success('DNS restored to DHCP', { id: t }); } catch { toast.error('Restore failed', { id: t }); }
                    }}>Restore Default (DHCP)</button>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* ── Live Ping Chart ── */}
          {activeTab === 'ping_chart' && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="ping_chart" className="tab-view">
              <div className="card" style={{ marginBottom: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                  <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Signal size={18} color="var(--primary)" /> Live Ping Monitor</h3>
                  <div className="stats-badge">LIVE</div>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '12px', marginBottom: '24px' }}>
                  {Object.entries(pingHistory).map(([host, data]) => (
                    <div key={host} style={{ padding: '14px', background: '#f9fafb', borderRadius: '10px', textAlign: 'center', border: '1px solid var(--border)' }}>
                      <div style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 700, marginBottom: '4px' }}>{data.label}</div>
                      <div style={{ fontSize: '24px', fontWeight: 800, color: data.current < 50 ? 'var(--success)' : data.current < 100 ? 'var(--warning)' : 'var(--error)' }}>
                        {data.current >= 0 ? `${data.current.toFixed(0)}ms` : '—'}
                      </div>
                      <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '4px' }}>
                        avg {data.avg >= 0 ? `${data.avg}ms` : '—'} · min {data.min >= 0 ? `${data.min}ms` : '—'}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              {Object.entries(pingHistory).map(([host, data]) => {
                const chartData = data.history.filter(h => h.latency >= 0).map(h => ({ t: h.timestamp.slice(11,19), ms: h.latency }));
                return chartData.length > 1 ? (
                  <div key={host} className="card" style={{ marginBottom: '16px' }}>
                    <div style={{ fontSize: '13px', fontWeight: 700, marginBottom: '12px', color: 'var(--primary)' }}>{data.label} ({host})</div>
                    <ResponsiveContainer width="100%" height={120}>
                      <LineChart data={chartData}>
                        <XAxis dataKey="t" tick={{ fontSize: 9 }} interval="preserveStartEnd" />
                        <YAxis tick={{ fontSize: 9 }} unit="ms" width={40} />
                        <Tooltip formatter={v => [`${v.toFixed(1)}ms`, 'Ping']} />
                        <Line type="monotone" dataKey="ms" stroke="var(--primary)" strokeWidth={2} dot={false} isAnimationActive={false} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                ) : null;
              })}
            </motion.div>
          )}

          {/* ── System Tools ── */}
          {activeTab === 'sys_tools' && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="sys_tools" className="tab-view" style={{ maxWidth: '680px', margin: '0 auto' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {/* Startup */}
                <div className="card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}><Rocket size={16} color="var(--primary)" /> Windows Startup</h3>
                      <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Launch optimizer automatically on Windows boot</p>
                    </div>
                    <button onClick={async () => {
                      const ep = startupEnabled ? '/startup/disable' : '/startup/enable';
                      const t = toast.loading(startupEnabled ? 'Removing startup entry...' : 'Adding startup entry...');
                      try { await axios.post(`${API_BASE}${ep}`); fetchStartupStatus(); toast.success(startupEnabled ? 'Removed from startup' : 'Added to startup', { id: t }); } catch { toast.error('Failed', { id: t }); }
                    }} style={{ background: 'none', border: 'none', cursor: 'pointer', color: startupEnabled ? 'var(--success)' : 'var(--text-muted)' }}>
                      {startupEnabled ? <ToggleRight size={36} /> : <ToggleLeft size={36} />}
                    </button>
                  </div>
                </div>
                {/* Network Adapter Power Save */}
                <div className="card">
                  <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}><Power size={16} color="var(--primary)" /> Network Adapter Power Saving</h3>
                  <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '16px' }}>Disable Windows power management on all network adapters to reduce latency spikes</p>
                  {adapterStatus && <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '12px' }}>Active adapters: {adapterStatus.active_adapters?.join(', ') || 'Detecting...'}</div>}
                  <button className="btn" onClick={async () => { const t = toast.loading('Disabling adapter power saving...'); try { const r = await axios.post(`${API_BASE}/adapter/power-save-disable`); toast.success(r.data.message || 'Done', { id: t }); fetchAdapterStatus(); } catch { toast.error('Failed', { id: t }); } }}>
                    Disable Power Saving
                  </button>
                </div>
                {/* IPv6 Toggle */}
                <div className="card">
                  <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}><Layers size={16} color="var(--primary)" /> IPv6 Control</h3>
                  <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '16px' }}>Disable IPv6 on all adapters — many games route better on IPv4-only</p>
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <button className="btn" onClick={async () => { const t = toast.loading('Disabling IPv6...'); try { await axios.post(`${API_BASE}/adapter/ipv6-toggle`, { disable: true }); toast.success('IPv6 disabled', { id: t }); } catch { toast.error('Failed', { id: t }); } }}>Disable IPv6</button>
                    <button className="btn" style={{ background: '#6b7280' }} onClick={async () => { const t = toast.loading('Enabling IPv6...'); try { await axios.post(`${API_BASE}/adapter/ipv6-toggle`, { disable: false }); toast.success('IPv6 enabled', { id: t }); } catch { toast.error('Failed', { id: t }); } }}>Enable IPv6</button>
                  </div>
                </div>
                {/* MTU Optimizer */}
                <div className="card">
                  <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}><Signal size={16} color="var(--primary)" /> MTU Optimizer</h3>
                  <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '16px' }}>Auto-discover and set the optimal MTU size to eliminate packet fragmentation</p>
                  <button className="btn" onClick={async () => { const t = toast.loading('Discovering optimal MTU (this may take ~15s)...', { duration: 20000 }); try { const r = await axios.post(`${API_BASE}/adapter/mtu-optimize`); toast.success(`MTU set to ${r.data.optimal_mtu} bytes`, { id: t }); } catch { toast.error('Failed', { id: t }); } }}>
                    Optimize MTU
                  </button>
                </div>
                {/* Visual Effects */}
                <div className="card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div style={{ flex: 1, marginRight: '16px' }}>
                      <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                        {visualStatus?.is_optimized ? <EyeOff size={16} color="var(--success)" /> : <Eye size={16} color="var(--primary)" />} Windows Visual Effects
                      </h3>
                      <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '16px' }}>Disable transparency, animations, and shadows for raw performance</p>
                    </div>
                    <div style={{ padding: '6px 12px', borderRadius: '20px', background: visualStatus?.is_optimized ? '#dcfce7' : '#f3f4f6', color: visualStatus?.is_optimized ? '#15803d' : 'var(--text-muted)', fontSize: '11px', fontWeight: 700, whiteSpace: 'nowrap' }}>
                      {visualStatus?.is_optimized ? 'GAMING MODE' : 'DEFAULT'}
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <button className="btn" onClick={async () => { const t = toast.loading('Applying gaming visual mode...'); try { const r = await axios.post(`${API_BASE}/visual/optimize`); fetchVisualStatus(); toast.success(`Applied ${r.data.tweaks_applied?.length || 0} tweaks`, { id: t }); } catch { toast.error('Failed', { id: t }); } }}>
                      <EyeOff size={14} style={{ marginRight: '6px' }} /> Gaming Mode
                    </button>
                    <button className="btn" style={{ background: '#6b7280' }} onClick={async () => { const t = toast.loading('Restoring visual effects...'); try { await axios.post(`${API_BASE}/visual/restore`); fetchVisualStatus(); toast.success('Visual effects restored', { id: t }); } catch { toast.error('Failed', { id: t }); } }}>
                      <Eye size={14} style={{ marginRight: '6px' }} /> Restore
                    </button>
                  </div>
                </div>
                {/* Report Export */}
                <div className="card">
                  <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}><FileText size={16} color="var(--primary)" /> System Report</h3>
                  <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '16px' }}>Export a full system diagnostics and performance report as JSON</p>
                  <button className="btn" onClick={async () => { const t = toast.loading('Generating report...'); try { const r = await axios.get(`${API_BASE}/report/export`); toast.success(`Report saved to: ${r.data.file?.split(/[\\/]/).pop()}`, { id: t, duration: 6000 }); } catch { toast.error('Report export failed', { id: t }); } }}>
                    <Download size={14} style={{ marginRight: '6px' }} /> Export Report
                  </button>
                </div>
              </div>
            </motion.div>
          )}

          {/* ── Game Library ── */}
          {activeTab === 'game_library' && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="game_library" className="tab-view">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', flexWrap: 'wrap', gap: '12px' }}>
                <div>
                  <h2 style={{ margin: 0 }}>Game Library</h2>
                  <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '4px' }}>{gameLibrary.total} games across {Object.keys(gameLibrary.by_store || {}).join(', ') || 'all stores'}</p>
                </div>
                <button className="btn" onClick={async () => { setGameScanLoading(true); const t = toast.loading('Scanning game libraries...'); try { await axios.post(`${API_BASE}/games/scan`); await fetchGameLibrary(); toast.success('Scan complete', { id: t }); } catch { toast.error('Scan failed', { id: t }); } finally { setGameScanLoading(false); } }}>
                  <RefreshCw size={14} style={{ marginRight: '6px', animation: gameScanLoading ? 'spin 1s linear infinite' : 'none' }} /> Rescan
                </button>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '12px' }}>
                {gameLibrary.games?.length > 0 ? gameLibrary.games.map((g, i) => (
                  <div key={i} className="card" style={{ padding: '14px 16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ overflow: 'hidden' }}>
                      <div style={{ fontWeight: 600, fontSize: '14px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{g.name}</div>
                      <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>{g.store}</div>
                    </div>
                    {g.launch_cmd && (
                      <button className="btn" style={{ fontSize: '11px', padding: '6px 12px', flexShrink: 0, marginLeft: '10px' }}
                        onClick={async () => { const t = toast.loading(`Launching ${g.name}...`); try { await axios.post(`${API_BASE}/games/launch`, { launch_cmd: g.launch_cmd }); toast.success(`Launched ${g.name}`, { id: t }); } catch { toast.error('Launch failed', { id: t }); } }}>
                        <Play size={12} style={{ marginRight: '4px' }} /> Launch
                      </button>
                    )}
                  </div>
                )) : (
                  <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '48px', color: 'var(--text-muted)', fontSize: '14px' }}>
                    No games found. Click <strong>Rescan</strong> to search your system.
                  </div>
                )}
              </div>
            </motion.div>
          )}

          {/* ── Scheduler ── */}
          {activeTab === 'scheduler' && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="scheduler" className="tab-view" style={{ maxWidth: '680px', margin: '0 auto' }}>
              <div className="card" style={{ marginBottom: '20px' }}>
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}><Calendar size={18} color="var(--primary)" /> Schedule Auto-Optimize</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px' }}>
                  <div>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 700, marginBottom: '6px' }}>ACTION</div>
                    <select value={scheduleForm.action} onChange={e => setScheduleForm(f => ({ ...f, action: e.target.value }))}
                      style={{ width: '100%', padding: '10px 12px', border: '1px solid var(--border)', borderRadius: '8px', fontSize: '13px', outline: 'none', fontFamily: 'inherit', background: '#fff' }}>
                      {scheduleActions.map(a => <option key={a.key} value={a.key}>{a.label}</option>)}
                    </select>
                  </div>
                  <div>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 700, marginBottom: '6px' }}>TIME</div>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <input type="number" min={0} max={23} value={scheduleForm.hour} onChange={e => setScheduleForm(f => ({ ...f, hour: e.target.value }))} placeholder="HH"
                        style={{ flex: 1, padding: '10px 12px', border: '1px solid var(--border)', borderRadius: '8px', fontSize: '13px', outline: 'none', fontFamily: 'inherit' }} />
                      <input type="number" min={0} max={59} value={scheduleForm.minute} onChange={e => setScheduleForm(f => ({ ...f, minute: e.target.value }))} placeholder="MM"
                        style={{ flex: 1, padding: '10px 12px', border: '1px solid var(--border)', borderRadius: '8px', fontSize: '13px', outline: 'none', fontFamily: 'inherit' }} />
                    </div>
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
                  <input type="checkbox" id="repeat-chk" checked={scheduleForm.repeat} onChange={e => setScheduleForm(f => ({ ...f, repeat: e.target.checked }))} />
                  <label htmlFor="repeat-chk" style={{ fontSize: '13px', cursor: 'pointer' }}>Repeat daily</label>
                </div>
                <button className="btn" onClick={async () => {
                  const t = toast.loading('Adding scheduled job...');
                  try {
                    await axios.post(`${API_BASE}/schedule/add`, { action: scheduleForm.action, hour: parseInt(scheduleForm.hour || '0'), minute: parseInt(scheduleForm.minute || '0'), repeat: scheduleForm.repeat });
                    fetchSchedule();
                    toast.success('Job scheduled', { id: t });
                  } catch { toast.error('Failed', { id: t }); }
                }}>Add Schedule</button>
              </div>
              <div className="card">
                <h3 style={{ marginBottom: '16px' }}>Active Jobs ({scheduleJobs.length})</h3>
                {scheduleJobs.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: '24px', color: 'var(--text-muted)', fontSize: '13px' }}>No scheduled jobs. Add one above.</div>
                ) : scheduleJobs.map(job => (
                  <div key={job.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '14px 0', borderBottom: '1px solid var(--border)' }}>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '14px' }}>{job.label}</div>
                      <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '2px' }}>
                        {String(job.hour).padStart(2,'0')}:{String(job.minute).padStart(2,'0')} · {job.repeat ? 'Daily' : 'Once'} · {job.enabled ? '✓ Enabled' : '⏸ Disabled'}
                      </div>
                    </div>
                    <button className="btn" style={{ background: '#ef4444', fontSize: '11px', padding: '6px 12px' }}
                      onClick={async () => { const t = toast.loading('Removing job...'); try { await axios.post(`${API_BASE}/schedule/remove`, { id: job.id }); fetchSchedule(); toast.success('Job removed', { id: t }); } catch { toast.error('Failed', { id: t }); } }}>
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          </AnimatePresence>

        </main>
      </div>
    </div>
  );
};

NeuralIntelligenceCard.propTypes = {
  data: PropTypes.object
};

LearningCoreCard.propTypes = {
  data: PropTypes.object
};

HardwareHubCard.propTypes = {
  data: PropTypes.object,
  onRunTask: PropTypes.func.isRequired
};

NetworkEvolutionCard.propTypes = {
  data: PropTypes.object,
  onRunTask: PropTypes.func.isRequired
};

CloudLinkCard.propTypes = {
  data: PropTypes.object,
  onRunTask: PropTypes.func.isRequired
};

EcosystemSyncCard.propTypes = {
  data: PropTypes.object,
  onRunTask: PropTypes.func.isRequired
};

const StatCard = ({ icon: Icon, label, value, color, progress }) => (
  <div className="card">
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
      <div style={{ width: '36px', height: '36px', borderRadius: '8px', background: `${color}15`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Icon size={18} color={color} />
      </div>
      <div>
        <div style={{ color: 'var(--text-muted)', fontSize: '11px', fontWeight: 600 }}>{label}</div>
        <div style={{ fontSize: '22px', fontWeight: 700 }}>{value}</div>
      </div>
    </div>
    <div className="progress-bar">
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        className="progress-fill"
        style={{ background: color }}
      />
    </div>
  </div>
);

StatCard.propTypes = {
  icon: PropTypes.elementType.isRequired,
  label: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  color: PropTypes.string.isRequired,
  progress: PropTypes.number.isRequired
};

const ActionItem = ({ icon: Icon, label, sub, onClick }) => (
  <button className="action-item" onClick={onClick}>
    <div style={{
      width: '36px',
      height: '36px',
      borderRadius: '8px',
      background: '#eef2ff',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'var(--primary)'
    }}>
      <Icon size={16} />
    </div>
    <div>
      <div style={{ fontSize: '14px', fontWeight: 600 }}>{label}</div>
      <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{sub}</div>
    </div>
  </button>
);

ActionItem.propTypes = {
  icon: PropTypes.elementType.isRequired,
  label: PropTypes.string.isRequired,
  sub: PropTypes.string.isRequired,
  onClick: PropTypes.func
};

export default App;
