"""Cross-check vanilla declared Java requirements against all56 research target plans; no target execution."""
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs" / "research" / "legacy-launcher"
PIN = "d1453434ceefe73bef5aff497194e09f39dde7e1"
PATH = DOCS / "tests" / "test-cases.json"
METADATA = DOCS / "evidence" / "catalog-metadata-plans.json"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    before_hash = digest(PATH)
    plan = json.loads(PATH.read_text(encoding="utf-8"))
    original = json.loads(PATH.read_text(encoding="utf-8"))
    upstream = json.loads(METADATA.read_text(encoding="utf-8"))
    assert plan["source_commit"] == upstream["approved_source_commit"] == PIN
    with (ROOT / "analysis-local" / "legacyforge-d145343" / "config" / "versions.tsv").open(encoding="utf-8-sig", newline="") as file:
        source = list(csv.DictReader(file, delimiter="\t"))
    assert len(source) == len(plan["target_plans"]) == 56
    source_tuples = {(r["minecraftVersion"], r["loader"], r["loaderVersion"], r["javaRuntime"]) for r in source}
    plan_tuples = {(r["minecraft_version"], r["loader"], r["loader_version"], r["runtime_id"]) for r in plan["target_plans"]}
    assert source_tuples == plan_tuples
    current_majors = {upstream["minecraft_versions"][r["minecraft_version"]]["java_requirement_declared"]["majorVersion"]
                      for r in plan["target_plans"] if r["runtime_id"] == "current"}
    assert current_majors == {25}, "Current-runtime expected major not uniformly established as25"
    rows = []
    for row in plan["target_plans"]:
        meta = upstream["minecraft_versions"][row["minecraft_version"]]
        assert meta["status"] == "FOUND_HASH_VERIFIED_METADATA"
        assert meta["catalog_sha1_matches"] is True
        major = meta["java_requirement_declared"]["majorVersion"]
        before = row.get("java_major_expected")
        if row["runtime_id"] == "current":
            row["java_major_expected"] = 25
            row["java_major_expected_basis"] = "E21_UPSTREAM_VANILLA_DECLARED_REQUIREMENT_NOT_PACKAGED_RUNTIME_OBSERVATION"
        expected = row.get("java_major_expected")
        row["observed_upstream_java_major"] = major
        row["observed_upstream_java_component"] = meta["java_requirement_declared"].get("component")
        row["observed_upstream_metadata_url"] = meta["source"]["url"]
        row["observed_upstream_metadata_sha1"] = meta["catalog_declared_sha1"]
        row["observed_upstream_metadata_sha256"] = meta["source"]["response_sha256"]
        row["upstream_java_requirement_evidence_id"] = "E21"
        if expected is None:
            comparison = "SOURCE_EXPECTED_MAJOR_UNKNOWN"
        elif expected < major:
            comparison = "SOURCE_RUNTIME_TOO_OLD_FOR_DECLARED_VANILLA_BASELINE"
            if "SOURCE_RUNTIME_TOO_OLD_FOR_UPSTREAM_DECLARED_JAVA" not in row["blockers"]:
                row["blockers"].append("SOURCE_RUNTIME_TOO_OLD_FOR_UPSTREAM_DECLARED_JAVA")
        elif expected > major:
            comparison = "ABOVE_VANILLA_BASELINE_LOADER_AND_RUNTIME_UNVERIFIED"
        else:
            comparison = "MATCHES_DECLARED_VANILLA_BASELINE_RUNTIME_UNVERIFIED"
        row["runtime_baseline_comparison"] = comparison
        assert row["new_runtime_status"] == "BLOCKED"
        rows.append({"target_id": row["target_id"], "source_runtime": row["runtime_id"],
            "expected_major_before": before, "expected_major_after": expected,
            "upstream_declared_java_major": major, "comparison": comparison,
            "metadata_url": meta["source"]["url"], "catalog_sha1": meta["catalog_declared_sha1"],
            "metadata_sha256": meta["source"]["response_sha256"], "new_runtime_status": "BLOCKED"})
    for key in original:
        if key != "target_plans":
            assert original[key] == plan[key], "Only target_plans may change"
    temp = PATH.with_name(PATH.name + ".runtime-crosscheck.tmp")
    temp.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    temp.replace(PATH)
    result = {"schema": "legacyforge-phase6a-catalog-runtime-crosscheck-v1",
        "checked_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "approved_source_commit": PIN, "target_rows": len(rows),
        "current_expected_major_updated_to25": sum(r["source_runtime"] == "current" for r in rows),
        "matches_declared_baseline": sum(r["comparison"].startswith("MATCHES") for r in rows),
        "above_declared_baseline": sum(r["comparison"].startswith("ABOVE") for r in rows),
        "too_old_for_declared_baseline": sum(r["comparison"].startswith("SOURCE_RUNTIME_TOO_OLD") for r in rows),
        "test_plan_sha256_before": before_hash, "test_plan_sha256_after": digest(PATH),
        "metadata_evidence_sha256": digest(METADATA),
        "target_plans_only_update": True,
        "production_or_source_catalog_modified": False, "target_execution": 0,
        "runtime_results": {"BLOCKED": len(rows)}, "rows": rows,
        "limitations": [
            "Comparison is between research expected majors and upstream vanilla metadata declarations, not measured packaged JVMs.",
            "Higher-than-vanilla selected Java does not prove loader/game compatibility or diagnose a defect.",
            "Java25 current expectation is now pinned to verified upstream26.x metadata; actual package/runtime identity remains unavailable.",
            "No too-old major found among these labels, but JNI21 versusJava17/legacy and absent providers remain blocked as recorded.",
            "Loader-specific Java requirements, native ABI and hardware behavior require separate evidence."
        ]}
    out = Path(__file__).with_name("catalog-runtime-crosscheck.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("target_rows", "current_expected_major_updated_to25",
        "matches_declared_baseline", "above_declared_baseline", "too_old_for_declared_baseline", "target_plans_only_update")}))
if __name__ == "__main__":
    main()

