#!/usr/bin/env python3
"""
AI-SE OS Project Restructure Script
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path("/Users/suniltomar/Desktop/workspace/AI_AGENT_OS")
OLD_AI_OS = BASE_DIR / "ai-se-os"
NEW_ROOT = BASE_DIR / "ai-se-os"

print("Starting restructure...")
print(f"Old: {OLD_AI_OS}")
print(f"New: {NEW_ROOT}")

# Create directories
dirs = [
    "src/ai_se_os/core",
    "src/ai_se_os/kernel",
    "src/ai_se_os/intelligence",
    "src/ai_se_os/execution",
    "src/ai_se_os/cache",
    "src/ai_se_os/observability",
    "src/ai_se_os/plugins",
    "src/ai_se_os/change_detection",
    "src/ai_se_os/api",
    "sdk/python",
    "sdk/java",
    "sdk/node",
    "tests/unit",
    "tests/integration",
    "tests/performance",
    "tests/chaos",
    "tests/benchmarks",
]

for d in dirs:
    (NEW_ROOT / d).mkdir(parents=True, exist_ok=True)
    print(f"Created: {d}")

# Fix imports in test files
print("\nFixing imports...")
test_files = list((OLD_AI_OS / "tests").glob("test_*.py"))
for test_file in test_files:
    content = test_file.read_text()
    content = content.replace("from src.core.", "from ai_se_os.core.")
    content = content.replace("from src.cache.", "from ai_se_os.cache.")
    content = content.replace("from src.intelligence.", "from ai_se_os.intelligence.")
    content = content.replace("from src.execution.", "from ai_se_os.execution.")
    dest = NEW_ROOT / "tests" / "unit" / test_file.name
    dest.write_text(content)
    print(f"Fixed: {test_file.name}")

# Copy source files
print("\nCopying source files...")
for src_dir in (OLD_AI_OS / "src").iterdir():
    if src_dir.is_dir():
        dest = NEW_ROOT / "src" / "ai_se_os" / src_dir.name
        shutil.copytree(src_dir, dest, dirs_exist_ok=True)
        print(f"Copied: {src_dir.name}/")

print("\n✅ Restructure complete!")
print(f"Location: {NEW_ROOT}")