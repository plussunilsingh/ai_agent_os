"""
AI-SE OS Genome Analyzer
Repository intelligence gathering and genome snapshots
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
import json
import os
import hashlib

from ..core.data_models import (
    GenomeSnapshot,
    ArchitectureDNA,
    DomainDNA,
    BuildDNA,
    SecurityDNA,
    RuntimeDNA,
    TestDNA,
    HealthDNA
)
from ..core.events import Event, EventType, get_event_bus


@dataclass
class RepositoryFingerprint:
    """Deterministic repository fingerprint"""
    git_hash: str = ""
    file_count: int = 0
    language_breakdown: Dict[str, int] = field(default_factory=dict)
    dependency_count: int = 0
    module_count: int = 0
    test_count: int = 0
    total_lines: int = 0
    age_days: int = 0


class GenomeAnalyzer:
    """
    Analyzes repository structure and produces Genome snapshots.
    
    The Genome has 15 DNA dimensions that capture the complete
    engineering state of a repository.
    """

    def __init__(self, storage_dir: Optional[str] = None):
        self._storage_dir = storage_dir
        self._event_bus = get_event_bus()
        self._snapshots: Dict[str, List[GenomeSnapshot]] = {}  # repo_id -> snapshots

    def create_snapshot(
        self,
        repository_id: str,
        git_hash: str,
        fingerprint: Optional[RepositoryFingerprint] = None
    ) -> GenomeSnapshot:
        """
        Create a complete genome snapshot for a repository.
        In a real implementation, this would analyze the actual filesystem.
        """
        snapshot = GenomeSnapshot(
            repository_id=repository_id,
            git_hash=git_hash,
            timestamp=datetime.now(),
            version=self._next_version(repository_id)
        )

        # Populate DNA dimensions
        if fingerprint:
            snapshot.architecture = self._analyze_architecture(fingerprint)
            snapshot.domain = self._analyze_domain(fingerprint)
            snapshot.build = self._analyze_build(fingerprint)
            snapshot.security = self._analyze_security(fingerprint)
            snapshot.runtime = self._analyze_runtime(fingerprint)
            snapshot.test = self._analyze_test(fingerprint)
            snapshot.health = self._analyze_health(fingerprint)

        # Store snapshot
        if repository_id not in self._snapshots:
            self._snapshots[repository_id] = []
        self._snapshots[repository_id].append(snapshot)

        # Persist
        self._persist(snapshot)

        # Publish event
        self._event_bus.publish(Event(
            type=EventType.GENOME_SNAPSHOT_CREATED,
            source="genome_analyzer",
            producer="intelligence",
            payload={
                "repository_id": str(repository_id),
                "snapshot_id": str(snapshot.id),
                "version": snapshot.version,
                "git_hash": git_hash,
                "intelligence_score": snapshot.health.intelligence_score
            }
        ))

        return snapshot

    def _next_version(self, repository_id: str) -> str:
        """Get next version number for a repository"""
        existing = self._snapshots.get(repository_id, [])
        major = len(existing) + 1
        return f"{major}.0.0"

    def _analyze_architecture(self, fp: RepositoryFingerprint) -> ArchitectureDNA:
        """Analyze architecture DNA"""
        return ArchitectureDNA(
            modules=[{"name": f"module_{i}", "path": f"src/{'/' if i else ''}"} for i in range(fp.module_count)],
            dependencies=[],
            layers=["presentation", "business", "data"] if fp.module_count > 2 else [],
            patterns=["layered"] if fp.module_count > 1 else [],
            violations=[],
            drift_score=0.0
        )

    def _analyze_domain(self, fp: RepositoryFingerprint) -> DomainDNA:
        """Analyze domain DNA"""
        return DomainDNA(
            entities=[],
            services=[],
            rules=[],
            events=[]
        )

    def _analyze_build(self, fp: RepositoryFingerprint) -> BuildDNA:
        """Analyze build DNA"""
        # Determine build system from file extensions
        if ".gradle" in str(fp.language_breakdown):
            system = "gradle"
        elif "pom.xml" in str(fp.language_breakdown):
            system = "maven"
        elif "package.json" in str(fp.language_breakdown):
            system = "npm"
        else:
            system = "unknown"

        return BuildDNA(
            system=system,
            dependencies=[],
            tasks=["build", "test", "lint"],
            config={}
        )

    def _analyze_security(self, fp: RepositoryFingerprint) -> SecurityDNA:
        """Analyze security DNA"""
        return SecurityDNA(
            auth={},
            secrets=[],
            policies=[],
            scans=[]
        )

    def _analyze_runtime(self, fp: RepositoryFingerprint) -> RuntimeDNA:
        """Analyze runtime DNA"""
        return RuntimeDNA(
            deployment={},
            environments=["development", "staging", "production"],
            scaling={},
            resources={}
        )

    def _analyze_test(self, fp: RepositoryFingerprint) -> TestDNA:
        """Analyze test DNA"""
        return TestDNA(
            frameworks=[],
            coverage=0.0,
            patterns=[],
            flaky_tests=[]
        )

    def _analyze_health(self, fp: RepositoryFingerprint) -> HealthDNA:
        """Analyze health DNA"""
        # Calculate intelligence score based on metrics
        test_ratio = fp.test_count / max(fp.file_count, 1)
        doc_ratio = 0.0  # Would need documentation analysis

        intelligence_score = (
            min(fp.file_count / 100, 1.0) * 0.3 +
            test_ratio * 0.3 +
            (1.0 if fp.dependency_count > 0 else 0.0) * 0.2 +
            doc_ratio * 0.2
        )

        return HealthDNA(
            build_status="passing",
            test_pass_rate=0.95,
            coverage=0.0,
            security_status="clean",
            confidence=0.8,
            intelligence_score=round(intelligence_score, 2)
        )

    def get_snapshot(
        self,
        repository_id: str,
        version: Optional[str] = None
    ) -> Optional[GenomeSnapshot]:
        """Get a genome snapshot"""
        snapshots = self._snapshots.get(repository_id, [])
        if not snapshots:
            return None

        if version:
            for s in snapshots:
                if s.version == version:
                    return s
            return None

        return snapshots[-1]  # Latest

    def get_snapshot_history(self, repository_id: str) -> List[GenomeSnapshot]:
        """Get all snapshots for a repository"""
        return self._snapshots.get(repository_id, [])

    def compare_snapshots(
        self,
        repository_id: str,
        version_a: str,
        version_b: str
    ) -> Dict[str, Any]:
        """Compare two snapshots and return differences"""
        snap_a = self.get_snapshot(repository_id, version_a)
        snap_b = self.get_snapshot(repository_id, version_b)

        if not snap_a or not snap_b:
            return {"error": "Snapshot not found"}

        return {
            "repository_id": repository_id,
            "version_a": version_a,
            "version_b": version_b,
            "health_change": snap_b.health.intelligence_score - snap_a.health.intelligence_score,
            "architecture_drift": snap_b.architecture.drift_score - snap_a.architecture.drift_score,
            "test_coverage_change": snap_b.test.coverage - snap_a.test.coverage,
            "module_count_change": len(snap_b.architecture.modules) - len(snap_a.architecture.modules),
            "dependency_count_change": len(snap_b.build.dependencies) - len(snap_a.build.dependencies)
        }

    def get_intelligence_score(self, repository_id: str) -> float:
        """Get current intelligence score for a repository"""
        snapshot = self.get_snapshot(repository_id)
        if not snapshot:
            return 0.0
        return snapshot.health.intelligence_score

    def _persist(self, snapshot: GenomeSnapshot) -> None:
        """Persist snapshot to disk"""
        if not self._storage_dir:
            return

        os.makedirs(self._storage_dir, exist_ok=True)
        repo_dir = os.path.join(self._storage_dir, str(snapshot.repository_id))
        os.makedirs(repo_dir, exist_ok=True)

        filepath = os.path.join(repo_dir, f"snapshot_{snapshot.version}.json")
        try:
            with open(filepath, "w") as f:
                json.dump(snapshot.to_dict(), f, indent=2)
        except Exception as e:
            print(f"Error persisting snapshot: {e}")

    def get_insights(self, repository_id: str) -> Dict[str, Any]:
        """Get insights about a repository"""
        snapshot = self.get_snapshot(repository_id)
        if not snapshot:
            return {"error": "No snapshot available"}

        return {
            "intelligence_score": snapshot.health.intelligence_score,
            "health_status": snapshot.health.build_status,
            "test_pass_rate": snapshot.health.test_pass_rate,
            "security_status": snapshot.health.security_status,
            "architecture_layers": snapshot.architecture.layers,
            "architecture_patterns": snapshot.architecture.patterns,
            "architecture_drift": snapshot.architecture.drift_score,
            "module_count": len(snapshot.architecture.modules),
            "dependency_count": len(snapshot.build.dependencies),
            "enforcement_policies": snapshot.security.policies
        }