"""Direct Git helper rejects credential/target mistakes before network activity."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time
import pytest
from package import render_package, render_workspace_package

SOURCE = Path('shared/skills/reefy-develop/scripts/push_project.py')
spec = importlib.util.spec_from_file_location('project_push', SOURCE)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
PROJECT = 'a' * 32
URL = 'https://synthetic--s1--synthetic.reefy.dev/git/' + PROJECT + '.git'
TOKEN = 'synthetic.' + 'x' * 100 + '.signature'


def connection(tmp_path, **changes):
    value = dict(project_id=PROJECT, git_url=URL, username='git', access_token=TOKEN,
                 expires_at=int(time.time()) + 600)
    value.update(changes)
    path = tmp_path / 'connection.json'
    path.write_text(json.dumps(value))
    path.chmod(0o600)
    return path


@pytest.mark.parametrize('change', [
    {'project_id': 'b' * 32}, {'expires_at': 0}, {'expires_at': float('inf')},
    {'expires_at': time.time()+2000}, {'access_token': 'bad\nheader'}, {'username': 'root'},
])
def test_invalid_connection_never_reaches_git(tmp_path, change):
    with pytest.raises(ValueError):
        helper.load_connection(connection(tmp_path, **change), URL)


@pytest.mark.parametrize('endpoint', [URL.replace('https:', 'http:'),
    URL.replace('.reefy.dev', '.reefy.dev.attacker.example'), URL+'?token=x',
    URL.replace('/git/', ':444/git/'), URL.replace('https://', 'https://user@')])
def test_target_cannot_redirect_credentials(tmp_path, endpoint):
    with pytest.raises(ValueError):
        helper.load_connection(connection(tmp_path, git_url=endpoint), endpoint)


def test_connection_file_must_be_private_regular_file(tmp_path):
    path = connection(tmp_path)
    path.chmod(0o644)
    with pytest.raises(ValueError):
        helper.load_connection(path, URL)
    path.chmod(0o600)
    link = tmp_path/'link'
    link.symlink_to(path)
    with pytest.raises(OSError):
        helper.load_connection(link, URL)


def test_jwt_and_real_project_shape_supported_in_both_environments(tmp_path):
    for endpoint in (URL, URL.replace('.dev/', '.ai/')):
        assert helper.load_connection(connection(tmp_path, git_url=endpoint), endpoint)['access_token'] == TOKEN


def test_push_auth_is_ephemeral_and_failure_cannot_expose_token(tmp_path, monkeypatch):
    repo = tmp_path/'project'
    (repo/'.git').mkdir(parents=True)
    monkeypatch.setattr(helper.subprocess, 'check_output', lambda *a, **k: 'b'*40+'\n')
    calls = []
    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        return subprocess.CompletedProcess(argv, 0, b'', b'')
    monkeypatch.setattr(helper.subprocess, 'run', run)
    result = helper.push(connection(tmp_path), URL, repo)
    assert result['pushed'] is True and result['commit'] == 'b'*40
    argv, kwargs = calls[0]
    assert TOKEN not in repr(argv)
    env = kwargs['env']
    settings = {env['GIT_CONFIG_KEY_'+str(i)]: env['GIT_CONFIG_VALUE_'+str(i)]
                for i in range(int(env['GIT_CONFIG_COUNT']))}
    assert settings['http.followRedirects'] == 'false'
    assert settings['http.sslVerify'] == 'true'
    assert settings['credential.helper'] == ''
    assert not list((repo/'.git').iterdir())
    monkeypatch.setattr(helper.subprocess, 'run', lambda argv, **kw: subprocess.CompletedProcess(argv,1,b'',TOKEN.encode()))
    with pytest.raises(ValueError, match='direct_git_push_failed') as error:
        helper.push(connection(tmp_path), URL, repo)
    assert TOKEN not in str(error.value)


def test_registered_and_portable_packages_include_identical_development_helper():
    key = 'skills/reefy-develop/scripts/push_project.py'
    for package in (render_package('reefy.dev'), render_package('reefy.ai'), render_workspace_package()):
        assert package[key] == SOURCE.read_bytes()
        skill = package['skills/reefy-develop/SKILL.md'].decode()
        for name in ('prepare_private_app_project','get_private_app_project_connection',
                     'publish_private_app_project','get_private_app_project_operation',
                     'install_private_app','update_private_app'):
            assert name in skill
        assert 'never dictate its URL' in skill
        assert 'Do not ask users to install another plugin' in skill
