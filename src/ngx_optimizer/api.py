# pyre-ignore-all-errors
import sys
import os
import subprocess
import platform
from flask import Flask, jsonify, request, send_from_directory # type: ignore
from flask_cors import CORS # type: ignore
import threading
import time

# Add src to python path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ngx_optimizer.modules.ram_cleaner import RAMCleaner # type: ignore
from ngx_optimizer.modules.system_monitor import SystemMonitor # type: ignore
from ngx_optimizer.modules.config_manager import ConfigManager # type: ignore
from ngx_optimizer.modules.fps_boost import FPSBoost # type: ignore
from ngx_optimizer.modules.network_optimizer import NetworkOptimizer # type: ignore
from ngx_optimizer.modules.gaming_optimizer import GamingOptimizer # type: ignore
from ngx_optimizer.modules.network_analyzer import NetworkAnalyzer # type: ignore
from ngx_optimizer.modules.neural_intelligence import NeuralIntelligence # type: ignore
from ngx_optimizer.modules.learning_core import LearningCore # type: ignore
from ngx_optimizer.modules.hardware_controller import HardwareController # type: ignore
from ngx_optimizer.modules.network_evolution import NetworkEvolution # type: ignore
from ngx_optimizer.modules.cloud_link import CloudLink # type: ignore
from ngx_optimizer.modules.ecosystem_integration import EcosystemIntegration # type: ignore
from ngx_optimizer.modules.traffic_shaper import TrafficShaper # type: ignore
from ngx_optimizer.modules.multi_internet import MultiInternet # type: ignore
from ngx_optimizer.modules.lol_optimizer import LoLOptimizer # type: ignore
from ngx_optimizer.modules.advanced_optimizer import AdvancedOptimizer # type: ignore

app = Flask(__name__)
CORS(app)

# Locate built React frontend for serving
_WEB_DIST = None

def _get_web_dist():
    global _WEB_DIST
    if _WEB_DIST:
        return _WEB_DIST
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _WEB_DIST = os.path.join(base, 'web-ui', 'dist')
    return _WEB_DIST

# Initialize modules
config_manager = ConfigManager()
ram_cleaner = RAMCleaner()
system_monitor = SystemMonitor()
fps_boost = FPSBoost()
network_optimizer = NetworkOptimizer(config_manager=config_manager)
gaming_optimizer = GamingOptimizer(config_manager=config_manager)
network_analyzer = NetworkAnalyzer()
neural_intelligence = NeuralIntelligence()
learning_core = LearningCore()
hardware_controller = HardwareController()
network_evolution = NetworkEvolution()
cloud_link = CloudLink()
ecosystem_integration = EcosystemIntegration()
traffic_shaper = TrafficShaper()
multi_internet = MultiInternet()
lol_optimizer = LoLOptimizer()
advanced_optimizer = AdvancedOptimizer()

# Start background monitoring
system_monitor.start_monitoring(interval=5 if config_manager.get_low_power_mode() else 2)
network_analyzer.start_continuous_analysis(interval=60 if config_manager.get_low_power_mode() else 30)

def neural_loop():
    while True:
        stats = system_monitor.get_current_stats()
        neural_intelligence.add_metrics(stats.get('cpu', 0), stats.get('memory', 0))
        time.sleep(5 if config_manager.get_low_power_mode() else 2)

threading.Thread(target=neural_loop, daemon=True).start()

def learning_loop():
    while True:
        is_gaming = gaming_optimizer.is_optimizing
        learning_core.capture_snapshot(is_gaming)
        if int(time.time()) % 300 == 0: # Save every 5 mins
            learning_core.save_data()
        time.sleep(60)

threading.Thread(target=learning_loop, daemon=True).start()

# Game Detection Auto-Optimization
_detected_game_cache = set()

def game_detection_loop():
    global _detected_game_cache
    while True:
        try:
            current_games = gaming_optimizer._detect_running_games()
            current_names = {g['name'] for g in current_games}
            new_games = current_names - _detected_game_cache
            if new_games:
                gaming_optimizer.optimize_for_gaming()
            _detected_game_cache = current_names
        except Exception:
            pass
        time.sleep(30 if config_manager.get_low_power_mode() else 10)

threading.Thread(target=game_detection_loop, daemon=True).start()

@app.route('/api/detected-games', methods=['GET'])
def get_detected_games():
    try:
        games = gaming_optimizer._detect_running_games()
        return jsonify({'games': games, 'count': len(games)})
    except Exception as e:
        return jsonify({'games': [], 'count': 0, 'error': str(e)})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "active", "version": "2.3.1"})

def _wmic(cmd: str) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=5, shell=True).stdout.strip()
    except Exception:
        return ""

