"""
Advanced System Monitor Module
Real-time system monitoring with performance analytics and predictive insights
"""

import psutil
import time
import threading
import json
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import subprocess
import platform

class SystemMonitor:
    """Advanced system monitor with real-time analytics"""
    
    def __init__(self):
        self.is_monitoring = False
        self.monitoring_thread = None
        self.performance_data = []
        self.alerts = []
        self.thresholds = {
            'cpu_critical': 90,
            'cpu_warning': 80,
            'memory_critical': 95,
            'memory_warning': 85,
            'disk_critical': 95,
            'disk_warning': 85,
            'temperature_critical': 85,
            'temperature_warning': 75
        }
        
    def start_monitoring(self, interval: int = 5):
        """Start real-time system monitoring"""
        if self.is_monitoring:
            return {'status': 'already_monitoring'}
        
        try:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(
                target=self._monitoring_loop, 
                args=(interval,), 
                daemon=True
            )
            self.monitoring_thread.start()
            
            return {'status': 'started', 'interval': interval}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
        
        return {'status': 'stopped'}
    
    def _monitoring_loop(self, interval: int):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect comprehensive system data
                data = self._collect_system_data()
                
                # Analyze performance
                analysis = self._analyze_performance(data)
                
                # Check for alerts
                alerts = self._check_alerts(data)
                
                # Store data
                self.performance_data.append({
                    'timestamp': datetime.now().isoformat(),
                    'data': data,
                    'analysis': analysis,
                    'alerts': alerts
                })
                
                # Keep only last 1000 entries
                if len(self.performance_data) > 1000:
                    self.performance_data.pop(0)
                
                time.sleep(interval)
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(interval)
    
    def _collect_system_data(self) -> Dict:
        """Collect comprehensive system data"""
        try:
            # CPU data
            cpu_data = {
                'usage_percent': psutil.cpu_percent(interval=1),
                'usage_per_core': psutil.cpu_percent(interval=1, percpu=True),
                'frequency': psutil.cpu_freq(),
                'count': psutil.cpu_count(),
                'count_logical': psutil.cpu_count(logical=True),
                'temperature': self._get_cpu_temperature()
            }
            
            # Memory data
            memory = psutil.virtual_memory()
            memory_data = {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'free': memory.free,
                'percentage': memory.percent,
                'cached': getattr(memory, 'cached', 0),
                'buffers': getattr(memory, 'buffers', 0)
            }
            
            # Disk data
            disk_data = {}
            for partition in psutil.disk_partitions():
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    disk_data[partition.device] = {
                        'total': partition_usage.total,
                        'used': partition_usage.used,
                        'free': partition_usage.free,
                        'percentage': (partition_usage.used / partition_usage.total) * 100,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype
                    }
                except:
                    continue
            
            # Network data
            network_data = {
                'io_counters': psutil.net_io_counters(),
                'connections': len(psutil.net_connections()),
                'interfaces': list(psutil.net_if_addrs().keys())
            }
            
            # Process data
            process_data = {
                'total_processes': len(psutil.pids()),
                'top_processes': self._get_top_processes(5)
            }
            
            # System info
            system_data = {
                'boot_time': psutil.boot_time(),
                'uptime': time.time() - psutil.boot_time(),
                'platform': platform.system(),
                'platform_version': platform.version(),
                'architecture': platform.architecture()[0]
            }
            
            return {
                'cpu': cpu_data,
                'memory': memory_data,
                'disk': disk_data,
                'network': network_data,
                'processes': process_data,
                'system': system_data,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def _get_cpu_temperature(self) -> Optional[float]:
        """Get CPU temperature if available"""
        try:
            if platform.system() == "Windows":
                # Try to get temperature from WMI
                import wmi
                w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
                temperature_infos = w.Sensor()
                for sensor in temperature_infos:
                    if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name:
                        return float(sensor.Value)
            return None
        except:
            return None
    
    def _get_top_processes(self, count: int = 5) -> List[Dict]:
        """Get top processes by CPU and memory usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    if proc.info['memory_info']:
                        processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cpu_percent': proc.info['cpu_percent'],
                            'memory_mb': proc.info['memory_info'].rss / (1024 * 1024)
                        })
                except:
                    continue
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            return processes[:count]
            
        except:
            return []
    
    def _analyze_performance(self, data: Dict) -> Dict:
        """Analyze system performance and generate insights"""
        try:
            analysis = {
                'overall_health': 'good',
                'performance_score': 100,
                'recommendations': [],
                'trends': {}
            }
            
            # CPU analysis
            cpu_usage = data.get('cpu', {}).get('usage_percent', 0)
            if cpu_usage > 80:
                analysis['overall_health'] = 'poor'
                analysis['performance_score'] -= 30
                analysis['recommendations'].append("High CPU usage detected - consider closing unnecessary applications")
            elif cpu_usage > 60:
                analysis['overall_health'] = 'fair'
                analysis['performance_score'] -= 15
                analysis['recommendations'].append("Moderate CPU usage - system is working hard")
            
            # Memory analysis
            memory_usage = data.get('memory', {}).get('percentage', 0)
            if memory_usage > 90:
                analysis['overall_health'] = 'poor'
                analysis['performance_score'] -= 40
                analysis['recommendations'].append("Critical memory usage - immediate cleanup needed")
            elif memory_usage > 80:
                analysis['overall_health'] = 'fair'
                analysis['performance_score'] -= 20
                analysis['recommendations'].append("High memory usage - consider freeing up RAM")
            
            # Disk analysis
            disk_usage = 0
            for disk in data.get('disk', {}).values():
                if isinstance(disk, dict) and 'percentage' in disk:
                    disk_usage = max(disk_usage, disk['percentage'])
            
            if disk_usage > 90:
                analysis['overall_health'] = 'poor'
                analysis['performance_score'] -= 25
                analysis['recommendations'].append("Critical disk space - cleanup recommended")
            elif disk_usage > 80:
                analysis['overall_health'] = 'fair'
                analysis['performance_score'] -= 15
                analysis['recommendations'].append("High disk usage - consider freeing up space")
            
            # Temperature analysis
            temp = data.get('cpu', {}).get('temperature')
            if temp and temp > 80:
                analysis['overall_health'] = 'poor'
                analysis['performance_score'] -= 20
                analysis['recommendations'].append("High CPU temperature - check cooling system")
            elif temp and temp > 70:
                analysis['overall_health'] = 'fair'
                analysis['performance_score'] -= 10
                analysis['recommendations'].append("Moderate CPU temperature - monitor cooling")
            
            # Calculate trends
            if len(self.performance_data) >= 5:
                analysis['trends'] = self._calculate_trends()
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_trends(self) -> Dict:
        """Calculate performance trends"""
        try:
            if len(self.performance_data) < 5:
                return {}
            
            recent_data = self.performance_data[-5:]
            
            # CPU trend
            cpu_values = [entry['data'].get('cpu', {}).get('usage_percent', 0) for entry in recent_data]
            cpu_trend = 'stable'
            if len(cpu_values) >= 2:
                if cpu_values[-1] > cpu_values[0] + 10:
                    cpu_trend = 'increasing'
                elif cpu_values[-1] < cpu_values[0] - 10:
                    cpu_trend = 'decreasing'
            
            # Memory trend
            memory_values = [entry['data'].get('memory', {}).get('percentage', 0) for entry in recent_data]
            memory_trend = 'stable'
            if len(memory_values) >= 2:
                if memory_values[-1] > memory_values[0] + 5:
                    memory_trend = 'increasing'
                elif memory_values[-1] < memory_values[0] - 5:
                    memory_trend = 'decreasing'
            
            return {
                'cpu_trend': cpu_trend,
                'memory_trend': memory_trend,
                'overall_trend': 'stable' if cpu_trend == 'stable' and memory_trend == 'stable' else 'changing'
            }
            
        except:
            return {}
    
    def _check_alerts(self, data: Dict) -> List[Dict]:
        """Check for system alerts"""
        alerts = []
        
        try:
            # CPU alerts
            cpu_usage = data.get('cpu', {}).get('usage_percent', 0)
            if cpu_usage >= self.thresholds['cpu_critical']:
                alerts.append({
                    'type': 'critical',
                    'component': 'CPU',
                    'message': f'Critical CPU usage: {cpu_usage:.1f}%',
                    'timestamp': datetime.now().isoformat()
                })
            elif cpu_usage >= self.thresholds['cpu_warning']:
                alerts.append({
                    'type': 'warning',
                    'component': 'CPU',
                    'message': f'High CPU usage: {cpu_usage:.1f}%',
                    'timestamp': datetime.now().isoformat()
                })
            
            # Memory alerts
            memory_usage = data.get('memory', {}).get('percentage', 0)
            if memory_usage >= self.thresholds['memory_critical']:
                alerts.append({
                    'type': 'critical',
                    'component': 'Memory',
                    'message': f'Critical memory usage: {memory_usage:.1f}%',
                    'timestamp': datetime.now().isoformat()
                })
            elif memory_usage >= self.thresholds['memory_warning']:
                alerts.append({
                    'type': 'warning',
                    'component': 'Memory',
                    'message': f'High memory usage: {memory_usage:.1f}%',
                    'timestamp': datetime.now().isoformat()
                })
            
            # Disk alerts
            for disk_name, disk_data in data.get('disk', {}).items():
                if isinstance(disk_data, dict) and 'percentage' in disk_data:
                    disk_usage = disk_data['percentage']
                    if disk_usage >= self.thresholds['disk_critical']:
                        alerts.append({
                            'type': 'critical',
                            'component': 'Disk',
                            'message': f'Critical disk usage on {disk_name}: {disk_usage:.1f}%',
                            'timestamp': datetime.now().isoformat()
                        })
                    elif disk_usage >= self.thresholds['disk_warning']:
                        alerts.append({
                            'type': 'warning',
                            'component': 'Disk',
                            'message': f'High disk usage on {disk_name}: {disk_usage:.1f}%',
                            'timestamp': datetime.now().isoformat()
                        })
            
            # Temperature alerts
            temp = data.get('cpu', {}).get('temperature')
            if temp:
                if temp >= self.thresholds['temperature_critical']:
                    alerts.append({
                        'type': 'critical',
                        'component': 'Temperature',
                        'message': f'Critical CPU temperature: {temp:.1f}°C',
                        'timestamp': datetime.now().isoformat()
                    })
                elif temp >= self.thresholds['temperature_warning']:
                    alerts.append({
                        'type': 'warning',
                        'component': 'Temperature',
                        'message': f'High CPU temperature: {temp:.1f}°C',
                        'timestamp': datetime.now().isoformat()
                    })
            
            # Store alerts
            self.alerts.extend(alerts)
            
            # Keep only last 100 alerts
            if len(self.alerts) > 100:
                self.alerts = self.alerts[-100:]
            
        except Exception as e:
            alerts.append({
                'type': 'error',
                'component': 'Monitor',
                'message': f'Monitoring error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            })
        
        return alerts
    
    def get_current_status(self) -> Dict:
        """Get current system status"""
        try:
            if not self.performance_data:
                return {'status': 'no_data'}
            
            latest = self.performance_data[-1]
            return {
                'status': 'monitoring',
                'latest_data': latest,
                'monitoring_duration': len(self.performance_data),
                'total_alerts': len(self.alerts)
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_performance_summary(self, hours: int = 1) -> Dict:
        """Get performance summary for specified hours"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_data = [
                entry for entry in self.performance_data
                if datetime.fromisoformat(entry['timestamp']) >= cutoff_time
            ]
            
            if not recent_data:
                return {'status': 'no_data'}
            
            # Calculate averages
            cpu_values = [entry['data'].get('cpu', {}).get('usage_percent', 0) for entry in recent_data]
            memory_values = [entry['data'].get('memory', {}).get('percentage', 0) for entry in recent_data]
            
            return {
                'period_hours': hours,
                'data_points': len(recent_data),
                'avg_cpu_usage': sum(cpu_values) / len(cpu_values) if cpu_values else 0,
                'avg_memory_usage': sum(memory_values) / len(memory_values) if memory_values else 0,
                'max_cpu_usage': max(cpu_values) if cpu_values else 0,
                'max_memory_usage': max(memory_values) if memory_values else 0,
                'alerts_count': len([entry for entry in recent_data if entry.get('alerts')])
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_alerts(self, limit: int = 50) -> List[Dict]:
        """Get recent alerts"""
        return self.alerts[-limit:] if self.alerts else []
    
    def set_thresholds(self, thresholds: Dict[str, float]):
        """Set alert thresholds"""
        self.thresholds.update(thresholds)
        return {'status': 'updated', 'thresholds': self.thresholds}
    
    def export_data(self, filename: str = None) -> str:
        """Export monitoring data to JSON file"""
        try:
            if not filename:
                filename = f"system_monitor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'monitoring_duration': len(self.performance_data),
                'performance_data': self.performance_data,
                'alerts': self.alerts,
                'thresholds': self.thresholds
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return filename
            
        except Exception as e:
            return f"Export failed: {str(e)}"
