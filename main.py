import os
import platform
import time
from datetime import datetime

import psutil


def format_uptime(seconds):
    """Format elapsed seconds as days, hours, and minutes."""
    minutes = int(seconds // 60)
    days, minutes = divmod(minutes, 1440)
    hours, minutes = divmod(minutes, 60)
    return f"{days}d {hours}h {minutes}m"


def get_system_info():
    """Collect basic operating system and Python information."""
    return {
        "Operating System": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.machine(),
        "Python Version": platform.python_version(),
        "Processor": platform.processor() or "Not available",
        "Current Time": datetime.now().astimezone().strftime(
            "%Y-%m-%d %H:%M:%S %Z"
        ),
        "Current Directory": os.getcwd(),
        "System Uptime": format_uptime(time.time() - psutil.boot_time()),
    }


def get_resource_usage():
    """Collect CPU, memory, and disk usage."""
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(os.path.abspath(os.sep))

    return {
        "CPU Usage": f"{psutil.cpu_percent(interval=1)}%",
        "Memory Usage": f"{memory.percent}%",
        "Memory Available": f"{memory.available / (1024 ** 3):.2f} GB",
        "Disk Usage": f"{disk.percent}%",
        "Disk Free": f"{disk.free / (1024 ** 3):.2f} GB",
    }


def display_report(title, information):
    """Print a formatted section of the diagnostics report."""
    print("\n" + "=" * 55)
    print(f" {title}")
    print("=" * 55)

    for label, value in information.items():
        print(f"{label:<25}: {value}")

def main():
    """Run the diagnostics program."""
    print("SYSTEM DIAGNOSTICS TOOL")

    display_report("SYSTEM INFORMATION", get_system_info())
    display_report("RESOURCE USAGE", get_resource_usage())

    print("\nDiagnostics completed.")


if __name__ == "__main__":
    main()


