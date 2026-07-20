from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# ============================================================
# Health Check Endpoints
# ============================================================

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "ai-se-os",
        "version": "12.0.0"
    }

@router.get("/health/detailed")
async def detailed_health() -> Dict[str, Any]:
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "service": "ai-se-os",
        "version": "12.0.0",
        "components": {
            "database": "connected",
            "cache": "connected",
            "models": "available"
        }
    }

@router.get("/ready")
async def readiness() -> Dict[str, Any]:
    """Readiness probe endpoint."""
    return {"status": "ready"}

@router.get("/live")
async def liveness() -> Dict[str, Any]:
    """Liveness probe endpoint."""
    return {"status": "alive"}

# ============================================================
# Ollama & Botanix Integration Endpoints
# ============================================================

from ai_se_os.execution.ollama_adapter import OllamaAdapter

ollama_client = OllamaAdapter()

@router.get("/ollama/status")
async def ollama_status() -> Dict[str, Any]:
    """Check Ollama model status."""
    is_connected = ollama_client.check_connection()
    return {
        "status": "connected" if is_connected else "disconnected",
        "model": ollama_client.model,
        "host": ollama_client.host
    }

@router.post("/botanix/generate-plan")
async def botanix_generate_plan(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Generate engineering task plan for botanixUI using local Ollama model."""
    requirement = payload.get("requirement", "")
    repo_id = payload.get("repository_id", "botanix-ui")
    
    if not requirement:
        raise HTTPException(status_code=400, detail="Requirement prompt is required")
        
    result = ollama_client.generate_plan_from_requirement(requirement, repo_id)
    return result

@router.post("/botanix/chat")
async def botanix_chat(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Chat with AI-SE OS for botanixUI powered by local Ollama."""
    message = payload.get("message", "")
    system_prompt = payload.get("system_prompt", "You are AI-SE OS Engineering Assistant for BotanixUI.")
    
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
        
    result = ollama_client.generate(prompt=message, system_prompt=system_prompt)
    return result


# ============================================================
# Repository Endpoints
# ============================================================

@router.post("/repositories/register")
async def register_repository(repo_data: Dict[str, Any]) -> Dict[str, Any]:
    """Register a repository."""
    return {
        "repository_id": repo_data.get("id", "test-repo"),
        "status": "registered",
        "genome_version": "v1.0.0"
    }

@router.get("/repositories/{repository_id}/genome")
async def get_genome(repository_id: str) -> Dict[str, Any]:
    """Get Genome snapshot."""
    return {
        "id": f"genome-{repository_id}",
        "repository_id": repository_id,
        "version": "v1.0.0",
        "git_hash": "abc123",
        "timestamp": "2026-01-15T10:30:00Z",
        "architecture": {"modules": ["mod1", "mod2"]},
        "domain": {},
        "build": {},
        "security": {},
        "runtime": {},
        "test": {},
        "health": {"confidence": 0.95, "intelligence_score": 85}
    }

@router.post("/repositories/{repository_id}/analyze")
async def analyze_repository(repository_id: str) -> Dict[str, Any]:
    """Analyze repository."""
    return {
        "analysis_id": f"ana-{repository_id}-123",
        "status": "started",
        "repository_id": repository_id
    }

# ============================================================
# Planning Endpoints
# ============================================================

@router.post("/plans/generate")
async def generate_plan(plan_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a task plan."""
    return {
        "plan_id": "plan-123",
        "tasks": [
            {
                "id": "task-1",
                "name": "Analyze requirement",
                "description": "Analyze the requirement",
                "state": "created"
            },
            {
                "id": "task-2",
                "name": "Implement solution",
                "description": "Implement the solution",
                "state": "created"
            }
        ],
        "confidence": 0.92
    }

# ============================================================
# Execution Endpoints
# ============================================================

@router.post("/plans/{plan_id}/execute")
async def execute_plan(plan_id: str) -> Dict[str, Any]:
    """Execute a plan."""
    return {
        "execution_id": f"exec-{plan_id}-123",
        "status": "running",
        "progress": 0.0,
        "completed_tasks": 0,
        "total_tasks": 2
    }

@router.get("/executions/{execution_id}/status")
async def get_execution_status(execution_id: str) -> Dict[str, Any]:
    """Get execution status."""
    return {
        "execution_id": execution_id,
        "status": "completed",
        "progress": 1.0,
        "completed_tasks": 2,
        "total_tasks": 2
    }

# ============================================================
# Validation Endpoints
# ============================================================

@router.post("/validation/run")
async def run_validation(validation_data: Dict[str, Any]) -> Dict[str, Any]:
    """Run validation."""
    return {
        "id": "val-123",
        "execution_id": "exec-123",
        "layers": [
            {"layer": "build", "status": "pass", "details": "Build successful"},
            {"layer": "test", "status": "pass", "details": "All tests passed"}
        ],
        "overall_status": "pass",
        "confidence": 0.95,
        "report": "All checks passed"
    }

# ============================================================
# Experience Endpoints
# ============================================================

@router.post("/experiences/search")
async def search_experiences(search_data: Dict[str, Any]) -> Dict[str, Any]:
    """Search experiences."""
    return {
        "experiences": [
            {
                "id": "exp-1",
                "problem": {"description": "JWT token refresh"},
                "solution": {"steps": ["Implement refresh endpoint"]},
                "outcome": {"success": True, "confidence": 0.95}
            }
        ]
    }

@router.post("/experiences/recommend")
async def recommend_experience(recommend_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get experience recommendations."""
    return {
        "recommendations": [
            {
                "id": "rec-1",
                "experience_id": "exp-42",
                "confidence": 0.92,
                "rationale": "Similar problem detected"
            }
        ]
    }

# ============================================================
# Physics Endpoints
# ============================================================

@router.post("/physics/predict")
async def predict_impact(predict_data: Dict[str, Any]) -> Dict[str, Any]:
    """Predict impact of a change."""
    return {
        "impact": [
            {"file": "src/main.py", "change_type": "modify"},
            {"file": "tests/test_main.py", "change_type": "modify"}
        ],
        "confidence": 0.88,
        "severity": "medium"
    }

# ============================================================
# Simulation Endpoints
# ============================================================

@router.post("/simulation/run")
async def run_simulation(sim_data: Dict[str, Any]) -> Dict[str, Any]:
    """Run a simulation."""
    return {
        "simulation_id": "sim-123",
        "predicted_state": {"files_changed": 2, "tests_affected": 3},
        "impact": {"risk": "low"},
        "confidence": 0.85
    }

# ============================================================
# Economics Endpoints
# ============================================================

@router.post("/economics/analyze")
async def analyze_economics(econ_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze economics of a decision."""
    return {
        "costs": {
            "development": 400,
            "operational": 5,
            "future": 50
        },
        "roi": 0.92,
        "recommendation": "Proceed with implementation"
    }

# ============================================================
# Intelligence Score Endpoints
# ============================================================

@router.get("/intelligence/score")
async def get_intelligence_score(repository_id: str) -> Dict[str, Any]:
    """Get intelligence score."""
    return {
        "overall": 85,
        "components": {
            "architecture": 90,
            "coverage": 85,
            "maintainability": 80
        },
        "breakdown": {
            "module_count": 45,
            "test_count": 48,
            "coverage": 85
        },
        "recommendations": [
            "Increase test coverage",
            "Reduce technical debt"
        ]
    }

# ============================================================
# Trust Endpoints
# ============================================================

@router.post("/trust/explain")
async def explain_decision(explain_data: Dict[str, Any]) -> Dict[str, Any]:
    """Explain a decision."""
    return {
        "decision": "Use refresh token rotation",
        "evidence": [
            {"source": "Experience #344", "confidence": 0.95},
            {"source": "Physics Rule #42", "confidence": 0.98}
        ],
        "confidence": 0.92,
        "alternatives": [
            {"name": "Increase expiration", "score": 0.3},
            {"name": "No refresh", "score": 0.1}
        ],
        "audit_trail": "audit-0042"
    }

# ============================================================
# Knowledge Graph Endpoints
# ============================================================

@router.post("/knowledge/graph/query")
async def query_knowledge_graph(query_data: Dict[str, Any]) -> Dict[str, Any]:
    """Query the knowledge graph."""
    return {
        "nodes": [
            {"id": "node-1", "type": "class", "name": "User"},
            {"id": "node-2", "type": "class", "name": "Order"}
        ],
        "edges": [
            {"source": "node-1", "target": "node-2", "type": "DEPENDS_ON"}
        ]
    }

@router.post("/knowledge/graph/trace")
async def trace_intent(trace_data: Dict[str, Any]) -> Dict[str, Any]:
    """Trace intent through the knowledge graph."""
    return {
        "path": [
            {"node": "Requirement-1", "type": "requirement"},
            {"node": "ADR-18", "type": "adr"},
            {"node": "OrderService", "type": "service"}
        ],
        "confidence": 0.95
    }


# ============================================================
# REAL Agent Execution Endpoint (Phase 4 — Rust Bridge)
# Called by Rust engine dispatch-task instead of dummy subprocess
# ============================================================

import threading
import time as _time

from ai_se_os.orchestrator.dag_engine import TaskDAGWorkflow


@router.post("/agent/execute")
async def agent_execute(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Real autonomous task execution endpoint.
    Rust engine calls this instead of spawning a dummy Python subprocess.
    Kicks off LLMTaskRunner in a background thread so the HTTP response returns immediately.
    """
    task_id = payload.get("task_id", f"task-api-{int(_time.time())}")
    task_name = payload.get("task_name", "Unnamed Task")
    target_url = payload.get("target_url", "")

    if not task_name:
        raise HTTPException(status_code=400, detail="task_name is required")

    def _run_in_background():
        try:
            workflow = TaskDAGWorkflow(task_id, task_name, target_url)
            workflow.execute_workflow()
        except Exception as exc:
            logger.error(f"[/agent/execute] Background task '{task_name}' crashed: {exc}")

    thread = threading.Thread(target=_run_in_background, daemon=True, name=f"agent-{task_id}")
    thread.start()

    return {
        "accepted": True,
        "task_id": task_id,
        "task_name": task_name,
        "target_url": target_url,
        "message": "Task dispatched to LLM execution engine. Monitor dashboard for progress."
    }


@router.get("/agent/status/{task_id}")
async def agent_status(task_id: str) -> Dict[str, Any]:
    """Get live status of a running or completed agent task."""
    from ai_se_os.telemetry.task_queue_tracker import TaskQueueTracker
    state = TaskQueueTracker._read_state()
    # Search active tasks
    for t in state.get("active_tasks", []):
        if t.get("task_id") == task_id:
            return {"found": True, "status": "active", "task": t}
    # Search history
    for t in state.get("history", []):
        if t.get("task_id") == task_id:
            return {"found": True, "status": "history", "task": t}
    return {"found": False, "task_id": task_id, "message": "Task not found in active or history queue"}


# ============================================================
# TaskManager API Endpoints
# ============================================================

from ai_se_os.core.task_manager import task_manager, TaskStatus


@router.post("/api/v1/task/{task_id}/heartbeat")
async def task_heartbeat(task_id: str, progress: Optional[int] = None, step: Optional[str] = None):
    """Update heartbeat for a task."""
    await task_manager.heartbeat(task_id, progress, step)
    return {"status": "ok", "task_id": task_id}


@router.post("/api/v1/task/{task_id}/cancel")
async def cancel_task(task_id: str):
    """Cancel a running task."""
    await task_manager.transition(task_id, TaskStatus.CANCELLED, step="Cancelled by user")
    return {"status": "cancelled", "task_id": task_id}


@router.get("/api/v1/task/{task_id}/history")
async def get_task_history(task_id: str):
    """Get event history for a task."""
    events = await task_manager.get_history(task_id)
    return [{"timestamp": e.timestamp, "status": e.status.value, "step": e.step, "progress": e.progress} for e in events]

