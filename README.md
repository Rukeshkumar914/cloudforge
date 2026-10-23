# CloudForge 🚀

**CloudForge** is a Python-based DevOps toolkit for system health checks, resource monitoring, configurable threshold alerts, and JSON report generation.

Built as a hands-on DevOps engineering project using Python, pytest, Docker, Docker Compose, and GitHub Actions.

## Features

- **System Health Checks** — Report operating system, Python version, and disk information.
- **Resource Monitoring** — Monitor CPU, memory, and disk usage.
- **Configurable Thresholds** — Set custom CPU, memory, and disk warning limits.
- **JSON Reports** — Display reports in the terminal or export them to JSON files.
- **Logging** — Track command execution, warnings, and errors.
- **Error Handling** — Handle expected failures and unexpected exceptions.
- **Automated Testing** — Validate functionality using pytest.
- **Containerization** — Run the application using Docker and Docker Compose.
- **Continuous Integration** — Run automated checks through GitHub Actions.

## Requirements

- Python 3.10 or newer (Python 3.14 has been tested)
- pip
- Git
- Docker and Docker Compose (for containerized execution)

## Installation

Clone the repository:

```bash
git clone https://github.com/Rukeshkumar914/cloudforge.git
cd cloudforge
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

### 1. System Health Check

```bash
python -m app health
```

### 2. System Metrics

```bash
python -m app metrics
```

The metrics report includes CPU usage, memory usage, available memory, disk usage, free disk space, configured thresholds, warnings, and overall status.

### 3. Configure Alert Thresholds

```bash
python -m app metrics \
  --cpu-threshold 70 \
  --memory-threshold 75 \
  --disk-threshold 85
```

The application reports warnings when a metric exceeds its configured threshold.

### 4. Export a JSON Report

Export metrics to a JSON file:

```bash
python -m app metrics --output reports/metrics.json
```

Export system health information:

```bash
python -m app health --output reports/health.json
```

Create a report directory automatically when it does not exist.

### 5. View Available Options

```bash
python -m app --help
python -m app metrics --help
```

## Run Tests

Run the complete test suite:

```bash
python -m pytest -v
```

## Docker

Build the Docker image:

```bash
docker build -t cloudforge .
```

Run a system health check inside a container:

```bash
docker run --rm cloudforge health
```

Run metrics monitoring:

```bash
docker run --rm cloudforge metrics
```

If your Dockerfile uses a different entrypoint or command configuration, adjust these commands to match it.

## Docker Compose

Build and start the configured services:

```bash
docker compose up --build
```

Stop the services:

```bash
docker compose down
```

## Continuous Integration

CloudForge uses GitHub Actions to run automated CI checks.

View workflow runs:

https://github.com/Rukeshkumar914/cloudforge/actions

## Project Structure

```text
cloudforge/
├── app/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── health.py
│   └── monitor.py
├── tests/
│   ├── test_cli.py
│   └── test_monitor.py
├── .github/
│   └── workflows/
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

The exact file names may vary slightly depending on the current repository structure.

## Learning Outcomes

This project demonstrates practical experience with:

- Python CLI development
- Linux system resource monitoring
- Logging and exception handling
- Automated testing with pytest
- Docker containerization
- Docker Compose
- Git and GitHub
- GitHub Actions CI

## Future Improvements

- Prometheus metrics integration
- Alert notifications
- Scheduled health checks
- Cloud monitoring integration
- Additional monitoring and integration tests

## Author

GitHub: https://github.com/Rukeshkumar914
