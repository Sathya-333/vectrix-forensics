from datetime import UTC, datetime

import pytest

from vectrix.core.events import EventType, ForensicEvent


def create_event(**overrides):
    data = {
        "event_type": EventType.PROCESS_EXECUTION,
        "build_id": "BUILD-001",
        "source": "vectrix.test",
        "process_id": 1234,
        "parent_process_id": 1000,
        "details": {"executable": "/usr/bin/python3"},
    }

    data.update(overrides)
    return ForensicEvent(**data)


def test_event_creation():
    event = create_event()

    assert event.build_id == "BUILD-001"
    assert event.event_type == EventType.PROCESS_EXECUTION
    assert event.process_id == 1234


def test_event_ids_are_unique():
    first = create_event()
    second = create_event()

    assert first.event_id != second.event_id


def test_timestamp_is_timezone_aware():
    event = create_event()

    assert event.timestamp.tzinfo is not None
    assert event.timestamp.utcoffset() is not None


def test_event_serialization():
    event = create_event()
    data = event.to_dict()

    assert data["event_id"] == str(event.event_id)
    assert data["event_type"] == "process_execution"
    assert data["build_id"] == "BUILD-001"
    assert data["source"] == "vectrix.test"
    assert data["details"]["executable"] == "/usr/bin/python3"


def test_empty_build_id_is_rejected():
    with pytest.raises(ValueError):
        create_event(build_id="   ")


def test_empty_source_is_rejected():
    with pytest.raises(ValueError):
        create_event(source="")


def test_naive_timestamp_is_rejected():
    with pytest.raises(ValueError):
        create_event(timestamp=datetime(2026, 11, 9))


def test_invalid_process_id_is_rejected():
    with pytest.raises(ValueError):
        create_event(process_id=0)


def test_invalid_parent_process_id_is_rejected():
    with pytest.raises(ValueError):
        create_event(parent_process_id=-1)


def test_custom_utc_timestamp():
    timestamp = datetime(2026, 11, 9, 12, 0, tzinfo=UTC)
    event = create_event(timestamp=timestamp)

    assert event.timestamp == timestamp