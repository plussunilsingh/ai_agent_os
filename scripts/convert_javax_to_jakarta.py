#!/usr/bin/env python3
"""
Spring Boot 3 Migration Helper
Converts legacy 'javax.persistence' -> 'jakarta.persistence' and 'javax.servlet' -> 'jakarta.servlet' across target admin source files.
"""

import os

def fix_imports(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    modified = content.replace("javax.persistence", "jakarta.persistence")
    modified = modified.replace("javax.servlet", "jakarta.servlet")
    
    # Remove duplicate package com.example... or inner class ApiResponse if present
    if "class ApiResponse<T> {" in modified:
        idx = modified.find("class ApiResponse<T> {")
        modified = modified[:idx]

    if modified != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(modified)

def process_dir(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith(".java"):
                fix_imports(os.path.join(dirpath, fname))

if __name__ == "__main__":
    admin_src = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "admin", "src"))
    process_dir(admin_src)
    print("Converted javax -> jakarta across admin Java sources.")
