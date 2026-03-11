import React, { useState, useEffect, useCallback } from 'react';
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
  Share2
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';
import toast, { Toaster } from 'react-hot-toast';

const API_BASE = 'http://localhost:5000/api';

// --- Sub-Components for Dashboard ---

const NeuralIntelligenceCard = ({ data }) => (
  <div className="card" style={{ border: '1px solid var(--accent-purple)', background: 'rgba(137, 0, 255, 0.03)' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
      <h3 style={{ fontSize: '18px', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <Zap size={20} color="var(--accent-purple)" />
        Neural Intelligence
      </h3>
      <div style={{ fontSize: '10px', color: 'var(--accent-purple)', fontWeight: 'bold' }}>VERSION 1.0 ALPHA</div>
    </div>

    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Stability Index</span>
        <span style={{ fontSize: '18px', fontWeight: '800', color: (data?.stability_score || 0) > 80 ? 'var(--success)' : 'var(--warning)' }}>
          {data?.stability_score || 100}%
        </span>
      </div>

      <div className="progress-bar" style={{ height: '4px', background: 'rgba(255,255,255,0.05)' }}>
        <div className="progress-fill" style={{
          width: `${data?.stability_score || 100}%`,
          background: 'var(--accent-purple)',
          boxShadow: '0 0 10px var(--accent-purple)'
        }}></div>
      </div>

      {data?.predicted_bottleneck && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          style={{
            padding: '12px',
            background: 'rgba(239, 68, 68, 0.1)',
            borderRadius: '12px',
            border: '1px solid var(--error)',
            marginTop: '8px'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--error)', fontWeight: 'bold', fontSize: '11px' }}>
            <Activity size={12} />
            PREDICTIVE WARNING
          </div>
          <div style={{ fontSize: '13px', fontWeight: 'bold', marginTop: '4px', color: 'white' }}>
            {data.predicted_bottleneck.replaceAll('_', ' ')}
          </div>
        </motion.div>
      )}

      <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px', display: 'flex', justifyContent: 'space-between' }}>
        <span>Trend Analysis: {data?.trend || 'CALCULATING'}</span>
        <span>Neural Sync: Active</span>
      </div>
    </div>
  </div>
);

const LearningCoreCard = ({ data }) => (
  <div className="card" style={{ border: '1px solid var(--accent-cyan)', background: 'rgba(0, 242, 254, 0.03)' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
      <h3 style={{ fontSize: '18px', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <HardDrive size={20} color="var(--accent-cyan)" />
        Dynamic Learning
      </h3>
      <div style={{ fontSize: '10px', color: 'var(--accent-cyan)', fontWeight: 'bold' }}>NEURAL HABITS v1.0</div>
    </div>

    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Knowledge Progress</span>
        <span style={{ fontSize: '14px', fontWeight: '800', color: 'var(--accent-cyan)' }}>
          {data?.learning_progress?.toFixed(1) || 0}%
        </span>
      </div>

      <div className="progress-bar" style={{ height: '4px', background: 'rgba(255,255,255,0.05)' }}>
        <div className="progress-fill" style={{
          width: `${data?.learning_progress || 0}%`,
          background: 'var(--accent-cyan)',
          boxShadow: '0 0 10px var(--accent-cyan)'
        }}></div>
      </div>

      <div style={{ marginTop: '8px' }}>
        <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '8px', fontWeight: 'bold' }}>IDENTIFIED BACKGROUND DRAINERS:</div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
          {data?.candidates?.length > 0 ? data.candidates.map(c => (
            <span key={c} style={{ padding: '4px 8px', background: 'rgba(0, 242, 254, 0.1)', borderRadius: '6px', fontSize: '10px', color: 'var(--accent-cyan)', border: '1px solid rgba(0, 242, 254, 0.2)' }}>
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
  <div className="card" style={{ border: '1px solid var(--error)', background: 'rgba(255, 69, 58, 0.03)' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
      <h3 style={{ fontSize: '18px', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <Activity size={20} color="var(--error)" />
        Hardware Hub
      </h3>
      <div style={{ fontSize: '10px', color: 'var(--error)', fontWeight: 'bold' }}>THERMAL GUARD ACTIVE</div>
    </div>

    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
      <div style={{ padding: '12px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid var(--border)' }}>
        <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginBottom: '4px' }}>CPU TEMP</div>
        <div style={{ fontSize: '20px', fontWeight: '800', color: (data?.cpu_temp || 0) > 70 ? 'var(--error)' : 'white' }}>
          {data?.cpu_temp?.toFixed(1) || 0}°C
        </div>
      </div>
      <div style={{ padding: '12px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid var(--border)' }}>
        <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginBottom: '4px' }}>GPU TEMP</div>
        <div style={{ fontSize: '20px', fontWeight: '800', color: (data?.gpu_temp || 0) > 70 ? 'var(--error)' : 'white' }}>
          {data?.gpu_temp?.toFixed(1) || 0}°C
        </div>
      </div>
    </div>

    <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div>
        <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>GPU PROFILE</div>
        <div style={{ fontSize: '13px', fontWeight: 'bold', color: 'var(--accent)' }}>{data?.gpu_mode || 'STANDARD'}</div>
      </div>
      <button className="glow-btn" style={{ padding: '6px 12px', fontSize: '11px' }} onClick={() => onRunTask('/optimize/gpu', 'GPU P-State Shift')}>
        MAX POWER
      </button>
    </div>

    <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '12px', textAlign: 'center' }}>
      Thermal Status: <span style={{ color: data?.thermal_status === 'COOL' ? 'var(--success)' : 'var(--error)', fontWeight: 'bold' }}>{data?.thermal_status || 'OPTIMAL'}</span>
    </div>
  </div>
);

const NetworkEvolutionCard = ({ data, onRunTask }) => (
  <div className="card" style={{ border: '1px solid var(--success)', background: 'rgba(52, 199, 89, 0.03)' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
      <h3 style={{ fontSize: '18px', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <Network size={20} color="var(--success)" />
        Network Evolution
      </h3>
      <div style={{ fontSize: '10px', color: 'var(--success)', fontWeight: 'bold' }}>GEO-ROUTING v2.0</div>
    </div>

    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Multi-Path Tunneling</span>
        <span style={{ fontSize: '12px', fontWeight: 'bold', color: data?.tunneling_active ? 'var(--success)' : 'var(--text-muted)' }}>
          {data?.tunneling_active ? 'ENABLED' : 'DISABLED'}
        </span>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Active Region</span>
        <span style={{ fontSize: '13px', fontWeight: 'bold', color: 'white' }}>{data?.current_region || 'AUTO'}</span>
      </div>

      <div style={{ padding: '12px', background: 'rgba(52, 199, 89, 0.1)', borderRadius: '12px', border: '1px solid rgba(52, 199, 89, 0.2)', marginTop: '4px' }}>
        <div style={{ fontSize: '11px', color: 'var(--success)', fontWeight: 'bold' }}>NETWORK PERFORMANCE GAIN</div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginTop: '4px' }}>
          <span style={{ fontSize: '24px', fontWeight: '800', color: 'white' }}>{data?.ping_improvement || '-0ms'}</span>
          <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>LATENCY DROP</span>
        </div>
      </div>

      <div style={{ marginTop: '8px', display: 'flex', gap: '8px' }}>
        <button className="glow-btn" style={{ flex: 1, padding: '8px', fontSize: '11px', background: data?.tunneling_active ? 'var(--success)' : 'rgba(255,255,255,0.05)' }} onClick={() => onRunTask('/optimize/network-tunnel', 'Neural Tunnel Shift', { active: !data?.tunneling_active })}>
          {data?.tunneling_active ? 'DISABLE TUNNEL' : 'ENABLE TUNNEL'}
        </button>
      </div>

      <div style={{ fontSize: '10px', color: 'var(--text-muted)', textAlign: 'center' }}>
        Packet Loss Protection: <span style={{ color: 'var(--success)', fontWeight: 'bold' }}>{data?.packet_loss_protection || 'ACTIVE'}</span>
      </div>
    </div>
  </div>
);

const CloudLinkCard = ({ data, onRunTask }) => (
  <div className="card" style={{ border: '1px solid var(--accent-blue)', background: 'rgba(0, 122, 255, 0.03)' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
      <h3 style={{ fontSize: '18px', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <Share2 size={20} color="var(--accent-blue)" />
        Cloud Link
      </h3>
      <div style={{ fontSize: '10px', color: 'var(--accent-blue)', fontWeight: 'bold' }}>GLOBAL SYNC ACTIVE</div>
    </div>

    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Global Stability Rank</span>
        <span style={{ fontSize: '14px', fontWeight: '800', color: 'var(--accent-blue)' }}>{data?.stability_rank || 'ELITE'}</span>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Neural Score</span>
        <span style={{ fontSize: '18px', fontWeight: '800', color: 'white' }}>{data?.score || 9450} XP</span>
      </div>

      <div style={{ padding: '12px', background: 'rgba(0, 122, 255, 0.1)', borderRadius: '12px', border: '1px solid rgba(0, 122, 255, 0.2)', marginTop: '4px' }}>
        <div style={{ fontSize: '11px', color: 'var(--accent-blue)', fontWeight: 'bold' }}>DISCORD RICH PRESENCE</div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '6px' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>{data?.discord_presence || 'DISCONNECTED'}</span>
          <button className="glow-btn" style={{ padding: '4px 10px', fontSize: '10px' }} onClick={() => onRunTask('/cloud/discord', 'Discord RPC Shift', { active: data?.discord_presence === 'Disconnected' })}>
            SYNC
          </button>
        </div>
      </div>

      <div style={{ fontSize: '10px', color: 'var(--text-muted)', textAlign: 'center', marginTop: '8px' }}>
        World Position: <span style={{ color: 'var(--accent-blue)', fontWeight: 'bold' }}>{data?.global_position || '#124 GLOBAL'}</span>
      </div>
    </div>
  </div>
);

const EcosystemSyncCard = ({ data, onRunTask }) => (
  <div className="card" style={{ border: '1px solid var(--accent)', background: 'rgba(94, 92, 230, 0.03)' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
      <h3 style={{ fontSize: '18px', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <Gamepad2 size={20} color="var(--accent)" />
        Ecosystem Sync
      </h3>
      <div style={{ fontSize: '10px', color: 'var(--accent)', fontWeight: 'bold' }}>NEURAL LAUNCH ACTIVE</div>
    </div>

    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Detected Hubs</span>
        <div style={{ display: 'flex', gap: '4px' }}>
          {data?.stores?.map(s => (
            <span key={s} style={{ padding: '2px 6px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px', fontSize: '9px', fontWeight: 'bold' }}>{s.toUpperCase()}</span>
          ))}
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Auto-Boost Launch</span>
        <span style={{ fontSize: '12px', fontWeight: 'bold', color: 'var(--success)' }}>ENABLED</span>
      </div>

      <div style={{ padding: '12px', background: 'rgba(94, 92, 230, 0.05)', borderRadius: '12px', border: '1px solid rgba(94, 92, 230, 0.1)', marginTop: '4px' }}>
        <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginBottom: '4px' }}>LAST NEURAL LAUNCH</div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '14px', fontWeight: '700' }}>{data?.last_boosted_launch || 'None'}</span>
          <Zap size={14} color="var(--accent)" className="pulsing" />
        </div>
      </div>

      <button className="glow-btn" style={{ marginTop: '8px', padding: '10px' }} onClick={() => onRunTask('/ecosystem/launch', 'Neural Launch Sequence', { game: 'Valorant', store: 'Steam' })}>
        QUICK LAUNCH & BOOST
      </button>

      <div style={{ fontSize: '10px', color: 'var(--text-muted)', textAlign: 'center', marginTop: '4px' }}>
        Integration Sync: <span style={{ color: 'var(--success)', fontWeight: 'bold' }}>SECURE</span>
      </div>
    </div>
  </div>
);

// --- Main App Component ---

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isApiConnected, setIsApiConnected] = useState(true);
  const [hasShownConnectionToast, setHasShownConnectionToast] = useState(false);
  const [statusData, setStatusData] = useState(null);
  const [cpuHistory, setCpuHistory] = useState([]);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [taskStatus, setTaskStatus] = useState(null);
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
        toast.success("Neural Link Synchronized", {
          id: 'conn-success',
          icon: '🧠',
          style: {
            background: '#0a0c14',
            color: '#fff',
            border: '1px solid var(--accent)',
            fontSize: '14px',
            fontWeight: '600'
          }
        });
        setHasShownConnectionToast(true);
      }
      setIsApiConnected(true);
      
      if (resp.data.neural?.history) {
        // Sync with backend history for a smooth feed
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
        toast.error("Neural Link Fractured: Reconnecting...", {
          id: 'conn-error',
          style: {
            background: '#0a0c14',
            color: '#fff',
            border: '1px solid var(--error)',
            fontSize: '14px'
          }
        });
      }
      setIsApiConnected(false);
      console.error("Fetch Error:", err);
    }
  }, [isApiConnected, hasShownConnectionToast]);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, [fetchData]);

  const closeApp = () => globalThis.location.reload();
  const minimizeApp = () => console.log('Minimize');
  const maximizeApp = () => console.log('Maximize');

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'fps_boost', label: 'FPS Boost', icon: Zap },
    { id: 'network', label: 'Network', icon: Network },
    { id: 'settings', label: 'Settings', icon: Settings }
  ];

  const SUPPORTED_GAMES = [
    'Valorant', 'CS2', 'Fortnite', 'Apex Legends',
    'League of Legends', 'Dota 2', 'PUBG', 'Rust', 'Minecraft'
  ];

  const toggleSetting = async (key) => {
    const newVal = !settings[key];
    const updated = { ...settings, [key]: newVal };
    setSettings(updated);
    
    const toastId = toast.loading(`Updating ${key.replaceAll('_', ' ')}...`, {
      style: { background: '#0a0c14', color: '#fff', border: '1px solid var(--border)' }
    });

    try {
      await axios.post(`${API_BASE}/settings`, updated);
      toast.success(`${key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')} Updated`, { id: toastId });
    } catch (err) {
      toast.error("Failed to sync settings", { id: toastId });
      console.error("Failed to update settings:", err);
    }
  };

  /**
   * Run an optimization task.
   * @param {string} endpoint - The API endpoint
   * @param {string} label - Display label for status
   * @param {object} [data={}] - Payload for the post request
   */
  const runTask = async (endpoint, label, data = {}) => {
    setTaskStatus(`Initializing ${label}...`);
    const toastId = toast.loading(`Executing ${label}...`, {
      style: { background: '#0a0c14', color: '#fff', border: '1px solid var(--accent)' }
    });

    try {
      await axios.post(`${API_BASE}${endpoint}`, data);
      setTaskStatus(`${label} Complete!`);
      toast.success(`${label} Success`, { 
        id: toastId,
        icon: '⚡',
        style: { background: '#0a0c14', color: '#fff', border: '1px solid var(--success)' }
      });
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
    const toastId = toast.loading("Executing Neural Peak Optimization...", {
      style: { background: '#0a0c14', color: '#fff', border: '1px solid var(--accent-purple)' }
    });

    try {
      await axios.post(`${API_BASE}/optimize/quick`);
      toast.success("System Peaked! Performance Maximum.", { 
        id: toastId,
        icon: '🚀',
        duration: 4000
      });
      setTimeout(() => setIsOptimizing(false), 2000);
    } catch (err) {
      toast.error("Optimization Sequence Interrupted", { id: toastId });
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
            background: '#0a0c14',
            color: '#fff',
            border: '1px solid rgba(255,255,255,0.1)',
            backdropFilter: 'blur(10px)',
            borderRadius: '12px',
          },
          success: {
            iconTheme: { primary: 'var(--success)', secondary: '#fff' }
          },
          error: {
            iconTheme: { primary: 'var(--error)', secondary: '#fff' }
          }
        }}
      />
      {/* Premium Desktop Title Bar */}
      <div style={{
        height: '32px',
        background: 'rgba(5, 6, 10, 0.8)',
        backdropFilter: 'blur(10px)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '0 12px',
        WebkitAppRegion: 'drag',
        borderBottom: '1px solid var(--border)',
        zIndex: 1000
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--accent)', boxShadow: '0 0 10px var(--accent)' }}></div>
          <div style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: '800', letterSpacing: '1.5px', textTransform: 'uppercase' }}>Neural Optimizer Core v2.2.6</div>
        </div>
        <div style={{ display: 'flex', WebkitAppRegion: 'no-drag' }}>
          <button onClick={minimizeApp} className="window-ctrl">─</button>
          <button onClick={maximizeApp} className="window-ctrl">☐</button>
          <button onClick={closeApp} className="window-ctrl close">✕</button>
        </div>
      </div>

      <div style={{ display: 'flex', height: 'calc(100vh - 32px)', overflow: 'hidden' }}>
        {/* Floating Sidebar */}
        <motion.div
          initial={{ x: -100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.8, ease: "circOut" }}
          className="sidebar glass"
        >
          <div className="brand" style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '0 10px 40px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              background: 'linear-gradient(135deg, var(--accent), var(--accent-purple))',
              borderRadius: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 8px 16px rgba(94, 92, 230, 0.3)'
            }}>
              <Activity size={20} color="white" />
            </div>
            <div>
              <h2 style={{ fontSize: '16px', fontWeight: '900', letterSpacing: '-0.5px' }}>NGXSMK</h2>
              <div style={{ fontSize: '10px', color: 'var(--accent)', fontWeight: 'bold' }}>NEURAL CORE</div>
            </div>
          </div>

          <nav style={{ flex: 1 }}>
            {navItems.map((item, index) => (
              <motion.button
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.1 + index * 0.05 }}
                key={item.id}
                className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                onClick={() => setActiveTab(item.id)}
              >
                <item.icon size={18} style={{ opacity: activeTab === item.id ? 1 : 0.6 }} />
                <span>{item.label}</span>
              </motion.button>
            ))}
          </nav>

          <div style={{ marginTop: 'auto' }}>
            <div className="card" style={{ padding: '16px', background: 'rgba(255,255,255,0.02)', border: '1px dashed var(--border)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div className="pulsing" style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--success)' }}></div>
                <div style={{ fontSize: '12px', fontWeight: '600' }}>System Status</div>
              </div>
              <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>Neural Link is Stable</div>
            </div>
          </div>
        </motion.div>

        {/* Improved Main Content */}
        <main className="main-content">
          <motion.header
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
            style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '48px' }}
          >
            <div>
              <h1 style={{ fontSize: '36px', marginBottom: '4px' }}>Command <span className="glow-text">Center</span></h1>
              <p style={{ color: 'var(--text-secondary)', fontSize: '15px' }}>
                {isApiConnected ? (
                  <>Welcome back. Neural cores are <span style={{ color: 'var(--success)', fontWeight: '600' }}>synchronized</span>.</>
                ) : (
                  <span style={{ color: 'var(--error)', fontWeight: 'bold' }}>⚠️ Neural Core Offline: Backend Unreachable</span>
                )}
              </p>
            </div>
            {!isApiConnected && (
              <button className="glow-btn" onClick={fetchData} style={{ padding: '10px 20px', borderRadius: '12px' }}>
                RE-SYNC CORE
              </button>
            )}
            {isApiConnected && (
              <button
                className={`glow-btn ${isOptimizing ? 'pulsing' : ''}`}
                onClick={handleOptimize}
                disabled={isOptimizing}
                style={{ background: isOptimizing ? 'var(--success)' : 'var(--accent)', padding: '14px 28px', borderRadius: '14px', fontSize: '14px', fontWeight: '700' }}
              >
                {isOptimizing ? 'PEAKING PERFORMANCE...' : 'QUICK OPTIMIZE'}
              </button>
            )}
          </motion.header>

          <AnimatePresence mode="wait">
            {activeTab === 'dashboard' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                key="dashboard"
                style={{ display: 'flex', gap: '24px', flexDirection: 'column' }}
              >
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: '24px', alignItems: 'start' }}>
                  <motion.div
                    initial={{ x: -20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.3 }}
                    className="card"
                    style={{ minHeight: '400px', display: 'flex', flexDirection: 'column' }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
                      <div>
                        <h3 style={{ fontSize: '20px', marginBottom: '4px' }}>Neural Performance Feed</h3>
                        <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Real-time CPU cycle analysis</div>
                      </div>
                      <div className="stats-badge secondary">LIVE DATA</div>
                    </div>
                    <div style={{ flex: 1, minHeight: '300px' }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={cpuHistory}>
                          <defs>
                            <linearGradient id="colorCpu" x1="0" y1="0" x2="0" y2="1">
                              <stop offset="5%" stopColor="var(--accent)" stopOpacity={0.4} />
                              <stop offset="95%" stopColor="var(--accent)" stopOpacity={0} />
                            </linearGradient>
                          </defs>
                          <Area
                            type="monotone"
                            dataKey="cpu"
                            stroke="var(--accent)"
                            fillOpacity={1}
                            fill="url(#colorCpu)"
                            strokeWidth={4}
                            isAnimationActive={false}
                          />
                        </AreaChart>
                      </ResponsiveContainer>
                    </div>
                  </motion.div>

                  <motion.div
                    initial={{ x: 20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.4 }}
                    style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}
                  >
                    <div className="card">
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                        <h3 style={{ fontSize: '18px' }}>Neural Tasks</h3>
                        {taskStatus && (
                          <motion.div
                            initial={{ opacity: 0, x: 10 }}
                            animate={{ opacity: 1, x: 0 }}
                            style={{ fontSize: '10px', color: taskStatus.includes('Error') ? 'var(--error)' : 'var(--accent)', fontWeight: 'bold', textTransform: 'uppercase' }}
                          >
                            {taskStatus}
                          </motion.div>
                        )}
                      </div>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        <ActionItem icon={Trash2} label="Memory Purge" sub="Force RAM stabilization" onClick={() => runTask('/optimize/ram', 'RAM Flush')} />
                        <ActionItem icon={Network} label="Network Tuner" sub="Optimize routing tables" onClick={() => runTask('/optimize/network', 'Net Tuner')} />
                        <ActionItem icon={Zap} label="Core Boost" sub="Aggressive process priority" onClick={() => runTask('/optimize/fps', 'Core Boost')} />
                      </div>
                    </div>

                    <NeuralIntelligenceCard data={statusData?.neural} />
                  </motion.div>

                  <motion.div
                    initial={{ x: 20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.5 }}
                  >
                    <LearningCoreCard data={statusData?.learning} />
                  </motion.div>

                  <motion.div
                    initial={{ x: 20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.6 }}
                  >
                    <HardwareHubCard data={statusData?.hardware} onRunTask={runTask} />
                  </motion.div>

                  <motion.div
                    initial={{ x: 20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.7 }}
                  >
                    <NetworkEvolutionCard data={statusData?.net_evolution} onRunTask={runTask} />
                  </motion.div>

                  <motion.div
                    initial={{ x: 20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.8 }}
                  >
                    <CloudLinkCard data={statusData?.cloud} onRunTask={runTask} />
                  </motion.div>

                  <motion.div
                    initial={{ x: 20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.9 }}
                  >
                    <EcosystemSyncCard data={statusData?.ecosystem} onRunTask={runTask} />
                  </motion.div>
                </div>
              </motion.div>
            )}

            {activeTab === 'fps_boost' && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="fps" className="tab-view">
                <div className="stats-grid">
                  <StatCard icon={Zap} label="Optimized" value={statusData?.fps?.optimized_processes || 0} color="var(--accent)" progress={statusData?.fps?.optimized_processes * 10} />
                  <StatCard icon={ShieldCheck} label="Stability" value="Locked" color="var(--success)" progress={100} />
                </div>
                <div className="card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                    <h3>Process Monitor</h3>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 'bold' }}>SCANNING SYSTEM PROCESSES...</div>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '16px' }}>
                    {SUPPORTED_GAMES.map(g => {
                      const isOptimized = statusData?.fps?.optimized_details?.some(p => p.name.toLowerCase().includes(g.toLowerCase()));
                      return (
                        <div key={g} style={{
                          padding: '16px',
                          background: isOptimized ? 'rgba(94, 92, 230, 0.1)' : 'rgba(255,255,255,0.02)',
                          borderRadius: '16px',
                          border: isOptimized ? '1px solid var(--accent)' : '1px solid var(--border)',
                          textAlign: 'center',
                          position: 'relative',
                          overflow: 'hidden'
                        }}>
                          {isOptimized && <div style={{ position: 'absolute', top: '4px', right: '4px', width: '6px', height: '6px', borderRadius: '50%', background: 'var(--accent)', boxShadow: '0 0 10px var(--accent)' }}></div>}
                          <div style={{ fontWeight: '600', fontSize: '14px', color: isOptimized ? 'var(--accent)' : 'var(--text-primary)' }}>{g}</div>
                          <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '4px' }}>
                            {isOptimized ? 'NEURAL FLASH ACTIVE' : 'IDLE / NOT DETECTED'}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div className="card" style={{ marginTop: '24px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                    <h3>High Impact Processes</h3>
                    <div style={{ fontSize: '11px', color: 'var(--error)', fontWeight: 'bold' }}>RESOURCE DRAINS DETECTED</div>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    {(statusData?.ram?.top_procs || []).map((p) => (
                      <div key={`${p.pid}-${p.name}`} style={{ display: 'flex', alignItems: 'center', gap: '20px', padding: '16px', background: 'rgba(255,255,255,0.01)', borderRadius: '12px', border: '1px solid var(--border)' }}>
                        <div style={{ width: '60px', height: '40px', borderRadius: '10px', background: 'rgba(239, 68, 68, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--error)', fontSize: '10px', fontWeight: 'bold' }}>
                          PID {p.pid}
                        </div>
                        <div style={{ flex: 1 }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                            <span style={{ fontWeight: '600', fontSize: '14px' }}>{p.name}</span>
                            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{p.memory_mb?.toFixed(0) || 0} MB</span>
                          </div>
                          <div className="progress-bar" style={{ height: '4px', marginTop: '0' }}>
                            <div className="progress-fill" style={{ width: `${Math.min(100, (p.memory_mb / 1024) * 100)}%`, background: 'var(--error)', boxShadow: 'none' }}></div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'network' && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="network" className="tab-view">
                <div className="stats-grid">
                  <StatCard icon={Network} label="Network Load" value={`${statusData?.network?.load || 0}%`} color="var(--accent-cyan)" progress={statusData?.network?.load || 0} />
                  <StatCard icon={ShieldCheck} label="Geo Routing" value="Secure" color="var(--success)" progress={100} />
                </div>
                <div className="card">
                  <h3>Network Interface Analysis</h3>
                  <div style={{ marginTop: '24px' }}>
                    {(statusData?.network?.interfaces || []).map((iface) => (
                      <div key={`${iface.name}-${iface.ip}`} style={{ padding: '16px', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between' }}>
                        <div>
                          <div style={{ fontWeight: 'bold' }}>{iface.name}</div>
                          <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{iface.ip}</div>
                        </div>
                        <div style={{ textAlign: 'right' }}>
                          <div style={{ color: 'var(--success)', fontWeight: 'bold' }}>ACTIVE</div>
                          <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{iface.speed} Mbps</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'settings' && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} key="settings" className="tab-view" style={{ maxWidth: '600px', margin: '0 auto' }}>
                <div className="card">
                  <h3>General Configuration</h3>
                  <div style={{ marginTop: '32px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
                    <button
                      className="action-item"
                      style={{ justifyContent: 'space-between', padding: '20px' }}
                      onClick={() => toggleSetting('aggressive_mode')}
                    >
                      <div>
                        <div style={{ fontWeight: '700' }}>Aggressive Optimization</div>
                        <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Unleash full neural power for maximum FPS.</div>
                      </div>
                      <div style={{ width: '40px', height: '20px', background: settings.aggressive_mode ? 'var(--accent)' : 'var(--border)', borderRadius: '10px', position: 'relative', transition: '0.3s' }}>
                        <div style={{ width: '16px', height: '16px', background: 'white', borderRadius: '50%', position: 'absolute', right: settings.aggressive_mode ? '2px' : '22px', top: '2px', transition: '0.3s' }}></div>
                      </div>
                    </button>
                    <button
                      className="action-item"
                      style={{ justifyContent: 'space-between', padding: '20px' }}
                      onClick={() => toggleSetting('auto_optimize')}
                    >
                      <div>
                        <div style={{ fontWeight: '700' }}>Auto-Optimize</div>
                        <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Automatically trigger peaks when games are detected.</div>
                      </div>
                      <div style={{ width: '40px', height: '20px', background: settings.auto_optimize ? 'var(--accent)' : 'var(--border)', borderRadius: '10px', position: 'relative', transition: '0.3s' }}>
                        <div style={{ width: '16px', height: '16px', background: 'white', borderRadius: '50%', position: 'absolute', right: settings.auto_optimize ? '2px' : '22px', top: '2px', transition: '0.3s' }}></div>
                      </div>
                    </button>
                    <button
                      className="action-item"
                      style={{ justifyContent: 'space-between', padding: '20px' }}
                      onClick={() => toggleSetting('start_on_boot')}
                    >
                      <div>
                        <div style={{ fontWeight: '700' }}>Start with Windows</div>
                        <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Initialize neural links on system boot.</div>
                      </div>
                      <div style={{ width: '40px', height: '20px', background: settings.start_on_boot ? 'var(--accent)' : 'var(--border)', borderRadius: '10px', position: 'relative', transition: '0.3s' }}>
                        <div style={{ width: '16px', height: '16px', background: 'white', borderRadius: '50%', position: 'absolute', right: settings.start_on_boot ? '2px' : '22px', top: '2px', transition: '0.3s' }}></div>
                      </div>
                    </button>
                    <div style={{ marginTop: '24px', padding: '24px', background: 'rgba(94, 92, 230, 0.05)', borderRadius: '16px', border: '1px solid var(--border)' }}>
                      <div style={{ fontSize: '12px', color: 'var(--accent)', fontWeight: 'bold', marginBottom: '8px' }}>NEURAL BRIDGE STATUS</div>
                      <code style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
                        Backend: Flask/3.0.0 • Python 3.11.2 • Bridge: Active
                      </code>
                    </div>
                  </div>
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
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
      <div style={{
        width: '40px',
        height: '40px',
        borderRadius: '12px',
        background: `rgba(${color === 'var(--accent)' ? '94, 92, 230' : '0, 242, 254'}, 0.1)`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <Icon size={20} color={color} />
      </div>
      <div>
        <div style={{ color: 'var(--text-muted)', fontSize: '12px', fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: '1px' }}>{label}</div>
        <div style={{ fontSize: '24px', fontWeight: '800' }}>{value}</div>
      </div>
    </div>
    <div className="progress-bar">
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        className="progress-fill"
        style={{ background: color, boxShadow: `0 0 10px ${color}` }}
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
      width: '40px',
      height: '40px',
      borderRadius: '10px',
      background: 'rgba(94, 92, 230, 0.1)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'var(--accent)'
    }}>
      <Icon size={18} />
    </div>
    <div>
      <div style={{ fontSize: '14px', fontWeight: '700' }}>{label}</div>
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
