import pytest

from vectrix.core.config import VectrixConfig


def test_default_configuration():
    config = VectrixConfig()

    assert config.project_name == "VECTRIX"
    assert config.version == "0.1.0"
    assert config.log_level == "INFO"


def test_environment_overrides(monkeypatch):
    monkeypatch.setenv("VECTRIX_DATA_DIR", "custom_data")
    monkeypatch.setenv("VECTRIX_EVIDENCE_DIR", "custom_evidence")
    monkeypatch.setenv("VECTRIX_LOG_DIR", "custom_logs")
    monkeypatch.setenv("VECTRIX_LOG_LEVEL", "debug")

    config = VectrixConfig.from_environment()

    assert str(config.data_dir) == "custom_data"
    assert str(config.evidence_dir) == "custom_evidence"
    assert str(config.log_dir) == "custom_logs"
    assert config.log_level == "DEBUG"


def test_directory_creation(tmp_path):
    config = VectrixConfig(
        data_dir=tmp_path / "data",
        evidence_dir=tmp_path / "data" / "evidence",
        log_dir=tmp_path / "data" / "logs",
    )

    config.create_directories()

    assert config.data_dir.is_dir()
    assert config.evidence_dir.is_dir()
    assert config.log_dir.is_dir()


def test_configuration_is_immutable():
    config = VectrixConfig()

    with pytest.raises(AttributeError):
        config.version = "0.2.0"