"""
AI-SE OS Change Detection Service
Proactively detects changes and asks LLM for analysis
"""

import asyncio
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from ..core.data_models import GenomeSnapshot
from ..execution.model_router import ModelRouter


@dataclass
class Change:
    """Detected change"""
    id: str
    type: str  # model, repository, sdk, framework, dependency, security, performance
    description: str
    severity: str  # critical, high, medium, low
    timestamp: datetime = field(default_factory=datetime.now)
    details: Dict[str, Any] = field(default_factory=dict)
    affected_components: List[str] = field(default_factory=list)


@dataclass
class ChangeAnalysis:
    """LLM analysis of changes"""
    changes_detected: bool
    analysis: str
    recommended_actions: List[str]
    confidence: float
    requires_approval: bool
    auto_apply: bool


class ChangeDetectionService:
    """
    Detects changes in the environment and asks LLM for analysis
    """
    
    def __init__(self, model_router: Optional[ModelRouter] = None):
        self.model_router = model_router or ModelRouter()
        self.last_check = datetime.now()
        self.detected_changes: List[Change] = []
        self.config_hashes: Dict[str, str] = {}
    
    def check_for_changes(self) -> List[Change]:
        """Check all sources for changes"""
        changes = []
        
        # Check various sources
        changes.extend(self._check_model_changes())
        changes.extend(self._check_repository_changes())
        changes.extend(self._check_sdk_versions())
        changes.extend(self._check_framework_updates())
        changes.extend(self._check_security_updates())
        changes.extend(self._check_performance_degradation())
        
        self.detected_changes.extend(changes)
        self.last_check = datetime.now()
        
        return changes
    
    def ask_llm_for_analysis(self, changes: List[Change]) -> ChangeAnalysis:
        """Ask the LLM to analyze detected changes and recommend actions"""
        if not changes:
            return ChangeAnalysis(
                changes_detected=False,
                analysis="No changes detected",
                recommended_actions=[],
                confidence=1.0,
                requires_approval=False,
                auto_apply=False
            )
        
        # Build prompt for LLM
        prompt = self._build_analysis_prompt(changes)
        
        # Send to LLM via model router
        try:
            response = self.model_router.route_and_generate(
                prompt=prompt,
                task_type="analysis"
            )
            return self._parse_llm_response(response)
        except Exception as e:
            # Fallback: conservative analysis
            return ChangeAnalysis(
                changes_detected=True,
                analysis=f"Detected {len(changes)} changes. Manual review recommended.",
                recommended_actions=["Review changes and update configurations"],
                confidence=0.7,
                requires_approval=True,
                auto_apply=False
            )
    
    def _build_analysis_prompt(self, changes: List[Change]) -> str:
        """Build prompt for LLM analysis"""
        changes_json = json.dumps([
            {
                "type": c.type,
                "description": c.description,
                "severity": c.severity,
                "details": c.details
            }
            for c in changes[:10]  # Limit to top 10 changes
        ], indent=2)
        
        return f"""
You are analyzing changes detected by the AI-SE OS system.

Detected Changes:
{changes_json}

Please analyze these changes and provide:
1. What is the overall impact of these changes?
2. Which changes are critical and need immediate attention?
3. What actions should be taken to address these changes?
4. Should any changes be auto-applied vs require manual approval?

Provide your response in JSON format:
{{
    "changes_detected": true,
    "analysis": "Overall impact analysis",
    "recommended_actions": ["Action 1", "Action 2"],
    "confidence": 0.95,
    "requires_approval": true,
    "auto_apply": false,
    "critical_changes": ["change_id_1"]
}}
"""
    
    def _parse_llm_response(self, response: str) -> ChangeAnalysis:
        """Parse LLM response"""
        try:
            # Try to extract JSON from response
            data = json.loads(response)
            return ChangeAnalysis(
                changes_detected=data.get("changes_detected", True),
                analysis=data.get("analysis", ""),
                recommended_actions=data.get("recommended_actions", []),
                confidence=data.get("confidence", 0.8),
                requires_approval=data.get("requires_approval", True),
                auto_apply=data.get("auto_apply", False)
            )
        except (json.JSONDecodeError, AttributeError):
            return ChangeAnalysis(
                changes_detected=True,
                analysis=response[:200] if response else "No analysis available",
                recommended_actions=["Review changes manually"],
                confidence=0.6,
                requires_approval=True,
                auto_apply=False
            )
    
    def _check_model_changes(self) -> List[Change]:
        """Check for new or updated LLM models"""
        changes = []
        try:
            available_models = self.model_router.get_available_models()
            known_models = self._get_known_models()
            
            for model_info in available_models:
                model_id = model_info.get("id") if isinstance(model_info, dict) else getattr(model_info, 'id', str(model_info))
                if model_id not in known_models:
                    changes.append(Change(
                        id=f"model-new-{model_id}",
                        type="model",
                        description=f"New model available: {model_id}",
                        severity="medium",
                        details={"model_id": model_id},
                        affected_components=["model_router"]
                    ))
        except Exception:
            pass
        return changes
    
    def _check_repository_changes(self) -> List[Change]:
        """Check for repository changes"""
        changes = []
        # Would check registered repositories for git changes
        # Simplified for now
        return changes
    
    def _check_sdk_versions(self) -> List[Change]:
        """Check for SDK version updates"""
        changes = []
        # Would check PyPI, npm, Maven for updates
        # Simplified for now
        return changes
    
    def _check_framework_updates(self) -> List[Change]:
        """Check for framework updates"""
        changes = []
        # Would check framework changelogs
        return changes
    
    def _check_security_updates(self) -> List[Change]:
        """Check for security updates"""
        changes = []
        # Would check security advisories
        return changes
    
    def _check_performance_degradation(self) -> List[Change]:
        """Check for performance degradation"""
        changes = []
        # Would check performance metrics
        return changes
    
    def _get_known_models(self) -> List[str]:
        """Get list of known models"""
        # In real implementation, would load from config
        return ["deepseek-v4-pro", "deepseek-v4-flash", "claude-3.5-sonnet"]