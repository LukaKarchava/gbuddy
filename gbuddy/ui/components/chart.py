"""Minimal smooth bar charts."""

import tkinter as tk

import customtkinter as ctk

from gbuddy.ui.theme import Theme


class SmoothChart(ctk.CTkFrame):
    def __init__(self, master, theme: Theme, height=160, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.theme = theme
        self.canvas = tk.Canvas(
            self,
            height=height,
            bg=theme.surface,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

    def draw_bars(self, series, accent=None):
        c = self.canvas
        c.delete("all")
        c.update_idletasks()
        w = max(c.winfo_width(), 320)
        h = max(c.winfo_height(), 120)
        accent = accent or self.theme.accent
        pad_x, pad_y = 24, 28

        if not series:
            return

        max_v = max(v for _, v in series) or 1
        n = len(series)
        gap = 10
        bar_w = (w - pad_x * 2 - gap * (n - 1)) / n

        for i, (label, value) in enumerate(series):
            bh = max(6, (value / max_v) * (h - pad_y - 32))
            x1 = pad_x + i * (bar_w + gap)
            y1 = h - pad_y - bh
            x2 = x1 + bar_w
            y2 = h - pad_y

            # Rounded-top feel via two rects
            c.create_rectangle(x1, y1 + 8, x2, y2, fill=accent, outline="")
            c.create_rectangle(x1, y1, x2, y1 + 10, fill=accent, outline="")
            c.create_text(
                (x1 + x2) / 2, h - 12,
                text=label,
                fill=self.theme.muted,
                font=("Segoe UI", 9),
            )

    def draw_hourly(self, hours, accent=None):
        """24-hour activity heatline."""
        c = self.canvas
        c.delete("all")
        c.update_idletasks()
        w = max(c.winfo_width(), 320)
        h = max(c.winfo_height(), 100)
        accent = accent or self.theme.accent
        pad = 20
        max_v = max(hours) or 1

        points = []
        for i, v in enumerate(hours):
            x = pad + (i / 23) * (w - pad * 2)
            y = h - pad - (v / max_v) * (h - pad * 2)
            points.extend([x, y])

        if len(points) >= 4:
            c.create_line(*points, fill=accent, width=2, smooth=True)
            for i in range(0, len(points), 2):
                c.create_oval(
                    points[i] - 2, points[i + 1] - 2,
                    points[i] + 2, points[i + 1] + 2,
                    fill=accent, outline="",
                )
