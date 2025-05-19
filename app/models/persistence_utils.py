import json
from pathlib import Path

def load_json(file_path):
    """Carga datos desde un archivo JSON"""
    path = Path(file_path)
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_json(data, file_path):
    """Guarda datos en un archivo JSON"""
    path = Path(file_path)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)