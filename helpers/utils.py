# helpers/utils.py

import random
import re
from datetime import timedelta

# 🌸 SCRIPT / CALLIGRAPHIC FONT MAP
FONT_MAP = {
    'A': '𝑨', 'B': '𝑩', 'C': '𝑪', 'D': '𝑫', 'E': '𝑬', 'F': '𝑭',
    'G': '𝑮', 'H': '𝑯', 'I': '𝑰', 'J': '𝑱', 'K': '𝑲', 'L': '𝑳',
    'M': '𝑴', 'N': '𝑵', 'O': '𝑶', 'P': '𝑷', 'Q': '𝑸', 'R': '𝑹',
    'S': '𝑺', 'T': '𝑻', 'U': '𝑼', 'V': '𝑽', 'W': '𝑾', 'X': '𝑿',
    'Y': '𝒀', 'Z': '𝒁',
    'a': '𝒂', 'b': '𝒃', 'c': '𝒄', 'd': '𝒅', 'e': '𝒆', 'f': '𝒇',
    'g': '𝒈', 'h': '𝒉', 'i': '𝒊', 'j': '𝒋', 'k': '𝒌', 'l': '𝒍',
    'm': '𝒎', 'n': '𝒏', 'o': '𝒐', 'p': '𝒑', 'q': '𝒒', 'r': '𝒓',
    's': '𝒔', 't': '𝒕', 'u': '𝒖', 'v': '𝒗', 'w': '𝒘', 'x': '𝒙',
    'y': '𝒚', 'z': '𝒛'
}

# ---------------- RANDOM PERCENTAGE ----------------
def random_percentage():
    """Returns a random love/crush percentage (1–100)."""
    return random.randint(1, 100)

# ---------------- TIME FORMATTER ----------------
def format_delta(delta: timedelta):
    """Formats timedelta → 2h 5m 10s (daily.py fix)"""
    seconds = int(delta.total_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts)

# ---------------- TEXT STYLIZER ----------------
def stylize_text(text: str) -> str:
    """Converts normal text to Script / Calligraphic font
    Keeps usernames, links, commands safe
    """
    def apply_font(t):
        return "".join(FONT_MAP.get(ch, ch) for ch in t)

    pattern = r"(@\w+|https?://\S+|`[^`]+`|/[a-zA-Z0-9_]+)"
    parts = re.split(pattern, str(text))

    styled = []
    for part in parts:
        if re.match(pattern, part):
            styled.append(part)
        else:
            styled.append(apply_font(part))

    return "".join(styled)
