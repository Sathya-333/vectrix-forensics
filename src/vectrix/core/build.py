
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from vectrix.core.events import EventType, ForensicEvent
from vectrix.core.repository import (
    RepositoryMetadata,
    collect_repository_metadata,
)


class BuildStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class BuildSession:
    """Represent one VECTRIX build execution."""

    build_id: UUID = field(default_factory=uuid4)

    status: BuildStatus = BuildStatus.CREATED

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    started_at: datetime | None = None
    finished_at: datetime | None = None

    error: str | None = None

    repository: RepositoryMetadata | None = None

    def create_event(
        self,
        event_type: EventType,
        source: str = "vectrix.build",
        details: dict[str, Any] | None = None,
    ) -> ForensicEvent:
        """Create a forensic event associated with this build."""

        return ForensicEvent(
            event_type=event_type,
            build_id=str(self.build_id),
            source=source,
            details=details if details is not None else {},
        )

    @classmethod
    def from_repository(cls, repository_path: Path) -> "BuildSession":
        """Create a build session with captured repository metadata."""

        metadata = collect_repository_metadata(repository_path)

        return cls(repository=metadata)

    def to_dict(self) -> dict:
        """Serialize build session metadata into a dictionary."""

        repository_data = None

        if self.repository is not None:
            repository_data = {
                "root_path": str(self.repository.root_path),
                "commit_sha": self.repository.commit_sha,
                "branch": self.repository.branch,
                "is_dirty": self.repository.is_dirty,
                "captured_at": self.repository.captured_at.isoformat(),
            }

        return {
            "build_id": str(self.build_id),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": (
                self.started_at.isoformat()
                if self.started_at is not None
                else None
            ),
            "finished_at": (
                self.finished_at.isoformat()
                if self.finished_at is not None
                else None
            ),
            "error": self.error,
            "repository": repository_data,
        }

    def start(self) -> None:
        """Transition the build from CREATED to RUNNING."""

        if self.status != BuildStatus.CREATED:
            raise ValueError(
                f"Cannot start build in {self.status.value} state"
            )

        self.status = BuildStatus.RUNNING
        self.started_at = datetime.now(UTC)

    def complete(self) -> None:
        """Transition the build from RUNNING to COMPLETED."""

        if self.status != BuildStatus.RUNNING:
            raise ValueError(
                f"Cannot complete build in {self.status.value} state"
            )

        self.status = BuildStatus.COMPLETED
        self.finished_at = datetime.now(UTC)

    def fail(self, error: str) -> None:
        """Transition the build to FAILED."""

        if self.status not in (
            BuildStatus.CREATED,
            BuildStatus.RUNNING,
        ):
            raise ValueError(
                f"Cannot fail build in {self.status.value} state"
            )

        if not error.strip():
            raise ValueError("Failure reason cannot be empty")

        self.status = BuildStatus.FAILED
        self.finished_at = datetime.now(UTC)
        self.error = error
