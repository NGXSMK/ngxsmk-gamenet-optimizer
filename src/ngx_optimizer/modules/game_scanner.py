# pyre-ignore-all-errors
"""
Game Scanner Module
Scans Steam, Epic Games, Riot, and Ubisoft libraries for installed games.
"""

import os
import json
import re
import subprocess
from typing import Dict, List, Any, Optional

from .compat import get_logger # type: ignore
logger = get_logger("game_scanner")

class GameScanner:
    def __init__(self):
        self._cache: List[Dict[str, Any]] = []

    # ── Steam ────────────────────────────────────────────────────────────────
    def _scan_steam(self) -> List[Dict[str, Any]]:
        games = []
        steam_root = r"C:\Program Files (x86)\Steam"
        lib_file = os.path.join(steam_root, 'steamapps', 'libraryfolders.vdf')
        if not os.path.exists(lib_file):
            return games

        # Parse VDF to find all library paths
        library_paths = [os.path.join(steam_root, 'steamapps')]
        try:
            with open(lib_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            for m in re.finditer(r'"path"\s+"([^"]+)"', content):
                path = m.group(1).replace('\\\\', '\\')
                apps_path = os.path.join(path, 'steamapps')
                if os.path.isdir(apps_path):
                    library_paths.append(apps_path)
        except Exception as e:
            logger.debug("Steam VDF parse error: %s", e)

        for lib in library_paths:
            try:
                for fname in os.listdir(lib):
                    if fname.startswith('appmanifest_') and fname.endswith('.acf'):
                        acf_path = os.path.join(lib, fname)
                        try:
                            with open(acf_path, 'r', encoding='utf-8', errors='ignore') as f:
                                text = f.read()
                            name_m = re.search(r'"name"\s+"([^"]+)"', text)
                            appid_m = re.search(r'"appid"\s+"([^"]+)"', text)
                            if name_m:
                                games.append({
                                    'name': name_m.group(1),
                                    'store': 'Steam',
                                    'app_id': appid_m.group(1) if appid_m else '',
                                    'launch_cmd': f'steam://rungameid/{appid_m.group(1)}' if appid_m else ''
                                })
                        except Exception:
                            pass
            except Exception:
                pass
        return games

    # ── Epic Games ───────────────────────────────────────────────────────────
    def _scan_epic(self) -> List[Dict[str, Any]]:
        games = []
        launcher_data = os.path.join(
            os.environ.get('PROGRAMDATA', r'C:\ProgramData'),
            'Epic', 'EpicGamesLauncher', 'Data', 'Manifests'
        )
        if not os.path.isdir(launcher_data):
            return games
        try:
            for fname in os.listdir(launcher_data):
                if fname.endswith('.item'):
                    try:
                        with open(os.path.join(launcher_data, fname), 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        name = data.get('DisplayName') or data.get('AppName', 'Unknown')
                        app_name = data.get('AppName', '')
                        games.append({
                            'name': name,
                            'store': 'Epic Games',
                            'app_id': app_name,
                            'launch_cmd': f'com.epicgames.launcher://apps/{app_name}?action=launch'
                        })
                    except Exception:
                        pass
        except Exception as e:
            logger.debug("Epic scan error: %s", e)
        return games

    # ── Riot Games ───────────────────────────────────────────────────────────
    def _scan_riot(self) -> List[Dict[str, Any]]:
        games = []
        riot_root = r"C:\Riot Games"
        if not os.path.isdir(riot_root):
            return games
        riot_games = {
            'League of Legends': 'league-of-legends',
            'VALORANT': 'valorant',
            'Teamfight Tactics': 'teamfight-tactics',
        }
        for name, product in riot_games.items():
            game_path = os.path.join(riot_root, name)
            if os.path.isdir(game_path):
                games.append({
                    'name': name,
                    'store': 'Riot',
                    'app_id': product,
                    'launch_cmd': f'riotclient://launch-product/{product}/patchline/live'
                })
        return games

    # ── Ubisoft ──────────────────────────────────────────────────────────────
    def _scan_ubisoft(self) -> List[Dict[str, Any]]:
        games = []
        ubi_dirs = [
            r"C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games",
            r"C:\Program Files\Ubisoft\Ubisoft Game Launcher\games",
        ]
        for root in ubi_dirs:
            if os.path.isdir(root):
                try:
                    for entry in os.scandir(root):
                        if entry.is_dir():
                            games.append({
                                'name': entry.name,
                                'store': 'Ubisoft',
                                'app_id': '',
                                'launch_cmd': ''
                            })
                except Exception as e:
                    logger.debug("Ubisoft scan error: %s", e)
        return games

    def scan_all(self) -> List[Dict[str, Any]]:
        """Scan all game stores and return combined library."""
        all_games: List[Dict[str, Any]] = []
        all_games.extend(self._scan_steam())
        all_games.extend(self._scan_epic())
        all_games.extend(self._scan_riot())
        all_games.extend(self._scan_ubisoft())
        # Sort alphabetically
        all_games.sort(key=lambda g: g['name'].lower())
        self._cache = all_games
        return all_games

    def get_library(self) -> Dict[str, Any]:
        """Return cached library or rescan."""
        if not self._cache:
            self.scan_all()
        by_store: Dict[str, List[str]] = {}
        for g in self._cache:
            store = g['store']
            by_store.setdefault(store, []).append(g['name'])
        return {
            'games': self._cache,
            'total': len(self._cache),
            'by_store': {s: len(v) for s, v in by_store.items()}
        }

    def launch_game(self, launch_cmd: str) -> Dict[str, Any]:
        """Launch a game via its store URI."""
        if not launch_cmd:
            return {'success': False, 'error': 'No launch command'}
        try:
            subprocess.Popen(['cmd', '/c', 'start', '', launch_cmd], shell=False)
            return {'success': True, 'launched': launch_cmd}
        except Exception as e:
            logger.debug("Game launch failed: %s", e)
            return {'success': False, 'error': str(e)}