def _get_cpu_name() -> str:
    name = _wmic("wmic cpu get name /format:csv")
    lines = [l.strip() for l in name.splitlines() if l.strip() and ',' in l]
    return lines[-1].split(',', 1)[-1] if lines else platform.processor() or "Unknown"

def _get_gpu_info() -> list:
    out = _wmic("wmic path win32_videocontroller get name,adapterram /format:csv")
    gpus = []
    for line in out.splitlines():
        line = line.strip()
        if not line or ',' not in line:
            continue
        parts = line.split(',')
        if len(parts) >= 3 and parts[1]:
            name = parts[1].strip()
            vram_bytes = parts[2].strip() if len(parts) > 2 else "0"
            gpus.append({'name': name, 'vram_gb': round(int(vram_bytes) / (1024**3), 1) if vram_bytes.isdigit() else 0})
    return gpus

@app.route('/api/system/info', methods=['GET'])
def system_info():
    try:
        import psutil as _psutil
        cpu = _psutil.cpu_freq()
        ram = _psutil.virtual_memory()
        disk = _psutil.disk_usage('/')
        return jsonify({
            'os': f"{platform.system()} {platform.release()}",
            'hostname': platform.node(),
            'cpu': {
                'name': _get_cpu_name(),
                'cores': _psutil.cpu_count(logical=False) or 0,
                'threads': _psutil.cpu_count(logical=True) or 0,
                'frequency_mhz': round(cpu.current, 0) if cpu else 0,
            },
            'ram': {
                'total_gb': round(ram.total / (1024**3), 1),
                'speed_mhz': 0,
            },
            'disk': {
                'total_gb': round(disk.total / (1024**3), 1),
                'free_gb': round(disk.free / (1024**3), 1),
            },
            'gpu': _get_gpu_info(),
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    stats = system_monitor.get_current_stats()
    # Format for frontend
    return jsonify({
        'cpu': round(stats.get('cpu', 0), 1),
        'ram': round(stats.get('memory', 0), 1),
        'timestamp': stats.get('timestamp')
    })

@app.route('/api/optimize/quick', methods=['POST'])
def quick_optimize():
    # Benchmark: capture baseline
    baseline = system_monitor.get_current_stats()
    baseline_ping = network_analyzer.ping_host('8.8.8.8', 2)['avg']

    # Multi-module quick optimization
    freed = ram_cleaner.clean_memory()
    fps_res = fps_boost.optimize_game_performance()
    net_res = network_optimizer.start_network_optimization()

    # Benchmark: capture after
    after = system_monitor.get_current_stats()
    after_ping = network_analyzer.ping_host('8.8.8.8', 2)['avg']

    cpu_diff = after.get('cpu', 0) - baseline.get('cpu', 0)
    ram_diff = after.get('memory', 0) - baseline.get('memory', 0)
    ping_diff = after_ping - baseline_ping if after_ping > 0 and baseline_ping > 0 else 0

    return jsonify({
        'success': True,
        'message': 'Full System Optimization Complete',
        'details': {
            'ram_freed_mb': round(freed, 2),
            'fps_boosted': fps_res.get('processes_optimized', 0) > 0,
            'network_optimized': net_res.get('status') != 'error',
            'tasks': ['Neural RAM Flush', 'CPU Priority Shift', 'Network Stack Tweak']
        },
        'benchmark': {
            'before': {'cpu': round(baseline.get('cpu', 0), 1), 'ram': round(baseline.get('memory', 0), 1), 'ping': round(baseline_ping, 1)},
            'after': {'cpu': round(after.get('cpu', 0), 1), 'ram': round(after.get('memory', 0), 1), 'ping': round(after_ping, 1)},
            'delta': {'cpu': round(cpu_diff, 1), 'ram': round(ram_diff, 1), 'ping': round(ping_diff, 1)}
        }
    })
@app.route('/api/optimize/ram', methods=['POST'])
def clean_ram():
    freed = ram_cleaner.clean_memory()
    return jsonify({
        'success': True,
        'freed_mb': round(freed, 2)
    })

@app.route('/api/optimize/fps', methods=['POST'])
def boost_fps():
    results = fps_boost.optimize_game_performance()
    return jsonify(results)

@app.route('/api/optimize/network', methods=['POST'])
def optimize_network():
    data = request.get_json(silent=True) or {}
    profile = data.get('profile', 'gaming')
    results = network_optimizer.start_network_optimization(profile=profile)
    return jsonify(results)

@app.route('/api/network/speedtest', methods=['POST'])
def run_speedtest():
    results = network_optimizer.run_speed_test()
    return jsonify(results)

@app.route('/api/optimize/gaming', methods=['POST'])
def optimize_gaming():
    results = gaming_optimizer.optimize_for_gaming()
    return jsonify(results)

@app.route('/api/optimize/deep-sleep', methods=['POST'])
def trigger_deep_sleep():
    suspended = learning_core.deep_sleep_background()
    return jsonify({
        'success': True,
        'suspended': suspended,
        'count': len(suspended)
    })

@app.route('/api/optimize/gpu', methods=['POST'])
def toggle_gpu():
    if config_manager.get_low_power_mode():
        return jsonify({'success': False, 'mode': 'LOW POWER MODE - GPU control disabled', 'low_power_mode': True})
    data = request.get_json(silent=True) or {}
    mode = data.get('mode', 'Extreme')
    success = hardware_controller.set_gpu_performance_mode(mode)
    return jsonify({'success': success, 'mode': mode})

@app.route('/api/optimize/network-tunnel', methods=['POST'])
def toggle_tunnel():
    data = request.get_json(silent=True) or {}
    active = data.get('active', True)
    success = network_evolution.toggle_multipath_tunneling(active)
    return jsonify({'success': success, 'active': active})

@app.route('/api/cloud/discord', methods=['POST'])
def toggle_discord():
    data = request.get_json(silent=True) or {}
    active = data.get('active', True)
    success = cloud_link.toggle_discord_presence(active)
    return jsonify({'success': success, 'active': active})

@app.route('/api/ecosystem/launch', methods=['POST'])
def launch_game():
    data = request.get_json(silent=True) or {}
    game = data.get('game', 'Unknown')
    store = data.get('store', 'Steam')
    success = ecosystem_integration.launch_with_boost(game, store)
    return jsonify({'success': success, 'game': game})

@app.route('/api/status', methods=['GET'])
def get_full_status():
    fps_status = fps_boost.get_optimization_status()
    ram_status = ram_cleaner.get_optimization_status()
    net_ifaces = network_optimizer.get_network_interfaces()
    gaming_status = gaming_optimizer.get_gaming_status()
    net_analysis = network_analyzer.get_latest_results()
    
    stats = system_monitor.get_current_stats()
    
    return jsonify({
        'cpu': {'usage': stats.get('cpu', 0)},
        'memory': {'usage': stats.get('memory', 0)},
        'low_power_mode': config_manager.get_low_power_mode(),
        'fps': fps_status,
        'ram': ram_status,
        'gaming': gaming_status,
        'network': {
            'interfaces': net_ifaces,
            'analysis': net_analysis,
            'is_optimizing': network_optimizer.is_optimizing
        },
        'neural': neural_intelligence.get_neural_status(),
        'learning': learning_core.get_learned_insights(),
        'hardware': hardware_controller.get_hardware_status(),
        'net_evolution': network_evolution.get_evolution_status(),
        'cloud': {'status': 'LOW POWER MODE', 'message': 'CloudLink suspended'} if config_manager.get_low_power_mode() else cloud_link.get_cloud_status(),
        'ecosystem': {'status': 'LOW POWER MODE', 'message': 'Ecosystem sync suspended'} if config_manager.get_low_power_mode() else ecosystem_integration.get_ecosystem_status(),
        'traffic': traffic_shaper.get_shaping_status(),
        'multi_internet': multi_internet.get_optimization_status(),
        'lol': lol_optimizer.get_lol_performance_metrics(),
        'lol_servers': lol_optimizer.get_lol_server_latency(),
        'advanced': advanced_optimizer.get_optimization_status()
    })

@app.route('/api/config/low-power', methods=['GET', 'POST'])
def low_power_config():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        enabled = data.get('enabled', False)
        config_manager.set_low_power_mode(enabled)
        return jsonify({'success': True, 'low_power_mode': enabled})
    return jsonify({'low_power_mode': config_manager.get_low_power_mode()})

@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    if request.method == 'POST':
        new_settings = request.json
        config_manager.save_settings(new_settings)
        return jsonify({'success': True})
    
    return jsonify(config_manager.load_settings())

@app.route('/api/traffic-shaper/status', methods=['GET'])
def get_traffic_shaper_status():
    return jsonify(traffic_shaper.get_shaping_status())

@app.route('/api/traffic-shaper/start', methods=['POST'])
def start_traffic_shaping():
    traffic_shaper.start_traffic_shaping()
    return jsonify({'success': True, 'message': 'Traffic shaping started'})

@app.route('/api/traffic-shaper/stop', methods=['POST'])
def stop_traffic_shaping():
    traffic_shaper.stop_traffic_shaping()
    return jsonify({'success': True, 'message': 'Traffic shaping stopped'})

@app.route('/api/traffic-shaper/priority', methods=['POST'])
def toggle_gaming_priority():
    data = request.get_json(silent=True) or {}
    traffic_shaper.gaming_priority_enabled = data.get('enabled', False)
    return jsonify({'success': True, 'gaming_priority': traffic_shaper.gaming_priority_enabled})

@app.route('/api/traffic-shaper/processes', methods=['GET'])
def get_network_processes():
    return jsonify(traffic_shaper.get_network_usage_per_process())

@app.route('/api/multi-internet/connections', methods=['GET'])
def get_multi_connections():
    return jsonify(multi_internet.get_available_connections())

@app.route('/api/multi-internet/status', methods=['GET'])
def get_multi_internet_status():
    return jsonify(multi_internet.get_optimization_status())

@app.route('/api/multi-internet/start', methods=['POST'])
def start_multi_monitoring():
    multi_internet.start_monitoring()
    return jsonify({'success': True, 'message': 'Multi-Internet monitoring started'})

@app.route('/api/multi-internet/stop', methods=['POST'])
def stop_multi_monitoring():
    multi_internet.stop_monitoring()
    return jsonify({'success': True, 'message': 'Multi-Internet monitoring stopped'})

@app.route('/api/lol/optimize', methods=['POST'])
def optimize_lol():
    return jsonify(lol_optimizer.optimize_lol_performance())

@app.route('/api/lol/metrics', methods=['GET'])
def get_lol_metrics():
    return jsonify(lol_optimizer.get_lol_performance_metrics())

@app.route('/api/lol/servers', methods=['GET'])
def get_lol_servers():
    return jsonify(lol_optimizer.get_lol_server_latency())

@app.route('/api/advanced/start', methods=['POST'])
def start_advanced_opt():
    data = request.get_json(silent=True) or {}
    profile = data.get('profile', 'gaming')
    return jsonify(advanced_optimizer.start_advanced_optimization(profile))

@app.route('/api/advanced/stop', methods=['POST'])
def stop_advanced_opt():
    return jsonify({'success': advanced_optimizer.stop_advanced_optimization()})

@app.route('/api/advanced/status', methods=['GET'])
def get_advanced_status():
    return jsonify(advanced_optimizer.get_optimization_status())

# Serve React frontend static files (catch-all route, must be last)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    web_dist = _get_web_dist()
    if not os.path.isdir(web_dist):
        return jsonify({"status": "NGXSMK API running", "version": "2.3.1"})
    if path and os.path.isfile(os.path.join(web_dist, path)):
        return send_from_directory(web_dist, path)
    if os.path.isfile(os.path.join(web_dist, 'index.html')):
        return send_from_directory(web_dist, 'index.html')
    return jsonify({"status": "NGXSMK API running", "version": "2.3.1"})


@app.errorhandler(Exception)
def handle_global_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal Neural Circuit Error',
        'details': str(e)
    }), 500

