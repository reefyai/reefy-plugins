"""Deployment parity and safe package connection configuration."""
import json
import pytest
from package import render_package


def test_environment_render_preserves_workflow_and_connection_identity():
    dev,prod = render_package('reefy.dev'),render_package('reefy.ai')
    assert dev.keys()==prod.keys()
    skill='skills/reefy-setup/SKILL.md'
    assert dev[skill]==prod[skill]
    manifests=[json.loads(p['plugin.json']) for p in (dev,prod)]
    assert manifests[0]['name']==manifests[1]['name']
    for package,domain in ((dev,'reefy.dev'),(prod,'reefy.ai')):
        manifest=json.loads(package['plugin.json'])
        assert manifest['extensions']['com.openai']['onboardingSkill'][2:] in package
        mcp=json.loads(package['mcp.json'])['mcpServers']['reefy']
        auth=mcp['extensions']['com.openai']['auth']
        assert mcp['url']=='https://'+domain+'/mcp'
        assert auth['authorizationUrl']=='https://'+domain+'/oauth/mcp/authorize'
        assert auth['tokenUrl']=='https://'+domain+'/oauth/mcp/token'
        assert auth['client']['tokenEndpointAuthMethod']=='none'
        assert 'clientSecret' not in auth
        assert set(auth['baseScopes'])=={'reefy:devices:read','reefy:devices:adopt','reefy:apps:install','reefy:events:read'}


@pytest.mark.parametrize('domain',['reefy.dev.attacker.example','http://reefy.dev','localhost',''])
def test_unconfigured_authorities_rejected(domain):
    with pytest.raises(ValueError):
        render_package(domain)


def test_update_preserves_registered_identity_assets_and_mapping(tmp_path):
    import zipfile
    from package import build_update
    base,out=tmp_path/'original.zip',tmp_path/'updated.zip'
    original={'name':'synthetic-reefy','version':'1.0.0','apps':'./.app.json',
              'author':{'name':'Synthetic developer'},'interface':{'displayName':'Synthetic Reefy'}}
    mapping={'apps':{'synthetic-reefy':{'id':'synthetic-app'}}}
    with zipfile.ZipFile(base,'w') as z:
        z.writestr('.codex-plugin/plugin.json',json.dumps(original))
        z.writestr('.app.json',json.dumps(mapping))
        z.writestr('assets/icon.svg','<svg/>')
        z.writestr('skills/existing/SKILL.md','Existing workflow')
    assert build_update(base,out,'reefy.dev','synthetic-app')=={'name':'synthetic-reefy','version':'2026.1029.1'}
    with zipfile.ZipFile(out) as z:
        assert json.loads(z.read('.app.json'))==mapping
        assert z.read('assets/icon.svg')==b'<svg/>'
        assert z.read('skills/existing/SKILL.md')==b'Existing workflow'
        root=json.loads(z.read('plugin.json'))
        assert root['name']==original['name'] and root['author']==original['author']
        assert root['extensions']['com.openai']['apps']=='./.app.json'
        assert 'mcp.json' not in z.namelist()
    with pytest.raises(ValueError,match='mapping'):
        build_update(base,out,'reefy.dev','foreign-app')


def test_update_rejects_traversal_before_writing(tmp_path):
    import zipfile
    from package import build_update
    base,out=tmp_path/'unsafe.zip',tmp_path/'result.zip'
    with zipfile.ZipFile(base,'w') as z:
        z.writestr('../escape','unsafe')
    with pytest.raises(ValueError,match='Unsafe'):
        build_update(base,out,'reefy.dev','synthetic-app')
    assert not out.exists()


