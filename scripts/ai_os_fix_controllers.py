#!/usr/bin/env python3
"""
AI-SE OS Controller Fixer
Uses OllamaAdapter to generate clean DispatchSalesController.java with proper org.yt.common.ApiResponse imports.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ai_se_os.execution.ollama_adapter import OllamaAdapter
from ai_se_os.validation.truth_governance import TruthGovernanceEngine

def fix_dispatch_controller():
    adapter = OllamaAdapter(model="qwen2.5:7b")
    prompt = (
        "Write Java code for DispatchSalesController.java under package org.yt.controller. "
        "Must import org.yt.common.ApiResponse; import org.springframework.http.ResponseEntity; "
        "import org.springframework.web.bind.annotation.*; "
        "Create GET /api/admin/sales/dispatch/orders returning ResponseEntity<ApiResponse<List<String>>> "
        "and POST /api/admin/sales/dispatch returning ResponseEntity<ApiResponse<String>>."
    )
    
    res = adapter.generate(prompt=prompt, system_prompt="You are AI-SE OS Java Engineer. Output valid Java code only.")
    code = res.get("response", "")
    
    if "```" in code:
        lines = code.split("\n")
        code = "\n".join([l for l in lines if not l.startswith("```")])
        
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    target_path = os.path.join(workspace_root, "admin", "src", "main", "java", "org", "yt", "controller", "DispatchSalesController.java")
    
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(code)
        
    print(f"AI-SE OS generated clean DispatchSalesController.java -> {target_path}")
    
    # Run Truth Governance Java Build Verification
    admin_repo = os.path.join(workspace_root, "admin")
    gov_res = TruthGovernanceEngine.verify_java_build(admin_repo)
    print(f"👉 Truth Governance Build Result: Passed={gov_res['build_passed']} (Exit Code={gov_res['exit_code']})")

if __name__ == "__main__":
    fix_dispatch_controller()
