import React, { useState, useEffect } from 'react';

const GITHUB_REPO = 'https://github.com/NGXSMK/ngxsmk-gamenet-optimizer';
const BASE = '/ngxsmk-gamenet-optimizer';
const DOWNLOAD_URL_64 = `${BASE}/assets/NGXSMK_GameNet_Optimizer_x64.exe`;
const DOWNLOAD_URL_32 = `${BASE}/assets/NGXSMK_GameNet_Optimizer_x86.exe`;
const DOWNLOAD_URL_SETUP = `${BASE}/assets/NGXSMK_GameNet_Optimizer_Setup.exe`;

const features = [
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
      </svg>
    ),
    title: 'One-Click FPS Boost',
    desc: 'Instantly prioritize your game processes, adjust CPU affinity, and disable background bloat. See results in seconds, not minutes.',
    color: '#6366f1',
  },
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
      </svg>
    ),
    title: 'Intelligent Ping Reducer',
    desc: 'Optimizes your network stack, DNS, and routing in real-time. Drops latency by 20-40% in Valorant, League, CS2, Fortnite, and more.',
    color: '#10b981',
  },
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z"/>
        <path d="M12 6v6l4 2"/>
      </svg>
    ),
    title: 'AI-Powered Tuning',
    desc: 'Neural engine analyzes your system patterns live. It predicts bottlenecks before they happen and adjusts settings automatically.',
    color: '#8b5cf6',
  },
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
        <path d="M8 7h8"/>
        <path d="M8 11h6"/>
        <path d="M8 15h4"/>
      </svg>
    ),
    title: 'RAM Cleaner & Manager',
    desc: 'Frees up 50%+ more RAM than Windows alone. Intelligently suspends only what matters — never crashes your game.',
    color: '#f59e0b',
  },
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="23 7 16 12 23 17 23 7"/>
        <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
      </svg>
    ),
    title: 'Auto Game Detection',
    desc: 'Detects Valorant, LoL, CS2, Fortnite, Apex, PUBG, and more running. Applies the perfect optimization profile instantly.',
    color: '#ec4899',
  },
  {
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
      </svg>
    ),
    title: 'Real-Time Dashboard',
    desc: 'Live CPU, RAM, network charts with trend analysis. See exactly what your PC is doing — and how much performance you just gained.',
    color: '#06b6d4',
  },
];

const supportedGames = [
  { name: 'Valorant', icon: 'V' },
  { name: 'League of Legends', icon: 'L' },
  { name: 'CS2', icon: 'CS' },
  { name: 'Fortnite', icon: 'F' },
  { name: 'Apex Legends', icon: 'A' },
  { name: 'PUBG', icon: 'P' },
  { name: 'Dota 2', icon: 'D' },
  { name: 'Minecraft', icon: 'M' },
  { name: 'Rust', icon: 'R' },
];

const faqs = [
  {
    q: 'Is this safe? Will I get banned?',
    a: 'Completely safe. GameNet Optimizer uses only standard Windows APIs — it never touches game memory or executables. It is fully compatible with Vanguard, EAC, VAC, and all major anti-cheat systems. The entire source code is open for audit.',
  },
  {
    q: 'Is it really free? No hidden paywalls?',
    a: '100% free and open-source under the MIT license. No ads, no premium tiers, no data selling, no account required. Download, run, and enjoy.',
  },
  {
    q: 'Will it work on my low-end PC?',
    a: 'Yes — it was designed FOR low-end PCs. The built-in Low Power Mode reduces CPU overhead to near zero while still delivering meaningful FPS gains. Runs on both 32-bit and 64-bit Windows 10/11.',
  },
  {
    q: 'Does it collect my data?',
    a: 'No. GameNet Optimizer runs entirely offline. No telemetry, no analytics, no accounts, no internet required (except for the optional speed test feature). What happens on your PC stays on your PC.',
  },
  {
    q: 'How is this different from Razer Cortex / MSI Afterburner?',
    a: 'Those tools are either bloated, have paywalls, or focus on hardware overlays. GameNet Optimizer is a lean, all-in-one optimizer that combines FPS boosting, network tuning, RAM cleaning, and AI-driven automation in a single 15MB executable — with zero ads and zero cost.',
  },
];

