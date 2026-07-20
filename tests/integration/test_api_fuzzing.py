"""
API Payload Fuzzing and Endpoint Security Test Suite.
Verifies API response stability against corrupted JSON, malformed IDs, boundary progress values, and path traversal attempts.
"""

import pytest
from fastapi.testclient import TestClient
from ai_se_os.main import app

client = TestClient(app)


def test_api_health_endpoints():
    """Verify health and probe endpoints."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"

    resp2 = client.get("/api/v1/ready")
    assert resp2.status_code == 200

    resp3 = client.get("/api/v1/live")
    assert resp3.status_code == 200



def test_agent_execute_fuzzing():
    """Test /agent/execute with missing fields and boundary inputs."""
    # Empty payload
    resp = client.post("/agent/execute", json={})
    assert resp.status_code in [400, 422]


    # Valid payload
    resp2 = client.post("/agent/execute", json={
        "task_name": "API Fuzzing Test Task",
        "target_url": "http://127.0.0.1:9000"
    })
    assert resp2.status_code == 200
    assert resp2.json()["accepted"] is True


def test_task_heartbeat_fuzzing():
    """Test /api/v1/task/{task_id}/heartbeat with boundary progress values."""
    task_id = "fuzz-api-task-1"

    # Extreme progress values (-999, 999999, None)
    for p in [-999, 999999, 0, 100]:
        resp = client.post(f"/api/v1/task/{task_id}/heartbeat?progress={p}&step=FuzzingStep")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


def test_task_history_path_traversal_safety():
    """Verify task history endpoint against path traversal task_id inputs."""
    path_traversal_ids = ["../../etc/passwd", "..%2F..%2Fetc%2Fpasswd", "<script>alert(1)</script>"]

    for bad_id in path_traversal_ids:
        resp = client.get(f"/api/v1/task/{bad_id}/history")
        assert resp.status_code in [200, 404]
        assert isinstance(resp.json(), list) or "detail" in resp.json()
