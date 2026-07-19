"""
AI-SE OS Core Data Models
Complete canonical data model for the Engineering Intelligence Platform
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Set, Union
from enum import Enum
from uuid import UUID, uuid4
from dataclasses import dataclass, field
import json


# ============================================================================
# ENUMS
# ============================================================================

class RepositoryStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"

class ModuleType(str, Enum):
    SERVICE = "service"
    LIBRARY = "library"
    UTILITY = "utility"
    TEST = "test"
    CONFIG = "config"

class ClassType(str, Enum):
    CLASS = "class"
    INTERFACE = "interface"
    ENUM = "enum"
    RECORD = "record"

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

class AgentExecutionStatus(str, Enum):
    PENDING = "pending"
    LEASING = "leasing"
    EXECUTING = "executing"
    VALIDATING = "validating"
    RECOVERING = "recovering"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ValidationLayer(str, Enum):
    BUILD = "build"
    STATIC = "static"
    TEST = "test"
    ARCHITECTURE = "architecture"
    SECURITY = "security"
    POLICY = "policy"
    RUNTIME = "runtime"
    ACCEPTANCE = "acceptance"

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class KnowledgeNodeType(str, Enum):
    REPOSITORY = "repository"
    MODULE = "module"
    CLASS = "class"
    METHOD = "method"
    API = "api"
    DATABASE = "database"
    REQUIREMENT = "requirement"
    STORY = "story"
    ADR = "adr"
    TEST = "test"
    BUG = "bug"
    INCIDENT = "incident"
    DEPLOYMENT = "deployment"
    PIPELINE = "pipeline"
    SERVICE = "service"
    OWNER = "owner"
    TEAM = "team"
    RELEASE = "release"
    POLICY = "policy"
    LIBRARY = "library"
    FRAMEWORK = "framework"
    CONTAINER = "container"
    ENVIRONMENT = "environment"
    CONFIG = "config"
    FEATURE = "feature"
    METRIC = "metric"

class KnowledgeEdgeType(str, Enum):
    CALLS = "calls"
    IMPORTS = "imports"
    DEPENDS_ON = "depends_on"
    IMPLEMENTS = "implements"
    OWNS = "owns"
    BREAKS = "breaks"
    FIXES = "fixes"
    TESTED_BY = "tested_by"
    DEPLOYS_TO = "deploys_to"
    USES = "uses"
    DOCUMENTS = "documents"
    CREATED_BY = "created_by"
    SUPERSEDES = "supersedes"
    APPROVED_BY = "approved_by"
    SATISFIES = "satisfies"
    TRACES_TO = "traces_to"
    VALIDATES = "validates"
    VERIFIES = "verifies"

class RecoveryStrategyType(str, Enum):
    RETRY = "retry"
    ROLLBACK = "rollback"
    REPLAN = "replan"
    FIX = "fix"
    ESCALATE = "escalate"


# ============================================================================
# CORE ENTITIES
# ============================================================================

@dataclass
class Repository:
    """Repository entity"""
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    url: str = ""
    git_hash: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    owner_id: Optional[UUID] = None
    team_id: Optional[UUID] = None
    status: RepositoryStatus = RepositoryStatus.ACTIVE
    languages: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    intelligence_score: float = 0.0

@dataclass
class Module:
    """Module entity"""
    id: UUID = field(default_factory=uuid4)
    repository_id: UUID = field(default_factory=uuid4)
    name: str = ""
    path: str = ""
    type: ModuleType = ModuleType.SERVICE
    description: str = ""
    owner_id: Optional[UUID] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"

@dataclass
class Method:
    """Method entity"""
    id: UUID = field(default_factory=uuid4)
    class_id: UUID = field(default_factory=uuid4)
    name: str = ""
    return_type: str = ""
    parameters: List[Dict[str, str]] = field(default_factory=list)
    modifiers: List[str] = field(default_factory=list)
    throws: List[str] = field(default_factory=list)
    body_hash: str = ""
    doc: str = ""
    complexity: float = 0.0
    called_by: List[UUID] = field(default_factory=list)
    calls: List[UUID] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


# ============================================================================
# GENOME & DNA
# ============================================================================

@dataclass
class ArchitectureDNA:
    """Architecture DNA component"""
    modules: List[Module] = field(default_factory=list)
    dependencies: List[Dict[str, str]] = field(default_factory=list)
    layers: List[str] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)
    violations: List[str] = field(default_factory=list)
    drift_score: float = 0.0

@dataclass
class DomainDNA:
    """Domain DNA component"""
    entities: List[Dict[str, Any]] = field(default_factory=list)
    services: List[Dict[str, Any]] = field(default_factory=list)
    rules: List[str] = field(default_factory=list)
    events: List[str] = field(default_factory=list)

@dataclass
class BuildDNA:
    """Build DNA component"""
    system: str = "maven"
    dependencies: List[Dict[str, str]] = field(default_factory=list)
    tasks: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SecurityDNA:
    """Security DNA component"""
    auth: Dict[str, Any] = field(default_factory=dict)
    secrets: List[str] = field(default_factory=list)
    policies: List[str] = field(default_factory=list)
    scans: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class RuntimeDNA:
    """Runtime DNA component"""
    deployment: Dict[str, Any] = field(default_factory=dict)
    environments: List[str] = field(default_factory=list)
    scaling: Dict[str, Any] = field(default_factory=dict)
    resources: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TestDNA:
    """Test DNA component"""
    frameworks: List[str] = field(default_factory=list)
    coverage: float = 0.0
    patterns: List[str] = field(default_factory=list)
    flaky_tests: List[str] = field(default_factory=list)

@dataclass
class HealthDNA:
    """Health DNA component"""
    build_status: str = "passing"
    test_pass_rate: float = 0.0
    coverage: float = 0.0
    security_status: str = "clean"
    confidence: float = 0.0
    intelligence_score: float = 0.0

@dataclass
class GenomeSnapshot:
    """Complete Genome Snapshot with 15 DNA dimensions"""
    id: UUID = field(default_factory=uuid4)
    repository_id: UUID = field(default_factory=uuid4)
    version: str = "1.0.0"
    git_hash: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    created_by: Optional[UUID] = None

    # 15 DNA Dimensions
    architecture: ArchitectureDNA = field(default_factory=ArchitectureDNA)
    domain: DomainDNA = field(default_factory=DomainDNA)
    build: BuildDNA = field(default_factory=BuildDNA)
    security: SecurityDNA = field(default_factory=SecurityDNA)
    runtime: RuntimeDNA = field(default_factory=RuntimeDNA)
    test: TestDNA = field(default_factory=TestDNA)
    health: HealthDNA = field(default_factory=HealthDNA)

    # Additional dimensions (simplified for brevity)
    api: Dict[str, Any] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)
    infrastructure: Dict[str, Any] = field(default_factory=dict)
    deployment: Dict[str, Any] = field(default_factory=dict)
    business_process: Dict[str, Any] = field(default_factory=dict)
    ownership: Dict[str, Any] = field(default_factory=dict)
    incident: Dict[str, Any] = field(default_factory=dict)
    observability: Dict[str, Any] = field(default_factory=dict)
    performance: Dict[str, Any] = field(default_factory=dict)
    compliance: Dict[str, Any] = field(default_factory=dict)
    data_flow: Dict[str, Any] = field(default_factory=dict)
    dependency_risk: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": str(self.id),
            "repository_id": str(self.repository_id),
            "version": self.version,
            "git_hash": self.git_hash,
            "timestamp": self.timestamp.isoformat(),
            "created_by": str(self.created_by) if self.created_by else None,
            "architecture": self._serialize_architecture(),
            "domain": self._serialize_domain(),
            "build": self._serialize_build(),
            "security": self._serialize_security(),
            "runtime": self._serialize_runtime(),
            "test": self._serialize_test(),
            "health": self._serialize_health(),
        }

    def _serialize_architecture(self) -> Dict[str, Any]:
        modules = getattr(self.architecture, 'modules', [])
        module_names = []
        for m in modules:
            if isinstance(m, dict):
                module_names.append(m.get("name", str(m)))
            else:
                module_names.append(getattr(m, 'name', str(m)))
        return {
            "modules": module_names,
            "dependencies": getattr(self.architecture, 'dependencies', []),
            "layers": getattr(self.architecture, 'layers', []),
            "patterns": getattr(self.architecture, 'patterns', []),
            "violations": getattr(self.architecture, 'violations', []),
            "drift_score": getattr(self.architecture, 'drift_score', 0.0)
        }

    def _serialize_domain(self) -> Dict[str, Any]:
        return {
            "entities": self.domain.entities,
            "services": self.domain.services,
            "rules": self.domain.rules,
            "events": self.domain.events
        }

    def _serialize_build(self) -> Dict[str, Any]:
        return {
            "system": self.build.system,
            "dependencies": self.build.dependencies,
            "tasks": self.build.tasks,
            "config": self.build.config
        }

    def _serialize_security(self) -> Dict[str, Any]:
        return {
            "auth": self.security.auth,
            "secrets_count": len(self.security.secrets),
            "policies_count": len(self.security.policies),
            "scans": self.security.scans
        }

    def _serialize_runtime(self) -> Dict[str, Any]:
        return {
            "deployment": self.runtime.deployment,
            "environments": self.runtime.environments,
            "scaling": self.runtime.scaling,
            "resources": self.runtime.resources
        }

    def _serialize_test(self) -> Dict[str, Any]:
        return {
            "frameworks": self.test.frameworks,
            "coverage": self.test.coverage,
            "patterns": self.test.patterns,
            "flaky_tests": self.test.flaky_tests
        }

    def _serialize_health(self) -> Dict[str, Any]:
        return {
            "build_status": self.health.build_status,
            "test_pass_rate": self.health.test_pass_rate,
            "coverage": self.health.coverage,
            "security_status": self.health.security_status,
            "confidence": self.health.confidence,
            "intelligence_score": self.health.intelligence_score
        }


# ============================================================================
# KNOWLEDGE GRAPH
# ============================================================================

@dataclass
class KnowledgeNode:
    """Knowledge Graph Node"""
    id: UUID = field(default_factory=uuid4)
    type: KnowledgeNodeType = KnowledgeNodeType.REPOSITORY
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class KnowledgeEdge:
    """Knowledge Graph Edge"""
    id: UUID = field(default_factory=uuid4)
    source_id: UUID = field(default_factory=uuid4)
    target_id: UUID = field(default_factory=uuid4)
    type: KnowledgeEdgeType = KnowledgeEdgeType.DEPENDS_ON
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class KnowledgeGraph:
    """Complete Knowledge Graph"""
    nodes: List[KnowledgeNode] = field(default_factory=list)
    edges: List[KnowledgeEdge] = field(default_factory=list)
    version: str = "1.0.0"
    updated_at: datetime = field(default_factory=datetime.now)

    def add_node(self, node: KnowledgeNode) -> None:
        """Add a node to the graph"""
        self.nodes.append(node)
        self.updated_at = datetime.now()

    def add_edge(self, edge: KnowledgeEdge) -> None:
        """Add an edge to the graph"""
        self.edges.append(edge)
        self.updated_at = datetime.now()

    def get_nodes_by_type(self, node_type: KnowledgeNodeType) -> List[KnowledgeNode]:
        """Get all nodes of a specific type"""
        return [n for n in self.nodes if n.type == node_type]

    def get_edges_for_node(self, node_id: UUID) -> List[KnowledgeEdge]:
        """Get all edges connected to a node"""
        return [
            e for e in self.edges
            if e.source_id == node_id or e.target_id == node_id
        ]


# ============================================================================
# EXPERIENCE & PLAYBOOKS
# ============================================================================

@dataclass
class Experience:
    """Engineering Experience"""
    id: UUID = field(default_factory=uuid4)
    repository_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)

    problem: Dict[str, Any] = field(default_factory=dict)
    reasoning: Dict[str, Any] = field(default_factory=dict)
    solution: Dict[str, Any] = field(default_factory=dict)
    validation: Dict[str, Any] = field(default_factory=dict)
    outcome: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "repository_id": str(self.repository_id),
            "created_at": self.created_at.isoformat(),
            "problem": self.problem,
            "reasoning": self.reasoning,
            "solution": self.solution,
            "validation": self.validation,
            "outcome": self.outcome
        }

@dataclass
class Playbook:
    """Reusable Execution Playbook"""
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    description: str = ""
    success_rate: float = 0.0
    execution_count: int = 0

    context: Dict[str, Any] = field(default_factory=dict)
    tasks: List[Dict[str, Any]] = field(default_factory=list)
    failures: List[Dict[str, Any]] = field(default_factory=list)
    success_metrics: Dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_used_at: Optional[datetime] = None


# ============================================================================
# TASK & EXECUTION
# ============================================================================

@dataclass
class Task:
    """Task definition"""
    id: UUID = field(default_factory=uuid4)
    parent_id: Optional[UUID] = None
    repository_id: UUID = field(default_factory=uuid4)
    name: str = ""
    description: str = ""
    state: TaskState = TaskState.CREATED

    scope: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[UUID] = field(default_factory=list)
    validation: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    success_criteria: List[str] = field(default_factory=list)

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None

@dataclass
class AgentExecution:
    """Agent Execution record"""
    id: UUID = field(default_factory=uuid4)
    task_id: UUID = field(default_factory=uuid4)
    agent_id: UUID = field(default_factory=uuid4)
    status: AgentExecutionStatus = AgentExecutionStatus.PENDING

    lease: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    result: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class ValidationResult:
    """Validation result"""
    id: UUID = field(default_factory=uuid4)
    execution_id: UUID = field(default_factory=uuid4)
    layers: List[Dict[str, Any]] = field(default_factory=list)
    overall_status: str = "pass"
    confidence: float = 0.0
    report: str = ""
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class RecoveryAttempt:
    """Recovery attempt"""
    id: UUID = field(default_factory=uuid4)
    execution_id: UUID = field(default_factory=uuid4)
    attempt_number: int = 0

    failure: Dict[str, Any] = field(default_factory=dict)
    strategy: Dict[str, Any] = field(default_factory=dict)
    result: Dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(default_factory=datetime.now)
    duration: Optional[float] = None