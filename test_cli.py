import unittest

from cli import build_parser, check_thresholds


class TestCLI(unittest.TestCase):
    def test_threshold_warning_when_limit_exceeded(self):
        usage = {"cpu": 85.0, "memory": 50.0, "disk": 20.0}
        limits = {"cpu": 80.0, "memory": 80.0, "disk": 80.0}

        warnings = check_thresholds(usage, limits)

        self.assertEqual(len(warnings), 1)
        self.assertIn("cpu", warnings[0])
        self.assertIn("85.0%", warnings[0])

    def test_no_warning_when_usage_is_below_limit(self):
        usage = {"cpu": 40.0, "memory": 50.0, "disk": 20.0}
        limits = {"cpu": 80.0, "memory": 80.0, "disk": 80.0}

        self.assertEqual(check_thresholds(usage, limits), [])

    def test_threshold_can_be_disabled(self):
        usage = {"cpu": 99.0, "memory": 50.0, "disk": 20.0}
        limits = {"cpu": None, "memory": None, "disk": None}

        self.assertEqual(check_thresholds(usage, limits), [])

    def test_parser_accepts_cli_arguments(self):
        parser = build_parser()
        args = parser.parse_args([
            "--cpu-threshold", "80",
            "--mem-threshold", "75",
            "--disk-threshold", "90",
            "--log", "/tmp/sample.log",
        ])

        self.assertEqual(args.cpu_threshold, 80.0)
        self.assertEqual(args.mem_threshold, 75.0)
        self.assertEqual(args.disk_threshold, 90.0)
        self.assertEqual(args.log, "/tmp/sample.log")


if __name__ == "__main__":
    unittest.main()
