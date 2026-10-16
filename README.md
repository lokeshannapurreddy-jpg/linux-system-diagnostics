# Linux System Diagnostics

[![CI](https://github.com/lokeshannapurreddy-jpg/linux-system-diagnostics/actions/workflows/ci.yml/badge.svg)](https://github.com/lokeshannapurreddy-jpg/linux-system-diagnostics/actions/workflows/ci.yml)

A Python command-line utility for collecting system information, monitoring resource usage, checking configurable thresholds, and analyzing log files.

## Features

- Collects operating system, OS version, processor architecture, Python version, and current working directory.
- Reports CPU utilization, memory utilization, available memory, disk utilization, and available disk space.
- Supports configurable CPU, memory, and disk usage thresholds.
- Analyzes log files to count lines, identify error-related messages, and summarize recurring errors.
- Handles missing and inaccessible log files with clear error messages.
- Includes automated unit tests using Python's unittest framework.
- Runs automated tests through GitHub Actions on Python 3.10 and 3.12.

## Requirements

- Python 3.10 or later
- psutil

## Installation

Clone the repository and enter the project directory:

    git clone https://github.com/lokeshannapurreddy-jpg/linux-system-diagnostics.git
    cd linux-system-diagnostics

Optionally, create and activate a virtual environment:

    python -m venv .venv
    source .venv/bin/activate

Install the dependency:

    python -m pip install psutil

## Usage

### Display system information and resource usage

    python main.py

### Monitor resource usage with thresholds

    python cli.py --cpu-threshold 80

Set multiple thresholds:

    python cli.py --cpu-threshold 80 --mem-threshold 75 --disk-threshold 90

The CLI prints current resource usage and displays a warning when a configured threshold is exceeded.

### Analyze a log file

    python cli.py --log /path/to/application.log

The report includes the total number of lines, the number of error-related lines, and the most frequent matching error messages.

### Combine resource monitoring and log analysis

    python cli.py --cpu-threshold 80 --mem-threshold 75 --disk-threshold 90 --log /path/to/application.log

### Display CLI options

    python cli.py --help

## Run the tests

Run the complete test suite:

    python -m unittest discover -v

The suite covers system information, log analysis, CLI argument parsing, and resource threshold checks.

## Project structure

    linux-system-diagnostics/
    ├── .github/
    │   └── workflows/
    │       └── ci.yml
    ├── .gitignore
    ├── README.md
    ├── main.py
    ├── test_main.py
    ├── cli.py
    ├── test_cli.py
    ├── log_analyzer.py
    └── test_log_analyzer.py

## Continuous integration

GitHub Actions runs the automated test suite on Python 3.10 and Python 3.12 when code is pushed or a pull request is opened.

## Platform compatibility

The project has been tested in an Ubuntu environment using Python's unittest framework. The system diagnostics functionality uses psutil to collect resource metrics.

## Limitations

- Resource usage values represent a snapshot taken when the command runs.
- Log analysis identifies messages containing configured error-related keywords; it is not a complete log-format parser.
- Resource metrics and available disk space depend on the environment in which the program runs.

## License

No license has been specified yet.
