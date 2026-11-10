import subprocess

import pytest

from vectrix.core.repository import collect_repository_metadata


def initialize_git_repository(path):
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

    (path / "sample.txt").write_text("VECTRIX test\n")

    subprocess.run(
        ["git", "-C", str(path), "add", "sample.txt"],
        check=True,
    )

    subprocess.run(
        ["git", "-C", str(path), "commit", "-m", "Initial test commit"],
        check=True,
        capture_output=True,
        text=True,
    )


def test_collect_repository_metadata(tmp_path):
    repository = tmp_path / "repository"
    initialize_git_repository(repository)

    metadata = collect_repository_metadata(repository)

    assert metadata.root_path == repository.resolve()
    assert len(metadata.commit_sha) == 40
    assert metadata.branch == "main"
    assert metadata.is_dirty is False
    assert metadata.captured_at.tzinfo is not None


def test_detect_dirty_repository(tmp_path):
    repository = tmp_path / "repository"
    initialize_git_repository(repository)

    (repository / "sample.txt").write_text("Modified content\n")

    metadata = collect_repository_metadata(repository)

    assert metadata.is_dirty is True


def test_collect_metadata_from_subdirectory(tmp_path):
    repository = tmp_path / "repository"
    initialize_git_repository(repository)

    subdirectory = repository / "src"
    subdirectory.mkdir()

    metadata = collect_repository_metadata(subdirectory)

    assert metadata.root_path == repository.resolve()


def test_reject_non_git_directory(tmp_path):
    repository = tmp_path / "not_a_repository"
    repository.mkdir()

    with pytest.raises(subprocess.CalledProcessError):
        collect_repository_metadata(repository)
