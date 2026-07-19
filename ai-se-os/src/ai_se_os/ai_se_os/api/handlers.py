"""
AI-SE OS API Handlers
Business logic for API endpoints
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from uuid import UUID, uuid4

from ..core.data_models import (
    Repository,
    Task,
    Plan,
    Execution,
    ValidationResult,
    Experience,
    GenomeSnapshot,
    SimulationResult,
    EconomicsAnalysis,
    IntelligenceScore,
    TrustExplanation
)
from ..core.events import Event, EventType, get_event_bus
from ..kernel.state_manager import StateManager, NamespaceKey
from ..kernel.scheduler import Scheduler, ScheduledTask
from ..intelligence.genome import GenomeAnalyzer
from ..intelligence.knowledge_graph import KnowledgeGraphService
from ..intelligence.reasoning import ReasoningEngine
from ..intelligence.decision_engine import DecisionEngine
from ..execution.context_compiler import ContextCompiler
from ..execution.prompt_compiler import PromptCompiler
from ..execution.model_router import ModelRouter
from ..execution.agent_runtime import AgentRuntime
from ..execution.validation_engine import ValidationEngine
from ..execution.recovery_engine import RecoveryEngine
from ..cache.cache_service import CacheService


class APIHandlers:
    """
    Business logic handlers for all API endpoints.
    Wires together all AI-SE OS subsystems.
    """

    def __init__(self):
        # Core infrastructure
        self.state_manager = StateManager()
        self.scheduler = Scheduler()
        self.event_bus = get_event_bus()

        # Cache
        self.cache_service = CacheService()

        # Intelligence
        self.genome_analyzer = GenomeAnalyzer()
        self.knowledge_graph = KnowledgeGraphService()
        self.reasoning_engine = ReasoningEngine()
        self.decision_engine = DecisionEngine()

        # Execution
        self.context_compiler = ContextCompiler(self.cache_service)
        self.prompt_compiler = PromptCompiler(self.cache_service)
        self.model_router = ModelRouter(self.cache_service)
        self.agent_runtime = AgentRuntime(self.scheduler, self.decision_engine)
        self.validation_engine = ValidationEngine()
        self.recovery_engine = RecoveryEngine()

        # Registered repositories
        self._repositories: Dict[str, Dict[str, Any]] = {}

    def register_repository(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a repository"""
        repo_id = repo_data.get("id", str(uuid4()))
        self._repositories[repo_id] = {
            **repo_data,
            "registered_at": datetime.now().isoformat(),
            "status": "registered"
        }

        # Create namespace
        ns = NamespaceKey(repository=repo_id)
        self.state_manager.set(ns, "config", repo_data, immutable=True)

        # Publish event
        self.event_bus.publish(Event(
            type=EventType.REPOSITORY_REGISTERED,
            source="api_handlers",
            producer="api",
            payload={"repository_id": repo_id, "name": repo_data.get("name", "")}
        ))

        return {"status": "registered", "repository_id": repo_id}

    def get_genome(self, repository_id: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Get genome snapshot"""
        snapshot = self.genome_analyzer.get_snapshot(repository_id, version)
        if not snapshot:
            return {"error": "No genome snapshot available"}
        return snapshot.to_dict()

    def analyze_repository(self, repository_id: str) -> Dict[str, Any]:
        """Trigger repository analysis"""
        # Create a fingerprint (simulated)
        from ..intelligence.genome import RepositoryFingerprint
        fp = RepositoryFingerprint(
            git_hash="abc123",
            file_count=100,
            language_breakdown={"python": 50, "java": 30, "javascript": 20},
            dependency_count=25,
            module_count=8,
            test_count=30,
            total_lines=10000,
            age_days=365
        )

        snapshot = self.genome_analyzer.create_snapshot(repository_id, fp.git_hash, fp)
        return {
            "repository_id": repository_id,
            "status": "analyzed",
            "snapshot_version": snapshot.version,
            "intelligence_score": snapshot.health.intelligence_score
        }

    def generate_plan(self, requirement: str, repository_id: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate a task plan"""
        # Create tasks from requirement
        task = ScheduledTask(
            name=f"Plan: {requirement[:50]}",
            priority=5,
            metadata={"requirement": requirement, "repository_id": repository_id}
        )
        task_id = self.scheduler.enqueue_task(task)

        return {
            "plan_id": f"plan-{task_id[:8]}",
            "tasks": [{"id": task_id, "name": task.name, "state": task.state.value}],
            "confidence": 0.85,
            "created_at": datetime.now().isoformat()
        }

    def execute_plan(self, plan_id: str, model: Optional[str] = None, max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """Execute a plan"""
        # Dequeue and execute
        task = self.scheduler.dequeue_task()
        if not task:
            return {"error": "No pending tasks"}

        # Route to model
        from ..execution.model_router import TaskType
        route = self.model_router.route(TaskType.EXECUTION, task)

        execution_id = str(uuid4())
        self.scheduler.update_task_state(task.id, TaskState.RUNNING)

        return {
            "execution_id": execution_id,
            "plan_id": plan_id,
            "status": "started",
            "progress": 0.0,
            "model": model or route.model_id,
            "routing_rationale": route.rationale
        }

    def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """Get execution status"""
        execution = self.agent_runtime.get_execution(execution_id)
        if not execution:
            return {"error": "Execution not found"}
        return execution

    def run_validation(self, repository_id: str, change_id: Optional[str] = None, layers: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run validation"""
        report = self.validation_engine.run_validation(
            execution_id=str(uuid4()),
            repository_id=repository_id,
            change_id=change_id,
            layers=layers
        )
        return {
            "id": report.id,
            "execution_id": report.execution_id,
            "layers": [{"name": l.name, "status": l.status} for l in report.layers],
            "overall_status": report.overall_status,
            "confidence": report.confidence,
            "report": report.summary,
            "created_at": report.created_at
        }

    def search_experiences(self, query: str, filters: Optional[Dict] = None, limit: int = 10) -> Dict[str, Any]:
        """Search experiences"""
        return {"experiences": [], "total": 0, "query": query}

    def predict_impact(self, repository_id: str, change: Dict[str, Any]) -> Dict[str, Any]:
        """Predict impact"""
        prediction = self.reasoning_engine.predict_impact(repository_id, change)
        return {
            "repository_id": repository_id,
            "prediction": {
                "risk_level": prediction.risk_level,
                "files_affected": len(prediction.files_affected),
                "estimated_effort_hours": prediction.estimated_effort_hours,
                "breaking_changes": prediction.breaking_changes
            },
            "confidence": prediction.confidence,
            "reasoning": prediction.reasoning
        }

    def get_intelligence_score(self, repository_id: str) -> Dict[str, Any]:
        """Get intelligence score"""
        score = self.genome_analyzer.get_intelligence_score(repository_id)
        insights = self.genome_analyzer.get_insights(repository_id)
        return {
            "overall": score,
            "components": {
                "architecture": 0.8,
                "testing": 0.7,
                "security": 0.85,
                "documentation": 0.6
            },
            "breakdown": insights,
            "recommendations": [
                "Improve test coverage",
                "Add API documentation"
            ]
        }

    def explain_decision(self, decision_id: str) -> Dict[str, Any]:
        """Explain a decision"""
        explanation = self.decision_engine.explain(decision_id)
        if not explanation:
            return {"error": "Decision not found"}
        return {
            "decision_id": explanation.decision_id,
            "decision": explanation.decision,
            "summary": explanation.summary,
            "evidence": explanation.evidence,
            "confidence": explanation.confidence,
            "audit_trail": explanation.audit_trail
        }

    def query_knowledge_graph(self, query: str, parameters: Optional[Dict] = None) -> Dict[str, Any]:
        """Query knowledge graph"""
        results = self.knowledge_graph.query_cypher("default", query)
        return {"results": results, "query": query, "execution_time_ms": 0}

    def trace_intent(self, source_id: str, target_type: str, depth: int = 5) -> Dict[str, Any]:
        """Trace intent"""
        return self.knowledge_graph.trace_intent("default", source_id, target_type, depth)

    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            "repositories": len(self._repositories),
            "state": self.state_manager.get_stats(),
            "scheduler": self.scheduler.get_stats(),
            "validation": self.validation_engine.get_stats(),
            "recovery": self.recovery_engine.get_stats(),
            "decisions": self.decision_engine.get_stats(),
            "event_bus": self.event_bus.get_stats(),
            "agent_runtime": self.agent_runtime.get_stats()
        }