const comparisonData = [
  ['Price', 'Free', 'Freemium', 'Free', 'Free'],
  ['FPS Boost', 'Yes', 'Yes', 'No', 'No'],
  ['Ping Reducer', 'Yes', 'No', 'No', 'No'],
  ['AI Auto-Tuning', 'Yes', 'No', 'No', 'No'],
  ['RAM Cleaner', 'Yes', 'Yes', 'No', 'Yes'],
  ['Game Auto-Detect', 'Yes', 'No', 'No', 'No'],
  ['Network QoS', 'Yes', 'No', 'No', 'No'],
  ['Open Source', 'Yes', 'No', 'No', 'No'],
  ['No Ads', 'Yes', 'No', 'Yes', 'Yes'],
  ['Portable EXE', 'Yes', 'Yes', 'Yes', 'Yes'],
  ['File Size', '~15 MB', '~80 MB', '~200 MB', '~50 MB'],
];

const GitHubStars = () => {
  const [stars, setStars] = useState(null);

  useEffect(() => {
    fetch('https://api.github.com/repos/NGXSMK/ngxsmk-gamenet-optimizer')
      .then(r => r.json())
      .then(d => setStars(d.stargazers_count || '0'))
      .catch(() => setStars('0'));
  }, []);

  return stars ? (
    <span className="gh-stars">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
      {stars} Stars on GitHub
    </span>
  ) : null;
};

