# VECTRIX

**Build Execution Forensics & Cross-Build Attack Reconstruction Engine**

VECTRIX is a Linux-focused build forensics platform designed to observe build-time execution, preserve evidence, identify suspicious mutations, and reconstruct potential software supply-chain attacks across multiple builds.

## Core Objectives

- Capture actual build execution activity.
- Record process, filesystem, and network events.
- Associate forensic evidence with individual builds.
- Identify suspicious build-time behavior.
- Compare clean and potentially compromised builds.
- Reconstruct cross-build attack propagation.
- Generate verifiable forensic evidence bundles.

## Key Capabilities (Planned)

1. **Build Observation** — Monitor execution inside isolated Linux build environments.
2. **Execution Recording** — Capture process activity, filesystem modifications, and network behavior.
3. **Forensic Analysis** — Identify suspicious changes and behavioral anomalies.
4. **Cross-Build Correlation** — Trace dependencies, artifacts, and suspicious activity across builds.
5. **Attack Reconstruction** — Build evidence-backed timelines and impact assessments.
6. **Evidence Preservation** — Generate integrity-verifiable forensic evidence bundles.

## Technology Stack

Current foundation:

- Python
- Typer — CLI framework
- Rich — Terminal output
- pytest — Testing
- Ruff — Linting

Planned integrations:

- Docker — Isolated build environments
- eBPF-based telemetry — Linux execution monitoring
- Syft — Software Bill of Materials (SBOM)
- Cosign / Sigstore — Artifact signature verification
- NetworkX — Forensic relationship graphs
- SQLite — Local evidence storage
- Terraform and Ansible — Infrastructure provisioning and configuration

## Project Status

**Current Phase:** Phase 1 — Foundation & Build Environment

VECTRIX is under active development.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd vectrix
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

Display available commands:

```bash
vectrix --help
```

Display the current version:

```bash
vectrix version
```

## Development and Testing

Run the test suite:

```bash
pytest -v
```

Run lint checks:

```bash
ruff check .
```

## Project Structure

```text
vectrix/
├── docs/
│   └── architecture/
├── examples/
├── scripts/
├── src/
│   └── vectrix/
│       ├── __init__.py
│       └── cli.py
├── tests/
│   └── test_cli.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Development Roadmap

| Phase | Focus |
|---|---|
| Phase 1 | Foundation & Build Environment |
| Phase 2 | Build Execution Recorder |
| Phase 3 | Forensic Intelligence & Detection |
| Phase 4 | Cross-Build Reconstruction & Infrastructure |
| Phase 5 | Hardening, Testing & Release |

---

**VECTRIX — Observe. Correlate. Reconstruct.**