#!/usr/bin/env python3
"""
AI-SE OS Full UI Page & API End-to-End Test Suite
Tests every BotanixUI page and API call with Chapter 42 Truth Governance rules.
Outputs docs/ui_and_api_verification_matrix.md
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("UIApiTestSuite")

def run_suite():
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    
    print("==================================================================")
    print("🧪 AI-SE OS: FULL UI PAGE & API END-TO-END VERIFICATION SUITE")
    print("==================================================================")
    
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "auth_flow": {},
        "apis": [],
        "pages": []
    }
    
    # Step 1: Login & Session Token Acquisition
    t0 = time.time()
    try:
        login_payload = json.dumps({"action": "login", "username": "superadmin", "password": "superadmin@123"}).encode()
        req = urllib.request.Request("http://127.0.0.1:9000/api/admin/auth", data=login_payload, headers={"Content-Type": "application/json"})
        with opener.open(req, timeout=4) as resp:
            data = json.loads(resp.read().decode())
            token = data.get("token")
            results["auth_flow"] = {
                "success": data.get("success", False),
                "username": data.get("username"),
                "token_acquired": bool(token),
                "latency_ms": round((time.time() - t0) * 1000, 2)
            }
    except Exception as e:
        results["auth_flow"] = {"success": False, "error": str(e)}
        token = None

    # Step 2: Test API Endpoints
    apis_to_test = [
        ("Auth Login Proxy", "http://127.0.0.1:9000/api/admin/auth", "POST"),
        ("Material Intake API", "http://127.0.0.1:9000/api/admin/materials/intake", "GET"),
        ("Inventory Control API", "http://127.0.0.1:9000/api/admin/inventory", "GET"),
        ("Spring Boot Actuator Health", "http://127.0.0.1:8080/api/v1/actuator/health", "GET")
    ]
    
    for name, url, method in apis_to_test:
        t0 = time.time()
        try:
            headers = {"User-Agent": "AI-SE-OS-UiTester"}
            if token:
                headers["Authorization"] = f"Bearer {token}"
                
            if method == "POST":
                headers["Content-Type"] = "application/json"
                body = json.dumps({"action": "validate", "token": token}).encode()
                req = urllib.request.Request(url, data=body, headers=headers, method="POST")
            else:
                req = urllib.request.Request(url, headers=headers, method="GET")
                
            with opener.open(req, timeout=4) as resp:
                elapsed = round((time.time() - t0) * 1000, 2)
                results["apis"].append({
                    "name": name,
                    "url": url,
                    "method": method,
                    "status": resp.status,
                    "latency_ms": elapsed,
                    "passed": resp.status in [200, 201]
                })
        except urllib.error.HTTPError as he:
            elapsed = round((time.time() - t0) * 1000, 2)
            results["apis"].append({
                "name": name,
                "url": url,
                "method": method,
                "status": he.code,
                "latency_ms": elapsed,
                "passed": he.code in [200, 201]
            })
        except Exception as e:
            elapsed = round((time.time() - t0) * 1000, 2)
            results["apis"].append({
                "name": name,
                "url": url,
                "method": method,
                "status": 0,
                "latency_ms": elapsed,
                "passed": False,
                "error": str(e)
            })

    # Step 3: Test BotanixUI Pages (Port 9000)
    ui_pages = [
        ("Dashboard", "http://127.0.0.1:9000/admin/dashboard"),
        ("Live Stock", "http://127.0.0.1:9000/admin/products"),
        ("Incoming Material", "http://127.0.0.1:9000/admin/incoming"),
        ("Dispatch Samples", "http://127.0.0.1:9000/admin/samples"),
        ("Logistics Lookup", "http://127.0.0.1:9000/admin/logistics"),
        ("Batch Traceability", "http://127.0.0.1:9000/admin/traceability"),
        ("Sales", "http://127.0.0.1:9000/admin/sales"),
        ("Customers", "http://127.0.0.1:9000/admin/customers"),
        ("Suppliers", "http://127.0.0.1:9000/admin/suppliers")
    ]
    
    for name, page_url in ui_pages:
        t0 = time.time()
        try:
            req = urllib.request.Request(page_url, headers={"User-Agent": "AI-SE-OS-UiTester"})
            with opener.open(req, timeout=4) as resp:
                elapsed = round((time.time() - t0) * 1000, 2)
                html = resp.read().decode('utf-8', errors='ignore')
                results["pages"].append({
                    "name": name,
                    "url": page_url,
                    "status": resp.status,
                    "latency_ms": elapsed,
                    "dom_bytes": len(html),
                    "passed": resp.status == 200
                })
        except Exception as e:
            elapsed = round((time.time() - t0) * 1000, 2)
            results["pages"].append({
                "name": name,
                "url": page_url,
                "status": 0,
                "latency_ms": elapsed,
                "passed": False,
                "error": str(e)
            })

    # Write Markdown Verification Matrix Report
    doc_path = os.path.join(os.path.dirname(__file__), "..", "docs", "ui_and_api_verification_matrix.md")
    
    md = f"""# 🧪 UI & API Full Verification Matrix Report

**Audit Timestamp**: {results['timestamp']}  
**Governance Policy**: AI-SE OS Constitution Chapter 42 (Zero Fake Claims / Real Sockets)  

---

## 🔑 1. Authentication & Session Flow
- **Login Executed**: `superadmin`
- **Token Acquired**: `{results['auth_flow']['token_acquired']}`
- **Auth Status**: `{"🟢 SUCCESS" if results['auth_flow']['success'] else "🔴 FAILED"}`
- **Measured Auth Latency**: `{results['auth_flow']['latency_ms']} ms`

---

## ⚡ 2. API Endpoints Health Matrix

| API Endpoint | Target URL | Method | HTTP Status | Measured Latency | Governance Result |
|---|---|---|---|---|---|
"""
    for api in results["apis"]:
        status_icon = "🟢 **PASSED**" if api["passed"] else "🔴 **FAILED**"
        md += f"| **{api['name']}** | `{api['url']}` | `{api['method']}` | `{api['status']}` | `{api['latency_ms']} ms` | {status_icon} |\n"

    md += """
---

## 🎨 3. BotanixUI Page Render Matrix (Port 9000)

| UI Module Page | Route URL | HTTP Status | DOM Size | Measured Render Latency | Verification Status |
|---|---|---|---|---|---|
"""
    for pg in results["pages"]:
        status_icon = "🟢 **OPERATIONAL**" if pg["passed"] else "🔴 **UNREACHABLE**"
        md += f"| **{pg['name']}** | `{pg['url']}` | `{pg['status']}` | `{pg.get('dom_bytes', 0):,} Bytes` | `{pg['latency_ms']} ms` | {status_icon} |\n"

    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(md)
        
    print(json.dumps(results, indent=2))
    logger.info(f"UI & API Verification Matrix saved to {doc_path}")

if __name__ == "__main__":
    run_suite()
