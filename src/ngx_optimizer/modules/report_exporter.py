# pyre-ignore-all-errors
"""
Report Exporter Module
Generates a full system health and performance report.
"""

import json
import os
import time
import platform
from datetime import datetime
from typing import Dict, Any, Optional, Callable

from .compat import get_logger, DATA_DIR # type: ignore
logger = get_logger("report_exporter")

class ReportExporter:
    def __init__(self):
        self._collectors: Dict[str, Callable] = {}

    def register(self, key: str, fn: Callable):
        """Register a data collector function."""
        self._collectors[key] = fn

    def generate(self) -> Dict[str, Any]:
        """Generate a full system report."""
        report: Dict[str, Any] = {
            'meta': {
                'generated_at': datetime.now().isoformat(),
                'version': '2.3.1',
                'os': f"{platform.system()} {platform.release()}",
                'hostname': platform.node(),
                'machine': platform.machine(),
            },
            'sections': {}
        }

        for key, fn in self._collectors.items():
            try:
                report['sections'][key] = fn()
            except Exception as e:
                report['sections'][key] = {'error': str(e)}

        return report

    def export_to_file(self) -> Dict[str, Any]:
        """Generate report and save to disk."""
        try:
            report = self.generate()
            os.makedirs(DATA_DIR, exist_ok=True)
            fname = f"report_{int(time.time())}.json"
            fpath = os.path.join(DATA_DIR, fname)
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
            return {
                'success': True,
                'file': fpath,
                'report': report
            }
        except Exception as e:
            logger.error("Report export failed: %s", e)
            return {'success': False, 'error': str(e)}
