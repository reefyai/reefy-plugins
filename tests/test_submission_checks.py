"""Synthetic listing preflight catches package blockers before portal upload."""
import json
import pytest
from package import render_package
from tools.submission_checks import listing_issues


@pytest.fixture
def candidate():
    files = render_package('reefy.ai')
    manifest = json.loads(files['plugin.json'])
    manifest['extensions']['com.openai']['interface'] = {
        'displayName': 'Synthetic app', 'shortDescription': 'Manage synthetic devices',
        'longDescription': 'Manage devices in a synthetic account.',
        'developerName': 'Synthetic publisher', 'category': 'Developer Tools',
        'websiteURL': 'https://synthetic.example',
        'supportURL': 'https://synthetic.example/support',
        'privacyPolicyURL': 'https://synthetic.example/privacy',
        'termsOfServiceURL': 'https://synthetic.example/terms',
        'logo': './assets/reefy.png', 'composerIcon': './assets/reefy.png',
        'defaultPrompt': ['Show my devices'],
    }
    files['plugin.json'] = json.dumps(manifest).encode()
    return files


def test_complete_listing_and_bundled_icon_pass(candidate):
    assert listing_issues(candidate) == []


@pytest.mark.parametrize('field,value', [
    ('shortDescription', 'x' * 31), ('longDescription', ''),
    ('termsOfServiceURL', None), ('supportURL', 'http://synthetic.example'),
    ('privacyPolicyURL', 'https://secret@synthetic.example'),
    ('logo', '../outside.png'), ('composerIcon', './assets/missing.png'),
    ('defaultPrompt', ['a', 'b', 'c', 'd']),
])
def test_invalid_listing_is_reported_without_changing_package(candidate, field, value):
    manifest = json.loads(candidate['plugin.json'])
    manifest['extensions']['com.openai']['interface'][field] = value
    candidate['plugin.json'] = json.dumps(manifest).encode()
    before = dict(candidate)
    assert any(field in issue for issue in listing_issues(candidate))
    assert candidate == before


@pytest.mark.parametrize('path', ['.app.json', 'hooks/start.json'])
def test_registered_connections_and_lifecycle_hooks_are_not_submission_packages(candidate, path):
    candidate[path] = b'{}'
    assert any('Public submission' in issue for issue in listing_issues(candidate))


def test_approved_production_listing_and_terms_have_no_offline_listing_blockers():
    files = render_package('reefy.ai')
    interface = json.loads(files['plugin.json'])['extensions']['com.openai']['interface']
    assert interface['displayName'] == 'Reefy'
    assert interface['shortDescription'] == 'Manage your AI computers'
    assert 'Use text or ChatGPT Voice' in interface['longDescription']
    assert 'GPU-powered computers' in interface['longDescription']
    assert interface['termsOfServiceURL'] == 'https://reefy.ai/terms'
    assert listing_issues(files) == []


def test_review_materials_are_not_silently_claimed_complete(candidate):
    from tools.submission_checks import review_issues
    issues = review_issues(candidate)
    assert len(issues) == 4
    manifest = json.loads(candidate['plugin.json'])
    settings = manifest['extensions']['com.openai']
    positive = {'description':'Synthetic case','prompt':'Show a synthetic record','tools_triggered':'read_synthetic','expected_behavior':'Show only owned synthetic data'}
    negative = {'description':'Synthetic denial','prompt':'Read another account'}
    settings['review'] = {'test_cases': {'positive':[positive] * 5, 'negative':[negative] * 3}, 'demo_recording_url':'https://synthetic.example/demo'}
    settings['publication'] = {'release_notes':'Synthetic release notes'}
    candidate['plugin.json'] = json.dumps(manifest).encode()
    assert review_issues(candidate) == []
    settings['review']['test_credentials'] = 'synthetic-only'
    candidate['plugin.json'] = json.dumps(manifest).encode()
    assert any('secure portal' in i for i in review_issues(candidate))


def test_build_retains_submission_blockers_for_the_exact_archives(monkeypatch, tmp_path):
    import zipfile
    from tools import build
    monkeypatch.setattr(build, 'ROOT', tmp_path)
    monkeypatch.setattr(build.subprocess, 'check_output', lambda args, **kwargs: 'a' * 40 if args[1] == 'rev-parse' else '')
    build.build()
    report = json.loads((tmp_path / 'dist/submission-preflight.json').read_text())
    assert report['source_sha'] == 'a' * 40
    assert {p['file'] for p in report['packages']} == {'reefy.zip', 'reefy-dev.zip'}
    for package in report['packages']:
        with zipfile.ZipFile(tmp_path / 'dist' / package['file']) as archive:
            files = {name: archive.read(name) for name in archive.namelist()}
        assert package['listing_issues'] == listing_issues(files)
        from tools.submission_checks import review_issues
        assert package['review_issues'] == review_issues(files)
