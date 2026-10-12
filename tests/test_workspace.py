"""The importable bundle must resolve to one existing connection and shared source."""
import json
from pathlib import Path
import pytest

from package import render_workspace_package, REPOSITORY
from tools.build import write_archive


def test_catalog_resolves_complete_generated_package():
    catalog = json.loads((REPOSITORY / '.agents/plugins/marketplace.json').read_text())
    assert len(catalog['plugins']) == 1
    entry = catalog['plugins'][0]
    assert entry['source'] == {'source': 'local', 'path': './plugins/reefy-dev'}
    assert 'pluginId' not in entry  # Ownership must be verified before adopting a workspace plugin.
    destination = REPOSITORY / entry['source']['path']
    committed = {p.relative_to(destination).as_posix(): p.read_bytes()
                 for p in destination.rglob('*') if p.is_file()}
    rendered = render_workspace_package()
    assert committed == rendered, 'Regenerate with python tools/sync_workspace.py'
    manifest = json.loads(rendered['plugin.json'])
    assert entry['name'] == manifest['name']
    settings = manifest['extensions']['com.openai']
    assert settings['onboardingSkill'][2:] in committed
    assert settings['apps'][2:] in committed
    assert 'mcp.json' not in committed and '.mcp.json' not in committed
    assert 'mcpServers' not in settings


def test_registered_mapping_and_package_identity_preserved():
    files = render_workspace_package()
    manifest = json.loads(files['plugin.json'])
    mapping = json.loads(files['.app.json'])
    assert files['.app.json'] == (REPOSITORY / 'providers/chatgpt/registered/.app.json').read_bytes()
    assert list(mapping['apps']) == [manifest['name']]
    assert next(iter(mapping['apps'].values()))['id'].startswith('asdk_app_')
    overlay = json.loads(files['.codex-plugin/plugin.json'])
    assert overlay['name'] == manifest['name']
    assert overlay['version'] == manifest['version']
    assert overlay['interface'] == manifest['extensions']['com.openai']['interface']
    assert 'mcpServers' not in overlay


def test_workspace_bundle_has_environment_bound_shared_resources():
    files = render_workspace_package()
    assert files['skills/reefy-setup/SKILL.md'] == (REPOSITORY / 'shared/skills/reefy-setup/SKILL.md').read_bytes()
    guide = files['skills/reefy-setup/references/new-device.md']
    source = (REPOSITORY / 'shared/docs/device-onboarding.md').read_bytes()
    assert guide == source.replace(b'{{REEFY_ORIGIN}}', b'https://reefy.dev')
    assert b'https://reefy.ai/dashboard' not in guide


def test_changed_mapping_fails_closed(monkeypatch, tmp_path):
    source = tmp_path / 'providers/chatgpt/registered'
    source.mkdir(parents=True)
    (source / 'plugin.json').write_text(json.dumps({'name': 'synthetic-plugin'}))
    (source / '.app.json').write_text(json.dumps({'apps': {'foreign-plugin': {'id': 'synthetic-app'}}}))
    monkeypatch.setattr('package.REPOSITORY', tmp_path)
    with pytest.raises(ValueError, match='identity'):
        render_workspace_package()


def test_workspace_archive_is_reproducible(tmp_path):
    first, second = tmp_path / 'first.zip', tmp_path / 'second.zip'
    files = render_workspace_package()
    write_archive(first, files)
    write_archive(second, files)
    assert first.read_bytes() == second.read_bytes()
