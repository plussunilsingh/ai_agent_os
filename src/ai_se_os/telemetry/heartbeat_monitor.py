"""
AI-SE OS Worker Heartbeat Protocol & Monitor (PR 2)
Tracks worker heartbeats, stage-specific timeouts, and identifies dead/stale worker processes.
"""

import logging
import threading
import time
from typing import Dict, Any, List, Optional

logger = logging.getLogger("HeartbeatMonitor")


class WorkerHeartbeat:
    """Active worker heartbeat entry."""
    def __init__(self, task_id: str, stage_name: str, timeout_sec: int = 45, metadata: Optional[Dict[str, Any]] = None):
        self.task_id = task_id
        self.stage_name = stage_name
        self.timeout_sec = timeout_sec
        self.last_seen_epoch = time.time()
        self.last_seen_time = time.strftime("%H:%M:%S IST")
        self.metadata = metadata or {}


class HeartbeatMonitor:
    """
    Centralized Worker Heartbeat Monitor.
    Workers emit heartbeats during execution; the monitor checks for expired heartbeats.
    """
    _lock = threading.RLock()
    _heartbeats: Dict[str, WorkerHeartbeat] = {}

    @classmethod
    def send_heartbeat(
        cls,
        task_id: str,
        stage_name: str = "Executing",
        timeout_sec: int = 45,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Record or update worker heartbeat for a task."""
        with cls._lock:
            hb = WorkerHeartbeat(
                task_id=task_id,
                stage_name=stage_name,
                timeout_sec=timeout_sec,
                metadata=metadata
            )
            cls._heartbeats[task_id] = hb
            logger.debug(f"[Heartbeat] Task '{task_id}' [{stage_name}] heartbeat received (timeout={timeout_sec}s)")

    @classmethod
    def is_alive(cls, task_id: str) -> bool:
        """Check if worker for task_id is alive (last_seen within stage timeout)."""
        with cls._lock:
            hb = cls._heartbeats.get(task_id)
            if not hb:
                return False
            elapsed = time.time() - hb.last_seen_epoch
            return elapsed <= hb.timeout_sec

    @classmethod
    def get_stale_tasks(cls) -> List[str]:
        """Return list of task_ids whose heartbeats have expired."""
        with cls._lock:
            stale = []
            now_ts = time.time()
            for task_id, hb in cls._heartbeats.items():
                if now_ts - hb.last_seen_epoch > hb.timeout_sec:
                    stale.append(task_id)
            return stale

    @classmethod
    def unregister(cls, task_id: str):
        """Remove task from heartbeat tracking upon task completion."""
        with cls._lock:
            cls._heartbeats.pop(task_id, None)

    @classmethod
    def clear(cls):
        """Reset heartbeat tracking (used in testing)."""
        with cls._lock:
            cls._heartbeats.clear()
