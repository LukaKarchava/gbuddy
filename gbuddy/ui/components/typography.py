"""Typography hierarchy."""

import customtkinter as ctk

DISPLAY = ("Inter", "SF Pro Display", "Segoe UI Variable Display", "Segoe UI", "Ubuntu")
BODY = ("Inter", "SF Pro Text", "Segoe UI Variable Text", "Segoe UI", "Ubuntu")


class Typography:
    DISPLAY = DISPLAY
    BODY = BODY

    @staticmethod
    def brand(size=32):
        return ctk.CTkFont(family=DISPLAY[0], size=size, weight="bold")

    @staticmethod
    def display(size=24, weight="bold"):
        return ctk.CTkFont(family=DISPLAY[0], size=size, weight=weight)

    @staticmethod
    def hero(size=54):
        return ctk.CTkFont(family=DISPLAY[0], size=size, weight="bold")

    @staticmethod
    def stat(size=20):
        return ctk.CTkFont(family=DISPLAY[0], size=size, weight="bold")

    @staticmethod
    def body(size=14, weight="normal"):
        return ctk.CTkFont(family=BODY[0], size=size, weight=weight)

    @staticmethod
    def whisper(size=13):
        return ctk.CTkFont(family=BODY[0], size=size, weight="normal")

    @staticmethod
    def caption(size=11, weight="normal"):
        return ctk.CTkFont(family=BODY[0], size=size, weight=weight)

    @staticmethod
    def tiny(size=10, weight="normal"):
        return ctk.CTkFont(family=BODY[0], size=size, weight=weight)
