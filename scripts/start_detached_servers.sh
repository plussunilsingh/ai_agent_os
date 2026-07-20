#!/bin/bash
# AI-SE OS Detached Background Server Launcher
# Starts BotanixUI (Port 9000) and Java Admin App (Port 8080) in detached background mode (nohup)
# Returns immediately (exit code 0) so NO agent tasks remain pending or blocked!

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "🚀 Launching Detached Background Servers..."

# 1. Start BotanixUI on Port 9000 (if not already listening)
if ! lsof -i:9000 >/dev/null 2>&1; then
    echo "Starting BotanixUI on Port 9000 (Detached)..."
    cd "$ROOT_DIR/botanixUI"
    nohup npm run dev -- -p 9000 > "$ROOT_DIR/AI_AGENT_OS/docs/botanix_ui_server.log" 2>&1 &
else
    echo "BotanixUI is already running on Port 9000."
fi

# 2. Start Java Admin App on Port 8080 (if not already listening)
if ! lsof -i:8080 >/dev/null 2>&1; then
    echo "Starting Java Admin App on Port 8080 (Detached)..."
    cd "$ROOT_DIR/admin"
    nohup ./gradlew bootRun > "$ROOT_DIR/AI_AGENT_OS/docs/admin_backend_server.log" 2>&1 &
else
    echo "Java Admin App is already running on Port 8080."
fi

sleep 2
echo "✅ Detached Servers Launcher Completed. Agent task ends cleanly."
