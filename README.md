# Ateno Python SDK (`ateno-py`)

Official Python SDK and CLI for Ateno.

## Overview

This package provides:

- A Python client (`AtenoClient`) for calling Ateno APIs.
- A CLI command (`ateno`) exposed via `pyproject.toml` scripts.
- Homebrew distribution support through the `AtenoTech/ateno-homebrew` tap.

Version source of truth: `pyproject.toml`.

## Install

### pip

```bash
pip install ateno
```

### Homebrew

```bash
brew tap AtenoTech/ateno-homebrew
brew install ateno
```

## Quick Start

```python
from ateno import AtenoClient

client = AtenoClient(api_key="YOUR_API_KEY")
result = client.create_event("example.event", {"source": "python"})
print(result)
```

## API Reference

### `AtenoClient(api_key, base_url="https://api.ateno.ai")`

- `api_key`: Bearer token used for authorization.
- `base_url`: API host override for local/test environments.

### `create_event(name, data)`

- Performs `POST {base_url}/events`.
- Sends payload: `{"name": name, "data": data}`.
- Returns parsed JSON response.

## CLI

The package exposes an `ateno` command through:

```toml
[project.scripts]
ateno = "ateno.main:main"
```

Current commands:

```bash
ateno --version
```

Default execution prints initialization/help guidance.

## Local Development

### Prerequisites

- Python 3.10+
- `pip` and `venv`

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

### Run locally

```bash
ateno --version
python -m ateno.main --version
```

## Contributor Workflow

### Branch and commit conventions

- Use focused feature/fix branches.
- Prefer Conventional Commit style such as `feat: ...`, `fix: ...`, `docs: ...`, and `chore: ...`.

### Change checklist

- Implement code changes in `ateno/`.
- Keep API and CLI docs aligned with behavior.
- Validate package installation in a clean virtualenv.
- Update `pyproject.toml` version for releases.

## Release Process

Homebrew formula updates should come from release automation, not manual checksum workflows in normal operation.

1. Bump `version` in `pyproject.toml`.
2. Commit and push to `main`.
3. Tag matching release (`vX.Y.Z`).

```bash
git add .
git commit -m "release: v0.1.x"
git push origin main
git tag v0.1.x
git push origin v0.1.x
```

4. Verify GitHub Actions succeeded.
5. Validate package installation:

```bash
brew update
brew upgrade ateno || brew install ateno
ateno --version
```

## Homebrew Notes

- Formula lives in `ateno-homebrew/Formula/ateno.rb`.
- Formula creates an isolated `libexec` virtual environment and installs package dependencies with pip.
- Global `ateno` command is symlinked from the isolated environment.

## Troubleshooting

### Factory reset (Homebrew)

```bash
brew update
brew uninstall --force ateno
rm -rf /opt/homebrew/Cellar/ateno
brew install ateno
```

### `ModuleNotFoundError` or dependency issues

- Reinstall from a clean cellar using the reset steps above.
- Confirm formula references expected Python version (`python@3.12` currently).

## License

MIT
