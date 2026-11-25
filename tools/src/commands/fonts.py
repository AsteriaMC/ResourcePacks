from rich import print as rprint

from src.command import ScriptCommand
from src.fonts.validation import validate_font_providers_all_unique

class ValidateFontCodes(ScriptCommand):
    script_name = "validate_font_codes"
    description = "Ensures font codes are all unique. No collisions have occurred"

    def execute(self):
        rprint("[green]Validating fonts...[/green]")
        validate_font_providers_all_unique()
        rprint("[green]done.[/green]")
