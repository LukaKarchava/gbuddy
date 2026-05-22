"""GBuddy — fixed layout, safe hotspot companion."""

import os
import customtkinter as ctk
import psutil

from gbuddy.config import APP_NAME
from gbuddy.core.personality import PersonalityEngine
from gbuddy.core.storage import Storage
from gbuddy.core.tracker import UsageTracker, format_amount
from gbuddy.ui.components.mascot import BuddyMascot
from gbuddy.ui.components.typography import Typography
from gbuddy.ui.theme import Theme

WIN_W, WIN_H = 480, 720
PAD = 20
CONTENT_W = WIN_W - PAD * 2  # 440


class GBuddyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.theme = Theme()
        self.storage = Storage()
        self.tracker = UsageTracker()
        self.personality = PersonalityEngine()
        self._last_state = None
        self._tick = 0
        self._bar_display = 0.0

        self.title(APP_NAME)
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.minsize(WIN_W, WIN_H)
        self.maxsize(WIN_W, WIN_H)
        self.resizable(False, False)
        self.configure(fg_color=self.theme.bg)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Set window icon
        try:
            import sys
            from PIL import Image, ImageTk
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            icon_path = os.path.join(base_path, "icon.png")
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                self.icon_img = ImageTk.PhotoImage(img)
                self.wm_iconphoto(True, self.icon_img)
        except Exception:
            pass

        self.storage.sync_calendar(psutil.net_io_counters())
        self._build()
        self._apply_mood("calm")
        self.after(500, self._loop)

    def _build(self):
        # Header Area
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=PAD, pady=(20, 16))

        logo_box = ctk.CTkFrame(header, fg_color="transparent")
        logo_box.pack()

        ctk.CTkLabel(
            logo_box,
            text="GBuddy",
            font=Typography.brand(26),
            text_color=self.theme.text,
        ).pack(side="left")

        # Premium dot with glow
        dot_frame = ctk.CTkFrame(logo_box, fg_color="transparent")
        dot_frame.pack(side="left", padx=(8, 0))
        
        self.logo_dot = ctk.CTkLabel(
            dot_frame,
            text="●",
            font=Typography.brand(18),
            text_color=self.theme.brand_primary,
        )
        self.logo_dot.pack()

        ctk.CTkLabel(
            header,
            text="Your calm hotspot companion",
            font=Typography.caption(12, weight="bold"),
            text_color=self.theme.muted,
        ).pack(pady=(2, 0))

        # Main Card (Container)
        main_card = ctk.CTkFrame(self, fg_color=self.theme.card, corner_radius=28)
        main_card.pack(fill="both", expand=True, padx=PAD, pady=(0, 20))

        inner = ctk.CTkFrame(main_card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=22, pady=22)

        # 1. Mascot & Usage (Primary Focus)
        hero_section = ctk.CTkFrame(inner, fg_color="transparent")
        hero_section.pack(fill="x")

        self.mascot = BuddyMascot(hero_section, self.theme, size=140)
        self.mascot.pack(pady=(0, 10))
        self.mascot.tick_breath()

        self.whisper = ctk.CTkLabel(
            hero_section,
            text="safe hotspot usage",
            font=Typography.caption(13, weight="bold"),
            text_color=self.theme.accent,
        )
        self.whisper.pack(pady=(0, 12))

        # Stats Grid
        stats_frame = ctk.CTkFrame(inner, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 18))

        self.used_row = self._stat_row(stats_frame, "Used today")
        self.limit_row = self._stat_row(stats_frame, "Your limit")
        self.left_row = self._stat_row(stats_frame, "Still safe")

        # Progress Bar (Premium)
        self.progress = ctk.CTkProgressBar(
            inner,
            height=12,
            corner_radius=6,
            fg_color=self.theme.card_inner,
            progress_color=self.theme.accent_bar,
            border_width=0,
        )
        self.progress.pack(fill="x", pady=(0, 6))
        self.progress.set(0)

        self.pct_lbl = ctk.CTkLabel(
            inner,
            text="0% used",
            font=Typography.tiny(11, weight="bold"),
            text_color=self.theme.muted,
        )
        self.pct_lbl.pack(anchor="e", pady=(0, 18))

        # 2. Limit Management
        self.limit_card = ctk.CTkFrame(
            inner, 
            fg_color=self.theme.card_inner, 
            corner_radius=18,
            border_width=1,
            border_color="#27272a"
        )
        self.limit_card.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            self.limit_card,
            text="Set Safe Limit",
            font=Typography.caption(11, weight="bold"),
            text_color=self.theme.muted,
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=16, pady=(12, 6))

        self.limit_entry = ctk.CTkEntry(
            self.limit_card,
            width=70,
            height=34,
            corner_radius=10,
            fg_color=self.theme.card,
            border_width=1,
            border_color="#3f3f46",
            font=Typography.body(14, weight="bold"),
            justify="center",
        )
        self.limit_entry.grid(row=1, column=0, padx=(16, 8), pady=(0, 16))
        gb = self.storage.settings.get("hotspot_limit_mb", 3072) / 1024
        self.limit_entry.insert(0, f"{gb:.1f}")
        self.limit_entry.bind("<Return>", self._save_limit)

        ctk.CTkLabel(
            self.limit_card,
            text="GB",
            font=Typography.caption(12, weight="bold"),
            text_color=self.theme.text,
        ).grid(row=1, column=1, sticky="w", pady=(0, 16))

        self.save_btn = ctk.CTkButton(
            self.limit_card,
            text="Save limit",
            width=100,
            height=34,
            corner_radius=10,
            fg_color=self.theme.brand_primary,
            hover_color="#059669",
            text_color="#ffffff",
            font=Typography.caption(12, weight="bold"),
            command=self._save_limit,
        )
        self.save_btn.grid(row=1, column=2, padx=(8, 16), pady=(0, 16), sticky="e")
        self.limit_card.grid_columnconfigure(1, weight=1)

        # 3. Auto-Protect & Autostart
        util_frame = ctk.CTkFrame(inner, fg_color="transparent")
        util_frame.pack(fill="x")

        self.auto_off_var = ctk.BooleanVar(value=self.storage.settings.get("auto_protect", False))
        self.auto_off_cb = ctk.CTkCheckBox(
            util_frame,
            text="Auto-disconnect WiFi",
            font=Typography.tiny(11, weight="bold"),
            variable=self.auto_off_var,
            command=self._toggle_auto_protect,
            border_width=2,
            corner_radius=5,
            checkbox_width=18,
            checkbox_height=18,
            fg_color=self.theme.brand_primary,
            hover_color="#059669",
        )
        self.auto_off_cb.pack(side="left")

        self.autostart_var = ctk.BooleanVar(value=self.storage.settings.get("autostart", False))
        self.autostart_cb = ctk.CTkCheckBox(
            util_frame,
            text="Start with laptop",
            font=Typography.tiny(11, weight="bold"),
            variable=self.autostart_var,
            command=self._toggle_autostart,
            border_width=2,
            corner_radius=5,
            checkbox_width=18,
            checkbox_height=18,
            fg_color=self.theme.brand_primary,
            hover_color="#059669",
        )
        self.autostart_cb.pack(side="left", padx=(12, 0))

        # Incoming / Outgoing
        flow_frame = ctk.CTkFrame(inner, fg_color="transparent")
        flow_frame.pack(fill="x", pady=(10, 0))

        self.in_val = self._mini_pill(flow_frame, 0, "IN", self.theme.flow_in)
        self.out_val = self._mini_pill(flow_frame, 1, "OUT", self.theme.flow_out)

        # Message Bar
        self.message_lbl = ctk.CTkLabel(
            main_card,
            text="Your hotspot is chilling.",
            font=Typography.tiny(11),
            text_color=self.theme.muted,
            height=30,
        )
        self.message_lbl.pack(side="bottom", pady=(0, 12))

        # Footer
        ctk.CTkLabel(
            self,
            text="crafted with precision by Luka Karchava",
            font=Typography.tiny(9),
            text_color="#27272a",
        ).pack(side="bottom", pady=(0, 8))

        # Check for onboarding
        if not self.storage.settings.get("onboarded"):
            self.after(1000, self._show_onboarding)

    def _show_onboarding(self):
        """Simple one-time onboarding overlay."""
        overlay = ctk.CTkFrame(self, fg_color="#000000", corner_radius=28)
        overlay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.45)
        
        inner = ctk.CTkFrame(overlay, fg_color="transparent")
        inner.pack(expand=True, padx=30)
        
        ctk.CTkLabel(
            inner,
            text="Using phone hotspot?",
            font=Typography.display(20),
            text_color="#ffffff",
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            inner,
            text="GBuddy helps protect your mobile data by warning you before you exceed your safe limit.",
            font=Typography.body(13),
            text_color="#a1a1aa",
            wraplength=300,
            justify="center",
        ).pack(pady=(0, 24))
        
        def close_onboarding():
            self.storage.settings["onboarded"] = True
            self.storage.save()
            overlay.destroy()
            
        ctk.CTkButton(
            inner,
            text="Got it",
            font=Typography.caption(12, weight="bold"),
            fg_color=self.theme.brand_primary,
            hover_color="#059669",
            command=close_onboarding,
            corner_radius=10,
            height=36,
        ).pack()

    def _toggle_auto_protect(self):
        self.storage.settings["auto_protect"] = self.auto_off_var.get()
        self.storage.save()

    def _toggle_autostart(self):
        enabled = self.autostart_var.get()
        self.storage.settings["autostart"] = enabled
        self.storage.save()
        
        import platform
        import os
        if platform.system() == "Linux":
            autostart_dir = os.path.expanduser("~/.config/autostart")
            os.makedirs(autostart_dir, exist_ok=True)
            desktop_file = os.path.join(autostart_dir, "gbuddy.desktop")
            
            if enabled:
                # Find executable path
                import sys
                exe = sys.executable
                script = os.path.abspath("main.py")
                icon_path = os.path.abspath("icon.png")
                content = f"""[Desktop Entry]
Type=Application
Exec={exe} {script}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=GBuddy
Comment=Safe mobile hotspot companion
Icon={icon_path}
"""
                with open(desktop_file, "w") as f:
                    f.write(content)
            else:
                if os.path.exists(desktop_file):
                    os.remove(desktop_file)

    def _save_limit(self, event=None):
        try:
            val = self.limit_entry.get().strip().replace(",", ".")
            if not val:
                return
            gb = float(val)
            if gb <= 0:
                raise ValueError("Limit must be positive")
            
            mb = int(gb * 1024)
            if mb < 100:
                mb = 100
                self.limit_entry.delete(0, "end")
                self.limit_entry.insert(0, "0.1")

            self.storage.settings["hotspot_limit_mb"] = mb
            self.storage.save()
            
            # Update UI immediately
            limit_b = self._limit_bytes()
            self.limit_row.configure(text=format_amount(limit_b))
            self._loop() # Force UI refresh
            
            # Show toast feedback
            self._show_toast("Limit saved successfully", self.theme.brand_primary)
            
            # Success Glow
            self.limit_card.configure(border_color=self.theme.brand_primary)
            self.after(600, lambda: self.limit_card.configure(border_color="#27272a"))
            
        except ValueError:
            self._show_toast("Invalid limit amount", self.theme.accent_danger)

    def _show_toast(self, text, color):
        """Animated premium toast feedback."""
        toast = ctk.CTkFrame(
            self,
            fg_color=color,
            corner_radius=14,
            height=40,
        )
        # Position toast above the limit card
        toast.place(relx=0.5, rely=0.62, anchor="center")
        
        lbl = ctk.CTkLabel(
            toast,
            text=text,
            font=Typography.caption(11, weight="bold"),
            text_color="#ffffff",
            padx=20,
        )
        lbl.pack(expand=True, fill="both")
        
        self.after(2000, lambda: toast.destroy())

    def _bar_color(self, pct):
        if pct >= 1.0:
            return self.theme.accent_danger
        if pct >= 0.85:
            return self.theme.accent_warn
        return self.theme.accent_bar

    def _apply_mood(self, state):
        info = self.personality.state_info(state)
        self.whisper.configure(text=info["mood"], text_color=info["glow"])
        self.mascot.set_bg(self.theme.card)

    def _smooth_bar(self, target):
        """Smooth progress animation with color blending."""
        current = self.progress.get()
        # Responsive easing
        step = (target - current) * 0.12
        
        if abs(step) < 0.001:
            self.progress.set(target)
            self.progress.configure(progress_color=self._bar_color(target))
            return
            
        new_val = current + step
        self.progress.set(new_val)
        self.progress.configure(progress_color=self._bar_color(new_val))
        self.after(35, lambda: self._smooth_bar(target))

    def _loop(self):
        net, _ = self.tracker.sample()
        self.storage.sync_calendar(net)

        t = self.storage.data["today"]
        total, up, down = UsageTracker.session_split(
            net, t["sent_start"], t["recv_start"]
        )
        limit_b = self._limit_bytes()
        left = max(0, limit_b - total)
        pct = min(1.0, total / limit_b) if limit_b else 0
        pct_int = int(pct * 100)
        state = self.personality.pick_state(total, limit_b)
        
        # Override mascot to worried if limit is reached
        display_state = "worried" if state == "limit" else state

        if display_state != self._last_state:
            self._last_state = display_state
            self.mascot.set_state(display_state, animate=True)
            self._apply_mood(state)

        self.used_row.configure(text=format_amount(total))
        self.limit_row.configure(text=format_amount(limit_b))
        self.left_row.configure(text=format_amount(left))
        self.pct_lbl.configure(text=f"{pct_int}% used")
        
        # Smooth progress bar update
        self._smooth_bar(pct)

        self.in_val.configure(text=format_amount(down))
        self.out_val.configure(text=format_amount(up))

        if state == "limit":
            self.message_lbl.configure(
                text="Limit reached. GBuddy is protecting your hotspot.",
                text_color=self.theme.accent_danger,
            )
            # Auto-off logic
            if self.storage.settings.get("auto_protect") and not self.storage.settings.get("limit_hit_notified"):
                from gbuddy.core.hotspot_protect import disable_wifi
                if disable_wifi():
                    self.message_lbl.configure(text="WiFi turned off to protect mobile data.")
                else:
                    self.message_lbl.configure(text="Could not turn off WiFi automatically.")
                self.storage.settings["limit_hit_notified"] = True
                self.storage.save()
        elif self._tick % 10 == 0:
            self.message_lbl.configure(
                text=self.personality.message(state),
                text_color=self.theme.muted,
            )
            # Reset notification flag if we are below limit again
            if total < limit_b:
                self.storage.settings["limit_hit_notified"] = False

        self._tick += 1
        if self._tick % 25 == 0:
            self.storage.save()

        self.after(1000, self._loop)

    def _stat_row(self, parent, label):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=4)
        row.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            row,
            text=label,
            font=Typography.caption(12, weight="bold"),
            text_color=self.theme.muted,
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        val = ctk.CTkLabel(
            row,
            text="—",
            font=Typography.stat(18),
            text_color=self.theme.text,
            anchor="e",
        )
        val.grid(row=0, column=1, sticky="e")
        return val

    def _mini_pill(self, parent, col, label, color):
        pill = ctk.CTkFrame(parent, fg_color=self.theme.card_inner, corner_radius=10)
        pill.pack(side="left", padx=3)
        
        ctk.CTkLabel(pill, text=label, font=Typography.tiny(8), text_color=self.theme.muted).pack(side="left", padx=(6, 2))
        val = ctk.CTkLabel(pill, text="0 MB", font=Typography.tiny(9), text_color=color)
        val.pack(side="left", padx=(0, 6))
        return val

    def _limit_bytes(self):
        mb = self.storage.settings.get("hotspot_limit_mb", 3072)
        return max(100, mb) * 1024 * 1024

    def _on_close(self):
        self.storage.persist_today(psutil.net_io_counters())
        self.storage.save()
        self.destroy()
