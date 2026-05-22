"""Persistent data — daily/monthly usage, streaks, badges, hourly patterns."""

import json
from datetime import date, datetime, timedelta
from pathlib import Path

DATA_DIR = Path.home() / ".config" / "gbuddy"
DATA_FILE = DATA_DIR / "data.json"

DEFAULT = {
    "settings": {
        "hotspot_limit_mb": 3072,
        "auto_protect": False,
        "limit_hit_notified": False,
        "onboarded": False,
        "autostart": False,
    },
    "today": {"date": "", "bytes": 0, "sent_start": 0, "recv_start": 0},
    "month": {"month": "", "bytes": 0},
    "history": [],
    "hourly": {},
    "achievements": {},
    "streak": {"count": 0, "last_date": ""},
    "notified": {"monthly": [], "badges": []},
}


class Storage:
    """Load, save, and update GBuddy data."""

    def __init__(self):
        self.data = self._load()

    def _load(self):
        if not DATA_FILE.exists():
            return json.loads(json.dumps(DEFAULT))
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError):
            return json.loads(json.dumps(DEFAULT))

        merged = json.loads(json.dumps(DEFAULT))
        for key, default in DEFAULT.items():
            if key in raw:
                if isinstance(default, dict):
                    merged[key] = {**default, **raw[key]}
                else:
                    merged[key] = raw[key]
        return merged

    def save(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    @property
    def settings(self):
        return self.data["settings"]

    def today_str(self):
        return date.today().isoformat()

    def month_str(self):
        return date.today().strftime("%Y-%m")

    def sync_calendar(self, net):
        today = self.data["today"]
        old_date = today.get("date", "")

        if old_date and old_date != self.today_str():
            day_bytes = today.get("bytes", 0)
            if day_bytes > 0:
                self.data["history"].append({"date": old_date, "bytes": day_bytes})
                self.data["history"] = self.data["history"][-14:]
                self.data["month"]["bytes"] = self.data["month"].get("bytes", 0) + day_bytes

            limit = self.settings["low_usage_mb"] * 1024 * 1024
            if day_bytes <= limit:
                streak = self.data["streak"]
                if streak.get("last_date") != old_date:
                    streak["count"] = streak.get("count", 0) + 1
                    streak["last_date"] = old_date
            else:
                self.data["streak"]["count"] = 0

            self.data["today"] = {
                "date": self.today_str(),
                "bytes": 0,
                "sent_start": net.bytes_sent,
                "recv_start": net.bytes_recv,
            }
        elif today.get("date") != self.today_str():
            self.data["today"] = {
                "date": self.today_str(),
                "bytes": 0,
                "sent_start": net.bytes_sent,
                "recv_start": net.bytes_recv,
            }
        else:
            if not today.get("sent_start"):
                today["sent_start"] = net.bytes_sent
                today["recv_start"] = net.bytes_recv

        if self.data["month"].get("month") != self.month_str():
            self.data["month"] = {"month": self.month_str(), "bytes": 0}

        return self

    def today_live_bytes(self, net):
        t = self.data["today"]
        live = max(0, net.bytes_sent - t["sent_start"])
        live += max(0, net.bytes_recv - t["recv_start"])
        return t.get("bytes", 0) + live

    def month_total_bytes(self, today_bytes):
        return self.data["month"].get("bytes", 0) + today_bytes

    def record_hourly(self, session_delta_bytes):
        """Add bytes to current hour bucket for activity patterns."""
        key = self.today_str()
        hours = self.data.setdefault("hourly", {}).setdefault(key, [0] * 24)
        hour = datetime.now().hour
        hours[hour] += session_delta_bytes

    def chart_series(self, today_bytes, days=7):
        by_date = {r["date"]: r["bytes"] for r in self.data.get("history", [])}
        by_date[self.data["today"]["date"]] = today_bytes
        series = []
        for i in range(days - 1, -1, -1):
            d = (date.today() - timedelta(days=i)).isoformat()
            label = datetime.strptime(d, "%Y-%m-%d").strftime("%a")
            series.append((label, by_date.get(d, 0)))
        return series

    def hourly_today(self):
        return self.data.get("hourly", {}).get(self.today_str(), [0] * 24)

    def peak_hour_label(self):
        hours = self.hourly_today()
        if not any(hours):
            return "—"
        peak = max(range(24), key=lambda h: hours[h])
        if hours[peak] == 0:
            return "Quiet day"
        start = peak % 12 or 12
        suffix = "am" if peak < 12 else "pm"
        end = (peak + 1) % 12 or 12
        end_s = "am" if (peak + 1) % 24 < 12 else "pm"
        return f"{start}{suffix} – {end}{end_s}"

    def weekly_average(self, today_bytes):
        series = self.chart_series(today_bytes, days=7)
        total = sum(b for _, b in series)
        return total / max(len(series), 1)

    def persist_today(self, net):
        t = self.data["today"]
        live = max(0, net.bytes_sent - t["sent_start"]) + max(
            0, net.bytes_recv - t["recv_start"]
        )
        t["bytes"] = t.get("bytes", 0) + live
        t["sent_start"] = net.bytes_sent
        t["recv_start"] = net.bytes_recv

    def unlock_badge(self, badge_id):
        if self.data["achievements"].get(badge_id):
            return False
        self.data["achievements"][badge_id] = datetime.now().isoformat()
        return True
