"""
Settings Dialog Module
Advanced settings dialog with comprehensive configuration options
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from typing import Dict, Any, Optional

# Standard fonts
FONT_FAMILY_BOLD = 'Segoe UI Semibold'
FONT_FAMILY_REGULAR = 'Segoe UI'

class SettingsDialog:
    """Advanced settings dialog for NGXSMK GameNet Optimizer"""
    
    def __init__(self, parent, config_manager, colors=None, fonts=None):
        self.parent = parent
        self.config_manager = config_manager
        self.colors = colors or {
            'bg_primary': '#0a0a0a',
            'bg_secondary': '#121212',
            'bg_tertiary': '#1a1a1a',
            'accent': '#00ff88',
            'accent_hover': '#00cc6e',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'text_muted': '#666666',
            'success': '#00ff88',
            'error': '#ff4d4d'
        }
        self.fonts = fonts or {
            'h1': (FONT_FAMILY_BOLD, 22),
            'h2': (FONT_FAMILY_BOLD, 18),
            'body': (FONT_FAMILY_REGULAR, 11),
            'body_bold': (FONT_FAMILY_BOLD, 11),
            'small': (FONT_FAMILY_REGULAR, 9)
        }
        self.settings = {}
        self.dialog = None
        
    def show_settings(self):
        """Show the settings dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Advanced Settings")
        self.dialog.geometry("900x750")
        self.dialog.configure(bg=self.colors['bg_primary'])
        self.dialog.resizable(True, True)
        
        # Center the dialog
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Load current settings
        self.settings = self.config_manager.load_settings()
        
        # Create notebook for different setting categories
        self.create_settings_notebook()
        
        # Create buttons
        self.create_buttons()
        
        # Center the dialog
        self.center_dialog()
    
    def _initialize_variables(self):
        """Initialize all tkinter variables"""
        # General settings
        self.auto_start = tk.BooleanVar(value=self.settings.get('general', {}).get('auto_start', False))
        self.start_minimized = tk.BooleanVar(value=self.settings.get('general', {}).get('start_minimized', False))
        self.auto_optimize = tk.BooleanVar(value=self.settings.get('general', {}).get('auto_optimize', False))
        self.theme = tk.StringVar(value=self.settings.get('general', {}).get('theme', 'dark'))
        self.language = tk.StringVar(value=self.settings.get('general', {}).get('language', 'en'))
        
        # Optimization settings
        self.cpu_aggressive = tk.BooleanVar(value=self.settings.get('optimization', {}).get('cpu_aggressive', False))
        self.cpu_priority = tk.StringVar(value=self.settings.get('optimization', {}).get('cpu_priority', 'high'))
        self.mem_aggressive = tk.BooleanVar(value=self.settings.get('optimization', {}).get('mem_aggressive', False))
        self.mem_threshold = tk.IntVar(value=self.settings.get('optimization', {}).get('mem_threshold', 80))
        
        # Network settings
        self.custom_dns = tk.BooleanVar(value=self.settings.get('network', {}).get('custom_dns', False))
        self.dns_primary = tk.StringVar(value=self.settings.get('network', {}).get('dns_primary', '8.8.8.8'))
        self.dns_secondary = tk.StringVar(value=self.settings.get('network', {}).get('dns_secondary', '1.1.1.1'))
        self.tcp_optimization = tk.BooleanVar(value=self.settings.get('network', {}).get('tcp_optimization', True))
        self.udp_optimization = tk.BooleanVar(value=self.settings.get('network', {}).get('udp_optimization', True))
        self.qos_enabled = tk.BooleanVar(value=self.settings.get('network', {}).get('qos_enabled', False))
        
        # Gaming settings
        self.auto_detect_games = tk.BooleanVar(value=self.settings.get('gaming', {}).get('auto_detect_games', True))
        self.game_mode = tk.BooleanVar(value=self.settings.get('gaming', {}).get('game_mode', True))
        self.anti_cheat_optimization = tk.BooleanVar(value=self.settings.get('gaming', {}).get('anti_cheat_optimization', True))
        self.gaming_priority = tk.StringVar(value=self.settings.get('gaming', {}).get('gaming_priority', 'high'))
        self.fps_boost = tk.BooleanVar(value=self.settings.get('gaming', {}).get('fps_boost', True))
        self.latency_optimization = tk.BooleanVar(value=self.settings.get('gaming', {}).get('latency_optimization', True))
        
        # Monitoring settings
        self.monitoring_enabled = tk.BooleanVar(value=self.settings.get('monitoring', {}).get('monitoring_enabled', True))
        self.monitoring_interval = tk.IntVar(value=self.settings.get('monitoring', {}).get('monitoring_interval', 5))
        self.alerts_enabled = tk.BooleanVar(value=self.settings.get('monitoring', {}).get('alerts_enabled', True))
        self.cpu_threshold = tk.IntVar(value=self.settings.get('monitoring', {}).get('cpu_threshold', 80))
        self.memory_threshold = tk.IntVar(value=self.settings.get('monitoring', {}).get('memory_threshold', 80))
        self.temperature_threshold = tk.IntVar(value=self.settings.get('monitoring', {}).get('temperature_threshold', 80))
        
        # Advanced settings
        self.ai_enabled = tk.BooleanVar(value=self.settings.get('advanced', {}).get('ai_enabled', False))
        self.predictive_optimization = tk.BooleanVar(value=self.settings.get('advanced', {}).get('predictive_optimization', False))
        self.adaptive_learning = tk.BooleanVar(value=self.settings.get('advanced', {}).get('adaptive_learning', False))
        self.debug_mode = tk.BooleanVar(value=self.settings.get('advanced', {}).get('debug_mode', False))
        self.verbose_logging = tk.BooleanVar(value=self.settings.get('advanced', {}).get('verbose_logging', False))
        self.performance_logging = tk.BooleanVar(value=self.settings.get('advanced', {}).get('performance_logging', False))
        
    def create_settings_notebook(self):
        """Create settings notebook with premium styling"""
        # Header
        header = tk.Frame(self.dialog, bg=self.colors['bg_secondary'], pady=20)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="⚙️ ADVANCED CONFIGURATION", font=self.fonts['h2'],
                 fg=self.colors['text_primary'], bg=self.colors['bg_secondary']).pack(padx=25, anchor=tk.W)
        
        # Main content area
        main_content = tk.Frame(self.dialog, bg=self.colors['bg_primary'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        self._initialize_variables()
        
        # Modern notebook style
        style = ttk.Style()
        style.configure('Settings.TNotebook', background=self.colors['bg_primary'], borderwidth=0)
        style.configure('Settings.TNotebook.Tab', 
                       background=self.colors['bg_tertiary'], 
                       foreground=self.colors['text_secondary'],
                       padding=[15, 8], font=self.fonts['body_bold'])
        style.map('Settings.TNotebook.Tab',
                 background=[('selected', self.colors['accent'])],
                 foreground=[('selected', self.colors['bg_primary'])])
        
        self.notebook = ttk.Notebook(main_content, style='Settings.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create different setting tabs
        self.create_general_settings()
        self.create_optimization_settings()
        self.create_network_settings()
        self.create_gaming_settings()
        self.create_monitoring_settings()
        self.create_advanced_settings()
    
    def create_general_settings(self):
        """Create general settings tab with modern styling"""
        general_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'], padx=20, pady=20)
        self.notebook.add(general_frame, text="🔧 General")
        
        def create_group(parent, title):
            group = tk.LabelFrame(parent, text=f"  {title}  ", font=self.fonts['body_bold'],
                                 fg=self.colors['accent'], bg=self.colors['bg_primary'],
                                 relief=tk.FLAT, bd=0)
            group.pack(fill=tk.X, pady=(0, 20))
            inner = tk.Frame(group, bg=self.colors['bg_secondary'], padx=15, pady=15)
            inner.pack(fill=tk.X, pady=5)
            return inner

        # Auto-Start Group
        auto_inner = create_group(general_frame, "STARTUP BEHAVIOR")
        
        for text, var in [("Start with Windows", self.auto_start),
                         ("Start minimized in tray", self.start_minimized),
                         ("Auto-optimize on application startup", self.auto_optimize)]:
            tk.Checkbutton(auto_inner, text=text, variable=var,
                          font=self.fonts['body'], fg=self.colors['text_primary'],
                          bg=self.colors['bg_secondary'], selectcolor=self.colors['bg_tertiary'],
                          activebackground=self.colors['bg_secondary'], activeforeground=self.colors['accent'],
                          relief=tk.FLAT, bd=0).pack(anchor=tk.W, pady=5)

        # UI Group
        ui_inner = create_group(general_frame, "APPEARANCE & LANGUAGE")
        
        # Theme
        theme_row = tk.Frame(ui_inner, bg=self.colors['bg_secondary'])
        theme_row.pack(fill=tk.X, pady=5)
        tk.Label(theme_row, text="Active Theme:", font=self.fonts['body_bold'],
                fg=self.colors['text_secondary'], bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        for t in ["Dark", "Light", "Gaming"]:
            tk.Radiobutton(theme_row, text=t, variable=self.theme, value=t.lower(),
                          font=self.fonts['body'], fg=self.colors['text_primary'],
                          bg=self.colors['bg_secondary'], selectcolor=self.colors['bg_tertiary'],
                          activebackground=self.colors['bg_secondary'], activeforeground=self.colors['accent'],
                          relief=tk.FLAT, bd=0).pack(side=tk.LEFT, padx=15)

        # Language
        lang_row = tk.Frame(ui_inner, bg=self.colors['bg_secondary'], pady=10)
        lang_row.pack(fill=tk.X)
        tk.Label(lang_row, text="System Language:", font=self.fonts['body_bold'],
                fg=self.colors['text_secondary'], bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        lang_combo = ttk.Combobox(lang_row, textvariable=self.language, 
                                 values=['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko'],
                                 state='readonly', width=12)
        lang_combo.pack(side=tk.LEFT, padx=15)
    
    def create_optimization_settings(self):
        """Create optimization settings tab with modern styling"""
        opt_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'], padx=20, pady=20)
        self.notebook.add(opt_frame, text="⚡ Optimization")
        
        def create_group(parent, title):
            group = tk.LabelFrame(parent, text=f"  {title}  ", font=self.fonts['body_bold'],
                                 fg=self.colors['accent'], bg=self.colors['bg_primary'],
                                 relief=tk.FLAT, bd=0)
            group.pack(fill=tk.X, pady=(0, 20))
            inner = tk.Frame(group, bg=self.colors['bg_secondary'], padx=15, pady=15)
            inner.pack(fill=tk.X, pady=5)
            return inner

        # CPU Group
        cpu_inner = create_group(opt_frame, "CPU ENGINE")
        tk.Checkbutton(cpu_inner, text="Enable aggressive CPU resource allocation", 
                      variable=self.cpu_aggressive, font=self.fonts['body'], 
                      fg=self.colors['text_primary'], bg=self.colors['bg_secondary'],
                      selectcolor=self.colors['bg_tertiary'], relief=tk.FLAT).pack(anchor=tk.W, pady=5)
        
        priority_row = tk.Frame(cpu_inner, bg=self.colors['bg_secondary'], pady=10)
        priority_row.pack(fill=tk.X)
        tk.Label(priority_row, text="Process Priority:", font=self.fonts['body_bold'],
                fg=self.colors['text_secondary'], bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        for p in ["High", "Normal", "Low"]:
            tk.Radiobutton(priority_row, text=p, variable=self.cpu_priority, value=p.lower(),
                          font=self.fonts['body'], fg=self.colors['text_primary'],
                          bg=self.colors['bg_secondary'], selectcolor=self.colors['bg_tertiary']).pack(side=tk.LEFT, padx=15)

        # Memory Group
        mem_inner = create_group(opt_frame, "MEMORY ARCHITECTURE")
        tk.Checkbutton(mem_inner, text="Enable real-time aggressive memory purging", 
                      variable=self.mem_aggressive, font=self.fonts['body'], 
                      fg=self.colors['text_primary'], bg=self.colors['bg_secondary'],
                      selectcolor=self.colors['bg_tertiary']).pack(anchor=tk.W, pady=5)
        
        thresh_row = tk.Frame(mem_inner, bg=self.colors['bg_secondary'], pady=10)
        thresh_row.pack(fill=tk.X)
        tk.Label(thresh_row, text="Cleanup Threshold (%):", font=self.fonts['body_bold'],
                fg=self.colors['text_secondary'], bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        scale = tk.Scale(thresh_row, from_=50, to=95, orient=tk.HORIZONTAL,
                        variable=self.mem_threshold, bg=self.colors['bg_secondary'], 
                        fg=self.colors['text_primary'], highlightthickness=0, 
                        troughcolor=self.colors['bg_tertiary'], activebackground=self.colors['accent'])
        scale.pack(side=tk.LEFT, padx=15, fill=tk.X, expand=True)
    
    def create_network_settings(self):
        """Create network settings tab with modern styling"""
        net_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'], padx=20, pady=20)
        self.notebook.add(net_frame, text="🌐 Network")
        
        def create_group(parent, title):
            group = tk.LabelFrame(parent, text=f"  {title}  ", font=self.fonts['body_bold'],
                                 fg=self.colors['accent'], bg=self.colors['bg_primary'],
                                 relief=tk.FLAT, bd=0)
            group.pack(fill=tk.X, pady=(0, 20))
            inner = tk.Frame(group, bg=self.colors['bg_secondary'], padx=15, pady=15)
            inner.pack(fill=tk.X, pady=5)
            return inner

        # DNS Group
        dns_inner = create_group(net_frame, "DNS ARCHITECTURE")
        tk.Checkbutton(dns_inner, text="Use custom low-latency DNS servers", 
                      variable=self.custom_dns, font=self.fonts['body'], 
                      fg=self.colors['text_primary'], bg=self.colors['bg_secondary'],
                      selectcolor=self.colors['bg_tertiary']).pack(anchor=tk.W, pady=5)
        
        entry_row = tk.Frame(dns_inner, bg=self.colors['bg_secondary'], pady=10)
        entry_row.pack(fill=tk.X)
        
        for label, var in [("Primary:", self.dns_primary), ("Secondary:", self.dns_secondary)]:
            tk.Label(entry_row, text=label, font=self.fonts['body_bold'],
                    fg=self.colors['text_secondary'], bg=self.colors['bg_secondary']).pack(side=tk.LEFT, padx=(10, 5))
            tk.Entry(entry_row, textvariable=var, font=self.fonts['body'],
                    bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'], 
                    insertbackground=self.colors['accent'], relief=tk.FLAT, width=15).pack(side=tk.LEFT, padx=5)

        # Optimization Group
        net_inner = create_group(net_frame, "PROTOCOL OPTIMIZATION")
        for text, var in [("Apply advanced TCP stack optimizations", self.tcp_optimization),
                         ("Apply advanced UDP/LAG reduction", self.udp_optimization),
                         ("Enable hardware-level Quality of Service (QoS)", self.qos_enabled)]:
            tk.Checkbutton(net_inner, text=text, variable=var,
                          font=self.fonts['body'], fg=self.colors['text_primary'],
                          bg=self.colors['bg_secondary'], selectcolor=self.colors['bg_tertiary']).pack(anchor=tk.W, pady=5)
    
    def create_gaming_settings(self):
        """Create gaming settings tab with modern styling"""
        gaming_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'], padx=20, pady=20)
        self.notebook.add(gaming_frame, text="🎮 Gaming")
        
        def create_group(parent, title):
            group = tk.LabelFrame(parent, text=f"  {title}  ", font=self.fonts['body_bold'],
                                 fg=self.colors['accent'], bg=self.colors['bg_primary'], relief=tk.FLAT, bd=0)
            group.pack(fill=tk.X, pady=(0, 20))
            inner = tk.Frame(group, bg=self.colors['bg_secondary'], padx=15, pady=15)
            inner.pack(fill=tk.X, pady=5)
            return inner

        # Detection Group
        det_inner = create_group(gaming_frame, "SESSION DETECTION")
        tk.Checkbutton(det_inner, text="Intelligent automatic game session detection", 
                      variable=self.auto_detect_games, font=self.fonts['body'], 
                      fg=self.colors['text_primary'], bg=self.colors['bg_secondary'],
                      selectcolor=self.colors['bg_tertiary']).pack(anchor=tk.W)

        # Optimization Group
        opt_inner = create_group(gaming_frame, "PERFORMANCE ENGINE")
        for text, var in [("Enable Windows Game Mode integration", self.game_mode),
                         ("Apply low-level anti-cheat compatibility patches", self.anti_cheat_optimization),
                         ("Execute high-priority FPS boost sub-processes", self.fps_boost),
                         ("Apply kernel-level latency optimizations", self.latency_optimization)]:
            tk.Checkbutton(opt_inner, text=text, variable=var,
                          font=self.fonts['body'], fg=self.colors['text_primary'],
                          bg=self.colors['bg_secondary'], selectcolor=self.colors['bg_tertiary']).pack(anchor=tk.W, pady=5)
        
        priority_row = tk.Frame(opt_inner, bg=self.colors['bg_secondary'], pady=10)
        priority_row.pack(fill=tk.X)
        tk.Label(priority_row, text="Thread Priority:", font=self.fonts['body_bold'],
                fg=self.colors['text_secondary'], bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        for p in ["High", "Normal", "Low"]:
            tk.Radiobutton(priority_row, text=p, variable=self.gaming_priority, value=p.lower(),
                          font=self.fonts['body'], fg=self.colors['text_primary'],
                          bg=self.colors['bg_secondary'], selectcolor=self.colors['bg_tertiary']).pack(side=tk.LEFT, padx=15)

    def create_monitoring_settings(self):
        """Create monitoring settings tab with modern styling"""
        monitor_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'], padx=20, pady=20)
        self.notebook.add(monitor_frame, text="📊 Monitoring")
        
        def create_group(parent, title):
            group = tk.LabelFrame(parent, text=f"  {title}  ", font=self.fonts['body_bold'],
                                 fg=self.colors['accent'], bg=self.colors['bg_primary'], relief=tk.FLAT, bd=0)
            group.pack(fill=tk.X, pady=(0, 20))
            inner = tk.Frame(group, bg=self.colors['bg_secondary'], padx=15, pady=15)
            inner.pack(fill=tk.X, pady=5)
            return inner

        # Global Setup
        glob_inner = create_group(monitor_frame, "TELEMETRY ENGINE")
        tk.Checkbutton(glob_inner, text="Enable real-time performance monitoring", 
                      variable=self.monitoring_enabled, font=self.fonts['body'], 
                      fg=self.colors['text_primary'], bg=self.colors['bg_secondary'],
                      selectcolor=self.colors['bg_tertiary']).pack(anchor=tk.W)
        tk.Checkbutton(glob_inner, text="Enable critical threshold system alerts", 
                      variable=self.alerts_enabled, font=self.fonts['body'], 
                      fg=self.colors['text_primary'], bg=self.colors['bg_secondary'],
                      selectcolor=self.colors['bg_tertiary']).pack(anchor=tk.W)
        
        # Interval
        int_row = tk.Frame(glob_inner, bg=self.colors['bg_secondary'], pady=10)
        int_row.pack(fill=tk.X)
        tk.Label(int_row, text="Refresh Interval (s):", font=self.fonts['body_bold'],
                fg=self.colors['text_secondary'], bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        tk.Scale(int_row, from_=1, to=60, orient=tk.HORIZONTAL, variable=self.monitoring_interval,
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'], highlightthickness=0,
                troughcolor=self.colors['bg_tertiary']).pack(side=tk.LEFT, padx=15, fill=tk.X, expand=True)

        # Thresholds
        thresh_inner = create_group(monitor_frame, "CRITICAL THRESHOLDS")
        def add_scale(label, var, f, t):
            row = tk.Frame(thresh_inner, bg=self.colors['bg_secondary'], pady=5)
            row.pack(fill=tk.X)
            tk.Label(row, text=label, font=self.fonts['body'], width=20, anchor=tk.W,
                    fg=self.colors['text_secondary'], bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
            tk.Scale(row, from_=f, to=t, orient=tk.HORIZONTAL, variable=var,
                    bg=self.colors['bg_secondary'], fg=self.colors['text_primary'], highlightthickness=0,
                    troughcolor=self.colors['bg_tertiary']).pack(side=tk.LEFT, padx=15, fill=tk.X, expand=True)
            
        add_scale("CPU Usage (%)", self.cpu_threshold, 50, 100)
        add_scale("RAM Usage (%)", self.memory_threshold, 50, 100)
        add_scale("Core Temp (°C)", self.temperature_threshold, 60, 100)

    def create_advanced_settings(self):
        """Create advanced settings tab with modern styling"""
        advanced_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'], padx=20, pady=20)
        self.notebook.add(advanced_frame, text="🔬 Advanced")
        
        def create_group(parent, title):
            group = tk.LabelFrame(parent, text=f"  {title}  ", font=self.fonts['body_bold'],
                                 fg=self.colors['accent'], bg=self.colors['bg_primary'], relief=tk.FLAT, bd=0)
            group.pack(fill=tk.X, pady=(0, 20))
            inner = tk.Frame(group, bg=self.colors['bg_secondary'], padx=15, pady=15)
            inner.pack(fill=tk.X, pady=5)
            return inner

        # AI Group
        ai_inner = create_group(advanced_frame, "NEURAL OPTIMIZER")
        for text, var in [("Enable full AI-driven system optimization", self.ai_enabled),
                         ("Enable predictive workload forecasting", self.predictive_optimization),
                         ("Enable adaptive learning from system behavior", self.adaptive_learning)]:
            tk.Checkbutton(ai_inner, text=text, variable=var,
                          font=self.fonts['body'], fg=self.colors['text_primary'],
                          bg=self.colors['bg_secondary'], selectcolor=self.colors['bg_tertiary']).pack(anchor=tk.W, pady=5)

        # Logging
        log_inner = create_group(advanced_frame, "DIAGNOSTICS & LOGGING")
        for text, var in [("Enable system-wide debug mode", self.debug_mode),
                         ("Enable verbose optimization logging", self.verbose_logging),
                         ("Enable hardware performance trace", self.performance_logging)]:
            tk.Checkbutton(log_inner, text=text, variable=var,
                          font=self.fonts['body'], fg=self.colors['text_primary'],
                          bg=self.colors['bg_secondary'], selectcolor=self.colors['bg_tertiary']).pack(anchor=tk.W, pady=5)
    
    def create_buttons(self):
        """Create dialog buttons with premium styling"""
        button_frame = tk.Frame(self.dialog, bg=self.colors['bg_secondary'], pady=20, padx=25)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        def create_btn(text, cmd, bg, fg):
            btn = tk.Button(button_frame, text=text, command=cmd,
                           font=self.fonts['body_bold'], bg=bg, fg=fg,
                           relief=tk.FLAT, bd=0, padx=25, pady=10, cursor='hand2')
            btn.pack(side=tk.RIGHT, padx=5)
            return btn
        
        create_btn("SAVE CHANGES", self.save_and_close, self.colors['accent'], self.colors['bg_primary'])
        create_btn("CANCEL", self.cancel_settings, self.colors['bg_tertiary'], self.colors['text_primary'])
        create_btn("APPLY", self.apply_settings, self.colors['bg_tertiary'], self.colors['accent'])
    
    def center_dialog(self):
        """Center the dialog on screen"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def apply_settings(self):
        """Apply settings without closing dialog"""
        try:
            # Collect all settings
            settings = {
                'general': {
                    'auto_start': self.auto_start.get(),
                    'start_minimized': self.start_minimized.get(),
                    'auto_optimize': self.auto_optimize.get(),
                    'theme': self.theme.get(),
                    'language': self.language.get()
                },
                'optimization': {
                    'cpu_aggressive': self.cpu_aggressive.get(),
                    'cpu_priority': self.cpu_priority.get(),
                    'mem_aggressive': self.mem_aggressive.get(),
                    'mem_threshold': self.mem_threshold.get()
                },
                'network': {
                    'custom_dns': self.custom_dns.get(),
                    'dns_primary': self.dns_primary.get(),
                    'dns_secondary': self.dns_secondary.get(),
                    'tcp_optimization': self.tcp_optimization.get(),
                    'udp_optimization': self.udp_optimization.get(),
                    'qos_enabled': self.qos_enabled.get()
                },
                'gaming': {
                    'auto_detect_games': self.auto_detect_games.get(),
                    'game_mode': self.game_mode.get(),
                    'anti_cheat_optimization': self.anti_cheat_optimization.get(),
                    'gaming_priority': self.gaming_priority.get(),
                    'fps_boost': self.fps_boost.get(),
                    'latency_optimization': self.latency_optimization.get()
                },
                'monitoring': {
                    'monitoring_enabled': self.monitoring_enabled.get(),
                    'monitoring_interval': self.monitoring_interval.get(),
                    'alerts_enabled': self.alerts_enabled.get(),
                    'cpu_threshold': self.cpu_threshold.get(),
                    'memory_threshold': self.memory_threshold.get(),
                    'temperature_threshold': self.temperature_threshold.get()
                },
                'advanced': {
                    'ai_enabled': self.ai_enabled.get(),
                    'predictive_optimization': self.predictive_optimization.get(),
                    'adaptive_learning': self.adaptive_learning.get(),
                    'debug_mode': self.debug_mode.get(),
                    'verbose_logging': self.verbose_logging.get(),
                    'performance_logging': self.performance_logging.get()
                }
            }
            
            # Save settings
            self.config_manager.save_settings(settings)
            
            messagebox.showinfo("Settings", "Settings applied successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply settings: {str(e)}")
    
    def cancel_settings(self):
        """Cancel settings changes"""
        self.dialog.destroy()
    
    def save_and_close(self):
        """Save settings and close dialog"""
        try:
            # Apply settings first
            self.apply_settings()
            # Close dialog
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
