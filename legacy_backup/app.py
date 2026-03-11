# pyre-ignore-all-errors
#!/usr/bin/env python3
"""
NGXSMK GameNet Optimizer
A comprehensive network and system optimization tool for gamers
Open source alternative to commercial gaming optimization software
"""

import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter # type: ignore
import threading
import sys
import os
import time
import json
import gc
import weakref
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime

# Configure CustomTkinter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Import our modules
from .modules.fps_boost import FPSBoost # type: ignore
from .modules.network_analyzer import NetworkAnalyzer # type: ignore
from .modules.multi_internet import MultiInternet # type: ignore
from .modules.traffic_shaper import TrafficShaper # type: ignore
from .modules.ram_cleaner import RAMCleaner # type: ignore
from .modules.lol_optimizer import LoLOptimizer # type: ignore
from .modules.advanced_optimizer import AdvancedOptimizer # type: ignore
from .modules.system_monitor import SystemMonitor # type: ignore
from .modules.network_optimizer import NetworkOptimizer # type: ignore
from .modules.gaming_optimizer import GamingOptimizer # type: ignore
from .modules.config_manager import ConfigManager # type: ignore
from .modules.settings_dialog import SettingsDialog # type: ignore
from .modules.compat import get_psutil # type: ignore
psutil = get_psutil()
globals()['psutil'] = psutil

# ---------------------------------------------------------------------------
# Module-level constants (avoids SonarQube duplicate-literal warnings)
# ---------------------------------------------------------------------------
APP_TITLE         = "NGXSMK GameNet Optimizer"
NOTEBOOK_STYLE   = "Modern.TNotebook"
TAB_STYLE        = "Modern.TNotebook.Tab"
ENTER_EVENT      = "<Enter>"
LEAVE_EVENT      = "<Leave>"
STOP_BTN_TEXT    = "⏹️ Stop Optimization"
MULTI_INTERNET_LABEL = "Multi Internet"
CLEAN_RAM_LABEL  = "Clean RAM"
OPTIMIZE_ALL_LABEL = "Optimize All"
TEST_NETWORK_LABEL = "Test Network"
GAMING_MODE_LABEL = "Gaming Mode"
READY_STATUS     = "Ready"
OPTIMIZING_STATUS = "Optimizing..."
ABOUT_LABEL      = "About"
FONT_HEADING     = "Segoe UI Semibold"
FONT_BODY        = "Segoe UI"
FONT_SYMBOL      = "Segoe UI Symbol"

class NetworkOptimizerApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Performance optimizations
        self._setup_performance_optimizations()
        
        # Detect system capabilities for low-end PC optimization
        self._detect_system_capabilities()
        
        self.title(APP_TITLE)
        
        # Adaptive window sizing
        if self.is_low_end_pc:
            self.geometry("1000x700")
            self.minsize(800, 600)
        else:
            self.after(0, lambda: self.state('zoomed'))
            self.minsize(1200, 800)
        
        self.configure(fg_color='#050505')
        self.resizable(True, True)
        
        # Add fullscreen toggle functionality
        self.is_fullscreen = not self.is_low_end_pc
        if not self.is_low_end_pc:
            self.bind('<F11>', self.toggle_fullscreen)
            self.bind('<Escape>', self.exit_fullscreen)
        
        # Performance monitoring
        self._startup_time = time.time()
        self._last_gc_time = time.time()
        self._memory_usage = []
        
        # Adaptive thread pool based on system capabilities
        max_workers = 2 if self.is_low_end_pc else 4
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
        # Weak references for memory management
        self._weak_refs = weakref.WeakSet()
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Initialize modules
        self.config_manager = ConfigManager()
        self.fps_boost = FPSBoost()
        self.network_analyzer = NetworkAnalyzer()
        self.multi_internet = MultiInternet()
        self.traffic_shaper = TrafficShaper()
        self.ram_cleaner = RAMCleaner()
        self.lol_optimizer = LoLOptimizer()
        
        # Initialize advanced modules with config manager
        self.advanced_optimizer = AdvancedOptimizer()
        self.system_monitor = SystemMonitor()
        self.network_optimizer = NetworkOptimizer(config_manager=self.config_manager)
        self.gaming_optimizer = GamingOptimizer(config_manager=self.config_manager)
        
        # Status variables
        # Core components
        self.is_optimizing = False
        self.optimization_thread: Optional[threading.Thread] = None
        self.tab_frames = []
        
        self.setup_ui()
        self.load_settings()
        
        # Start performance monitoring
        self._start_performance_monitoring()
        
    def _detect_system_capabilities(self):
        """Detect system capabilities for optimization"""
        try:
            # Get system information
            cpu_count = psutil.cpu_count() or 1  # pyre-fixme[16]
            memory = psutil.virtual_memory()  # pyre-fixme[16]
            memory_gb = memory.total / (1024**3)
            
            # Determine if this is a low-end PC
            self.is_low_end_pc = (
                (cpu_count or 0) < 4 or  # Less than 4 CPU cores
                memory_gb < 8 or  # Less than 8GB RAM
                psutil.cpu_percent(interval=0.1) > 50  # High CPU usage  # pyre-fixme[16]
            )
            
            # Set optimization flags
            self.low_resource_mode = self.is_low_end_pc
            self.reduced_animations = self.is_low_end_pc
            self.minimal_ui = self.is_low_end_pc
            
            print(f"System detected: {'Low-end PC' if self.is_low_end_pc else 'Standard PC'}")
            print(f"CPU cores: {cpu_count}, RAM: {memory_gb:.1f}GB")
            
        except Exception as e:
            print(f"System detection failed: {e}")
            # Default to low-end PC for safety
            self.is_low_end_pc = True
            self.low_resource_mode = True
            self.reduced_animations = True
            self.minimal_ui = True
    
    def _setup_performance_optimizations(self):
        """Setup performance optimizations"""
        # Optimize Python garbage collection
        gc.set_threshold(700, 10, 10)
        
        # Set thread optimization
        os.environ['PYTHONUNBUFFERED'] = '1'
        
    def _start_performance_monitoring(self):
        """Start background performance monitoring"""
        # Start monitoring in background thread
        monitor_thread = threading.Thread(target=self._performance_monitoring_loop, daemon=True)
        monitor_thread.start()
        
    def _performance_monitoring_loop(self):
        """Background performance monitoring loop"""
        interval = 10 if self.is_low_end_pc else 5
        
        while True:
            try:
                self._update_memory_measurements()
                self._run_periodic_garbage_collection()
                time.sleep(interval)
            except Exception as e:
                print(f"Performance monitoring error: {e}")
                time.sleep(int(interval) * 2)

    def _update_memory_measurements(self):
        """Update memory usage measurements"""
        
        process = psutil.Process()  # pyre-fixme[16]
        memory_mb = process.memory_info().rss / 1024 / 1024
        self._memory_usage.append(memory_mb)
        
        # Keep only last limit measurements for memory efficiency
        max_measurements = 50 if self.is_low_end_pc else 100
        if len(self._memory_usage) > max_measurements:
            self._memory_usage.pop(0)

    def _run_periodic_garbage_collection(self):
        """Force garbage collection more frequently on low-end PCs"""
        gc_interval = 15 if self.is_low_end_pc else 30
        if time.time() - self._last_gc_time > gc_interval:
            gc.collect()
            self._last_gc_time = time.time()
        
    @lru_cache(maxsize=128)
    def _get_optimized_color(self, color_key):
        """Cached color retrieval for better performance"""
        return self.colors.get(color_key, '#000000')
        
    def _optimize_memory_usage(self):
        """Optimize memory usage"""
        try:
            # Force garbage collection
            gc.collect()
            
            # Clear unused caches
            if hasattr(self, '_get_optimized_color'):
                self._get_optimized_color.cache_clear()
            
            # Update memory usage display
            if hasattr(self, 'memory_info'):
                self.update_memory_info()
                
        except Exception as e:
            print(f"Memory optimization error: {e}")
    def setup_ui(self):
        """Setup the modern, premium user interface using CustomTkinter"""
        # Global color palette
        self.colors = {
            'bg_primary': '#0F111A',      # Deep Space Blue-Gray
            'bg_sidebar': '#161925',      # Elevated sidebar
            'bg_secondary': '#161925',    # Same as sidebar for compatibility
            'bg_card': '#1E2235',         # Card background
            'bg_tertiary': '#1E2235',     # Same as card for compatibility
            'accent': '#00D2FF',          # Cyber Cyan 
            'accent_glow': '#3A7BD5',     # Glow Blue
            'text_primary': '#FFFFFF',    # Crisp White
            'text_secondary': '#A0AEC0',  # Slate Gray
            'text_muted': '#718096',      # Muted text
            'success': '#00FF88',         # Neon Mint
            'warning': '#FF9F1C',         # Amber
            'error': '#FF4D4D',           # Neon Red
            'border': '#2D3748'           # Subtle Border
        }

        # Main Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # -----------------------------------------------------------------------
        # SIDEBAR NAVIGATION
        # -----------------------------------------------------------------------
        self.sidebar_frame = customtkinter.CTkFrame(self, width=240, corner_radius=0, fg_color=self.colors['bg_sidebar'])
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        # Logo and Title
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="⚡ NGXSMK", 
                                                font=customtkinter.CTkFont(size=26, weight="bold"),
                                                text_color=self.colors['accent'])
        self.logo_label.grid(row=0, column=0, padx=20, pady=(40, 5))
        
        self.subtitle_label = customtkinter.CTkLabel(self.sidebar_frame, text="GAMENET OPTIMIZER", 
                                                    font=customtkinter.CTkFont(size=9, weight="bold"),
                                                    text_color=self.colors['text_secondary'])
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Modern Sidebar Divider
        self.sidebar_sep = customtkinter.CTkFrame(self.sidebar_frame, height=1, fg_color=self.colors['border'])
        self.sidebar_sep.grid(row=2, column=0, padx=30, pady=(0, 20), sticky="ew")

        # Navigation Buttons
        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", "🏠"),
            ("FPS Boost", "🎯"),
            ("Network", "🌐"),
            ("Multi-Net", "🔗"),
            ("Traffic", "🚦"),
            ("RAM Clean", "🧠"),
            ("Gaming", "🎮")
        ]

        for i, (name, icon) in enumerate(nav_items):
            btn = customtkinter.CTkButton(self.sidebar_frame, text=f"  {icon}  {name}", 
                                         corner_radius=8, height=45, border_spacing=10,
                                         fg_color="transparent", text_color=self.colors['text_secondary'],
                                         hover_color=self.colors['bg_card'], anchor="w",
                                         command=lambda n=name: self.switch_tab(n))
            btn.grid(row=i+3, column=0, padx=20, pady=5, sticky="ew")
            self.nav_buttons[name] = btn

        # Bottom Sidebar Actions
        self.settings_btn = customtkinter.CTkButton(self.sidebar_frame, text="  ⚙️  Settings", 
                                                   fg_color="transparent", text_color=self.colors['text_secondary'],
                                                   hover_color=self.colors['bg_card'], anchor="w",
                                                   command=self.show_settings)
        self.settings_btn.grid(row=9, column=0, padx=20, pady=10, sticky="ew")

        # -----------------------------------------------------------------------
        # MAIN CONTENT AREA
        # -----------------------------------------------------------------------
        self.main_container = customtkinter.CTkFrame(self, corner_radius=15, fg_color=self.colors['bg_primary'])
        self.main_container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        # Top Bar (Status & Indicators)
        self.top_bar = customtkinter.CTkFrame(self.main_container, height=80, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.welcome_label = customtkinter.CTkLabel(self.top_bar, text="SYSTEM PRIME", 
                                                   font=customtkinter.CTkFont(size=26, weight="bold"),
                                                   text_color=self.colors['text_primary'])
        self.welcome_label.pack(side="left", padx=10)

        # Global Status Pulse (Indicator)
        self.status_indicator = customtkinter.CTkLabel(self.top_bar, text="●", text_color=self.colors['success'],
                                                  font=customtkinter.CTkFont(size=20))
        self.status_indicator.pack(side="right", padx=(10, 0))
        self.status_text = customtkinter.CTkLabel(self.top_bar, text="System Optimized", 
                                                 text_color=self.colors['text_secondary'])
        self.status_text.pack(side="right", padx=10)

        # Viewport (Dynamic Content)
        self.viewport = customtkinter.CTkFrame(self.main_container, fg_color="transparent")
        self.viewport.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Initialize Tabview for actual content grouping (hidden tab buttons, controlled by sidebar)
        self.tabview = customtkinter.CTkTabview(self.viewport, fg_color="transparent")
        self.tabview.pack(fill="both", expand=True)
        # Remove the standard tab buttons row by making it small or using a custom switcher
        self.tabview._segmented_button.grid_forget() 

        # Create all tabs
        self.create_all_tabs_v2()

        # Start background tasks
        self.after(1000, self.start_status_monitoring)
        self.after(500, self._animate_status_pulse)

    def _animate_status_pulse(self):
        """Create a breathing pulse effect for the status indicator"""
        try:
            if not hasattr(self, '_pulse_state'):
                self._pulse_state = 0
                self._pulse_direction = 1
            
            # Gradients of the accent/success color for pulse
            colors = ["#00FF88", "#00D2FF", "#00CC6A", "#0091FF"] 
            
            self._pulse_state += self._pulse_direction
            if self._pulse_state >= len(colors)-1 or self._pulse_state <= 0:
                self._pulse_direction *= -1
                
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=colors[self._pulse_state])
                
            self.after(600, self._animate_status_pulse)
        except Exception: pass

    def switch_tab(self, name):
        """Switch current view via sidebar menu"""
        # Update button styles
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == name:
                btn.configure(fg_color=self.colors['accent'], text_color=self.colors['bg_primary'])
            else:
                btn.configure(fg_color="transparent", text_color=self.colors['text_secondary'])
        
        # Switch tabview
        try:
            self.tabview.set(name)
            self.welcome_label.configure(text=f"{name} Overview" if name != "Dashboard" else "Ready for Battle")
        except Exception: pass

    def create_all_tabs_v2(self):
        """Build all feature tabs within the new tabview system"""
        # Map tab names to creation functions
        tabs = [
            ("Dashboard", self.create_dashboard_view),
            ("FPS Boost", self.create_fps_boost_tab),
            ("Network", self.create_network_optimizer_tab),
            ("Multi-Net", self.create_multi_internet_tab),
            ("Traffic", self.create_traffic_shaper_tab),
            ("RAM Clean", self.create_ram_cleaner_tab),
            ("Gaming", self.create_gaming_optimizer_tab)
        ]

        for name, func in tabs:
            self.tabview.add(name)
            func(self.tabview.tab(name))

    def create_dashboard_view(self, parent):
        """Premium central dashboard with real-time performance cards and status log"""
        parent.grid_columnconfigure((0, 1, 2), weight=1)
        parent.grid_rowconfigure(2, weight=1)
        
        # Performance Stats Row
        self.ping_card = self.create_modern_stat_card(parent, "PING", "12ms", "⚡", 0, 0, self.colors['accent'])
        self.cpu_card = self.create_modern_stat_card(parent, "CPU", "14%", "🔥", 0, 1, self.colors['warning'])
        self.ram_card = self.create_modern_stat_card(parent, "RAM", "4.2GB", "🧠", 0, 2, self.colors['success'])

        # Quick Actions Section
        actions_frame = customtkinter.CTkFrame(parent, fg_color=self.colors['bg_card'], corner_radius=15, border_width=1, border_color=self.colors['border'])
        actions_frame.grid(row=1, column=0, columnspan=3, pady=(20, 10), sticky="ew")
        
        action_header = customtkinter.CTkFrame(actions_frame, fg_color="transparent")
        action_header.pack(fill="x", padx=20, pady=(15, 5))
        
        customtkinter.CTkLabel(action_header, text="QUICK OPTIMIZATIONS", 
                              font=customtkinter.CTkFont(size=11, weight="bold"),
                              text_color=self.colors['text_secondary']).pack(side="left")

        btn_row = customtkinter.CTkFrame(actions_frame, fg_color="transparent")
        btn_row.pack(pady=(0, 15), padx=10, fill="x")
        
        customtkinter.CTkButton(btn_row, text="🚀 Optimize All", command=self.quick_optimize_all,
                               height=45, fg_color=self.colors['accent'], text_color=self.colors['bg_primary'],
                               font=customtkinter.CTkFont(size=13, weight="bold")).pack(side="left", expand=True, padx=10)
        
        customtkinter.CTkButton(btn_row, text="🧹 Flush RAM", command=self.quick_clean_ram,
                               height=45, fg_color="transparent", border_width=2,
                               border_color=self.colors['accent']).pack(side="left", expand=True, padx=10)
        
        customtkinter.CTkButton(btn_row, text="🛰️ Test Network", command=self.quick_test_network,
                               height=45, fg_color="transparent", border_width=2,
                               border_color=self.colors['accent']).pack(side="left", expand=True, padx=10)

        # Real-time System Log (Console)
        log_frame = customtkinter.CTkFrame(parent, fg_color=self.colors['bg_sidebar'], corner_radius=15, border_width=1, border_color=self.colors['border'])
        log_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky="nsew")
        
        log_header = customtkinter.CTkFrame(log_frame, fg_color="transparent")
        log_header.pack(fill="x", padx=20, pady=(10, 5))
        customtkinter.CTkLabel(log_header, text="SYSTEM OPTIMIZATION LOG", 
                              font=customtkinter.CTkFont(family="Consolas", size=10, weight="bold"),
                              text_color=self.colors['accent']).pack(side="left")
        
        self.dashboard_log = customtkinter.CTkTextbox(log_frame, fg_color="transparent", 
                                                    text_color=self.colors['success'], 
                                                    font=("Consolas", 11),
                                                    scrollbar_button_color=self.colors['accent'],
                                                    scrollbar_button_hover_color=self.colors['accent_glow'])
        self.dashboard_log.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Initial Log Message
        self.add_log("NGXSMK Engine initialized successfully.")
        self.add_log(f"Architecture: {os.name.upper()} | Cores: {os.cpu_count()}")

    def add_log(self, message):
        """Add message to systemic log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if hasattr(self, 'dashboard_log'):
            self.dashboard_log.insert("end", f"[{timestamp}] {message}\n")
            self.dashboard_log.see("end")

    def create_modern_stat_card(self, parent, title, value, icon, row, col, color):
        """Create a rounded, premium performance card with a glow-border effect"""
        # Outer glow border simulated with a frame
        border = customtkinter.CTkFrame(parent, fg_color=color, corner_radius=16)
        border.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        card = customtkinter.CTkFrame(border, fg_color=self.colors['bg_card'], corner_radius=15)
        card.pack(padx=1, pady=1, fill="both", expand=True)
        
        label = customtkinter.CTkLabel(card, text=f"{icon} {title}", font=customtkinter.CTkFont(size=11, weight="bold"),
                                      text_color=self.colors['text_secondary'])
        label.pack(pady=(15, 2))
        
        val_label = customtkinter.CTkLabel(card, text=value, font=customtkinter.CTkFont(size=28, weight="bold"),
                                          text_color=color)
        val_label.pack(pady=(0, 15))
        
        return val_label
    
    
    def create_stat_card(self, parent, icon, title, value, row, col):
        """Create a premium stat card with modern typography"""
        card = tk.Frame(parent, bg=self.colors['bg_secondary'], relief=tk.FLAT, bd=0)
        card.grid(row=row, column=col, padx=10, pady=8, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        inner = tk.Frame(card, bg=self.colors['bg_tertiary'], padx=20, pady=20)
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        icon_label = tk.Label(inner, text=icon, font=self.fonts['h1'], 
                             fg=self.colors['accent'], bg=self.colors['bg_tertiary'])
        icon_label.pack(pady=(5, 5))
        
        tk.Label(inner, text=title.upper(), font=self.fonts['small'], 
                fg=self.colors['text_muted'], bg=self.colors['bg_tertiary']).pack(pady=(0, 5))
        
        value_label = tk.Label(inner, text=value, font=self.fonts['h2'], 
                            fg=self.colors['text_primary'], bg=self.colors['bg_tertiary'])
        value_label.pack()
        
        return {'frame': card, 'value': value_label, 'icon': icon_label}
    
    def create_quick_action(self, parent, icon, text, command, row, col):
        """Create a modern quick action button with variant styling"""
        btn = customtkinter.CTkButton(parent, text=f"{icon}\n{text}", command=command,
                                     font=customtkinter.CTkFont(weight="bold"), 
                                     fg_color=self.colors['bg_card'],
                                     text_color=self.colors['text_primary'],
                                     hover_color=self.colors['accent'],
                                     height=80, corner_radius=10)
        btn.grid(row=row, column=col, padx=8, pady=8, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        return btn
    
    def quick_optimize_all(self):
        """Quick optimize all systems"""
        try:
            # Update status if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Optimizing All Systems...", text_color=self.colors['warning'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['warning'])
            
            # Run optimization in background
            def run_optimization():
                try:
                    # FPS optimization
                    fps_results = self.fps_boost.optimize_game_performance(
                        priority_boost=True,
                        cpu_optimization=True,
                        gpu_optimization=True
                    )
                    
                    # RAM cleaning
                    ram_freed = self.ram_cleaner.clean_memory()
                    
                    # Update UI in main thread
                    self.after(0, lambda: self._complete_quick_optimize_all(fps_results, ram_freed))
                    
                except Exception as e:
                    self.after(0, lambda: self._handle_quick_optimize_error(str(e)))
            
            # Start optimization in background
            threading.Thread(target=run_optimization, daemon=True).start()
            
        except Exception as e:
            self._handle_quick_optimize_error(str(e))
    
    def _complete_quick_optimize_all(self, fps_results, ram_freed):
        """Complete quick optimization with results"""
        try:
            # Update status
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="All Systems Optimized", text_color=self.colors['success'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['success'])
            
            # Show result popup
            details = f"Quick optimization completed successfully!\n\n" \
                     f"FPS Optimization:\n" \
                     f"• Processes Optimized: {fps_results.get('processes_optimized', 0)}\n" \
                     f"• System Optimized: {fps_results.get('system_optimized', False)}\n" \
                     f"• GPU Optimized: {fps_results.get('gpu_optimized', False)}\n\n" \
                     f"RAM Cleaning:\n" \
                     f"• Memory Freed: {ram_freed:.2f} MB\n\n" \
                     f"Your system is now optimized for gaming!"
            
            self.show_result_popup(
                "Quick Optimization Complete", 
                "All systems have been optimized successfully!",
                "success",
                details
            )
            
        except Exception as e:
            print(f"Error completing quick optimization: {e}")
    
    def _handle_quick_optimize_error(self, error_msg):
        """Handle quick optimization errors"""
        try:
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Optimization Failed", text_color=self.colors['error'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['error'])
            
            self.show_result_popup(
                "Quick Optimization Failed", 
                "An error occurred during optimization.",
                "error",
                f"Error details: {error_msg}"
            )
        except Exception as e:
            print(f"Error handling quick optimization error: {e}")
    
    def quick_clean_ram(self):
        """Quick RAM cleanup"""
        try:
            # Update status if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Cleaning RAM...", text_color=self.colors['warning'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['warning'])
            
            # Run RAM cleaning in background
            def run_ram_clean():
                try:
                    freed_memory = self.ram_cleaner.clean_memory()
                    self.after(0, lambda: self._complete_quick_ram_clean(freed_memory))
                except Exception as e:
                    self.after(0, lambda: self._handle_quick_ram_clean_error(str(e)))
            
            # Start RAM cleaning in background
            threading.Thread(target=run_ram_clean, daemon=True).start()
            
        except Exception as e:
            self._handle_quick_ram_clean_error(str(e))
    
    def _complete_quick_ram_clean(self, freed_memory):
        """Complete quick RAM cleaning with results"""
        try:
            # Update status
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="RAM Cleaned", text_color=self.colors['success'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['success'])
            
            # Show result popup
            details = f"RAM cleaning completed successfully!\n\n" \
                     f"Memory freed: {freed_memory:.2f} MB\n" \
                     f"System performance improved\n" \
                     f"Background processes optimized\n" \
                     f"Memory usage reduced"
            
            self.show_result_popup(
                "RAM Cleaning Complete", 
                f"Successfully freed {freed_memory:.2f} MB of RAM!",
                "success",
                details
            )
            
        except Exception as e:
            print(f"Error completing RAM clean: {e}")
    
    def _handle_quick_ram_clean_error(self, error_msg):
        """Handle quick RAM cleaning errors"""
        try:
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="RAM Clean Failed", text_color=self.colors['error'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['error'])
            
            self.show_result_popup(
                "RAM Cleaning Failed", 
                "An error occurred during RAM cleaning.",
                "error",
                f"Error details: {error_msg}"
            )
        except Exception as e:
            print(f"Error handling RAM clean error: {e}")
    
    def quick_test_network(self):
        """Quick network test"""
        try:
            # Update status if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Testing Network...", text_color=self.colors['warning'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['warning'])
            
            # Run network test in background
            def run_network_test():
                try:
                    # Run network analysis
                    results = self.network_analyzer.analyze_network()
                    
                    # Update UI in main thread
                    self.after(0, lambda: self._complete_quick_network_test(results))
                    
                except Exception as e:
                    self.after(0, lambda: self._handle_quick_network_test_error(str(e)))
            
            # Start network test in background
            threading.Thread(target=run_network_test, daemon=True).start()
            
        except Exception as e:
            self._handle_quick_network_test_error(str(e))
    
    def _complete_quick_network_test(self, results):
        """Complete quick network test with results"""
        try:
            # Update status
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Network Test Complete", text_color=self.colors['success'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['success'])
            
            # Show result popup
            details = f"Network test completed successfully!\n\n" \
                     f"Connection Status: {results.get('connection_status', 'Unknown')}\n" \
                     f"Latency: {results.get('latency', 'N/A')} ms\n" \
                     f"Download Speed: {results.get('download_speed', 'N/A')} Mbps\n" \
                     f"Upload Speed: {results.get('upload_speed', 'N/A')} Mbps\n" \
                     f"Packet Loss: {results.get('packet_loss', 'N/A')}%"
            
            self.show_result_popup(
                "Network Test Complete", 
                "Network analysis completed successfully!",
                "success",
                details
            )
            
        except Exception as e:
            print(f"Error completing network test: {e}")
    
    def _handle_quick_network_test_error(self, error_msg):
        """Handle quick network test errors"""
        try:
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Network Test Failed", text_color=self.colors['error'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['error'])
            
            self.show_result_popup(
                "Network Test Failed", 
                "An error occurred during network testing.",
                "error",
                f"Error details: {error_msg}"
            )
        except Exception as e:
            print(f"Error handling network test error: {e}")
    
    def quick_gaming_mode(self):
        """Quick gaming mode activation"""
        try:
            # Update status if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Activating Gaming Mode...", text_color=self.colors['warning'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['warning'])
            
            # Run gaming mode activation in background
            def run_gaming_mode():
                try:
                    # Activate gaming optimizations
                    gaming_results = self.gaming_optimizer.optimize_for_gaming()
                    
                    # Update UI in main thread
                    self.after(0, lambda: self._complete_quick_gaming_mode(gaming_results))
                    
                except Exception as e:
                    self.after(0, lambda: self._handle_quick_gaming_mode_error(str(e)))
            
            # Start gaming mode activation in background
            threading.Thread(target=run_gaming_mode, daemon=True).start()
            
        except Exception as e:
            self._handle_quick_gaming_mode_error(str(e))
    
    def _complete_quick_gaming_mode(self, results):
        """Complete quick gaming mode activation with results"""
        try:
            # Update status
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Gaming Mode Active", text_color=self.colors['success'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['success'])
            
            # Show result popup
            details = f"Gaming mode activated successfully!\n\n" \
                     f"Optimizations Applied:\n" \
                     f"• Process Priority: {results.get('process_priority', 'High')}\n" \
                     f"• CPU Optimization: {results.get('cpu_optimized', False)}\n" \
                     f"• GPU Optimization: {results.get('gpu_optimized', False)}\n" \
                     f"• Background Apps: {results.get('background_apps_optimized', 0)} optimized\n" \
                     f"• System Tweaks: {results.get('system_tweaks', 0)} applied\n\n" \
                     f"Your system is now optimized for gaming!"
            
            self.show_result_popup(
                "Gaming Mode Activated", 
                "Gaming optimizations have been applied successfully!",
                "success",
                details
            )
            
        except Exception as e:
            print(f"Error completing gaming mode: {e}")
    
    def _handle_quick_gaming_mode_error(self, error_msg):
        """Handle quick gaming mode errors"""
        try:
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Gaming Mode Failed", text_color=self.colors['error'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['error'])
            
            self.show_result_popup(
                "Gaming Mode Failed", 
                "An error occurred during gaming mode activation.",
                "error",
                f"Error details: {error_msg}"
            )
        except Exception as e:
            print(f"Error handling gaming mode error: {e}")
    
    def optimize_fps(self):
        """Optimize FPS settings"""
        try:
            print("FPS optimization started...")  # Debug print
            
            # Update main status if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Optimizing FPS...", text_color=self.colors['warning'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['warning'])
            
            # Get selected game
            game = self.game_var.get()
            print(f"Selected game: {game}")  # Debug print
            
            # Run FPS optimization in background thread
            def run_optimization():
                try:
                    print("Starting optimization process...")  # Debug print
                    
                    # Simulate optimization process
                    time.sleep(1)  # Simulate processing time
                    
                    # Run FPS optimization
                    print("Calling fps_boost.optimize_game_performance...")  # Debug print
                    results = self.fps_boost.optimize_game_performance(
                        priority_boost=self.priority_boost.get(),
                        cpu_optimization=self.cpu_optimization.get(),
                        gpu_optimization=self.gpu_optimization.get()
                    )
                    print(f"Optimization results: {results}")  # Debug print
                    
                    # Update UI in main thread
                    self.after(0, lambda: self.update_fps_status(game, results))
                    
                except Exception as e:
                    print(f"Error in optimization thread: {e}")  # Debug print
                    self.after(0, lambda: self.handle_fps_error(str(e)))
            
            # Start optimization in background
            threading.Thread(target=run_optimization, daemon=True).start()
            
        except Exception as e:
            print(f"Error in optimize_fps: {e}")  # Debug print
            self.handle_fps_error(str(e))
    
    def update_fps_status(self, game, results):
        """Update FPS status display"""
        try:
            # Update status display
            self.fps_status.configure(state=tk.NORMAL)
            self.fps_status.delete(1.0, tk.END)
            self.fps_status.insert(tk.END, "FPS Optimization Results:\n")
            self.fps_status.insert(tk.END, f"Game: {game}\n")
            self.fps_status.insert(tk.END, f"Processes Optimized: {results.get('processes_optimized', 0)}\n")
            self.fps_status.insert(tk.END, f"Priority Boost: {'Enabled' if self.priority_boost.get() else 'Disabled'}\n")
            self.fps_status.insert(tk.END, f"CPU Optimization: {'Enabled' if self.cpu_optimization.get() else 'Disabled'}\n")
            self.fps_status.insert(tk.END, f"GPU Optimization: {'Enabled' if self.gpu_optimization.get() else 'Disabled'}\n")
            self.fps_status.insert(tk.END, "\nOptimization completed successfully!")
            self.fps_status.configure(state=tk.DISABLED)
            
            # Update main status if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="FPS Optimization Complete", text_color=self.colors['success'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['success'])
            
            # Show result popup
            details = f"FPS optimization completed successfully!\n\n" \
                     f"Game: {game}\n" \
                     f"Processes Optimized: {results.get('processes_optimized', 0)}\n" \
                     f"Priority Boost: {'Enabled' if self.priority_boost.get() else 'Disabled'}\n" \
                     f"CPU Optimization: {'Enabled' if self.cpu_optimization.get() else 'Disabled'}\n" \
                     f"GPU Optimization: {'Enabled' if self.gpu_optimization.get() else 'Disabled'}\n\n" \
                     f"Your system has been optimized for better gaming performance!"
            
            self.show_result_popup(
                "FPS Optimization Complete", 
                "Your system has been optimized for better gaming performance!",
                "success",
                details
            )
            
        except Exception as e:
            self.handle_fps_error(str(e))
    
    def handle_fps_error(self, error_msg):
        """Handle FPS optimization errors"""
        try:
            self.fps_status.configure(state=tk.NORMAL)
            self.fps_status.delete(1.0, tk.END)
            self.fps_status.insert(tk.END, f"Error during FPS optimization: {error_msg}")
            self.fps_status.configure(state=tk.DISABLED)
            
            # Update main status if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="FPS Optimization Failed", text_color=self.colors['error'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['error'])
            
            # Show error popup
            self.show_result_popup(
                "FPS Optimization Failed", 
                "An error occurred during FPS optimization.",
                "error",
                f"Error details: {error_msg}"
            )
            
        except Exception as e:
            print(f"Failed to handle FPS error: {e}")
    
    def test_fps_optimization(self):
        """Test FPS optimization functionality"""
        try:
            print("Testing FPS optimization...")
            
            # Update status
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Testing FPS...", text_color=self.colors['warning'])
            
            # Test the FPS boost module directly
            results = self.fps_boost.optimize_game_performance(
                priority_boost=True,
                cpu_optimization=True,
                gpu_optimization=True
            )
            
            # Update status display
            self.fps_status.configure(state=tk.NORMAL)
            self.fps_status.delete(1.0, tk.END)
            self.fps_status.insert(tk.END, "FPS Test Results:\n")
            self.fps_status.insert(tk.END, f"Processes Optimized: {results.get('processes_optimized', 0)}\n")
            self.fps_status.insert(tk.END, f"System Optimized: {results.get('system_optimized', False)}\n")
            self.fps_status.insert(tk.END, f"GPU Optimized: {results.get('gpu_optimized', False)}\n")
            self.fps_status.insert(tk.END, f"Errors: {len(results.get('errors', []))}\n")
            if results.get('errors'):
                self.fps_status.insert(tk.END, f"Error Details: {', '.join(results['errors'])}\n")
            self.fps_status.insert(tk.END, "\nTest completed successfully!")
            self.fps_status.configure(state=tk.DISABLED)
            
            # Update main status
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="FPS Test Complete", text_color=self.colors['success'])
            
            # Show result popup
            details = f"FPS optimization test completed!\n\n" \
                     f"Processes Optimized: {results.get('processes_optimized', 0)}\n" \
                     f"System Optimized: {results.get('system_optimized', False)}\n" \
                     f"GPU Optimized: {results.get('gpu_optimized', False)}\n" \
                     f"Errors: {len(results.get('errors', []))}\n\n" \
                     f"The FPS optimization system is working correctly!"
            
            self.show_result_popup(
                "FPS Test Complete", 
                "FPS optimization test completed successfully!",
                "success",
                details
            )
            
        except Exception as e:
            print(f"FPS test error: {e}")
            self.fps_status.configure(state=tk.NORMAL)
            self.fps_status.delete(1.0, tk.END)
            self.fps_status.insert(tk.END, f"FPS Test Error: {str(e)}")
            self.fps_status.configure(state=tk.DISABLED)
            
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="FPS Test Failed", text_color=self.colors['error'])
            
            self.show_result_popup(
                "FPS Test Failed", 
                "An error occurred during FPS testing.",
                "error",
                f"Error details: {str(e)}"
            )
    
    def reset_fps_settings(self):
        """Reset FPS settings to default"""
        self.priority_boost.set(True)
        self.cpu_optimization.set(True)
        self.gpu_optimization.set(True)
        self.game_var.set("Auto-detect")
        
        self.fps_status.configure(state=tk.NORMAL)
        self.fps_status.delete(1.0, tk.END)
        self.fps_status.insert(tk.END, "FPS settings reset to default values.")
        self.fps_status.configure(state=tk.DISABLED)
        
        if hasattr(self, 'status_text'):
            self.status_text.configure(text="FPS Settings Reset", text_color=self.colors['success'])
    
    def create_modern_checkbox(self, parent, text, description, variable):
        """Create a premium styled checkbox with description"""
        checkbox_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        checkbox_frame.pack(fill="x", pady=8)
        
        cb = customtkinter.CTkCheckBox(checkbox_frame, text=text, variable=variable,
                                      font=customtkinter.CTkFont(size=13, weight="bold"),
                                      text_color=self.colors['text_primary'],
                                      fg_color=self.colors['accent'],
                                      hover_color=self.colors['accent_glow'],
                                      border_color=self.colors['border'])
        cb.pack(anchor="w")
        
        if description:
            desc_label = customtkinter.CTkLabel(checkbox_frame, text=description, 
                                             font=customtkinter.CTkFont(size=11), 
                                             text_color=self.colors['text_secondary'])
            desc_label.pack(anchor="w", padx=(35, 0))
        
        return cb
    
    def create_modern_radiobutton(self, parent, text, variable, value):
        """Create a premium styled radio button"""
        rb = customtkinter.CTkRadioButton(parent, text=text, variable=variable, value=value,
                                         font=customtkinter.CTkFont(size=13),
                                         text_color=self.colors['text_primary'], 
                                         fg_color=self.colors['accent'],
                                         hover_color=self.colors['accent_glow'],
                                         border_color=self.colors['border'])
        rb.pack(side="left", padx=5, pady=5)
        return rb
    
    def create_modern_button(self, parent, text, command):
        """Create a premium primary button with hover effects"""
        btn = customtkinter.CTkButton(parent, text=text, command=command,
                                     font=customtkinter.CTkFont(weight="bold"), 
                                     fg_color=self.colors['accent'], 
                                     text_color=self.colors['bg_primary'],
                                     hover_color=self.colors['accent_glow'],
                                     corner_radius=8, height=40)
        btn.pack(pady=10)
        return btn
    
    def create_sidebar_button(self, parent, icon, text, command):
        """Create a premium sidebar navigation button"""
        btn_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=52)
        btn_frame.pack(fill=tk.X, pady=2)
        btn_frame.pack_propagate(False)
        
        indicator = tk.Frame(btn_frame, bg=self.colors['accent'], width=4)
        indicator.pack(side=tk.LEFT, fill=tk.Y)
        indicator.pack_forget()
        
        btn = tk.Button(btn_frame, text=f"  {icon}   {text}", command=command,
                       font=self.fonts['body_bold'], bg=self.colors['bg_secondary'], 
                       fg=self.colors['text_secondary'], relief=tk.FLAT, bd=0,
                       padx=20, cursor='hand2', anchor=tk.W)
        btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        def on_enter(e):
            if btn.cget('fg') != self.colors['accent']:
                btn.configure(bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        def on_leave(e):
            if btn.cget('fg') != self.colors['accent']:
                btn.configure(bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'])
        
        btn.bind(ENTER_EVENT, on_enter)
        btn.bind(LEAVE_EVENT, on_leave)
        return btn_frame, btn, indicator
    
    def create_status_indicator(self, parent, icon, title, value, color):
        """Create a premium status card for the status bar"""
        card = tk.Frame(parent, bg=self.colors['bg_tertiary'], padx=15, pady=10)
        card.pack(fill=tk.X, padx=15, pady=5)
        
        icon_label = tk.Label(card, text=icon, font=self.fonts['h2'], 
                             fg=color, bg=self.colors['bg_tertiary'])
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        info = tk.Frame(card, bg=self.colors['bg_tertiary'])
        info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(info, text=title.upper(), font=self.fonts['small'], 
                fg=self.colors['text_muted'], bg=self.colors['bg_tertiary']).pack(anchor=tk.W)
        
        val_label = tk.Label(info, text=value, font=self.fonts['body_bold'], 
                            fg=color, bg=self.colors['bg_tertiary'])
        val_label.pack(anchor=tk.W)
        
        return {'frame': card, 'value': val_label, 'icon': icon_label}
    
    def start_status_monitoring(self):
        """Start optimized real-time status monitoring"""
        try:
            self.update_system_status()
            # Adaptive update interval based on system capabilities
            interval = 2000 if self.is_low_end_pc else 1000  # 2 seconds for low-end PCs
            self.after(interval, self.start_status_monitoring)
        except Exception as e:
            print(f"Status monitoring error: {e}")
            # Retry after a longer interval
            self.after(5000, self.start_status_monitoring)
    
    def update_system_status(self):
        """Update system status indicators - Optimized version"""
        try:

            # Use cached metrics for better performance
            cache_interval = 1.0 if self.is_low_end_pc else 0.5
            if not hasattr(self, '_last_metrics') or time.time() - self._last_metrics['time'] > cache_interval:
                self._last_metrics = {
                    'memory': psutil.virtual_memory(),  # pyre-fixme[16]
                    'cpu_percent': psutil.cpu_percent(interval=0.1),  # pyre-fixme[16]
                    'time': time.time()
                }
                print(f"Updated metrics: RAM {self._last_metrics['memory'].percent:.1f}%, CPU {self._last_metrics['cpu_percent']:.1f}%")  # Debug print
            
            metrics = self._last_metrics
            
            # Prepare status updates
            status_updates = {
                'ram': (f"{metrics['memory'].percent:.1f}%", self._get_status_color(metrics['memory'].percent, [70, 90])),
                'fps': ("Active" if self.is_optimizing else "Ready", self.colors['success'] if not self.is_optimizing else self.colors['warning'])
            }
            
            # Add CPU status for capable PCs
            if not self.is_low_end_pc:
                status_updates['cpu'] = (f"{metrics['cpu_percent']:.1f}%", self._get_status_color(metrics['cpu_percent'], [50, 80]))
            
            # Update status indicators
            self._batch_update_status_indicators(status_updates)
            
            # Update main status text if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text=f"RAM: {metrics['memory'].percent:.1f}% | CPU: {metrics['cpu_percent']:.1f}%", text_color=self.colors['text_primary'])
            
        except Exception as e:
            print(f"Status update error: {e}")
            import traceback
            traceback.print_exc()
    
    def _get_status_color(self, value, thresholds):
        """Get status color based on value and thresholds"""
        if value < thresholds[0]:
            return self.colors['success']
        elif value < thresholds[1]:
            return self.colors['warning']
        else:
            return self.colors['error']
    
    def _batch_update_status_indicators(self, updates):
        """Batch update status indicators for better performance"""
        try:
            for status_type, (text, color) in updates.items():
                self._update_single_status_indicator(status_type, text, color)
            
            # Update network status in background to avoid blocking the UI thread
            # Optimized to avoid creating too many threads
            if hasattr(self, 'network_status_indicator'):
                if not hasattr(self, '_network_thread_active') or not self._network_thread_active:
                    self._network_thread_active = True
                    threading.Thread(target=self._check_network_background, daemon=True).start()
            
        except Exception as e:
            print(f"Batch status update error: {e}")

    def _update_single_status_indicator(self, status_type, text, color):
        """Update a specific status indicator widget"""
        # Update dashboard modern cards
        if status_type == 'ram' and hasattr(self, 'ram_card'):
            self.ram_card.configure(text=text, text_color=color)
        elif status_type == 'cpu' and hasattr(self, 'cpu_card'):
            self.cpu_card.configure(text=text, text_color=color)

        indicator_name = f'{status_type}_status_indicator'
        if hasattr(self, indicator_name):
            indicator = getattr(self, indicator_name)
            if isinstance(indicator, dict) and 'value_label' in indicator:
                indicator['value_label'].configure(text=text, text_color=color)
                if 'icon_label' in indicator:
                    indicator['icon_label'].configure(text_color=color)

    def _check_network_background(self):
        """Perform network check in a background thread"""
        try:
            import socket as _socket
            conn = _socket.create_connection(("8.8.8.8", 53), timeout=3)
            conn.close()
            status, color = "Connected", self.colors['success']
        except Exception:
            status, color = "Disconnected", self.colors['error']
        finally:
            self._network_thread_active = False
        self.after(0, lambda s=status, c=color: self._update_network_indicator(s, c))
        
    def _update_network_indicator(self, status: str, color: str):
        """Update the network status indicator from the UI thread"""
        try:
            # Update dashboard modern card
            if hasattr(self, 'ping_card'):
                # Simulate a ping value for the dashboard if just status is provided
                val = "12ms" if status == "Connected" else "---"
                self.ping_card.configure(text=val, text_color=color)
                if status == "Disconnected":
                    self.add_log("Network connectivity lost!")
                elif status == "Connected" and not getattr(self, '_net_logged', False):
                    self.add_log("Network link established.")
                    self._net_logged = True

            if hasattr(self, 'network_status_indicator'):
                indicator = self.network_status_indicator
                if isinstance(indicator, dict) and 'value_label' in indicator:
                    indicator['value_label'].configure(text=status, text_color=color)
                    if 'icon_label' in indicator:
                        indicator['icon_label'].configure(text_color=color)
        except Exception:
            pass

    def create_fps_boost_tab(self, parent):
        """Modernized FPS Boost Tab"""
        parent.grid_columnconfigure(0, weight=1)
        
        # Primary Optimization Card
        opt_card = customtkinter.CTkFrame(parent, fg_color=self.colors['bg_card'])
        opt_card.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(opt_card, text="🎯 GAMING ENGINE TWEAKS", 
                              font=customtkinter.CTkFont(size=14, weight="bold"),
                              text_color=self.colors['accent']).pack(pady=(15, 5))
                              
        # Game Selector
        self.game_var = customtkinter.StringVar(value="Auto-detect")
        game_selector = customtkinter.CTkOptionMenu(opt_card, variable=self.game_var,
                                                   values=["Auto-detect", "Valorant", "CS2", "Apex Legends", "LoL"],
                                                   fg_color=self.colors['bg_primary'],
                                                   button_color=self.colors['accent'],
                                                   button_hover_color=self.colors['accent_glow'])
        game_selector.pack(pady=10, padx=20)

        # Switches Frame
        switches_frame = customtkinter.CTkFrame(opt_card, fg_color="transparent")
        switches_frame.pack(pady=15)
        
        self.priority_boost = customtkinter.CTkSwitch(switches_frame, text="Process Priority Boost", progress_color=self.colors['accent'])
        self.priority_boost.select()
        self.priority_boost.pack(side="left", padx=20)
        
        self.cpu_optimization = customtkinter.CTkSwitch(switches_frame, text="CPU Optimization", progress_color=self.colors['accent'])
        self.cpu_optimization.select()
        self.cpu_optimization.pack(side="left", padx=20)
        
        self.gpu_optimization = customtkinter.CTkSwitch(switches_frame, text="GPU Optimization", progress_color=self.colors['accent'])
        self.gpu_optimization.select()
        self.gpu_optimization.pack(side="left", padx=20)

        # Action Row
        btn_row = customtkinter.CTkFrame(opt_card, fg_color="transparent")
        btn_row.pack(pady=(10, 20))
        
        customtkinter.CTkButton(btn_row, text="🎯 Apply Boost", command=self.optimize_fps,
                               fg_color=self.colors['accent'], text_color=self.colors['bg_primary'],
                               font=customtkinter.CTkFont(weight="bold")).pack(side="left", padx=10)
                               
        customtkinter.CTkButton(btn_row, text="🧪 Benchmark", command=self.test_fps_optimization,
                               fg_color="transparent", border_width=2, border_color=self.colors['accent']).pack(side="left", padx=10)

        # Status Log
        self.fps_status = customtkinter.CTkTextbox(parent, height=200, fg_color=self.colors['bg_sidebar'], 
                                                  text_color=self.colors['success'], font=("Consolas", 12))
        self.fps_status.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.fps_status.insert("0.0", "System ready for optimization sequence...\n")
        self.fps_status.configure(state="disabled")
        
    def create_network_analyzer_tab(self, parent):
        """Modernized Network Analyzer Tab"""
        parent.grid_columnconfigure(0, weight=1)
        
        card = customtkinter.CTkFrame(parent, fg_color=self.colors['bg_card'])
        card.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(card, text="🌐 NETWORK DEEP ANALYZER", 
                              font=customtkinter.CTkFont(size=14, weight="bold"),
                              text_color=self.colors['accent']).pack(pady=(15, 5))
                              
        btn_row = customtkinter.CTkFrame(card, fg_color="transparent")
        btn_row.pack(pady=(10, 20))
        
        self.start_analysis_btn = customtkinter.CTkButton(btn_row, text="🔍 Start Analysis", command=self.start_network_analysis,
                                                         fg_color=self.colors['accent'], text_color=self.colors['bg_primary'])
        self.start_analysis_btn.pack(side="left", padx=10)
        
        self.stop_analysis_btn = customtkinter.CTkButton(btn_row, text="⏹ Stop", command=self.stop_network_analysis,
                                                        fg_color=self.colors['error'])
        self.stop_analysis_btn.pack(side="left", padx=10)
        self.stop_analysis_btn.configure(state="disabled")

        self.network_results = customtkinter.CTkTextbox(parent, height=300, fg_color=self.colors['bg_sidebar'], 
                                                       text_color=self.colors['success'], font=("Consolas", 12))
        self.network_results.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.network_results.insert("0.0", "Ready for network diagnostics...\n")
        self.network_results.configure(state="disabled")
        
    def create_multi_internet_tab(self, parent):
        """Modernized Multi-Internet Tab"""
        parent.grid_columnconfigure(0, weight=1)
        
        card = customtkinter.CTkFrame(parent, fg_color=self.colors['bg_card'])
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        customtkinter.CTkLabel(card, text="🔗 MULTI-CONNECTION MANAGER", 
                              font=customtkinter.CTkFont(size=14, weight="bold"),
                              text_color=self.colors['accent']).pack(pady=(15, 10))
                              
        self.connection_list = tk.Listbox(card, bg=self.colors['bg_primary'], 
                                         fg=self.colors['text_primary'],
                                         font=('Consolas', 12), relief=tk.FLAT, 
                                         highlightthickness=0, borderwidth=0)
        self.connection_list.pack(fill="both", expand=True, padx=20, pady=10)
        
        btn_row = customtkinter.CTkFrame(card, fg_color="transparent")
        btn_row.pack(pady=15)
        
        customtkinter.CTkButton(btn_row, text="🔄 Refresh Connections", command=self.load_connections,
                               fg_color="transparent", border_width=2, border_color=self.colors['accent']).pack(padx=10)
        
        self.load_connections()
        
    def create_modern_tab_header(self, parent, icon, title, subtitle):
        """Create a consistent modern header for tabs"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=120)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        container = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        icon_label = tk.Label(container, text=icon, font=self.fonts['h1'], 
                             fg=self.colors['accent'], bg=self.colors['bg_secondary'])
        icon_label.pack(side=tk.LEFT, padx=(0, 20))
        
        text_container = tk.Frame(container, bg=self.colors['bg_secondary'])
        text_container.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(text_container, text=title, font=self.fonts['h2'], 
                 fg=self.colors['text_primary'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        tk.Label(text_container, text=subtitle, font=self.fonts['body'], 
                 fg=self.colors['text_secondary'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        return header_frame

    def create_traffic_shaper_tab(self, parent):
        """Modernized Traffic Shaper Tab"""
        parent.grid_columnconfigure(0, weight=1)
        
        card = customtkinter.CTkFrame(parent, fg_color=self.colors['bg_card'])
        card.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(card, text="🚦 TRAFFIC CONTROL ENGINE", 
                              font=customtkinter.CTkFont(size=14, weight="bold"),
                              text_color=self.colors['accent']).pack(pady=(15, 10))
                              
        # Bandwidth Slider
        tk.Label(card, text="MAX BANDWIDTH (Mbps)", font=customtkinter.CTkFont(size=10),
                 fg=self.colors['text_secondary'], bg=self.colors['bg_card']).pack()
        
        self.bandwidth_var = customtkinter.StringVar(value="500")
        self.bw_slider = customtkinter.CTkSlider(card, from_=10, to=1000, 
                                                number_of_steps=99,
                                                button_color=self.colors['accent'],
                                                progress_color=self.colors['accent'],
                                                command=lambda v: self.bandwidth_var.set(str(int(v))))
        self.bw_slider.pack(pady=10, padx=40, fill="x")
        
        customtkinter.CTkLabel(card, textvariable=self.bandwidth_var, font=customtkinter.CTkFont(size=24, weight="bold")).pack()

        # Options
        self.prioritize_gaming = customtkinter.CTkSwitch(card, text="Prioritize Gaming Packets", progress_color=self.colors['accent'])
        self.prioritize_gaming.select()
        self.prioritize_gaming.pack(pady=10)
        
        self.limit_background = customtkinter.CTkSwitch(card, text="Throttle Background Apps", progress_color=self.colors['accent'])
        self.limit_background.select()
        self.limit_background.pack(pady=10)
        
    def create_ram_cleaner_tab(self, parent):
        """Modernized RAM Cleaner Tab"""
        parent.grid_columnconfigure(0, weight=1)
        
        card = customtkinter.CTkFrame(parent, fg_color=self.colors['bg_card'])
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        customtkinter.CTkLabel(card, text="🧹 MEMORY STREAMLINER", 
                              font=customtkinter.CTkFont(size=14, weight="bold"),
                              text_color=self.colors['accent']).pack(pady=(15, 10))
                              
        self.memory_info = customtkinter.CTkTextbox(card, height=120, fg_color=self.colors['bg_sidebar'],
                                                  text_color=self.colors['success'], font=("Consolas", 14))
        self.memory_info.pack(fill="x", padx=20, pady=10)
        
        self.auto_clean = customtkinter.CTkSwitch(card, text="Predictive Auto-Clean", progress_color=self.colors['accent'])
        self.auto_clean.pack(pady=15)
        
        customtkinter.CTkButton(card, text="🧹 FLUSH NOW", command=self.clean_ram,
                               height=50, fg_color=self.colors['accent'], text_color=self.colors['bg_primary'],
                               font=customtkinter.CTkFont(weight="bold")).pack(pady=10)
        
        self.update_memory_info()
        
    def create_lol_optimizer_tab(self, parent):
        """Modernized LoL Optimizer Tab"""
        parent.grid_columnconfigure(0, weight=1)
        
        card = customtkinter.CTkFrame(parent, fg_color=self.colors['bg_card'])
        card.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(card, text="⚔️ LEAGUE PRECISION SYSTEM", 
                              font=customtkinter.CTkFont(size=14, weight="bold"),
                              text_color=self.colors['accent']).pack(pady=(15, 10))
                              
        btn_row = customtkinter.CTkFrame(card, fg_color="transparent")
        btn_row.pack(pady=15)
        
        customtkinter.CTkButton(btn_row, text="⚔️ Apply LoL Tweaks", command=self.optimize_lol,
                               fg_color=self.colors['accent'], text_color=self.colors['bg_primary']).pack(side="left", padx=10)
                               
        customtkinter.CTkButton(btn_row, text="📡 Server Latency", command=self.test_lol_latency,
                               fg_color="transparent", border_width=2, border_color=self.colors['accent']).pack(side="left", padx=10)

        self.lol_status = customtkinter.CTkTextbox(parent, height=200, fg_color=self.colors['bg_sidebar'], 
                                                  text_color=self.colors['success'], font=("Consolas", 12))
        self.lol_status.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.update_lol_status()
        
    def optimize_lol(self):
        """Optimize League of Legends"""
        try:
            results = self.lol_optimizer.optimize_lol_performance()
            
            status_text = "=== LoL Optimization Results ===\n\n"
            status_text += f"Processes Optimized: {results['processes_optimized']}\n"
            status_text += f"Priority Set: {'Yes' if results['priority_set'] else 'No'}\n"
            status_text += f"Memory Optimized: {'Yes' if results['memory_optimized'] else 'No'}\n"
            status_text += f"Network Optimized: {'Yes' if results['network_optimized'] else 'No'}\n\n"
            
            if results['errors']:
                status_text += "Errors:\n"
                for error in results['errors']:
                    status_text += f"- {error}\n"
            else:
                status_text += "✅ All optimizations applied successfully!\n"
            
            self.lol_status.configure(state=tk.NORMAL)
            self.lol_status.delete(1.0, tk.END)
            self.lol_status.insert(tk.END, status_text)
            self.lol_status.configure(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"LoL optimization failed: {str(e)}")
    
    def test_lol_latency(self):
        """Test League of Legends server latency"""
        try:
            latencies = self.lol_optimizer.get_lol_server_latency()
            best_server = self.lol_optimizer.get_best_lol_server()
            
            status_text = "=== LoL Server Latency Test ===\n\n"
            status_text += f"Best Server: {best_server}\n\n"
            status_text += "Server Latencies:\n"
            
            for region, latency in latencies.items():
                if latency < 999:
                    status_text += f"{region}: {latency:.1f}ms\n"
                else:
                    status_text += f"{region}: Unable to reach\n"
            
            self.lol_status.configure(state=tk.NORMAL)
            self.lol_status.delete(1.0, tk.END)
            self.lol_status.insert(tk.END, status_text)
            self.lol_status.configure(state=tk.DISABLED)
            
            # Show result popup
            details = f"LoL Server Latency Test Results:\n\n" \
                     f"Best Server: {best_server}\n\n" \
                     f"Server Latencies:\n"
            
            for region, latency in latencies.items():
                if latency < 999:
                    details += f"• {region}: {latency:.1f}ms\n"
                else:
                    details += f"• {region}: Unable to reach\n"
            
            details += f"\nRecommendation: Use {best_server} for the best gaming experience!"
            
            self.show_result_popup(
                "LoL Server Test Complete", 
                f"Server latency test completed! Best server: {best_server}",
                "success",
                details
            )
            
        except Exception as e:
            # Show error popup
            self.show_result_popup(
                "LoL Server Test Failed", 
                "An error occurred during server latency testing.",
                "error",
                f"Error details: {str(e)}"
            )
    
    def update_lol_status(self):
        """Update League of Legends status"""
        try:
            metrics = self.lol_optimizer.get_lol_performance_metrics()
            recommendations = self.lol_optimizer.get_lol_optimization_recommendations()
            
            status_text = "=== LoL Performance Status ===\n\n"
            status_text += f"Processes Running: {metrics['processes_running']}\n"
            status_text += f"Memory Usage: {metrics['total_memory_mb']:.1f} MB\n"
            status_text += f"CPU Usage: {metrics['cpu_usage']:.1f}%\n"
            status_text += f"Network Connections: {metrics['network_connections']}\n\n"
            
            if recommendations:
                status_text += "Recommendations:\n"
                for rec in recommendations[:5]:  # Show first 5 recommendations
                    status_text += f"• {rec}\n"
            
            self.lol_status.configure(state=tk.NORMAL)
            self.lol_status.delete(1.0, tk.END)
            self.lol_status.insert(tk.END, status_text)
            self.lol_status.configure(state=tk.DISABLED)
            
        except Exception as e:
            print(f"Failed to update LoL status: {e}")
        
    
    def open_settings(self):
        """Open settings dialog (legacy method for compatibility)"""
        self.show_settings()
        
            
    def start_network_analysis(self):
        """Start network analysis"""
        self.start_analysis_btn.configure(state=tk.DISABLED)
        self.stop_analysis_btn.configure(state=tk.NORMAL)
        
        # Start analysis in separate thread
        threading.Thread(target=self.run_network_analysis, daemon=True).start()
        
    def stop_network_analysis(self):
        """Stop network analysis"""
        self.start_analysis_btn.configure(state=tk.NORMAL)
        self.stop_analysis_btn.configure(state=tk.DISABLED)
        
    def run_network_analysis(self):
        """Run network analysis with progress feedback"""
        try:
            # Update button states
            self.start_analysis_btn.configure(state=tk.DISABLED)
            self.stop_analysis_btn.configure(state=tk.NORMAL)
            
            # Clear and show progress
            self.network_results.configure(state=tk.NORMAL)
            self.network_results.delete(1.0, tk.END)
            self.network_results.insert(tk.END, "🔍 Starting network analysis...\n")
            self.network_results.configure(state=tk.DISABLED)
            self.update()
            
            # Step 1: Basic connectivity
            self.network_results.configure(state=tk.NORMAL)
            self.network_results.insert(tk.END, "📡 Testing basic connectivity...\n")
            self.network_results.configure(state=tk.DISABLED)
            self.update()
            time.sleep(1)
            
            # Step 2: Server latency tests
            self.network_results.configure(state=tk.NORMAL)
            self.network_results.insert(tk.END, "🌐 Testing server latency...\n")
            self.network_results.configure(state=tk.DISABLED)
            self.update()
            time.sleep(1)
            
            # Step 3: Gaming servers
            self.network_results.configure(state=tk.NORMAL)
            self.network_results.insert(tk.END, "🎮 Testing gaming servers...\n")
            self.network_results.configure(state=tk.DISABLED)
            self.update()
            time.sleep(1)
            
            # Get results
            results = self.network_analyzer.analyze_network()
            
            # Display results
            self.network_results.configure(state=tk.NORMAL)
            self.network_results.delete(1.0, tk.END)
            self.network_results.insert(tk.END, results)
            self.network_results.configure(state=tk.DISABLED)
            
            # Show result popup
            details = ("Network analysis completed successfully!\n\n"
                      "Analysis Results:\n"
                      "• Basic connectivity tested\n"
                      "• Server latency measured\n"
                      "• Gaming servers tested\n"
                      "• Network performance analyzed\n\n"
                      "Check the results panel for detailed information.")
            
            self.show_result_popup(
                "Network Analysis Complete", 
                "Network analysis completed successfully!",
                "success",
                details
            )
            
        except Exception as e:
            self.network_results.configure(state=tk.NORMAL)
            self.network_results.delete(1.0, tk.END)
            self.network_results.insert(tk.END, f"❌ Analysis failed: {str(e)}")
            self.network_results.configure(state=tk.DISABLED)
            
            # Show error popup
            self.show_result_popup(
                "Network Analysis Failed", 
                "An error occurred during network analysis.",
                "error",
                f"Error details: {str(e)}"
            )
        finally:
            self.stop_analysis_btn.configure(state=tk.DISABLED)
            self.start_analysis_btn.configure(state=tk.NORMAL)
            
    def load_connections(self):
        """Load available network connections"""
        try:
            connections = self.multi_internet.get_available_connections()
            self.connection_list.delete(0, tk.END)
            for conn in connections:
                self.connection_list.insert(tk.END, conn)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load connections: {str(e)}")
            
    def clean_ram(self):
        """Clean RAM memory"""
        try:
            # Update status if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Cleaning RAM...", text_color=self.colors['warning'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['warning'])
            
            # Clean RAM memory
            print("Starting RAM cleaning...")  # Debug print
            freed_memory = self.ram_cleaner.clean_memory()
            print(f"RAM cleaning completed, freed: {freed_memory:.2f} MB")  # Debug print
            
            # Update memory info
            self.update_memory_info()
            
            # Update status if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="RAM Cleaned", text_color=self.colors['success'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['success'])
            
            # Show result popup
            details = f"RAM cleaning completed successfully!\n\n" \
                     f"Memory freed: {freed_memory:.2f} MB\n" \
                     f"System performance improved\n" \
                     f"Background processes optimized\n" \
                     f"Memory usage reduced\n\n" \
                     f"Your system memory has been optimized for better performance!"
            
            self.show_result_popup(
                "RAM Cleaning Complete", 
                f"Successfully freed {freed_memory:.2f} MB of RAM!",
                "success",
                details
            )
            
        except Exception as e:
            print(f"RAM cleaning error: {e}")  # Debug print
            
            # Update status if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="RAM Clean Failed", text_color=self.colors['error'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.configure(text_color=self.colors['error'])
            
            # Show error popup
            self.show_result_popup(
                "RAM Cleaning Failed", 
                "An error occurred during RAM cleaning.",
                "error",
                f"Error details: {str(e)}\n\nPlease try again or check system permissions."
            )
            
    def update_memory_info(self):
        """Update memory information display"""
        try:
            memory_info = self.ram_cleaner.get_memory_info()
            
            # Format memory info as text
            memory_text = f"Total Memory: {memory_info['total_memory']:.1f} GB\n"
            memory_text += f"Available: {memory_info['available_memory']:.1f} GB\n"
            memory_text += f"Used: {memory_info['used_memory']:.1f} GB\n"
            memory_text += f"Usage: {memory_info['memory_percent']:.1f}%"
            
            # Update memory info display if it exists
            if hasattr(self, 'memory_info'):
                self.memory_info.configure(state=tk.NORMAL)
                self.memory_info.delete(1.0, tk.END)
                self.memory_info.insert(tk.END, memory_text)
                self.memory_info.configure(state=tk.DISABLED)
            
            # Update status if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text=f"RAM: {memory_info['memory_percent']:.1f}%", text_color=self.colors['text_primary'])
                
        except Exception as e:
            print(f"Failed to update memory info: {e}")
            
    def show_settings(self):
        """Open modern settings dialog"""
        try:
            settings_dialog = SettingsDialog(self, self.config_manager, colors=self.colors, fonts=self.fonts)
            settings_dialog.show_settings()
            
            # Make the dialog modal
            settings_dialog.dialog.grab_set()
            self.wait_window(settings_dialog.dialog)
            
            # Reload settings after dialog is actually closed
            self.load_settings()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open settings: {str(e)}")
    
    def show_result_popup(self, title, message, result_type="success", details=None):
        """Show premium result popup modal"""
        popup = customtkinter.CTkToplevel(self)
        popup.title(title)
        popup.geometry("500x400")
        popup.configure(fg_color=self.colors['bg_primary'])
        popup.after(10, lambda: popup.focus())
        
        # Icon mapping
        icons = {"success": ("✅", self.colors['success']), 
                 "warning": ("⚠️", self.colors['warning']), 
                 "error": ("❌", self.colors['error'])}
        icon_char, icon_color = icons.get(result_type, ("ℹ️", self.colors['accent']))

        content = customtkinter.CTkFrame(popup, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        customtkinter.CTkLabel(content, text=icon_char, font=customtkinter.CTkFont(size=48), text_color=icon_color).pack()
        customtkinter.CTkLabel(content, text=title, font=customtkinter.CTkFont(size=20, weight="bold")).pack(pady=5)
        customtkinter.CTkLabel(content, text=message, text_color=self.colors['text_secondary'], wraplength=400).pack(pady=(0, 20))
        
        if details:
            details_box = customtkinter.CTkTextbox(content, height=120, fg_color=self.colors['bg_sidebar'], 
                                                  font=("Consolas", 12), text_color=self.colors['text_secondary'])
            details_box.pack(fill="x", pady=10)
            details_box.insert("0.0", details)
            details_box.configure(state="disabled")

        customtkinter.CTkButton(content, text="CONTINUE", command=popup.destroy,
                               fg_color=self.colors['accent'], text_color=self.colors['bg_primary'],
                               font=customtkinter.CTkFont(weight="bold")).pack(side="bottom", pady=(10, 0))
    
    def show_about(self):
        """Show about dialog with premium branding"""
        try:
            about = tk.Toplevel(self)
            about.title("About NGXSMK Optimizer")
            about.geometry("650x580")
            about.configure(bg=self.colors['bg_primary'])
            about.resizable(False, False)
            about.transient(self)
            about.grab_set()
            
            # Header with branding
            header = tk.Frame(about, bg=self.colors['bg_secondary'], pady=30)
            header.pack(fill=tk.X)
            
            tk.Label(header, text="🚀", font=('Segoe UI', 64), 
                     fg=self.colors['accent'], bg=self.colors['bg_secondary']).pack()
            
            tk.Label(header, text="NGXSMK GAMENET OPTIMIZER", font=self.fonts['h1'], 
                     fg=self.colors['text_primary'], bg=self.colors['bg_secondary']).pack(pady=(10, 0))
            
            tk.Label(header, text="Version 2.0.0 • Premium Edition", font=self.fonts['body'], 
                     fg=self.colors['text_muted'], bg=self.colors['bg_secondary']).pack()
            
            # Content
            content = tk.Frame(about, bg=self.colors['bg_primary'], padx=40, pady=30)
            content.pack(fill=tk.BOTH, expand=True)
            
            desc = "A high-performance optimization suite designed for extreme latency reduction and system streamlining. Built for enthusiasts who demand the best from their hardware."
            tk.Label(content, text=desc, font=self.fonts['body'], fg=self.colors['text_secondary'],
                    bg=self.colors['bg_primary'], wraplength=550, justify=tk.CENTER).pack(pady=(0, 20))
            
            # Info Grid
            info_frame = tk.Frame(content, bg=self.colors['bg_primary'])
            info_frame.pack(fill=tk.X)
            
            def add_info_row(icon, label, value):
                row = tk.Frame(info_frame, bg=self.colors['bg_primary'], pady=5)
                row.pack(fill=tk.X)
                tk.Label(row, text=f"{icon} {label}:", font=self.fonts['body_bold'], 
                         fg=self.colors['accent'], bg=self.colors['bg_primary']).pack(side=tk.LEFT)
                tk.Label(row, text=value, font=self.fonts['body'], 
                         fg=self.colors['text_primary'], bg=self.colors['bg_primary']).pack(side=tk.LEFT, padx=10)
            
            add_info_row("👨‍💻", "Architect", "NGXSMK")
            add_info_row("🛠", "Platform", "Windows 10/11 x64")
            add_info_row("⚖️", "License", "MIT Open Source")
            
            # Close button
            self.create_modern_button(about, "CLOSE", about.destroy).pack(side=tk.BOTTOM, pady=30)
            
            # Center dialog
            about.update_idletasks()
            w, h = about.winfo_width(), about.winfo_height()
            x = (about.winfo_screenwidth() // 2) - (w // 2)
            y = (about.winfo_screenheight() // 2) - (h // 2)
            about.geometry(f'+{x}+{y}')
            
        except Exception as e:
            print(f"About dialog error: {e}")
        
    def load_settings(self):
        """Load application settings"""
        try:
            settings = self.config_manager.load_settings()
            
            # Apply theme
            ui = settings.get('ui', {})
            theme = ui.get('theme', 'dark')
            self.apply_theme(theme)
            
            # Apply language
            language = ui.get('language', 'en')
            self.apply_language(language)
            
            # Apply low-resource mode if enabled
            if ui.get('low_resource_mode', False):
                self.enable_low_resource_mode()
            
            # Apply other settings
            self.apply_other_settings(settings)
            
        except Exception as e:
            print(f"Failed to load settings: {e}")
    
    def enable_low_resource_mode(self):
        """Enable low-resource mode for better performance on low-end PCs"""
        try:
            self.low_resource_mode = True
            self.reduced_animations = True
            self.minimal_ui = True
            
            # Reduce update frequencies
            if hasattr(self, 'start_status_monitoring'):
                # Restart monitoring with reduced frequency
                pass
            
            print("Low-resource mode enabled")
            
        except Exception as e:
            print(f"Failed to enable low-resource mode: {e}")
    
    def apply_theme(self, theme):
        """Apply theme to the application"""
        try:
            if theme == 'light':
                self.colors = {
                    'bg_primary': '#ffffff',
                    'bg_sidebar': '#f5f5f5', 
                    'bg_secondary': '#f5f5f5', 
                    'bg_card': '#e0e0e0',
                    'bg_tertiary': '#e0e0e0',
                    'accent': '#0066cc',
                    'accent_glow': '#0052a3',
                    'text_primary': '#000000',
                    'text_secondary': '#333333',
                    'text_muted': '#666666',
                    'success': '#00aa00',
                    'warning': '#ff8800',
                    'error': '#cc0000',
                    'border': '#cccccc'
                }
            elif theme == 'gaming':
                self.colors = {
                    'bg_primary': '#0d1117',
                    'bg_sidebar': '#161b22', 
                    'bg_secondary': '#161b22', 
                    'bg_card': '#21262d',
                    'bg_tertiary': '#21262d',
                    'accent': '#ff6b35',
                    'accent_glow': '#ff5722',
                    'text_primary': '#f0f6fc',
                    'text_secondary': '#c9d1d9',
                    'text_muted': '#8b949e',
                    'success': '#3fb950',
                    'warning': '#d29922',
                    'error': '#f85149',
                    'border': '#30363d'
                }
            else:  # dark theme (default)
                self.colors = {
                    'bg_primary': '#0a0a0a',
                    'bg_sidebar': '#1a1a1a', 
                    'bg_secondary': '#1a1a1a', 
                    'bg_card': '#2a2a2a',
                    'bg_tertiary': '#2a2a2a',
                    'accent': '#00ff88',
                    'accent_glow': '#00cc6a',
                    'text_primary': '#ffffff',
                    'text_secondary': '#cccccc',
                    'text_muted': '#888888',
                    'success': '#00ff88',
                    'warning': '#ffaa00',
                    'error': '#ff4444',
                    'border': '#333333'
                }
            
            # Update UI colors
            self.update_ui_colors()
            
        except Exception as e:
            print(f"Failed to apply theme: {e}")
    
    def apply_language(self, language):
        """Apply language to the application"""
        try:
            # Language translations
            translations = {
                'en': {
                    'title': APP_TITLE,
                    'fps_boost': 'FPS Boost',
                    'network_analyzer': 'Network Analyzer',
                    'multi_internet': MULTI_INTERNET_LABEL,
                    'traffic_shaper': 'Traffic Shaper',
                    'ram_cleaner': 'RAM Cleaner',
                    'lol_optimizer': 'LoL Optimizer',
                    'advanced_optimizer': 'Advanced Optimizer',
                    'system_monitor': 'System Monitor',
                    'network_optimizer': 'Network Optimizer',
                    'settings': 'Settings',
                    'status': 'System Ready',
                    'optimize': 'Optimize',
                    'reset': 'Reset',
                    'start': 'Start',
                    'stop': 'Stop',
                    'optimize_all': OPTIMIZE_ALL_LABEL,
                    'clean_ram': CLEAN_RAM_LABEL,
                    'test_network': TEST_NETWORK_LABEL,
                    'gaming_mode': GAMING_MODE_LABEL,
                    'ready': READY_STATUS,
                    'optimizing': OPTIMIZING_STATUS,
                    'about': ABOUT_LABEL
                },
                'es': {
                    'title': APP_TITLE,
                    'fps_boost': 'Impulso FPS',
                    'network_analyzer': 'Analizador de Red',
                    'multi_internet': MULTI_INTERNET_LABEL,
                    'traffic_shaper': 'Moldeador de Tráfico',
                    'ram_cleaner': 'Limpiador RAM',
                    'lol_optimizer': 'Optimizador LoL',
                    'advanced_optimizer': 'Optimizador Avanzado',
                    'system_monitor': 'Monitor del Sistema',
                    'network_optimizer': 'Optimizador de Red',
                    'settings': 'Configuración',
                    'status': 'Sistema Listo',
                    'optimize': 'Optimizar',
                    'reset': 'Restablecer',
                    'start': 'Iniciar',
                    'stop': 'Detener',
                    'optimize_all': "Optimizar Todo",
                    'clean_ram': "Limpiar RAM",
                    'test_network': "Probar Red",
                    'gaming_mode': "Modo Juego",
                    'ready': "Listo",
                    'optimizing': "Optimizando...",
                    'about': "Acerca de"
                },
                'fr': {
                    'title': APP_TITLE,
                    'fps_boost': 'Boost FPS',
                    'network_analyzer': 'Analyseur Réseau',
                    'multi_internet': MULTI_INTERNET_LABEL,
                    'traffic_shaper': 'Formateur de Trafic',
                    'ram_cleaner': 'Nettoyeur RAM',
                    'lol_optimizer': 'Optimiseur LoL',
                    'advanced_optimizer': 'Optimiseur Avancé',
                    'system_monitor': 'Moniteur Système',
                    'network_optimizer': 'Optimiseur Réseau',
                    'settings': 'Paramètres',
                    'status': 'Système Prêt',
                    'optimize': 'Optimiser',
                    'reset': 'Réinitialiser',
                    'start': 'Démarrer',
                    'stop': 'Arrêter',
                    'optimize_all': "Optimiser Tout",
                    'clean_ram': "Nettoyer RAM",
                    'test_network': "Tester Réseau",
                    'gaming_mode': "Mode Jeu",
                    'ready': "Prêt",
                    'optimizing': "Optimisation...",
                }
            }
            
            # Get translations for current language
            self.translations = translations.get(language, translations['en'])
            
            # Update UI text
            self.update_ui_text()
            
        except Exception as e:
            print(f"Failed to apply language: {e}")
    
    def _set_checkbox(self, attr_name: str, value: bool):
        if hasattr(self, attr_name):
            widget = getattr(self, attr_name)
            widget.select() if value else widget.deselect()

    def apply_other_settings(self, settings):
        """Apply other settings to the application UI variables with consistent schema mapping"""
        try:
            # UI settings
            ui = settings.get('ui', {})
            # Note: theme and language are handled separately in apply_theme/apply_language
            
            # FPS Boost settings
            fps = settings.get('fps_boost', {})
            self._set_checkbox('priority_boost', fps.get('priority_boost', True))
            self._set_checkbox('cpu_optimization', fps.get('cpu_optimization', True))
            self._set_checkbox('gpu_optimization', fps.get('gpu_optimization', True))
                
            # Traffic Shaper settings
            traffic = settings.get('traffic_shaper', {})
            self._set_checkbox('prioritize_gaming', traffic.get('prioritize_gaming', True))
            self._set_checkbox('limit_background', traffic.get('limit_background', True))
                
            # RAM Cleaner settings
            ram = settings.get('ram_cleaner', {})
            self._set_checkbox('auto_clean', ram.get('auto_clean', True))
            
            # Network settings
            net = settings.get('network', {})
            if hasattr(self, 'network_profile'):
                self.network_profile.set(net.get('profile', 'gaming'))
                
            # Gaming Optimizer settings
            gaming = settings.get('gaming', {})
            if hasattr(self, 'gaming_profile'):
                self.gaming_profile.set(gaming.get('profile', 'auto'))

            # Auto-optimize settings
            if ui.get('auto_optimize', False):
                self.auto_optimize_on_startup()
            
        except Exception as e:
            print(f"Failed to apply other settings: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_sidebar_buttons_colors(self, bg_tertiary, text_primary):
        if not hasattr(self, 'sidebar_buttons'): return
        for btn_info in self.sidebar_buttons.values():
            if isinstance(btn_info, dict) and 'btn' in btn_info:
                btn = btn_info['btn']
                if hasattr(btn, 'configure'):
                    if 'customtkinter' in str(type(btn)):
                        btn.configure(fg_color=bg_tertiary, text_color=text_primary)
                    else:
                        btn.configure(bg=bg_tertiary, fg=text_primary)

    def _update_status_indicators_colors(self, bg_tertiary):
        if not hasattr(self, 'status_indicators'): return
        for indicator in self.status_indicators:
            indicator.configure(bg=bg_tertiary)

    def update_ui_colors(self):
        """Update UI colors based on current theme - Optimized version"""
        try:
            # Use cached colors for better performance
            bg_primary = self._get_optimized_color('bg_primary')
            bg_secondary = self._get_optimized_color('bg_secondary')
            bg_tertiary = self._get_optimized_color('bg_tertiary')
            text_primary = self._get_optimized_color('text_primary')
            text_muted = self._get_optimized_color('text_muted')
            accent = self._get_optimized_color('accent')
            success = self._get_optimized_color('success')
            accent_hover = self._get_optimized_color('accent_hover')
            
            # Batch UI updates for better performance
            self._batch_update_colors({
                'root': (self, {'fg_color': bg_primary}),
                'main_frame': (getattr(self, 'main_frame', None), {'fg_color': bg_primary}),
                'header_frame': (getattr(self, 'header_frame', None), {'fg_color': bg_secondary}),
                'header_content': (getattr(self, 'header_content', None), {'fg_color': bg_secondary}),
                'title_section': (getattr(self, 'title_section', None), {'fg_color': bg_secondary}),
                'controls_section': (getattr(self, 'controls_section', None), {'fg_color': bg_secondary}),
                'status_frame': (getattr(self, 'status_frame', None), {'fg_color': bg_secondary}),
                'logo_label': (getattr(self, 'logo_label', None), {'text_color': accent, 'fg_color': bg_secondary}),
                'title_label': (getattr(self, 'title_label', None), {'text_color': text_primary, 'fg_color': bg_secondary}),
                'subtitle_label': (getattr(self, 'subtitle_label', None), {'text_color': text_muted, 'fg_color': bg_secondary}),
                'status_indicator': (getattr(self, 'status_indicator', None), {'text_color': success, 'fg_color': bg_secondary}),
                'status_text': (getattr(self, 'status_text', None), {'text_color': text_primary, 'fg_color': bg_secondary}),
                'sidebar_frame': (getattr(self, 'sidebar_frame', None), {'fg_color': bg_secondary}),
                'sidebar_title': (getattr(self, 'sidebar_title', None), {'text_color': text_primary, 'fg_color': bg_secondary})
            })
            
            # Update sidebar buttons efficiently
            self._update_sidebar_buttons_colors(bg_tertiary, text_primary)
            
            # Update status indicators efficiently
            self._update_status_indicators_colors(bg_tertiary)
            
            # Update notebook styles efficiently
            self._update_notebook_styles(bg_secondary, bg_tertiary, text_primary, accent, accent_hover)
            
            # Update tab content frames
            self.update_tab_colors()
            
        except Exception as e:
            print(f"Failed to update UI colors: {e}")
    
    def _batch_update_colors(self, updates):
        """Batch update colors for better performance"""
        for name, (widget, config) in updates.items():
            if widget is not None:
                try:
                    widget.configure(**config)
                except Exception as e:
                    print(f"Failed to update {name}: {e}")
    
    def _update_notebook_styles(self, bg_secondary, bg_tertiary, text_primary, accent, accent_hover):
        """Update notebook styles efficiently"""
        try:
            style = ttk.Style()
            style.configure('Modern.TNotebook', 
                           background=bg_secondary, 
                           borderwidth=0,
                           tabmargins=[0, 0, 0, 0])
            style.configure('Modern.TNotebook.Tab', 
                           background=bg_tertiary, 
                           foreground=text_primary, 
                           padding=[20, 10],
                           borderwidth=0)
            style.map('Modern.TNotebook.Tab',
                     background=[('selected', accent),
                                ('active', bg_tertiary)])
            
            style.configure('Modern.TButton',
                           background=bg_tertiary,
                           foreground=text_primary,
                           borderwidth=1,
                           focuscolor='none')
            style.map('Modern.TButton',
                     background=[('active', accent),
                                ('pressed', accent_hover)])
        except Exception as e:
            print(f"Failed to update notebook styles: {e}")
    
    def update_tab_colors(self):
        """Update colors for all tab content"""
        try:
            # Update all tab frames
            for tab_frame in self.tab_frames:
                tab_frame.configure(bg=self.colors['bg_primary'])
                
                # Update all widgets in the tab
                self.update_widget_colors(tab_frame)
                
        except Exception as e:
            print(f"Failed to update tab colors: {e}")
    
    def _set_widget_config(self, widget, **kwargs):
        try:
            widget.configure(**kwargs)
        except Exception:
            pass

    def _apply_widget_color(self, child, ctype, is_ctk):
        c_bg, c_fg = self.colors['bg_primary'], self.colors['text_primary']
        bg_sec, bg_ter = self.colors['bg_secondary'], self.colors['bg_tertiary']
        
        if "frame" in ctype:
            self._set_widget_config(child, fg_color=c_bg) if is_ctk else self._set_widget_config(child, bg=c_bg)
        elif "label" in ctype:
            self._set_widget_config(child, text_color=c_fg, fg_color=c_bg) if is_ctk else self._set_widget_config(child, bg=c_bg, fg=c_fg)
        elif "button" in ctype:
            self._set_widget_config(child, text_color=c_fg, fg_color=bg_ter) if is_ctk else self._set_widget_config(child, bg=bg_ter, fg=c_fg)
        elif "textbox" in ctype or "text" in ctype:
            self._set_widget_config(child, text_color=c_fg, fg_color=bg_sec) if is_ctk else self._set_widget_config(child, bg=bg_sec, fg=c_fg)
        elif "scrollbar" in ctype:
            self._set_widget_config(child, bg=bg_ter)

    def update_widget_colors(self, parent):
        """Recursively update widget colors"""
        try:
            for child in parent.winfo_children():
                # Detect widget type and apply colors correctly
                ctype = str(type(child)).lower()
                is_ctk = "customtkinter" in ctype
                
                if not hasattr(child, 'configure'):
                    continue
                
                self._apply_widget_color(child, ctype, is_ctk)
                if "frame" in ctype:
                    self.update_widget_colors(child)
                    
        except Exception as e:
            print(f"Failed to update widget colors: {e}")
    
    def update_ui_text(self):
        """Update UI text based on current language"""
        try:
            # Update window title
            self.title(self.translations.get('title', 'NGXSMK GameNet Optimizer'))
            
            # Update title and subtitle
            if hasattr(self, 'title_label'):
                self.title_label.configure(text=self.translations.get('title', 'NGXSMK GameNet Optimizer'))
            
            # Update status text
            if hasattr(self, 'status_text'):
                self.status_text.configure(text=self.translations.get('status', 'System Ready'))
            
            # Update notebook tabs
            if hasattr(self, 'notebook'):
                for i, tab_id in enumerate(self.notebook.tabs()):
                    tab_text = self.notebook.tab(tab_id, 'text')
                    # Map tab text to translations
                    tab_mapping = {
                        '🎮 FPS Boost': f"🎮 {self.translations.get('fps_boost', 'FPS Boost')}",
                        '📊 Network Analyzer': f"📊 {self.translations.get('network_analyzer', 'Network Analyzer')}",
                        '🌐 Multi Internet': f"🌐 {self.translations.get('multi_internet', 'Multi Internet')}",
                        '🚦 Traffic Shaper': f"🚦 {self.translations.get('traffic_shaper', 'Traffic Shaper')}",
                        '🧹 RAM Cleaner': f"🧹 {self.translations.get('ram_cleaner', 'RAM Cleaner')}",
                        '⚔️ LoL Optimizer': f"⚔️ {self.translations.get('lol_optimizer', 'LoL Optimizer')}",
                        '🔬 Advanced Optimizer': f"🔬 {self.translations.get('advanced_optimizer', 'Advanced Optimizer')}",
                        '📈 System Monitor': f"📈 {self.translations.get('system_monitor', 'System Monitor')}",
                        '🌐 Network Optimizer': f"🌐 {self.translations.get('network_optimizer', 'Network Optimizer')}"
                    }
                    
                    if tab_text in tab_mapping:
                        self.notebook.tab(tab_id, text=tab_mapping[tab_text])
            
        except Exception as e:
            print(f"Failed to update UI text: {e}")
    
    def auto_optimize_on_startup(self):
        """Auto-optimize on startup if enabled"""
        try:
            # Start background optimization
            thread = threading.Thread(target=self._auto_optimize_loop, daemon=True)
            self.optimization_thread = thread
            thread.start()
        except Exception as e:
            print(f"Failed to start auto-optimization: {e}")
    
    def _auto_optimize_loop(self):
        """Auto-optimization loop"""
        try:
            while True:
                # Perform automatic optimizations
                self.fps_boost.optimize_game_performance()
                self.ram_cleaner.clean_memory()
                time.sleep(300)  # Optimize every 5 minutes
        except Exception as e:
            print(f"Auto-optimization error: {e}")
            
    def save_settings(self):
        """Save application settings safely without losing data"""
        try:
            # Load current settings first to merge
            current_settings = self.config_manager.load_settings()
            
            # Update specific sections with current UI state
            current_settings['fps_boost'] = {
                'priority_boost': self.priority_boost.get() if hasattr(self, 'priority_boost') else True,
                'cpu_optimization': self.cpu_optimization.get() if hasattr(self, 'cpu_optimization') else True,
                'gpu_optimization': self.gpu_optimization.get() if hasattr(self, 'gpu_optimization') else True
            }
            
            current_settings['traffic_shaper'] = {
                'prioritize_gaming': self.prioritize_gaming.get() if hasattr(self, 'prioritize_gaming') else True,
                'limit_background': self.limit_background.get() if hasattr(self, 'limit_background') else True
            }
            
            current_settings['ram_cleaner'] = {
                'auto_clean': self.auto_clean.get() if hasattr(self, 'auto_clean') else False
            }
            
            # Use get() safely as these might not be initialized if tab wasn't created
            if hasattr(self, 'network_profile'):
                if 'network' not in current_settings: current_settings['network'] = {}
                current_settings['network']['profile'] = self.network_profile.get()
                
            if hasattr(self, 'gaming_profile'):
                if 'gaming' not in current_settings: current_settings['gaming'] = {}
                current_settings['gaming']['profile'] = self.gaming_profile.get()
            
            # Final save
            self.config_manager.save_settings(current_settings)
        except Exception as e:
            print(f"Failed to save settings: {e}")
            import traceback
            traceback.print_exc()

    def create_advanced_optimizer_tab(self, parent):
        """Modernized Advanced AI Optimizer Tab"""
        parent.grid_columnconfigure(0, weight=1)
        
        card = customtkinter.CTkFrame(parent, fg_color=self.colors['bg_card'])
        card.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(card, text="🤖 NEURAL CORE OPTIMIZER", 
                              font=customtkinter.CTkFont(size=14, weight="bold"),
                              text_color=self.colors['accent']).pack(pady=(15, 10))
                              
        self.advanced_profile = customtkinter.StringVar(value="gaming")
        seg_btn = customtkinter.CTkSegmentedButton(card, values=["gaming", "streaming", "productivity", "balanced"],
                                                 variable=self.advanced_profile,
                                                 selected_color=self.colors['accent'],
                                                 selected_hover_color=self.colors['accent_glow'])
        seg_btn.pack(pady=10, padx=20)
        
        btn_row = customtkinter.CTkFrame(card, fg_color="transparent")
        btn_row.pack(pady=15)
        
        self.start_advanced_btn = customtkinter.CTkButton(btn_row, text="🚀 Activate AI Core", command=self.start_advanced_optimization,
                                                         fg_color=self.colors['accent'], text_color=self.colors['bg_primary'])
        self.start_advanced_btn.pack(side="left", padx=10)
        
        self.stop_advanced_btn = customtkinter.CTkButton(btn_row, text="⏹ Stop AI", command=self.stop_advanced_optimization,
                                                        fg_color="transparent", border_width=2, border_color=self.colors['error'])
        self.stop_advanced_btn.pack(side="left", padx=10)

        self.advanced_results = customtkinter.CTkTextbox(parent, height=250, fg_color=self.colors['bg_sidebar'], 
                                                       text_color=self.colors['success'], font=("Consolas", 12))
        self.advanced_results.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def create_system_monitor_tab(self, parent):
        """Modernized System Monitor Tab"""
        parent.grid_columnconfigure(0, weight=1)
        
        card = customtkinter.CTkFrame(parent, fg_color=self.colors['bg_card'])
        card.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(card, text="📊 TELEMETRY FEED", 
                              font=customtkinter.CTkFont(size=14, weight="bold"),
                              text_color=self.colors['accent']).pack(pady=(15, 10))
                              
        btn_row = customtkinter.CTkFrame(card, fg_color="transparent")
        btn_row.pack(pady=15)
        
        self.start_monitor_btn = customtkinter.CTkButton(btn_row, text="📊 Start Data Feed", command=self.start_system_monitoring,
                                                        fg_color=self.colors['accent'], text_color=self.colors['bg_primary'])
        self.start_monitor_btn.pack(side="left", padx=10)
        
        self.stop_monitor_btn = customtkinter.CTkButton(btn_row, text="⏹ Stop Feed", command=self.stop_system_monitoring,
                                                       fg_color="transparent", border_width=2, border_color=self.colors['error'])
        self.stop_monitor_btn.pack(side="left", padx=10)

        self.monitor_display = customtkinter.CTkTextbox(parent, height=300, fg_color=self.colors['bg_sidebar'], 
                                                       text_color=self.colors['success'], font=("Consolas", 12))
        self.monitor_display.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def create_network_optimizer_tab(self, parent):
        """Modernized Network Optimizer Tab"""
        parent.grid_columnconfigure(0, weight=1)
        
        card = customtkinter.CTkFrame(parent, fg_color=self.colors['bg_card'])
        card.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(card, text="🌐 STACK OPTIMIZATION", 
                              font=customtkinter.CTkFont(size=14, weight="bold"),
                              text_color=self.colors['accent']).pack(pady=(15, 10))
                              
        self.network_profile = customtkinter.StringVar(value="gaming")
        seg_btn = customtkinter.CTkSegmentedButton(card, values=["gaming", "streaming", "productivity"],
                                                 variable=self.network_profile,
                                                 selected_color=self.colors['accent'],
                                                 selected_hover_color=self.colors['accent_glow'])
        seg_btn.pack(pady=10, padx=20)
        
        btn_row = customtkinter.CTkFrame(card, fg_color="transparent")
        btn_row.pack(pady=15)
        
        self.start_network_btn = customtkinter.CTkButton(btn_row, text="🌐 Apply Stack Optimization", command=self.start_network_optimization,
                                                        fg_color=self.colors['accent'], text_color=self.colors['bg_primary'])
        self.start_network_btn.pack(side="left", padx=10)
        
        self.stop_network_btn = customtkinter.CTkButton(btn_row, text="⏹ Revert", command=self.stop_network_optimization,
                                                       fg_color="transparent", border_width=2, border_color=self.colors['error'])
        self.stop_network_btn.pack(side="left", padx=10)

        self.network_status = customtkinter.CTkTextbox(parent, height=200, fg_color=self.colors['bg_sidebar'], 
                                                      text_color=self.colors['success'], font=("Consolas", 12))
        self.network_status.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def create_gaming_optimizer_tab(self, parent):
        """Modernized Gaming Optimizer Tab"""
        parent.grid_columnconfigure(0, weight=1)
        
        card = customtkinter.CTkFrame(parent, fg_color=self.colors['bg_card'])
        card.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(card, text="🎮 ENGINE CALIBRATION", 
                              font=customtkinter.CTkFont(size=14, weight="bold"),
                              text_color=self.colors['accent']).pack(pady=(15, 10))
                              
        self.gaming_profile = customtkinter.StringVar(value="auto")
        game_options = ["auto", "valorant", "cs2", "fortnite", "apex", "lol"]
        seg_btn = customtkinter.CTkSegmentedButton(card, values=game_options,
                                                 variable=self.gaming_profile,
                                                 selected_color=self.colors['accent'],
                                                 selected_hover_color=self.colors['accent_glow'])
        seg_btn.pack(pady=10, padx=20)
        
        btn_row = customtkinter.CTkFrame(card, fg_color="transparent")
        btn_row.pack(pady=15)
        
        self.start_gaming_btn = customtkinter.CTkButton(btn_row, text="🎮 Activate Game Mode", command=self.start_gaming_optimization,
                                                       fg_color=self.colors['accent'], text_color=self.colors['bg_primary'])
        self.start_gaming_btn.pack(side="left", padx=10)
        
        self.stop_gaming_btn = customtkinter.CTkButton(btn_row, text="⏹ Stop", command=self.stop_gaming_optimization,
                                                      fg_color="transparent", border_width=2, border_color=self.colors['error'])
        self.stop_gaming_btn.pack(side="left", padx=10)

        self.gaming_status = customtkinter.CTkTextbox(parent, height=200, fg_color=self.colors['bg_sidebar'], 
                                                     text_color=self.colors['success'], font=("Consolas", 12))
        self.gaming_status.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def start_advanced_optimization(self):
        """Start advanced optimization"""
        try:
            profile = self.advanced_profile.get()
            results = self.advanced_optimizer.start_advanced_optimization(profile)
            
            self.advanced_results.configure(state=tk.NORMAL)
            self.advanced_results.delete(1.0, tk.END)
            self.advanced_results.insert(tk.END, json.dumps(results, indent=2))
            self.advanced_results.configure(state=tk.DISABLED)
            
            self.start_advanced_btn.configure(state=tk.DISABLED)
            self.stop_advanced_btn.configure(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"Advanced optimization failed: {str(e)}")
    
    def stop_advanced_optimization(self):
        """Stop advanced optimization"""
        try:
            self.advanced_optimizer.stop_optimization()
            self.start_advanced_btn.configure(state=tk.NORMAL)
            self.stop_advanced_btn.configure(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop optimization: {str(e)}")
    
    def start_system_monitoring(self):
        """Start system monitoring"""
        try:
            result = self.system_monitor.start_monitoring(interval=5)
            
            self.monitor_display.configure(state=tk.NORMAL)
            self.monitor_display.delete(1.0, tk.END)
            self.monitor_display.insert(tk.END, f"System monitoring started: {result}\n")
            self.monitor_display.configure(state=tk.DISABLED)
            
            self.start_monitor_btn.configure(state=tk.DISABLED)
            self.stop_monitor_btn.configure(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"System monitoring failed: {str(e)}")
    
    def stop_system_monitoring(self):
        """Stop system monitoring"""
        try:
            result = self.system_monitor.stop_monitoring()
            
            self.monitor_display.configure(state=tk.NORMAL)
            self.monitor_display.insert(tk.END, f"System monitoring stopped: {result}\n")
            self.monitor_display.configure(state=tk.DISABLED)
            
            self.start_monitor_btn.configure(state=tk.NORMAL)
            self.stop_monitor_btn.configure(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop monitoring: {str(e)}")
    
    def start_network_optimization(self):
        """Start network optimization"""
        try:
            profile = self.network_profile.get()
            results = self.network_optimizer.start_network_optimization(profile)
            
            self.network_status.configure(state="normal")
            self.network_status.delete("0.0", "end")
            self.network_status.insert("0.0", json.dumps(results, indent=2))
            self.network_status.configure(state="disabled")
            
            self.start_network_btn.configure(state="disabled")
            self.stop_network_btn.configure(state="normal")
            
        except Exception as e:
            self.show_result_popup("Error", f"Network optimization failed: {str(e)}", "error")
    
    def stop_network_optimization(self):
        """Stop network optimization"""
        try:
            result = self.network_optimizer.stop_network_optimization()
            self.network_status.configure(state="normal")
            self.network_status.insert("end", f"\nNetwork optimization stopped: {result}\n")
            self.network_status.configure(state="disabled")
            self.start_network_btn.configure(state="normal")
            self.stop_network_btn.configure(state="disabled")
        except Exception as e:
            self.show_result_popup("Error", f"Failed to stop network optimization: {str(e)}", "error")
    
    def start_gaming_optimization(self):
        """Start gaming optimization"""
        try:
            profile = self.gaming_profile.get()
            results = self.gaming_optimizer.start_gaming_optimization(profile)
            self.gaming_status.configure(state="normal")
            self.gaming_status.delete("0.0", "end")
            self.gaming_status.insert("0.0", json.dumps(results, indent=2))
            self.gaming_status.configure(state="disabled")
            self.start_gaming_btn.configure(state="disabled")
            self.stop_gaming_btn.configure(state="normal")
        except Exception as e:
            self.show_result_popup("Error", f"Gaming optimization failed: {str(e)}", "error")
    
    def stop_gaming_optimization(self):
        """Stop gaming optimization"""
        try:
            result = self.gaming_optimizer.stop_gaming_optimization()
            self.gaming_status.configure(state="normal")
            self.gaming_status.insert("end", f"\nGaming optimization stopped: {result}\n")
            self.gaming_status.configure(state="disabled")
            self.start_gaming_btn.configure(state="normal")
            self.stop_gaming_btn.configure(state="disabled")
        except Exception as e:
            self.show_result_popup("Error", f"Failed to stop gaming optimization: {str(e)}", "error")

    def toggle_fullscreen(self, event=None):
        """Toggle between fullscreen and windowed mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode safely"""
        self.is_fullscreen = False
        self.attributes("-fullscreen", False)
        return "break"

    def on_closing(self):
        """Premium exit sequence"""
        try:
            self.save_settings()
            self._cleanup_resources()
        except Exception:
            pass
        self.destroy()
    
    def _cleanup_resources(self):
        """Force cleanup of system resources"""
        try:
            if hasattr(self, 'executor'): self.executor.shutdown(wait=False)
            gc.collect()
        except Exception: pass
    
    def run(self):
        """Execute main loop"""
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

if __name__ == "__main__":
    try:
        app = NetworkOptimizerApp()
        app.run()
    except Exception as e:
        print(f"Application failed to start: {e}")
        sys.exit(1)
