"""Repository automation for reproducible portable scaffold artifacts."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from package import render_package, render_workspace_package
from tools.submission_checks import listing_issues, review_issues


def write_archive(path, files):
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def build():
    destination = ROOT / 'dist'
    destination.mkdir(exist_ok=True)
    source = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip())
    artifacts = []
    preflight = []
    for domain, name in [('reefy.dev', 'reefy-dev'), ('reefy.ai', 'reefy')]:
        files = render_package(domain)
        path = destination / (name + '.zip')
        write_archive(path, files)
        preflight.append({'file': path.name, 'listing_issues': listing_issues(files),
                          'review_issues': review_issues(files)})
        artifacts.append({'file': path.name, 'domain': domain,
                          'package_version': json.loads(files['plugin.json'])['version'],
                          'artifact_kind': 'portable-scaffold',
                          'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    files = render_workspace_package()
    path = destination / 'reefy-dev-workspace.zip'
    write_archive(path, files)
    artifacts.append({'file': path.name, 'domain': 'reefy.dev',
                      'package_version': json.loads(files['plugin.json'])['version'],
                      'artifact_kind': 'registered-workspace-package',
                      'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    receipt = {'source_sha': source, 'source_dirty': dirty,
               'artifact_kind': 'package-build', 'artifacts': artifacts}
    (destination / 'submission-preflight.json').write_text(json.dumps({'source_sha': source, 'packages': preflight, 'note': 'Offline checks only; live acceptance, reviewer access and portal approval are separate.'}, indent=2) + '\n')
    (destination / 'provenance.json').write_text(json.dumps(receipt, indent=2) + '\n')
    (destination / 'SHA256SUMS').write_text(''.join(a['sha256'] + '  ' + a['file'] + '\n' for a in artifacts))
    return receipt


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))
