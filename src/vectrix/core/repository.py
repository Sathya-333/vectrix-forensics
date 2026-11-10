import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class RepositoryMetadata:
    """Capture source repository identity for a build."""

    root_path: Path
    commit_sha: str
    branch: str
    is_dirty: bool
    captured_at: datetime


def get_git_output(
    repository_path: Path,
    *arguments: str,
) -> str:
    """Execute a Git command and return its output."""

    result = subprocess.run(
        ["git", "-C", str(repository_path), *arguments],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout.strip()


def collect_repository_metadata(
    repository_path: Path,
) -> RepositoryMetadata:
    """Collect Git metadata for a repository."""

    root_path = Path(
        get_git_output(repository_path, "rev-parse", "--show-toplevel")
    ).resolve()

    commit_sha = get_git_output(
        root_path,
        "rev-parse",
        "HEAD",
    )

    branch = get_git_output(
        root_path,
        "branch",
        "--show-current",
    )

    status = get_git_output(
        root_path,
        "status",
        "--porcelain",
    )

    return RepositoryMetadata(
        root_path=root_path,
        commit_sha=commit_sha,
        branch=branch,
        is_dirty=bool(status),
        captured_at=datetime.now(UTC),
    )