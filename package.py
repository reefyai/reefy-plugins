"""Render the approved portable scaffold without environment-specific workflows."""
import json
from pathlib import Path

REPOSITORY = Path(__file__).parent
ROOT = REPOSITORY / 'providers/chatgpt/plugin'


def render_package(domain):
    if domain not in ('reefy.dev', 'reefy.ai'):
        raise ValueError('Expected a configured Reefy deployment domain')
    files = {}
    for source in ROOT.rglob('*'):
        if not source.is_file():
            continue
        relative = source.relative_to(ROOT).as_posix()
        if relative.endswith('.json'):
            value = json.loads(source.read_text())
            if relative == 'mcp.json':
                server = value['mcpServers']['reefy']
                server['url'] = 'https://' + domain + '/mcp'
                auth = server['extensions']['com.openai']['auth']
                auth['authorizationUrl'] = 'https://' + domain + '/oauth/mcp/authorize'
                auth['tokenUrl'] = 'https://' + domain + '/oauth/mcp/token'
            elif relative == 'plugin.json':
                value['extensions']['com.openai']['interface']['displayName'] = (
                    'Reefy Dev' if domain == 'reefy.dev' else 'Reefy')
            files[relative] = (json.dumps(value, indent=2) + '\n').encode()
        else:
            files[relative] = source.read_bytes()
    for source in (REPOSITORY / 'shared/skills').rglob('*'):
        if source.is_file() and '__pycache__' not in source.parts and source.suffix not in ('.pyc', '.pyo'):
            relative = source.relative_to(REPOSITORY / 'shared').as_posix()
            files[relative] = source.read_bytes()
    guide = REPOSITORY / 'shared/docs/device-onboarding.md'
    files['skills/reefy-setup/references/new-device.md'] = guide.read_bytes().replace(
        b'{{REEFY_ORIGIN}}', ('https://' + domain).encode())
    return files


def build_update(base_zip, output_zip, domain, expected_app_id):
    """Preserve the downloaded private plugin identity and registered mapping."""
    import copy
    import re
    import zipfile
    from pathlib import PurePosixPath
    with zipfile.ZipFile(base_zip) as archive:
        names = archive.namelist()
        if (len(names) != len(set(names)) or
                sum(i.file_size for i in archive.infolist()) > 100_000_000 or
                any(PurePosixPath(n).is_absolute() or '..' in PurePosixPath(n).parts or '\\' in n for n in names)):
            raise ValueError('Unsafe plugin archive')
        files = {n: archive.read(n) for n in names if not n.endswith('/')}
    mapping = json.loads(files['.app.json'])
    aliases = [key for key, value in mapping['apps'].items() if value.get('id') == expected_app_id]
    if len(aliases) != 1 or len(mapping['apps']) != 1:
        raise ValueError('Expected the existing single Reefy app mapping')
    alias = aliases[0]
    root = json.loads(files['plugin.json']) if 'plugin.json' in files else None
    overlay = json.loads(files['.codex-plugin/plugin.json']) if '.codex-plugin/plugin.json' in files else None
    identity = root or overlay
    if not identity or identity.get('name') != alias:
        raise ValueError('Plugin identity does not match its registered server')
    version = re.fullmatch(r'(\d+)\.(\d+)\.(\d+)', identity.get('version', ''))
    if not version:
        raise ValueError('Unsupported existing version format')
    rendered = render_package(domain)
    manifest = json.loads(rendered['plugin.json'])
    # Use the reviewed source release, not an independent bump of the downloaded ZIP.
    updated_version = manifest['version']
    if tuple(map(int, updated_version.split('.'))) <= tuple(map(int, version.groups())):
        raise ValueError('Package release must be newer than the installed version')
    manifest.update({key: copy.deepcopy(identity[key]) for key in ('name', 'author') if key in identity})
    manifest['version'] = updated_version
    settings = copy.deepcopy((root or {}).get('extensions', {}).get('com.openai') or
        {k: v for k, v in (overlay or {}).items() if k not in ('name', 'version', 'author', 'description')})
    settings.setdefault('interface', {}).update(copy.deepcopy(manifest['extensions']['com.openai']['interface']))
    settings['apps'] = './.app.json'
    settings['onboardingSkill'] = './skills/reefy-setup/SKILL.md'
    manifest['extensions']['com.openai'] = settings
    rendered['plugin.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    # Registered app packages already resolve OAuth through .app.json.
    # A second direct MCP server shadows that connection in fresh chats.
    rendered.pop('mcp.json')
    for mcp_path in ('mcp.json', '.mcp.json'):
        if mcp_path not in files:
            continue
        existing_mcp = json.loads(files[mcp_path])
        existing_mcp.get('mcpServers', {}).pop(alias, None)
        if existing_mcp.get('mcpServers'):
            files[mcp_path] = (json.dumps(existing_mcp, indent=2) + '\n').encode()
        else:
            files.pop(mcp_path)
    if settings.get('mcpServers') == './.mcp.json' and '.mcp.json' not in files:
        settings.pop('mcpServers')
        rendered['plugin.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    if overlay:
        if overlay.get('mcpServers') == './.mcp.json' and '.mcp.json' not in files:
            overlay.pop('mcpServers')
        overlay['interface'] = copy.deepcopy(settings['interface'])
        overlay['description'] = manifest['description']
        overlay['version'] = updated_version
        overlay['skills'] = './skills/'
        overlay['onboardingSkill'] = settings['onboardingSkill']
        files['.codex-plugin/plugin.json'] = (json.dumps(overlay, indent=2) + '\n').encode()
    # Keep assets and the exact registered app mapping. Replace only package
    # configuration and our approved setup skill, not unrelated workflows.
    files.update({k: v for k, v in rendered.items() if k != 'README.md'})
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            archive.writestr(name, data)
    return {'name': identity['name'], 'version': updated_version}


def render_workspace_package():
    """Render the registered dev connection without a duplicate direct server."""
    source = REPOSITORY / 'providers/chatgpt/registered'
    manifest = json.loads((source / 'plugin.json').read_text())
    mapping_bytes = (source / '.app.json').read_bytes()
    mapping = json.loads(mapping_bytes)
    if list(mapping['apps']) != [manifest['name']]:
        raise ValueError('Registered identity does not match app mapping')
    settings = manifest['extensions']['com.openai']
    if settings.get('apps') != './.app.json' or 'mcpServers' in settings:
        raise ValueError('Workspace package requires the registered connection only')
    files = {name: data for name, data in render_package('reefy.dev').items()
             if name.startswith(('skills/', 'assets/'))}
    files['plugin.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    files['.app.json'] = mapping_bytes
    overlay = {key: manifest[key] for key in ('name', 'version', 'author', 'description')}
    overlay.update({'apps': settings['apps'], 'interface': settings['interface'],
                    'skills': './skills/', 'onboardingSkill': settings['onboardingSkill'],
                    'extensions': {'com.openai': {'onboardingSkill': settings['onboardingSkill']}}})
    files['.codex-plugin/plugin.json'] = (json.dumps(overlay, indent=2) + '\n').encode()
    return files
