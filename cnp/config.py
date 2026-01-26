import os
import json

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".cnp")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)

def save_config(data):
    ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)