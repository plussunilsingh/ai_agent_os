#!/bin/bash
# AI-SE OS - Complete Validation & Structure Script
# This script validates all files and shows end-to-end structure

echo "============================================================"
echo "     AI-SE OS - COMPLETE FILE STRUCTURE VALIDATION"
echo "============================================================"
echo ""

# Set the project root
PROJECT_ROOT="/Users/suniltomar/Desktop/workspace/AI_AGENT_OS/ai-se-os"

# Navigate to project
cd "$PROJECT_ROOT" || { echo "❌ Project not found!"; exit 1; }

echo "📁 Project Root: $PROJECT_ROOT"
echo ""

# ============================================================
# SECTION 1: RUN THE RESTRUCTURE (FIX ANY ISSUES)
# ============================================================

echo "🔧 Running restructure fixes..."

# Create directories
mkdir -p .ai_os_runtime/{config,policies,prompts,schemas,templates}
mkdir -p .githooks
mkdir -p scripts
mkdir -p sdk/java/src/main/java/com/ai_se_os
mkdir -p sdk/node/src

# Move root markdown files to docs/
mv ROADMAP.md docs/roadmap.md 2>/dev/null
mv RUNBOOK.md docs/runbook.md 2>/dev/null
mv IMPLEMENTATION_ORDER.md docs/implementation_order.md 2>/dev/null

