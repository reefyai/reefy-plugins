"""Calendar releases remain strict SemVer across registered and portable packages."""
import json
import re
import zipfile
from package import render_package, render_workspace_package, build_update


def test_date_release_is_canonical_in_all_package_forms():
    versions=[]
    for files in (render_package('reefy.dev'),render_package('reefy.ai'),render_workspace_package()):
        version=json.loads(files['plugin.json'])['version']
        assert re.fullmatch(r'[1-9][0-9]{3}\.[1-9][0-9]{2,3}\.(0|[1-9][0-9]*)',version)
        assert version=='2026.1029.2'
        versions.append(version)
    assert len(set(versions))==1


def test_downloaded_legacy_version_uses_canonical_release(tmp_path):
    original=tmp_path/'legacy.zip';out=tmp_path/'updated.zip'
    with zipfile.ZipFile(original,'w') as z:
        z.writestr('plugin.json',json.dumps({'name':'synthetic','version':'1.0.19'}))
        z.writestr('.app.json',json.dumps({'apps':{'synthetic':{'id':'synthetic-app'}}}))
    result=build_update(original,out,'reefy.dev','synthetic-app')
    assert result['version']==json.loads(render_workspace_package()['plugin.json'])['version']
    with zipfile.ZipFile(out) as z:
        assert json.loads(z.read('plugin.json'))['version']==result['version']


def test_update_rejects_same_or_older_source_release(tmp_path):
    import pytest
    for installed in ('2026.1029.2','2026.1029.3','2027.105.0'):
        original=tmp_path/'installed.zip';out=tmp_path/'result.zip'
        with zipfile.ZipFile(original,'w') as z:
            z.writestr('plugin.json',json.dumps({'name':'synthetic','version':installed}))
            z.writestr('.app.json',json.dumps({'apps':{'synthetic':{'id':'synthetic-app'}}}))
        with pytest.raises(ValueError,match='newer'):
            build_update(original,out,'reefy.dev','synthetic-app')
        assert not out.exists()
