#!/usr/bin/env python3
import urllib.request
import urllib.error
import json

endpoints = [
    "/api/admin/auth",
    "/api/admin/materials/intake",
    "/api/admin/inventory/dashboard",
    "/api/admin/inventory/purchases?page=0&size=100",
    "/api/admin/inventory/sales?page=0&size=100",
    "/api/admin/inventory/customers",
    "/api/admin/inventory/suppliers",
    "/api/admin/inventory/materials",
    "/api/admin/inventory/supplier-samples?page=0&size=100",
    "/api/admin/inventory/sample-dispatches?page=0&size=100",
    "/api/admin/pricing",
    "/api/admin/config",
    "/api/admin/leads",
    "/api/admin/logs",
    "/api/admin/communications"
]

print("🔍 SCANNING ALL BOTANIX UI API ENDPOINTS AGAINST BACKEND...")
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

for ep in endpoints:
    url = f"http://127.0.0.1:9000{ep}"
    try:
        req = urllib.request.Request(url, headers={"Authorization": "Bearer fake", "x-botanix-user-name": "superadmin"})
        with opener.open(req, timeout=3) as resp:
            print(f"🟢 [{resp.status}] {ep}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"🔴 [{e.code}] {ep} -> {body[:120]}")
    except Exception as e:
        print(f"💥 [ERR] {ep} -> {str(e)}")
