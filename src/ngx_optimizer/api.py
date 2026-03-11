# pyre-ignore-all-errors
import sys
import os
from flask import Flask, jsonify, request # type: ignore
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

app = Flask(__name__)
CORS(app)

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

# Start background monitoring
system_monitor.start_monitoring(interval=2)
network_analyzer.start_continuous_analysis(interval=30)

def neural_loop():
    while True:
        stats = system_monitor.get_current_stats()
        neural_intelligence.add_metrics(stats.get('cpu', 0), stats.get('memory', 0))
        time.sleep(2)

threading.Thread(target=neural_loop, daemon=True).start()

def learning_loop():
    while True:
        is_gaming = gaming_optimizer.is_optimizing
        learning_core.capture_snapshot(is_gaming)
        if int(time.time()) % 300 == 0: # Save every 5 mins
            learning_core.save_data()
        time.sleep(60)

threading.Thread(target=learning_loop, daemon=True).start()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "active", "version": "2.2.6"})

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
    # Multi-module quick optimization
    freed = ram_cleaner.clean_memory()
    fps_res = fps_boost.optimize_game_performance()
    net_res = network_optimizer.start_network_optimization()
    
    return jsonify({
        'success': True,
        'message': 'Full System Optimization Complete',
        'details': {
            'ram_freed_mb': round(freed, 2),
            'fps_boosted': fps_res.get('processes_optimized', 0) > 0,
            'network_optimized': net_res.get('status') != 'error',
            'tasks': ['Neural RAM Flush', 'CPU Priority Shift', 'Network Stack Tweak']
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
        'cloud': cloud_link.get_cloud_status(),
        'ecosystem': ecosystem_integration.get_ecosystem_status()
    })

@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    if request.method == 'POST':
        new_settings = request.json
        config_manager.save_settings(new_settings)
        return jsonify({'success': True})
    
    return jsonify(config_manager.load_settings())

@app.errorhandler(Exception)
def handle_global_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal Neural Circuit Error',
        'details': str(e)
    }), 500

def run_server():
    app.run(host='127.0.0.1', port=5000, debug=False)

if __name__ == '__main__':
    print("NGXSMK Backend API starting on http://localhost:5000")
    run_server()
