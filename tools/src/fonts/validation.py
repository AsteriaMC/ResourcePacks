from pathlib import Path
from .font_provider import BitmapProvider
from .pack import get_all_packs


def validate_font_providers__unique_chars():
    chars = {}
    for pack in get_all_packs():
        for p in pack.fonts:
            
            if isinstance(p, BitmapProvider):
                for row in p.chars:
                    for c in row:
                        assert c not in chars, f"Collision Error: U+{ord(c):04X} is already taken " \
                            f"by {chars[c]}, also used by {p.file}"
                        chars[c] = p.file

def validate_font_providers__file_exists():
    missing = []
    for pack in get_all_packs():
        for p in pack.fonts:

            if isinstance(p, BitmapProvider) and not p.texture_path(pack.path).is_file():
                missing.append(f"{pack.path.name}: {p.file}")

    assert not missing, "Missing textures:\n  " + "\n  ".join(missing)
