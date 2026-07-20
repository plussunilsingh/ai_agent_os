"""
AI-SE OS Dynamic Target Discovery Engine
Generic inspection of any target application: OpenAPI/Swagger API discovery, HTML form field extraction, and dynamic route resolution.
Zero hardcoded URLs or payloads.
"""

import json
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse

logger = logging.getLogger("TargetDiscovery")

_opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


class TargetDiscoveryEngine:
    """
    Generic discovery engine that inspects target URLs at runtime to discover:
    - OpenAPI/Swagger endpoints & JSON schemas
    - HTML forms, inputs, and interactive elements
    - API base paths and route structures
    """

    @classmethod
    def discover_target(cls, target_url: str) -> Dict[str, Any]:
        """Discovers API schemas, HTML forms, and available routes for any given target URL."""
        if not target_url:
            return {"discovered": False, "reason": "No target URL provided"}

        parsed = urlparse(target_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        openapi_schema = cls._try_discover_openapi(base_url)
        html_forms = cls._try_discover_html_forms(target_url)

        return {
            "discovered": True,
            "target_url": target_url,
            "base_url": base_url,
            "openapi_endpoints": openapi_schema.get("endpoints", []),
            "html_forms": html_forms,
            "summary": openapi_schema.get("summary", "Generic target app")
        }

    @classmethod
    def _try_discover_openapi(cls, base_url: str) -> Dict[str, Any]:
        """Probes common OpenAPI/Swagger endpoint paths autonomously."""
        candidates = [
            "/openapi.json",
            "/v3/api-docs",
            "/api-docs",
            "/swagger.json",
            "/api/v1/openapi.json"
        ]

        endpoints = []
        for path in candidates:
            url = f"{base_url}{path}"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "AI-SE-OS-Discovery"}, method="GET")
                with _opener.open(req, timeout=3) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode("utf-8"))
                        paths = data.get("paths", {})
                        for route, methods in paths.items():
                            for method, details in methods.items():
                                endpoints.append({
                                    "method": method.upper(),
                                    "path": route,
                                    "full_url": f"{base_url}{route}",
                                    "summary": details.get("summary", details.get("operationId", ""))
                                })
                        return {
                            "found": True,
                            "spec_url": url,
                            "endpoints": endpoints[:30],
                            "summary": f"Discovered OpenAPI spec with {len(endpoints)} endpoints"
                        }
            except Exception:
                continue

        return {"found": False, "endpoints": []}

    @classmethod
    def _try_discover_html_forms(cls, target_url: str) -> List[Dict[str, Any]]:
        """Inspects HTML content of target URL for form fields and input elements."""
        try:
            req = urllib.request.Request(target_url, headers={"User-Agent": "AI-SE-OS-Discovery"}, method="GET")
            with _opener.open(req, timeout=5) as resp:
                if resp.status == 200:
                    html = resp.read().decode("utf-8", errors="ignore")
                    # Simple regex extraction of input names and form actions
                    import re
                    inputs = re.findall(r'<input[^>]+name=["\']([^"\']+)["\']', html, re.IGNORECASE)
                    forms = re.findall(r'<form[^>]+action=["\']([^"\']+)["\']', html, re.IGNORECASE)
                    return [{
                        "form_actions": forms,
                        "input_fields": list(set(inputs))
                    }]
        except Exception:
            pass
        return []