# ---- Profile Manager ----
_PROFILES_FILE = os.path.join(os.path.dirname(config_manager.config_file), 'profiles.json')

def _load_profiles():
    try:
        if os.path.exists(_PROFILES_FILE):
            with open(_PROFILES_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return []

def _save_profiles(profiles):
    os.makedirs(os.path.dirname(_PROFILES_FILE), exist_ok=True)
    with open(_PROFILES_FILE, 'w') as f:
        json.dump(profiles, f, indent=2)

@app.route('/api/profiles/list', methods=['GET'])
def list_profiles():
    return jsonify({'profiles': _load_profiles()})

@app.route('/api/profiles/save', methods=['POST'])
def save_profile():
    data = request.get_json(force=True)
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Profile name required'}), 400
    profiles = _load_profiles()
    # Update existing profile with same name or append
    now = time.time()
    settings_snapshot = {
        'aggressive_mode': data.get('aggressive_mode', False),
        'auto_optimize': data.get('auto_optimize', False),
    }
    for p in profiles:
        if p['name'] == name:
            p['settings'] = settings_snapshot
            p['updated_at'] = now
            break
    else:
        profiles.append({'name': name, 'settings': settings_snapshot, 'created_at': now, 'updated_at': now})
    _save_profiles(profiles)
    return jsonify({'success': True, 'profiles': profiles})

@app.route('/api/profiles/delete', methods=['POST'])
def delete_profile():
    data = request.get_json(force=True)
    name = data.get('name', '').strip()
    profiles = _load_profiles()
    profiles = [p for p in profiles if p['name'] != name]
    _save_profiles(profiles)
    return jsonify({'success': True, 'profiles': profiles})

@app.route('/api/profiles/apply', methods=['POST'])
def apply_profile():
    data = request.get_json(force=True)
    name = data.get('name', '').strip()
    profiles = _load_profiles()
    for p in profiles:
        if p['name'] == name:
            return jsonify({'success': True, 'settings': p['settings']})
    return jsonify({'error': 'Profile not found'}), 404

def run_server():
    app.run(host='127.0.0.1', port=5000, debug=False)

if __name__ == '__main__':
    print("NGXSMK Backend API starting on http://localhost:5000")
    run_server()
