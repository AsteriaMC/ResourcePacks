from typing import Annotated, Literal, Union
import json
from pathlib import Path
from dataclasses import dataclass

from pydantic import BaseModel, Field, TypeAdapter, model_validator, ConfigDict

from src.core.settings import get_settings

""" 
"//": "\uE000",
            "type": "bitmap",
            "file": "minecraft:font/ranks/rank_patreon.png",
            "ascent": 7,
            "height": 8,
            "chars": [
                ""
            ]
"""

class FontUnicodeRange:
    START = 0xE800
    END = 0xF8FF


class BitmapProvider(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: Literal["bitmap"]
    file: str
    ascent: int
    height: int
    chars: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def _check(self):
        #
        if self.ascent > self.height:
            raise ValueError(f"ascent {self.ascent} > height {self.height}")
        
        # 
        widths = {len(row) for row in self.chars}
        if len(widths) > 1:
            raise ValueError("all chars rows must be the same length")

        return self

    def texture_path(self, pack_root):
        ns, _, path = self.file.rpartition(":")
        return pack_root / "assets" / (ns or "minecraft") / "textures" / path

# add more providers here
FontProvider = Annotated[
    Union[BitmapProvider,],
    Field(discriminator="type"),
]

class FontFile(BaseModel):
    """ for loading defaults.json
    >> FontFile.model_validate_json(path.read_text("utf-8"))
    """
    providers: list[FontProvider]

