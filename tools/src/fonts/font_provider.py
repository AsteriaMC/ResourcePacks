import json
from pathlib import Path
from dataclasses import dataclass

from src.settings import get_settings


class FontUnicodeRange:
    START = 0xE000
    END = 0xF8FF

""" 
"//": "\uE000",
            "type": "bitmap",
            "file": "minecraft:font/ranks/rank_patreon.png",
            "ascent": 7,
            "height": 8,
            "chars": [
                ""
            ]
"""
@dataclass
class FontProvider:
    type_: str
    file: str
    ascent: int 
    height: int
    chars: list[str] 

    @classmethod
    def from_dict(cls, d):
        return cls(
            type_=d["type"],
            file=d["file"],
            ascent=int(d["ascent"]),
            height=int(d.get("height", 8)),  # minecraft defaults height to 8
            chars=d["chars"],
        )

    @classmethod
    def get_font_providers(cls, file_paths : list[Path]):
        """ list of bitmap FontProvider objects
        (reference/space/ttf providers have no file/chars and are skipped)
        """
        ret = []

        for fpath in file_paths:
            with open(fpath, 'r', encoding="utf-8") as f:
                data = json.load(f)
                for provider in data.get('providers', []):
                    if provider.get('type') != 'bitmap':
                        continue
                    p = cls.from_dict(provider)
                    ret.append(p)

        return ret
