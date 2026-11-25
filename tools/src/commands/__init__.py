import importlib
import pkgutil

for _mod in pkgutil.walk_packages(__path__, __name__ + "."):
    importlib.import_module(_mod.name)
