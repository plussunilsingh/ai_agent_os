"""
AI-SE OS Evolution Engine
Tracks repository changes and evolution over time
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ChangeType(str, Enum):
    ADD = "add"
    MODIFY = "modify"
    DELETE = "delete"
    RENAME = "rename"


@dataclass
class Change:
    """A single repository change"""
    type: ChangeType
    file: str
    timestamp: datetime = field(default_factory=datetime.now)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvolutionResult:
    """Evolution analysis result"""
    changes: List[Change] = field(default_factory=list)
    total_changes: int = 0
    additions: int = 0
    modifications: int = 0
    deletions: int = 0


class EvolutionEngine:
    """Tracks repository evolution and changes"""
    
    def __init__(self):
        self._history: Dict[str, List[Change]] = {}
    
    def track_evolution(self, genome: Any, repo_path: str) -> EvolutionResult:
        """Track evolution since last genome"""
        repo_id = getattr(genome, 'repository_id', 'default')
        
        # Simulate change detection
        changes = self._detect_changes(repo_path)
        
        result = EvolutionResult(
            changes=changes,
            total_changes=len(changes),
            additions=sum(1 for c in changes if c.type == ChangeType.ADD),
            modifications=sum(1 for c in changes if c.type == ChangeType.MODIFY),
            deletions=sum(1 for c in changes if c.type == ChangeType.DELETE)
        )
        
        # Store changes
        if repo_id not in self._history:
            self._history[repo_id] = []
        self._history[repo_id].extend(changes)
        
        return result
    
    def _detect_changes(self, repo_path: str) -> List[Change]:
        """Detect changes in repository"""
        # Simplified change detection
        import os
        changes = []
        
        if os.path.exists(repo_path):
            for root, dirs, files in os.walk(repo_path):
                for file in files:
                    if file.endswith('.py'):
                        full_path = os.path.join(root, file)
                        # Simulate detecting a modification
                        changes.append(Change(
                            type=ChangeType.MODIFY,
                            file=full_path.replace(repo_path, '').lstrip('/')
                        ))
        
        return changes