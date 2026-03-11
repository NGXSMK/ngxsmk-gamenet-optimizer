# pyre-ignore-all-errors
"""
Multi Internet Module
Manages multiple internet connections for load balancing and failover
"""

import subprocess
import platform
import time
import threading
from typing import Dict, List, Optional, Any, cast

from .compat import get_psutil, get_logger # type: ignore
psutil = get_psutil()
globals()['psutil'] = psutil
logger = get_logger("multi_internet")

class MultiInternet:
    def __init__(self):
        self.system: str = platform.system()
        self.is_monitoring: bool = False
        self.monitor_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self.latest_status: List[Dict[str, Any]] = []
        
    def get_available_connections(self) -> List[Dict[str, Any]]:
        """Get list of available network connections"""
        conns: List[Dict[str, Any]] = []
        try:
            nia = psutil.net_if_addrs() # pyre-ignore[16]
            nis = psutil.net_if_stats() # pyre-ignore[16]
            for name, _ in nia.items():
                is_up = nis[name].isup if name in nis else False
                conns.append({'name': name, 'status': 'Connected' if is_up else 'Disconnected'})
        except Exception as e:
            logger.debug("Failed to get multi_internet connections: %s", e)
        return conns
    
    def start_monitoring(self):
        """Start connection monitoring"""
        with self._lock:
            if self.is_monitoring: return
            self.is_monitoring = True
            
        thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread = thread
        thread.start()
        
    def stop_monitoring(self):
        """Stop connection monitoring"""
        with self._lock:
            self.is_monitoring = False
        thread = self.monitor_thread
        if thread:
            thread.join(timeout=2)
            self.monitor_thread = None
        
    def _monitor_loop(self):
        """Monitoring loop with active connection polling"""
        while True:
            with self._lock:
                if not self.is_monitoring:
                    break
            
            try:
                conns = self.get_available_connections()
                with self._lock:
                    self.latest_status = conns
                
                # Sleep in increments
                for _ in range(10):
                    with self._lock:
                        if not self.is_monitoring:
                            break
                    time.sleep(1)
            except Exception as e:
                logger.debug("Multi internet monitoring loop: %s", e)
                time.sleep(10)
    
    def get_optimization_status(self) -> Dict[str, Any]:
        """Get current status for UI"""
        with self._lock:
            monitoring = self.is_monitoring
            conns = self.latest_status.copy() if self.latest_status else self.get_available_connections()
            
        return {
            'is_monitoring': monitoring,
            'connections': len(conns),
            'interface_details': conns
        }