# Move unknown directories
mv config/* .ai_os_runtime/config/ 2>/dev/null && rm -rf config 2>/dev/null
mv policies/* .ai_os_runtime/policies/ 2>/dev/null && rm -rf policies 2>/dev/null
mv prompts/* .ai_os_runtime/prompts/ 2>/dev/null && rm -rf prompts 2>/dev/null
mv schemas/* .ai_os_runtime/schemas/ 2>/dev/null && rm -rf schemas 2>/dev/null
mv templates/* .ai_os_runtime/templates/ 2>/dev/null && rm -rf templates 2>/dev/null
mv hooks .githooks 2>/dev/null

# Move restructure.py to scripts/
mv restructure.py scripts/restructure.py 2>/dev/null

# Clean Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
rm -rf .pytest_cache 2>/dev/null

# Create README files for SDKs
echo '# Java SDK - Coming Soon' > sdk/java/README.md 2>/dev/null
echo '# Node SDK - Coming Soon' > sdk/node/README.md 2>/dev/null
touch sdk/java/src/main/java/com/ai_se_os/.keep 2>/dev/null
touch sdk/node/src/.keep 2>/dev/null

echo "✅ Restructure complete!"
echo ""

# ============================================================
# SECTION 2: VALIDATE REQUIRED FILES
# ============================================================

echo "============================================================"
echo "📋 REQUIRED ROOT FILES VALIDATION"
echo "============================================================"

ROOT_FILES=(
    "README.md"
    "CONTRIBUTING.md"
    "LICENSE"
    "CHANGELOG.md"
    "pyproject.toml"
    "setup.py"
    "requirements.txt"
    "requirements-dev.txt"
    ".env.example"
    ".gitignore"
    ".pre-commit-config.yaml"
    ".python-version"
)

ROOT_MISSING=0
for file in "${ROOT_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - MISSING"
        ROOT_MISSING=$((ROOT_MISSING + 1))
    fi
done

if [ $ROOT_MISSING -eq 0 ]; then
    echo ""
    echo "✅ All required root files present!"
else
    echo ""
    echo "⚠️ $ROOT_MISSING required root files missing!"
fi
echo ""

# ============================================================
# SECTION 3: VALIDATE SOURCE CODE STRUCTURE
# ============================================================

echo "============================================================"
echo "📦 SOURCE CODE VALIDATION"
echo "============================================================"

if [ -d "src/ai_se_os" ]; then
    echo "✅ src/ai_se_os/ exists"

    # Check for nested directory
    if [ -d "src/ai_se_os/ai_se_os" ]; then
        echo "  ❌ Nested ai_se_os/ found! Moving contents..."
        mv src/ai_se_os/ai_se_os/* src/ai_se_os/ 2>/dev/null
        rmdir src/ai_se_os/ai_se_os 2>/dev/null
    else
        echo "  ✅ No nested ai_se_os/ found"
    fi

    # Count Python files
    SRC_FILES=$(find src/ai_se_os -type f -name "*.py" | wc -l | tr -d ' ')
    echo "  📄 Python files: $SRC_FILES"

    # List subdirectories
    echo "  📁 Subdirectories:"
    find src/ai_se_os -maxdepth 1 -type d | grep -v "^src/ai_se_os$" | sed 's/^/    /' | sort
else
    echo "❌ src/ai_se_os/ NOT FOUND!"
fi
echo ""

# ============================================================
# SECTION 4: VALIDATE TEST STRUCTURE
# ============================================================

echo "============================================================"
# ============================================================
# 🧪 TEST STRUCTURE VALIDATION
# ============================================================

if [ -d "tests" ]; then
    echo "✅ tests/ exists"

    # Check required test subdirectories
    TEST_DIRS=("unit" "integration" "performance" "chaos" "benchmarks")
    for dir in "${TEST_DIRS[@]}"; do
        if [ -d "tests/$dir" ]; then
            FILES=$(find tests/$dir -type f -name "*.py" 2>/dev/null | wc -l | tr -d ' ')
            echo "  ✅ tests/$dir/ - $FILES test files"
        else
            echo "  ❌ tests/$dir/ - MISSING"
        fi
    done

    TOTAL_TESTS=$(find tests -type f -name "*.py" 2>/dev/null | wc -l | tr -d ' ')
    echo ""
    echo "  📊 Total test files: $TOTAL_TESTS"
else
    echo "❌ tests/ NOT FOUND!"
fi
echo ""

# ============================================================
# SECTION 5: VALIDATE SDK STRUCTURE
# ============================================================

echo "============================================================"
echo "🔌 SDK VALIDATION"
echo "============================================================"

if [ -d "sdk" ]; then
    echo "✅ sdk/ exists"

    # Python SDK
    if [ -d "sdk/python" ]; then
        PY_FILES=$(find sdk/python -type f -name "*.py" 2>/dev/null | wc -l | tr -d ' ')
        echo "  ✅ sdk/python/ - $PY_FILES Python files"
    else
        echo "  ❌ sdk/python/ - MISSING"
    fi

    # Java SDK
    if [ -d "sdk/java" ]; then
        if [ -f "sdk/java/README.md" ]; then
            echo "  ✅ sdk/java/ - README.md present"
        else
            echo "  ⚠️ sdk/java/ - README.md missing"
        fi
    else
        echo "  ❌ sdk/java/ - MISSING"
    fi

    # Node SDK
    if [ -d "sdk/node" ]; then
        if [ -f "sdk/node/README.md" ]; then
            echo "  ✅ sdk/node/ - README.md present"
        else
            echo "  ⚠️ sdk/node/ - README.md missing"
        fi
    else
        echo "  ❌ sdk/node/ - MISSING"
    fi
else
    echo "❌ sdk/ NOT FOUND!"
fi
echo ""

# ============================================================
# SECTION 6: VALIDATE DOCUMENTATION STRUCTURE
# ============================================================

echo "============================================================"
echo "📚 DOCUMENTATION VALIDATION"
echo "============================================================"

if [ -d "docs" ]; then
    echo "✅ docs/ exists"
    DOC_FILES=$(find docs -type f -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    echo "  📄 Markdown files: $DOC_FILES"
    echo ""
    echo "  📁 Documentation files:"
    find docs -type f -name "*.md" | sed 's/^/    /' | sort
else
    echo "❌ docs/ NOT FOUND!"
fi
echo ""

# ============================================================
# SECTION 7: VALIDATE .AI_OS_RUNTIME STRUCTURE
# ============================================================

echo "============================================================"
echo "⚙️ RUNTIME VALIDATION"
echo "============================================================"

if [ -d ".ai_os_runtime" ]; then
    echo "✅ .ai_os_runtime/ exists"

    RUNTIME_DIRS=("config" "policies" "prompts" "schemas" "templates")
    for dir in "${RUNTIME_DIRS[@]}"; do
        if [ -d ".ai_os_runtime/$dir" ]; then
            FILES=$(find .ai_os_runtime/$dir -type f 2>/dev/null | wc -l | tr -d ' ')
            echo "  ✅ .ai_os_runtime/$dir/ - $FILES files"
        else
            echo "  ❌ .ai_os_runtime/$dir/ - MISSING"
        fi
    done
else
    echo "⚠️ .ai_os_runtime/ NOT FOUND"
fi
echo ""

# ============================================================
# SECTION 8: ROOT CLEANLINESS CHECK
# ============================================================

echo "============================================================"
echo "🧹 ROOT CLEANLINESS CHECK"
echo "============================================================"

echo "📁 Files at root:"
echo ""

ls -la | grep -v "^d" | grep -v "total" | awk '{print "  " $9}' | sort

echo ""
echo "📁 Directories at root:"
echo ""

ls -la | grep "^d" | awk '{print "  " $9}' | sort

# Check for files that shouldn't be at root
echo ""
echo "🔍 Checking for unusual files at root..."
UNUSUAL_FILES=0
for file in *.py 2>/dev/null; do
    if [ -f "$file" ] && [ "$file" != "setup.py" ]; then
        echo "  ⚠️ $file - Should probably be in scripts/ or src/"
        UNUSUAL_FILES=$((UNUSUAL_FILES + 1))
    fi
done

if [ $UNUSUAL_FILES -eq 0 ]; then
    echo "  ✅ No unusual Python files at root"
fi
echo ""

# ============================================================
# SECTION 9: COMPLETE FILE TREE
# ============================================================

echo "============================================================"
echo "🌳 COMPLETE FILE TREE"
echo "============================================================"
echo ""

# Use tree if available, else use find
if command -v tree &> /dev/null; then
    tree -L 4 -a --dirsfirst --ignore='.git' 2>/dev/null | head -100
else
    echo "📁 Directory Structure (using find):"
    echo ""
    find . -type d -maxdepth 4 | grep -v ".git" | grep -v "__pycache__" | sort | sed 's/^\./ai-se-os/' | while read dir; do
        depth=$(echo "$dir" | tr -cd '/' | wc -c)
        indent=""
        for i in $(seq 1 $depth); do
            indent="  $indent"
        done
        echo "$indent📁 $(basename "$dir")/"
    done
fi

echo ""
echo "📄 File count by type:"
echo ""
find . -type f ! -path "./.git/*" | sed 's/.*\.//' | sort | uniq -c | sort -rn | while read count ext; do
    echo "  $count .$ext files"
done

# ============================================================
# SECTION 10: SUMMARY
# ============================================================

echo ""
echo "============================================================"
echo "📊 VALIDATION SUMMARY"
echo "============================================================"

# Count all files
TOTAL_FILES=$(find . -type f ! -path "./.git/*" 2>/dev/null | wc -l | tr -d ' ')
PY_FILES=$(find . -type f -name "*.py" ! -path "./.git/*" 2>/dev/null | wc -l | tr -d ' ')
MD_FILES=$(find . -type f -name "*.md" ! -path "./.git/*" 2>/dev/null | wc -l | tr -d ' ')
YAML_FILES=$(find . -type f \( -name "*.yml" -o -name "*.yaml" \) ! -path "./.git/*" 2>/dev/null | wc -l | tr -d ' ')

echo "  📁 Project Root: $PROJECT_ROOT"
echo "  📄 Total Files: $TOTAL_FILES"
echo "  🐍 Python Files: $PY_FILES"
echo "  📝 Markdown Files: $MD_FILES"
echo "  ⚙️ YAML Files: $YAML_FILES"
echo ""
echo "  ✅ Root files: $([ $ROOT_MISSING -eq 0 ] && echo "All present" || echo "$ROOT_MISSING missing")"
echo "  🧪 Test files: $TOTAL_TESTS"
echo "  📚 Doc files: $DOC_FILES"
echo ""

# Check if any critical issues remain
CRITICAL_ISSUES=0

if [ ! -f "README.md" ]; then
    echo "  ❌ README.md is missing!"
    CRITICAL_ISSUES=$((CRITICAL_ISSUES + 1))
fi

if [ ! -d "src/ai_se_os" ]; then
    echo "  ❌ src/ai_se_os/ is missing!"
    CRITICAL_ISSUES=$((CRITICAL_ISSUES + 1))
fi

if [ ! -d "tests/unit" ]; then
    echo "  ❌ tests/unit/ is missing!"
    CRITICAL_ISSUES=$((CRITICAL_ISSUES + 1))
fi

if [ $CRITICAL_ISSUES -eq 0 ]; then
    echo ""
    echo "✅ No critical issues found! Project structure is correct."
else
    echo ""
    echo "⚠️ $CRITICAL_ISSUES critical issues found!"
fi

echo ""
echo "============================================================"
echo "✅ VALIDATION COMPLETE"
echo "============================================================"
echo ""
echo "🚀 Next steps:"
echo "  1. Run: ./scripts/setup.sh"
echo "  2. Run: pytest -v"
echo "  3. Run: docker-compose up -d"
echo ""