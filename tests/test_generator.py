import unittest
import string
from passcraft.generator import (
    generate_password,
    generate_passphrase,
    calculate_entropy,
    estimate_strength,
    WORDLIST
)

class TestPasscraftGenerator(unittest.TestCase):
    def test_generate_password_default_length(self):
        pwd = generate_password()
        self.assertEqual(len(pwd), 16)

    def test_generate_password_custom_length(self):
        pwd = generate_password(length=24)
        self.assertEqual(len(pwd), 24)

    def test_generate_password_invalid_length(self):
        with self.assertRaises(ValueError):
            generate_password(length=3)

    def test_generate_password_no_charsets(self):
        with self.assertRaises(ValueError):
            generate_password(use_upper=False, use_lower=False, use_digits=False, use_symbols=False)

    def test_generate_password_includes_selected_types(self):
        for _ in range(10):
            pwd = generate_password(length=12, use_upper=True, use_lower=True, use_digits=True, use_symbols=True)
            has_upper = any(c in string.ascii_uppercase for c in pwd)
            has_lower = any(c in string.ascii_lowercase for c in pwd)
            has_digit = any(c in string.digits for c in pwd)
            has_symbol = any(c in string.punctuation for c in pwd)
            self.assertTrue(has_upper and has_lower and has_digit and has_symbol)

    def test_generate_password_avoid_ambiguous(self):
        ambiguous = "il1Lo0O"
        for _ in range(20):
            pwd = generate_password(length=20, avoid_ambiguous=True)
            self.assertFalse(any(c in ambiguous for c in pwd))

    def test_generate_passphrase_defaults(self):
        phrase = generate_passphrase()
        words = phrase.split("-")
        self.assertEqual(len(words), 4)
        for w in words:
            self.assertIn(w, WORDLIST)

    def test_generate_passphrase_custom(self):
        phrase = generate_passphrase(num_words=5, separator="_", capitalize=True)
        words = phrase.split("_")
        self.assertEqual(len(words), 5)
        for w in words:
            self.assertTrue(w[0].isupper())

    def test_calculate_entropy_and_strength(self):
        # Entropy for a 16-char password with 94 possible chars ~ 104.8 bits
        pwd = "aB3!cD4@eF5#gH6$"
        entropy = calculate_entropy(pwd)
        self.assertGreater(entropy, 80)
        self.assertEqual(estimate_strength(entropy), "Very Strong")

        # Weak password
        weak_entropy = calculate_entropy("1234")
        self.assertLess(weak_entropy, 30)
        self.assertEqual(estimate_strength(weak_entropy), "Weak")

if __name__ == "__main__":
    unittest.main()
