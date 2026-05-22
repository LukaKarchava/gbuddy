"""Hotspot companion voice — calm, protective, never technical."""

import random

STATES = {
    "calm": {
        "mood": "safe hotspot usage",
        "glow": "#6eb5ff",
        "glow_soft": "#0a1420",
        "glow_mid": "#122030",
    },
    "happy": {
        "mood": "easy browsing day",
        "glow": "#6ee7a8",
        "glow_soft": "#0a1610",
        "glow_mid": "#122818",
    },
    "careful": {
        "mood": "careful — hotspot heating up",
        "glow": "#ffb07a",
        "glow_soft": "#1a1008",
        "glow_mid": "#2a1810",
    },
    "worried": {
        "mood": "close to your safe limit",
        "glow": "#ff9a9a",
        "glow_soft": "#1a0808",
        "glow_mid": "#2a1010",
    },
    "limit": {
        "mood": "protecting your hotspot",
        "glow": "#ef4444",
        "glow_soft": "#200808",
        "glow_mid": "#301010",
    },
}

MESSAGES = {
    "calm": [
        "Your hotspot is chilling. Plenty left.",
        "Calm and in control today.",
        "GBuddy is keeping watch for you.",
    ],
    "happy": [
        "Nice pace on your mobile data.",
        "Easy day — your limit looks healthy.",
        "Smooth hotspot session.",
    ],
    "careful": [
        "You're getting closer to your safe limit.",
        "Maybe pause a big download?",
        "GBuddy is rooting for your leftover data.",
    ],
    "worried": [
        "You are close to your safe limit.",
        "Careful — save some data for later.",
        "Slow down a little if you can.",
    ],
    "limit": [
        "Safe limit reached. GBuddy has your back.",
        "Protecting the data you wanted to save.",
        "Take a breath — you hit your chosen cap.",
    ],
}


class PersonalityEngine:
    def pick_state(self, used_bytes, limit_bytes):
        if limit_bytes <= 0:
            limit_bytes = 3 * 1024 * 1024 * 1024
        pct = used_bytes / limit_bytes
        if pct >= 1.0:
            return "limit"
        if pct >= 0.88:
            return "worried"
        if pct >= 0.72:
            return "careful"
        if pct >= 0.45:
            return "happy"
        return "calm"

    def state_info(self, state_key):
        return STATES[state_key]

    def message(self, state_key):
        return random.choice(MESSAGES[state_key])

    def remaining_line(self, left_bytes, limit_bytes):
        if left_bytes <= 0:
            return "no safe data left today"
        unit = "GB" if left_bytes >= 1024 ** 3 else "MB"
        val = left_bytes / (1024 ** 3) if unit == "GB" else left_bytes / (1024 ** 2)
        if unit == "GB":
            val = f"{val:.1f}"
        else:
            val = f"{int(val)}" if val >= 10 else f"{val:.1f}"
        return f"{val} {unit} left on your safe limit"
