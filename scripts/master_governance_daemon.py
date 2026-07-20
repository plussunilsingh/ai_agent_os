#!/usr/bin/env python3
"""
AI-SE OS Master Governance Supervisor Daemon
Runs continuously in the background to monitor target applications (/admin, /botanixUI),
enforces Chapter 42 Truth Governance rules, measures real HTTP SLA latencies,
and updates docs/master_governance_telemetry.json without blocking the master agent window.
"""

import os
import sys
import json
import time
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ai_se_os.validation.truth_governance import TruthGovernanceEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Daemon] %(message)s")
logger = logging.getLogger("GovernanceDaemon")

def run_governance_daemon():
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    admin_repo = os.path.join(workspace_root, "admin")
    botanix_repo = os.path.join(workspace_root, "botanixUI")
    telemetry_file = os.path.join(os.path.dirname(__file__), "..", "docs", "master_governance_telemetry.json")
    status_doc = os.path.join(os.path.dirname(__file__), "..", "docs", "master_governance_status.md")
    
    logger.info("🛡️ Starting Master Governance Supervisor Daemon...")
    
    iteration = 0
    while True:
        iteration += 1
        logger.info(f"🔄 Execution Monitoring Cycle #{iteration}...")
        
        # 1. Real Java Build Check
        java_build = TruthGovernanceEngine.verify_java_build(admin_repo)
        
        # 2. Real HTTP Latency Check on Port 8080 (Context /api/v1/actuator/health)
        backend_http = TruthGovernanceEngine.measure_real_http_latency("http://127.0.0.1:8080/api/v1/actuator/health", 8080)
        
        # 3. Real HTTP Latency Check on BotanixUI Port 9000
        frontend_http = TruthGovernanceEngine.measure_real_http_latency("http://127.0.0.1:9000", 9000)
        
        # 4. Real HTTP Latency Check on AI-SE OS Port 8000
        ai_os_http = TruthGovernanceEngine.measure_real_http_latency("http://127.0.0.1:8000/health", 8000)
        
        telemetry = {
            "cycle": iteration,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "governance_policy": "Chapter 42 - Truth Enforcement Active",
            "target_apps": {
                "java_admin": {
                    "repo_path": admin_repo,
                    "build_passed": java_build["build_passed"],
                    "exit_code": java_build["exit_code"],
                    "http_status": backend_http
                },
                "botanix_ui": {
                    "repo_path": botanix_repo,
                    "port": 9000,
                    "http_status": frontend_http
                },
                "ai_se_os_engine": {
                    "port": 8000,
                    "http_status": ai_os_http
                }
            }
        }
        
        # Write JSON Telemetry
        with open(telemetry_file, "w", encoding="utf-8") as f:
            json.dump(telemetry, f, indent=2)
            
        # Write Markdown Status Doc
        md_content = f"""# 🛡️ Master Governance Telemetry Status (Cycle #{iteration})

**Last Updated**: {telemetry['timestamp']}  
**Governance Standard**: AI-SE OS Constitution Chapter 42 (Truth & Validation)  
**Daemon Status**: 🟢 Running Asynchronously  

---

## ☕ Java Admin App Status (`/admin`)
- **Build Passed**: `{java_build['build_passed']}` (Exit Code: `{java_build['exit_code']}`)
- **HTTP Reachable**: `{backend_http['reachable']}`
- **HTTP Status Code**: `{backend_http['status_code']}`
- **Measured Real Latency**: `{backend_http['measured_latency_ms']} ms`

---

## 🎨 BotanixUI App Status (`/botanixUI` - Port 9000)
- **HTTP Reachable**: `{frontend_http['reachable']}`
- **HTTP Status Code**: `{frontend_http['status_code']}`
- **Measured Real Latency**: `{frontend_http['measured_latency_ms']} ms`

---

## 🤖 AI-SE OS Core Server (`/AI_AGENT_OS` - Port 8000)
- **HTTP Reachable**: `{ai_os_http['reachable']}`
- **HTTP Status Code**: `{ai_os_http['status_code']}`
- **Measured Real Latency**: `{ai_os_http['measured_latency_ms']} ms`
"""
        with open(status_doc, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        logger.info(f"Cycle #{iteration} complete. Slept 30s.")
        time.sleep(30)

if __name__ == "__main__":
    run_governance_daemon()
