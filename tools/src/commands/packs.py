from rich import print as rprint

from src.core.command import ScriptCommand
from src.fonts.pack import get_all_packs
from src.core.settings import get_settings

class PacksCreateResourcePack(ScriptCommand):
    script_name = "packs_zip"
    description = "Creates a resource pack and puts in in dist"

    def execute(self):
        s = get_settings() 
        for i, pack in enumerate(get_all_packs()):
            pack.zip(s.DIST_PATH, f'{i}.zip')

