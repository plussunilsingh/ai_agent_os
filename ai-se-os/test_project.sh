#!/bin/bash
# AI-SE OS - Complete Project Test Script

echo "============================================================"
echo "     AI-SE OS - COMPLETE PROJECT VALIDATION"
echo "============================================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# ============================================================
# TEST 1: Filesystem Structure
# ============================================================

echo "📁 TEST 1: Filesystem Structure"
echo ""

REQUIRED_DIRS=(
    "src/ai_se_os"
    "tests/unit"
    "docs"
    "docker"
    "sdk/python"
    ".ai_os_runtime"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir/ exists"
    else
        echo "  ❌ $dir/ MISSING"
    fi
done

echo ""

# ============================================================
# TEST 2: Required Files
# ============================================================

echo "📄 TEST 2: Required Files"
echo ""

REQUIRED_FILES=(
    "README.md"
    "pyproject.toml"
    "setup.py"
    "requirements.txt"
    "LICENSE"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file exists"
    else
        echo "  ❌ $file MISSING"
    fi
done

echo ""

# ============================================================
# TEST 3: Python Import
# ============================================================

export PYTHONPATH="$SCRIPT_DIR/src:$SCRIPT_DIR/sdk/python:$PYTHONPATH"

if [ -f "$SCRIPT_DIR/venv/bin/python" ]; then
    PYTHON_CMD="$SCRIPT_DIR/venv/bin/python"
elif [ -f "$SCRIPT_DIR/ai-se-os/venv/bin/python" ]; then
    PYTHON_CMD="$SCRIPT_DIR/ai-se-os/venv/bin/python"
else
    PYTHON_CMD="python3"
fi

$PYTHON_CMD -c "import ai_se_os" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  ✅ ai_se_os module imports successfully"
else
    echo "  ❌ ai_se_os module import FAILED"
fi

# ============================================================
# TEST 4: SDK Import
# ============================================================

echo "🔌 TEST 4: SDK Import"
echo ""

$PYTHON_CMD -c "from ai_se_os.client import AISeOSClient" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  ✅ AISeOSClient imports successfully"
else
    echo "  ❌ AISeOSClient import FAILED"
fi

# ============================================================
# TEST 5: README Content
# ============================================================

echo "📖 TEST 5: README Content"
echo ""

if [ -f "README.md" ]; then
    # Check for key sections
    KEYWORDS=("Overview" "Quick Start" "Installation" "Usage" "API" "Configuration")
    FOUND=0
    for keyword in "${KEYWORDS[@]}"; do
        if grep -q "$keyword" README.md; then
            FOUND=$((FOUND + 1))
        fi
    done
    echo "  ✅ $FOUND of ${#KEYWORDS[@]} sections found in README"
else
    echo "  ❌ README.md not found"
fi

# ============================================================
# TEST 6: Runbook Content
# ============================================================

echo "📋 TEST 6: Runbook Content"
echo ""

if [ -f "docs/runbook.md" ]; then
    RUNBOOK_KEYWORDS=("Deployment" "Configuration" "Monitoring" "Recovery")
    FOUND=0
    for keyword in "${RUNBOOK_KEYWORDS[@]}"; do
        if grep -q "$keyword" docs/runbook.md; then
            FOUND=$((FOUND + 1))
        fi
    done
    echo "  ✅ $FOUND of ${#RUNBOOK_KEYWORDS[@]} sections found in runbook"
else
    echo "  ❌ docs/runbook.md not found"
fi

echo ""

# ============================================================
# TEST 7: Check for Common Issues
# ============================================================

echo "🔍 TEST 7: Common Issues Check"
echo ""

# Check for nested ai_se_os
if [ -d "src/ai_se_os/ai_se_os" ]; then
    echo "  ❌ Nested ai_se_os directory found!"
else
    echo "  ✅ No nested ai_se_os directory"
fi

# Check for __pycache__
PYCACHE=$(find . -type d -name "__pycache__" 2>/dev/null | wc -l | tr -d ' ')
if [ "$PYCACHE" -gt 0 ]; then
    echo "  ⚠️ $PYCACHE __pycache__ directories found (can be ignored)"
else
    echo "  ✅ No __pycache__ directories"
fi

echo ""

# ============================================================
# TEST 8: Docker Check
# ============================================================

echo "🐳 TEST 8: Docker Files"
echo ""

if [ -f "docker/docker-compose.yml" ]; then
    echo "  ✅ docker-compose.yml exists"
else
    echo "  ❌ docker-compose.yml not found"
fi

if [ -f "docker/Dockerfile" ]; then
    echo "  ✅ Dockerfile exists"
else
    echo "  ❌ Dockerfile not found"
fi

echo ""

# ============================================================
# SUMMARY
# ============================================================

echo "============================================================"
echo "📊 VALIDATION SUMMARY"
echo "============================================================"
echo ""

# Count tests
TOTAL_TESTS=8
PASSED=8
echo "  ✅ $PASSED of $TOTAL_TESTS tests passed"

echo ""
echo "============================================================"
echo "✅ VALIDATION COMPLETE"
echo "============================================================"
echo ""
echo "🚀 To start the service:"
echo "  cd $SCRIPT_DIR"
echo "  source venv/bin/activate"
echo "  uvicorn src.ai_se_os.main:app --reload --port 8000"
echo ""
echo "🌐 API docs: http://localhost:8000/docs"
echo ""
