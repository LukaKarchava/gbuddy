"""GBuddy wordmark — G white, Buddy gradient glow."""

import tkinter as tk

import customtkinter as ctk

from gbuddy.ui.components.typography import Typography
from gbuddy.ui.theme import Theme


class GBuddyLogo(ctk.CTkFrame):
    def __init__(self, master, theme: Theme, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.theme = theme
        self.w = 240
        self.h = 52
        self.canvas = tk.Canvas(
            self,
            width=self.w,
            height=self.h,
            bg=theme.bg,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack()
        self._paint()

    def set_bg(self, color):
        self.canvas.configure(bg=color)
        self._paint()

    def _paint(self):
        c = self.canvas
        c.delete("all")
        w, h = self.w, self.h
        cy = h / 2
        font = (Typography.DISPLAY[0], 34, "bold")

        # Soft halo
        for r, col in ((52, "#12182a"), (38, "#151525"), (26, "#181830")):
            c.create_oval(w // 2 - r, cy - r, w // 2 + r, cy + r, fill=col, outline="")

        c.create_text(46, cy, text="G", font=font, fill=self.theme.brand_g, anchor="center")
        # Gradient feel: two-tone Buddy
        c.create_text(
            118, cy, text="Bud", font=font,
            fill=self.theme.brand_buddy_start, anchor="center",
        )
        c.create_text(
            168, cy, text="dy", font=font,
            fill=self.theme.brand_buddy_end, anchor="center",
        )
