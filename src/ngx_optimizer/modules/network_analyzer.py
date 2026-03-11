# pyre-ignore-all-errors
"""
Network Analyzer Module
Analyzes network performance, latency, and connection quality
"""

import socket
import time
import threading
import subprocess
import platform
import statistics
import typing
from typing import Dict, List, Tuple, Optional, Any, cast

from .compat import get_psutil, get_logger # type: ignore
psutil = get_psutil()
globals()['psutil'] = psutil

logger = get_logger("network_analyzer")

try:
    import ping3 # type: ignore
    PING3_AVAILABLE = True
except ImportError:
    PING3_AVAILABLE = False

class NetworkAnalyzer:
    # Class-level constants for better maintainability
    DEFAULT_TEST_SERVERS = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
    GAMING_SERVERS = {
        'Valorant': ['104.18.0.0', '104.18.1.0'],
        'CS2': ['162.254.196.0', '162.254.197.0'],
        'LoL': ['104.160.131.1', '104.160.131.2']
    }

    def __init__(self):
        self.system: str = platform.system()
        self.is_analyzing: bool = False
        self.analysis_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self.results: Dict[str, Any] = {}
    
    def ping_host(self, host: str, count: int = 4) -> Dict[str, float]:
        """Ping a host and return latency statistics"""
        if PING3_AVAILABLE:
            return self._ping_with_ping3(host, count)
        return self._ping_with_system(host, count)
    
    def _ping_with_ping3(self, host: str, count: int) -> Dict[str, float]:
        """Ping using ping3 library"""
        latencies: List[float] = []
        for _ in range(count):
            try:
                latency = ping3.ping(host, timeout=5)
                if latency is not None:
                    latencies.append(float(latency) * 1000.0)
            except Exception as e:
                logger.debug("ping3 ping issue: %s", e)
                continue
        
        if not latencies: return {'min': 0.0, 'max': 0.0, 'avg': 0.0, 'packet_loss': 100.0}
        return {'min': min(latencies), 'max': max(latencies), 'avg': statistics.mean(latencies), 'packet_loss': float(count - len(latencies)) / count * 100.0}
    
    def _ping_with_system(self, host: str, count: int) -> Dict[str, float]:
        """Ping using system ping command"""
        try:
            cmd = ['ping', '-n' if self.system == "Windows" else '-c', str(count), host]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if res.returncode == 0: return self._parse_ping_output(res.stdout)
            return {'min': 0.0, 'max': 0.0, 'avg': 0.0, 'packet_loss': 100.0}
        except Exception as e:
            logger.debug("System ping failed: %s", e)
            return {'min': 0.0, 'max': 0.0, 'avg': 0.0, 'packet_loss': 100.0}

    def _parse_ping_output(self, output: str) -> Dict[str, float]:
        """Parse system ping output for latency"""
        lats: List[float] = []
        for line in output.split('\n'):
            if 'time=' in line or 'time<' in line:
                try:
                    p = line.split('time' + ('=' if 'time=' in line else '<'))[1].split()[0].replace('ms', '')
                    lats.append(float(p))
                except (IndexError, ValueError): pass
        if not lats: return {'min': 0.0, 'max': 0.0, 'avg': 0.0, 'packet_loss': 100.0}
        return {'min': min(lats), 'max': max(lats), 'avg': statistics.mean(lats), 'packet_loss': 0.0}
    
    def test_bandwidth(self) -> Dict[str, float]:
        """Test internet bandwidth (simplified estimation)"""
        try:
            ping_res = self.ping_host('8.8.8.8', 2)
            avg = float(ping_res['avg'])
            if avg <= 0.0: return {'download': 0.0, 'upload': 0.0, 'ping': 0.0}
            
            # Use float explicitly to help type inference
            est_dl: float = 100.0 + (50.0 - avg) * 2.0 if avg < 50.0 else max(5.0, 50.0 - (avg - 50.0) * 0.5)
            est_ul: float = est_dl * 0.8
            dl_1dp: float = int(float(est_dl) * 10) / 10.0
            ul_1dp: float = int(float(est_ul) * 10) / 10.0
            avg_1dp: float = int(float(avg) * 10) / 10.0
            return {'download': dl_1dp, 'upload': ul_1dp, 'ping': avg_1dp}
        except Exception as e:
            logger.debug("Bandwidth test failed: %s", e)
            return {'download': 0.0, 'upload': 0.0, 'ping': 0.0}
    
    def analyze_network_connections(self) -> List[Dict[str, Any]]:
        """Analyze current network connections"""
        conns: List[Dict[str, Any]] = []
        try:
            for c in psutil.net_connections(kind='inet'): # pyre-ignore[16]
                if getattr(c, 'status', '') == 'ESTABLISHED':
                    l = getattr(c, 'laddr', None)
                    r = getattr(c, 'raddr', None)
                    conns.append({
                        'local': f"{l.ip}:{l.port}" if l else "N/A",
                        'remote': f"{r.ip}:{r.port}" if r else "N/A",
                        'pid': getattr(c, 'pid', 0)
                    })
        except Exception as e:
            logger.debug("Connection status issue: %s", e)
        return conns
    
    def get_network_interfaces(self) -> List[Dict[str, Any]]:
        """Get information about network interfaces"""
        ifaces: List[Dict[str, Any]] = []
        try:
            for name, addresses in psutil.net_if_addrs().items(): # pyre-ignore[16]
                info = {'name': name, 'ip': 'N/A', 'is_up': True}
                for a in addresses:
                    if a.family == socket.AF_INET:
                        info['ip'] = a.address
                        break
                ifaces.append(info)
        except Exception as e:
            logger.debug("Interface polling issue: %s", e)
        return ifaces
    
    def test_gaming_servers(self) -> Dict[str, Dict[str, float]]:
        """Test latency to gaming servers"""
        results: Dict[str, Dict[str, float]] = {}
        for game, servers in self.GAMING_SERVERS.items():
            lats = []
            for s in servers:
                p = self.ping_host(s, 2)
                if p['avg'] > 0: lats.append(float(p['avg']))
            results[game] = {'avg_latency': statistics.mean(lats) if lats else 0.0}
        return results
    
    def analyze_network(self) -> Dict[str, Any]:
        """Main network analysis function - returns dictionary for UI"""
        try:
            p1 = self.ping_host('8.8.8.8', 2)
            bw = self.test_bandwidth()
            gaming = self.test_gaming_servers()
            quality = self.get_network_quality_score()
            
            return {
                'connection_status': 'Connected' if p1['avg'] > 0 else 'Disconnected',
                'latency': p1['avg'],
                'download_speed': bw['download'],
                'upload_speed': bw['upload'],
                'gaming_servers': gaming,
                'quality_score': quality['score'],
                'quality_rating': quality['quality']
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_network_quality_score(self) -> Dict[str, Any]:
        """Calculate network quality score"""
        try:
            p = self.ping_host('8.8.8.8', 3)
            avg = float(p['avg'])
            loss = float(p['packet_loss'])
            if avg <= 0.0: return {'score': 0, 'quality': 'Poor'}
            
            score = 100
            if avg > 100: score -= 30
            elif avg > 50: score -= 15
            if loss > 5: score -= 40
            elif loss > 1: score -= 15
            
            q = 'Poor'
            if score >= 80: q = 'Excellent'
            elif score >= 60: q = 'Good'
            elif score >= 40: q = 'Fair'
            
            return {'score': max(0, score), 'quality': q, 'latency': avg, 'loss': loss}
        except Exception as e:
            logger.debug("Network Quality score calc failed: %s", e)
            return {'score': 0, 'quality': 'Unknown'}

    def start_continuous_analysis(self, interval: int = 30):
        """Start continuous network analysis"""
        if self.is_analyzing: return
        self.is_analyzing = True
        thread = threading.Thread(target=self._loop, args=(interval,), daemon=True)
        self.analysis_thread = thread
        thread.start()
    
    def stop_continuous_analysis(self):
        """Stop continuous network analysis"""
        self.is_analyzing = False
        thread = self.analysis_thread
        if thread:
            thread.join(timeout=2)
            self.analysis_thread = None
    
    def get_latest_results(self) -> Dict[str, Any]:
        """Thread-safe getter for analysis results"""
        with self._lock:
            return self.results.copy()
    
    def _loop(self, interval: int):
        """Loop for continuous analysis"""
        while self.is_analyzing:
            try:
                new_results = self.analyze_network()
                with self._lock:
                    self.results = new_results
                
                # Sleep in smaller increments to react faster to stop flag
                for _ in range(interval):
                    if not self.is_analyzing:
                        break
                    time.sleep(1)
            except Exception as e:
                logger.debug("Network analyzer background loop error: %s", e)
                time.sleep(interval)
