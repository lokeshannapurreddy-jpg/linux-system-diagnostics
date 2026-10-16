import argparse
import sys

import psutil

from log_analyzer import LogAnalysisError, analyze_log


def check_thresholds(usage, limits):
    """Return warnings for metrics that exceed their configured limits."""
    warnings = []

    for name, limit in limits.items():
        if limit is not None and usage[name] > limit:
            warnings.append(
                f"WARNING: {name} usage {usage[name]:.1f}% "
                f"exceeds threshold {limit}%"
            )

    return warnings


def build_parser():
    parser = argparse.ArgumentParser(
        description="Linux system diagnostics and log analysis"
    )
    parser.add_argument(
        "--cpu-threshold",
        type=float,
        help="Warn when CPU usage exceeds this percentage",
    )
    parser.add_argument(
        "--mem-threshold",
        type=float,
        help="Warn when memory usage exceeds this percentage",
    )
    parser.add_argument(
        "--disk-threshold",
        type=float,
        help="Warn when disk usage exceeds this percentage",
    )
    parser.add_argument(
        "--log",
        help="Path to a log file to analyze",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    limits = {
        "cpu": args.cpu_threshold,
        "memory": args.mem_threshold,
        "disk": args.disk_threshold,
    }

    for name, limit in limits.items():
        if limit is not None and not 0 <= limit <= 100:
            parser.error(f"{name} threshold must be between 0 and 100")

    usage = {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
    }

    print("SYSTEM RESOURCE USAGE")
    for name, value in usage.items():
        print(f"{name}: {value:.1f}%")

    warnings = check_thresholds(usage, limits)

    for warning in warnings:
        print(warning)

    if args.log:
        try:
            result = analyze_log(args.log)
        except LogAnalysisError as error:
            print(f"ERROR: {error}", file=sys.stderr)
            return 2

        print("\nLOG ANALYSIS")
        print(f"Total lines: {result['total_lines']}")
        print(f"Error lines: {result['error_lines']}")
        print("Most frequent errors:")

        for message, count in result["top_errors"]:
            print(f"  {count}x {message}")

    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
