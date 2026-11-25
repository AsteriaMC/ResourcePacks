from pathlib import Path
from dataclasses import dataclass, field

from src.settings import get_settings
from .font_provider import FontProvider, FontUnicodeRange


class _FontMixin:

    def get_used_characters(self):
        """ returns a set of characters that are used by FontProviders """
        char = set()
        for p in self.fonts:
            for row in p.chars:
                char.update(row)  # a row can hold several chars

        return char

    def get_next_available_unicode(self):
        """ get an unused unicode not used by font """
        fs = self.get_used_characters()

        for i in range(FontUnicodeRange.START, FontUnicodeRange.END, 1):
            c = chr(i)
            if c in fs: continue
            yield c

@dataclass
class ResourcePack(_FontMixin):
    path : Path = field(default_factory=Path)
    fonts : list[FontProvider] = field(default_factory=list)

    @classmethod
    def load(cls, path : Path):
        # get fonts (base pack + any overlay folders like nexo_1_21_4/)
        font_paths = path.rglob('assets/*/font/default.json')
        fonts = FontProvider.get_font_providers(font_paths)

        return cls(
            path=path,
            fonts=fonts,
        )


def get_all_packs():
    """ every folder under PACKS_PATH that has a pack.mcmeta,
    skipping packs nested inside another pack.
    """
    pack_path = get_settings().PACKS_PATH
    roots = sorted(m.parent for m in pack_path.rglob("pack.mcmeta"))
    top_level = [r for r in roots if not any(p in roots for p in r.parents)]
    return [ResourcePack.load(r) for r in top_level]
