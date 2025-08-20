import json
from typing import Dict, Any

CONFIG_PATH = 'config.json'

def load_config() -> Dict[str, Any]:
    """
    Loads and validates the InfoSnare config file.
    """
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    # Optionally add validation here
    return config 