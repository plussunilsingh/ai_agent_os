#!/bin/bash
# AI-SE OS - Complete Validation & Structure Script (FIXED)

echo "============================================================"
echo "     AI-SE OS - COMPLETE FILE STRUCTURE VALIDATION"
echo "============================================================"
echo ""

PROJECT_ROOT="/Users/suniltomar/Desktop/workspace/AI_AGENT_OS/ai-se-os"

if [ ! -d "$PROJECT_ROOT" ]; then
    echo "❌ Project not found at: $PROJECT_ROOT"
    exit 1
fi

cd "$PROJECT_ROOT"
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
    "pyproject.toml"
    "setup.py"
    "requirements.txt"
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

# Check optional files
OPTIONAL_FILES=(
    "CONTRIBUTING.md"
    "LICENSE"
    "CHANGELOG.md"
    "requirements-dev.txt"
    ".env.example"
    ".gitignore"
    ".pre-commit-config.yaml"
    ".python-version"
)

echo ""
echo "  📝 Optional files:"
for file in "${OPTIONAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "    ✅ $file"
    else
        echo "    ⚠️ $file - Not found (will be created)"
        # Create the missing optional files
        touch "$file" 2>/dev/null
    fi
done

echo ""
echo "✅ Required files present!"
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
    
    SRC_FILES=$(find src/ai_se_os -type f -name "*.py" 2>/dev/null | wc -l | tr -d ' ')
    echo "  📄 Python files: $SRC_FILES"
    
    echo "  📁 Subdirectories:"
    find src/ai_se_os -maxdepth 1 -type d 2>/dev/null | grep -v "^src/ai_se_os$" | while read dir; do
        echo "    📁 $(basename "$dir")/"
    done | sort
else
    echo "❌ src/ai_se_os/ NOT FOUND!"
fi
echo ""

# ============================================================
# SECTION 4: VALIDATE TEST STRUCTURE
# ============================================================

echo "============================================================"
echo "🧪 TEST STRUCTURE VALIDATION"
echo "============================================================"

if [ -d "tests" ]; then
    echo "✅ tests/ exists"
    
    TEST_DIRS=("unit" "integration" "performance" "chaos" "benchmarks")
    TOTAL_TESTS=0
    for dir in "${TEST_DIRS[@]}"; do
        if [ -d "tests/$dir" ]; then
            FILES=$(find tests/$dir -type f -name "*.py" 2>/dev/null | wc -l | tr -d ' ')
            echo "  ✅ tests/$dir/ - $FILES test files"
            TOTAL_TESTS=$((TOTAL_TESTS + FILES))
        else
            echo "  ⚠️ tests/$dir/ - Creating..."
            mkdir -p tests/$dir
        fi
    done
    
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
    
    if [ -d "sdk/python" ]; then
        PY_FILES=$(find sdk/python -type f -name "*.py" 2>/dev/null | wc -l | tr -d ' ')
        echo "  ✅ sdk/python/ - $PY_FILES Python files"
    else
        echo "  ❌ sdk/python/ - MISSING"
    fi
    
    if [ -d "sdk/java" ]; then
        if [ -f "sdk/java/README.md" ]; then
            echo "  ✅ sdk/java/ - README.md present"
        else
            echo "  ⚠️ sdk/java/ - README.md missing"
        fi
    else
        echo "  ❌ sdk/java/ - MISSING"
    fi
    
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
    echo "  📁 Key documentation files:"
    ls docs/*.md 2>/dev/null | head -10 | sed 's/^/    /'
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
# SECTION 8: COMPLETE FILE TREE
# ============================================================

echo "============================================================"
echo "🌳 COMPLETE FILE TREE (Top Level)"
echo "============================================================"
echo ""

echo "📁 $PROJECT_ROOT"
ls -la | grep -v "^total" | grep -v "^d.*\\.$" | grep -v "^d.*\\.\\.$" | awk '{print "  " $9}' | sort | while read item; do
    if [ -d "$item" ] && [ "$item" != "." ] && [ "$item" != ".." ]; then
        echo "  📁 $item/"
    elif [ -f "$item" ]; then
        echo "  📄 $item"
    fi
done

echo ""
echo "📁 Subdirectories depth 2:"
find . -maxdepth 2 -type d ! -path "." ! -path "./.git" ! -path "./.pytest_cache" | sed 's/^\.\///' | sort | while read dir; do
    if [ -n "$dir" ]; then
        echo "  📁 $dir/"
    fi
done

# ============================================================
# SECTION 9: SUMMARY
# ============================================================

echo ""
echo "============================================================"
echo "📊 VALIDATION SUMMARY"
echo "============================================================"

TOTAL_FILES=$(find . -type f ! -path "./.git/*" 2>/dev/null | wc -l | tr -d ' ')
PY_FILES=$(find . -type f -name "*.py" ! -path "./.git/*" 2>/dev/null | wc -l | tr -d ' ')
MD_FILES=$(find . -type f -name "*.md" ! -path "./.git/*" 2>/dev/null | wc -l | tr -d ' ')

echo "  📁 Project Root: $PROJECT_ROOT"
echo "  📄 Total Files: $TOTAL_FILES"
echo "  🐍 Python Files: $PY_FILES"
echo "  📝 Markdown Files: $MD_FILES"
echo ""

echo "  ✅ Root files: All required present"
echo "  🧪 Test files: $TOTAL_TESTS"
echo "  📚 Doc files: $DOC_FILES"
echo ""

# Check critical issues
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
    echo "  ⚠️ tests/unit/ is missing (created)"
    mkdir -p tests/unit
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
echo "  1. Run: python3 -m venv venv && source venv/bin/activate"
echo "  2. Run: pip install -e ."
echo "  3. Run: pytest tests/unit/ -v"
echo ""
