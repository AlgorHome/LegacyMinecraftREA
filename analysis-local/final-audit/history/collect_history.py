"""Offline allowlist-only historical evidence extraction; never execute target code.

Input is restricted to the launcher log directory and the supplied game log
directory. Raw lines, account data, URLs with queries, command lines, and local
paths are never emitted or retained. A matching event means only that a message
was recorded, not that its assertion is true or that it was observed in this run.
"""
from pathlib import Path
import collections
import gzip
import hashlib
import json
import re
from urllib.parse import urlsplit

ROOT = Path(r"C:\Users\arinze\AppData\Roaming\.tlauncher")
OUT = Path(__file__).parent
SOURCES = [*sorted((ROOT / 'logs').glob('launcher.log*')),
           *sorted((ROOT / 'legacy/Minecraft/game/logs').glob('*.log*'))]

EVENTS = {
    'bootstrap_version_message': r'\bbootstrap\b.*?\b(?:version|v)\b|\bbootstrap\s+\d+\.\d+',
    'launcher_version_message': r'(?:Legacy\s*Launcher|TLauncher).*?(?:\bversion\b|\bv\d)|(?:Legacy\s*Launcher|TLauncher)\s+\d+\.\d+',
    'java_version_message': r'\b(?:Java|JVM|JRE)\b.*?\b(?:version|runtime)\b|\bjava version\b',
    'update_message': r'\b(?:updat(?:e|ed|ing|er)|updates)\b',
    'download_message': r'\b(?:download(?:ed|ing|er|s)?|fetch(?:ing|ed)?)\b',
    'hash_verification_message': r'\b(?:checksum|sha-?1|sha-?256|hash(?:es|ing)?|verif(?:y|ied|ication))\b',
    'repair_message': r'\b(?:repair|recover(?:ed|y|ing)?|corrupt(?:ed|ion)?|missing)\b',
    'process_launch_message': r'\b(?:launching|started|starting|launch)\b',
    'process_exit_message': r'\b(?:exited|exit code|exitcode|process.*?finished|process.*?terminated)\b',
    'error_message': r'\b(?:ERROR|Exception|failed|failure)\b',
    'graphics_message': r'\b(?:LWJGL|OpenGL|GLFW|Backend library)\b',
    'audio_message': r'\b(?:OpenAL|Sound engine|audio)\b',
    'game_version_message': r'\b(?:Minecraft|game version|version id)\b',
    'shutdown_message': r'\b(?:Stopping!|Shutting down|shutdown|stopped|Stopping)\b',
}
EVENTS = {k: re.compile(v, re.I) for k, v in EVENTS.items()}
TIMESTAMP = re.compile(r'(?:\d{4}-\d{2}-\d{2}[ T])?\d{2}:\d{2}:\d{2}(?:[.,]\d{1,9})?')
VER = r'(?P<version>\d{1,4}(?:[._]\d{1,4}){1,4}(?:\+[0-9]+|\+legacy)?(?:[-_](?:ea|beta|rc)[0-9]*)?)'
VERSION_PATTERNS = {
    'Legacy Launcher': re.compile(r'(?:Legacy\s*Launcher|TLauncher|Launcher)(?:[\s:=v_-]|version){1,20}' + VER, re.I),
    'bootstrap': re.compile(r'bootstrap(?:\s+|[\s:=v_-]|version){1,20}' + VER, re.I),
    'Java': re.compile(r'(?:Java version|Java:|JVM version|JRE version|openjdk version)(?:[\s:=v_\"-]|version){1,20}' + VER, re.I),
    'Minecraft': re.compile(r'(?:Minecraft(?: version)?|game version|version id)(?:[\s:=v_\"-]|version){1,20}' + VER, re.I),
    'LWJGL': re.compile(r'(?:LWJGL(?: version)?|Backend library)(?:[\s:=v_\"-]|version){1,20}' + VER, re.I),
    'OpenAL': re.compile(r'(?:OpenAL(?: Soft)? version)[\s:=\"]{1,10}' + VER, re.I),
    'OpenGL': re.compile(r'(?:OpenGL version)[\s:=\"]{1,10}' + VER, re.I),
    'GLFW': re.compile(r'(?:GLFW version)[\s:=\"]{1,10}' + VER, re.I),
}
KNOWN_PUBLIC_VERSIONS = {
    'archived_launcher': '1.159.2', 'installed_launcher': '1.169.4',
    'archived_bootstrap': '1.32.2', 'installed_bootstrap': '1.40.3',
    'selected_minecraft': '1.21.11', 'game_java': '21.0.7',
}
ALLOWED_HOSTS = {
    'piston-meta.mojang.com', 'piston-data.mojang.com', 'launchermeta.mojang.com',
    'launcher.mojang.com', 'resources.download.minecraft.net', 'libraries.minecraft.net',
    'meta.fabricmc.net', 'maven.fabricmc.net', 'maven.minecraftforge.net',
    'files.minecraftforge.net', 'launchermeta.mojang.com', 'llaun.ch', 'tlauncher.org',
    'repo.llaun.ch', 'repo.legacylauncher.ru', 'repo.tlauncher.org',
}
URL = re.compile(r'https?://[^\s\"<>\]\)]+', re.I)
PUBLIC_PATH = re.compile(
    r'^/(?:mc/game/version_manifest(?:_v2)?\.json|'
    r'v1/(?:packages|objects)/[0-9a-f]{40}/[A-Za-z0-9_.+-]+|'
    r'[0-9a-f]{2}/[0-9a-f]{40}|'
    r'(?:net/minecraft|org/lwjgl|net/java|com/mojang|net/fabricmc|org/ow2|net/minecraftforge)/[A-Za-z0-9_./+:-]+|'
    r'(?:[A-Za-z0-9_.-]+/){0,4}(?:bootstrap|launcher)(?:[-_.A-Za-z0-9]+)?\.json(?:\.mgz(?:\.signed)?)?)$', re.I)
