import yaml
from pathlib import Path

def load_config(path="config/base.yaml"):
  with open(path, "r") as f:
    return yaml.safe_load(f)