"""CLI interface for PassCraft."""

import argparse
import sys
from passcraft.generator import (
    generate_password,
    generate_passphrase,
    calculate_entropy,
    estimate_strength,
)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="passcraft",
        description="PassCraft: Secure, cryptographic password & passphrase generator.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  passcraft                     # 16-character secure password
  passcraft -l 24 -n 5          # 5 passwords, 24 characters each
  passcraft --no-symbols        # Alphanumeric only
  passcraft -w 4                # Diceware passphrase with 4 words
  passcraft -w 5 -s "_" --cap   # 5-word capitalized passphrase separated by underscores
  passcraft --show-entropy      # Include entropy bits and strength rating
        """
    )

    # Password options
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=16,
        help="Password length (default: 16, min: 4)"
    )
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=1,
        help="Number of passwords to generate (default: 1)"
    )
    parser.add_argument(
        "--no-upper",
        action="store_true",
        help="Exclude uppercase letters"
    )
    parser.add_argument(
        "--no-lower",
        action="store_true",
        help="Exclude lowercase letters"
    )
    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Exclude digits"
    )
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude symbols/special characters"
    )
    parser.add_argument(
        "--avoid-ambiguous",
        action="store_true",
        help="Avoid visually ambiguous characters (il1Lo0O)"
    )

    # Passphrase options
    parser.add_argument(
        "-w", "--words",
        type=int,
        default=None,
        help="Generate a multi-word passphrase with N words instead of a character password"
    )
    parser.add_argument(
        "-s", "--separator",
        type=str,
        default="-",
        help="Word separator for passphrase mode (default: '-')"
    )
    parser.add_argument(
        "--capitalize", "--cap",
        action="store_true",
        help="Capitalize each word in passphrase mode"
    )

    # Info options
    parser.add_argument(
        "--show-entropy",
        action="store_true",
        help="Display entropy bits and estimated strength rating"
    )

    return parser

def main(args=None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(args)

    try:
        if parsed.words is not None:
            # Passphrase mode
            for _ in range(parsed.count):
                phrase = generate_passphrase(
                    num_words=parsed.words,
                    separator=parsed.separator,
                    capitalize=parsed.capitalize
                )
                print(phrase)
                if parsed.show_entropy:
                    entropy = calculate_entropy(phrase)
                    strength = estimate_strength(entropy)
                    print(f"  [Entropy: {entropy} bits | Strength: {strength}]")
        else:
            # Password mode
            for _ in range(parsed.count):
                pwd = generate_password(
                    length=parsed.length,
                    use_upper=not parsed.no_upper,
                    use_lower=not parsed.no_lower,
                    use_digits=not parsed.no_digits,
                    use_symbols=not parsed.no_symbols,
                    avoid_ambiguous=parsed.avoid_ambiguous,
                )
                print(pwd)
                if parsed.show_entropy:
                    entropy = calculate_entropy(pwd)
                    strength = estimate_strength(entropy)
                    print(f"  [Entropy: {entropy} bits | Strength: {strength}]")

        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
