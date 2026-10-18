"""Fetch exactly one statically derived public metadata URL and verify offline.

No target code is imported/executed. No redirects, cookies, auth, query strings,
binary artifact downloads, installations, devices, or private addresses are used.
Fetched metadata bytes and extracted public-key bytes remain local only.
"""
from pathlib import Path
import datetime
import hashlib
import hmac
import io
import gzip
import ipaddress
import json
import socket
import urllib.error
import urllib.request
import zipfile

OUT = Path(__file__).parent
OUT.mkdir(parents=True, exist_ok=True)
INSTALLED = Path(r'C:\Users\arinze\AppData\Roaming\.tlauncher\legacy\Minecraft\launcher\bootstrap.jar')
ORIGINAL = Path(r'C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\installer-extracted-local\bootstrap.jar')
HOST = 'bootstrap.llaun.ch'
URL = 'https://bootstrap.llaun.ch/legacy/bootstrap.json.mgz.signed'
MAX_BYTES = 1024 * 1024

def sha(data):
    return hashlib.sha256(data).hexdigest()

with zipfile.ZipFile(INSTALLED) as outer:
    meta = json.loads(outer.read('META-INF/bootstrap-meta.json'))
    assert meta['shortBrand'] == 'legacy'
    nested_name = 'BOOT-INF/lib/bootstrap-1.40.3-plain.jar'
    nested_bytes = outer.read(nested_name)
    with zipfile.ZipFile(io.BytesIO(nested_bytes)) as nested:
        key_member = 'net/legacylauncher/bootstrap/transport/public.der'
        key = nested.read(key_member)
    common_name = 'BOOT-INF/lib/common-1.169.3-177-gbe31b827.jar'
    common_bytes = outer.read(common_name)
    with zipfile.ZipFile(io.BytesIO(common_bytes)) as common:
        host_class = common.read('net/legacylauncher/repository/HostsV1.class')
        assert b'bootstrap.llaun.ch' in host_class
with zipfile.ZipFile(ORIGINAL) as original:
    original_key = original.read('public.der')
assert key == original_key
assert sha(key) == '4fd4703ee5c9f4339bfc5e7ea7aa36eb0ffa6e6f6915df0ec5563ac0835a294c'
(OUT / 'public.der').write_bytes(key)

def tlv(raw, offset=0):
    tag = raw[offset]
    offset += 1
    size = raw[offset]
    offset += 1
    if size & 0x80:
        count = size & 0x7f
        assert 1 <= count <= 4
        size = int.from_bytes(raw[offset:offset + count], 'big')
        offset += count
    end = offset + size
    assert end <= len(raw)
    return tag, raw[offset:end], end

# Strict bounded X.509 SubjectPublicKeyInfo -> RSAPublicKey parser.
tag, spki, end = tlv(key)
assert tag == 0x30 and end == len(key)
tag, algorithm, pos = tlv(spki)
assert tag == 0x30 and algorithm == bytes.fromhex('06092a864886f70d0101010500')
tag, bit_string, pos = tlv(spki, pos)
assert tag == 3 and pos == len(spki) and bit_string[0] == 0
tag, rsa_seq, end = tlv(bit_string[1:])
assert tag == 0x30 and end == len(bit_string) - 1
tag, modulus, pos = tlv(rsa_seq)
assert tag == 2
tag, exponent, pos = tlv(rsa_seq, pos)
assert tag == 2 and pos == len(rsa_seq)
n, e = int.from_bytes(modulus, 'big'), int.from_bytes(exponent, 'big')
assert n.bit_length() == 2048 and e == 65537

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

