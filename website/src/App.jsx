import React from 'react';

const features = [
  {
    icon: '⚡',
    title: 'FPS Boost',
    desc: 'Intelligently prioritizes game processes, adjusts CPU affinity, and optimizes system services for maximum frame rates.',
  },
  {
    icon: '🌐',
    title: 'Ping Reducer',
    desc: 'Optimizes network stack, DNS settings, and routing tables to minimize latency in online games.',
  },
  {
    icon: '🧠',
    title: 'AI-Powered Tuning',
    desc: 'Neural engine analyzes your system patterns and predicts bottlenecks before they impact performance.',
  },
  {
    icon: '💾',
    title: 'RAM Cleaner',
    desc: 'Frees up memory by intelligently suspending background processes without affecting stability.',
  },
  {
    icon: '🎮',
    title: 'Game Detection',
    desc: 'Auto-detects running games and applies optimized profiles for Valorant, LoL, CS2, Fortnite, and more.',
  },
  {
    icon: '📊',
    title: 'Real-Time Monitor',
    desc: 'Live CPU, RAM, and network usage charts with historical data and trend analysis.',
  },
  {
    icon: '🔀',
    title: 'Traffic Shaper',
    desc: 'QoS-based traffic management prioritizes gaming traffic over background downloads and streaming.',
  },
  {
    icon: '🖥️',
    title: 'Multi-Internet',
    desc: 'Manage multiple network connections simultaneously with automatic failover and load balancing.',
  },
  {
    icon: '📡',
    title: 'LoL Server Test',
    desc: 'Test latency to all League of Legends servers and get the optimal server recommendation.',
  },
];

const stats = [
  { value: '15-30%', label: 'FPS Improvement' },
  { value: '20-40%', label: 'Ping Reduction' },
  { value: '50%+', label: 'More Free RAM' },
  { value: 'Free', label: 'Open Source' },
];

const Footer = () => (
  <footer className="footer">
    <div className="container">
      <div className="footer-grid">
        <div className="footer-col">
          <h4>NGXSMK GameNet Optimizer</h4>
          <p>Open-source Windows gaming optimizer. Built for gamers, by gamers.</p>
        </div>
        <div className="footer-col">
          <h4>Links</h4>
          <a href="https://github.com/NGXSMK/ngxsmk-gamenet-optimizer">GitHub Repository</a>
          <a href="https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/releases">Releases</a>
          <a href="https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/issues">Issues</a>
        </div>
        <div className="footer-col">
          <h4>Tech Stack</h4>
          <span>Python / Flask</span>
          <span>React / Electron</span>
          <span>psutil / PyInstaller</span>
        </div>
      </div>
      <div className="footer-bottom">
        <p>&copy; {new Date().getFullYear()} NGXSMK. MIT License.</p>
      </div>
    </div>
  </footer>
);

