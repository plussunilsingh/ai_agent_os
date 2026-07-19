"""
AI-SE OS Core Data Models - Complete
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from uuid import UUID, uuid4

# ============================================================
# ENUMS
# ============================================================

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
    SERVICE = "service"
    OWNER = "owner"
    TEAM = "team"
    POLICY = "policy"
    LIBRARY = "library"
    FRAMEWORK = "framework"

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

# ============================================================
# CORE MODELS
# ============================================================

@dataclass
class Repository:
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
class Class:
    name: str
    package: str = ""
    type: str = "class"
    methods: List[Dict[str, str]] = field(default_factory=list)
    fields: List[Dict[str, str]] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    extends: Optional[str] = None
    implements: List[str] = field(default_factory=list)

@dataclass
class Method:
    name: str
    return_type: str = "void"
    parameters: List[Dict[str, str]] = field(default_factory=list)
    modifiers: List[str] = field(default_factory=list)
    doc: str = ""

@dataclass
class Dependency:
    source: str
    target: str
    type: str = "import"
    version: Optional[str] = None
    optional: bool = False

# ============================================================
# PLANNING MODELS
# ============================================================

@dataclass
class Plan:
    id: str = ""
    tasks: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class Task:
    id: str
    name: str
    description: str
    state: TaskState = TaskState.CREATED
    scope: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    success_criteria: List[str] = field(default_factory=list)

@dataclass
class TaskResult:
    task_id: str
    status: str
    output: str = ""
    error: Optional[str] = None
    duration: float = 0.0

@dataclass
class ExecutionPlan:
    id: str
    plan: Plan
    status: str = "pending"
    results: List[TaskResult] = field(default_factory=list)

# ============================================================
# KNOWLEDGE GRAPH MODELS
# ============================================================

@dataclass
class KnowledgeNode:
    id: UUID = field(default_factory=uuid4)
    type: KnowledgeNodeType = KnowledgeNodeType.REPOSITORY
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class KnowledgeEdge:
    id: UUID = field(default_factory=uuid4)
    source_id: UUID = field(default_factory=uuid4)
    target_id: UUID = field(default_factory=uuid4)
    type: KnowledgeEdgeType = KnowledgeEdgeType.DEPENDS_ON
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class KnowledgeGraph:
    version: str = "1.0.0"
    nodes: Dict[UUID, KnowledgeNode] = field(default_factory=dict)
    edges: List[KnowledgeEdge] = field(default_factory=list)
    updated_at: datetime = field(default_factory=datetime.now)

    def add_node(self, node: KnowledgeNode) -> None:
        self.nodes[node.id] = node
        self.updated_at = datetime.now()

    def add_edge(self, edge: KnowledgeEdge) -> None:
        self.edges.append(edge)
        self.updated_at = datetime.now()

    def get_edges_for_node(self, node_id: UUID) -> List[KnowledgeEdge]:
        return [e for e in self.edges if e.source_id == node_id or e.target_id == node_id]

# ============================================================
# GENOME MODELS
# ============================================================

@dataclass
class GenomeSnapshot:
    id: UUID = field(default_factory=uuid4)
    repository_id: UUID = field(default_factory=uuid4)
    version: str = "1.0.0"
    git_hash: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    created_by: Optional[UUID] = None
    architecture: Dict[str, Any] = field(default_factory=dict)
    domain: Dict[str, Any] = field(default_factory=dict)
    build: Dict[str, Any] = field(default_factory=dict)
@dataclass
class ArchitectureDNA:
    modules: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[Dict[str, Any]] = field(default_factory=list)
    layers: List[str] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)
    violations: List[Dict[str, Any]] = field(default_factory=list)
    drift_score: float = 0.0

@dataclass
class DomainDNA:
    entities: List[Dict[str, Any]] = field(default_factory=list)
    services: List[Dict[str, Any]] = field(default_factory=list)
    rules: List[Dict[str, Any]] = field(default_factory=list)
    events: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class BuildDNA:
    system: str = "unknown"
    dependencies: List[Dict[str, Any]] = field(default_factory=list)
    tasks: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SecurityDNA:
    auth: Dict[str, Any] = field(default_factory=dict)
    secrets: List[str] = field(default_factory=list)
    policies: List[Dict[str, Any]] = field(default_factory=list)
    scans: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class RuntimeDNA:
    deployment: Dict[str, Any] = field(default_factory=dict)
    environments: List[str] = field(default_factory=list)
    scaling: Dict[str, Any] = field(default_factory=dict)
    resources: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TestDNA:
    frameworks: List[str] = field(default_factory=list)
    coverage: float = 0.0
    patterns: List[str] = field(default_factory=list)
    flaky_tests: List[str] = field(default_factory=list)

@dataclass
class HealthDNA:
    build_status: str = "passing"
    test_pass_rate: float = 1.0
    coverage: float = 0.0
    security_status: str = "clean"
    confidence: float = 1.0
    intelligence_score: float = 0.0

@dataclass
class GenomeSnapshot:
    id: UUID = field(default_factory=uuid4)
    repository_id: UUID = field(default_factory=uuid4)
    version: str = "1.0.0"
    git_hash: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    created_by: Optional[UUID] = None
    architecture: ArchitectureDNA = field(default_factory=ArchitectureDNA)
    domain: DomainDNA = field(default_factory=DomainDNA)
    build: BuildDNA = field(default_factory=BuildDNA)
    security: SecurityDNA = field(default_factory=SecurityDNA)
    runtime: RuntimeDNA = field(default_factory=RuntimeDNA)
    test: TestDNA = field(default_factory=TestDNA)
    health: HealthDNA = field(default_factory=HealthDNA)
    intelligence_score: float = 0.0

# ============================================================
# EXPERIENCE MODELS
# ============================================================

@dataclass
class Experience:
    id: str = ""
    problem: str = ""
    solution: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    outcome: str = ""
    confidence: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)

# ============================================================
# CHANGE & EVOLUTION MODELS
# ============================================================

@dataclass
class Change:
    id: str
    type: str
    file_path: str
    description: str
    author: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Evolution:
    id: str
    repository_id: str
    changes: List[Change]
    version: str
    created_at: datetime = field(default_factory=datetime.now)

# ============================================================
# VALIDATION MODELS
# ============================================================

@dataclass
class ValidationResult:
    id: str = ""
    execution_id: str = ""
    status: str = "pass"
    layers: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    report: str = ""
    created_at: datetime = field(default_factory=datetime.now)

# ============================================================
# ADR MODELS
# ============================================================

@dataclass
class ADR:
    id: str
    title: str
    status: str = "proposed"
    context: str = ""
    decision: str = ""
    consequences: str = ""
    alternatives: List[Dict[str, Any]] = field(default_factory=list)
    date: datetime = field(default_factory=datetime.now)
    author: str = ""
