from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_PACKS_PATH = ROOT / 'packs'

class Settings:
    PACKS_PATH: Path = _PACKS_PATH

@lru_cache
def get_settings():
    return Settings()
