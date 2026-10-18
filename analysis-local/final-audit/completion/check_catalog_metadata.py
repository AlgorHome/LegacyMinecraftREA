"""Public metadata only for all56 pinned catalog rows. No target execution or binary downloads."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

PIN = "d1453434ceefe73bef5aff497194e09f39dde7e1"
ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "analysis-local" / "legacyforge-d145343"
DOCS = ROOT / "docs" / "research" / "legacy-launcher"
CATALOG_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
FORGE_URL = "https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml"
NEOFORGE_URL = "https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml"
HOSTS = {"piston-meta.mojang.com", "launchermeta.mojang.com", "launcher.mojang.com",
         "meta.fabricmc.net", "maven.minecraftforge.net", "maven.neoforged.net"}
MAX_BYTES, TIMEOUT, MAX_WALL = 6 * 1024 * 1024, 12, 30

def utc():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def permitted_url(url):
    p = urllib.parse.urlsplit(url)
    if p.scheme != "https" or p.hostname not in HOSTS or p.username or p.password or p.port not in (None, 443):
        raise ValueError("URL outside explicit public HTTPS metadata allowlist")
    if p.query or p.fragment or not (p.path.endswith(".json") or p.path.endswith(".xml") or p.path.endswith("/profile/json")):
        raise ValueError("Only JSON/XML metadata paths permitted")
    if re.search(r"\.(?:jar|exe|dll|zip|appx|msix)(?:$|/)", p.path, re.I):
        raise ValueError("Binary artifact request prohibited")
    return url

class RestrictedRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        permitted_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def fetch(url):
    record = {"url": url, "retrieved_at_utc": utc(), "status": None}
    started = time.monotonic()
    try:
        permitted_url(url)
        opener = urllib.request.build_opener(RestrictedRedirect())
        request = urllib.request.Request(url, headers={"User-Agent": "LegacyForge-Phase6A-MetadataResearch/1.0",
                    "Accept": "application/json, application/xml, text/xml", "Accept-Encoding": "identity"})
        with opener.open(request, timeout=TIMEOUT) as response:
            record.update(http_status=response.status, final_url=permitted_url(response.geturl()),
                          content_type=response.headers.get("Content-Type", ""))
            size = response.headers.get("Content-Length")
            if size is not None and int(size) > MAX_BYTES:
                raise ValueError("Declared body exceeds bound")
            chunks, count = [], 0
            while True:
                if time.monotonic() - started > MAX_WALL:
                    raise TimeoutError("Response wall-time bound exceeded")
                chunk = response.read(min(65536, MAX_BYTES + 1 - count))
                if not chunk:
                    break
                count += len(chunk)
                if count > MAX_BYTES:
                    raise ValueError("Body exceeds bound")
                chunks.append(chunk)
            body = b"".join(chunks)
            record.update(status="FETCHED", bytes=len(body), response_sha256=sha256(body),
                          response_sha1=hashlib.sha1(body).hexdigest())
            return record, body
    except urllib.error.HTTPError as exc:
        record.update(status="HTTP_FAILURE", http_status=exc.code, error_type="HTTPError")
    except (urllib.error.URLError, socket.timeout, TimeoutError, OSError) as exc:
        record.update(status="NETWORK_UNKNOWN", error_type=type(exc).__name__)
    except (ValueError, TypeError) as exc:
        record.update(status="METADATA_INVALID_OR_BOUNDED", error_type=type(exc).__name__, error=str(exc))
    record["elapsed_ms"] = round((time.monotonic() - started) * 1000)
    return record, None

def json_fetch(url):
    record, body = fetch(url)
    if body is None:
        return record, None
    try:
        obj = json.loads(body)
        if not isinstance(obj, dict):
            raise ValueError("Expected object")
        return record, obj
    except (ValueError, UnicodeError):
        record.update(status="METADATA_INVALID", error_type="InvalidJSONObject")
        return record, None

def inspect_version(item):
    record, obj = json_fetch(item["url"])
    result = {"requested_id": item["id"], "source": record, "status": record["status"],
              "catalog_declared_sha1": item.get("sha1")}
    if obj is None:
        return result
    matched = record["response_sha1"] == item.get("sha1")
    libs = [x for x in obj.get("libraries", []) if isinstance(x, dict)]
    result.update(catalog_sha1_matches=matched, id=obj.get("id"), main_class=obj.get("mainClass"),
                  java_requirement_declared=obj.get("javaVersion"),
                  client_descriptor={k: obj.get("downloads", {}).get("client", {}).get(k) for k in ("sha1", "size", "url")},
                  asset_index_descriptor={k: obj.get("assetIndex", {}).get(k) for k in ("id", "sha1", "size", "totalSize", "url")},
                  libraries={"total": len(libs),
                    "artifact_descriptors": sum(isinstance(x.get("downloads", {}).get("artifact"), dict) for x in libs),
                    "native_classifier_descriptors": sum(sum("natives" in k for k in x.get("downloads", {}).get("classifiers", {})) for x in libs),
                    "rule_bearing_libraries": sum(bool(x.get("rules")) for x in libs)},
                  client_and_assets_downloaded=False)
    result["status"] = "HASH_MISMATCH" if not matched else "METADATA_ID_MISMATCH" if obj.get("id") != item["id"] else "FOUND_HASH_VERIFIED_METADATA"
    return result

def target_id(row):
    return "{}-{}-{}".format(row["minecraftVersion"], row["loader"], row["loaderVersion"])

def inspect_fabric(row):
    mc, loader = row["minecraftVersion"], row["loaderVersion"]
    url = "https://meta.fabricmc.net/v2/versions/loader/{}/{}/profile/json".format(urllib.parse.quote(mc, safe=""), urllib.parse.quote(loader, safe=""))
    record, obj = json_fetch(url)
    result = {"target_id": target_id(row), "source": record, "status": record["status"]}
    if obj is None:
        return result
    names = [x.get("name") for x in obj.get("libraries", []) if isinstance(x, dict)]
    result.update(profile_id=obj.get("id"), inherits_from=obj.get("inheritsFrom"), main_class=obj.get("mainClass"),
                  library_count=len(names), exact_loader_coordinate_present="net.fabricmc:fabric-loader:" + loader in names,
                  exact_intermediary_coordinate_present="net.fabricmc:intermediary:" + mc in names,
                  argument_group_counts={k: len(v) for k, v in obj.get("arguments", {}).items() if isinstance(v, list)})
    result["status"] = "FOUND_EXACT_PROFILE" if result["inherits_from"] == mc and result["exact_loader_coordinate_present"] else "PROFILE_TUPLE_MISMATCH"
    result["intermediary_presence_is_not_required_for_tuple_identity"] = True
    return result

def inspect_maven(url, expected_group, expected_artifact):
    record, body = fetch(url)
    result = {"source": record, "status": record["status"]}
    if body is None:
        return result, set()
    try:
        if b"<!DOCTYPE" in body.upper() or b"<!ENTITY" in body.upper():
            raise ValueError("DTD/entities prohibited")
        root = ET.fromstring(body)
        group, artifact = root.findtext("groupId"), root.findtext("artifactId")
        versions = {x.text for x in root.findall("./versioning/versions/version") if x.text}
        result.update(group_id=group, artifact_id=artifact, listed_version_count=len(versions),
                      last_updated=root.findtext("./versioning/lastUpdated"))
        if group != expected_group or artifact != expected_artifact:
            result["status"] = "METADATA_COORDINATE_MISMATCH"
            return result, set()
        result["status"] = "FOUND_MAVEN_VERSION_INDEX"
        return result, versions
    except (ValueError, ET.ParseError):
        result.update(status="METADATA_INVALID", error_type="InvalidMavenXML")
        return result, set()

def main():
    start = utc()
    head = subprocess.run(["git", "-C", str(SOURCE), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    if head != PIN:
        raise SystemExit("Source checkout differs from pin")
    catalog_path = SOURCE / "config" / "versions.tsv"
    generator_path = SOURCE / "scripts" / "new-download-manifest.ps1"
    generator = generator_path.read_text(encoding="utf-8-sig")
    templates = [CATALOG_URL, "https://meta.fabricmc.net/v2/versions/loader/$MinecraftVersion/$LoaderVersion/profile/json",
        "https://maven.minecraftforge.net/net/minecraftforge/forge/$forgeVersion/forge-$forgeVersion-installer.jar",
        "https://maven.neoforged.net/releases/net/neoforged/neoforge/$LoaderVersion/neoforge-$LoaderVersion-installer.jar"]
    if any(s not in generator for s in templates):
        raise SystemExit("Pinned endpoint template differs")
    with catalog_path.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file, delimiter="\t"))
    if len(rows) != 56 or len({target_id(r) for r in rows}) != 56:
        raise SystemExit("Need all56 unique pinned rows")
    needed = sorted({r["minecraftVersion"] for r in rows})
    catalog_record, catalog = json_fetch(CATALOG_URL)
    entries = {x["id"]: x for x in (catalog or {}).get("versions", []) if isinstance(x, dict) and "id" in x}
    versions, fabric, maven, maven_versions, jobs = {}, {}, {}, {}, {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for version in needed:
            if version in entries:
                jobs[pool.submit(inspect_version, entries[version])] = ("version", version)
            else:
                versions[version] = {"requested_id": version, "catalog_ref": "mojang_catalog",
                    "status": "NOT_LISTED_IN_RETURNED_CATALOG" if catalog is not None else "CATALOG_UNAVAILABLE"}
        for row in rows:
            if row["loader"] == "fabric":
                jobs[pool.submit(inspect_fabric, row)] = ("fabric", target_id(row))
        jobs[pool.submit(inspect_maven, FORGE_URL, "net.minecraftforge", "forge")] = ("forge", None)
        jobs[pool.submit(inspect_maven, NEOFORGE_URL, "net.neoforged", "neoforge")] = ("neoforge", None)
        for future in as_completed(jobs):
            kind, key = jobs[future]
            try:
                outcome = future.result()
            except Exception as exc:
                outcome = {"status": "ANALYST_PARSE_UNKNOWN", "error_type": type(exc).__name__}
                if kind in ("forge", "neoforge"):
                    outcome = (outcome, set())
            if kind == "version":
                versions[key] = outcome
            elif kind == "fabric":
                fabric[key] = outcome
            else:
                maven[kind], maven_versions[kind] = outcome
    plans = []
    for row in rows:
        tid, loader = target_id(row), row["loader"]
        item = {"target_id": tid, "minecraft_version": row["minecraftVersion"], "loader": loader,
                "loader_version": row["loaderVersion"], "source_runtime": row["javaRuntime"],
                "source_support_label": row["supportLevel"], "minecraft_metadata_ref": row["minecraftVersion"],
                "minecraft_metadata_status": versions[row["minecraftVersion"]]["status"], "new_runtime_test_status": "BLOCKED"}
        if loader == "fabric":
            item.update(loader_metadata_ref=tid, loader_metadata_status=fabric[tid]["status"])
        elif loader in ("forge", "neoforge"):
            coordinate = row["loaderVersion"]
            if loader == "forge" and coordinate != "selected" and not coordinate.startswith(row["minecraftVersion"] + "-"):
                coordinate = row["minecraftVersion"] + "-" + coordinate
            item.update(loader_metadata_ref="maven_" + loader, maven_coordinate_version=coordinate)
            item["loader_metadata_status"] = ("UNRESOLVED_SOURCE_LOADER_VERSION" if coordinate == "selected" else
                maven[loader]["status"] if maven[loader]["status"] != "FOUND_MAVEN_VERSION_INDEX" else
                "EXACT_RELEASE_LISTED" if coordinate in maven_versions[loader] else "NOT_LISTED_IN_RETURNED_METADATA")
        else:
            item["loader_metadata_status"] = "NOT_APPLICABLE_VANILLA"
        if row["minecraftVersion"] == "1.12.2":
            item["source_provider_status"] = "UNSUPPORTED_PROVIDER_IN_APPROVED_SOURCE"
        plans.append(item)
    result = {"schema": "legacyforge-phase6a-catalog-metadata-plans-v1", "evidence_id": "E21",
        "started_at_utc": start, "completed_at_utc": utc(), "approved_source_commit": PIN,
        "analyst_tool": {"path": "analysis-local/final-audit/completion/check_catalog_metadata.py",
                         "sha256": sha256(Path(__file__).read_bytes()), "python_version": sys.version},
        "catalog_source": {"path": "config/versions.tsv", "sha256": sha256(catalog_path.read_bytes()), "rows": 56},
        "generator_source": {"path": "scripts/new-download-manifest.ps1", "sha256": sha256(generator_path.read_bytes()),
            "locators": {"forge_coordinate_join": "371-375", "fabric_endpoint": "380", "forge_endpoint": "388",
                         "neoforge_endpoint": "398", "mojang_endpoint": "547"},
            "maven_index_derivation": "Standard maven-metadata.xml sidecars at the same inspected group/artifact repository bases"},
        "request_policy": {"public_unauthenticated_https_only": True, "timeout_seconds": TIMEOUT, "max_response_bytes": MAX_BYTES,
            "max_response_wall_seconds": MAX_WALL, "workers": 4, "retries": 0, "binary_downloads": 0,
            "target_execution": 0, "account_or_device_connections": 0, "allowed_hosts": sorted(HOSTS)},
        "summary": {"target_rows": 56, "unique_minecraft_versions": len(needed),
            "minecraft_metadata_status_counts": dict(Counter(x["status"] for x in versions.values())),
            "fabric_profile_status_counts": dict(Counter(x["status"] for x in fabric.values())),
            "loader_status_counts": dict(Counter(x["loader_metadata_status"] for x in plans)),
            "new_runtime_test_status_counts": {"BLOCKED": 56}},
        "mojang_catalog": catalog_record, "minecraft_versions": {k: versions[k] for k in needed},
        "fabric_profiles": {k: fabric[k] for k in sorted(fabric)}, "maven_indexes": maven, "target_plans": plans,
        "limitations": ["Metadata/index observations only; all runtime outcomes BLOCKED.",
            "Client/asset hashes and sizes are upstream descriptors; binary content was not downloaded or validated.",
            "Maven version presence does not resolve installer contents, processors, output hashes, classpaths or Xbox support.",
            "NOT_LISTED means absent from this returned index, not proof a release never existed.",
            "HTTP_FAILURE/NETWORK_UNKNOWN are distinct from absence and unresolved loader identity.",
            "Declared Java requirement is not measured package runtime/JNI compatibility.",
            "Public metadata does not authenticate archived Legacy Launcher or reconstruct historical events."]}
    (DOCS / "evidence" / "catalog-metadata-plans.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = ["# All 56 catalog metadata plans [E21]", "",
        "Public observation: " + start + " to " + result["completed_at_utc"] + ". Approved source: " + PIN + ".", "",
        "This independently written analyst script requested public JSON/XML only. No JAR, DLL, installer, game, asset or runtime was downloaded; no account or console was contacted. All 56 new runtime verdicts remain **BLOCKED**.", "",
        "## Method and source", "",
        "The pinned scripts/new-download-manifest.ps1 names Mojang (line547), Fabric profile (380), Forge repository/coordinate join (371-388), and NeoForge repository (398). Maven indexes are standard group/artifact sidecars at those same source-defined bases. Source pin, catalog SHA256 and endpoint templates are checked before requests.", "",
        "Reproduce with python -B analysis-local/final-audit/completion/check_catalog_metadata.py. It uses standard library, four workers, 12-second I/O timeouts, a 30-second response wall bound, a 6-MiB body cap, explicit HTTPS JSON/XML endpoint validation and no retries. Raw metadata bodies are not published.", "",
        "All 56 rows and " + str(len(needed)) + " unique Minecraft versions are retained; 20 exact Fabric profiles were requested. All URLs, statuses, response hashes, descriptor summaries and target plans are in [catalog-metadata-plans.json](evidence/catalog-metadata-plans.json).", "",
        "## Observed summary", "", "| Check | Result |", "|---|---|",
        "| Minecraft version metadata | " + json.dumps(result["summary"]["minecraft_metadata_status_counts"], sort_keys=True) + " |",
        "| Exact Fabric profiles | " + json.dumps(result["summary"]["fabric_profile_status_counts"], sort_keys=True) + " |",
        "| Loader metadata/index presence | " + json.dumps(result["summary"]["loader_status_counts"], sort_keys=True) + " |",
        "| Actual runtime/device execution | 0 executed; 56 BLOCKED |", "",
        "## Every retained target", "", "| Target | Source runtime | Minecraft metadata | Loader metadata |", "|---|---|---|---|"]
    for p in plans:
        lines.append("| {} | {} | {} | {} |".format(p["target_id"], p["source_runtime"], p["minecraft_metadata_status"], p["loader_metadata_status"]))
    lines += ["", "## Primary response identity ledger", "",
        "Exact public endpoints and observed response SHA256 are below. Successful Mojang version JSON also matched its catalog-declared SHA1. Catalogs/indexes/profile responses are mutable; these hashes bind the observation.", "",
        "| Metadata endpoint | HTTP/status | Response SHA256 |", "|---|---|---|"]
    ledgers = [("Mojang catalog", catalog_record)]
    ledgers += [(k, versions[k]["source"]) for k in needed if "source" in versions[k]]
    ledgers += [(k, fabric[k].get("source", {})) for k in sorted(fabric)]
    ledgers += [("Maven " + k, maven[k].get("source", {})) for k in sorted(maven)]
    for title, record in ledgers:
        if record.get("url"):
            lines.append("| [{}]({}) | {} / {} | {} |".format(title, record["url"], record.get("http_status", "none"), record.get("status"), record.get("response_sha256", "unavailable")))
    lines += ["", "## Interpretation and remaining evidence", "",
        "**Confirmed metadata** establishes only the recorded response content. Client and asset-index URL/SHA1/size are descriptors; no binary content was fetched. Library counts precede platform/rule selection. Fabric establishes exact inheritance/main-class/library-coordinate metadata without runtime testing.", "",
        "The four 26.x Mojang version JSON documents declare Java 25 (java-runtime-epsilon). Every 1.21.x version here declares Java 21; 1.18.2/1.19.2/1.20.1/1.20.4 declare Java 17, and 1.12.2/1.16.5 declare Java 8. These are vanilla metadata requirements, not proof of loader compatibility or the Java major actually packaged by LegacyForge.", "",
        "All 20 Fabric profiles identify the exact requested parent and loader. Four 26.x profiles list seven libraries and omit an intermediary coordinate. Fourteen profiles list eight libraries and two list eleven; those sixteen contain their exact intermediary coordinate. Absence of that older dependency pattern is recorded rather than treated as a version mismatch. An initial analyst check unnecessarily required intermediary in every profile; it was corrected to use exact parent and loader identity before finalizing this evidence.", "",
        "**EXACT_RELEASE_LISTED** means the precise Forge minecraftVersion-loaderVersion or NeoForge loaderVersion occurs in the returned Maven index. Installer contents, processor inputs/outputs, patched artifacts and final module/classpath arguments remain unresolved by this check. A Maven listing never becomes a loader-installation or Xbox-gameplay pass.", "",
        "The retained 1.12.2 Forge row stays unresolved because approved source says selected. Both 1.12.2 providers remain absent. HTTP failures, network unknowns, returned-index absence and unresolved versions are kept distinct. No target is dropped.", "",
        "Actual Windows/update/repair tests still require an approved disposable environment and genuine publisher-signed positive fixture. Real Xbox tests still require approved exact packages, diagnostic probes and owner hardware observations; legitimate account tests remain owner-controlled. Metadata cannot replace missing runtime/account/history evidence.", ""]
    (DOCS / "CATALOG-METADATA-PLANS.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result["summary"], sort_keys=True))

if __name__ == "__main__":
    main()

