"""
AI-SE OS Plugin Manager
Discovers, loads, and manages plugins
"""

from typing import Dict, Any, Optional, List
import importlib
import inspect
import os
import sys
import logging

from .base import BasePlugin

logger = logging.getLogger(__name__)


class PluginManager:
    """
    Manages the lifecycle of AI-SE OS plugins.
    
    Handles:
    - Plugin discovery from directories
    - Loading and initialization
    - Hook dispatch
    - Shutdown
    """

    def __init__(self, plugin_dirs: Optional[List[str]] = None):
        self._plugins: Dict[str, BasePlugin] = {}
        self._plugin_dirs = plugin_dirs or []
        self._initialized = False

    def discover_plugins(self, directory: Optional[str] = None) -> List[str]:
        """
        Discover plugins in a directory.
        
        Args:
            directory: Directory to scan for plugins
            
        Returns:
            List of discovered plugin names
        """
        if directory and directory not in self._plugin_dirs:
            self._plugin_dirs.append(directory)

        discovered = []
        for plugin_dir in self._plugin_dirs:
            if not os.path.exists(plugin_dir):
                continue

            sys.path.insert(0, os.path.dirname(plugin_dir))

            for filename in os.listdir(plugin_dir):
                if filename.endswith(".py") and not filename.startswith("_"):
                    module_name = filename[:-3]
                    try:
                        module = importlib.import_module(module_name)
                        for name, obj in inspect.getmembers(module):
                            if (inspect.isclass(obj) and
                                issubclass(obj, BasePlugin) and
                                obj != BasePlugin):
                                plugin = obj()
                                self._plugins[plugin.metadata.name] = plugin
                                discovered.append(plugin.metadata.name)
                    except Exception as e:
                        logger.error(f"Failed to load plugin {module_name}: {e}")

        return discovered

    def register_plugin(self, plugin: BasePlugin) -> str:
        """Register a plugin instance"""
        self._plugins[plugin.metadata.name] = plugin
        return plugin.metadata.name

    def initialize_all(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, bool]:
        """Initialize all registered plugins"""
        results = {}
        for name, plugin in self._plugins.items():
            try:
                success = plugin.initialize(context or {})
                results[name] = success
                if success:
                    logger.info(f"Plugin '{name}' initialized successfully")
                else:
                    logger.warning(f"Plugin '{name}' failed to initialize")
            except Exception as e:
                results[name] = False
                logger.error(f"Plugin '{name}' initialization error: {e}")

        self._initialized = all(results.values())
        return results

    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Get a plugin by name"""
        return self._plugins.get(name)

    def get_all_plugins(self) -> Dict[str, BasePlugin]:
        """Get all registered plugins"""
        return dict(self._plugins)

    def dispatch_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Dispatch an event to all plugins"""
        for plugin in self._plugins.values():
            try:
                plugin.on_event(event_type, payload)
            except Exception as e:
                logger.error(f"Plugin '{plugin.metadata.name}' event handler error: {e}")

    def dispatch_repository_analyze(self, repository_id: str, genome: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch repository analyze hook"""
        results = {}
        for plugin in self._plugins.values():
            try:
                result = plugin.on_repository_analyze(repository_id, genome)
                if result:
                    results[plugin.metadata.name] = result
            except Exception as e:
                logger.error(f"Plugin '{plugin.metadata.name}' analyze error: {e}")
        return results

    def dispatch_plan_generate(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch plan generate hook"""
        results = {}
        for plugin in self._plugins.values():
            try:
                result = plugin.on_plan_generate(plan)
                if result:
                    results[plugin.metadata.name] = result
            except Exception as e:
                logger.error(f"Plugin '{plugin.metadata.name}' plan error: {e}")
        return results

    def dispatch_validation(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch validation hook"""
        results = {}
        for plugin in self._plugins.values():
            try:
                result = plugin.on_validation(report)
                if result:
                    results[plugin.metadata.name] = result
            except Exception as e:
                logger.error(f"Plugin '{plugin.metadata.name}' validation error: {e}")
        return results

    def shutdown_all(self) -> Dict[str, bool]:
        """Shutdown all plugins"""
        results = {}
        for name, plugin in self._plugins.items():
            try:
                success = plugin.shutdown()
                results[name] = success
            except Exception as e:
                results[name] = False
                logger.error(f"Plugin '{name}' shutdown error: {e}")
        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get plugin manager statistics"""
        return {
            "total_plugins": len(self._plugins),
            "initialized": self._initialized,
            "plugins": {
                name: plugin.get_info()
                for name, plugin in self._plugins.items()
            }
        }