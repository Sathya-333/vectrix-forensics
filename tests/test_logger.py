import json

import pytest

from vectrix.core.config import VectrixConfig
from vectrix.core.logger import get_logger


def create_test_config(tmp_path, log_level="INFO"):
    return VectrixConfig(
        data_dir=tmp_path / "data",
        evidence_dir=tmp_path / "evidence",
        log_dir=tmp_path / "logs",
        log_level=log_level,
    )


def close_logger(logger):
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


def test_logger_creates_json_log(tmp_path):
    config = create_test_config(tmp_path)
    logger = get_logger("vectrix.test.json", config)

    try:
        logger.info("Test log message")
        logger.handlers[0].flush()

        log_file = config.log_dir / "vectrix.log"
        record = json.loads(log_file.read_text().strip())

        assert record["level"] == "INFO"
        assert record["logger"] == "vectrix.test.json"
        assert record["message"] == "Test log message"
        assert record["timestamp"].endswith("Z")
    finally:
        close_logger(logger)


def test_logger_respects_log_level(tmp_path):
    config = create_test_config(tmp_path, "INFO")
    logger = get_logger("vectrix.test.level", config)

    try:
        logger.debug("Hidden debug message")
        logger.info("Visible info message")
        logger.handlers[0].flush()

        records = [
            json.loads(line)
            for line in (config.log_dir / "vectrix.log")
            .read_text()
            .splitlines()
        ]

        assert len(records) == 1
        assert records[0]["message"] == "Visible info message"
    finally:
        close_logger(logger)


def test_logger_rejects_invalid_level(tmp_path):
    config = create_test_config(tmp_path, "INVALID")

    with pytest.raises(TypeError):
        get_logger("vectrix.test.invalid", config)


def test_logger_records_exceptions(tmp_path):
    config = create_test_config(tmp_path)
    logger = get_logger("vectrix.test.exception", config)

    try:
        try:
            raise RuntimeError("Controlled test exception")
        except RuntimeError:
            logger.exception("Build execution failed")

        logger.handlers[0].flush()

        record = json.loads(
            (config.log_dir / "vectrix.log").read_text().strip()
        )

        assert record["message"] == "Build execution failed"
        assert "RuntimeError" in record["exception"]
        assert "Controlled test exception" in record["exception"]
    finally:
        close_logger(logger)