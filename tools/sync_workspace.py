"""Regenerate the checked-in workspace bundle from authoritative sources."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from package import render_workspace_package


def sync_workspace():
    destination = ROOT / 'plugins/reefy-dev'
    files = render_workspace_package()
    existing = {path.relative_to(destination).as_posix(): path
                for path in destination.rglob('*') if path.is_file()}
    for name, path in existing.items():
        if name not in files:
            path.unlink()
    for name, content in files.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


if __name__ == '__main__':
    sync_workspace()
