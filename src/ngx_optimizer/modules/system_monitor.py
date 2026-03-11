# pyre-ignore-all-errors
"""
Advanced System Monitor Module
Real-time system monitoring with performance analytics and predictive insights
"""

import typing
import time
import threading
import json
import os
import platform
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, cast

from .compat import get_psutil # type: ignore
psutil = get_psutil()
globals()['psutil'] = psutil

class SystemMonitor:
    def __init__(self):
        self.is_monitoring = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self._data_lock = threading.Lock()
        self.performance_data: List[Dict[str, Any]] = []
        
    def start_monitoring(self, interval: int = 5):
        """Start monitoring"""
        if self.is_monitoring: return
        self.is_monitoring = True
        thread = threading.Thread(target=self._monitoring_loop, args=(interval,), daemon=True)
        self.monitoring_thread = thread
        thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        thread = self.monitoring_thread
        if thread:
            thread.join(timeout=2)
    
    def _monitoring_loop(self, interval: int):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                data = self.get_current_stats()
                with self._data_lock:
                    self.performance_data.append(data)
                    if len(self.performance_data) > 100: self.performance_data.pop(0)
                time.sleep(interval)
            except Exception:
                time.sleep(interval)
    
    def get_current_stats(self) -> Dict[str, Any]:
        """Collect current system stats"""
        try:
            vmem = psutil.virtual_memory() # pyre-ignore[16]
            return {
                'cpu': float(psutil.cpu_percent(interval=None)), # pyre-ignore[16]
                'memory': float(vmem.percent),
                'timestamp': datetime.now().isoformat()
            }
        except Exception:
            return {'cpu': 0.0, 'memory': 0.0, 'timestamp': datetime.now().isoformat()}
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get summary of recently collected data"""
        with self._data_lock:
            if not self.performance_data: return {'status': 'No data'}
            recent = self.performance_data[-1]
            history_len = len(self.performance_data)
            
        return {
            'current_cpu': recent.get('cpu', 0.0),
            'current_memory': recent.get('memory', 0.0),
            'history_count': history_len
        }

    def get_optimization_status(self) -> Dict[str, Any]:
        """Get current status for UI"""
        return {
            'is_monitoring': self.is_monitoring,
            'summary': self.get_performance_summary()
        }
