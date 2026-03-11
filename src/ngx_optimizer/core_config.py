"""
Low Resource Configuration for NGXSMK GameNet Optimizer
Optimized settings for low-end PCs
"""

# Low Resource Mode Settings
LOW_RESOURCE_CONFIG = {
    # UI Optimizations
    'ui': {
        'reduced_fonts': True,
        'smaller_icons': True,
        'minimal_animations': True,
        'compact_layout': True,
        'hide_subtitles': True,
        'reduced_status_indicators': True
    },
    
    # Performance Optimizations
    'performance': {
        'reduced_threads': True,
        'max_threads': 2,
        'gc_interval': 15,  # seconds
        'monitoring_interval': 10,  # seconds
        'status_update_interval': 2000,  # milliseconds
        'cache_size': 50,
        'memory_limit': 100  # MB
    },
    
    # Feature Reductions
    'features': {
        'disable_advanced_monitoring': True,
        'disable_network_analysis': False,  # Keep essential features
        'disable_real_time_updates': True,
        'simplified_ui': True,
        'minimal_tabs': True
    },
    
    # Window Settings
    'window': {
        'default_size': (1000, 700),
        'min_size': (800, 600),
        'no_fullscreen': True,
        'reduced_padding': True
    },
    
    # Memory Management
    'memory': {
        'aggressive_gc': True,
        'weak_references': True,
        'cache_cleanup': True,
        'process_optimization': True
    }
}

# System Requirements for Low Resource Mode
LOW_RESOURCE_REQUIREMENTS = {
    'min_ram': 4,  # GB
    'max_ram': 8,  # GB
    'min_cpu_cores': 2,
    'max_cpu_cores': 4,
    'cpu_usage_threshold': 50  # %
}

def should_enable_low_resource_mode():
    """Check if low resource mode should be enabled"""
    try:
        import psutil
        
        # Get system info
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        cpu_count = psutil.cpu_count()
        cpu_usage = psutil.cpu_percent(interval=0.1)
        
        # Check if system meets low resource criteria
        return (
            memory_gb < LOW_RESOURCE_REQUIREMENTS['max_ram'] or
            cpu_count < LOW_RESOURCE_REQUIREMENTS['min_cpu_cores'] or
            cpu_usage > LOW_RESOURCE_REQUIREMENTS['cpu_usage_threshold']
        )
        
    except Exception:
        # Default to low resource mode if detection fails
        return True

def get_optimized_settings():
    """Get optimized settings for the current system"""
    if should_enable_low_resource_mode():
        return LOW_RESOURCE_CONFIG
    else:
        # Return standard settings for capable systems
        return {
            'ui': {
                'reduced_fonts': False,
                'smaller_icons': False,
                'minimal_animations': False,
                'compact_layout': False,
                'hide_subtitles': False,
                'reduced_status_indicators': False
            },
            'performance': {
                'reduced_threads': False,
                'max_threads': 4,
                'gc_interval': 30,
                'monitoring_interval': 5,
                'status_update_interval': 1000,
                'cache_size': 100,
                'memory_limit': 200
            },
            'features': {
                'disable_advanced_monitoring': False,
                'disable_network_analysis': False,
                'disable_real_time_updates': False,
                'simplified_ui': False,
                'minimal_tabs': False
            },
            'window': {
                'default_size': (1200, 800),
                'min_size': (1000, 700),
                'no_fullscreen': False,
                'reduced_padding': False
            },
            'memory': {
                'aggressive_gc': False,
                'weak_references': True,
                'cache_cleanup': False,
                'process_optimization': True
            }
        }
