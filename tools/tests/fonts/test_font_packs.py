from src.fonts.validation import validate_font_providers__unique_chars, validate_font_providers__file_exists

def test_font_providers_all_unique():
    validate_font_providers__unique_chars()

def test_font_providers__file_exists():
    validate_font_providers__file_exists()
