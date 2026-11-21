# PassCraft 🔐

> A sleek, cryptographically secure CLI tool for generating passwords and diceware-style passphrases with zero external dependencies.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)

---

## ✨ Features

- **Cryptographically Secure:** Powered by Python's built-in `secrets` module (CSPRNG).
- **Flexible Password Generation:** Customize length, character sets (uppercase, lowercase, numbers, symbols), and eliminate visually confusing characters (`l, 1, I, 0, O`).
- **Diceware Passphrase Mode:** Generate memorable multi-word passphrases with customizable separators and capitalization.
- **Entropy & Strength Estimation:** Gauge password resilience with bit-entropy analysis.
- **Zero Dependencies:** Runs on vanilla Python 3 standard library.
- **Full Test Coverage:** Built with automated unit tests for reliability.

---

## 🚀 Quick Start

### Running directly

Clone the repository and run using Python:

```bash
git clone https://github.com/zypherianastrid/passcraft.git
cd passcraft
python -m passcraft
```

### Installation (Optional)

Install locally in editable mode:

```bash
pip install -e .
passcraft --help
```

---

## 📖 Usage Examples

### 1. Default Password (16 characters)
```bash
python -m passcraft
# Output: k9#xP$8m!Qw2@vRt
```

### 2. Custom Length and Multiple Passwords
```bash
python -m passcraft -l 24 -n 3
```

### 3. Avoid Ambiguous Characters (no `l`, `1`, `I`, `0`, `O`)
```bash
python -m passcraft -l 16 --avoid-ambiguous
```

### 4. Diceware Passphrase Mode
```bash
# 4 words separated by hyphens
python -m passcraft -w 4

# 5 words, capitalized, separated by underscores
python -m passcraft -w 5 -s "_" --capitalize
# Output: Blossom_Galaxy_Falcon_Summit_Harbor
```

### 5. Check Password Entropy & Strength
```bash
python -m passcraft -l 20 --show-entropy
# Output:
# 'X*"4vXEhN]6'x%ce@rN
#   [Entropy: 131.1 bits | Strength: Very Strong]
```

---

## 🛠️ Options Cheat Sheet

| Option | Shorthand | Description | Default |
|---|---|---|---|
| `--length` | `-l` | Password length | `16` |
| `--count` | `-n` | Number of passwords/phrases to generate | `1` |
| `--no-upper` | | Exclude uppercase letters (`A-Z`) | `False` |
| `--no-lower` | | Exclude lowercase letters (`a-z`) | `False` |
| `--no-digits` | | Exclude digits (`0-9`) | `False` |
| `--no-symbols` | | Exclude special characters | `False` |
| `--avoid-ambiguous` | | Remove confusing characters (`il1Lo0O`) | `False` |
| `--words` | `-w` | Switch to passphrase mode with N words | `None` |
| `--separator` | `-s` | Word separator in passphrase mode | `"-"` |
| `--capitalize` | `--cap` | Capitalize each word in passphrase | `False` |
| `--show-entropy` | | Display entropy bits and strength rating | `False` |

---

## 🧪 Running Tests

```bash
python -m unittest discover -s tests -v
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
