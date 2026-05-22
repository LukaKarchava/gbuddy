"""Insights — charts and patterns, still friendly not technical."""

import customtkinter as ctk

from gbuddy.ui.components.card import SoftCard
from gbuddy.ui.components.chart import SmoothChart
from gbuddy.ui.components.typography import Typography
from gbuddy.ui.theme import Theme


class InsightsPage(ctk.CTkFrame):
    def __init__(self, master, theme: Theme):
        super().__init__(master, fg_color="transparent")
        self.theme = theme

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        scroll.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            scroll,
            text="Insights",
            font=Typography.display(26),
            text_color=theme.text,
        ).grid(row=0, column=0, sticky="w", pady=(4, 4))

        ctk.CTkLabel(
            scroll,
            text="gentle patterns from your week",
            font=Typography.caption(13),
            text_color=theme.muted,
        ).grid(row=1, column=0, sticky="w", pady=(0, 20))

        # Weekly bars
        wk = SoftCard(scroll, theme, elevated=True)
        wk.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        ctk.CTkLabel(
            wk, text="This week", font=Typography.body(14), text_color=theme.text
        ).pack(anchor="w", padx=20, pady=(18, 8))
        self.week_chart = SmoothChart(wk, theme, height=150)
        self.week_chart.pack(fill="x", padx=12, pady=(0, 18))

        # Today hourly
        hr = SoftCard(scroll, theme)
        hr.grid(row=3, column=0, sticky="ew", pady=(0, 14))
        ctk.CTkLabel(
            hr, text="Today by hour", font=Typography.body(14), text_color=theme.text
        ).pack(anchor="w", padx=20, pady=(18, 8))
        self.hour_chart = SmoothChart(hr, theme, height=110)
        self.hour_chart.pack(fill="x", padx=12, pady=(0, 18))

        # Stat row
        row = ctk.CTkFrame(scroll, fg_color="transparent")
        row.grid(row=4, column=0, sticky="ew", pady=(0, 20))
        row.grid_columnconfigure((0, 1), weight=1)

        self.avg_card = self._mini_stat(row, 0, "daily average")
        self.peak_card = self._mini_stat(row, 1, "busiest time")

    def _mini_stat(self, parent, col, title):
        c = SoftCard(parent, self.theme)
        c.grid(row=0, column=col, sticky="nsew", padx=(0, 8) if col == 0 else (8, 0))
        ctk.CTkLabel(
            c, text=title, font=Typography.caption(11), text_color=self.theme.muted
        ).pack(pady=(14, 2))
        val = ctk.CTkLabel(
            c, text="—", font=Typography.display(20), text_color=self.theme.text
        )
        val.pack(pady=(0, 14))
        return val

    def update(self, snapshot):
        from gbuddy.core.tracker import format_bytes, format_bytes_unit

        self.week_chart.draw_bars(snapshot["chart_series"], snapshot["accent"])
        self.hour_chart.draw_hourly(snapshot["hourly"], snapshot["accent"])

        avg = snapshot["weekly_avg"]
        self.avg_card.configure(
            text=f"{format_bytes(avg)} {format_bytes_unit(avg)}"
        )
        self.peak_card.configure(text=snapshot["peak_hour"])
