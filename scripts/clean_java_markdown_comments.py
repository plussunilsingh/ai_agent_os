#!/usr/bin/env python3
"""
Robust Java Source Code Sanitizer
Truncates any trailing markdown prose/commentary outside the last closing brace '}' of the main Java class.
Also cleans duplicate 'src/main/java/yt' directory structure if present.
"""

import os
import shutil

def sanitize_java_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        
    last_brace_idx = -1
    for idx, line in enumerate(lines):
        if line.strip() == "}":
            last_brace_idx = idx
            
    if last_brace_idx != -1:
        cleaned_lines = lines[:last_brace_idx + 1]
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(cleaned_lines)

def sanitize_directory(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith(".java"):
                fpath = os.path.join(dirpath, fname)
                sanitize_java_file(fpath)

def remove_duplicate_yt_dir(admin_src):
    bad_dir = os.path.join(admin_src, "main", "java", "yt")
    if os.path.exists(bad_dir):
        shutil.rmtree(bad_dir)
        print(f"Removed duplicate dir {bad_dir}")

if __name__ == "__main__":
    admin_src = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "admin", "src"))
    remove_duplicate_yt_dir(admin_src)
    sanitize_directory(admin_src)
    print(f"Sanitized all Java source files in {admin_src}")
