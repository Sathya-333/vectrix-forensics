from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class EventType(str, Enum):
    PROCESS_EXECUTION = "process_execution"
    FILE_CREATED = "file_created"
    FILE_MODIFIED = "file_modified"
    FILE_DELETED = "file_deleted"
    NETWORK_CONNECTION = "network_connection"
    DEPENDENCY_DOWNLOAD = "dependency_download"
    BUILD_STARTED = "build_started"
    BUILD_COMPLETED = "build_completed"


@dataclass(frozen=True)
class ForensicEvent:
    event_type: EventType
    build_id: str
    source: str

    event_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    process_id: int | None = None
    parent_process_id: int | None = None

    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.build_id.strip():
            raise ValueError("build_id cannot be empty")

        if not self.source.strip():
            raise ValueError("source cannot be empty")

        if self.timestamp.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")

        if self.timestamp.utcoffset() is None:
            raise ValueError("timestamp must have a valid UTC offset")

        if self.process_id is not None and self.process_id <= 0:
            raise ValueError("process_id must be positive")

        if (
            self.parent_process_id is not None
            and self.parent_process_id <= 0
        ):
            raise ValueError("parent_process_id must be positive")

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "build_id": self.build_id,
            "source": self.source,
            "process_id": self.process_id,
            "parent_process_id": self.parent_process_id,
            "details": self.details,
        }