import unittest

from main import get_system_info


class TestSystemInfo(unittest.TestCase):
    def test_system_info_contains_required_fields(self):
        info = get_system_info()

        required_fields = [
            "Operating System",
            "OS Version",
            "Architecture",
            "Python Version",
            "Current Time",
            "Current Directory",
        ]

        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(field, info)
                self.assertTrue(info[field])

    def test_python_version_is_available(self):
        info = get_system_info()
        self.assertTrue(info["Python Version"])


if __name__ == "__main__":
    unittest.main()
