import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
CLI_PATH = PROJECT_DIR / "cli.py"


class TestCLIIntegration(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(CLI_PATH), *args],
            capture_output=True,
            text=True,
            timeout=15,
        )

    def test_help_displays_usage(self):
        result = self.run_cli("--help")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Linux system diagnostics", result.stdout)
        self.assertIn("--cpu-threshold", result.stdout)

    def test_invalid_cpu_threshold_is_rejected(self):
        result = self.run_cli("--cpu-threshold", "101")

        self.assertEqual(result.returncode, 2)
        self.assertIn("cpu threshold must be between 0 and 100",
                      result.stderr)

    def test_missing_log_file_returns_error(self):
        missing_path = str(
            Path(tempfile.gettempdir()) / "file_that_does_not_exist_987654.log"
        )
        result = self.run_cli("--log", missing_path)

        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR:", result.stderr)

    def test_valid_log_file_displays_analysis(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "sample.log"
            log_path.write_text(
                "INFO service started\n"
                "ERROR connection failed\n"
                "ERROR connection failed\n",
                encoding="utf-8",
            )

            result = self.run_cli("--log", str(log_path))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SYSTEM RESOURCE USAGE", result.stdout)
        self.assertIn("LOG ANALYSIS", result.stdout)
        self.assertIn("Total lines: 3", result.stdout)
        self.assertIn("Error lines: 2", result.stdout)


if __name__ == "__main__":
    unittest.main()
