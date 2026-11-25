from rich import print as rprint

from src.command import ScriptCommand
from src.fonts.validation import validate_font_providers__unique_chars, validate_font_providers__file_exists
from src.fonts.pack import get_next_available_unicode

class ValidateFontCodes(ScriptCommand):
    script_name = "validate_font_codes"
    description = "Ensures font codes are all unique. No collisions have occurred"

    def execute(self):
        rprint("[green]Validating fonts...[/green]")
        validate_font_providers__unique_chars()
        rprint("[green]done.[/green]")

class ValidateFontFiles(ScriptCommand):
    script_name = "validate_font_files"
    description = "Ensures all fonts have a file and that it exists"

    def execute(self):
        rprint("[green]Validating font files...[/green]")
        validate_font_providers__file_exists()
        rprint("[green]done.[/green]")

class FontAvailableUnicode(ScriptCommand):
    script_name = "font_get_available_unicode"
    description = "Gets the first available unicode from 'Private Use Areas'"

    def execute(self):
        codes = get_next_available_unicode()
        code = next(codes)
        rprint(f"char({hex(ord(code))}): {code}")
