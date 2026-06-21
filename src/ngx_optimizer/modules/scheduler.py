# pyre-ignore-all-errors
"""
Scheduler Module
Schedule automatic optimization tasks at specific times.
"""

import os
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable

from .compat import get_logger, DATA_DIR # type: ignore
logger = get_logger("scheduler")

ACTIONS = {
    'quick_optimize': 'Full Quick Optimization',
    'clean_ram':      'RAM Clean',
    'boost_fps':      'FPS Boost',
    'optimize_network': 'Network Optimize',
}

class Scheduler:
    def __init__(self):
        self._lock = threading.Lock()
        self._jobs: List[Dict[str, Any]] = []
        self._data_file = os.path.join(DATA_DIR, 'scheduled_jobs.json')
        self._callbacks: Dict[str, Callable] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._load()

    def register_callback(self, action: str, fn: Callable):
        """Register a callback function for an action name."""
        self._callbacks[action] = fn

    def _load(self):
        try:
            if os.path.exists(self._data_file):
                with open(self._data_file, 'r') as f:
                    self._jobs = json.load(f)
        except Exception as e:
            logger.debug("Scheduler load failed: %s", e)
            self._jobs = []

    def _save(self):
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(self._data_file, 'w') as f:
                json.dump(self._jobs, f, indent=2)
        except Exception as e:
            logger.debug("Scheduler save failed: %s", e)

    def add_job(self, action: str, hour: int, minute: int,
                repeat: bool = True, label: str = '') -> Dict[str, Any]:
        """Add a scheduled job."""
        if action not in ACTIONS:
            return {'success': False, 'error': f'Unknown action: {action}'}
        job = {
            'id': int(time.time() * 1000),
            'action': action,
            'label': label or ACTIONS[action],
            'hour': hour,
            'minute': minute,
            'repeat': repeat,
            'enabled': True,
            'last_run': None,
        }
        with self._lock:
            self._jobs.append(job)
        self._save()
        return {'success': True, 'job': job}

    def remove_job(self, job_id: int) -> Dict[str, Any]:
        """Remove a scheduled job by ID."""
        with self._lock:
            before = len(self._jobs)
            self._jobs = [j for j in self._jobs if j['id'] != job_id]
            removed = before > len(self._jobs)
        self._save()
        return {'success': removed}

    def get_jobs(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._jobs)

    def start(self):
        """Start the background scheduler thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _loop(self):
        """Check every 30 seconds if any job should fire."""
        while self._running:
            now = datetime.now()
            with self._lock:
                jobs_snapshot = list(self._jobs)

            for job in jobs_snapshot:
                if not job.get('enabled'):
                    continue
                if job['hour'] == now.hour and job['minute'] == now.minute:
                    last = job.get('last_run')
                    # Only fire once per minute
                    if last is None or (time.time() - last) > 59:
                        self._fire(job)
                        with self._lock:
                            for j in self._jobs:
                                if j['id'] == job['id']:
                                    j['last_run'] = time.time()
                                    if not job['repeat']:
                                        j['enabled'] = False
                        self._save()
            time.sleep(30)

    def _fire(self, job: Dict[str, Any]):
        """Execute a scheduled job."""
        action = job['action']
        logger.info("Scheduler firing: %s (%s)", job['label'], action)
        cb = self._callbacks.get(action)
        if cb:
            try:
                cb()
            except Exception as e:
                logger.error("Scheduled job %s failed: %s", action, e)

    def get_status(self) -> Dict[str, Any]:
        return {
            'is_running': self._running,
            'job_count': len(self._jobs),
            'jobs': self.get_jobs(),
            'available_actions': [
                {'key': k, 'label': v} for k, v in ACTIONS.items()
            ],
        }
