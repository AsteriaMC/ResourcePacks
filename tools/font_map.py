from font_provider import get_font_providers, get_font_cache, FontUnicodeRange


def test_font_providers_all_unique():
    providers = get_font_providers()
    chars = set()
    for p in providers:
        for c in p.chars:
            assert c not in chars, f"Collision Error: '{c}' is already taken. " \
                f"Check font that uses: {p.file}"
            chars.add(c)

def get_next_available_code():
    current = FontUnicodeRange.START
    fs = get_font_cache()

    for i in range(FontUnicodeRange.START, FontUnicodeRange.END, 1):
        c = chr(i)
        if c in fs: continue
        yield c


def main():
    test_font_providers_all_unique()
    codes = get_next_available_code()
    print(next(codes))

if __name__ == '__main__':
    main()