ARTIFACT = re.compile(r'(?<![A-Za-z0-9_-])(?:bootstrap|launcher|client|server|Minecraft|OpenAL|glfw|lwjgl(?:_[a-z0-9]+)?|jemalloc)(?:[-_.]\d+(?:\.\d+){1,4}(?:\+legacy)?)?\.(?:jar|dll|exe|json|zip|mgz)(?![A-Za-z0-9_])', re.I)
HASH = re.compile(r'\b(?:sha[-_ ]?1|sha[-_ ]?256|checksum)\s*[:=]?\s*([0-9A-Fa-f]{64}|[0-9A-Fa-f]{40})(?![0-9A-Fa-f])', re.I)
SENSITIVE = re.compile(r'access.?token|refresh.?token|bearer\s|authorization\s*:|--username|--uuid|--xuid|--clientid|password|clipboard', re.I)
STATUS_PATTERNS = {
    'process_exit_code': re.compile(r'(?:exit(?:ed)?(?: with)?(?: code)?|exitcode|process.*?(?:finished|terminated).*?(?:code|status))\s*[:=]?\s*(-?\d{1,10})\b', re.I),
    'http_status': re.compile(r'(?:HTTP(?:/\d(?:\.\d)?)?|response(?:\s+code)?|status(?:\s+code)?)\s*[:=]?\s*([1-5]\d{2})\b', re.I),
}
# Fixed public technical messages yield boolean events only, never free text.
TECH_EVENTS = {
    'openal_initialized_recorded': re.compile(r'OpenAL.*?initiali[sz]ed|initiali[sz]ed.*?OpenAL', re.I),
    'sound_engine_started_recorded': re.compile(r'Sound engine started', re.I),
    'game_stopping_recorded': re.compile(r'\bStopping!', re.I),
    'update_available_recorded': re.compile(r'update.*?available|new.*?version.*?available', re.I),
    'no_update_recorded': re.compile(r'(?:no updates|up.to.date|nothing to update|update not required)', re.I),
    'download_complete_recorded': re.compile(r'download.*?(?:completed|finished|successful)|(?:completed|finished).*?download', re.I),
    'hash_mismatch_recorded': re.compile(r'(?:hash|checksum|sha-?1|sha-?256).*?(?:mismatch|incorrect|invalid|failed)|(?:mismatch|incorrect|invalid).*?(?:hash|checksum|sha-?1|sha-?256)', re.I),
}

