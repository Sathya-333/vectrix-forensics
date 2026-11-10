import subprocess
from pathlib import Path
from uuid import UUID

import pytest

from vectrix.core.build import BuildSession, BuildStatus
from vectrix.core.events import EventType


def test_build_creation():
    build = BuildSession()

    assert isinstance(build.build_id, UUID)
    assert build.status == BuildStatus.CREATED
    assert build.created_at is not None
    assert build.started_at is None
    assert build.finished_at is None


def test_build_ids_are_unique():
    first = BuildSession()
    second = BuildSession()

    assert first.build_id != second.build_id


def test_build_start():
    build = BuildSession()

    build.start()

    assert build.status == BuildStatus.RUNNING
    assert build.started_at is not None


def test_build_completion():
    build = BuildSession()

    build.start()
    build.complete()

    assert build.status == BuildStatus.COMPLETED
    assert build.finished_at is not None
    assert build.error is None


def test_build_failure_from_created():
    build = BuildSession()

    build.fail("Build initialization failed")

    assert build.status == BuildStatus.FAILED
    assert build.finished_at is not None
    assert build.error == "Build initialization failed"


def test_build_failure_from_running():
    build = BuildSession()

    build.start()
    build.fail("Compilation failed")

    assert build.status == BuildStatus.FAILED
    assert build.error == "Compilation failed"
    assert build.finished_at is not None


def test_cannot_start_running_build_again():
    build = BuildSession()
    build.start()

    with pytest.raises(ValueError):
        build.start()


def test_cannot_complete_unstarted_build():
    build = BuildSession()

    with pytest.raises(ValueError):
        build.complete()


def test_cannot_fail_completed_build():
    build = BuildSession()
    build.start()
    build.complete()

    with pytest.raises(ValueError):
        build.fail("Late failure")


def test_cannot_complete_failed_build():
    build = BuildSession()
    build.fail("Initial failure")

    with pytest.raises(ValueError):
        build.complete()


def test_empty_failure_reason_is_rejected():
    build = BuildSession()

    with pytest.raises(ValueError):
        build.fail("   ")

def create_git_repository(path: Path) -> None:
    path.mkdir()

    subprocess.run(
        ["git", "init", "-b", "main", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )

    subprocess.run(
        ["git", "-C", str(path), "config", "user.name", "VECTRIX Test"],
        check=True,
    )

    subprocess.run(
        [
            "git", "-C", str(path),
            "config", "user.email", "vectrix-test@example.com",
        ],
        check=True,
    )

    (path / "sample.txt").write_text("test\n")

    subprocess.run(
        ["git", "-C", str(path), "add", "sample.txt"],
        check=True,
    )

    subprocess.run(
        ["git", "-C", str(path), "commit", "-m", "Test commit"],
        check=True,
        capture_output=True,
        text=True,
    )


def test_build_session_captures_repository(tmp_path):
    repository = tmp_path / "repository"
    create_git_repository(repository)

    build = BuildSession.from_repository(repository)

    assert build.repository is not None
    assert build.repository.root_path == repository.resolve()
    assert len(build.repository.commit_sha) == 40
    assert build.repository.branch == "main"
    assert build.repository.is_dirty is False


def test_build_sessions_have_unique_ids_for_same_repository(tmp_path):
    repository = tmp_path / "repository"
    create_git_repository(repository)

    first = BuildSession.from_repository(repository)
    second = BuildSession.from_repository(repository)

    assert first.build_id != second.build_id
    assert first.repository.commit_sha == second.repository.commit_sha


def test_repository_metadata_survives_build_lifecycle(tmp_path):
    repository = tmp_path / "repository"
    create_git_repository(repository)

    build = BuildSession.from_repository(repository)
    original_commit = build.repository.commit_sha

    build.start()
    build.complete()

    assert build.status == BuildStatus.COMPLETED
    assert build.repository.commit_sha == original_commit


def test_build_session_rejects_non_git_repository(tmp_path):
    repository = tmp_path / "not_a_repository"
    repository.mkdir()

    with pytest.raises(subprocess.CalledProcessError):
        BuildSession.from_repository(repository)

def test_build_serialization():
    build = BuildSession()

    data = build.to_dict()

    assert data["build_id"] == str(build.build_id)
    assert data["status"] == "created"
    assert data["created_at"] is not None
    assert data["started_at"] is None
    assert data["finished_at"] is None
    assert data["error"] is None
    assert data["repository"] is None


def test_build_serialization_after_completion():
    build = BuildSession()

    build.start()
    build.complete()

    data = build.to_dict()

    assert data["status"] == "completed"
    assert data["started_at"] is not None
    assert data["finished_at"] is not None


def test_build_serialization_with_repository(tmp_path):
    repository = tmp_path / "repository"
    create_git_repository(repository)

    build = BuildSession.from_repository(repository)

    data = build.to_dict()

    assert data["repository"]["root_path"] == str(repository.resolve())
    assert len(data["repository"]["commit_sha"]) == 40
    assert data["repository"]["branch"] == "main"
    assert data["repository"]["is_dirty"] is False

def test_create_build_event():
    build = BuildSession()

    event = build.create_event(EventType.BUILD_STARTED)

    assert event.event_type == EventType.BUILD_STARTED
    assert event.build_id == str(build.build_id)
    assert event.source == "vectrix.build"
    assert event.details == {}


def test_create_build_event_with_custom_details():
    build = BuildSession()
    details = {"message": "Build execution started"}

    event = build.create_event(
        EventType.BUILD_COMPLETED,
        source="vectrix.test",
        details=details,
    )

    assert event.event_type == EventType.BUILD_COMPLETED
    assert event.build_id == str(build.build_id)
    assert event.source == "vectrix.test"
    assert event.details == details