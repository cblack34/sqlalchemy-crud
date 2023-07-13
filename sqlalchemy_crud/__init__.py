import tomllib
from pathlib import Path

toml_path = Path(__file__).parent.parent / "pyproject.toml"
with open(toml_path, "rb") as f:
    pyprojectToml = tomllib.load(f)

__version__ = pyprojectToml["tool"]["poetry"]["version"]