result = {
    'schema': 'legacyforge-phase6a-history-v1',
    'evidence_type': 'historical_recorded_message_only',
    'raw_line_retention': False,
    'target_execution': False,
    'scope': ['logs/launcher.log*', 'legacy/Minecraft/game/logs/*.log*'],
    'limitations': [
        'Messages are historical assertions and were not reproduced or independently authenticated.',
        'Log rotation, clock changes, edits, absent logs, and omitted privacy-sensitive lines limit completeness.',
        'No archive installer execution, sandbox, Xbox, account, network traffic, or entitlement test was performed.',
        'Only predefined technical fields and fixed event labels are retained. Absence of retained events does not prove absence of behavior.',
    ],
    'sources': [], 'records': [],
}

for path in SOURCES:
    if not path.is_file():
        continue
    raw = path.read_bytes()
    expanded = gzip.decompress(raw) if path.name.endswith('.gz') else raw
    lines = expanded.decode('utf-8-sig', errors='replace').splitlines()
    relative = path.relative_to(ROOT).as_posix()
    source = {'path': relative, 'sha256': hashlib.sha256(raw).hexdigest(),
              'bytes': len(raw), 'line_count': len(lines), 'matched_record_count': 0,
              'sensitive_line_count_omitted': 0}
    if path.name.endswith('.gz'):
        source['decompressed_sha256'] = hashlib.sha256(expanded).hexdigest()
    for number, line in enumerate(lines, 1):
        if SENSITIVE.search(line):
            source['sensitive_line_count_omitted'] += 1
            continue
        tags = [tag for tag, regex in EVENTS.items() if regex.search(line)]
        tech_events = [tag for tag, regex in TECH_EVENTS.items() if regex.search(line)]
        versions = []
        for technology, pattern in VERSION_PATTERNS.items():
            for match in pattern.finditer(line):
                versions.append({'technology': technology, 'version': match['version']})
        statuses = []
        for kind, pattern in STATUS_PATTERNS.items():
            for match in pattern.finditer(line):
                statuses.append({'kind': kind, 'value': int(match[1])})
        endpoints = []
        for match in URL.finditer(line):
            try:
                parsed = urlsplit(match[0])
                host = parsed.hostname
                if host not in ALLOWED_HOSTS or parsed.username or parsed.password:
                    continue
                if PUBLIC_PATH.fullmatch(parsed.path):
                    endpoints.append(f'{parsed.scheme}://{host}{parsed.path}')
            except ValueError:
                pass
        artifacts = sorted({m[0] for m in ARTIFACT.finditer(line)})
        # Retain hashes only on technical transfer/integrity lines.
        hashes = sorted(set(HASH.findall(line))) if 'hash_verification_message' in tags else []
        fixed_mentions = [{'identity': key, 'version': value} for key, value in KNOWN_PUBLIC_VERSIONS.items()
                          if re.search(r'(?<![\d.])' + re.escape(value) + r'(?![\d.])', line)]
        if not (tags or tech_events or versions or statuses or endpoints or artifacts or fixed_mentions):
            continue
        stamp = TIMESTAMP.search(line[:80])
        record = {'source': relative, 'line': number}
        if stamp:
            record['timestamp_as_recorded'] = stamp[0]
        if tags:
            record['event_tags'] = tags
        if tech_events:
            record['technical_events'] = tech_events
        if versions:
            record['versions'] = versions
        if statuses:
            record['status_codes'] = statuses
        if endpoints:
            record['public_endpoints'] = sorted(set(endpoints))
        if artifacts:
            record['artifact_basenames'] = artifacts
        if hashes:
            record['hashes'] = hashes
        if fixed_mentions:
            record['known_public_version_mentions'] = fixed_mentions
        result['records'].append(record)
        source['matched_record_count'] += 1
    result['sources'].append(source)

OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'historical-evidence-sanitized.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
summary = {'sources': result['sources'], 'record_count': len(result['records']),
           'event_counts': dict(collections.Counter(t for r in result['records'] for t in r.get('event_tags', []))),
           'technical_event_counts': dict(collections.Counter(t for r in result['records'] for t in r.get('technical_events', []))),
           'versions': sorted({(v['technology'], v['version']) for r in result['records'] for v in r.get('versions', [])}),
           'status_codes': sorted({(v['kind'], v['value']) for r in result['records'] for v in r.get('status_codes', [])}),
           'public_endpoints': sorted({v for r in result['records'] for v in r.get('public_endpoints', [])})}
(OUT / 'historical-evidence-summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps({k: v for k, v in summary.items() if k != 'public_endpoints'} |
                 {'public_endpoint_count': len(summary['public_endpoints'])}, indent=2))
