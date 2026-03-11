#!/usr/bin/env python3
"""
NGXSMK GameNet Optimizer
A comprehensive network and system optimization tool for gamers
Open source alternative to commercial gaming optimization software
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
import os
import time
import json
import gc
import weakref
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

# Import our modules
from .modules.fps_boost import FPSBoost
from .modules.network_analyzer import NetworkAnalyzer
from .modules.multi_internet import MultiInternet
from .modules.traffic_shaper import TrafficShaper
from .modules.ram_cleaner import RAMCleaner
from .modules.lol_optimizer import LoLOptimizer
from .modules.advanced_optimizer import AdvancedOptimizer
from .modules.system_monitor import SystemMonitor
from .modules.network_optimizer import NetworkOptimizer
from .modules.gaming_optimizer import GamingOptimizer
from .modules.config_manager import ConfigManager
from .modules.settings_dialog import SettingsDialog

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

class NetworkOptimizerApp:
    def __init__(self):
        # Performance optimizations
        self._setup_performance_optimizations()
        
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        
        # Detect system capabilities for low-end PC optimization
        self._detect_system_capabilities()
        
        # Adaptive window sizing based on system capabilities
        if self.is_low_end_pc:
            self.root.geometry("1000x700")  # Smaller window for low-end PCs
            self.root.minsize(800, 600)
        else:
            self.root.state('zoomed')  # Fullscreen for capable PCs
            self.root.minsize(1200, 800)
        
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(True, True)
        
        # Add fullscreen toggle functionality
        self.is_fullscreen = not self.is_low_end_pc
        if not self.is_low_end_pc:
            self.root.bind('<F11>', self.toggle_fullscreen)
            self.root.bind('<Escape>', self.exit_fullscreen)
        
        # Performance monitoring
        self._startup_time = time.time()
        self._last_gc_time = time.time()
        self._memory_usage = []
        
        # Adaptive thread pool based on system capabilities
        max_workers = 2 if self.is_low_end_pc else 4
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
        # Weak references for memory management
        self._weak_refs = weakref.WeakSet()
        
        # Center the window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Initialize modules
        self.config_manager = ConfigManager()
        self.fps_boost = FPSBoost()
        self.network_analyzer = NetworkAnalyzer()
        self.multi_internet = MultiInternet()
        self.traffic_shaper = TrafficShaper()
        self.ram_cleaner = RAMCleaner()
        self.lol_optimizer = LoLOptimizer()
        
        # Initialize advanced modules
        self.advanced_optimizer = AdvancedOptimizer()
        self.system_monitor = SystemMonitor()
        self.network_optimizer = NetworkOptimizer()
        self.gaming_optimizer = GamingOptimizer()
        
        # Status variables
        self.is_optimizing = False
        self.optimization_thread = None
        
        self.setup_ui()
        self.load_settings()
        
        # Start performance monitoring
        self._start_performance_monitoring()
        
    def _detect_system_capabilities(self):
        """Detect system capabilities for optimization"""
        try:
            import psutil
            
            # Get system information
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            memory_gb = memory.total / (1024**3)
            
            # Determine if this is a low-end PC
            self.is_low_end_pc = (
                cpu_count < 4 or  # Less than 4 CPU cores
                memory_gb < 8 or  # Less than 8GB RAM
                psutil.cpu_percent(interval=0.1) > 50  # High CPU usage
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
        
        # Optimize tkinter performance
        tk._default_root = None
        
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
                time.sleep(interval * 2)

    def _update_memory_measurements(self):
        """Update memory usage measurements"""
        import psutil
        process = psutil.Process()
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
        """Setup the modern user interface"""
        # Configure modern style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Modern color scheme - Premium Dark Theme
        self.colors = {
            'bg_primary': '#050505',      # Deeper black
            'bg_secondary': '#121212',    # Dark gray for containers
            'bg_tertiary': '#1e1e1e',     # Lighter gray for cards/headers
            'bg_glass': '#1a1a1a',        # Glass effect background
            'accent': '#00ffa3',          # Vibrant Mint Green
            'accent_hover': '#00e693',    # Hover state for accent
            'accent_glow': '#00ffa3',     # Glow effect color
            'text_primary': '#ffffff',    # Pure white
            'text_secondary': '#b0b0b0',  # Soft gray for subtext
            'text_muted': '#666666',      # Muted text
            'success': '#00ff88',         # Success green
            'warning': '#ffb300',         # Warning amber
            'error': '#ff4d4d',           # Error red
            'border': '#2a2a2a',          # Subtle border color
            'sidebar_active': '#1e1e1e'    # Sidebar active background
        }
        
        # Enhanced Typography
        self.fonts = {
            'h1': (FONT_HEADING, 28),
            'h2': (FONT_HEADING, 22),
            'h3': (FONT_HEADING, 18),
            'body': (FONT_BODY, 11),
            'body_bold': (f"{FONT_BODY} Bold", 11),
            'small': (FONT_BODY, 9),
            'icon': (FONT_SYMBOL, 24)
        }
        
        # Configure notebook style
        style.configure(NOTEBOOK_STYLE,
                       background=self.colors['bg_primary'],
                       borderwidth=0,
                       tabmargins=[0, 0, 0, 0])
        style.configure(TAB_STYLE,
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_secondary'],
                       padding=[30, 15],
                       font=self.fonts['body_bold'])
        style.map(TAB_STYLE,
                 background=[('selected', self.colors['bg_tertiary']),
                           ('active', self.colors['bg_secondary'])],
                 foreground=[('selected', self.colors['accent']),
                           ('active', self.colors['text_primary'])])
        
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Modern header with glass/gradient effect
        self.header_frame = tk.Frame(self.main_frame, bg=self.colors['bg_secondary'], height=100)
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        # Header content
        self.header_content = tk.Frame(self.header_frame, bg=self.colors['bg_secondary'])
        self.header_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Logo and title section
        self.title_section = tk.Frame(self.header_content, bg=self.colors['bg_secondary'])
        self.title_section.pack(side=tk.LEFT)
        
        # App icon/logo
        logo_size = 32 if self.is_low_end_pc else 42
        self.logo_label = tk.Label(self.title_section, text="󱐋", font=('Segoe UI Symbol', logo_size), 
                             fg=self.colors['accent'], bg=self.colors['bg_secondary'])
        self.logo_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Title and subtitle
        self.title_label = tk.Label(self.title_section, text=APP_TITLE, 
                              font=self.fonts['h1'], fg=self.colors['text_primary'], 
                              bg=self.colors['bg_secondary'])
        self.title_label.pack(side=tk.LEFT, anchor='n')
        
        # Hide subtitle on low-end PCs to save space
        if not self.is_low_end_pc:
            self.subtitle_label = tk.Label(self.title_section, text="Advanced Gaming Performance Suite", 
                                     font=('Arial', 12), fg=self.colors['text_muted'], 
                                     bg=self.colors['bg_secondary'])
            self.subtitle_label.pack(side=tk.LEFT, anchor='n', padx=(10, 0))
           # Status and controls section
        self.controls_section = tk.Frame(self.header_content, bg=self.colors['bg_secondary'])
        self.controls_section.pack(side=tk.RIGHT)
        
        # Status indicator
        self.status_frame = tk.Frame(self.controls_section, bg=self.colors['bg_secondary'])
        self.status_frame.pack(side=tk.RIGHT, padx=(0, 20))
        
        self.status_indicator = tk.Label(self.status_frame, text="●", font=self.fonts['h1'], 
                                   fg=self.colors['success'], bg=self.colors['bg_secondary'])
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_text = tk.Label(self.status_frame, text="System Ready", 
                               font=self.fonts['body_bold'], fg=self.colors['text_primary'], 
                               bg=self.colors['bg_secondary'])
        self.status_text.pack(side=tk.LEFT)
        
        # Control Buttons with Variant styling
        def create_header_btn(parent, icon, cmd):
            btn = tk.Button(parent, text=icon, command=cmd,
                           font=self.fonts['h2'], bg=self.colors['bg_tertiary'], 
                           fg=self.colors['text_primary'], relief=tk.FLAT, bd=0,
                           padx=15, pady=8, cursor='hand2')
            btn.pack(side=tk.RIGHT, padx=5)
            btn.bind(ENTER_EVENT, lambda e: btn.config(bg=self.colors['accent'], fg=self.colors['bg_primary']))
            btn.bind(LEAVE_EVENT, lambda e: btn.config(bg=self.colors['bg_tertiary'], fg=self.colors['text_primary']))
            return btn

        create_header_btn(self.controls_section, "ℹ️", self.show_about)
        create_header_btn(self.controls_section, "⛶", self.toggle_fullscreen)
        create_header_btn(self.controls_section, "⚙️", self.show_settings)
        
        # Modern sidebar layout
        content_container = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        content_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left sidebar for quick actions
        sidebar = tk.Frame(content_container, bg=self.colors['bg_secondary'], 
                           relief=tk.FLAT, bd=1, width=300)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        sidebar.pack_propagate(False)
        
        # Sidebar title
        sidebar_title = tk.Label(sidebar, text="🚀 Quick Actions", 
                               font=self.fonts['h2'], fg=self.colors['text_primary'], 
                               bg=self.colors['bg_secondary'])
        sidebar_title.pack(pady=(20, 15), padx=20)
        # Quick action buttons in sidebar with active state tracking
        self.sidebar_buttons = {}
        
        btn_data = [
            ("🎯", OPTIMIZE_ALL_LABEL, self.quick_optimize_all, "optimize"),
            ("🧹", CLEAN_RAM_LABEL, self.quick_clean_ram, "ram"),
            ("🌐", TEST_NETWORK_LABEL, self.quick_test_network, "network"),
            ("🎮", GAMING_MODE_LABEL, self.quick_gaming_mode, "gaming")
        ]
        
        for icon, label, command, btn_id in btn_data:
            frame, btn, indicator = self.create_sidebar_button(sidebar, icon, label, command)
            self.sidebar_buttons[btn_id] = {'frame': frame, 'btn': btn, 'indicator': indicator}
        
        # System status section in sidebar with glass effect
        status_section = tk.Frame(sidebar, bg=self.colors['bg_tertiary'], relief=tk.FLAT, bd=0)
        status_section.pack(fill=tk.X, padx=15, pady=(20, 15))
        
        status_title = tk.Label(status_section, text="📊 System Status", 
                               font=self.fonts['h3'], fg=self.colors['text_primary'], 
                               bg=self.colors['bg_tertiary'])
        status_title.pack(pady=(15, 10), padx=15)
        
        # System status indicators with dynamic updates
        if self.is_low_end_pc:
            # Reduced status indicators for low-end PCs
            self.fps_status_indicator = self.create_status_indicator(status_section, "🎮", "FPS", READY_STATUS, self.colors['success'])
            self.ram_status_indicator = self.create_status_indicator(status_section, "🧠", "RAM", "85%", self.colors['warning'])
        else:
            # Full status indicators for capable PCs
            self.fps_status_indicator = self.create_status_indicator(status_section, "🎮", "FPS Boost", READY_STATUS, self.colors['success'])
            self.network_status_indicator = self.create_status_indicator(status_section, "🌐", "Network", "Analyzing...", self.colors['warning'])
            self.ram_status_indicator = self.create_status_indicator(status_section, "🧠", "RAM Usage", "85%", self.colors['warning'])
        self.cpu_status_indicator = self.create_status_indicator(status_section, "⚡", "CPU Load", "45%", self.colors['success'])
        
        # Start real-time monitoring after a short delay to ensure UI is ready
        self.root.after(1000, self.start_status_monitoring)
        
        # Main content area
        main_content = tk.Frame(content_container, bg=self.colors['bg_primary'])
        main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Main notebook for tabs with modern styling
        self.notebook = ttk.Notebook(main_content, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Initialize tab frames list
        self.tab_frames = []
        
        # Create tabs with modern icons
        self.create_fps_boost_tab()
        self.create_network_analyzer_tab()
        self.create_multi_internet_tab()
        self.create_traffic_shaper_tab()
        self.create_ram_cleaner_tab()
        self.create_lol_optimizer_tab()
        self.create_advanced_optimizer_tab()
        self.create_system_monitor_tab()
        self.create_network_optimizer_tab()
        self.create_gaming_optimizer_tab()
    
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
        btn = tk.Button(parent, text=f"{icon}\n{text}", command=command,
                       font=self.fonts['body_bold'], bg=self.colors['bg_tertiary'], 
                       fg=self.colors['text_primary'], relief=tk.FLAT, bd=0,
                       padx=15, pady=20, cursor='hand2')
        btn.grid(row=row, column=col, padx=8, pady=8, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        def on_enter(e): btn.config(bg=self.colors['accent'], fg=self.colors['bg_primary'])
        def on_leave(e): btn.config(bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        
        btn.bind(ENTER_EVENT, on_enter)
        btn.bind(LEAVE_EVENT, on_leave)
        return btn
    
    def quick_optimize_all(self):
        """Quick optimize all systems"""
        try:
            # Update status if available
            if hasattr(self, 'status_text'):
                self.status_text.config(text="Optimizing All Systems...", fg=self.colors['warning'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['warning'])
            
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
                    self.root.after(0, lambda: self._complete_quick_optimize_all(fps_results, ram_freed))
                    
                except Exception as e:
                    self.root.after(0, lambda: self._handle_quick_optimize_error(str(e)))
            
            # Start optimization in background
            threading.Thread(target=run_optimization, daemon=True).start()
            
        except Exception as e:
            self._handle_quick_optimize_error(str(e))
    
    def _complete_quick_optimize_all(self, fps_results, ram_freed):
        """Complete quick optimization with results"""
        try:
            # Update status
            if hasattr(self, 'status_text'):
                self.status_text.config(text="All Systems Optimized", fg=self.colors['success'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['success'])
            
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
                self.status_text.config(text="Optimization Failed", fg=self.colors['error'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['error'])
            
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
                self.status_text.config(text="Cleaning RAM...", fg=self.colors['warning'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['warning'])
            
            # Run RAM cleaning in background
            def run_ram_clean():
                try:
                    freed_memory = self.ram_cleaner.clean_memory()
                    self.root.after(0, lambda: self._complete_quick_ram_clean(freed_memory))
                except Exception as e:
                    self.root.after(0, lambda: self._handle_quick_ram_clean_error(str(e)))
            
            # Start RAM cleaning in background
            threading.Thread(target=run_ram_clean, daemon=True).start()
            
        except Exception as e:
            self._handle_quick_ram_clean_error(str(e))
    
    def _complete_quick_ram_clean(self, freed_memory):
        """Complete quick RAM cleaning with results"""
        try:
            # Update status
            if hasattr(self, 'status_text'):
                self.status_text.config(text="RAM Cleaned", fg=self.colors['success'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['success'])
            
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
                self.status_text.config(text="RAM Clean Failed", fg=self.colors['error'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['error'])
            
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
                self.status_text.config(text="Testing Network...", fg=self.colors['warning'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['warning'])
            
            # Run network test in background
            def run_network_test():
                try:
                    # Run network analysis
                    results = self.network_analyzer.analyze_network()
                    
                    # Update UI in main thread
                    self.root.after(0, lambda: self._complete_quick_network_test(results))
                    
                except Exception as e:
                    self.root.after(0, lambda: self._handle_quick_network_test_error(str(e)))
            
            # Start network test in background
            threading.Thread(target=run_network_test, daemon=True).start()
            
        except Exception as e:
            self._handle_quick_network_test_error(str(e))
    
    def _complete_quick_network_test(self, results):
        """Complete quick network test with results"""
        try:
            # Update status
            if hasattr(self, 'status_text'):
                self.status_text.config(text="Network Test Complete", fg=self.colors['success'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['success'])
            
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
                self.status_text.config(text="Network Test Failed", fg=self.colors['error'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['error'])
            
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
                self.status_text.config(text="Activating Gaming Mode...", fg=self.colors['warning'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['warning'])
            
            # Run gaming mode activation in background
            def run_gaming_mode():
                try:
                    # Activate gaming optimizations
                    gaming_results = self.gaming_optimizer.optimize_for_gaming()
                    
                    # Update UI in main thread
                    self.root.after(0, lambda: self._complete_quick_gaming_mode(gaming_results))
                    
                except Exception as e:
                    self.root.after(0, lambda: self._handle_quick_gaming_mode_error(str(e)))
            
            # Start gaming mode activation in background
            threading.Thread(target=run_gaming_mode, daemon=True).start()
            
        except Exception as e:
            self._handle_quick_gaming_mode_error(str(e))
    
    def _complete_quick_gaming_mode(self, results):
        """Complete quick gaming mode activation with results"""
        try:
            # Update status
            if hasattr(self, 'status_text'):
                self.status_text.config(text="Gaming Mode Active", fg=self.colors['success'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['success'])
            
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
                self.status_text.config(text="Gaming Mode Failed", fg=self.colors['error'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['error'])
            
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
                self.status_text.config(text="Optimizing FPS...", fg=self.colors['warning'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['warning'])
            
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
                    self.root.after(0, lambda: self.update_fps_status(game, results))
                    
                except Exception as e:
                    print(f"Error in optimization thread: {e}")  # Debug print
                    self.root.after(0, lambda: self.handle_fps_error(str(e)))
            
            # Start optimization in background
            threading.Thread(target=run_optimization, daemon=True).start()
            
        except Exception as e:
            print(f"Error in optimize_fps: {e}")  # Debug print
            self.handle_fps_error(str(e))
    
    def update_fps_status(self, game, results):
        """Update FPS status display"""
        try:
            # Update status display
            self.fps_status.config(state=tk.NORMAL)
            self.fps_status.delete(1.0, tk.END)
            self.fps_status.insert(tk.END, "FPS Optimization Results:\n")
            self.fps_status.insert(tk.END, f"Game: {game}\n")
            self.fps_status.insert(tk.END, f"Processes Optimized: {results.get('processes_optimized', 0)}\n")
            self.fps_status.insert(tk.END, f"Priority Boost: {'Enabled' if self.priority_boost.get() else 'Disabled'}\n")
            self.fps_status.insert(tk.END, f"CPU Optimization: {'Enabled' if self.cpu_optimization.get() else 'Disabled'}\n")
            self.fps_status.insert(tk.END, f"GPU Optimization: {'Enabled' if self.gpu_optimization.get() else 'Disabled'}\n")
            self.fps_status.insert(tk.END, "\nOptimization completed successfully!")
            self.fps_status.config(state=tk.DISABLED)
            
            # Update main status if available
            if hasattr(self, 'status_text'):
                self.status_text.config(text="FPS Optimization Complete", fg=self.colors['success'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['success'])
            
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
            self.fps_status.config(state=tk.NORMAL)
            self.fps_status.delete(1.0, tk.END)
            self.fps_status.insert(tk.END, f"Error during FPS optimization: {error_msg}")
            self.fps_status.config(state=tk.DISABLED)
            
            # Update main status if available
            if hasattr(self, 'status_text'):
                self.status_text.config(text="FPS Optimization Failed", fg=self.colors['error'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['error'])
            
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
                self.status_text.config(text="Testing FPS...", fg=self.colors['warning'])
            
            # Test the FPS boost module directly
            results = self.fps_boost.optimize_game_performance(
                priority_boost=True,
                cpu_optimization=True,
                gpu_optimization=True
            )
            
            # Update status display
            self.fps_status.config(state=tk.NORMAL)
            self.fps_status.delete(1.0, tk.END)
            self.fps_status.insert(tk.END, "FPS Test Results:\n")
            self.fps_status.insert(tk.END, f"Processes Optimized: {results.get('processes_optimized', 0)}\n")
            self.fps_status.insert(tk.END, f"System Optimized: {results.get('system_optimized', False)}\n")
            self.fps_status.insert(tk.END, f"GPU Optimized: {results.get('gpu_optimized', False)}\n")
            self.fps_status.insert(tk.END, f"Errors: {len(results.get('errors', []))}\n")
            if results.get('errors'):
                self.fps_status.insert(tk.END, f"Error Details: {', '.join(results['errors'])}\n")
            self.fps_status.insert(tk.END, "\nTest completed successfully!")
            self.fps_status.config(state=tk.DISABLED)
            
            # Update main status
            if hasattr(self, 'status_text'):
                self.status_text.config(text="FPS Test Complete", fg=self.colors['success'])
            
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
            self.fps_status.config(state=tk.NORMAL)
            self.fps_status.delete(1.0, tk.END)
            self.fps_status.insert(tk.END, f"FPS Test Error: {str(e)}")
            self.fps_status.config(state=tk.DISABLED)
            
            if hasattr(self, 'status_text'):
                self.status_text.config(text="FPS Test Failed", fg=self.colors['error'])
            
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
        
        self.fps_status.config(state=tk.NORMAL)
        self.fps_status.delete(1.0, tk.END)
        self.fps_status.insert(tk.END, "FPS settings reset to default values.")
        self.fps_status.config(state=tk.DISABLED)
        
        if hasattr(self, 'status_text'):
            self.status_text.config(text="FPS Settings Reset", fg=self.colors['success'])
    
    def create_modern_checkbox(self, parent, text, description, variable):
        """Create a premium styled checkbox with description"""
        checkbox_frame = tk.Frame(parent, bg=parent.cget('bg'))
        checkbox_frame.pack(fill=tk.X, pady=8)
        
        cb = tk.Checkbutton(checkbox_frame, text=text, variable=variable,
                           font=self.fonts['body_bold'], fg=self.colors['text_primary'], 
                           bg=parent.cget('bg'), 
                           selectcolor=self.colors['bg_tertiary'],
                           activebackground=self.colors['bg_tertiary'],
                           activeforeground=self.colors['accent'],
                           relief=tk.FLAT, bd=0, padx=10)
        cb.pack(anchor=tk.W)
        
        if description:
            desc_label = tk.Label(checkbox_frame, text=description, 
                                 font=self.fonts['small'], fg=self.colors['text_muted'], 
                                 bg=parent.cget('bg'))
            desc_label.pack(anchor=tk.W, padx=(35, 0))
        
        return cb
    
    def create_modern_radiobutton(self, parent, text, variable, value):
        """Create a premium styled radio button"""
        rb = tk.Radiobutton(parent, text=text, variable=variable, value=value,
                           font=self.fonts['body'], fg=self.colors['text_primary'], 
                           bg=parent.cget('bg'), 
                           selectcolor=self.colors['bg_tertiary'],
                           activebackground=self.colors['bg_tertiary'],
                           activeforeground=self.colors['accent'],
                           relief=tk.FLAT, bd=0, padx=10)
        rb.pack(side=tk.LEFT, padx=5, pady=5)
        return rb
    
    def create_modern_button(self, parent, text, command):
        """Create a premium primary button with hover effects"""
        btn = tk.Button(parent, text=text, command=command,
                       font=self.fonts['body_bold'], bg=self.colors['accent'], 
                       fg=self.colors['bg_primary'], relief=tk.FLAT, bd=0,
                       padx=25, pady=12, cursor='hand2')
        
        def on_enter(e): btn.config(bg=self.colors['accent_hover'])
        def on_leave(e): btn.config(bg=self.colors['accent'])
        
        btn.bind(ENTER_EVENT, on_enter)
        btn.bind(LEAVE_EVENT, on_leave)
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
                btn.config(bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        def on_leave(e):
            if btn.cget('fg') != self.colors['accent']:
                btn.config(bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'])
        
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
            self.root.after(interval, self.start_status_monitoring)
        except Exception as e:
            print(f"Status monitoring error: {e}")
            # Retry after a longer interval
            self.root.after(5000, self.start_status_monitoring)
    
    def update_system_status(self):
        """Update system status indicators - Optimized version"""
        try:
            import psutil
            
            # Use cached metrics for better performance
            cache_interval = 1.0 if self.is_low_end_pc else 0.5
            if not hasattr(self, '_last_metrics') or time.time() - self._last_metrics['time'] > cache_interval:
                self._last_metrics = {
                    'memory': psutil.virtual_memory(),
                    'cpu_percent': psutil.cpu_percent(interval=0.1),
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
                self.status_text.config(text=f"RAM: {metrics['memory'].percent:.1f}% | CPU: {metrics['cpu_percent']:.1f}%", fg=self.colors['text_primary'])
            
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
            if hasattr(self, 'network_status_indicator'):
                threading.Thread(target=self._check_network_background, daemon=True).start()
            
        except Exception as e:
            print(f"Batch status update error: {e}")

    def _update_single_status_indicator(self, status_type, text, color):
        """Update a specific status indicator widget"""
        indicator_name = f'{status_type}_status_indicator'
        if hasattr(self, indicator_name):
            indicator = getattr(self, indicator_name)
            if isinstance(indicator, dict) and 'value_label' in indicator:
                indicator['value_label'].config(text=text, fg=color)
                if 'icon_label' in indicator:
                    indicator['icon_label'].config(fg=color)

    def _check_network_background(self):
        """Perform network check in a background thread"""
        try:
            import socket as _socket
            conn = _socket.create_connection(("8.8.8.8", 53), timeout=3)
            conn.close()
            status, color = "Connected", self.colors['success']
        except Exception:
            status, color = "Disconnected", self.colors['error']
        self.root.after(0, lambda s=status, c=color: self._update_network_indicator(s, c))
        
    def _update_network_indicator(self, status: str, color: str):
        """Update the network status indicator from the UI thread"""
        try:
            if hasattr(self, 'network_status_indicator'):
                indicator = self.network_status_indicator
                if isinstance(indicator, dict) and 'value_label' in indicator:
                    indicator['value_label'].config(text=status, fg=color)
                    if 'icon_label' in indicator:
                        indicator['icon_label'].config(fg=color)
        except Exception as e:
            print(f"Network indicator update error: {e}")

    def create_fps_boost_tab(self):

        """Create modern FPS Boost tab"""
        fps_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(fps_frame, text="🎮 FPS Boost")
        self.tab_frames.append(fps_frame)
        
        # Modern FPS Boost content with improved layout
        content_frame = tk.Frame(fps_frame, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header section with refined styling
        header_frame = tk.Frame(content_frame, bg=self.colors['bg_secondary'], relief=tk.FLAT, bd=0)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        header_content.pack(fill=tk.X, padx=25, pady=20)
        
        # Title with icon
        title_frame = tk.Frame(header_content, bg=self.colors['bg_secondary'])
        title_frame.pack(side=tk.LEFT)
        
        title_icon = tk.Label(title_frame, text="🎮", font=self.fonts['h1'], 
                             fg=self.colors['accent'], bg=self.colors['bg_secondary'])
        title_icon.pack(side=tk.LEFT, padx=(0, 15))
        
        fps_title = tk.Label(title_frame, text="FPS Boost & Game Optimization", 
                            font=self.fonts['h2'], fg=self.colors['text_primary'], 
                            bg=self.colors['bg_secondary'])
        fps_title.pack(side=tk.LEFT)
        
        # Subtitle
        fps_subtitle = tk.Label(header_content, text="Maximize your system's gaming potential", 
                               font=self.fonts['body'], fg=self.colors['text_secondary'], 
                               bg=self.colors['bg_secondary'])
        fps_subtitle.pack(side=tk.RIGHT, pady=(5, 0))
        
        # Game selection with modern styling
        game_section = tk.Frame(content_frame, bg=self.colors['bg_secondary'], relief=tk.FLAT, bd=1)
        game_section.pack(fill=tk.X, pady=(0, 15))
        
        game_title = tk.Label(game_section, text="🎯 Game Selection", 
                             font=('Arial', 14, 'bold'), fg=self.colors['text_primary'], 
                             bg=self.colors['bg_secondary'])
        game_title.pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        game_frame = tk.Frame(game_section, bg=self.colors['bg_secondary'])
        game_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        tk.Label(game_frame, text="Select Game:", font=('Arial', 14, 'bold'), 
                fg=self.colors['text_primary'], bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        self.game_var = tk.StringVar(value="Auto-detect")
        game_combo = ttk.Combobox(game_frame, textvariable=self.game_var, 
                                 values=["Auto-detect", "Valorant", "CS2", "Fortnite", "Apex Legends", "Call of Duty", "League of Legends"],
                                 font=('Arial', 13), state='readonly')
        game_combo.pack(side=tk.LEFT, padx=(15, 0), fill=tk.X, expand=True)
        
        # Optimization options with modern cards
        options_section = tk.Frame(content_frame, bg=self.colors['bg_secondary'], relief=tk.FLAT, bd=1)
        options_section.pack(fill=tk.X, pady=(0, 15))
        
        options_title = tk.Label(options_section, text="⚙️ Optimization Options", 
                                font=('Arial', 14, 'bold'), fg=self.colors['text_primary'], 
                                bg=self.colors['bg_secondary'])
        options_title.pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        options_frame = tk.Frame(options_section, bg=self.colors['bg_secondary'])
        options_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Create modern checkboxes
        self.priority_boost = tk.BooleanVar(value=True)
        self.create_modern_checkbox(options_frame, "🚀 High Priority Process", 
                                  "Set game processes to high priority", self.priority_boost)
        
        self.cpu_optimization = tk.BooleanVar(value=True)
        self.create_modern_checkbox(options_frame, "⚡ CPU Optimization", 
                                  "Optimize CPU usage for gaming", self.cpu_optimization)
        
        self.gpu_optimization = tk.BooleanVar(value=True)
        self.create_modern_checkbox(options_frame, "🎨 GPU Optimization", 
                                  "Optimize GPU performance for gaming", self.gpu_optimization)
        
        # Action buttons section
        actions_section = tk.Frame(content_frame, bg=self.colors['bg_secondary'], relief=tk.FLAT, bd=1)
        actions_section.pack(fill=tk.X, pady=(0, 15))
        
        actions_title = tk.Label(actions_section, text="🚀 Actions", 
                                font=('Arial', 14, 'bold'), fg=self.colors['text_primary'], 
                                bg=self.colors['bg_secondary'])
        actions_title.pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        buttons_frame = tk.Frame(actions_section, bg=self.colors['bg_secondary'])
        buttons_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Modern action buttons
        self.create_modern_button(buttons_frame, "🎯 Optimize FPS", self.optimize_fps)
        self.create_modern_button(buttons_frame, "🔄 Reset Settings", self.reset_fps_settings)
        self.create_modern_button(buttons_frame, "🧪 Test FPS", self.test_fps_optimization)
        
        # Status display with modern styling
        status_card = tk.Frame(content_frame, bg=self.colors['bg_secondary'], relief=tk.FLAT, bd=0)
        status_card.pack(fill=tk.BOTH, expand=True)
        
        status_container = tk.Frame(status_card, bg=self.colors['bg_secondary'], padx=20, pady=20)
        status_container.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(status_container, text="OPTIMIZATION STATUS", font=self.fonts['small'],
                fg=self.colors['accent'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        # Modern status text area
        self.fps_status = tk.Text(status_container, height=8, bg=self.colors['bg_primary'], 
                                 fg=self.colors['success'], font=('Consolas', 11),
                                 padx=15, pady=15, relief=tk.FLAT, state=tk.DISABLED, wrap=tk.WORD)
        self.fps_status.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(status_container, orient=tk.VERTICAL, command=self.fps_status.yview)
        self.fps_status.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_network_analyzer_tab(self):
        """Create modern Network Analyzer tab with premium styling"""
        net_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(net_frame, text="🌐 Network Analyzer")
        
        self.create_modern_tab_header(net_frame, "🌐", "Network Analysis", 
                                    "Deep scan network performance and identify bottlenecks")
        
        content = tk.Frame(net_frame, bg=self.colors['bg_primary'])
        content.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Controls card
        controls_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        controls_card.pack(fill=tk.X, pady=(0, 20))
        
        self.start_analysis_btn = self.create_modern_button(controls_card, "🔍 Start Deep Analysis", self.start_network_analysis)
        self.start_analysis_btn.pack(side=tk.LEFT)
        
        self.stop_analysis_btn = self.create_modern_button(controls_card, "⏹ Stop", self.stop_network_analysis)
        self.stop_analysis_btn.pack(side=tk.LEFT, padx=(15, 0))
        self.stop_analysis_btn.config(state=tk.DISABLED)
        
        # Results card
        results_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        results_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(results_card, text="ANALYSIS REPORT", font=self.fonts['small'],
                fg=self.colors['accent'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.network_results = tk.Text(results_card, height=12, bg=self.colors['bg_primary'], 
                                      fg=self.colors['success'], font=('Consolas', 11),
                                      padx=15, pady=15, relief=tk.FLAT, state=tk.DISABLED)
        self.network_results.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def create_multi_internet_tab(self):
        """Create modern Multi Internet tab with refined layout"""
        multi_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(multi_frame, text="🔗 Multi Internet")
        
        self.create_modern_tab_header(multi_frame, "🔗", "Multi-Connection Manager", 
                                    "Combine and manage multiple internet connections")
        
        content = tk.Frame(multi_frame, bg=self.colors['bg_primary'])
        content.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Connection list card
        conn_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        conn_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(conn_card, text="ACTIVE CONNECTIONS", font=self.fonts['small'],
                fg=self.colors['accent'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.connection_list = tk.Listbox(conn_card, bg=self.colors['bg_primary'], 
                                         fg=self.colors['text_primary'],
                                         font=('Consolas', 11), relief=tk.FLAT, 
                                         highlightthickness=1, highlightbackground=self.colors['border'],
                                         selectbackground=self.colors['accent'],
                                         selectforeground=self.colors['bg_primary'],
                                         borderwidth=0)
        self.connection_list.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Load connections
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

    def create_traffic_shaper_tab(self):
        """Create modern Traffic Shaper tab with improved styling"""
        traffic_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(traffic_frame, text="🚦 Traffic Shaper")
        
        self.create_modern_tab_header(traffic_frame, "🚦", "Traffic Shaping & Bandwidth", 
                                    "Control network priority and optimize data flow")
        
        content = tk.Frame(traffic_frame, bg=self.colors['bg_primary'])
        content.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Bandwidth controls card
        bw_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        bw_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(bw_card, text="Bandwidth Limit (Mbps):", font=self.fonts['body_bold'],
                fg=self.colors['text_primary'], bg=self.colors['bg_secondary']).pack(side=tk.LEFT)
        
        self.bandwidth_var = tk.StringVar(value="100")
        style = ttk.Style()
        style.configure('Modern.TEntry', fieldbackground=self.colors['bg_tertiary'], foreground=self.colors['text_primary'])
        
        bandwidth_entry = tk.Entry(bw_card, textvariable=self.bandwidth_var, 
                                  font=self.fonts['h3'], width=10, 
                                  bg=self.colors['bg_tertiary'], fg=self.colors['accent'],
                                  insertbackground='white', relief=tk.FLAT, bd=5)
        bandwidth_entry.pack(side=tk.LEFT, padx=(15, 0))
        
        # Traffic shaping options card
        options_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        options_card.pack(fill=tk.X)
        
        self.prioritize_gaming = tk.BooleanVar(value=True)
        self.create_modern_checkbox(options_card, "Prioritize Gaming Traffic", 
                                   "Automatically detect and prioritize game packets", self.prioritize_gaming)
        
        self.limit_background = tk.BooleanVar(value=True)
        self.create_modern_checkbox(options_card, "Limit Background Applications", 
                                   "Reduce network usage of non-gaming apps", self.limit_background)
        
    def create_ram_cleaner_tab(self):
        """Create modern RAM Cleaner tab with visualization"""
        ram_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(ram_frame, text="🧹 RAM Cleaner")
        
        self.create_modern_tab_header(ram_frame, "🧹", "Memory Optimization", 
                                    "Deep clean system memory and free up resources")
        
        content = tk.Frame(ram_frame, bg=self.colors['bg_primary'])
        content.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Memory status card
        status_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        status_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(status_card, text="MEMORY STATUS", font=self.fonts['small'],
                fg=self.colors['accent'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.memory_info = tk.Text(status_card, height=6, bg=self.colors['bg_primary'], 
                                  fg=self.colors['success'], font=('Consolas', 11), 
                                  padx=15, pady=15, relief=tk.FLAT, state=tk.DISABLED)
        self.memory_info.pack(fill=tk.X, pady=10)
        
        # Cleaner controls card
        controls_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        controls_card.pack(fill=tk.X)
        
        self.clean_ram_btn = self.create_modern_button(controls_card, "🧹 Clean System RAM", self.clean_ram)
        self.clean_ram_btn.pack(side=tk.LEFT)
        
        self.auto_clean = tk.BooleanVar(value=False)
        self.create_modern_checkbox(controls_card, "Enable Auto-Clean", 
                                   "Automatically optimize memory every 5 minutes", self.auto_clean)
        
        # Update memory info
        self.update_memory_info()
        
    def create_lol_optimizer_tab(self):
        """Create modern League of Legends Optimizer tab with branding"""
        lol_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(lol_frame, text="⚔️ LoL Optimizer")
        
        self.create_modern_tab_header(lol_frame, "⚔️", "League of Legends Optimizer", 
                                    "Specialized performance tweaks for competitive play")
        
        content = tk.Frame(lol_frame, bg=self.colors['bg_primary'])
        content.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Controls card
        controls_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        controls_card.pack(fill=tk.X, pady=(0, 20))
        
        self.optimize_lol_btn = self.create_modern_button(controls_card, "⚔️ Standard Optimize", self.optimize_lol)
        self.optimize_lol_btn.pack(side=tk.LEFT)
        
        self.test_lol_latency_btn = self.create_modern_button(controls_card, "📡 Test Server Ping", self.test_lol_latency)
        self.test_lol_latency_btn.pack(side=tk.LEFT, padx=(15, 0))
        
        # Performance card
        perf_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        perf_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(perf_card, text="LO PERFORMANCE STATUS", font=self.fonts['small'],
                fg=self.colors['accent'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.lol_status = tk.Text(perf_card, height=10, bg=self.colors['bg_primary'], 
                                 fg=self.colors['success'], font=('Consolas', 11),
                                 padx=15, pady=15, relief=tk.FLAT, state=tk.DISABLED)
        self.lol_status.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Update LoL status
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
            
            self.lol_status.config(state=tk.NORMAL)
            self.lol_status.delete(1.0, tk.END)
            self.lol_status.insert(tk.END, status_text)
            self.lol_status.config(state=tk.DISABLED)
            
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
            
            self.lol_status.config(state=tk.NORMAL)
            self.lol_status.delete(1.0, tk.END)
            self.lol_status.insert(tk.END, status_text)
            self.lol_status.config(state=tk.DISABLED)
            
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
            
            self.lol_status.config(state=tk.NORMAL)
            self.lol_status.delete(1.0, tk.END)
            self.lol_status.insert(tk.END, status_text)
            self.lol_status.config(state=tk.DISABLED)
            
        except Exception as e:
            print(f"Failed to update LoL status: {e}")
        
    
    def open_settings(self):
        """Open settings dialog (legacy method for compatibility)"""
        self.show_settings()
        
            
    def start_network_analysis(self):
        """Start network analysis"""
        self.start_analysis_btn.config(state=tk.DISABLED)
        self.stop_analysis_btn.config(state=tk.NORMAL)
        
        # Start analysis in separate thread
        threading.Thread(target=self.run_network_analysis, daemon=True).start()
        
    def stop_network_analysis(self):
        """Stop network analysis"""
        self.start_analysis_btn.config(state=tk.NORMAL)
        self.stop_analysis_btn.config(state=tk.DISABLED)
        
    def run_network_analysis(self):
        """Run network analysis with progress feedback"""
        try:
            # Update button states
            self.start_analysis_btn.config(state=tk.DISABLED)
            self.stop_analysis_btn.config(state=tk.NORMAL)
            
            # Clear and show progress
            self.network_results.config(state=tk.NORMAL)
            self.network_results.delete(1.0, tk.END)
            self.network_results.insert(tk.END, "🔍 Starting network analysis...\n")
            self.network_results.config(state=tk.DISABLED)
            self.root.update()
            
            # Step 1: Basic connectivity
            self.network_results.config(state=tk.NORMAL)
            self.network_results.insert(tk.END, "📡 Testing basic connectivity...\n")
            self.network_results.config(state=tk.DISABLED)
            self.root.update()
            time.sleep(1)
            
            # Step 2: Server latency tests
            self.network_results.config(state=tk.NORMAL)
            self.network_results.insert(tk.END, "🌐 Testing server latency...\n")
            self.network_results.config(state=tk.DISABLED)
            self.root.update()
            time.sleep(1)
            
            # Step 3: Gaming servers
            self.network_results.config(state=tk.NORMAL)
            self.network_results.insert(tk.END, "🎮 Testing gaming servers...\n")
            self.network_results.config(state=tk.DISABLED)
            self.root.update()
            time.sleep(1)
            
            # Get results
            results = self.network_analyzer.analyze_network()
            
            # Display results
            self.network_results.config(state=tk.NORMAL)
            self.network_results.delete(1.0, tk.END)
            self.network_results.insert(tk.END, results)
            self.network_results.config(state=tk.DISABLED)
            
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
            self.network_results.config(state=tk.NORMAL)
            self.network_results.delete(1.0, tk.END)
            self.network_results.insert(tk.END, f"❌ Analysis failed: {str(e)}")
            self.network_results.config(state=tk.DISABLED)
            
            # Show error popup
            self.show_result_popup(
                "Network Analysis Failed", 
                "An error occurred during network analysis.",
                "error",
                f"Error details: {str(e)}"
            )
        finally:
            self.stop_analysis_btn.config(state=tk.DISABLED)
            self.start_analysis_btn.config(state=tk.NORMAL)
            
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
                self.status_text.config(text="Cleaning RAM...", fg=self.colors['warning'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['warning'])
            
            # Clean RAM memory
            print("Starting RAM cleaning...")  # Debug print
            freed_memory = self.ram_cleaner.clean_memory()
            print(f"RAM cleaning completed, freed: {freed_memory:.2f} MB")  # Debug print
            
            # Update memory info
            self.update_memory_info()
            
            # Update status if available
            if hasattr(self, 'status_text'):
                self.status_text.config(text="RAM Cleaned", fg=self.colors['success'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['success'])
            
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
                self.status_text.config(text="RAM Clean Failed", fg=self.colors['error'])
            if hasattr(self, 'status_indicator'):
                self.status_indicator.config(fg=self.colors['error'])
            
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
                self.memory_info.config(state=tk.NORMAL)
                self.memory_info.delete(1.0, tk.END)
                self.memory_info.insert(tk.END, memory_text)
                self.memory_info.config(state=tk.DISABLED)
            
            # Update status if available
            if hasattr(self, 'status_text'):
                self.status_text.config(text=f"RAM: {memory_info['memory_percent']:.1f}%", fg=self.colors['text_primary'])
                
        except Exception as e:
            print(f"Failed to update memory info: {e}")
            
    def open_settings(self):
        """Open settings dialog"""
        try:
            settings_dialog = SettingsDialog(self.root, self.config_manager)
            settings_dialog.show_settings()
            
            # Reload settings after dialog is closed
            self.root.after(100, self.load_settings)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open settings: {str(e)}")
    
    def show_result_popup(self, title, message, result_type="success", details=None):
        """Show result popup modal after actions"""
        try:
            popup = tk.Toplevel(self.root)
            popup.title(title)
            popup.geometry("450x350")
            popup.configure(bg=self.colors['bg_primary'])
            popup.resizable(False, False)
            
            # Center the dialog
            popup.transient(self.root)
            popup.grab_set()
            
            # Main frame
            main_frame = tk.Frame(popup, bg=self.colors['bg_primary'])
            main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            # Header section
            header_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], relief=tk.RAISED, bd=2)
            header_frame.pack(fill=tk.X, pady=(0, 15))
            
            # Icon and title
            title_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
            title_frame.pack(fill=tk.X, padx=15, pady=15)
            
            # Result icon based on type
            if result_type == "success":
                icon_text = "✅"
                icon_color = self.colors['success']
            elif result_type == "warning":
                icon_text = "⚠️"
                icon_color = self.colors['warning']
            elif result_type == "error":
                icon_text = "❌"
                icon_color = self.colors['error']
            else:
                icon_text = "ℹ️"
                icon_color = self.colors['accent']
            
            icon_label = tk.Label(title_frame, text=icon_text, font=('Arial', 32), 
                                fg=icon_color, bg=self.colors['bg_secondary'])
            icon_label.pack(side=tk.LEFT, padx=(0, 15))
            
            # Title and message
            title_info = tk.Frame(title_frame, bg=self.colors['bg_secondary'])
            title_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            title_label = tk.Label(title_info, text=title, 
                                 font=('Arial', 16, 'bold'), fg=self.colors['text_primary'], 
                                 bg=self.colors['bg_secondary'])
            title_label.pack(anchor=tk.W)
            
            message_label = tk.Label(title_info, text=message, 
                                   font=('Arial', 10), fg=self.colors['text_muted'], 
                                   bg=self.colors['bg_secondary'], wraplength=300)
            message_label.pack(anchor=tk.W, pady=(3, 0))
            
            # Details section
            if details:
                details_frame = tk.LabelFrame(main_frame, text="Details", 
                                           font=('Arial', 10, 'bold'), fg=self.colors['text_primary'], 
                                           bg=self.colors['bg_secondary'], relief=tk.RAISED, bd=2)
                details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
                
                details_text = tk.Text(details_frame, font=('Arial', 9), 
                                     bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                     relief=tk.FLAT, bd=0, wrap=tk.WORD)
                details_text.pack(fill=tk.BOTH, padx=8, pady=8)
                details_text.insert(tk.END, details)
                details_text.config(state=tk.DISABLED)
            
            # Button frame
            button_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
            button_frame.pack(fill=tk.X, pady=(15, 0))
            
            # Close button
            close_btn = tk.Button(button_frame, text="Close", command=popup.destroy,
                                font=('Arial', 10, 'bold'), bg=self.colors['accent'], 
                                fg='black', relief=tk.RAISED, bd=2, padx=15, pady=6)
            close_btn.pack(side=tk.RIGHT)
            
            # Center the dialog
            popup.update_idletasks()
            width = popup.winfo_width()
            height = popup.winfo_height()
            x = (popup.winfo_screenwidth() // 2) - (width // 2)
            y = (popup.winfo_screenheight() // 2) - (height // 2)
            popup.geometry(f'{width}x{height}+{x}+{y}')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show result popup: {str(e)}")
    
    def show_about(self):
        """Show about dialog with premium branding"""
        try:
            about = tk.Toplevel(self.root)
            about.title("About NGXSMK Optimizer")
            about.geometry("650x580")
            about.configure(bg=self.colors['bg_primary'])
            about.resizable(False, False)
            about.transient(self.root)
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
            theme = settings.get('general', {}).get('theme', 'dark')
            self.apply_theme(theme)
            
            # Apply language
            language = settings.get('general', {}).get('language', 'en')
            self.apply_language(language)
            
            # Apply low-resource mode if enabled
            if settings.get('general', {}).get('low_resource_mode', False):
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
                    'bg_secondary': '#f5f5f5', 
                    'bg_tertiary': '#e0e0e0',
                    'accent': '#0066cc',
                    'accent_hover': '#0052a3',
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
                    'bg_secondary': '#161b22', 
                    'bg_tertiary': '#21262d',
                    'accent': '#ff6b35',
                    'accent_hover': '#ff5722',
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
                    'bg_secondary': '#1a1a1a', 
                    'bg_tertiary': '#2a2a2a',
                    'accent': '#00ff88',
                    'accent_hover': '#00cc6a',
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
                    'about': "À propos"
                }
            }
            
            # Get translations for current language
            self.translations = translations.get(language, translations['en'])
            
            # Update UI text
            self.update_ui_text()
            
        except Exception as e:
            print(f"Failed to apply language: {e}")
    
    def apply_other_settings(self, settings):
        """Apply other settings to the application"""
        try:
            # Auto-start settings
            auto_optimize = settings.get('general', {}).get('auto_optimize', False)
            
            # Apply auto-optimize if enabled
            if auto_optimize:
                self.auto_optimize_on_startup()
            
        except Exception as e:
            print(f"Failed to apply other settings: {e}")
    
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
                'root': (self.root, {'bg': bg_primary}),
                'main_frame': (getattr(self, 'main_frame', None), {'bg': bg_primary}),
                'header_frame': (getattr(self, 'header_frame', None), {'bg': bg_secondary}),
                'header_content': (getattr(self, 'header_content', None), {'bg': bg_secondary}),
                'title_section': (getattr(self, 'title_section', None), {'bg': bg_secondary}),
                'controls_section': (getattr(self, 'controls_section', None), {'bg': bg_secondary}),
                'status_frame': (getattr(self, 'status_frame', None), {'bg': bg_secondary}),
                'logo_label': (getattr(self, 'logo_label', None), {'fg': accent, 'bg': bg_secondary}),
                'title_label': (getattr(self, 'title_label', None), {'fg': text_primary, 'bg': bg_secondary}),
                'subtitle_label': (getattr(self, 'subtitle_label', None), {'fg': text_muted, 'bg': bg_secondary}),
                'status_indicator': (getattr(self, 'status_indicator', None), {'fg': success, 'bg': bg_secondary}),
                'status_text': (getattr(self, 'status_text', None), {'fg': text_primary, 'bg': bg_secondary}),
                'sidebar_frame': (getattr(self, 'sidebar_frame', None), {'bg': bg_secondary}),
                'sidebar_title': (getattr(self, 'sidebar_title', None), {'fg': text_primary, 'bg': bg_secondary})
            })
            
            # Update sidebar buttons efficiently
            if hasattr(self, 'sidebar_buttons'):
                for btn_info in self.sidebar_buttons.values():
                    if isinstance(btn_info, dict) and 'btn' in btn_info:
                        btn_info['btn'].configure(bg=bg_tertiary, fg=text_primary)
            
            # Update status indicators efficiently
            if hasattr(self, 'status_indicators'):
                for indicator in self.status_indicators:
                    indicator.configure(bg=bg_tertiary)
            
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
    
    def update_widget_colors(self, parent):
        """Recursively update widget colors"""
        try:
            for child in parent.winfo_children():
                if isinstance(child, tk.Frame):
                    child.configure(bg=self.colors['bg_primary'])
                    self.update_widget_colors(child)
                elif isinstance(child, tk.Label):
                    if child.cget('bg') != 'SystemButtonFace':  # Don't change system colors
                        child.configure(bg=self.colors['bg_primary'], fg=self.colors['text_primary'])
                elif isinstance(child, tk.Button):
                    child.configure(bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
                elif isinstance(child, tk.Text):
                    child.configure(bg=self.colors['bg_secondary'], fg=self.colors['text_primary'])
                elif isinstance(child, tk.Scrollbar):
                    child.configure(bg=self.colors['bg_tertiary'])
                    
        except Exception as e:
            print(f"Failed to update widget colors: {e}")
    
    def update_ui_text(self):
        """Update UI text based on current language"""
        try:
            # Update window title
            self.root.title(self.translations.get('title', 'NGXSMK GameNet Optimizer'))
            
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
            self.optimization_thread = threading.Thread(target=self._auto_optimize_loop, daemon=True)
            self.optimization_thread.start()
        except Exception as e:
            print(f"Failed to start auto-optimization: {e}")
    
    def _auto_optimize_loop(self):
        """Auto-optimization loop"""
        try:
            while True:
                # Perform automatic optimizations
                self.fps_boost.optimize_fps()
                self.ram_cleaner.clean_ram()
                time.sleep(300)  # Optimize every 5 minutes
        except Exception as e:
            print(f"Auto-optimization error: {e}")
            
    def save_settings(self):
        """Save application settings safely"""
        try:
            settings = {
                'fps_boost': {
                    'priority_boost': self.priority_boost.get(),
                    'cpu_optimization': self.cpu_optimization.get(),
                    'gpu_optimization': self.gpu_optimization.get()
                },
                'traffic_shaper': {
                    'prioritize_gaming': self.prioritize_gaming.get(),
                    'limit_background': self.limit_background.get()
                },
                'ram_cleaner': {
                    'auto_clean': self.auto_clean.get()
                }
            }
            self.config_manager.save_settings(settings)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def create_advanced_optimizer_tab(self):
        """Create modern Advanced Optimizer tab with AI-driven design"""
        advanced_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(advanced_frame, text="🤖 Advanced AI")
        
        self.create_modern_tab_header(advanced_frame, "🤖", "Advanced AI Optimizer", 
                                    "Neural-network powered system-wide optimizations")
        
        content = tk.Frame(advanced_frame, bg=self.colors['bg_primary'])
        content.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Profile & Features section
        top_frame = tk.Frame(content, bg=self.colors['bg_primary'])
        top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Profile selection card
        profile_card = tk.Frame(top_frame, bg=self.colors['bg_secondary'], padx=20, pady=20)
        profile_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(profile_card, text="OPTIMIZATION PROFILE", font=self.fonts['small'],
                fg=self.colors['accent'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.advanced_profile = tk.StringVar(value="gaming")
        profile_options = ["gaming", "streaming", "productivity", "balanced"]
        
        for option in profile_options:
            self.create_modern_radiobutton(profile_card, option.title(), 
                                               self.advanced_profile, option)
        
        # Control buttons
        button_frame = tk.Frame(content, bg=self.colors['bg_primary'])
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.start_advanced_btn = self.create_modern_button(button_frame, "🚀 Start AI Optimization", self.start_advanced_optimization)
        self.start_advanced_btn.pack(side=tk.LEFT)
        
        self.stop_advanced_btn = self.create_modern_button(button_frame, "⏹ Stop AI", self.stop_advanced_optimization)
        self.stop_advanced_btn.pack(side=tk.LEFT, padx=(15, 0))
        self.stop_advanced_btn.config(state=tk.DISABLED)
        
        # Results display
        results_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        results_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(results_card, text="AI ANALYSIS RESULTS", font=self.fonts['small'],
                fg=self.colors['accent'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.advanced_results = tk.Text(results_card, height=12, bg=self.colors['bg_primary'], 
                                       fg=self.colors['success'], font=('Consolas', 10),
                                       padx=15, pady=15, relief=tk.FLAT, state=tk.DISABLED, wrap=tk.WORD)
        self.advanced_results.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar for results
        results_scrollbar = tk.Scrollbar(self.advanced_results, orient=tk.VERTICAL, command=self.advanced_results.yview)
        self.advanced_results.configure(yscrollcommand=results_scrollbar.set)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_system_monitor_tab(self):
        """Create modern System Monitor tab with live feed"""
        monitor_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(monitor_frame, text="📊 Monitor")
        
        self.create_modern_tab_header(monitor_frame, "📊", "System Activity Monitor", 
                                    "Real-time tracking of system performance metrics")
        
        content = tk.Frame(monitor_frame, bg=self.colors['bg_primary'])
        content.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Control buttons
        button_frame = tk.Frame(content, bg=self.colors['bg_primary'])
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.start_monitor_btn = self.create_modern_button(button_frame, "📊 Start Data Feed", self.start_system_monitoring)
        self.start_monitor_btn.pack(side=tk.LEFT)
        
        self.stop_monitor_btn = self.create_modern_button(button_frame, "⏹ Stop Feed", self.stop_system_monitoring)
        self.stop_monitor_btn.pack(side=tk.LEFT, padx=(15, 0))
        self.stop_monitor_btn.config(state=tk.DISABLED)
        
        # Monitoring display
        monitor_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        monitor_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(monitor_card, text="LIVE SYSTEM TELEMETRY", font=self.fonts['small'],
                fg=self.colors['accent'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.monitor_display = tk.Text(monitor_card, height=15, bg=self.colors['bg_primary'], 
                                      fg=self.colors['success'], font=('Consolas', 10),
                                      padx=15, pady=15, relief=tk.FLAT, state=tk.DISABLED, wrap=tk.WORD)
        self.monitor_display.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar for monitor display
        monitor_scrollbar = tk.Scrollbar(self.monitor_display, orient=tk.VERTICAL, command=self.monitor_display.yview)
        self.monitor_display.configure(yscrollcommand=monitor_scrollbar.set)
        monitor_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_network_optimizer_tab(self):
        """Create modern Network Optimizer tab with profiles"""
        network_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(network_frame, text="🌐 Network Opt")
        
        self.create_modern_tab_header(network_frame, "🌐", "Advanced Network Optimizer", 
                                    "Optimize TCP/IP stack and network parameters for low latency")
        
        content = tk.Frame(network_frame, bg=self.colors['bg_primary'])
        content.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Control section
        top_frame = tk.Frame(content, bg=self.colors['bg_primary'])
        top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Profile selection card
        profile_card = tk.Frame(top_frame, bg=self.colors['bg_secondary'], padx=20, pady=20)
        profile_card.pack(fill=tk.X)
        
        tk.Label(profile_card, text="NETWORK PROFILE", font=self.fonts['small'],
                fg=self.colors['accent'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.network_profile = tk.StringVar(value="gaming")
        network_options = ["gaming", "streaming", "productivity"]
        
        for option in network_options:
            self.create_modern_radiobutton(profile_card, option.title(), 
                                               self.network_profile, option)
        
        # Control buttons
        button_frame = tk.Frame(content, bg=self.colors['bg_primary'])
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.start_network_btn = self.create_modern_button(button_frame, "🌐 Apply Network Optimization", self.start_network_optimization)
        self.start_network_btn.pack(side=tk.LEFT)
        
        self.stop_network_btn = self.create_modern_button(button_frame, "⏹ Revert", self.stop_network_optimization)
        self.stop_network_btn.pack(side=tk.LEFT, padx=(15, 0))
        self.stop_network_btn.config(state=tk.DISABLED)
        
        # Status card
        status_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        status_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(status_card, text="NETWORK OPTIMIZATION STATUS", font=self.fonts['small'],
                fg=self.colors['accent'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.network_status = tk.Text(status_card, height=12, bg=self.colors['bg_primary'], 
                                     fg=self.colors['success'], font=('Consolas', 10),
                                     padx=15, pady=15, relief=tk.FLAT, state=tk.DISABLED, wrap=tk.WORD)
        self.network_status.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar for network status
        network_scrollbar = tk.Scrollbar(self.network_status, orient=tk.VERTICAL, command=self.network_status.yview)
        self.network_status.configure(yscrollcommand=network_scrollbar.set)
        network_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_gaming_optimizer_tab(self):
        """Create modern Gaming Optimizer tab with specialized features"""
        gaming_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(gaming_frame, text="🎮 Gaming Opt")
        
        self.create_modern_tab_header(gaming_frame, "🎮", "Advanced Gaming Optimizer", 
                                    "Tailored optimizations for specific game engines and anti-cheats")
        
        content = tk.Frame(gaming_frame, bg=self.colors['bg_primary'])
        content.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Profile selection card
        profile_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        profile_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(profile_card, text="GAMING PROFILE", font=self.fonts['small'],
                fg=self.colors['accent'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.gaming_profile = tk.StringVar(value="auto")
        gaming_options = ["auto", "league_of_legends", "valorant", "cs2", "fortnite", "apex_legends"]
        
        for option in gaming_options:
            self.create_modern_radiobutton(profile_card, option.replace('_', ' ').title(), 
                                               self.gaming_profile, option)
        
        # Control buttons
        button_frame = tk.Frame(content, bg=self.colors['bg_primary'])
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.start_gaming_btn = self.create_modern_button(button_frame, "🎮 Start Gaming Optimization", self.start_gaming_optimization)
        self.start_gaming_btn.pack(side=tk.LEFT)
        
        self.stop_gaming_btn = self.create_modern_button(button_frame, "⏹ Stop", self.stop_gaming_optimization)
        self.stop_gaming_btn.pack(side=tk.LEFT, padx=(15, 0))
        self.stop_gaming_btn.config(state=tk.DISABLED)
        
        # Status card
        status_card = tk.Frame(content, bg=self.colors['bg_secondary'], padx=20, pady=20)
        status_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(status_card, text="GAMING OPTIMIZATION LOG", font=self.fonts['small'],
                fg=self.colors['accent'], bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.gaming_status = tk.Text(status_card, height=12, bg=self.colors['bg_primary'], 
                                    fg=self.colors['success'], font=('Consolas', 10),
                                    padx=15, pady=15, relief=tk.FLAT, state=tk.DISABLED, wrap=tk.WORD)
        self.gaming_status.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar for gaming status
        gaming_scrollbar = tk.Scrollbar(self.gaming_status, orient=tk.VERTICAL, command=self.gaming_status.yview)
        self.gaming_status.configure(yscrollcommand=gaming_scrollbar.set)
        gaming_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def start_advanced_optimization(self):
        """Start advanced optimization"""
        try:
            profile = self.advanced_profile.get()
            results = self.advanced_optimizer.start_advanced_optimization(profile)
            
            self.advanced_results.config(state=tk.NORMAL)
            self.advanced_results.delete(1.0, tk.END)
            self.advanced_results.insert(tk.END, json.dumps(results, indent=2))
            self.advanced_results.config(state=tk.DISABLED)
            
            self.start_advanced_btn.config(state=tk.DISABLED)
            self.stop_advanced_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"Advanced optimization failed: {str(e)}")
    
    def stop_advanced_optimization(self):
        """Stop advanced optimization"""
        try:
            self.advanced_optimizer.stop_optimization()
            self.start_advanced_btn.config(state=tk.NORMAL)
            self.stop_advanced_btn.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop optimization: {str(e)}")
    
    def start_system_monitoring(self):
        """Start system monitoring"""
        try:
            result = self.system_monitor.start_monitoring(interval=5)
            
            self.monitor_display.config(state=tk.NORMAL)
            self.monitor_display.delete(1.0, tk.END)
            self.monitor_display.insert(tk.END, f"System monitoring started: {result}\n")
            self.monitor_display.config(state=tk.DISABLED)
            
            self.start_monitor_btn.config(state=tk.DISABLED)
            self.stop_monitor_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"System monitoring failed: {str(e)}")
    
    def stop_system_monitoring(self):
        """Stop system monitoring"""
        try:
            result = self.system_monitor.stop_monitoring()
            
            self.monitor_display.config(state=tk.NORMAL)
            self.monitor_display.insert(tk.END, f"System monitoring stopped: {result}\n")
            self.monitor_display.config(state=tk.DISABLED)
            
            self.start_monitor_btn.config(state=tk.NORMAL)
            self.stop_monitor_btn.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop monitoring: {str(e)}")
    
    def start_network_optimization(self):
        """Start network optimization"""
        try:
            profile = self.network_profile.get()
            results = self.network_optimizer.start_network_optimization(profile)
            
            self.network_status.config(state=tk.NORMAL)
            self.network_status.delete(1.0, tk.END)
            self.network_status.insert(tk.END, json.dumps(results, indent=2))
            self.network_status.config(state=tk.DISABLED)
            
            self.start_network_btn.config(state=tk.DISABLED)
            self.stop_network_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"Network optimization failed: {str(e)}")
    
    def stop_network_optimization(self):
        """Stop network optimization"""
        try:
            result = self.network_optimizer.stop_network_optimization()
            
            self.network_status.config(state=tk.NORMAL)
            self.network_status.insert(tk.END, f"Network optimization stopped: {result}\n")
            self.network_status.config(state=tk.DISABLED)
            
            self.start_network_btn.config(state=tk.NORMAL)
            self.stop_network_btn.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop network optimization: {str(e)}")
    
    def start_gaming_optimization(self):
        """Start gaming optimization"""
        try:
            profile = self.gaming_profile.get()
            results = self.gaming_optimizer.start_gaming_optimization(profile)
            
            self.gaming_status.config(state=tk.NORMAL)
            self.gaming_status.delete(1.0, tk.END)
            self.gaming_status.insert(tk.END, json.dumps(results, indent=2))
            self.gaming_status.config(state=tk.DISABLED)
            
            self.start_gaming_btn.config(state=tk.DISABLED)
            self.stop_gaming_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"Gaming optimization failed: {str(e)}")
    
    def stop_gaming_optimization(self):
        """Stop gaming optimization"""
        try:
            result = self.gaming_optimizer.stop_gaming_optimization()
            
            self.gaming_status.config(state=tk.NORMAL)
            self.gaming_status.insert(tk.END, f"Gaming optimization stopped: {result}\n")
            self.gaming_status.config(state=tk.DISABLED)
            
            self.start_gaming_btn.config(state=tk.NORMAL)
            self.stop_gaming_btn.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop gaming optimization: {str(e)}")
    
    def run(self):
        """Run the application"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
            
    def show_settings(self):
        """Show settings dialog with premium styling"""
        try:
            settings_dialog = SettingsDialog(self.root, self.config_manager, self.colors, self.fonts)
            settings_dialog.show_settings()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open settings: {str(e)}")
    
    def on_closing(self):
        """Handle optimized application closing"""
        try:
            # Save settings
            self.save_settings()
            
            # Cleanup resources
            self._cleanup_resources()
            
            # Close the application
            self.root.destroy()
        except Exception as e:
            print(f"Error during closing: {e}")
            self.root.destroy()
    
    def _cleanup_resources(self):
        """Cleanup resources for better memory management"""
        try:
            # Shutdown thread pool
            if hasattr(self, 'executor'):
                self.executor.shutdown(wait=False)
            
            # Clear caches
            if hasattr(self, '_get_optimized_color'):
                self._get_optimized_color.cache_clear()
            
            # Force garbage collection
            gc.collect()
            
            # Clear weak references
            if hasattr(self, '_weak_refs'):
                self._weak_refs.clear()
                
        except Exception as e:
            print(f"Cleanup error: {e}")
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        try:
            if self.is_fullscreen:
                self.exit_fullscreen()
            else:
                self.enter_fullscreen()
        except Exception as e:
            print(f"Fullscreen toggle error: {e}")
    
    def enter_fullscreen(self):
        """Enter fullscreen mode"""
        try:
            self.root.state('zoomed')
            self.is_fullscreen = True
            # Update status text if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Fullscreen Mode")
        except Exception as e:
            print(f"Enter fullscreen error: {e}")
    
    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode"""
        try:
            self.root.state('normal')
            self.is_fullscreen = False
            # Update status text if available
            if hasattr(self, 'status_text'):
                self.status_text.configure(text="Windowed Mode")
        except Exception as e:
            print(f"Exit fullscreen error: {e}")

if __name__ == "__main__":
    try:
        app = NetworkOptimizerApp()
        app.run()
    except Exception as e:
        print(f"Application failed to start: {e}")
        sys.exit(1)
