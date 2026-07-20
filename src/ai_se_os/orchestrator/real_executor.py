"""
AI-SE OS Real Tool Executor
Provides the actual callable tools that the LLM reasoning loop can invoke.
Each tool returns a dict with: {success: bool, result: str, error: str|None}
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
    """Read a file from disk, return content (up to 8KB)."""
    try:
        if not os.path.isabs(path):
            path = os.path.join("/Users/suniltomar/Desktop/workspace", path)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read(8192)
        return {"success": True, "result": content}
    except Exception as e:
        return {"success": False, "error": str(e), "result": ""}


def write_file(path: str, content: str) -> Dict[str, Any]:
    """Write content to a file, creating parent directories if needed."""
    try:
        if not os.path.isabs(path):
            path = os.path.join("/Users/suniltomar/Desktop/workspace", path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"success": True, "result": f"Written {len(content)} chars to {path}"}
    except Exception as e:
        return {"success": False, "error": str(e), "result": ""}


def run_shell(cmd: str, cwd: Optional[str] = None) -> Dict[str, Any]:
    """Run a shell command, return stdout + stderr (capped at 4KB)."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=60, cwd=cwd or "/Users/suniltomar/Desktop/workspace"
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


def verify_json_field(url: str, field_path: str, expected: Any, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    HTTP GET url, parse JSON, walk field_path (e.g. 'data.samples[0].status'),
    compare to expected value.
    """
    get_result = http_get(url, headers)
    if not get_result["success"]:
        return {"success": False, "error": f"GET failed: {get_result.get('error')}", "result": ""}
    raw = get_result["result"]
    # Ensure response is JSON before attempting field walk
    if not raw.strip().startswith(("{", "[")):
        return {
            "success": False,
            "error": f"Response is not JSON (starts with: {raw.strip()[:60]!r})",
            "result": raw[:500]
        }
    try:
        data = json.loads(raw)
        node = data
        for part in field_path.lstrip(".").replace("]", "").replace("[", ".").split("."):
            if part == "":
                continue
            if isinstance(node, list):
                node = node[int(part)]
            else:
                node = node[part]
        passed = node == expected
        return {
            "success": passed,
            "result": f"Field '{field_path}' = {repr(node)}, expected {repr(expected)} -> {'PASS' if passed else 'FAIL'}"
        }
    except Exception as e:
        return {"success": False, "error": f"Field walk error: {e}", "result": raw[:1000]}


# Tool dispatch map — used by LLMTaskRunner
TOOL_REGISTRY = {
    "http_get": lambda args: http_get(args["url"], args.get("headers")),
    "http_post": lambda args: http_post(args["url"], args.get("payload", {}), args.get("headers")),
    "read_file": lambda args: read_file(args["path"]),
    "write_file": lambda args: write_file(args["path"], args["content"]),
    "run_shell": lambda args: run_shell(args["cmd"], args.get("cwd")),
    "verify_json_field": lambda args: verify_json_field(
        args["url"], args["field"], args["expected"], args.get("headers")
    ),
}


def dispatch_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch a tool call by name. Returns result dict."""
    fn = TOOL_REGISTRY.get(tool_name)
    if not fn:
        return {"success": False, "error": f"Unknown tool: '{tool_name}'. Available: {list(TOOL_REGISTRY)}", "result": ""}
    try:
        return fn(args)
    except Exception as e:
        return {"success": False, "error": f"Tool '{tool_name}' raised: {e}", "result": ""}
