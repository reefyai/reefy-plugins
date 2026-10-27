"""Offline listing preflight; portal review and live-host acceptance remain separate."""
import json
import struct
from pathlib import PurePosixPath
from urllib.parse import urlsplit


def listing_issues(files):
    """Return actionable blockers without modifying a package or contacting services."""
    manifest = json.loads(files['plugin.json'])
    interface = manifest.get('extensions', {}).get('com.openai', {}).get('interface', {})
    issues = []
    for field, limit in (
        ('displayName', 30), ('shortDescription', 30),
        ('longDescription', 4000), ('developerName', 80), ('category', 80),
    ):
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip() or len(value) > limit:
            issues.append(f'{field}: required text, at most {limit} characters')
    for field in ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL'):
        value = interface.get(field)
        try:
            url = urlsplit(value) if isinstance(value, str) else None
            valid = url and url.scheme == 'https' and url.hostname and not url.username and not url.password
        except ValueError:
            valid = False
        if not valid or len(value) > 1024:
            issues.append(f'{field}: required HTTPS URL without credentials')
    prompts = interface.get('defaultPrompt', [])
    if isinstance(prompts, str):
        prompts = [prompts]
    if (not isinstance(prompts, list) or len(prompts) > 3 or
            any(not isinstance(p, str) or not p.strip() or len(p) > 128 for p in prompts)):
        issues.append('defaultPrompt: at most three nonempty prompts, each at most 128 characters')
    # Reefy distributes its existing PNG, rather than introducing image conversion.
    for field in ('logo', 'composerIcon'):
        value = interface.get(field)
        safe = (isinstance(value, str) and value.startswith('./') and
                '\\' not in value and '..' not in PurePosixPath(value).parts)
        data = files.get(value[2:]) if safe else None
        valid = data and len(data) <= 5 * 1024 * 1024 and data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) >= 24
        if valid:
            width, height = struct.unpack('>II', data[16:24])
            valid = 48 <= width == height <= 4096
        if not valid:
            issues.append(f'{field}: bundle a square PNG, 48-4096 pixels and at most 5 MiB')
    if '.app.json' in files or any(name.startswith('hooks/') for name in files):
        issues.append('Public submission cannot include app references or lifecycle hooks')
    return issues


def review_issues(files):
    """Flag missing review materials; never embed reviewer credentials."""
    settings = json.loads(files['plugin.json']).get('extensions', {}).get('com.openai', {})
    review = settings.get('review', {})
    cases = review.get('test_cases', {})
    issues = []
    for kind, count in (('positive', 5), ('negative', 3)):
        values = cases.get(kind, [])
        if not isinstance(values, list) or len(values) != count:
            issues.append(f'review.test_cases.{kind}: exactly {count} cases required')
            continue
        required = ('description', 'prompt', 'tools_triggered', 'expected_behavior') if kind == 'positive' else ('description', 'prompt')
        if any(not isinstance(case, dict) or any(not isinstance(case.get(k), str) or not case[k].strip() for k in required) for case in values):
            issues.append(f'review.test_cases.{kind}: complete all required case fields')
    value = review.get('demo_recording_url', '')
    try:
        url = urlsplit(value) if isinstance(value, str) else None
        valid = url and url.scheme == 'https' and url.hostname and not url.username and not url.password
    except ValueError:
        valid = False
    if not valid:
        issues.append('review.demo_recording_url: accessible HTTPS demonstration recording required')
    notes = settings.get('publication', {}).get('release_notes')
    if not isinstance(notes, str) or not notes.strip():
        issues.append('publication.release_notes: reviewed release notes required')
    if 'test_credentials' in review or 'reviewer_instructions' in review:
        issues.append('Reviewer credentials/instructions belong in the secure portal, not the ZIP')
    return issues
