import json
from dataclasses import dataclass
from functools import lru_cache

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
            height=int(d["height"]),
            chars=d["chars"],
        )

def get_font_files():
    pack_path = get_settings().PACKS_PATH
    return pack_path.rglob('*/assets/*/font/default.json')


@lru_cache
def get_font_providers():
    """ list of FontProvider objects"""
    ret = []

    for fpath in get_font_files():
        with open(fpath, 'r', encoding="utf-8") as f:
            data = json.load(f)
            for provider in data.get('providers', []):
                p = FontProvider.from_dict(provider)
                ret.append(p)

    return ret

@lru_cache
def get_font_cache():
    """ returns a set of characters that are used by FontProviders """
    ret = set()

    for p in get_font_providers():
        for c in p.chars:
            ret.add(c)

    return ret

def get_next_available_code():
    current = FontUnicodeRange.START
    fs = get_font_cache()

    for i in range(FontUnicodeRange.START, FontUnicodeRange.END, 1):
        c = chr(i)
        if c in fs: continue
        yield c
