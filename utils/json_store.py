import json
from pathlib import Path


def save_json(data, file_path: str) -> None:
    """
    Save a dictionary or list into a JSON file.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_json(file_path: str):
    """
    Load JSON data from file. Returns None if file does not exist.
    """
    path = Path(file_path)

    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
