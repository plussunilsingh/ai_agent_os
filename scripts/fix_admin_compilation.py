#!/usr/bin/env python3
"""
Target Admin Repository Java Compilation Repair Script
Cleans up header/footer prose and illegal characters from generated Java files.
"""

import os
import re

def fix_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Replace String备注 with String notes
    content = content.replace("String备注", "String notes")

    # If file contains prose before 'package ', strip leading prose
    if "package " in content:
        content = content[content.find("package "):]

    # If file contains multiple package statements (concatenated files), keep only the first valid one up to its class brace match
    package_statements = [m.start() for m in re.finditer(r"^package\s+", content, re.MULTILINE)]
    if len(package_statements) > 1:
        content = content[:package_statements[1]]

    # Truncate after last '}'
    last_brace = content.rfind("}")
    if last_brace != -1:
        content = content[:last_brace + 1]

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def fix_directory(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith(".java"):
                fpath = os.path.join(dirpath, fname)
                fix_file(fpath)

if __name__ == "__main__":
    admin_src = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "admin", "src"))
    fix_directory(admin_src)
    print(f"Repaired compilation files in {admin_src}")
