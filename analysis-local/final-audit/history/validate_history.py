"""Independent structural/privacy verification of the local sanitized evidence."""
from pathlib import Path
import collections
import hashlib
import json
import re
from urllib.parse import urlsplit

ROOT = Path(r'C:\Users\arinze\AppData\Roaming\.tlauncher')
OUT = Path(__file__).parent
data = json.loads((OUT / 'historical-evidence-sanitized.json').read_text(encoding='utf-8'))
allowed_sources = {'logs/launcher.log', 'logs/launcher.log.1', 'logs/launcher.log.2', 'logs/launcher.log.3',
    'legacy/Minecraft/game/logs/2026-10-17-1.log.gz', 'legacy/Minecraft/game/logs/latest.log'}
allowed_record_keys = {'source', 'line', 'timestamp_as_recorded', 'event_tags', 'technical_events', 'versions',
    'status_codes', 'public_endpoints', 'artifact_basenames', 'hashes', 'known_public_version_mentions'}
allowed_tags = {'bootstrap_version_message', 'launcher_version_message', 'java_version_message', 'update_message',
    'download_message', 'hash_verification_message', 'repair_message', 'process_launch_message', 'process_exit_message',
    'error_message', 'graphics_message', 'audio_message', 'game_version_message', 'shutdown_message'}
allowed_tech_events = {'openal_initialized_recorded', 'sound_engine_started_recorded', 'game_stopping_recorded',
    'update_available_recorded', 'no_update_recorded', 'download_complete_recorded', 'hash_mismatch_recorded'}
allowed_versions = {'archived_launcher': '1.159.2', 'installed_launcher': '1.169.4',
    'archived_bootstrap': '1.32.2', 'installed_bootstrap': '1.40.3',
    'selected_minecraft': '1.21.11', 'game_java': '21.0.7'}
allowed_hosts = {'piston-meta.mojang.com', 'piston-data.mojang.com', 'launchermeta.mojang.com',
    'launcher.mojang.com', 'resources.download.minecraft.net', 'libraries.minecraft.net',
    'meta.fabricmc.net', 'maven.fabricmc.net', 'maven.minecraftforge.net', 'files.minecraftforge.net',
    'llaun.ch', 'tlauncher.org', 'repo.llaun.ch', 'repo.legacylauncher.ru', 'repo.tlauncher.org'}
source_stats = {s['path']: s for s in data['sources']}
assert set(source_stats) == allowed_sources
assert data['raw_line_retention'] is False and data['target_execution'] is False
assert all(hashlib.sha256((ROOT / s['path']).read_bytes()).hexdigest() == s['sha256'] for s in data['sources'])
counted = collections.Counter()
for r in data['records']:
    assert set(r) <= allowed_record_keys
    assert r['source'] in allowed_sources
    assert isinstance(r['line'], int) and 1 <= r['line'] <= source_stats[r['source']]['line_count']
    counted[r['source']] += 1
    if 'timestamp_as_recorded' in r:
        assert re.fullmatch(r'(?:\d{4}-\d{2}-\d{2}[ T])?\d{2}:\d{2}:\d{2}(?:[.,]\d{1,9})?', r['timestamp_as_recorded'])
    assert set(r.get('event_tags', [])) <= allowed_tags
    assert set(r.get('technical_events', [])) <= allowed_tech_events
    for v in r.get('versions', []):
        assert set(v) == {'technology', 'version'}
        assert v['technology'] in {'Legacy Launcher', 'bootstrap', 'Java', 'Minecraft', 'LWJGL', 'OpenAL', 'OpenGL', 'GLFW'}
        assert re.fullmatch(r'\d{1,4}(?:[._]\d{1,4}){1,4}(?:\+[0-9]+|\+legacy)?(?:[-_](?:ea|beta|rc)[0-9]*)?', v['version'])
    for v in r.get('known_public_version_mentions', []):
        assert set(v) == {'identity', 'version'} and allowed_versions[v['identity']] == v['version']
    for v in r.get('status_codes', []):
        assert set(v) == {'kind', 'value'} and isinstance(v['value'], int)
        assert v['kind'] in {'http_status', 'process_exit_code'}
        if v['kind'] == 'http_status':
            assert 100 <= v['value'] <= 599
    for h in r.get('hashes', []):
        assert re.fullmatch(r'(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})', h)
    for name in r.get('artifact_basenames', []):
        assert '/' not in name and '\\' not in name and ':' not in name
        assert re.fullmatch(r'[A-Za-z0-9_.+-]+\.(?:jar|dll|exe|json|zip|mgz)', name)
    for url in r.get('public_endpoints', []):
        u = urlsplit(url)
        assert u.scheme in {'http', 'https'} and u.hostname in allowed_hosts
        assert u.username is None and u.password is None and not u.query and not u.fragment
        assert re.fullmatch(r'/[A-Za-z0-9_./+:-]*', u.path)
assert all(counted[s['path']] == s['matched_record_count'] for s in data['sources'])

report = {'scope': 'sanitized historical evidence only', 'record_count': len(data['records']),
    'source_count': len(source_stats), 'source_line_count': sum(s['line_count'] for s in data['sources']),
    'schema_allowlist_valid': True, 'source_hashes_stable_at_validation': True,
    'no_raw_line_fields': True, 'no_endpoint_query_or_credentials': True,
    'target_execution': False, 'dynamic_test_verdict': 'NOT_PERFORMED',
    'evidence_output_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'validation.json'}}
(OUT / 'validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps({k: v for k, v in report.items() if k != 'evidence_output_sha256'}, indent=2))
