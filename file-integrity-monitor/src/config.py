from pathlib import Path
import configparser

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = BASE_DIR / "config.ini"

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

MONITOR_PATH = str(BASE_DIR / config["monitor"]["path"])
SCAN_INTERVAL = int(config["monitor"]["scan_interval"])
HASH_ALGORITHM = config["hashing"]["algorithm"]
