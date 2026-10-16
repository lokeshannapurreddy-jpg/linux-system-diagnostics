# Linux System Diagnostics

A Python command-line tool that collects system information and monitors CPU, memory, and disk usage.

## Features
- Operating system and version information
- Processor architecture and Python version
- CPU utilization
- Memory utilization and available memory
- Disk utilization and available disk space
- Automated tests using Python unittest

## Requirements
- Python 3.10 or later
- psutil

## Installation
Run: python -m pip install psutil

## Run the application
Run: python main.py

## Run the tests
Run: python -m unittest -v test_main.py

## Project files
- main.py: Main application
- test_main.py: Automated tests
- README.md: Project documentation

## Platform compatibility

Verified on:
- Ubuntu 26.04.1 LTS with Python 3.14.4
- Windows with Python

The application runs on Ubuntu Linux, and both automated tests pass
in the Ubuntu environment.
