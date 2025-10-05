from typing import Dict, List, Tuple
import json


def load_user_agents(path: str) -> Dict[str, List[Tuple[str, str]]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise SystemExit(f"File with User-Agent not found: {path}") from e
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid JSON in {path}: {e}") from e

    norm = {}
    for engine, mapping in data.items():
        eng = str(engine).lower().strip()
        if isinstance(mapping, dict):
            norm[eng] = [(str(name), str(ua)) for name, ua in mapping.items()]
        elif isinstance(mapping, list):
            norm[eng] = [ua for ua in mapping]
        elif isinstance(mapping, str):
            norm[eng] = [mapping]
        else:
            norm[eng] = []
    return norm
