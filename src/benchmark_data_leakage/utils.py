from pathlib import Path


def find_repo_root(path=Path.cwd()):
    if (path / "pyproject.toml").exists():
        return path
    return find_repo_root(path.parent)