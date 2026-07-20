#!/usr/bin/env python3
"""
AI-SE OS Live Application Launcher
Launches Java Admin Backend (Port 8080) and BotanixUI Frontend (Port 3000/8000)
and maintains background dev servers for live user UI interaction.
"""

import os
import sys
import time
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AI-OS-LiveLauncher")

def launch_apps():
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    admin_dir = os.path.join(workspace_root, "admin")
    botanix_dir = os.path.join(workspace_root, "botanixUI")
    ai_os_dir = os.path.join(workspace_root, "AI_AGENT_OS")

    logger.info("🚀 Launching AI-SE OS Core API Server on port 8000...")
    ai_os_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.ai_se_os.api.routes:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=ai_os_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    logger.info("☕ Launching Java Admin Application on port 8080...")
    admin_proc = subprocess.Popen(
        ["./gradlew", "bootRun"],
        cwd=admin_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    logger.info("🎨 Launching BotanixUI Web Application on port 3000/8000...")
    botanix_proc = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=botanix_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    logger.info("==================================================")
    logger.info("🌐 LIVE APPLICATIONS ARE NOW ACTIVE & ACCESSIBLE:")
    logger.info("👉 BotanixUI App:     http://localhost:3000")
    logger.info("👉 Java Admin API:    http://localhost:8080/api/admin/users")
    logger.info("👉 AI-SE OS Server:   http://localhost:8000/health")
    logger.info("==================================================")

    # Keep background processes running
    time.sleep(3600)

if __name__ == "__main__":
    launch_apps()
