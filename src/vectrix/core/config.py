import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VectrixConfig:
    """Central configuration for VECTRIX."""

    project_name: str = "VECTRIX"
    version: str = "0.1.0"

    data_dir: Path = Path("data")
    evidence_dir: Path = Path("data/evidence")
    log_dir: Path = Path("data/logs")

    log_level: str = "INFO"

    @classmethod
    def from_environment(cls) -> "VectrixConfig":
        """Load configuration with optional environment overrides."""

        return cls(
            data_dir=Path(
                os.getenv("VECTRIX_DATA_DIR", "data")
            ),
            evidence_dir=Path(
                os.getenv("VECTRIX_EVIDENCE_DIR", "data/evidence")
            ),
            log_dir=Path(
                os.getenv("VECTRIX_LOG_DIR", "data/logs")
            ),
            log_level=os.getenv("VECTRIX_LOG_LEVEL", "INFO").upper(),
        )

    def create_directories(self) -> None:
        """Create required local storage directories."""

        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)