from .pack import get_all_packs


def validate_font_providers_all_unique():
    packs = get_all_packs()
    chars = {}
    for pack in packs:
        for provider in pack.fonts:
            for row in provider.chars:
                for c in row:  # a row can hold several chars (grid sprite sheets)
                    assert c not in chars, f"Collision Error: U+{ord(c):04X} is already taken " \
                        f"by {chars[c]}, also used by {provider.file}"
                    chars[c] = provider.file