@pytest.mark.parametrize('domain', ['reefy.dev', 'reefy.ai'])
@pytest.mark.parametrize('keep_other_server', [False, True])
@pytest.mark.parametrize('mcp_path', ['mcp.json', '.mcp.json'])
def test_registered_update_removes_direct_duplicate_from_existing_package(tmp_path, domain, keep_other_server, mcp_path):
    import zipfile
    from package import build_update
    base, out = tmp_path / 'original.zip', tmp_path / 'updated.zip'
    mapping = {'apps': {'synthetic-reefy': {'id': 'synthetic-app'}}}
    manifest = {'name': 'synthetic-reefy', 'version': '1.0.3',
                'extensions': {'com.openai': {'apps': './.app.json'}}}
    servers = {'synthetic-reefy': {'type': 'streamable-http', 'url': 'https://' + domain + '/mcp'}}
    other = {'type': 'streamable-http', 'url': 'https://synthetic.example/mcp'}
    if keep_other_server:
        servers['unrelated'] = other
    with zipfile.ZipFile(base, 'w') as z:
        z.writestr('plugin.json', json.dumps(manifest))
        z.writestr('.app.json', json.dumps(mapping))
        z.writestr(mcp_path, json.dumps({'mcpServers': servers}))
        z.writestr('.codex-plugin/plugin.json', json.dumps({'name':'synthetic-reefy','version':'1.0.3','apps':'./.app.json','mcpServers':'./.mcp.json'}))
    build_update(base, out, domain, 'synthetic-app')
    with zipfile.ZipFile(out) as z:
        assert json.loads(z.read('.app.json')) == mapping
        assert z.read('skills/reefy-setup/SKILL.md') == render_package(domain)['skills/reefy-setup/SKILL.md']
        if keep_other_server:
            assert json.loads(z.read(mcp_path))['mcpServers'] == {'unrelated': other}
        else:
            assert 'mcp.json' not in z.namelist()
            assert '.mcp.json' not in z.namelist()
            assert 'mcpServers' not in json.loads(z.read('.codex-plugin/plugin.json'))


@pytest.mark.parametrize('domain,other',[('reefy.dev','reefy.ai'),('reefy.ai','reefy.dev')])
def test_onboarding_reference_is_bundled_for_the_connected_environment(domain,other):
    package = render_package(domain)
    guide = package['skills/reefy-setup/references/new-device.md'].decode()
    assert '{{REEFY_ORIGIN}}' not in guide
    assert f'https://{domain}/dashboard' in guide
    assert f'https://{domain}/api/images/generate' in guide
    assert f'https://{other}/dashboard' not in guide
    assert f'https://{other}/api/images/generate' not in guide
    from pathlib import Path
    source = Path('shared/docs/device-onboarding.md').read_text()
    assert guide == source.replace('{{REEFY_ORIGIN}}','https://'+domain)


@pytest.mark.parametrize('domain', ['reefy.dev', 'reefy.ai'])
def test_bundled_storage_guide_does_not_require_new_firmware(domain):
    package = render_package(domain)
    guide = package['skills/reefy-setup/references/new-device.md'].decode()
    assert 'fresh storage inventory' not in guide
    assert 'Unsupported firmware, uncertain inventory' not in guide
    assert 'no new firmware capability or reflash is required' in guide


def test_voice_progress_has_bounded_checks_and_spoken_milestones():
    for domain in ('reefy.dev','reefy.ai'):
        skill=render_package(domain)['skills/reefy-setup/SKILL.md'].decode()
        for text in ('During an active Voice session','say that adoption is complete',
                     'announce the already-requested app installation','Speak when that app is verified running',
                     'at least 15 seconds','up to 90 seconds','no more than seven reads',
                     'speak one short factual result before the next wait',
                     'never read its URL aloud','do not promise an audible callback',
                     'A completed adoption operation is never evidence',
                     'perform the already-requested install_app once'):
            assert text in skill
        assert 'During background/text event waiting' in skill
        assert 'Never duplicate adoption or app installation' in skill


def test_friendly_names_preserve_user_choice_identity_and_retry_safety():
    for domain in ('reefy.dev', 'reefy.ai'):
        skill = render_package(domain)['skills/reefy-setup/SKILL.md'].decode()
        for requirement in (
            "honor the user's explicit name", 'Coral, Plankton, Anemone, Nautilus, Pearl or Lagoon',
            'connected account', 'Compare names case-insensitively', 'Coral 2',
            'Do not use device UUID fragments', 'never rename adopted devices automatically',
            'Save the chosen name with the request ID and reuse both on retries',
            'Do not add a naming question that blocks setup',
            "Let me know if you'd prefer another name", 'Never repeat adoption',
            'never claim a rename succeeded before its tool result',
        ):
            assert requirement in skill


@pytest.mark.parametrize('domain', ['reefy.dev', 'reefy.ai'])
def test_background_completion_has_visible_link_and_distinct_operation_card(domain):
    skill = render_package(domain)['skills/reefy-setup/SKILL.md'].decode()
    assert 'background event-task reply' in skill
    assert 'show the authoritative returned `app_url` as one **Open app** Markdown link' in skill
    assert 'Do not render a launcher card in that background reply' in skill
    assert 'Never dictate or spell a URL' in skill
    assert 'new app-start status card' in skill
    assert 'never reuse the adoption card' in skill


