import json

from vectrix.core.event_store import EventStore
from vectrix.core.events import EventType, ForensicEvent


def test_event_store_creates_storage_directory(tmp_path):
    storage_dir = tmp_path / "evidence"

    store = EventStore(storage_dir)

    assert storage_dir.exists()
    assert store.event_file.name == "events.jsonl"


def test_event_store_appends_event(tmp_path):
    store = EventStore(tmp_path)

    event = ForensicEvent(
        event_type=EventType.PROCESS_EXECUTION,
        build_id="BUILD-001",
        source="test.collector",
        process_id=1234,
    )

    store.append(event)

    records = [
        json.loads(line)
        for line in store.event_file.read_text().splitlines()
    ]

    assert len(records) == 1
    assert records[0]["event_id"] == str(event.event_id)


def test_event_store_preserves_multiple_events(tmp_path):
    store = EventStore(tmp_path)

    first = ForensicEvent(
        event_type=EventType.PROCESS_EXECUTION,
        build_id="BUILD-001",
        source="test.collector",
    )

    second = ForensicEvent(
        event_type=EventType.FILE_MODIFIED,
        build_id="BUILD-001",
        source="test.collector",
        details={"path": "/tmp/config.json"},
    )

    store.append(first)
    store.append(second)

    records = [
        json.loads(line)
        for line in store.event_file.read_text().splitlines()
    ]

    assert len(records) == 2
    assert records[0]["event_type"] == "process_execution"
    assert records[1]["event_type"] == "file_modified"