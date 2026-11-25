from functools import lru_cache
from pathlib import Path

ROOT = Path('')
_PACKS_PATH = ROOT / Path('packs')

class Settings:
    PACKS_PATH: str = _PACKS_PATH

@lru_cache
def get_settings():
    return Settings()
