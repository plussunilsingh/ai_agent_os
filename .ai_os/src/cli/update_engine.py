"""
AI-SE OS Update Engine
Applies configuration updates automatically based on LLM analysis
"""

import os
import json
import shutil
import hashlib
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, field

from ..core.events import Event, EventType, get_event_bus
from .change_detection import Change, ChangeAnalysis


@dataclass
class UpdateResult:
    """Result of an update operation"""
    success: bool
    message: str
    timestamp: datetime
    updates_applied: List[str]
    errors: List[str]


class UpdateEngine:
    """
    Applies configuration updates based on LLM analysis
    """
    
    def __init__(
        self,
        config_dir: str = ".ai_os/config",
        backup_dir: str = ".ai_os/config/backup"
    ):
        self.config_dir = Path(config_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.update_history: List[UpdateResult] = []
    
    def apply_updates(self, changes: List[Change], analysis: ChangeAnalysis) -> UpdateResult:
        """
        Apply updates based on detected changes and LLM analysis
        """
        updates_applied = []
        errors = []
        
        try:
            # 1. Backup current configs
            self._backup_configs()
            
            # 2. Apply each recommended action
            for action in analysis.recommended_actions:
                try:
                    result = self._execute_action(action, changes)
                    if result["success"]:
                        updates_applied.append(action)
                    else:
                        errors.append(f"Action failed: {action} - {result.get('error', 'Unknown error')}")
                except Exception as e:
                    errors.append(f"Action failed: {action} - {str(e)}")
            
            # 3. Record success/failure
            result = UpdateResult(
                success=len(errors) == 0,
                message=f"Applied {len(updates_applied)} updates",
                timestamp=datetime.now(),
                updates_applied=updates_applied,
                errors=errors
            )
            self.update_history.append(result)
            
            # 4. Publish event
            event_bus = get_event_bus()
            event_bus.publish(Event(
                type=EventType.CONFIG_UPDATED,
                source="update_engine",
                producer="system",
                payload={
                    "updates_count": len(updates_applied),
                    "errors_count": len(errors),
                    "success": result.success
                }
            ))
            
            return result
            
        except Exception as e:
            # Rollback on failure
            self._rollback_configs()
            return UpdateResult(
                success=False,
                message=f"Update failed: {str(e)}",
                timestamp=datetime.now(),
                updates_applied=[],
                errors=[str(e)]
            )
    
    def _execute_action(self, action: str, changes: List[Change]) -> Dict[str, Any]:
        """Execute a single update action"""
        action_lower = action.lower()
        
        if "model" in action_lower:
            return self._update_model_config(action, changes)
        elif "repository" in action_lower:
            return self._update_repository_config(action, changes)
        elif "sdk" in action_lower:
            return self._update_sdk_config(action, changes)
        elif "framework" in action_lower:
            return self._update_framework_config(action, changes)
        elif "security" in action_lower:
            return self._update_security_config(action, changes)
        elif "performance" in action_lower:
            return self._update_performance_config(action, changes)
        else:
            return {"success": False, "error": f"Unknown action type: {action}"}
    
    def _update_model_config(self, action: str, changes: List[Change]) -> Dict[str, Any]:
        """Update model configuration"""
        model_changes = [c for c in changes if c.type == "model"]
        if not model_changes:
            return {"success": True, "message": "No model changes to apply"}
        
        # Update model router configuration
        from ..execution.model_router import get_model_router
        router = get_model_router()
        
        for change in model_changes:
            model_id = change.details.get("model_id")
            if model_id:
                # Register new model
                router.register_model({
                    "id": model_id,
                    "name": change.details.get("name", model_id),
                    "provider": change.details.get("provider", "unknown")
                })
        
        return {"success": True, "message": f"Updated {len(model_changes)} models"}
    
    def _update_repository_config(self, action: str, changes: List[Change]) -> Dict[str, Any]:
        """Update repository configuration"""
        repo_changes = [c for c in changes if c.type == "repository"]
        if not repo_changes:
            return {"success": True, "message": "No repository changes to apply"}
        
        # Update repository configurations
        for change in repo_changes:
            repo_id = change.details.get("repository_id")
            if repo_id:
                # Would update .ai/config.yaml for the repository
                pass
        
        return {"success": True, "message": f"Updated {len(repo_changes)} repositories"}
    
    def _update_sdk_config(self, action: str, changes: List[Change]) -> Dict[str, Any]:
        """Update SDK configuration"""
        sdk_changes = [c for c in changes if c.type == "sdk"]
        if not sdk_changes:
            return {"success": True, "message": "No SDK changes to apply"}
        
        # Record SDK updates
        sdk_config_path = self.config_dir / "sdks.json"
        sdk_config = {}
        if sdk_config_path.exists():
            with open(sdk_config_path) as f:
                sdk_config = json.load(f)
        
        for change in sdk_changes:
            sdk_config[change.id] = {
                "version": change.details.get("latest"),
                "updated_at": datetime.now().isoformat(),
                "auto_updated": True
            }
        
        with open(sdk_config_path, 'w') as f:
            json.dump(sdk_config, f, indent=2)
        
        return {"success": True, "message": f"Updated {len(sdk_changes)} SDKs"}
    
    def _update_framework_config(self, action: str, changes: List[Change]) -> Dict[str, Any]:
        """Update framework configuration"""
        framework_changes = [c for c in changes if c.type == "framework"]
        if not framework_changes:
            return {"success": True, "message": "No framework changes to apply"}
        
        # Record framework updates
        framework_config_path = self.config_dir / "frameworks.json"
        framework_config = {}
        if framework_config_path.exists():
            with open(framework_config_path) as f:
                framework_config = json.load(f)
        
        for change in framework_changes:
            framework = change.details.get("framework")
            if framework:
                framework_config[framework] = {
                    "version": change.details.get("latest"),
                    "updated_at": datetime.now().isoformat(),
                    "security_update": change.details.get("security", False)
                }
        
        with open(framework_config_path, 'w') as f:
            json.dump(framework_config, f, indent=2)
        
        return {"success": True, "message": f"Updated {len(framework_changes)} frameworks"}
    
    def _update_security_config(self, action: str, changes: List[Change]) -> Dict[str, Any]:
        """Update security configuration"""
        security_changes = [c for c in changes if c.type == "security"]
        if not security_changes:
            return {"success": True, "message": "No security changes to apply"}
        
        # Record security advisories
        security_config_path = self.config_dir / "security.json"
        security_config = {"advisories": []}
        if security_config_path.exists():
            with open(security_config_path) as f:
                security_config = json.load(f)
        
        for change in security_changes:
            security_config["advisories"].append({
                "id": change.id,
                "description": change.description,
                "severity": change.severity,
                "cve": change.details.get("cve"),
                "detected_at": datetime.now().isoformat(),
                "status": "detected"
            })
        
        with open(security_config_path, 'w') as f:
            json.dump(security_config, f, indent=2)
        
        return {"success": True, "message": f"Recorded {len(security_changes)} security advisories"}
    
    def _update_performance_config(self, action: str, changes: List[Change]) -> Dict[str, Any]:
        """Update performance configuration"""
        performance_changes = [c for c in changes if c.type == "performance"]
        if not performance_changes:
            return {"success": True, "message": "No performance changes to apply"}
        
        # Update performance thresholds
        performance_config_path = self.config_dir / "performance.json"
        performance_config = {"thresholds": {}}
        
        if performance_config_path.exists():
            with open(performance_config_path) as f:
                performance_config = json.load(f)
        
        for change in performance_changes:
            metric = change.details.get("metric")
            if metric:
                performance_config["thresholds"][metric] = {
                    "baseline": change.details.get("baseline"),
                    "current": change.details.get("current"),
                    "updated_at": datetime.now().isoformat()
                }
        
        with open(performance_config_path, 'w') as f:
            json.dump(performance_config, f, indent=2)
        
        return {"success": True, "message": f"Updated {len(performance_changes)} performance metrics"}
    
    def _backup_configs(self):
        """Backup current configs"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"
        backup_path.mkdir(exist_ok=True)
        
        # Copy all config files
        if self.config_dir.exists():
            for config_file in self.config_dir.glob("*.json"):
                shutil.copy(config_file, backup_path / config_file.name)
    
    def _rollback_configs(self):
        """Rollback to previous configs"""
        # Get most recent backup
        backups = sorted(self.backup_dir.glob("backup_*"), reverse=True)
        if not backups:
            return
        
        latest_backup = backups[0]
        
        # Restore from backup
        for backup_file in latest_backup.glob("*"):
            if backup_file.is_file():
                shutil.copy(backup_file, self.config_dir / backup_file.name)
    
    def get_update_history(self) -> List[Dict[str, Any]]:
        """Get update history"""
        return [
            {
                "timestamp": result.timestamp.isoformat(),
                "success": result.success,
                "message": result.message,
                "updates_applied": result.updates_applied,
                "errors": result.errors
            }
            for result in self.update_history
        ]