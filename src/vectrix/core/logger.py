import json
import logging
from datetime import UTC, datetime

from vectrix.core.config import VectrixConfig


class JSONFormatter(logging.Formatter):
    """Format log records as structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.fromtimestamp(
                record.created, UTC
            ).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_entry["exception"] = self.formatException(
                record.exc_info
            )

        return json.dumps(log_entry)


def get_logger(
    name: str,
    config: VectrixConfig,
) -> logging.Logger:
    """Create a logger that writes structured JSON records."""

    level = getattr(logging, config.log_level, None)

    if not isinstance(level, int):
        raise TypeError(f"Invalid logging level: {config.log_level}")

    config.create_directories()

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        log_file = config.log_dir / "vectrix.log"

        handler = logging.FileHandler(
            log_file,
            encoding="utf-8",
        )

        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

    return logger