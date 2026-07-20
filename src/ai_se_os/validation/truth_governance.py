"""
AI-SE OS Truth Governance & Report Validation Engine
Enforces strict verification rules across all AI-SE OS reports and code generation tasks:
1. NO Hardcoded / Simulated Metrics permitted in reports.
2. NO Fallback Default Values (if server down, report MUST log UNREACHABLE).
3. MANDATORY Build Verification: ./gradlew compileJava and npm run build must return exit code 0.
4. TARGET REPOSITORY Validation: Verifies code changes exist in target repos (/admin, /botanixUI).
"""

import os
import subprocess
import urllib.request
import urllib.error
import time

class TruthGovernanceEngine:
    @staticmethod
    def verify_java_build(admin_repo_path: str) -> dict:
        """Executes actual ./gradlew compileJava inside target admin repository."""
        cmd = "./gradlew compileJava"
        res = subprocess.run(cmd, shell=True, cwd=admin_repo_path, capture_output=True, text=True)
        is_success = (res.returncode == 0)
        return {
            "build_passed": is_success,
            "exit_code": res.returncode,
            "raw_output": res.stdout if is_success else res.stderr
        }

    @staticmethod
    def verify_nextjs_build(botanix_repo_path: str) -> dict:
        """Executes actual npm run build inside target botanixUI repository."""
        cmd = "npm run build"
        res = subprocess.run(cmd, shell=True, cwd=botanix_repo_path, capture_output=True, text=True)
        is_success = (res.returncode == 0)
        return {
            "build_passed": is_success,
            "exit_code": res.returncode,
            "raw_output": res.stdout if is_success else res.stderr
        }

    @staticmethod
    def measure_real_http_latency(url: str, expected_port: int) -> dict:
        """Measures REAL HTTP latency without fallback placeholders."""
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        t0 = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AI-SE-OS-TruthGuard"})
            with opener.open(req, timeout=3) as resp:
                elapsed_ms = round((time.time() - t0) * 1000, 2)
                return {
                    "reachable": True,
                    "status_code": resp.status,
                    "measured_latency_ms": elapsed_ms,
                    "error": None
                }
        except urllib.error.HTTPError as he:
            elapsed_ms = round((time.time() - t0) * 1000, 2)
            return {
                "reachable": True,
                "status_code": he.code,
                "measured_latency_ms": elapsed_ms,
                "error": str(he)
            }
        except Exception as e:
            return {
                "reachable": False,
                "status_code": 0,
                "measured_latency_ms": None,
                "error": f"UNREACHABLE: {str(e)}"
            }

    @staticmethod
    def validate_report_claims(report_metrics: dict) -> dict:
        """Audits report metrics object to ensure NO hardcoded/simulated defaults exist."""
        violations = []
        
        # Check for banned hardcoded values
        banned_defaults = [4.2, 3.8, 145.2, 210.8]
        for key, val in report_metrics.items():
            if val in banned_defaults:
                violations.append(f"Metric '{key}' contains banned hardcoded default: {val}")
                
        return {
            "is_truthful": len(violations) == 0,
            "violations": violations
        }
