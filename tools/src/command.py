import inspect
from abc import ABC, abstractmethod
from typing import Dict, Type

from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from rich import print as rprint


class ScriptCommand(ABC):
    registry: Dict[str, Type["ScriptCommand"]] = {}
    script_name: str = None
    description: str = ""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if name := cls.__dict__.get("script_name"):
            ScriptCommand.registry[name] = cls

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Subclasses must implement this."""


def script_exists(script_name: str):
    return script_name in ScriptCommand.registry


def valid_args(script_name: str, *args, **kwargs) -> bool:
    cls = ScriptCommand.registry.get(script_name)
    if cls is None:
        raise KeyError(f"No script registered under '{script_name}'")

    cmd = cls()
    try:
        inspect.signature(cmd.execute).bind(*args, **kwargs)  # checks args without running
    except TypeError:
        return False
    return True


def execute(script_name: str, *args, **kwargs):
    cls = ScriptCommand.registry.get(script_name)
    if cls is None:
        raise KeyError(f"No script registered under '{script_name}'")
    return cls().execute(*args, **kwargs)


def panel_commands():
    panels = [
        Panel(
            f"[dim]{cls.description}[/dim]",
            title=f"[bold cyan]{name}[/bold cyan]",
            expand=True,
        )
        for name, cls in sorted(ScriptCommand.registry.items())
    ]
    rprint(Columns(panels))


def list_commands():
    table = Table(title="Scripts", show_lines=False, expand=False)
    table.add_column("Script", style="bold cyan", no_wrap=True)
    table.add_column("Description", style="dim")

    for name, cls in sorted(ScriptCommand.registry.items()):
        table.add_row(name, cls.description or "-")

    rprint(table)
