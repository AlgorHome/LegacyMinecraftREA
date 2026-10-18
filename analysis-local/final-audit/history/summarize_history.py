"""Summarize already sanitized records; no access to original log text."""
from pathlib import Path
import collections
import hashlib
import json
from urllib.parse import urlsplit

OUT = Path(__file__).parent
data = json.loads((OUT / 'historical-evidence-sanitized.json').read_text(encoding='utf-8'))

def kind(url):
    p = urlsplit(url)
    if 'version_manifest' in p.path:
        return 'minecraft_version_catalog'
    if p.hostname == 'resources.download.minecraft.net':
        return 'minecraft_asset_content'
    if p.hostname == 'libraries.minecraft.net':
        return 'minecraft_library_content'
    if p.hostname in {'piston-data.mojang.com', 'launcher.mojang.com'}:
        if p.path.endswith('/client.jar'):
            return 'minecraft_client_jar'
        if '/objects/' in p.path:
            return 'mojang_runtime_or_other_content'
    if p.hostname in {'piston-meta.mojang.com', 'launchermeta.mojang.com'}:
        return 'minecraft_or_runtime_metadata'
    return 'other_allowlisted_public_metadata'

groups = collections.defaultdict(list)
for ordinal, r in enumerate(data['records'], 1):
    r['sanitized_record_ordinal'] = ordinal
    for url in r.get('public_endpoints', []):
        groups[kind(url)].append((r, url))

summary = []
for category, members in groups.items():
    # Preserve source-file order; this is not a cross-log wall clock sort.
    per_source = collections.defaultdict(list)
    for record, url in members:
        per_source[record['source']].append((record, url))
    summary.append({'category': category, 'unique_endpoint_count': len({u for _, u in members}),
        'endpoint_occurrence_count': len(members), 'sources': [
            {'source': source, 'first': {'line': rs[0][0]['line'], 'record': rs[0][0]['sanitized_record_ordinal'],
                'timestamp_as_recorded': rs[0][0].get('timestamp_as_recorded'), 'public_endpoint': rs[0][1]},
             'last': {'line': rs[-1][0]['line'], 'record': rs[-1][0]['sanitized_record_ordinal'],
                'timestamp_as_recorded': rs[-1][0].get('timestamp_as_recorded'), 'public_endpoint': rs[-1][1]}}
            for source, rs in per_source.items()]})

selected = []
for r in data['records']:
    if (r.get('technical_events') or r.get('status_codes')
        or any(v['identity'] in {'archived_launcher', 'installed_launcher', 'archived_bootstrap', 'installed_bootstrap'}
               for v in r.get('known_public_version_mentions', []))
        or any(v['technology'] == 'Java' or v['version'] == '3.3.3+5' for v in r.get('versions', []))):
        selected.append(r)
out = {'evidence_type': data['evidence_type'], 'endpoint_categories': summary,
       'selected_events': selected, 'source_sha256': data['sources']}
(OUT / 'historical-findings-index.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps({'endpoint_categories': summary, 'selected_event_count': len(selected)}, indent=2))