@pytest.mark.parametrize('domain', ['reefy.dev', 'reefy.ai'])
def test_storage_choice_survives_package_updates(domain):
    skill = render_package(domain)['skills/reefy-setup/SKILL.md'].decode()
    guide = render_package(domain)['skills/reefy-setup/references/new-device.md'].decode()
    for content in (skill, guide):
        assert 'preserve_internal_storage:true' in content
        assert 'Storage choice required' in content
    assert 'Before any new-device adoption' in skill
    assert 'Do not adopt before the user answers' in skill


@pytest.mark.parametrize('domain', ['reefy.dev', 'reefy.ai'])
def test_firmware_workflow_keeps_reboot_and_erasure_separate(domain):
    skill = render_package(domain)['skills/reefy-setup/SKILL.md'].decode()
    for required in ('get_device_firmware', 'adoption_update_required',
                     'temporarily interrupt running apps', 'confirm_reboot:true',
                     'get_firmware_update', 'device.firmware_changed',
                     'Firmware update IDs are not adoption operation IDs',
                     'Existing erase-confirmation safeguards apply', 'Never say that using an SSD itself requires newer firmware',
                     'Card Stop status checks does not cancel firmware work'):
        assert required in skill


@pytest.mark.parametrize('domain', ['reefy.dev', 'reefy.ai'])
def test_firmware_reboot_restarts_normal_discovery_with_saved_context(domain):
    skill=render_package(domain)['skills/reefy-setup/SKILL.md'].decode()
    for required in ('device.registered', 'Before dispatching', 'without filtering to the old UUID',
                     'rerun normal device discovery', 'new request ID',
                     'chosen name, internal-storage preference, prior explicit erase approval and requested app',
                     'do not add a disk-matching workflow', 'Do not try to keep the old UUID sticky',
                     'unsubscribe the exact temporary firmware and registration subscriptions'):
        assert required in skill


@pytest.mark.parametrize('domain', ['reefy.dev', 'reefy.ai'])
def test_private_host_network_guide_preserves_authenticated_ui_and_build_isolation(domain):
    guide=render_package(domain)['skills/reefy-develop/references/project-format.md'].decode()
    for required in ('network_mode: "host"', 'dynamic_port: true', 'APP_PORT_8080',
                     '127.0.0.1', 'isolated build health check', 'Bridge networking remains the default'):
        assert required in guide


@pytest.mark.parametrize('domain', ['reefy.dev', 'reefy.ai'])
def test_hardware_suggestions_are_optional_product_references_not_checkout(domain):
    guide = render_package(domain)['skills/reefy-setup/references/new-device.md'].decode()
    for text in (
        'A suitable existing device skips shopping',
        'Do not recommend purchasing another computer unnecessarily',
        'optional Reefy-tested examples', 'any retailer',
        'not a required purchase or a Reefy checkout',
        'does not sell these items or process their payments',
        'do not purchase anything without', 'not live quotes',
        'Do not imply OpenAI endorsement',
    ):
        assert text in guide
    assert 'a.co/' not in guide
    for product in ('B00RORBNWG', 'B0H4TCY6TH', 'B0GGB2MPVH'):
        assert f'https://www.amazon.com/dp/{product})' in guide
    manifest = json.loads(render_package(domain)['plugin.json'])
    interface = manifest['extensions']['com.openai']['interface']
    for key in ('shortDescription', 'longDescription', 'defaultPrompt'):
        assert '$' not in str(interface[key]) and 'amazon.com' not in str(interface[key])


def test_registered_update_applies_approved_listing_without_replacing_connection(tmp_path):
    import zipfile
    from package import build_update
    base, out = tmp_path / 'original.zip', tmp_path / 'updated.zip'
    mapping = {'apps': {'synthetic-reefy': {'id': 'synthetic-app'}}}
    original = {'name': 'synthetic-reefy', 'version': '1.0.0', 'author': {'name': 'Synthetic developer'}, 'extensions': {'com.openai': {'apps': './.app.json', 'interface': {'displayName': 'Old name', 'shortDescription': 'Old subtitle'}}}}
    with zipfile.ZipFile(base, 'w') as z:
        z.writestr('plugin.json', json.dumps(original))
        z.writestr('.app.json', json.dumps(mapping))
    build_update(base, out, 'reefy.dev', 'synthetic-app')
    expected = json.loads(render_package('reefy.dev')['plugin.json'])['extensions']['com.openai']['interface']
    with zipfile.ZipFile(out) as z:
        updated = json.loads(z.read('plugin.json'))
        assert updated['extensions']['com.openai']['interface'] == expected
        assert updated['name'] == original['name'] and updated['author'] == original['author']
        assert json.loads(z.read('.app.json')) == mapping
        assert z.read(expected['logo'][2:]) == render_package('reefy.dev')[expected['logo'][2:]]
        assert 'mcp.json' not in z.namelist()
