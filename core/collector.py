import json
import os
from typing import Dict, Any

CONFIG_PATH = 'config.json'

class InfoSnareCollector:
    """
    Main orchestrator for InfoSnare. Loads plugins, reads config, and manages data collection loop.
    """
    def __init__(self):
        self.config = self.load_config()
        self.plugins = {}

    def load_config(self) -> Dict[str, Any]:
        if not os.path.exists(CONFIG_PATH):
            raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)

    def load_plugins(self):
        # Will dynamically import enabled plugins
        pass

    def run(self):
        # Main loop stub
        pass 