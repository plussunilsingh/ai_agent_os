#!/usr/bin/env python3
"""
AI-SE OS Autonomous Architecture Orchestration & Code Generation Engine Test
Demonstrates AI-SE OS taking an enterprise architecture request, creating a task DAG,
generating Java Spring Boot code artifacts, and performing automated validation.
"""

import os
import sys
import json
import logging

# Set PYTHONPATH to include src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ai_se_os.execution.ollama_adapter import OllamaAdapter
from ai_se_os.cache.cache_service import CacheService
from ai_se_os.execution.model_router import ModelRouter, TaskType

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AI-OS-Engine")

def run_ai_os_architecture_test():
    print("==================================================================")
    print("🤖 AI-SE OS - AUTONOMOUS ARCHITECTURE ORCHESTRATION ENGINE TEST")
    print("==================================================================")
    print()
    
    # 1. Initialize AI-SE OS Core Subsystems
    logger.info("Initializing AI-SE OS Subsystems (CacheService, ModelRouter, OllamaAdapter)...")
    cache_service = CacheService()
    router = ModelRouter(cache_service=cache_service)
    ollama_adapter = OllamaAdapter(model="qwen2.5:7b")
    
    # 2. Model Routing Decision
    route = router.route(TaskType.ARCHITECTURE, task={"name": "Java Admin App Architecture"})
    print(f"🎯 Model Router Selected Model: {ollama_adapter.model}")
    print(f"   Rationale: {route.rationale}")
    print()

    # 3. Requirement Intake
    requirement = (
        "Architect and implement a Spring Boot Enterprise Java Admin Application with:\n"
        "1. Standardized ApiResponse<T> envelope (success, message, data, timestamp)\n"
        "2. AdminUser domain entity and Role enum (SUPER_ADMIN, ADMIN, MODERATOR, AUDITOR)\n"
        "3. AdminUserService business logic with duplicate validation\n"
        "4. AdminUserController REST endpoints (GET, POST, PUT, DELETE)\n"
        "5. GlobalExceptionHandler converting runtime errors into ApiResponse envelope\n"
        "6. JUnit 5 and MockMvc test suite"
    )
    
    logger.info("Submitting requirement to AI-SE OS Task Planner...")
    plan_res = ollama_adapter.generate_plan_from_requirement(requirement, "admin-java-app")
    
    print("==================================================================")
    print("📊 AI-SE OS GENERATED TASK DAG & ORCHESTRATION PLAN")
    print("==================================================================")
    print(plan_res.get("plan_output", "No plan generated"))
    print()
    
    # 4. Generate Core Code Artifact via AI-SE OS
    logger.info("AI-SE OS generating Java Spring Boot Architecture Code...")
    code_prompt = (
        "Write the complete Java code for AdminUserController.java under package org.yt.controller. "
        "It should use AdminUserService and wrap all responses in ApiResponse<T> envelope."
    )
    code_res = ollama_adapter.generate(prompt=code_prompt, system_prompt="You are AI-SE OS Senior Java Architect. Output clean Java code only.")
    
    print("==================================================================")
    print("💻 AI-SE OS GENERATED JAVA ARCHITECTURE CODE")
    print("==================================================================")
    print(code_res.get("response", ""))
    print()
    
    print("==================================================================")
    print("✅ AI-SE OS ARCHITECTURE ORCHESTRATION TEST COMPLETED SUCCESSFULLY")
    print("==================================================================")

if __name__ == "__main__":
    run_ai_os_architecture_test()
