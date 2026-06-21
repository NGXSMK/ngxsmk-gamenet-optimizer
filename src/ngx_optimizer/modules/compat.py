"""
Compatibility layer for external dependencies
Handles fallback mechanisms for missing libraries
"""

import platform
import typing
from typing import Dict, List, Any, Optional, cast

class _PsutilFallback:
    class Process:
        def __init__(self, pid: int = 0):
            self.pid: int = pid
            self.info: Dict[str, Any] = {'name': '', 'pid': 0, 'exe': ''}
        def nice(self, **_kwargs: Any) -> int: return 0
        def cpu_affinity(self, **_kwargs: Any) -> List[int]: return []
        def memory_info(self) -> Any:
            class Mem: rss = 0
            return Mem()
        def cpu_percent(self, **_kwargs: Any) -> float: return 0.0
        def connections(self, **_kwargs: Any) -> List[Any]: return []
            
    class _NoSuchProcess(Exception): pass
    class _AccessDenied(Exception): pass
    
    NoSuchProcess = _NoSuchProcess # NOSONAR
    AccessDenied = _AccessDenied # NOSONAR
    HIGH_PRIORITY_CLASS: int = 0x00000080
    NORMAL_PRIORITY_CLASS: int = 0x00000020
    
    def process_iter(self, attrs=None, **_kwargs: Any) -> Any: return []
    def cpu_count(self, **_kwargs: Any) -> int: return 1
    def cpu_percent(self, *args, **kwargs) -> float: return 0.0
    def virtual_memory(self, *args, **kwargs) -> Any:
        class VM: total=0; available=0; used=0; percent=0
        return VM()
    def disk_usage(self, *args, **kwargs) -> Any:
        class DU: total=0; used=0; free=0; percent=0
        return DU()
    def net_io_counters(self, *args, **kwargs) -> Any:
        class NIO: bytes_sent=0; bytes_recv=0
        return NIO()
    def net_if_addrs(self, *args, **kwargs) -> Dict[str, Any]: return {}
    def net_connections(self, *args, **kwargs) -> List[Any]: return []
    def net_if_stats(self, *args, **kwargs) -> Dict[str, Any]: return {}
    def cpu_freq(self, *args, **kwargs) -> Any:
        class CF: current=0; min=0; max=0
        return CF()
    def pids(self, *args, **kwargs) -> List[int]: return []
    def boot_time(self, *args, **kwargs) -> float: return 0.0

def get_psutil() -> Any:
    """Get psutil instance or a fallback"""
    try:
        import psutil # type: ignore
        return psutil
    except ImportError:
        return cast(Any, _PsutilFallback())

import logging
import os

_LOG_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'NGXSMK GameNet Optimizer')
DATA_DIR = _LOG_DIR

def get_logger(name: str) -> logging.Logger:
    """Get a configured logger"""
    os.makedirs(_LOG_DIR, exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(os.path.join(_LOG_DIR, 'optimizer.log'), encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
