import customtkinter # type: ignore
import json
import os
from tkinter import messagebox, filedialog
import tkinter as tk
from typing import Dict, Any, Optional

# Standard fonts
FONT_FAMILY_BOLD = 'Segoe UI Semibold'
FONT_FAMILY_REGULAR = 'Segoe UI'

class SettingsDialog:
    """Modern CTk-based settings dialog"""
    
    def __init__(self, parent, config_manager, colors=None, fonts=None):
        self.parent = parent
        self.config_manager = config_manager
        self.colors = colors or {
            'bg_primary': '#0F111A',
            'bg_secondary': '#161925',
            'bg_card': '#1E2235',
            'accent': '#00D2FF',
            'accent_glow': '#0099FF',
            'text_primary': '#FFFFFF',
            'text_secondary': '#94A3B8'
        }
        self.fonts = fonts or {
            'h1': (FONT_FAMILY_REGULAR, 24, 'bold'),
            'h2': (FONT_FAMILY_REGULAR, 18, 'bold'),
            'body': (FONT_FAMILY_REGULAR, 14),
            'small': (FONT_FAMILY_REGULAR, 12)
        }
        self.settings: Dict[str, Any] = {}
        self.dialog = None
        self.tabview = None
        
        # Variables for UI components initial state
        self.auto_start: Optional[customtkinter.BooleanVar] = None
        self.auto_optimize: Optional[customtkinter.BooleanVar] = None
        self.theme: Optional[customtkinter.StringVar] = None
        self.language: Optional[customtkinter.StringVar] = None
        self.low_resource_mode: Optional[customtkinter.BooleanVar] = None
        self.priority_boost: Optional[customtkinter.BooleanVar] = None
        self.custom_dns: Optional[customtkinter.BooleanVar] = None
        self.dns_primary: Optional[customtkinter.StringVar] = None
        self.dns_secondary: Optional[customtkinter.StringVar] = None
        
    def show_settings(self):
        """Build and show the modern settings dialog"""
        dialog = customtkinter.CTkToplevel(self.parent)
        self.dialog = dialog
        dialog.title("ADVANCED SYSTEM CONFIGURATION")
        dialog.geometry("800x600")
        dialog.configure(fg_color=self.colors['bg_primary'])
        dialog.after(10, lambda: dialog.focus())
        
        self.settings = self.config_manager.load_settings()
        self._initialize_variables()
        self._setup_ui()
        
    def _initialize_variables(self):
        """Sync CTk variables with config schema"""
        ui: Dict[str, Any] = self.settings.get('ui', {})
        self.auto_start = customtkinter.BooleanVar(value=bool(ui.get('auto_start', False)))
        self.auto_optimize = customtkinter.BooleanVar(value=bool(ui.get('auto_optimize', False)))
        self.theme = customtkinter.StringVar(value=str(ui.get('theme', 'dark')))
        self.language = customtkinter.StringVar(value=str(ui.get('language', 'en')))
        self.low_resource_mode = customtkinter.BooleanVar(value=bool(ui.get('low_resource_mode', False)))
        
        fps: Dict[str, Any] = self.settings.get('fps_boost', {})
        self.priority_boost = customtkinter.BooleanVar(value=bool(fps.get('priority_boost', True)))
        
        net: Dict[str, Any] = self.settings.get('network', {})
        self.custom_dns = customtkinter.BooleanVar(value=bool(net.get('custom_dns', False)))
        self.dns_primary = customtkinter.StringVar(value=str(net.get('dns_primary', '8.8.8.8')))
        self.dns_secondary = customtkinter.StringVar(value=str(net.get('dns_secondary', '1.1.1.1')))

    def _setup_ui(self):
        """Create the integrated settings interface"""
        dialog = self.dialog
        if not dialog:
            return
            
        # Header
        header = customtkinter.CTkFrame(dialog, fg_color=self.colors['bg_secondary'], corner_radius=0)
        header.pack(fill="x", pady=(0, 2))
        
        h2_font = self.fonts.get('h2')
        if not isinstance(h2_font, customtkinter.CTkFont):
            h2_font = customtkinter.CTkFont(size=18, weight="bold")
            
        customtkinter.CTkLabel(header, text="⚙️ SYSTEM PREFERENCES", 
                               font=h2_font,
                               text_color=self.colors['accent']).pack(padx=20, pady=20, side="left")

        # Main Content - Tabs
        tabview = customtkinter.CTkTabview(dialog, segmented_button_fg_color=self.colors['bg_secondary'],
                                               segmented_button_selected_color=self.colors['accent'],
                                               segmented_button_unselected_color="transparent")
        self.tabview = tabview
        tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        t_gen = tabview.add("GEN")
        t_net = tabview.add("NET")
        t_game = tabview.add("GAME")
        
        # General Tab
        if self.auto_start and self.auto_optimize:
            customtkinter.CTkSwitch(t_gen, text="Launch at System Startup", variable=self.auto_start).pack(pady=10, anchor="w")
            customtkinter.CTkSwitch(t_gen, text="Intelligent Auto-Optimization", variable=self.auto_optimize).pack(pady=10, anchor="w")
            
            if self.low_resource_mode:
                customtkinter.CTkSwitch(t_gen, text="Low Resource Mode (for older PCs)", variable=self.low_resource_mode).pack(pady=10, anchor="w")
            
            # Theme and Language in a grid
            pref_frame = customtkinter.CTkFrame(t_gen, fg_color="transparent")
            pref_frame.pack(pady=15, fill="x")
            
            customtkinter.CTkLabel(pref_frame, text="Application Theme:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            customtkinter.CTkOptionMenu(pref_frame, values=["dark", "light", "gaming"], variable=self.theme).grid(row=0, column=1, padx=10, pady=5)
            
            customtkinter.CTkLabel(pref_frame, text="Language Context:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            customtkinter.CTkOptionMenu(pref_frame, values=["en", "es", "fr"], variable=self.language).grid(row=1, column=1, padx=10, pady=5)
        
        # Network Tab
        if self.custom_dns and self.dns_primary and self.dns_secondary:
            customtkinter.CTkSwitch(t_net, text="Force Custom DNS Architecture", variable=self.custom_dns).pack(pady=10, anchor="w")
            customtkinter.CTkEntry(t_net, placeholder_text="Primary DNS", textvariable=self.dns_primary, width=200).pack(pady=5, anchor="w")
            customtkinter.CTkEntry(t_net, placeholder_text="Secondary DNS", textvariable=self.dns_secondary, width=200).pack(pady=5, anchor="w")
        
        # Gaming Tab
        if self.priority_boost:
            customtkinter.CTkSwitch(t_game, text="Aggressive Priority Allocation", variable=self.priority_boost).pack(pady=10, anchor="w")

        # Footer Actions
        footer = customtkinter.CTkFrame(dialog, fg_color="transparent")
        footer.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkButton(footer, text="SAVE CONFIG", command=self.save_and_close,
                               fg_color=self.colors['accent'], text_color=self.colors['bg_primary'],
                               font=customtkinter.CTkFont(weight="bold")).pack(side="right", padx=10)
                               
        customtkinter.CTkButton(footer, text="REVERT", command=dialog.destroy,
                               fg_color="transparent", border_width=2, border_color=self.colors['accent']).pack(side="right", padx=10)

    def save_and_close(self):
        """Save and terminate dialog"""
        try:
            a_start, a_opt, t_heme = self.auto_start, self.auto_optimize, self.theme
            l_ang, l_res = self.language, self.low_resource_mode
            p_boost = self.priority_boost
            c_dns, d_prim, d_sec = self.custom_dns, self.dns_primary, self.dns_secondary
            
            settings = {
                'ui': {
                    'auto_start': a_start.get() if a_start else False,
                    'auto_optimize': a_opt.get() if a_opt else False,
                    'theme': t_heme.get() if t_heme else 'dark',
                    'language': l_ang.get() if l_ang else 'en',
                    'low_resource_mode': l_res.get() if l_res else False
                },
                'fps_boost': {
                    'priority_boost': p_boost.get() if p_boost else True
                },
                'network': {
                    'custom_dns': c_dns.get() if c_dns else False,
                    'dns_primary': d_prim.get() if d_prim else '8.8.8.8',
                    'dns_secondary': d_sec.get() if d_sec else '1.1.1.1'
                }
            }
            self.config_manager.save_settings(settings)
            dialog = self.dialog
            if dialog:
                dialog.destroy()
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to persist configuration: {str(e)}")
