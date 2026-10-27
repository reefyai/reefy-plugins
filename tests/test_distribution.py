"""Package artifacts have exact provenance, complete resources and no host state."""
import json
from pathlib import Path
import zipfile

from package import render_package
from tools.build import write_archive


def test_reproducible_zip_and_exact_bundle(tmp_path):
    files = render_package('reefy.dev')
    first, second = tmp_path / 'first.zip', tmp_path / 'second.zip'
    write_archive(first, files)
    write_archive(second, files)
    assert first.read_bytes() == second.read_bytes()
    with zipfile.ZipFile(first) as archive:
        assert {name: archive.read(name) for name in archive.namelist()} == files
        assert '.app.json' not in archive.namelist()
        assert '.git' not in archive.namelist()
        assert not any(name.endswith(('.key', '.pem', '.raw')) for name in archive.namelist())


def test_public_sources_do_not_name_private_repositories_or_infrastructure():
    root = Path(__file__).resolve().parents[1]
    files = list((root / 'shared').rglob('*.md')) + list((root / 'providers').rglob('*.md'))
    files += list((root / 'plugins').rglob('*.md'))
    files += list((root / 'docs').rglob('*.md')) + [root / 'README.md', root / 'AGENTS.md']
    forbidden = ('reefy-service', 'big-bird', '/Users/', 'configs/reefy-', 'app/routes/', 'app/services/')
    for path in files:
        text = path.read_text()
        assert not any(value in text for value in forbidden), path
        assert '\u2014' not in text, path


def test_shared_skill_is_used_in_both_environments():
    source = Path('shared/skills/reefy-setup/SKILL.md').read_bytes()
    for domain in ('reefy.dev', 'reefy.ai'):
        assert render_package(domain)['skills/reefy-setup/SKILL.md'] == source


def test_reefy_icon_is_bundled_unchanged_and_meets_submission_dimensions():
    import struct
    source = Path('providers/chatgpt/plugin/assets/reefy.png').read_bytes()
    assert source.startswith(b'\x89PNG\r\n\x1a\n')
    width, height = struct.unpack('>II', source[16:24])
    assert 48 <= width == height <= 4096
    assert len(source) <= 5 * 1024 * 1024
    for domain in ('reefy.dev', 'reefy.ai'):
        assert render_package(domain)['assets/reefy.png'] == source
