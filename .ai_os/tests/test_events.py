"""
Tests for Event System
"""

import pytest
from src.core.events import Event, EventType, EventPriority, EventBus, get_event_bus


class TestEventBus:
    def test_publish_and_subscribe(self):
        bus = EventBus()
        received = []

        def handler(event):
            received.append(event)

        bus.subscribe(EventType.SYSTEM_STARTUP, handler)
        bus.publish(Event(type=EventType.SYSTEM_STARTUP, source="test", producer="test"))

        assert len(received) == 1
        assert received[0].type == EventType.SYSTEM_STARTUP

    def test_global_subscription(self):
        bus = EventBus()
        received = []

        def handler(event):
            received.append(event)

        bus.subscribe_all(handler)
        bus.publish(Event(type=EventType.TASK_CREATED, source="test", producer="test"))
        bus.publish(Event(type=EventType.CACHE_HIT, source="test", producer="test"))

        assert len(received) == 2

    def test_event_filter(self):
        bus = EventBus()
        received = []

        def handler(event):
            received.append(event)

        bus.subscribe(
            EventType.TASK_CREATED,
            handler,
            filter_fn=lambda e: e.priority == EventPriority.HIGH
        )

        bus.publish(Event(type=EventType.TASK_CREATED, source="test", producer="test", priority=EventPriority.LOW))
        bus.publish(Event(type=EventType.TASK_CREATED, source="test", producer="test", priority=EventPriority.HIGH))

        assert len(received) == 1
        assert received[0].priority == EventPriority.HIGH

    def test_event_history(self):
        bus = EventBus()
        bus.publish(Event(type=EventType.SYSTEM_STARTUP, source="test", producer="test"))
        bus.publish(Event(type=EventType.TASK_CREATED, source="test", producer="test"))

        history = bus.get_history(limit=10)
        assert len(history) == 2

        filtered = bus.get_history(event_type=EventType.TASK_CREATED)
        assert len(filtered) == 1

    def test_unsubscribe(self):
        bus = EventBus()
        received = []

        def handler(event):
            received.append(event)

        sub_id = bus.subscribe(EventType.SYSTEM_STARTUP, handler)
        bus.publish(Event(type=EventType.SYSTEM_STARTUP, source="test", producer="test"))
        assert len(received) == 1

        bus.unsubscribe(sub_id)
        bus.publish(Event(type=EventType.SYSTEM_STARTUP, source="test", producer="test"))
        assert len(received) == 1  # No new events

    def test_event_serialization(self):
        event = Event(
            type=EventType.TASK_CREATED,
            source="test",
            producer="test",
            payload={"task_id": "123"}
        )
        data = event.to_dict()
        assert data["type"] == "task.created"
        assert data["payload"]["task_id"] == "123"
        assert "id" in data
        assert "timestamp" in data

    def test_stats(self):
        bus = EventBus()
        bus.publish(Event(type=EventType.SYSTEM_STARTUP, source="test", producer="test"))
        bus.publish(Event(type=EventType.TASK_CREATED, source="test", producer="test"))

        stats = bus.get_stats()
        assert stats["total_events"] == 2
        assert stats["event_type_counts"]["system.startup"] == 1
        assert stats["event_type_counts"]["task.created"] == 1