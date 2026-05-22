"""Professional desktop companion mascot — high quality version."""

import math
import tkinter as tk
import customtkinter as ctk
from gbuddy.core.personality import STATES
from gbuddy.ui.theme import Theme

class BuddyMascot(ctk.CTkFrame):
    def __init__(self, master, theme: Theme, size=140, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.theme = theme
        self.size = size
        self.state = "calm"
        self._breath = 0.0
        self._blink = 0.0
        self._is_blinking = False
        
        self.canvas = tk.Canvas(
            self,
            width=size,
            height=size,
            bg=theme.card,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack()

    def set_bg(self, color):
        self.canvas.configure(bg=color)
        self._paint()

    def set_state(self, state, animate=True):
        if state == self.state:
            return
        self.state = state
        self._paint()

    def tick_breath(self):
        self._breath += 0.05
        # Random blink logic
        if not self._is_blinking and math.sin(self._breath * 0.3) > 0.98:
            self._is_blinking = True
            self._blink = 0.0
        
        if self._is_blinking:
            self._blink += 0.3
            if self._blink > math.pi:
                self._is_blinking = False
                self._blink = 0.0

        self._paint()
        self.after(50, self.tick_breath)

    def _paint(self):
        c = self.canvas
        c.delete("all")
        s = self.size
        cx, cy = s / 2, s / 2
        
        # Smooth float animation
        offset = math.sin(self._breath) * 4
        cy += offset
        
        info = STATES.get(self.state, STATES["calm"])
        
        # 1. Premium Soft Shadow (scales with float)
        shadow_w = s * 0.4 * (1 - offset/40)
        shadow_h = 6
        c.create_oval(cx - shadow_w, s - 15, cx + shadow_w, s - 15 + shadow_h, fill="#0c0c0e", outline="")

        # 2. Outer Soft Glow
        gr = s * 0.44
        c.create_oval(cx - gr, cy - gr, cx + gr, cy + gr, fill=info["glow_soft"], outline="")
        
        # 3. Main Body
        bw, bh = s * 0.58, s * 0.68
        c.create_oval(cx - bw/2, cy - bh/2 + 2, cx + bw/2, cy + bh/2 + 2, fill="#e4e4e7", outline="")
        c.create_oval(cx - bw/2, cy - bh/2, cx + bw/2, cy + bh/2, fill=self.theme.mascot_body, outline="")
        
        # 4. Face Plate
        fw, fh = bw * 0.85, bh * 0.75
        fy = cy - bh * 0.02
        c.create_oval(cx - fw/2, fy - fh/2, cx + fw/2, fy + fh/2, fill=self.theme.mascot_face, outline="")
        
        # 5. Expressive Eyes with Blinking
        ink = "#18181b"
        eye_x = fw * 0.28
        eye_y = fy - 2
        
        blink_factor = math.sin(self._blink) if self._is_blinking else 0.0
        
        def draw_eye(ex):
            if blink_factor > 0.5:
                # Flat line for blink
                c.create_line(ex - 6, eye_y, ex + 6, eye_y, fill=ink, width=3)
            elif self.state == "calm":
                c.create_arc(ex - 6, eye_y - 2, ex + 6, eye_y + 4, start=30, extent=120, style="arc", outline=ink, width=3)
            elif self.state == "limit" or self.state == "worried":
                c.create_oval(ex - 3, eye_y - 1, ex + 3, eye_y + 6, fill=ink, outline="")
            elif self.state == "happy":
                c.create_oval(ex - 4, eye_y - 4, ex + 4, eye_y + 4, fill=ink, outline="")
            else:
                c.create_oval(ex - 3, eye_y - 3, ex + 3, eye_y + 3, fill=ink, outline="")

        draw_eye(cx - eye_x)
        draw_eye(cx + eye_x)

        # 6. Soft Cheeks
        if self.state != "limit":
            c.create_oval(cx - eye_x - 14, eye_y + 10, cx - eye_x - 6, eye_y + 14, fill=self.theme.mascot_cheek, outline="")
            c.create_oval(cx + eye_x + 6, eye_y + 10, cx + eye_x + 14, eye_y + 14, fill=self.theme.mascot_cheek, outline="")
