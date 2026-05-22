"""Floating mini companion window."""

import customtkinter as ctk

from gbuddy.ui.components.typography import Typography
from gbuddy.ui.theme import Theme


class MiniWidget(ctk.CTkToplevel):
    def __init__(self, master, theme: Theme):
        super().__init__(master)
        self.theme = theme
        self.overrideredirect(False)
        self.title("GBuddy")
        self.geometry("240x120")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color=theme.bg)

        self.value = ctk.CTkLabel(
            self,
            text="0 MB",
            font=Typography.display(22),
            text_color=theme.text,
        )
        self.value.pack(pady=(18, 2))

        self.sub = ctk.CTkLabel(
            self,
            text="today",
            font=Typography.caption(12),
            text_color=theme.muted,
        )
        self.sub.pack()

        self.speed = ctk.CTkLabel(
            self,
            text="↓ —",
            font=Typography.caption(11),
            text_color=theme.accent,
        )
        self.speed.pack(pady=(6, 14))

    def refresh(self, today_text, speed_text):
        self.value.configure(text=today_text)
        self.speed.configure(text=speed_text)
