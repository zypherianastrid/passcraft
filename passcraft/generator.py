"""Core generator logic for PassCraft."""

import math
import secrets
import string

# Curated wordlist for diceware-style passphrases
WORDLIST = [
    "acorn", "amber", "anchor", "anthem", "apex", "apple", "apron", "arch", "arrow", "atlas",
    "beacon", "blaze", "blink", "bloom", "breeze", "bridge", "bright", "brook", "cabin", "cactus",
    "canyon", "castle", "cedar", "charm", "cherry", "cipher", "cliff", "clover", "comet", "compass",
    "copper", "coral", "cosmos", "crane", "crest", "crystal", "dawn", "delta", "drift", "eagle",
    "echo", "ember", "falcon", "fern", "flare", "flint", "forest", "fossil", "frost", "galaxy",
    "glade", "glacier", "glow", "granite", "grove", "harbor", "haven", "hawk", "hazel", "helix",
    "horizon", "humming", "island", "ivory", "jasper", "jungle", "lagoon", "lantern", "lark", "leaf",
    "legacy", "light", "lily", "lotus", "lunar", "maple", "meadow", "meteor", "mist", "monarch",
    "moon", "moss", "nebula", "nectar", "nexus", "oasis", "ocean", "olive", "onyx", "opal",
    "orbit", "orchid", "path", "peak", "pebble", "petal", "phoenix", "pine", "pioneer", "planet",
    "polar", "prism", "pulse", "quarry", "quartz", "quest", "radiant", "rain", "ravine", "reef",
    "ridge", "river", "robin", "sage", "sapphire", "shadow", "shiver", "sierra", "silver", "solar",
    "spark", "spirit", "spring", "star", "stream", "summit", "sunflower", "sunset", "talon", "temple",
    "thunder", "tide", "tiger", "timber", "topaz", "trail", "tropic", "tulip", "twilight", "valley",
    "velvet", "venture", "vessel", "violet", "vista", "vortex", "voyage", "walnut", "wave", "whisper",
    "willow", "wind", "winter", "zenith", "zephyr"
]

AMBIGUOUS_CHARS = "il1Lo0O"

def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    avoid_ambiguous: bool = False
) -> str:
    """Generate a cryptographically secure random password."""
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    pools = []
    guaranteed = []

    if use_upper:
        chars = string.ascii_uppercase
        if avoid_ambiguous:
            chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
        if chars:
            pools.append(chars)
            guaranteed.append(secrets.choice(chars))

    if use_lower:
        chars = string.ascii_lowercase
        if avoid_ambiguous:
            chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
        if chars:
            pools.append(chars)
            guaranteed.append(secrets.choice(chars))

    if use_digits:
        chars = string.digits
        if avoid_ambiguous:
            chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
        if chars:
            pools.append(chars)
            guaranteed.append(secrets.choice(chars))

    if use_symbols:
        chars = string.punctuation
        if avoid_ambiguous:
            chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
        if chars:
            pools.append(chars)
            guaranteed.append(secrets.choice(chars))

    if not pools:
        raise ValueError("At least one character set must be enabled and non-empty.")

    all_chars = "".join(pools)
    remaining_length = length - len(guaranteed)
    remaining = [secrets.choice(all_chars) for _ in range(remaining_length)]

    combined = guaranteed + remaining
    # Fisher-Yates shuffle using cryptographically secure random
    for i in range(len(combined) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        combined[i], combined[j] = combined[j], combined[i]

    return "".join(combined)

def generate_passphrase(
    num_words: int = 4,
    separator: str = "-",
    capitalize: bool = False
) -> str:
    """Generate a memorable diceware-style passphrase."""
    if num_words < 2:
        raise ValueError("Passphrase must contain at least 2 words.")

    words = [secrets.choice(WORDLIST) for _ in range(num_words)]
    if capitalize:
        words = [w.capitalize() for w in words]

    return separator.join(words)

def calculate_entropy(password: str) -> float:
    """Estimate password entropy in bits."""
    if not password:
        return 0.0

    pool_size = 0
    if any(c in string.ascii_lowercase for c in password):
        pool_size += 26
    if any(c in string.ascii_uppercase for c in password):
        pool_size += 26
    if any(c in string.digits for c in password):
        pool_size += 10
    if any(c in string.punctuation for c in password):
        pool_size += len(string.punctuation)
    if any(c == ' ' for c in password):
        pool_size += 1

    if pool_size == 0:
        pool_size = len(set(password))

    return round(len(password) * math.log2(pool_size), 1)

def estimate_strength(entropy: float) -> str:
    """Classify password strength based on entropy bits."""
    if entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Moderate"
    elif entropy < 80:
        return "Strong"
    else:
        return "Very Strong"
