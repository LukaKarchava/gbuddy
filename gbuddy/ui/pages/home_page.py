"""Home — hero usage, mascot, mood, session ring."""

import customtkinter as ctk

from gbuddy.ui.components.card import SoftCard
from gbuddy.ui.components.mascot import BuddyMascot
from gbuddy.ui.components.progress_ring import ProgressRing
from gbuddy.ui.components.typography import Typography
from gbuddy.ui.theme import Theme


class HomePage(ctk.CTkFrame):
    def __init__(self, master, theme: Theme):
        super().__init__(master, fg_color="transparent")
        self.theme = theme
        self.grid_columnconfigure(0, weight=1)

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        scroll.grid_columnconfigure(0, weight=1)

        # Hero number
        self.hero_value = ctk.CTkLabel(
            scroll,
            text="0",
            font=Typography.hero_number(72),
            text_color=theme.text,
        )
        self.hero_value.grid(row=0, column=0, pady=(8, 0))

        self.hero_unit = ctk.CTkLabel(
            scroll,
            text="MB today",
            font=Typography.caption(15),
            text_color=theme.muted,
        )
        self.hero_unit.grid(row=1, column=0, pady=(0, 20))

        # Mascot
        self.mascot = BuddyMascot(scroll, theme, size=220)
        self.mascot.grid(row=2, column=0, pady=(0, 8))
        self.mascot.tick_breath()

        self.mood_label = ctk.CTkLabel(
            scroll,
            text="WiFi is napping",
            font=Typography.display(20),
            text_color=theme.text,
        )
        self.mood_label.grid(row=3, column=0)

        self.line_label = ctk.CTkLabel(
            scroll,
            text="A gentle day online",
            font=Typography.body(14),
            text_color=theme.muted,
        )
        self.line_label.grid(row=4, column=0, pady=(4, 24))

        # Session ring card
        ring_card = SoftCard(scroll, theme, elevated=True)
        ring_card.grid(row=5, column=0, sticky="ew", pady=(0, 16))
        ring_card.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(ring_card, fg_color="transparent")
        inner.pack(pady=20)

        self.ring = ProgressRing(inner, theme, size=150, width=9)
        self.ring.pack(side="left", padx=(20, 16))

        side = ctk.CTkFrame(inner, fg_color="transparent")
        side.pack(side="left", fill="y", pady=8)

        ctk.CTkLabel(
            side,
            text="this session",
            font=Typography.caption(12),
            text_color=theme.muted,
        ).pack(anchor="w")

        self.session_val = ctk.CTkLabel(
            side,
            text="0 MB",
            font=Typography.display(26),
            text_color=theme.text,
        )
        self.session_val.pack(anchor="w", pady=(4, 8))

        self.session_cap = ctk.CTkLabel(
            side,
            text="Just getting started",
            font=Typography.caption(12),
            text_color=theme.muted,
            wraplength=140,
            justify="left",
        )
        self.session_cap.pack(anchor="w")

        # Flow in / out — minimal pills
        flow = ctk.CTkFrame(scroll, fg_color="transparent")
        flow.grid(row=6, column=0, sticky="ew", pady=(0, 24))
        flow.grid_columnconfigure((0, 1), weight=1)

        self.in_pill = self._flow_pill(flow, 0, "coming in", "#5eead4")
        self.out_pill = self._flow_pill(flow, 1, "going out", "#f9a8d4")

    def _flow_pill(self, parent, col, title, color):
        f = SoftCard(parent, self.theme)
        f.grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 8, 8 if col == 0 else 0))
        ctk.CTkLabel(
            f, text=title, font=Typography.caption(11), text_color=self.theme.muted
        ).pack(pady=(14, 2))
        val = ctk.CTkLabel(f, text="0", font=Typography.display(22), text_color=color)
        val.pack(pady=(0, 14))
        return val

    def update(self, snapshot):
        from gbuddy.core.tracker import format_bytes, format_bytes_unit

        today = snapshot["today_bytes"]
        self.hero_value.configure(text=format_bytes(today))
        self.hero_unit.configure(text=f"{format_bytes_unit(today)} today")

        state = snapshot["state"]
        info = snapshot["state_info"]
        self.mascot.set_state(state, animate=snapshot.get("mood_changed", False))
        self.mood_label.configure(text=info["mood"])
        self.line_label.configure(text=snapshot["message"])

        self.ring.set_target(snapshot["session_progress"])
        self.ring.animate_step()
        self.session_val.configure(text=f"{format_bytes(snapshot['session_bytes'])} {format_bytes_unit(snapshot['session_bytes'])}")
        self.session_cap.configure(text=snapshot["session_caption"])

        self.in_pill.configure(text=format_bytes(snapshot["down"]))
        self.out_pill.configure(text=format_bytes(snapshot["up"]))
