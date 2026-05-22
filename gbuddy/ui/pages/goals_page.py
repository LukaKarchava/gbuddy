"""Goals — limits, streaks, badges."""

import customtkinter as ctk

from gbuddy.ui.components.card import SoftCard
from gbuddy.ui.components.typography import Typography
from gbuddy.ui.theme import Theme

ACHIEVEMENTS = {
    "hello": ("👋", "Met GBuddy"),
    "day_100": ("💯", "100 MB day"),
    "chill_streak": ("🌿", "3 chill days"),
    "month_half": ("🎯", "Under half limit"),
    "speedster": ("🚀", "Fast download"),
}


class GoalsPage(ctk.CTkFrame):
    def __init__(self, master, theme: Theme):
        super().__init__(master, fg_color="transparent")
        self.theme = theme

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        scroll.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            scroll, text="Goals", font=Typography.display(26), text_color=theme.text
        ).grid(row=0, column=0, sticky="w", pady=(4, 20))

        # Monthly
        mc = SoftCard(scroll, theme, elevated=True)
        mc.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        ctk.CTkLabel(
            mc, text="Monthly gentle limit", font=Typography.caption(12), text_color=theme.muted
        ).pack(anchor="w", padx=22, pady=(18, 4))
        self.month_val = ctk.CTkLabel(
            mc, text="0%", font=Typography.hero_number(48), text_color=theme.accent
        )
        self.month_val.pack(anchor="w", padx=22)
        self.month_sub = ctk.CTkLabel(
            mc, text="", font=Typography.caption(13), text_color=theme.muted
        )
        self.month_sub.pack(anchor="w", padx=22, pady=(0, 8))
        self.month_bar = ctk.CTkProgressBar(
            mc, height=8, corner_radius=6, progress_color=theme.accent, fg_color=theme.elevated
        )
        self.month_bar.pack(fill="x", padx=22, pady=(0, 22))
        self.month_bar.set(0)

        # Streak
        sc = SoftCard(scroll, theme)
        sc.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        ctk.CTkLabel(
            sc, text="chill-day streak", font=Typography.caption(12), text_color=theme.muted
        ).pack(anchor="w", padx=22, pady=(16, 0))
        self.streak_val = ctk.CTkLabel(
            sc, text="0", font=Typography.hero_number(40), text_color=theme.text
        )
        self.streak_val.pack(anchor="w", padx=22, pady=(0, 16))

        ctk.CTkLabel(
            scroll, text="badges", font=Typography.body(15), text_color=theme.muted
        ).grid(row=3, column=0, sticky="w", pady=(8, 10))

        self.badge_grid = ctk.CTkFrame(scroll, fg_color="transparent")
        self.badge_grid.grid(row=4, column=0, sticky="ew")

    def _render_badges(self, unlocked):
        for w in self.badge_grid.winfo_children():
            w.destroy()
        for i, (bid, (icon, name)) in enumerate(ACHIEVEMENTS.items()):
            on = bid in unlocked
            c = SoftCard(
                self.badge_grid,
                self.theme,
                elevated=on,
            )
            c.grid(row=i // 2, column=i % 2, padx=6, pady=6, sticky="nsew")
            self.badge_grid.grid_columnconfigure(i % 2, weight=1)
            ctk.CTkLabel(
                c,
                text=f"{icon}  {name}" if on else f"○  {name}",
                font=Typography.body(13, "bold" if on else "normal"),
                text_color=self.theme.text if on else self.theme.muted,
            ).pack(padx=16, pady=14)

    def update(self, snapshot):
        from gbuddy.core.tracker import format_bytes, format_bytes_unit

        pct = snapshot["month_pct"]
        self.month_val.configure(text=f"{pct}%")
        lim = snapshot["monthly_limit_mb"]
        used = snapshot["month_bytes"]
        self.month_sub.configure(
            text=f"{format_bytes(used)} {format_bytes_unit(used)} of {lim} MB"
        )
        self.month_bar.set(min(1.0, pct / 100))
        self.streak_val.configure(text=str(snapshot["streak"]))
        self._render_badges(snapshot["achievements"])
