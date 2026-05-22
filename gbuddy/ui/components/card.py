"""Soft elevated surfaces — minimal borders."""

import customtkinter as ctk

from gbuddy.ui.theme import Theme


class SoftCard(ctk.CTkFrame):
    """Rounded card with subtle fill, no harsh outlines."""

    def __init__(self, master, theme: Theme, elevated=False, **kwargs):
        fg = theme.elevated if elevated else theme.surface
        super().__init__(
            master,
            fg_color=fg,
            corner_radius=24,
            border_width=0,
            **kwargs,
        )
        self.theme = theme
