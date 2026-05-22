"""Safe hotspot limit ring — hero element."""

import tkinter as tk

import customtkinter as ctk

from gbuddy.ui.components.typography import Typography
from gbuddy.ui.theme import Theme


class LimitRing(ctk.CTkFrame):
    def __init__(self, master, theme: Theme, size=176, width=11, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.theme = theme
        self.size = size
        self.width = width
        self._display = 0.0
        self._target = 0.0
        self._color = theme.ring_safe
        self._center_main = "0 / 3 GB"
        self._center_sub = "safe hotspot limit"

        self.canvas = tk.Canvas(
            self,
            width=size,
            height=size,
            bg=theme.bg,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack()

    def set_progress(self, fraction, color):
        self._target = max(0.0, min(1.05, fraction))
        self._color = color

    def set_center(self, main_text, sub_text):
        self._center_main = main_text
        self._center_sub = sub_text

    def animate(self):
        diff = self._target - self._display
        if abs(diff) < 0.006:
            self._display = self._target
            self._paint()
            return
        self._display += diff * 0.12
        self._paint()
        self.after(28, self.animate)

    def _paint(self):
        c = self.canvas
        c.delete("all")
        s = self.size
        cx, cy = s / 2, s / 2
        r = (s - self.width * 2) / 2

        c.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            outline=self.theme.ring_track,
            width=self.width,
        )

        if self._display > 0.01:
            extent = min(360, 360 * self._display)
            c.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=90,
                extent=-extent,
                outline=self._color,
                width=self.width,
                style="arc",
            )

        c.create_text(
            cx, cy - 8,
            text=self._center_main,
            fill=self.theme.text,
            font=(Typography.DISPLAY[0], 17, "bold"),
        )
        c.create_text(
            cx, cy + 14,
            text=self._center_sub,
            fill=self.theme.muted,
            font=(Typography.BODY[0], 10),
        )
