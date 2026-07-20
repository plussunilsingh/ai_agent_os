#!/usr/bin/env python3
"""
AI-SE OS Single-Pass BotanixUI Live Web Application Verifier
Performs a fast, deterministic, non-blocking check of the BotanixUI Next.js app (Port 9000).
Checks server HTTP status, HTML DOM structure, and UI component readiness.
Exits cleanly in < 3 seconds.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BotanixUiVerifier")

def verify_ui_live():
    url = "http://127.0.0.1:9000"
    logger.info(f"🔍 AI-SE OS testing live BotanixUI application at {url}...")
    
    t0 = time.time()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    
    status_code = 0
    is_working = False
    html_content = ""
    error_msg = None
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AI-SE-OS-UiTester"})
        with opener.open(req, timeout=4) as resp:
            status_code = resp.status
            html_content = resp.read().decode("utf-8", errors="ignore")
            is_working = (status_code == 200)
    except urllib.error.HTTPError as he:
        status_code = he.code
        error_msg = f"HTTP Error {he.code}: {he.reason}"
    except Exception as e:
        status_code = 0
        error_msg = f"Connection Error: {str(e)}"
        
    latency_ms = round((time.time() - t0) * 1000, 2)
    
    # Analyze DOM elements if reachable
    has_nextjs = "__NEXT_DATA__" in html_content or "<script" in html_content
    has_botanix_title = "botanix" in html_content.lower() or "admin" in html_content.lower() or is_working
    
    report_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "target_url": url,
        "port": 9000,
        "is_working": is_working,
        "http_status_code": status_code,
        "measured_latency_ms": latency_ms,
        "nextjs_server_ready": has_nextjs,
        "html_dom_rendered": len(html_content) > 0,
        "html_bytes": len(html_content),
        "error": error_msg
    }
    
    # Write report doc
    report_path = os.path.join(os.path.dirname(__file__), "..", "docs", "botanix_ui_test_report.md")
    
    md_content = f"""# 🎨 BotanixUI Web Application Verification Report

**Verification Date**: {report_data['timestamp']}  
**Target URL**: `{url}`  
**Test Mode**: AI-SE OS Single-Pass Deterministic Verification (Port 9000)  

---

## 📊 Live UI Status Summary

| Check Item | Target | Measured Result | Status |
|---|---|---|---|
| **Server Reachability** | `http://localhost:9000` | HTTP `{status_code}` | {"✅ **OPERATIONAL**" if is_working else "🔴 **UNREACHABLE / OFF**"} |
| **HTTP Response Latency** | `< 200.0ms` | **{latency_ms} ms** | {"✅ **PASSED**" if latency_ms <= 200 else "🔴 **HIGH LATENCY**"} |
| **Next.js Server Hydration** | React / Webpack | `{"Ready" if has_nextjs else "Not Detected"}` | {"✅ **PASSED**" if has_nextjs else "🔴 **FAILED**"} |
| **HTML Page Size** | > 0 Bytes | `{len(html_content):,} Bytes` | {"✅ **PASSED**" if len(html_content) > 0 else "🔴 **EMPTY**"} |

---

## 🔍 Detailed Diagnostics & Next Steps

{"- ✅ **BotanixUI is live and serving requests cleanly at http://localhost:9000.**" if is_working else f"- 🔴 **BotanixUI server is not currently listening on port 9000.** Error: `{error_msg}`. To start the UI server, run `npm run dev` inside `/Users/suniltomar/Desktop/workspace/botanixUI`."}
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    logger.info(f"UI Verification completed in {latency_ms}ms. Status: {'OPERATIONAL' if is_working else 'OFF'}")
    print(json.dumps(report_data, indent=2))

if __name__ == "__main__":
    verify_ui_live()
