import os
import json

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".cnp")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)