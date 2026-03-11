# pyre-ignore-all-errors
"""
Dynamic Learning Core Module
Learns user habits and optimizes background processes based on gaming patterns.
"""

import os
import json
import time
from typing import Dict, List, Set, Any, Optional
from threading import Lock

from .compat import get_psutil, get_logger # type: ignore
psutil = get_psutil()
logger = get_logger("learning_core")

class LearningCore:
    def __init__(self, data_file: Optional[str] = None):
        if data_file is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_file = os.path.join(project_root, "learning_data.json")
        
        self.data_file = data_file
        self.lock = Lock()
        self.habit_profiles: Dict[str, Any] = {
            'common_background_procs': {}, # proc_name -> count when NOT gaming
            'gaming_background_procs': {}, # proc_name -> count when gaming
            'suspended_candidates': [],
            'learned_at': time.time()
        }
        self.load_data()
        
    def load_data(self):
        """Load learned habit data from disk"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.habit_profiles = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load learning data: {e}")

    def save_data(self):
        """Persist learned habit data to disk"""
        try:
            with self.lock:
                with open(self.data_file, 'w') as f:
                    json.dump(self.habit_profiles, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save learning data: {e}")

    def capture_snapshot(self, is_gaming: bool):
        """Record a snapshot of running processes to learn patterns"""
        current_procs: Set[str] = set()
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    current_procs.add(proc.info['name'].lower())
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            with self.lock:
                target_map = 'gaming_background_procs' if is_gaming else 'common_background_procs'
                for name in current_procs:
                    self.habit_profiles[target_map][name] = self.habit_profiles[target_map].get(name, 0) + 1
                
                # Update candidates for deep sleep
                # Candidates are procs that are FREQUENT in common use but RARE/NOT present in high-performance gaming sessions
                # or procs that the user manually kills often.
                self._update_candidates()
                
        except Exception as e:
            logger.debug(f"Snapshot capture failed: {e}")

    def _update_candidates(self):
        """Analyze profiles to find high-impact suspension candidates"""
        common = self.habit_profiles['common_background_procs']
        gaming = self.habit_profiles['gaming_background_procs']
        
        candidates: List[str] = []
        # Simple heuristic: often running normally, but rarely running when we've manually optimized
        for name, count in common.items():
            if count > 10: # Sufficient data
                gaming_count = gaming.get(name, 0)
                if gaming_count < (count * 0.1): # Less than 10% overlap
                    if name not in ['explorer.exe', 'taskhostw.exe', 'svchost.exe', 'api.py', 'electron.exe']:
                        candidates.append(str(name))
        
        self.habit_profiles['suspended_candidates'] = [c for i, c in enumerate(candidates) if i < 10]

    def get_learned_insights(self) -> Dict[str, Any]:
        """Return insights for UI"""
        with self.lock:
            return {
                'candidates': self.habit_profiles['suspended_candidates'],
                'learning_progress': float(min(100.0, (sum(self.habit_profiles['common_background_procs'].values()) / 1000.0) * 100.0)),
                'total_procs_tracked': len(self.habit_profiles['common_background_procs']),
                'last_updated': self.habit_profiles.get('learned_at')
            }

    def deep_sleep_background(self) -> List[str]:
        """Actually suspend detected low-use background processes"""
        suspended = []
        candidates = self.habit_profiles['suspended_candidates']
        
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                name = proc.info['name'].lower()
                if name in candidates:
                    proc.suspend()
                    suspended.append(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return suspended

    def wake_background(self):
        """Resume suspended processes"""
        candidates = self.habit_profiles['suspended_candidates']
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                name = proc.info['name'].lower()
                if name in candidates:
                    proc.resume()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.InternalError):
                continue
