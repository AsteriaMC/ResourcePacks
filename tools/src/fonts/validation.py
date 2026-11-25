from .font_provider import get_font_providers, get_font_cache, FontUnicodeRange

def validate_font_providers_all_unique():
    providers = get_font_providers()
    chars = set()
    for p in providers:
        for c in p.chars:
            assert c not in chars, f"Collision Error: '{c}' is already taken. " \
                f"Check font that uses: {p.file}"
            chars.add(c)
