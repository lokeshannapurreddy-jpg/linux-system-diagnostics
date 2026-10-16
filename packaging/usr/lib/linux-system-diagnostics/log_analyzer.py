import re
from collections import Counter


ERROR_PATTERN = re.compile(
    r"\b(error|failed|failure|critical|fatal|panic)\b",
    re.IGNORECASE,
)

TIMESTAMP_PATTERN = re.compile(
    r"^(\w{3}\s+\d+\s+[\d:]+|\d{4}-\d{2}-\d{2}[T ][\d:.,+Z-]+)\s*"
)

NUMBER_PATTERN = re.compile(r"\d+")


class LogAnalysisError(Exception):
    """Raised when a log file cannot be read."""


def normalize(line):
    """Remove timestamps and numbers to group similar log messages."""
    line = TIMESTAMP_PATTERN.sub("", line.strip())
    return NUMBER_PATTERN.sub("N", line)


def analyze_log(path, top=5):
    """Count log lines and summarize recurring error messages."""
    errors = Counter()
    total = 0

    try:
        with open(path, "r", errors="replace") as file:
            for line in file:
                total += 1

                if ERROR_PATTERN.search(line):
                    errors[normalize(line)] += 1

    except FileNotFoundError:
        raise LogAnalysisError(f"Log file not found: {path}") from None

    except PermissionError:
        raise LogAnalysisError(f"Permission denied reading: {path}") from None

    return {
        "total_lines": total,
        "error_lines": sum(errors.values()),
        "top_errors": errors.most_common(max(0, top)),
    }
