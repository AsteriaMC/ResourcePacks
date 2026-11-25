from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_PACKS_PATH = ROOT / 'packs'
_DIST_PATH = ROOT / 'dist'

class Settings:
    PACKS_PATH: Path = _PACKS_PATH
    DIST_PATH: Path = _DIST_PATH

@lru_cache
def get_settings():
    return Settings()