const App = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  const scrollTo = (id) => {
    setMenuOpen(false);
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="page">
      <header className="header">
        <div className="container header-inner">
          <div className="logo" onClick={() => scrollTo('hero')} style={{ cursor: 'pointer' }}>
            <div className="logo-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
              </svg>
            </div>
            <div>
              <span className="logo-text">GameNet Optimizer</span>
              <span className="logo-badge">by NGXSMK</span>
            </div>
          </div>
          <nav className={`nav ${menuOpen ? 'open' : ''}`}>
            <a href="#features" onClick={(e) => { e.preventDefault(); scrollTo('features'); }}>Features</a>
            <a href="#showcase" onClick={(e) => { e.preventDefault(); scrollTo('showcase'); }}>Screenshots</a>
            <a href="#faq" onClick={(e) => { e.preventDefault(); scrollTo('faq'); }}>FAQ</a>
            <a href={DOWNLOAD_URL_SETUP} target="_blank" rel="noopener noreferrer" className="nav-download">Download</a>
          </nav>
          <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle menu">
            <span></span><span></span><span></span>
          </button>
        </div>
      </header>

      <main>
        {/* Hero */}
        <section id="hero" className="hero">
          <div className="container">
            <div className="hero-content">
              <GitHubStars />
              <div className="hero-badge">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                Open Source &middot; Free &middot; Windows 10/11
              </div>
              <h1>
                Stop Tolerating Low FPS & High Ping
              </h1>
              <p className="hero-subtitle">
                One click optimizes your entire PC for gaming. AI-powered tuning, RAM recovery, network 
                stack optimization — all in a single, free, open-source tool.
              </p>
              <div className="hero-actions">
                <a href={DOWNLOAD_URL_SETUP} target="_blank" rel="noopener noreferrer" className="btn btn-primary btn-large">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                  Download Free (Setup)
                </a>
                <a href="#showcase" onClick={(e) => { e.preventDefault(); scrollTo('showcase'); }} className="btn btn-secondary btn-large">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                  See It in Action
                </a>
              </div>
            </div>
          </div>
        </section>

        {/* Problem / Pain Point */}
        <section className="problem">
          <div className="container">
            <h2 className="section-title">Frustrated by <span className="highlight">Lag and Stutters</span>?</h2>
            <p className="section-subtitle">
              You upgraded your GPU. You tweaked settings. But games still feel choppy. 
              The problem isn't your hardware — it's what Windows is doing behind your back.
            </p>
            <div className="problem-grid">
              <div className="problem-card">
                <div className="problem-icon" style={{ background: '#fef2f2', color: '#ef4444' }}>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                </div>
                <h3>100+ Background Processes</h3>
                <p>Windows runs dozens of services you don't need while gaming. They eat CPU cycles and RAM.</p>
              </div>
              <div className="problem-card">
                <div className="problem-icon" style={{ background: '#fffbeb', color: '#f59e0b' }}>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                </div>
                <h3>Suboptimal Network Stack</h3>
                <p>Default Windows network settings prioritize background traffic over your game data.</p>
              </div>
              <div className="problem-card">
                <div className="problem-icon" style={{ background: '#f5f3ff', color: '#8b5cf6' }}>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M9 9h.01"/><path d="M15 9h.01"/><path d="M9 15h.01"/><path d="M15 15h.01"/></svg>
                </div>
                <h3>Memory Fragmentation</h3>
                <p>Apps leak memory over time. Your 16 GB of RAM effectively becomes 8 GB after a few hours.</p>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="how-it-works">
          <div className="container">
            <h2 className="section-title">How It Works</h2>
            <p className="section-subtitle">Three clicks. Zero complexity.</p>
            <div className="steps">
              <div className="step">
                <div className="step-number">1</div>
                <h3>Download & Run</h3>
                <p>Download the 15 MB portable EXE. No installation, no setup, no account needed.</p>
              </div>
              <div className="step-arrow">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" strokeWidth="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
              </div>
              <div className="step">
                <div className="step-number">2</div>
                <h3>Click "Quick Optimize"</h3>
                <p>The AI neural engine analyzes your system, frees RAM, tweaks network settings, and prioritizes your games.</p>
              </div>
              <div className="step-arrow">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" strokeWidth="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
              </div>
              <div className="step">
                <div className="step-number">3</div>
                <h3>Play. Dominate. Repeat.</h3>
                <p>That's it. Launch any game — auto-detection kicks in. Sit back and enjoy the smoothest gaming of your life.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="features">
          <div className="container">
            <h2 className="section-title">Everything in One Tool</h2>
            <p className="section-subtitle">
              Nine powerful modules. One clean interface. Zero bloat.
            </p>
            <div className="features-grid">
              {features.map((f, i) => (
                <article key={i} className="feature-card" style={{ '--accent': f.color }}>
                  <div className="feature-icon" style={{ color: f.color, background: `${f.color}12` }}>{f.icon}</div>
                  <h3>{f.title}</h3>
                  <p>{f.desc}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* Supported Games */}
        <section className="games">
          <div className="container">
            <h2 className="section-title">Optimized for Your Favorite Games</h2>
            <p className="section-subtitle">
              Auto-detects and applies the perfect profile. More games added regularly.
            </p>
            <div className="games-grid">
              {supportedGames.map((g, i) => (
                <div key={i} className="game-badge">
                  <div className="game-icon">{g.icon}</div>
                  <span>{g.name}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Screenshots / Showcase */}
        <section id="showcase" className="showcase">
          <div className="container">
            <h2 className="section-title">What You'll See</h2>
            <p className="section-subtitle">Clean, modern interface. Real-time data. Total control.</p>
            <div className="showcase-grid">
              <div className="showcase-card">
                <div className="showcase-img">
                  <div className="mockup">
                    <div className="mockup-header">
                      <div className="mockup-dot" style={{ background: '#ef4444' }}></div>
                      <div className="mockup-dot" style={{ background: '#f59e0b' }}></div>
                      <div className="mockup-dot" style={{ background: '#10b981' }}></div>
                      <span className="mockup-title">GameNet Optimizer v2.3 &mdash; Dashboard</span>
                    </div>
                    <div className="mockup-body">
                      <div className="mockup-sidebar">
                        <div className="mockup-nav-item active">Dashboard</div>
                        <div className="mockup-nav-item">FPS Boost</div>
                        <div className="mockup-nav-item">Network</div>
                        <div className="mockup-nav-item">System</div>
                        <div className="mockup-nav-item">Settings</div>
                      </div>
                      <div className="mockup-content">
                        <div className="mockup-chart">
                          <div className="mockup-chart-line" style={{ width: '85%' }}></div>
                          <div className="mockup-chart-line" style={{ width: '60%' }}></div>
                          <div className="mockup-chart-line" style={{ width: '75%' }}></div>
                          <div className="mockup-chart-line" style={{ width: '45%' }}></div>
                          <div className="mockup-chart-line" style={{ width: '90%' }}></div>
                          <div className="mockup-chart-line" style={{ width: '55%' }}></div>
                          <div className="mockup-chart-line" style={{ width: '70%' }}></div>
                        </div>
                        <div className="mockup-cards">
                          <div className="mockup-stat"><div className="mockup-stat-value">32%</div><div className="mockup-stat-label">CPU</div></div>
                          <div className="mockup-stat"><div className="mockup-stat-value">45%</div><div className="mockup-stat-label">RAM</div></div>
                          <div className="mockup-stat"><div className="mockup-stat-value">12ms</div><div className="mockup-stat-label">Ping</div></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <h3>Live Dashboard</h3>
                <p>Real-time CPU, RAM, and network monitoring with historical charting.</p>
              </div>
              <div className="showcase-card">
                <div className="showcase-img">
                  <div className="mockup mockup-alt">
                    <div className="mockup-header">
                      <div className="mockup-dot" style={{ background: '#ef4444' }}></div>
                      <div className="mockup-dot" style={{ background: '#f59e0b' }}></div>
                      <div className="mockup-dot" style={{ background: '#10b981' }}></div>
                      <span className="mockup-title">Performance Benchmark</span>
                    </div>
                    <div className="mockup-body" style={{ flexDirection: 'column', padding: '20px' }}>
                      <div style={{ display: 'flex', gap: '16px', marginBottom: '16px' }}>
                        <div className="mockup-stat"><div className="mockup-stat-value" style={{ color: '#ef4444' }}>47%</div><div className="mockup-stat-label">CPU Before</div></div>
                        <div className="mockup-arrow">&rarr;</div>
                        <div className="mockup-stat"><div className="mockup-stat-value" style={{ color: '#10b981' }}>28%</div><div className="mockup-stat-label">CPU After</div></div>
                      </div>
                      <div className="benchmark-bar">
                        <div className="benchmark-fill" style={{ width: '65%', background: 'linear-gradient(90deg, #10b981, #6366f1)' }}>+19% FPS</div>
                      </div>
                    </div>
                  </div>
                </div>
                <h3>Before & After Benchmark</h3>
                <p>See exactly how much performance you reclaimed with one click.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Comparison */}
        <section className="comparison">
          <div className="container">
            <h2 className="section-title">How We Stack Up</h2>
            <p className="section-subtitle">No bloat. No paywalls. Just results.</p>
            <div className="comparison-table-wrapper">
              <table className="comparison-table">
                <thead>
                  <tr>
                    <th></th>
                    <th className="highlight-col"><span className="highlight">GameNet Optimizer</span></th>
                    <th>Razer Cortex</th>
                    <th>MSI Afterburner</th>
                    <th>CCleaner</th>
                  </tr>
                </thead>
                <tbody>
                  {comparisonData.map((row, i) => (
                    <tr key={i}>
                      <td className="feature-name">{row[0]}</td>
                      <td className="highlight-col">{row[1] === 'Yes' || row[1] === 'Free' ? <span className="check">&#10003;</span> : row[1]}</td>
                      <td>{row[2] === 'Yes' || row[2] === 'Freemium' ? <span className="check dim">&#10003;</span> : row[2] === 'No' ? <span className="cross">&#10007;</span> : row[2]}</td>
                      <td>{row[3] === 'Yes' ? <span className="check dim">&#10003;</span> : row[3] === 'No' ? <span className="cross">&#10007;</span> : row[3]}</td>
                      <td>{row[4] === 'Yes' ? <span className="check dim">&#10003;</span> : row[4] === 'No' ? <span className="cross">&#10007;</span> : row[4]}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* Trust / Stats */}
        <section className="trust">
          <div className="container">
            <div className="trust-grid">
              <div className="trust-item">
                <div className="trust-icon" style={{ background: '#ecfdf5', color: '#10b981' }}>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                </div>
                <h3>Open Source</h3>
                <p>MIT licensed. Every line of code is public and auditable. No backdoors, no secrets.</p>
              </div>
              <div className="trust-item">
                <div className="trust-icon" style={{ background: '#fef2f2', color: '#ef4444' }}>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                </div>
                <h3>Privacy First</h3>
                <p>Zero data collection. Zero telemetry. Zero accounts. Runs completely offline.</p>
              </div>
              <div className="trust-item">
                <div className="trust-icon" style={{ background: '#fffbeb', color: '#f59e0b' }}>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M8 12l2 2 4-4"/></svg>
                </div>
                <h3>Lightweight</h3>
                <p>15 MB portable EXE. No installers. No background services. No registry changes.</p>
              </div>
              <div className="trust-item">
                <div className="trust-icon" style={{ background: '#f5f3ff', color: '#8b5cf6' }}>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>
                </div>
                <h3>Anti-Cheat Safe</h3>
                <p>Compatible with Vanguard, EAC, VAC, and all major anti-cheat systems.</p>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section id="faq" className="faq">
          <div className="container">
            <h2 className="section-title">Frequently Asked Questions</h2>
            <div className="faq-list">
              {faqs.map((f, i) => (
                <details key={i}>
                  <summary>{f.q}</summary>
                  <p>{f.a}</p>
                </details>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Banner */}
        <section className="cta-banner">
          <div className="container">
            <h2>Ready to Dominate?</h2>
            <p>Download GameNet Optimizer free. No sign-up. No strings attached.</p>
            <a href={DOWNLOAD_URL_SETUP} target="_blank" rel="noopener noreferrer" className="btn btn-primary btn-large">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Download v2.3.1 Free (Setup)
            </a>
            <p className="cta-meta">
              <span>15 MB &middot; Portable EXE</span>
              <span> &middot; Windows 10/11 (32 &amp; 64-bit)</span>
            </p>
          </div>
        </section>
      </main>

      <footer className="footer">
        <div className="container">
          <div className="footer-grid">
            <div className="footer-brand">
              <h4>GameNet Optimizer</h4>
              <p>Built with frustration for lag, stutters, and bloated "optimizers" that don't deliver. By gamers, for gamers.</p>
              <a href={GITHUB_REPO} target="_blank" rel="noopener noreferrer" className="footer-gh-link">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
                GitHub
              </a>
            </div>
            <div className="footer-col">
              <h4>Product</h4>
              <a href="#features" onClick={(e) => { e.preventDefault(); scrollTo('features'); }}>Features</a>
              <a href="#showcase" onClick={(e) => { e.preventDefault(); scrollTo('showcase'); }}>Screenshots</a>
              <a href={DOWNLOAD_URL_SETUP} target="_blank" rel="noopener noreferrer">Download Setup</a>
              <a href={DOWNLOAD_URL_64} target="_blank" rel="noopener noreferrer">Download 64-bit</a>
              <a href={DOWNLOAD_URL_32} target="_blank" rel="noopener noreferrer">Download 32-bit</a>
              <a href={GITHUB_REPO} target="_blank" rel="noopener noreferrer">View Source</a>
            </div>
            <div className="footer-col">
              <h4>Support</h4>
              <a href={`${GITHUB_REPO}/issues`} target="_blank" rel="noopener noreferrer">Report Bug</a>
              <a href={`${GITHUB_REPO}/discussions`} target="_blank" rel="noopener noreferrer">Discussions</a>
              <a href={`${GITHUB_REPO}/blob/main/SECURITY.md`} target="_blank" rel="noopener noreferrer">Security</a>
            </div>
            <div className="footer-col">
              <h4>Legal</h4>
              <a href={`${GITHUB_REPO}/blob/main/LICENSE`} target="_blank" rel="noopener noreferrer">MIT License</a>
              <a href={`${GITHUB_REPO}/blob/main/CODE_OF_CONDUCT.md`} target="_blank" rel="noopener noreferrer">Code of Conduct</a>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; {new Date().getFullYear()} NGXSMK. Made with frustration, caffeine, and determination. MIT licensed.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
