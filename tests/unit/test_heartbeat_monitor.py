"""
Unit tests for Worker Heartbeat Monitor (PR 2).
"""

import time
import pytest
from ai_se_os.telemetry.heartbeat_monitor import HeartbeatMonitor


@pytest.fixture(autouse=True)
def reset_heartbeat():
    HeartbeatMonitor.clear()
    yield
    HeartbeatMonitor.clear()


def test_send_and_check_heartbeat_alive():
    task_id = "hb-task-1"
    HeartbeatMonitor.send_heartbeat(task_id, stage_name="LLM Reasoning", timeout_sec=10)

    assert HeartbeatMonitor.is_alive(task_id) is True
    assert HeartbeatMonitor.get_stale_tasks() == []


def test_heartbeat_timeout_expiry():
    task_id = "hb-task-2"
    # Send heartbeat with 1 second timeout
    HeartbeatMonitor.send_heartbeat(task_id, stage_name="Tool Execution", timeout_sec=1)

    time.sleep(1.1)

    assert HeartbeatMonitor.is_alive(task_id) is False
    assert task_id in HeartbeatMonitor.get_stale_tasks()


def test_heartbeat_unregister_on_completion():
    task_id = "hb-task-3"
    HeartbeatMonitor.send_heartbeat(task_id, stage_name="Done", timeout_sec=10)
    assert HeartbeatMonitor.is_alive(task_id) is True

    HeartbeatMonitor.unregister(task_id)
    assert HeartbeatMonitor.is_alive(task_id) is False
    assert HeartbeatMonitor.get_stale_tasks() == []
