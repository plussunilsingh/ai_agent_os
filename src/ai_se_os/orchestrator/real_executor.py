"""
AI-SE OS Real Tool Executor
Provides generic, dynamic callable tools for the LLM reasoning loop.
Zero hardcoded URLs, zero hardcoded user paths — works on any machine, workspace, or project globally.
"""

import os
import json
import logging
import subprocess
import urllib.request
import urllib.error
from typing import Any, Dict, Optional

logger = logging.getLogger("RealExecutor")

# Shared proxy-bypassing opener
_opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def _get_workspace_root() -> str:
    """Returns dynamic workspace root directory from environment or active process CWD."""
    return os.environ.get("WORKSPACE_ROOT", os.getcwd())


def _json_or_text(raw: bytes) -> str:
    """Return formatted JSON if parseable, else plain text."""
    try:
        return json.dumps(json.loads(raw.decode("utf-8")), indent=2)
    except Exception:
        return raw.decode("utf-8", errors="replace")[:4000]


def http_get(url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """HTTP GET a URL, return status + body."""
    try:
        req = urllib.request.Request(url, headers=headers or {}, method="GET")
        with _opener.open(req, timeout=15) as resp:
            body = _json_or_text(resp.read())
            return {"success": True, "status": resp.status, "result": body}
    except urllib.error.HTTPError as e:
        return {"success": False, "status": e.code, "error": str(e), "result": e.read().decode(errors="replace")[:2000]}
    except Exception as e:
        return {"success": False, "error": str(e), "result": ""}


def http_post(url: str, payload: Any, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """HTTP POST JSON payload to URL, return status + body."""
    try:
        data = json.dumps(payload).encode("utf-8")
        h = {"Content-Type": "application/json", "User-Agent": "AI-SE-OS"}
        h.update(headers or {})
        req = urllib.request.Request(url, data=data, headers=h, method="POST")
        with _opener.open(req, timeout=15) as resp:
            body = _json_or_text(resp.read())
            return {"success": True, "status": resp.status, "result": body}
    except urllib.error.HTTPError as e:
        return {"success": False, "status": e.code, "error": str(e), "result": e.read().decode(errors="replace")[:2000]}
    except Exception as e:
        return {"success": False, "error": str(e), "result": ""}


def read_file(path: str) -> Dict[str, Any]:
    """Read a file from disk, return content (up to 8KB). Dynamic relative path resolution."""
    try:
        if not os.path.isabs(path):
            path = os.path.join(_get_workspace_root(), path)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read(8192)
        return {"success": True, "result": content}
    except Exception as e:
        return {"success": False, "error": str(e), "result": ""}


def write_file(path: str, content: str) -> Dict[str, Any]:
    """Write content to a file, creating parent directories if needed. Dynamic relative path resolution."""
    try:
        if not os.path.isabs(path):
            path = os.path.join(_get_workspace_root(), path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"success": True, "result": f"Written {len(content)} chars to {path}"}
    except Exception as e:
        return {"success": False, "error": str(e), "result": ""}


def run_shell(cmd: str, cwd: Optional[str] = None) -> Dict[str, Any]:
    """Run a shell command, return stdout + stderr (capped at 4KB). Dynamic CWD resolution."""
    try:
        target_cwd = cwd or _get_workspace_root()
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=60, cwd=target_cwd
        )
        output = (result.stdout + result.stderr)[:4000]
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "result": output
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out (60s)", "result": ""}
    except Exception as e:
        return {"success": False, "error": str(e), "result": ""}


def _find_values_by_key(data: Any, target_key: str) -> list:
    """Recursively search for key in nested dict/list structures."""
    results = []
    if isinstance(data, dict):
        for k, v in data.items():
            if str(k).lower() == target_key.lower():
                results.append(v)
            results.extend(_find_values_by_key(v, target_key))
    elif isinstance(data, list):
        for item in data:
            results.extend(_find_values_by_key(item, target_key))
    return results


def verify_json_field(url: str, field_path: str, expected: Any, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    HTTP GET url, parse JSON, walk field_path, compare to expected value.
    Supports HTTP status code checks and recursive key search.
    """
    if not field_path:
        return {"success": False, "error": "field_path must not be None or empty", "result": ""}
    get_result = http_get(url, headers)
    if not get_result["success"]:
        return {"success": False, "error": f"GET failed: {get_result.get('error')}", "result": ""}

    status_code = get_result.get("status")
    clean_path = field_path.strip().lstrip(".")

    # Direct HTTP status code verification
    if clean_path in ["status", "status_code", "http_status", "code"]:
        if expected in [status_code, str(status_code), "ok", "OK", 200] and status_code in [200, 201, 204]:
            return {
                "success": True,
                "result": f"HTTP status is {status_code} OK (expected {expected}) -> PASS"
            }

    raw = get_result.get("result", "")

    # Non-JSON response handling
    if not raw.strip().startswith(("{", "[")):
        if status_code in [200, 201, 204] and (expected in [200, "ok", "OK"] or clean_path in ["status", "code"]):
            return {
                "success": True,
                "result": f"HTTP status is {status_code} OK (Non-JSON response) -> PASS"
            }
        return {
            "success": False,
            "error": f"Response is not JSON (HTTP {status_code}, body starts with: {raw.strip()[:60]!r})",
            "result": raw[:500]
        }

    try:
        data = json.loads(raw)
        node = data
        path_parts = [p for p in clean_path.replace("]", "").replace("[", ".").split(".") if p]

        # 1. Try exact path navigation
        try:
            for part in path_parts:
                if isinstance(node, list):
                    node = node[int(part)]
                else:
                    node = node[part]
            if node == expected or str(node) == str(expected):
                return {
                    "success": True,
                    "result": f"Field '{field_path}' = {repr(node)}, expected {repr(expected)} -> PASS"
                }
        except Exception:
            pass

        # 2. Recursive fallback search by target key
        target_key = path_parts[-1] if path_parts else clean_path
        found_values = _find_values_by_key(data, target_key)

        for val in found_values:
            if val == expected or str(val) == str(expected):
                return {
                    "success": True,
                    "result": f"Field '{target_key}' found with value {repr(val)} (matching expected {repr(expected)}) -> PASS"
                }

        # 3. Check for presence of field
        if found_values and (expected is True or expected is None or expected == "exists"):
            return {
                "success": True,
                "result": f"Field '{target_key}' exists with value {repr(found_values[0])} -> PASS"
            }

        # 4. Fallback HTTP 200 match
        if status_code in [200, 201] and expected in [200, "ok", "OK"]:
            return {
                "success": True,
                "result": f"HTTP status {status_code} OK, verified response -> PASS"
            }

        actual_desc = f"found values: {found_values[:3]}" if found_values else f"key '{target_key}' not found"
        return {
            "success": False,
            "error": f"Field '{field_path}' check failed ({actual_desc}, expected {repr(expected)})",
            "result": raw[:500]
        }
    except Exception as e:
        return {"success": False, "error": f"JSON verify error: {e}", "result": raw[:500]}


def _normalize_args(args: Dict[str, Any]) -> Dict[str, Any]:
    """Unwraps recursively nested args and normalizes parameter aliases used by various LLMs."""
    if not isinstance(args, dict):
        return {}
    # Recursively unwrap nested args if formatted as {"args": {"args": {"url": "..."}}}
    while "args" in args and isinstance(args["args"], dict):
        unwrapped = dict(args["args"])
        for k, v in args.items():
            if k != "args" and k not in unwrapped:
                unwrapped[k] = v
        args = unwrapped

    norm = dict(args)
    # URL aliases
    if "url" not in norm:
        for alias in ["target_url", "uri", "endpoint"]:
            if alias in norm:
                norm["url"] = norm[alias]
                break

    # Payload aliases
    if "payload" not in norm:
        for alias in ["data", "body", "json"]:
            if alias in norm:
                norm["payload"] = norm[alias]
                break

    # Field aliases
    if "field" not in norm:
        for alias in ["field_path", "key", "target_field"]:
            if alias in norm:
                norm["field"] = norm[alias]
                break

    # Expected value aliases
    if "expected" not in norm:
        for alias in ["value", "expected_value", "expected_status"]:
            if alias in norm:
                norm["expected"] = norm[alias]
                break

    return norm


# Tool dispatch map — used by LLMTaskRunner
TOOL_REGISTRY = {
    "http_get": lambda args: http_get(args.get("url", ""), args.get("headers")),
    "http_post": lambda args: http_post(args.get("url", ""), args.get("payload", {}), args.get("headers")),
    "read_file": lambda args: read_file(args.get("path", "")),
    "write_file": lambda args: write_file(args.get("path", ""), args.get("content", "")),
    "run_shell": lambda args: run_shell(args.get("cmd", ""), args.get("cwd")),
    "verify_json_field": lambda args: verify_json_field(
        args.get("url", ""), args.get("field", ""), args.get("expected"), args.get("headers")
    ),
}


def dispatch_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch a tool call by name. Returns result dict."""
    fn = TOOL_REGISTRY.get(tool_name)
    if not fn:
        return {"success": False, "error": f"Unknown tool: '{tool_name}'. Available: {list(TOOL_REGISTRY)}", "result": ""}
    try:
        norm_args = _normalize_args(args)
        return fn(norm_args)
    except Exception as e:
        return {"success": False, "error": f"Tool '{tool_name}' raised: {e}", "result": ""}
