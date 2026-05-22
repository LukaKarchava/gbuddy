"""
GBuddy data — saves daily usage, streaks, badges, and settings.
Uses a simple JSON file in ~/.config/gbuddy/
"""

import json
import os
from datetime import date, datetime
from pathlib import Path

DATA_DIR = Path.home() / ".config" / "gbuddy"
DATA_FILE = DATA_DIR / "data.json"

DEFAULT = {
    "settings": {
        "monthly_limit_mb": 5000,
        "theme": "mint",
        "launch_startup": False,
        "mini_widget": False,
        "notify_milestones": True,
        "low_usage_mb": 200,
    },
    "today": {
        "date": "",
        "bytes": 0,
        "sent_start": 0,
        "recv_start": 0,
    },
    "month": {"month": "", "bytes": 0},
    "history": [],
    "achievements": {},
    "streak": {"count": 0, "last_date": ""},
    "notified": {"monthly": [], "badges": []},
}


def load_data():
    """Read saved data or create fresh defaults."""
    if not DATA_FILE.exists():
        return fresh_data()

    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return fresh_data()

    merged = DEFAULT.copy()
    for key in DEFAULT:
        if key in data:
            if isinstance(DEFAULT[key], dict):
                merged[key] = {**DEFAULT[key], **data[key]}
            else:
                merged[key] = data[key]
    return merged


def save_data(data):
    """Write data to disk."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def fresh_data():
    return json.loads(json.dumps(DEFAULT))


def today_str():
    return date.today().isoformat()


def month_str():
    return date.today().strftime("%Y-%m")


def rollover_day(data, net_counters):
    """Start a new day — archive yesterday and reset counters."""
    today = data["today"]
    old_date = today.get("date", "")

    if old_date and old_date != today_str():
        day_bytes = today.get("bytes", 0)
        if day_bytes > 0:
            history = data["history"]
            history.append({"date": old_date, "bytes": day_bytes})
            data["history"] = history[-14:]
            data["month"]["bytes"] = data["month"].get("bytes", 0) + day_bytes

        settings = data["settings"]
        if day_bytes <= settings["low_usage_mb"] * 1024 * 1024:
            streak = data["streak"]
            if streak.get("last_date") != old_date:
                streak["count"] = streak.get("count", 0) + 1
                streak["last_date"] = old_date
        else:
            data["streak"]["count"] = 0

    data["today"] = {
        "date": today_str(),
        "bytes": 0,
        "sent_start": net_counters.bytes_sent,
        "recv_start": net_counters.bytes_recv,
    }
    return data


def rollover_month(data):
    """Start a new month bucket."""
    if data["month"].get("month") != month_str():
        data["month"] = {"month": month_str(), "bytes": 0}
    return data


def sync_day_month(data, net_counters):
    """Make sure today/month match calendar and baselines exist."""
    if data["today"].get("date") != today_str():
        data = rollover_day(data, net_counters)
    else:
        if not data["today"].get("sent_start"):
            data["today"]["sent_start"] = net_counters.bytes_sent
            data["today"]["recv_start"] = net_counters.bytes_recv

    data = rollover_month(data)
    return data


def session_bytes(net_counters, session_sent_start, session_recv_start):
    """Bytes used since app opened."""
    up = net_counters.bytes_sent - session_sent_start
    down = net_counters.bytes_recv - session_recv_start
    return up + down


def today_bytes(data, net_counters):
    """Bytes used today (saved + this session)."""
    t = data["today"]
    live = max(0, net_counters.bytes_sent - t["sent_start"])
    live += max(0, net_counters.bytes_recv - t["recv_start"])
    return t.get("bytes", 0) + live


def add_session_to_today(data, session_total):
    """Persist session usage into today's total when closing."""
    data["today"]["bytes"] = data["today"].get("bytes", 0) + session_total
    data["month"]["bytes"] = data["month"].get("bytes", 0) + session_total
    return data


def unlock_badge(data, badge_id):
    """Mark achievement unlocked; returns True if new."""
    achievements = data["achievements"]
    if achievements.get(badge_id):
        return False
    achievements[badge_id] = datetime.now().isoformat()
    data["achievements"] = achievements
    return True


def build_chart_series(data, today_total_bytes, days=7):
    """Return list of (label, bytes) for the last 7 days."""
    from datetime import timedelta

    by_date = {row["date"]: row["bytes"] for row in data.get("history", [])}
    by_date[data["today"]["date"]] = today_total_bytes

    series = []
    for i in range(days - 1, -1, -1):
        d = (date.today() - timedelta(days=i)).isoformat()
        label = datetime.strptime(d, "%Y-%m-%d").strftime("%a")
        series.append((label, by_date.get(d, 0)))
    return series
