import os
import tempfile
import unittest

from log_analyzer import LogAnalysisError, analyze_log, normalize


class TestLogAnalyzer(unittest.TestCase):
    def write_log(self, text):
        file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".log"
        )
        file.write(text)
        file.close()
        self.addCleanup(os.remove, file.name)
        return file.name

    def test_counts_recurring_errors(self):
        path = self.write_log(
            "Oct 16 10:00:01 host app[123]: ERROR disk failed on sda1\n"
            "Oct 16 10:00:05 host app[456]: ERROR disk failed on sda1\n"
            "Oct 16 10:00:09 host app[789]: info all good\n"
        )

        result = analyze_log(path)

        self.assertEqual(result["total_lines"], 3)
        self.assertEqual(result["error_lines"], 2)
        self.assertEqual(result["top_errors"][0][1], 2)

    def test_missing_file(self):
        with self.assertRaises(LogAnalysisError):
            analyze_log("/nonexistent/file.log")

    def test_normalize_removes_numbers(self):
        self.assertEqual(
            normalize("Oct 16 10:00:01 x: fail 42"),
            "x: fail N",
        )

    def test_empty_file(self):
        path = self.write_log("")
        result = analyze_log(path)

        self.assertEqual(result["total_lines"], 0)
        self.assertEqual(result["error_lines"], 0)
        self.assertEqual(result["top_errors"], [])

    def test_top_limits_results(self):
        path = self.write_log(
            "ERROR disk failed\n"
            "ERROR network failed\n"
            "ERROR memory failed\n"
        )

        result = analyze_log(path, top=2)

        self.assertEqual(len(result["top_errors"]), 2)


    def test_top_zero_returns_no_errors(self):
        path = self.write_log("ERROR disk failed\n")

        result = analyze_log(path, top=0)

        self.assertEqual(result["error_lines"], 1)
        self.assertEqual(result["top_errors"], [])

    def test_log_without_errors(self):
        path = self.write_log(
            "INFO service started\n"
            "WARNING memory usage high\n"
        )

        result = analyze_log(path)

        self.assertEqual(result["total_lines"], 2)
        self.assertEqual(result["error_lines"], 0)
        self.assertEqual(result["top_errors"], [])

    def test_negative_top_returns_no_errors(self):
        path = self.write_log("ERROR disk failed\n")

        result = analyze_log(path, top=-1)

        self.assertEqual(result["error_lines"], 1)
        self.assertEqual(result["top_errors"], [])


if __name__ == "__main__":
    unittest.main()
