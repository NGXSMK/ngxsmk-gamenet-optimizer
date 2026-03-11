"""
Low Resource Configuration for NGXSMK GameNet Optimizer
Optimized settings for low-end PCs
"""

from typing import Dict, Any, cast

class _PsutilFallback:
    def virtual_memory(self, *args, **kwargs) -> Any:
        class VM: total = 4 * (1024**3)
        return VM()
    def cpu_count(self, **_kwargs: Any) -> int: return 2
    def cpu_percent(self, *args, **kwargs) -> float: return 0.0

try:
    import psutil # type: ignore
except ImportError:
    psutil = cast(Any, _PsutilFallback())

# Ensure psutil is seen as Any for Pyre
globals()['psutil'] = psutil

# Low Resource Mode Settings
LOW_RESOURCE_CONFIG = {
    'ui': {
        'reduced_fonts': True, 'smaller_icons': True, 'minimal_animations': True,
        'compact_layout': True, 'hide_subtitles': True, 'reduced_status_indicators': True
    },
    'performance': {
        'reduced_threads': True, 'max_threads': 2, 'gc_interval': 15,
        'monitoring_interval': 10, 'status_update_interval': 2000,
        'cache_size': 50, 'memory_limit': 100
    },
    'features': {
        'disable_advanced_monitoring': True, 'disable_network_analysis': False,
        'disable_real_time_updates': True, 'simplified_ui': True, 'minimal_tabs': True
    },
    'window': {
        'default_size': (1000, 700), 'min_size': (800, 600),
        'no_fullscreen': True, 'reduced_padding': True
    },
    'memory': {
        'aggressive_gc': True, 'weak_references': True,
        'cache_cleanup': True, 'process_optimization': True
    }
}

LOW_RESOURCE_REQUIREMENTS = {
    'min_ram': 4, 'max_ram': 8, 'min_cpu_cores': 2, 'max_cpu_cores': 4,
    'cpu_usage_threshold': 50
}

def should_enable_low_resource_mode() -> bool:
    """Check if low resource mode should be enabled"""
    try:
        memory = psutil.virtual_memory() # pyre-ignore[16]
        memory_gb = memory.total / (1024**3)
        cpu_count = psutil.cpu_count() or 1 # pyre-ignore[16]
        cpu_usage = psutil.cpu_percent(interval=None) # pyre-ignore[16]
        
        return (
            memory_gb < LOW_RESOURCE_REQUIREMENTS['max_ram'] or
            cpu_count < LOW_RESOURCE_REQUIREMENTS['min_cpu_cores'] or
            cpu_usage > LOW_RESOURCE_REQUIREMENTS['cpu_usage_threshold']
        )
    except Exception:
        return True

def get_optimized_settings() -> Dict[str, Any]:
    """Get optimized settings for the current system"""
    if should_enable_low_resource_mode():
        return LOW_RESOURCE_CONFIG
    return {
        'ui': {
            'reduced_fonts': False, 'smaller_icons': False, 'minimal_animations': False,
            'compact_layout': False, 'hide_subtitles': False, 'reduced_status_indicators': False
        },
        'performance': {
            'reduced_threads': False, 'max_threads': 4, 'gc_interval': 30,
            'monitoring_interval': 5, 'status_update_interval': 1000,
            'cache_size': 100, 'memory_limit': 200
        },
        'features': {
            'disable_advanced_monitoring': False, 'disable_network_analysis': False,
            'disable_real_time_updates': False, 'simplified_ui': False, 'minimal_tabs': False
        },
        'window': { 'default_size': (1200, 800), 'min_size': (1000, 700), 'no_fullscreen': False, 'reduced_padding': False },
        'memory': { 'aggressive_gc': False, 'weak_references': True, 'cache_cleanup': False, 'process_optimization': True }
    }
