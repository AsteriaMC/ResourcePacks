import zipfile
from pathlib import Path
from dataclasses import dataclass, field

from src.core.settings import get_settings
from .font_provider import FontFile, FontProvider, FontUnicodeRange, BitmapProvider


class _FontMixin:

    def get_used_characters(self):
        """ returns a set of characters that are used by FontProviders """
        char = set()
        for p in self.fonts:

            if isinstance(p, BitmapProvider):
                for row in p.chars:
                    char.update(row)

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
        font_paths = path.rglob('assets/*/font/default.json')
        fonts = []
        for font_path in font_paths:
            fonts += FontFile.model_validate_json(font_path.read_text("utf-8")).providers

        return cls(
            path=path,
            fonts=fonts,
        )

    def zip(self, dest : Path, name : str):
        """ zips everything in self.path except filtered to dest path"""
        with zipfile.ZipFile(dest / name, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in self.path.rglob('*'):
                if file.is_file():
                    zf.write(file, arcname=file.relative_to(self.path))

def get_all_packs():
    """ every folder under PACKS_PATH that has a pack.mcmeta,
    skipping packs nested inside another pack.
    """
    pack_path = get_settings().PACKS_PATH
    roots = sorted(m.parent for m in pack_path.rglob("pack.mcmeta"))
    top_level = [r for r in roots if not any(p in roots for p in r.parents)]
    return [ResourcePack.load(r) for r in top_level]

def get_next_available_unicode():
    # 
    used = set()
    for pack in get_all_packs():
        used |= pack.get_used_characters()

    #
    for i in range(FontUnicodeRange.START, FontUnicodeRange.END, 1):
        c = chr(i)
        if c in used: continue
        yield c
