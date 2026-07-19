"""
AI-SE OS SDK Data Models
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TaskState(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    PLANNING = "planning"
    RUNNING = "running"
    WAITING = "waiting"
    RETRYING = "retrying"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    ARCHIVED = "archived"


class ValidationStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Repository:
    """Repository configuration"""
    id: str
    name: str
    language: str
    framework: str
    owner: str
    git_url: str
    build_command: Optional[str] = None
    test_command: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "language": self.language,
            "framework": self.framework,
            "owner": self.owner,
            "git_url": self.git_url,
            "build_command": self.build_command,
            "test_command": self.test_command
        }


@dataclass
class Task:
    """Task definition"""
    id: str
    name: str
    description: str
    state: TaskState
    scope: Dict[str, Any]
    dependencies: List[str]
    constraints: Dict[str, Any]
    success_criteria: List[str]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            state=TaskState(data["state"]),
            scope=data["scope"],
            dependencies=data["dependencies"],
            constraints=data["constraints"],
            success_criteria=data["success_criteria"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )


@dataclass
class Plan:
    """Task plan"""
    id: str
    tasks: List[Task]
    confidence: float
    created_at: datetime
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Plan":
        return cls(
            id=data["plan_id"],
            tasks=[Task.from_dict(t) for t in data["tasks"]],
            confidence=data["confidence"],
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        )


@dataclass
class Execution:
    """Execution record"""
    id: str
    task_id: str
    status: str
    progress: float
    current_task: Optional[str]
    completed_tasks: int
    total_tasks: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Execution":
        return cls(
            id=data["execution_id"],
            task_id=data.get("task_id", ""),
            status=data["status"],
            progress=data["progress"],
            current_task=data.get("current_task"),
            completed_tasks=data["completed_tasks"],
            total_tasks=data["total_tasks"]
        )


@dataclass
class ValidationResult:
    """Validation result"""
    id: str
    execution_id: str
    layers: List[Dict[str, Any]]
    overall_status: str
    confidence: float
    report: str
    created_at: datetime
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ValidationResult":
        return cls(
            id=data["id"],
            execution_id=data["execution_id"],
            layers=data["layers"],
            overall_status=data["overall_status"],
            confidence=data["confidence"],
            report=data["report"],
            created_at=datetime.fromisoformat(data["created_at"])
        )


@dataclass
class Experience:
    """Engineering experience"""
    id: str
    problem: Dict[str, Any]
    reasoning: Dict[str, Any]
    solution: Dict[str, Any]
    validation: Dict[str, Any]
    outcome: Dict[str, Any]
    created_at: datetime
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Experience":
        return cls(
            id=data["id"],
            problem=data["problem"],
            reasoning=data["reasoning"],
            solution=data["solution"],
            validation=data["validation"],
            outcome=data["outcome"],
            created_at=datetime.fromisoformat(data["created_at"])
        )


@dataclass
class GenomeSnapshot:
    """Genome snapshot"""
    id: str
    repository_id: str
    version: str
    git_hash: str
    timestamp: datetime
    architecture: Dict[str, Any]
    domain: Dict[str, Any]
    build: Dict[str, Any]
    security: Dict[str, Any]
    runtime: Dict[str, Any]
    test: Dict[str, Any]
    health: Dict[str, Any]
    intelligence_score: float
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GenomeSnapshot":
        return cls(
            id=data["id"],
            repository_id=data["repository_id"],
            version=data["version"],
            git_hash=data["git_hash"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            architecture=data["architecture"],
            domain=data["domain"],
            build=data["build"],
            security=data["security"],
            runtime=data["runtime"],
            test=data["test"],
            health=data["health"],
            intelligence_score=data.get("intelligence_score", 0.0)
        )


@dataclass
class SimulationResult:
    """Simulation result"""
    simulation_id: str
    predicted_state: Dict[str, Any]
    impact: Dict[str, Any]
    confidence: float
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SimulationResult":
        return cls(
            simulation_id=data["simulation_id"],
            predicted_state=data["predicted_state"],
            impact=data["impact"],
            confidence=data["confidence"]
        )


@dataclass
class EconomicsAnalysis:
    """Economics analysis"""
    costs: Dict[str, Any]
    roi: float
    recommendation: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EconomicsAnalysis":
        return cls(
            costs=data["costs"],
            roi=data["roi"],
            recommendation=data["recommendation"]
        )


@dataclass
class IntelligenceScore:
    """Intelligence score"""
    overall: float
    components: Dict[str, float]
    breakdown: Dict[str, Any]
    recommendations: List[str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IntelligenceScore":
        return cls(
            overall=data["overall"],
            components=data["components"],
            breakdown=data["breakdown"],
            recommendations=data["recommendations"]
        )


@dataclass
class TrustExplanation:
    """Trust explanation"""
    decision: str
    evidence: List[Dict[str, Any]]
    confidence: float
    alternatives: List[Dict[str, Any]]
    audit_trail: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TrustExplanation":
        return cls(
            decision=data["decision"],
            evidence=data["evidence"],
            confidence=data["confidence"],
            alternatives=data.get("alternatives", []),
            audit_trail=data.get("audit_trail", "")
        )