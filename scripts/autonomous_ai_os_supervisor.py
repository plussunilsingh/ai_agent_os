#!/usr/bin/env python3
"""
AI-SE OS Autonomous Task Supervisor & Execution Engine
Orchestrates multi-tier full-stack implementation by delegating all code generation
and planning tasks to AI-SE OS (Ollama qwen2.5:7b). Collects real performance & ROI metrics.
"""

import os
import sys
import json
import time
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ai_se_os.execution.ollama_adapter import OllamaAdapter
from ai_se_os.cache.cache_service import CacheService
from ai_se_os.execution.model_router import ModelRouter, TaskType

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AI-OS-Supervisor")

class AIOSSupervisor:
    def __init__(self):
        self.cache_service = CacheService()
        self.router = ModelRouter(cache_service=self.cache_service)
        self.adapter = OllamaAdapter(model="qwen2.5:7b")
        self.metrics = {
            "total_tasks_processed": 0,
            "total_latency_seconds": 0.0,
            "estimated_token_savings": 0,
            "llm_api_cost_usd": 0.00,  # Local Ollama is $0.00
            "tasks": []
        }

    def execute_chunk(self, chunk_id: str, title: str, prompt: str, target_file: str):
        logger.info(f"🚀 [AI-OS Task {chunk_id}] Delegating to AI-SE OS: '{title}'...")
        start_time = time.time()
        
        # Select model using AI-SE OS router
        route = self.router.route(TaskType.EXECUTION, task={"name": title})
        
        system_prompt = "You are AI-SE OS Autonomous Code Generation Engine. Output clean code only."
        res = self.adapter.generate(prompt=prompt, system_prompt=system_prompt)
        elapsed = time.time() - start_time
        
        if res.get("success"):
            code_output = res.get("response", "")
            # Save generated code to target file
            full_path = os.path.join(os.path.dirname(__file__), "..", target_file)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Clean markdown formatting if present
            cleaned_code = code_output
            if "```" in cleaned_code:
                lines = cleaned_code.split("\n")
                code_lines = []
                inside = False
                for line in lines:
                    if line.startswith("```"):
                        inside = not inside
                        continue
                    if inside:
                        code_lines.append(line)
                cleaned_code = "\n".join(code_lines) if code_lines else cleaned_code
                
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(cleaned_code)
                
            logger.info(f"✅ [AI-OS Task {chunk_id}] Completed in {elapsed:.2f}s -> Written to {target_file}")
            
            # Record metrics
            eval_count = res.get("usage", {}).get("eval_count", 250)
            self.metrics["total_tasks_processed"] += 1
            self.metrics["total_latency_seconds"] += elapsed
            self.metrics["estimated_token_savings"] += eval_count * 4  # Context compression factor
            self.metrics["tasks"].append({
                "chunk_id": chunk_id,
                "title": title,
                "status": "SUCCESS",
                "latency_sec": round(elapsed, 2),
                "model": self.adapter.model,
                "target_file": target_file
            })
            return True
        else:
            logger.error(f"❌ [AI-OS Task {chunk_id}] Failed: {res.get('error')}")
            self.metrics["tasks"].append({
                "chunk_id": chunk_id,
                "title": title,
                "status": "FAILED",
                "latency_sec": round(elapsed, 2),
                "error": res.get("error")
            })
            return False

    def run_fullstack_orchestration(self):
        print("==================================================================")
        print("🤖 AI-SE OS AUTONOMOUS MULTI-TIER SUPERVISOR INITIALIZATION")
        print("==================================================================")
        print()
        
        subtasks = [
            {
                "id": "CHUNK-1",
                "title": "PostgreSQL JPA AdminUserEntity",
                "prompt": "Write Java code for AdminUserEntity.java in package org.yt.entity mapped to database table 'admin_users' with JPA annotations (@Entity, @Table, @Id, @Column).",
                "target": "src/main/java/org/yt/entity/AdminUserEntity.java"
            },
            {
                "id": "CHUNK-2",
                "title": "PostgreSQL JPA AuditLogEntity",
                "prompt": "Write Java code for AuditLogEntity.java in package org.yt.entity mapped to database table 'audit_logs' with JPA annotations.",
                "target": "src/main/java/org/yt/entity/AuditLogEntity.java"
            },
            {
                "id": "CHUNK-3",
                "title": "Spring Data AdminUserRepository",
                "prompt": "Write Java code for AdminUserRepository.java in package org.yt.repository extending JpaRepository<AdminUserEntity, String> with custom query method findByEmail(String email).",
                "target": "src/main/java/org/yt/repository/AdminUserRepository.java"
            },
            {
                "id": "CHUNK-4",
                "title": "botanixUI TypeScript API Service Client",
                "prompt": "Write TypeScript code for botanixUiService.ts in src/botanixUI connecting botanixUI to Java Admin REST API (http://localhost:8080/api/admin/users) and AI-SE OS API (http://localhost:8000/api/v1/botanix).",
                "target": "src/botanixUI/botanixUiService.ts"
            },
            {
                "id": "CHUNK-5",
                "title": "botanixUI React Admin Dashboard Component",
                "prompt": "Write React TypeScript code for BotanixAdminDashboard.tsx in src/botanixUI rendering Admin user list, user creation modal, and AI task planner widget. Enforce high contrast text styling.",
                "target": "src/botanixUI/BotanixAdminDashboard.tsx"
            },
            {
                "id": "CHUNK-6",
                "title": "JUnit 5 JPA Repository Unit Test",
                "prompt": "Write Java code for AdminRepositoryTest.java in package org.yt.repository using @DataJpaTest to test AdminUserRepository CRUD operations.",
                "target": "src/test/java/org/yt/repository/AdminRepositoryTest.java"
            }
        ]
        
        for task in subtasks:
            self.execute_chunk(task["id"], task["title"], task["prompt"], task["target"])
            
        print()
        print("==================================================================")
        print("📊 AI-SE OS AUTONOMOUS EXECUTION PERFORMANCE & METRICS SUMMARY")
        print("==================================================================")
        print(json.dumps(self.metrics, indent=2))
        
        # Save metrics to report data file
        with open(os.path.join(os.path.dirname(__file__), "..", "docs", "execution_metrics.json"), "w") as f:
            json.dump(self.metrics, f, indent=2)
            
        logger.info("Metrics written to docs/execution_metrics.json")

if __name__ == "__main__":
    supervisor = AIOSSupervisor()
    supervisor.run_fullstack_orchestration()
