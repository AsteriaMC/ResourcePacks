from rich import print as rprint
from pathlib import Path

from PIL import Image

from src.core.settings import get_settings
from src.core.command import ScriptCommand
from src.fonts.validation import validate_font_providers__unique_chars, validate_font_providers__file_exists
from src.fonts.pack import get_next_available_unicode, ResourcePack, get_all_packs
from src.fonts.font_provider import BitmapProvider
from src.fonts.mappings import write_font_mappings


class FontMappings(ScriptCommand):
    script_name = "font_mappings"
    description = "Writes docs/FONT_MAPPINGS.md of font codes"

    def execute(self):
        out = write_font_mappings(get_all_packs(), get_settings().DOCS_PATH / "FONT_MAPPINGS.md")
        rprint(f"[green]wrote {out}[/green]")

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

class FontAdd(ScriptCommand):
    script_name = "font_add"
    description = "Add new font using .png"

    def execute(self, png : str):
        core = ResourcePack.load(get_settings().PACKS_PATH / 'core')
        textures = core.path / "assets" / "minecraft" / "textures"
        png_path = Path(png).resolve()

        if png_path.suffix != ".png" or not png_path.is_file():
            return rprint(f"[red]{png} must be an existing .png[/red]")
        if not png_path.is_relative_to(textures):
            return rprint(f"[red]put the png under {textures} first[/red]")

        #
        with Image.open(png_path) as img:
            h = img.height
        char = next(get_next_available_unicode())

        # save
        core.fonts.append(BitmapProvider(
            type='bitmap',
            file="minecraft:" + png_path.relative_to(textures).as_posix(),
            height=h,
            ascent=h - 1,
            chars=[char],
            **{"//": char},  # comment
        ))
        core.save_fonts()
        rprint(f"[green]{png_path.name} mapped to \\u{ord(char):04X}[/green]")
        
        #
        FontMappings.execute(None)
