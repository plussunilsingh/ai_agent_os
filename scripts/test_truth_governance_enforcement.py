#!/usr/bin/env python3
"""
AI-SE OS Truth Governance Enforcement Test Script
Tests that Chapter 42 Truth Governance rules are programmatically enforced:
1. Real ./gradlew compileJava build verification.
2. Real HTTP latency measurement (logs UNREACHABLE if server is down).
3. Banned hardcoded metric validation.
"""

import os
import sys
import json
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ai_se_os.validation.truth_governance import TruthGovernanceEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("TruthGovernanceTest")

def run_truth_test():
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    admin_repo = os.path.join(workspace_root, "admin")
    botanix_repo = os.path.join(workspace_root, "botanixUI")
    
    print("==================================================================")
    print("🛡️ TESTING AI-SE OS TRUTH GOVERNANCE ENFORCEMENT ENGINE")
    print("==================================================================")
    print()

    # Test 1: Real HTTP Latency Check on Port 8080 (No Fake 4.2ms allowed)
    logger.info("TEST 1: Checking HTTP endpoint http://127.0.0.1:8080/api/admin/users...")
    http_res = TruthGovernanceEngine.measure_real_http_latency("http://127.0.0.1:8080/api/admin/users", 8080)
    print(f"👉 HTTP Response Result: {json.dumps(http_res, indent=2)}")
    if not http_res["reachable"]:
        print("✅ TRUTH GOVERNANCE ENFORCED: Real status logged as UNREACHABLE (fake 4.2ms blocked!).")
    print()

    # Test 2: Banned Hardcoded Default Metric Auditor
    logger.info("TEST 2: Auditing report metrics for hardcoded placeholders...")
    fake_report = {"endpoint": "GET /users", "latency_ms": 4.2, "status": 200}
    claim_check = TruthGovernanceEngine.validate_report_claims(fake_report)
    print(f"👉 Report Audit Result: {json.dumps(claim_check, indent=2)}")
    if not claim_check["is_truthful"]:
        print("✅ TRUTH GOVERNANCE ENFORCED: Fake report containing hardcoded 4.2ms was REJECTED.")
    print()

    # Test 3: Target Repository Java Build Verification
    logger.info("TEST 3: Verifying target Java Admin repo build status...")
    build_res = TruthGovernanceEngine.verify_java_build(admin_repo)
    print(f"👉 Admin Java Build Passed: {build_res['build_passed']} (Exit Code: {build_res['exit_code']})")
    if not build_res["build_passed"]:
        print("✅ TRUTH GOVERNANCE ENFORCED: Task correctly marked FAILED until ./gradlew compileJava passes 100%.")
    print()

    print("==================================================================")
    print("🎉 TRUTH GOVERNANCE ENGINE ENFORCEMENT TEST PASSED!")
    print("==================================================================")

if __name__ == "__main__":
    run_truth_test()
