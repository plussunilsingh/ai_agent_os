"""
AI-SE OS Plugin Base
Abstract base class for all plugins
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PluginMetadata:
    """Plugin metadata"""
    name: str = ""
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    requires: List[str] = field(default_factory=list)
    hooks: List[str] = field(default_factory=list)


class BasePlugin(ABC):
    """
    Abstract base class for AI-SE OS plugins.
    
    Plugins can hook into:
    - on_repository_analyze: After repository analysis
    - on_plan_generate: After plan generation
    - on_execution_complete: After execution completes
    - on_validation: During validation
    - on_event: On any system event
    """

    def __init__(self):
        self.metadata = PluginMetadata()
        self._initialized = False

    @abstractmethod
    def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize the plugin with system context"""
        pass

    @abstractmethod
    def shutdown(self) -> bool:
        """Shutdown the plugin"""
        pass

    def on_repository_analyze(self, repository_id: str, genome: Dict[str, Any]) -> Dict[str, Any]:
        """Hook: After repository analysis"""
        return {}

    def on_plan_generate(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Hook: After plan generation"""
        return {}

    def on_execution_complete(self, execution: Dict[str, Any]) -> None:
        """Hook: After execution completes"""
        pass

    def on_validation(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Hook: During validation"""
        return {}

    def on_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Hook: On any system event"""
        pass

    def get_info(self) -> Dict[str, Any]:
        """Get plugin information"""
        return {
            "name": self.metadata.name,
            "version": self.metadata.version,
            "description": self.metadata.description,
            "author": self.metadata.author,
            "initialized": self._initialized,
            "hooks": self.metadata.hooks
        }