record = {
    'evidence_kind': 'independent_public_signed_metadata_fixture_check',
    'requested_url': URL,
    'request_started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'target_execution': False, 'authentication_used': False,
    'redirects_allowed': False, 'maximum_response_bytes': MAX_BYTES,
    'installed_bootstrap_sha256': sha(INSTALLED.read_bytes()),
    'archived_bootstrap_sha256': sha(ORIGINAL.read_bytes()),
    'installed_nested_bootstrap_sha256': sha(nested_bytes),
    'installed_common_jar_sha256': sha(common_bytes),
    'hosts_class_sha256': sha(host_class),
    'public_key_sha256': sha(key), 'public_key_bytes': len(key),
    'archived_and_installed_key_identical': True,
    'key_algorithm': 'RSA-2048; public exponent 65537; DER SubjectPublicKeyInfo',
    'signature_algorithm': 'RSASSA-PKCS1-v1_5 with SHA-1 over UTF-8 lowercase hexadecimal SHA-256 of bytes after the 256-byte signature prefix',
    'verifier': 'Python standard library ASN.1 parsing, modular exponentiation, constant-time encoded-message comparison; no target code',
    'verification_result': 'NOT_REACHED',
}
try:
    addresses = {item[4][0] for item in socket.getaddrinfo(HOST, 443, type=socket.SOCK_STREAM)}
    assert addresses and all(ipaddress.ip_address(address).is_global for address in addresses)
    record['dns_addresses_all_public'] = True
    request = urllib.request.Request(URL, headers={'User-Agent': 'LegacyForge-Phase6A-Research/1.0', 'Accept': 'application/octet-stream'})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect)
    with opener.open(request, timeout=15) as response:
        record['http_status'] = response.status
        body = response.read(MAX_BYTES + 1)
        assert response.status == 200 and len(body) <= MAX_BYTES
    (OUT / 'bootstrap.json.mgz.signed').write_bytes(body)
    record['response_bytes'] = len(body)
    record['response_sha256'] = sha(body)
    assert len(body) > 256
    signature, payload = body[:256], body[256:]
    signature_integer = int.from_bytes(signature, 'big')
    assert 0 < signature_integer < n
    encoded = pow(signature_integer, e, n).to_bytes(256, 'big')
    signed_message = hashlib.sha256(payload).hexdigest().encode('utf-8')
    digest_info = bytes.fromhex('3021300906052b0e03021a05000414') + hashlib.sha1(signed_message).digest()
    expected = b'\x00\x01' + b'\xff' * (256 - len(digest_info) - 3) + b'\x00' + digest_info
    valid = hmac.compare_digest(encoded, expected)
    record['verification_result'] = 'VALID' if valid else 'INVALID'
    record['payload_bytes'] = len(payload)
    record['payload_sha256'] = sha(payload)
    record['signature_bytes'] = 256
    record['payload_marker_hex'] = payload[:5].hex()
    # Negative controls alter local copies only. No malformed input is sent anywhere.
    changed_payload = bytes([payload[0] ^ 1]) + payload[1:]
    changed_msg = hashlib.sha256(changed_payload).hexdigest().encode('utf-8')
    changed_di = bytes.fromhex('3021300906052b0e03021a05000414') + hashlib.sha1(changed_msg).digest()
    changed_expected = b'\x00\x01' + b'\xff' * (256 - len(changed_di) - 3) + b'\x00' + changed_di
    record['local_payload_bitflip_rejected'] = not hmac.compare_digest(encoded, changed_expected)
    changed_signature = bytes([signature[0] ^ 1]) + signature[1:]
    changed_integer = int.from_bytes(changed_signature, 'big')
    changed_encoded = pow(changed_integer, e, n).to_bytes(256, 'big') if 0 < changed_integer < n else b''
    record['local_signature_bitflip_rejected'] = not hmac.compare_digest(changed_encoded, expected)
    if valid:
        assert payload[:5] == b'gzip:'
        with gzip.GzipFile(fileobj=io.BytesIO(payload[5:])) as compressed:
            expanded = compressed.read(4 * 1024 * 1024 + 1)
        assert len(expanded) <= 4 * 1024 * 1024 and isinstance(json.loads(expanded), dict)
        (OUT / 'bootstrap-metadata-decoded-local.json').write_bytes(expanded)
        record.update({'compression_marker': 'gzip:', 'bounded_gzip_json_parse_valid': True,
                       'maximum_decompressed_bytes': 4 * 1024 * 1024,
                       'decompressed_json_bytes': len(expanded),
                       'decompressed_json_sha256': sha(expanded)})
except urllib.error.HTTPError as error:
    record['http_status'] = error.code
    record['failure_kind'] = 'HTTPError'
except Exception as error:
    record['failure_kind'] = type(error).__name__
record['request_finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
record['limitations'] = [
    'Signature correspondence establishes a response matching the extracted key, not historical installer authenticity or real-world publisher identity.',
    'No launcher updater execution, update application, rollback, sandbox, Xbox, account, or entitlement test was performed.',
    'Metadata bytes and extracted public key remain local only; no referenced binaries are fetched.',
]
(OUT / 'fixture-check-local.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
print(json.dumps(record, indent=2))
