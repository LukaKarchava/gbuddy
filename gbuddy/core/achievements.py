"""Badge unlock rules."""

from gbuddy.core import notifications as notify_mod

ACHIEVEMENTS = {
    "hello": "Met GBuddy",
    "day_100": "100 MB in one day",
    "chill_streak": "3 chill days in a row",
    "month_half": "Under half your monthly limit",
    "speedster": "5 MB/s download moment",
}


def check_all(storage, today_b, month_b, month_pct, down_bps):
    unlock(storage, "hello")
    if today_b >= 100 * 1024 * 1024:
        unlock(storage, "day_100")
    if storage.data["streak"].get("count", 0) >= 3:
        unlock(storage, "chill_streak")
    if month_pct < 50 and month_b > 50 * 1024 * 1024:
        unlock(storage, "month_half")
    if down_bps >= 5 * 1024 * 1024:
        unlock(storage, "speedster")


def unlock(storage, badge_id):
    notified = storage.data["notified"].setdefault("badges", [])
    if badge_id in notified:
        return
    if storage.unlock_badge(badge_id):
        notified.append(badge_id)
        if storage.settings.get("notify_milestones", True):
            title = ACHIEVEMENTS.get(badge_id, "New badge")
            notify_mod.notify("GBuddy", f"Unlocked: {title}")
        storage.save()
        return True
    return False


def check_milestones(storage, month_pct):
    if not storage.settings.get("notify_milestones", True):
        return
    from gbuddy.config import MILESTONE_PERCENTS

    done = storage.data["notified"].setdefault("monthly", [])
    for m in MILESTONE_PERCENTS:
        if month_pct >= m and m not in done:
            done.append(m)
            notify_mod.notify(
                "GBuddy",
                f"You've reached {m}% of your monthly gentle limit.",
            )
    storage.save()
