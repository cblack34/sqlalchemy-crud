import toml
from pathlib import Path

toml_path = Path(__file__).parent.parent / "pyproject.toml"
with open(toml_path, "r") as f:
    pyprojectToml = toml.load(f)

__version__ = pyprojectToml["tool"]["poetry"]["version"]
