import io
import unittest
from unittest.mock import patch
from passcraft.cli import main

class TestPasscraftCLI(unittest.TestCase):
    def test_cli_default_password(self):
        f = io.StringIO()
        with patch('sys.stdout', f):
            exit_code = main(["--count", "1", "--length", "16"])
        self.assertEqual(exit_code, 0)
        output = f.getvalue().strip()
        self.assertTrue(len(output) >= 16)

    def test_cli_multiple_passwords(self):
        f = io.StringIO()
        with patch('sys.stdout', f):
            exit_code = main(["-n", "3", "-l", "12"])
        self.assertEqual(exit_code, 0)
        lines = [line.strip() for line in f.getvalue().strip().split("\n") if line.strip()]
        self.assertEqual(len(lines), 3)
        for line in lines:
            self.assertEqual(len(line), 12)

    def test_cli_passphrase_mode(self):
        f = io.StringIO()
        with patch('sys.stdout', f):
            exit_code = main(["-w", "4", "--separator", "."])
        self.assertEqual(exit_code, 0)
        output = f.getvalue().strip()
        words = output.split(".")
        self.assertEqual(len(words), 4)

    def test_cli_show_entropy(self):
        f = io.StringIO()
        with patch('sys.stdout', f):
            exit_code = main(["-l", "16", "--show-entropy"])
        self.assertEqual(exit_code, 0)
        output = f.getvalue()
        self.assertIn("Entropy:", output)
        self.assertIn("Strength:", output)

if __name__ == "__main__":
    unittest.main()
