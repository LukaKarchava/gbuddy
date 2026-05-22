"""Settings — themes, mascot, notifications."""

import customtkinter as ctk

from gbuddy.ui.components.card import SoftCard
from gbuddy.ui.components.typography import Typography
from gbuddy.ui.theme import THEMES, Theme, MASCOT_STYLES


class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, theme: Theme, on_change):
        super().__init__(master, fg_color="transparent")
        self.theme = theme
        self.on_change = on_change

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(
            scroll, text="Settings", font=Typography.display(26), text_color=theme.text
        ).pack(anchor="w", pady=(4, 20))

        self._section(scroll, "Theme", self._theme_row)
        self._section(scroll, "Mascot look", self._mascot_row)
        self._section(scroll, "Monthly limit (MB)", self._limit_row)
        self.notify_sw = self._toggle(
            scroll, "Gentle milestone alerts", lambda: on_change("notify", None)
        )
        self.startup_sw = self._toggle(
            scroll, "Open when computer starts", lambda: on_change("startup", None)
        )
        self.widget_sw = self._toggle(
            scroll, "Floating mini buddy", lambda: on_change("widget", None)
        )

    def _section(self, parent, title, builder):
        ctk.CTkLabel(
            parent, text=title, font=Typography.caption(12), text_color=self.theme.muted
        ).pack(anchor="w", pady=(12, 6))
        card = SoftCard(parent, self.theme)
        card.pack(fill="x", pady=(0, 8))
        builder(card)

    def _theme_row(self, card):
        self.theme_menu = ctk.CTkOptionMenu(
            card,
            values=list(THEMES.keys()),
            command=lambda v: self.on_change("theme", v),
            fg_color=self.theme.elevated,
            button_color=self.theme.accent_dim,
        )
        self.theme_menu.pack(padx=18, pady=16, anchor="w")

    def _mascot_row(self, card):
        self.mascot_menu = ctk.CTkOptionMenu(
            card,
            values=list(MASCOT_STYLES.keys()),
            command=lambda v: self.on_change("mascot_style", v),
            fg_color=self.theme.elevated,
            button_color=self.theme.accent_dim,
        )
        self.mascot_menu.pack(padx=18, pady=16, anchor="w")

    def _limit_row(self, card):
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=18, pady=16)
        self.limit_entry = ctk.CTkEntry(row, width=120, fg_color=self.theme.elevated)
        self.limit_entry.pack(side="left")
        ctk.CTkButton(
            row,
            text="Save",
            width=80,
            command=lambda: self.on_change("limit", self.limit_entry.get()),
            fg_color=self.theme.accent,
            hover_color=self.theme.accent_dim,
        ).pack(side="left", padx=12)

    def _toggle(self, parent, label, command=None):
        card = SoftCard(parent, self.theme)
        card.pack(fill="x", pady=(0, 8))
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=18, pady=14)
        ctk.CTkLabel(row, text=label, font=Typography.body(14)).pack(side="left")
        sw = ctk.CTkSwitch(row, text="", width=46, command=command)
        sw.pack(side="right")
        return sw

    def load_settings(self, settings):
        self.theme_menu.set(settings.get("theme", "noir"))
        self.mascot_menu.set(settings.get("mascot_style", "soft"))
        self.limit_entry.delete(0, "end")
        self.limit_entry.insert(0, str(settings.get("monthly_limit_mb", 5000)))
        if settings.get("notify_milestones", True):
            self.notify_sw.select()
        if settings.get("launch_startup"):
            self.startup_sw.select()
        if settings.get("mini_widget"):
            self.widget_sw.select()
