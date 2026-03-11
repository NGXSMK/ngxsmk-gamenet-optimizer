# pyre-ignore-all-errors
"""
Neural Intelligence Module
Provides predictive bottleneck analysis and system stability scoring
"""

import time
from typing import Dict, List, Any, Optional
from datetime import datetime

from .compat import get_logger # type: ignore
logger = get_logger("neural_intelligence")

class NeuralIntelligence:
    def __init__(self, history_limit: int = 50):
        self.history_limit = history_limit
        self.metric_history: List[Dict[str, Any]] = []
        self.stability_score: float = 100.0
        self.predicted_bottleneck: Optional[str] = None
        
    def add_metrics(self, cpu: float, ram: float):
        """Add new metrics to history for analysis"""
        self.metric_history.append({
            'cpu': cpu,
            'ram': ram,
            'timestamp': time.time()
        })
        
        if len(self.metric_history) > self.history_limit:
            self.metric_history.pop(0)
            
        self._analyze_stability()

    def _analyze_stability(self):
        """Calculate system stability based on variance and trends"""
        count = len(self.metric_history)
        if count < 5:
            return

        cpus = [m['cpu'] for m in self.metric_history]
        rams = [m['ram'] for m in self.metric_history]
        
        # Pure Python Variance (Volatility)
        def get_std(data: List[float]):
            avg = sum(data) / len(data)
            variance = sum((x - avg) ** 2 for x in data) / len(data)
            return variance ** 0.5

        cpu_volatility = get_std(cpus)
        ram_volatility = get_std(rams)
        
        # Pure Python Slope (Linear Regression)
        def get_slope(data: List[float]):
            n = len(data)
            x = list(range(n))
            sum_x = sum(x)
            sum_y = sum(data)
            sum_xy = sum(i * data[i] for i in range(n))
            sum_x2 = sum(i * i for i in range(n))
            denominator = (n * sum_x2 - sum_x**2)
            if denominator == 0: return 0.0
            return (n * sum_xy - sum_x * sum_y) / denominator

        cpu_slope = get_slope(cpus)
        
        # Neural Stability Calculation
        base_stability = 100.0
        penalty = (cpu_volatility * 0.5) + (ram_volatility * 0.8)
        
        if cpu_slope > 2.0:
            penalty += 10
            
        self.stability_score = float(max(0.0, min(100.0, base_stability - penalty)))
        
        # Predictive Bottleneck Logic
        if cpu_slope > 1.5 and cpus[-1] > 70:
            self.predicted_bottleneck = "POTENTIAL CPU SPIKE"
        elif rams[-1] > 85:
            self.predicted_bottleneck = "RAM EXHAUSTION RISK"
        elif cpu_volatility > 15:
            self.predicted_bottleneck = "UNSTABLE LOAD DETECTED"
        else:
            self.predicted_bottleneck = "OPTIMAL"

        if self.stability_score > 95:
            rank = "ELITE"
        elif self.stability_score > 80:
            rank = "STABLE"
        else:
            rank = "CAUTION"

        return {
            'stability_score': float(f"{self.stability_score:.1f}"),
            'stability_rank': rank,
            'predicted_bottleneck': self.predicted_bottleneck,
            'trend': "UPWARDS" if cpu_slope < -0.5 else "STABLE",
            'history': self.metric_history[-30:],  # type: ignore
            'timestamp': datetime.now().isoformat()
        }