const App = () => {
  const [menuOpen, setMenuOpen] = React.useState(false);

  return (
    <div className="page">
      <header className="header">
        <div className="container header-inner">
          <div className="logo">
            <div className="logo-icon">N</div>
            <span className="logo-text">NGXSMK <small>GameNet Optimizer</small></span>
          </div>
          <nav className={`nav ${menuOpen ? 'open' : ''}`}>
            <a href="#features" onClick={() => setMenuOpen(false)}>Features</a>
            <a href="#download" onClick={() => setMenuOpen(false)}>Download</a>
            <a href="https://github.com/NGXSMK/ngxsmk-gamenet-optimizer" target="_blank" rel="noopener noreferrer">GitHub</a>
          </nav>
          <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)} aria-label="Menu">
            <span></span><span></span><span></span>
          </button>
        </div>
      </header>

      <main>
        <section className="hero">
          <div className="container hero-inner">
            <div className="hero-badge">Open Source &middot; Windows &middot; Free</div>
            <h1>Optimize Your PC for <span className="highlight">Maximum Gaming Performance</span></h1>
            <p className="hero-subtitle">
              Boost FPS, reduce ping, clean RAM, and tune your system automatically with AI-powered optimization. 
              Built for Windows 10/11 &mdash; 32-bit and 64-bit.
            </p>
            <div className="hero-actions">
              <a href="#download" className="btn btn-primary">Download Now</a>
              <a href="https://github.com/NGXSMK/ngxsmk-gamenet-optimizer" target="_blank" rel="noopener noreferrer" className="btn btn-secondary">View on GitHub</a>
            </div>
          </div>
        </section>

        <section className="stats-bar">
          <div className="container stats-grid">
            {stats.map((s, i) => (
              <div key={i} className="stat-item">
                <div className="stat-value">{s.value}</div>
                <div className="stat-label">{s.label}</div>
              </div>
            ))}
          </div>
        </section>

        <section id="features" className="features">
          <div className="container">
            <h2 className="section-title">Everything You Need</h2>
            <p className="section-subtitle">
              A comprehensive suite of optimization tools in one lightweight application.
            </p>
            <div className="features-grid">
              {features.map((f, i) => (
                <article key={i} className="feature-card">
                  <div className="feature-icon">{f.icon}</div>
                  <h3>{f.title}</h3>
                  <p>{f.desc}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section id="download" className="download">
          <div className="container download-inner">
            <h2 className="section-title">Get Started</h2>
            <p className="section-subtitle">
              Download the latest release and start optimizing your gaming experience today.
            </p>
            <div className="download-cards">
              <div className="download-card">
                <div className="download-icon">⬇️</div>
                <h3>Portable EXE (64-bit)</h3>
                <p>Standalone executable. No installation required. Recommended for most users.</p>
                <a href="https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/releases/latest" className="btn btn-primary" target="_blank" rel="noopener noreferrer">
                  Download 64-bit
                </a>
              </div>
              <div className="download-card">
                <div className="download-icon">⬇️</div>
                <h3>Portable EXE (32-bit)</h3>
                <p>For older 32-bit Windows systems. Same features, optimized for x86 architecture.</p>
                <a href="https://github.com/NGXSMK/ngxsmk-gamenet-optimizer/releases/latest" className="btn btn-primary" target="_blank" rel="noopener noreferrer">
                  Download 32-bit
                </a>
              </div>
              <div className="download-card">
                <div className="download-icon">🐍</div>
                <h3>Run from Source</h3>
                <p>Clone the repo and run with Python 3.8+. Full control, contributions welcome.</p>
                <a href="https://github.com/NGXSMK/ngxsmk-gamenet-optimizer" className="btn btn-secondary" target="_blank" rel="noopener noreferrer">
                  View Source
                </a>
              </div>
            </div>
          </div>
        </section>

        <section className="faq">
          <div className="container">
            <h2 className="section-title">Frequently Asked Questions</h2>
            <div className="faq-list">
              <details>
                <summary>Is it safe to use?</summary>
                <p>Yes. The application is fully open-source under the MIT license. It does not collect any personal data or modify system files in an irreversible way. All optimizations can be reset by restarting your PC.</p>
              </details>
              <details>
                <summary>Does it work with anti-cheat systems?</summary>
                <p>Yes. NGXSMK GameNet Optimizer uses only standard Windows API calls and does not modify game memory or executables. It is compatible with Vanguard, EAC, VAC, and other anti-cheat systems.</p>
              </details>
              <details>
                <summary>Will it work on my low-end PC?</summary>
                <p>Absolutely. The application includes a Low Power Mode that reduces CPU overhead and polling frequency, making it suitable for older hardware. It runs on both 32-bit and 64-bit Windows 10/11.</p>
              </details>
              <details>
                <summary>How do I build from source?</summary>
                <p>Clone the repo, install Python 3.8+ and Node.js 18+, then run <code>pip install -r requirements.txt</code> followed by <code>cd web-ui && npm install && npm run build</code>. Use the build scripts in the <code>scripts/</code> directory to create a standalone EXE.</p>
              </details>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default App;
