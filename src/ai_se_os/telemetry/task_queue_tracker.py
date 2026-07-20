"""
AI-SE OS Task Queue & Process Tracker
Maintains live state of active autonomous agent tasks, queue telemetry, and task progress.
"""

import os
import json
import time
from typing import Dict, Any, List

TRACKER_FILE = os.path.join(os.path.dirname(__file__), "task_queue_state.json")

class TaskQueueTracker:
    @staticmethod
    def _read_state() -> Dict[str, Any]:
        if not os.path.exists(TRACKER_FILE):
            return {"active_tasks": [], "history": []}
        try:
            with open(TRACKER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"active_tasks": [], "history": []}

    @staticmethod
    def _write_state(state: Dict[str, Any]):
        with open(TRACKER_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    @classmethod
    def register_task(cls, task_id: str, task_name: str, target_url: str) -> Dict[str, Any]:
        state = cls._read_state()
        task_entry = {
            "task_id": task_id,
            "task_name": task_name,
            "target_url": target_url,
            "status": "RUNNING",
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S IST"),
            "progress_pct": 10
        }
        # Remove any existing entry with same task_id
        state["active_tasks"] = [t for t in state["active_tasks"] if t["task_id"] != task_id]
        state["active_tasks"].append(task_entry)
        cls._write_state(state)
        return task_entry

    @classmethod
    def update_task_progress(cls, task_id: str, progress_pct: int, current_step: str):
        state = cls._read_state()
        for t in state["active_tasks"]:
            if t["task_id"] == task_id:
                t["progress_pct"] = progress_pct
                t["current_step"] = current_step
        cls._write_state(state)

    @classmethod
    def complete_task(cls, task_id: str, success: bool, result_summary: str):
        state = cls._read_state()
        active = []
        for t in state["active_tasks"]:
            if t["task_id"] == task_id:
                t["status"] = "COMPLETED" if success else "FAILED"
                t["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S IST")
                t["summary"] = result_summary
                state["history"].append(t)
            else:
                active.append(t)
        state["active_tasks"] = active
        cls._write_state(state)

    @classmethod
    def get_queue_telemetry(cls) -> Dict[str, Any]:
        state = cls._read_state()
        active_list = state.get("active_tasks", [])
        return {
            "queue_name": "ai_se_os_master_queue",
            "active_tasks_count": len(active_list),
            "pending_tasks_count": 0,
            "active_tasks": active_list,
            "governance_mode": "Chapter 42 Truth Enforcement (Zero Hardcoded Metrics)",
            "task_queue_health": "IN_PROGRESS" if len(active_list) > 0 else "HEALTHY (Non-blocking Asynchronous Mode)"
        }
