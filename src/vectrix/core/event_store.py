import json
from pathlib import Path

from vectrix.core.events import ForensicEvent


class EventStore:
    """Persist forensic events in JSONL format."""

    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.event_file = self.storage_dir / "events.jsonl"

    def append(self, event: ForensicEvent) -> None:
        """Append one forensic event to the event store."""

        record = json.dumps(
            event.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
        )

        with self.event_file.open("a", encoding="utf-8") as file:
            file.write(record + "\n")