"""Synthetic controls for the receipt validator only. No target/device execution."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
DOCS = ROOT.parents[2] / "docs" / "research" / "legacy-launcher"
if not DOCS.is_dir():
    DOCS = Path(r"C:\Users\arinze\Desktop\ReverseLegacyCraft\docs\research\legacy-launcher")
PHASE = sys.argv[1] if len(sys.argv) > 1 else "baseline"
FIXTURES = ROOT / "validator-controls"
FIXTURES.mkdir(exist_ok=True)
PLAN = json.loads((DOCS / "tests" / "test-cases.json").read_text(encoding="utf-8"))
CASES = {c["test_id"]: c for c in PLAN["cases"]}
spec = importlib.util.spec_from_file_location("receipt_validator", DOCS / "tools" / "verify-test-receipts.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

ATTACHMENT = FIXTURES / "SYNTHETIC-CONTROL-ONLY.txt"
ATTACHMENT.write_text("Synthetic validator control. No Windows/Xbox/device/target test was performed.\n", encoding="utf-8")
ATTACHMENT_HASH = hashlib.sha256(ATTACHMENT.read_bytes()).hexdigest()
TARGET_PLAN = next(p for p in PLAN["target_plans"] if p["runtime_id"] == "java21" and p["loader"] == "fabric")
BASE_TARGET = {k: TARGET_PLAN[k] for k in ("minecraft_version", "loader", "loader_version", "runtime_id")}
BASE_TARGET.update(java_major=21, jni_requested=21, jni_accepted=21)

def make(test_id):
    receipt = {
        "schema": "legacyforge-phase6a-test-receipt-v1",
        "test_id": test_id, "status": "PASS", "reason": "SYNTHETIC VALIDATOR CONTROL ONLY",
        "source_commit": mod.COMMIT,
        "environment": {"type": "synthetic-validator-control", "os_build": "SYNTHETIC-NO-DEVICE",
            "console_model": "Xbox Series X", "debugger_attached": False,
            "network_mode": "synthetic-no-network", "isolation_type": "virtual-machine", "isolation_approved": True},
        "artifacts": {key: hashlib.sha256(key.encode()).hexdigest() for key in mod.SECTION_FIELDS["artifacts"]},
        "target": copy.deepcopy(BASE_TARGET),
        "observation": {
            "exit_or_hresult": 0, "duration_ms": 1, "memory_peak_bytes": 1,
            "checked_files": 1, "reused_files": 1, "downloaded_files": 0, "hash_failures": 0,
            "graphics_version": "SYNTHETIC", "presented_frames": 1, "symptom": "SYNTHETIC CONTROL ONLY",
            "signature_acceptance": True, "signature_rejections": ["synthetic-truncation"],
            "synthetic_java_result": "fixture", "resource_samples": [{"synthetic": True}],
            "graphics_capability_results": {"synthetic": True}, "auth_stage_results": {"synthetic": True},
            "ownership_result": "SYNTHETIC-NO-ACCOUNT"
        },
        "constraints": ["SYNTHETIC CONTROL. Never report as actual hardware or target evidence."],
        "evidence": {"kind": "actual-test-observation", "observed_at_utc": "2026-10-17T00:00:00Z",
            "observer_role": "SYNTHETIC validator control only; no hardware or target execution",
            "criteria_results": {c["id"]: True for c in CASES[test_id]["criteria"]},
            "attachments": [{"path": ATTACHMENT.name, "sha256": ATTACHMENT_HASH}]}
    }
    return receipt

def write(receipt):
    path = FIXTURES / (receipt["test_id"] + ".synthetic.json")
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return path

priors = {}
for n in list(range(1, 12)) + [13]:
    key = "X%02d" % n
    priors[key] = make(key)
    write(priors[key])
linked = make("X12")
linked["evidence"]["prerequisite_receipts"] = [key + ".synthetic.json" for key in priors]
results = []

def run(name, receipt, expected_valid):
    try:
        errors = mod.validate(receipt, CASES, FIXTURES / "X12.synthetic.json", PLAN["target_plans"])
        exception = None
    except Exception as exc:
        errors = []
        exception = type(exc).__name__ + ": " + str(exc)
    observed_valid = not errors and exception is None
    results.append({"name": name, "expected_valid": expected_valid, "observed_valid": observed_valid,
                    "control_satisfied": observed_valid == expected_valid and exception is None,
                    "errors": errors, "exception": exception})

run("valid_blocked_template_is_not_pass", json.loads((DOCS / "tests" / "result.template.json").read_text(encoding="utf-8")), True)
run("well_formed_synthetic_windows_receipt", make("W01"), True)
run("well_formed_synthetic_x12_linked_receipts", linked, True)
windows_loader = make("W10")
windows_loader["artifacts"].pop("mesa_sha256", None)
windows_loader["artifacts"].pop("glfw_sha256", None)
run("desktop_loader_uses_actual_provider_not_assumed_mesa", windows_loader, True)
upper_hashes = copy.deepcopy(linked)
for key in upper_hashes["artifacts"]:
    upper_hashes["artifacts"][key] = upper_hashes["artifacts"][key].upper()
run("hex_hash_case_is_not_a_different_artifact", upper_hashes, True)

def mutate(name, path, value, source=None):
    r = copy.deepcopy(source or linked)
    current = r
    parts = path.split(".")
    for part in parts[:-1]:
        current = current[part]
    current[parts[-1]] = value
    run(name, r, False)

mutate("wrong_source_commit", "source_commit", "0" * 40)
mutate("unknown_top_level_field", "forbidden", "synthetic")
mutate("unknown_nested_field", "target.access_token", "SYNTHETIC-NOT-A-REAL-TOKEN")
mutate("wrong_console", "environment.console_model", "desktop")
mutate("unapproved_isolation", "environment.isolation_approved", False, make("W01"))
mutate("nonisolated_windows", "environment.isolation_type", "host", make("W01"))
mutate("debugger_resource_measurement", "environment.debugger_attached", True, make("X02"))
mutate("non_utc_observation", "evidence.observed_at_utc", "2026-10-17T01:00:00+01:00")
mutate("static_evidence_kind", "evidence.kind", "static-source")
mutate("missing_passing_criterion", "evidence.criteria_results", {})
mutate("outside_attachment", "evidence.attachments", [{"path": "../outside.txt", "sha256": ATTACHMENT_HASH}])
mutate("bad_attachment_hash", "evidence.attachments", [{"path": ATTACHMENT.name, "sha256": "0"*64}])
mutate("unknown_target_tuple", "target.minecraft_version", "SYNTHETIC-UNKNOWN")
mutate("wrong_target_java_major", "target.java_major", 17)
mutate("missing_predecessors", "evidence.prerequisite_receipts", [])
mutate("missing_loader_inventory", "artifacts.loader_inventory_sha256", None)
mutate("malformed_target_null", "target", None)
mutate("malformed_target_list", "target", [])

unsupported = copy.deepcopy(linked)
p = next(p for p in PLAN["target_plans"] if p["source_implementation_status"] == "UNSUPPORTED_PROVIDER")
for k in ("minecraft_version", "loader", "loader_version", "runtime_id"):
    unsupported["target"][k] = p[k]
unsupported["target"]["java_major"] = p["java_major_expected"]
run("unsupported_catalog_provider", unsupported, False)

for test_id, field, value, control_name in [
    ("X03", "artifacts.appx_sha256", "0"*64, "predecessor_package_mismatch"),
    ("X05", "target.minecraft_version", "SYNTHETIC-OTHER", "predecessor_tuple_mismatch"),
    ("X03", "artifacts.jvm_sha256", "0"*64, "predecessor_jvm_identity_mismatch"),
    ("X05", "artifacts.glfw_sha256", "0"*64, "predecessor_native_identity_mismatch"),
    ("X05", "artifacts.manifest_sha256", "0"*64, "predecessor_manifest_identity_mismatch"),
    ("X10", "artifacts.loader_inventory_sha256", "0"*64, "predecessor_loader_inventory_mismatch"),
    ("X03", "target.java_major", 17, "predecessor_java_major_mismatch")
]:
    altered = copy.deepcopy(priors[test_id])
    current = altered
    parts = field.split(".")
    for part in parts[:-1]:
        current = current[part]
    current[parts[-1]] = value
    write(altered)
    run(control_name, linked, False)
    write(priors[test_id])

write(linked)

report = {"schema": "phase6a-receipt-validator-controls-v1", "phase": PHASE,
          "meaning": "Synthetic format/reference controls only. No target, guest, hardware or account test ran.",
          "control_count": len(results), "satisfied": sum(x["control_satisfied"] for x in results),
          "validator_sha256": hashlib.sha256((DOCS / "tools" / "verify-test-receipts.py").read_bytes()).hexdigest(),
          "test_plan_sha256": hashlib.sha256((DOCS / "tests" / "test-cases.json").read_bytes()).hexdigest(),
          "results": results}
(ROOT / ("validator-controls-" + PHASE + ".json")).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"phase": PHASE, "control_count": report["control_count"], "satisfied": report["satisfied"],
                  "failures": [x["name"] for x in results if not x["control_satisfied"]]}))

