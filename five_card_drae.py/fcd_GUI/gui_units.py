# gui_units.py

# === COLORS ===
POKER_GREEN = "#0b6623"
GOLD = "#FFD700"
WHITE = "#FFFFFF"
DARK_GRAY = "#222222"
LIGHT_GREY = "#CCCCCC"
BUTTON_BG = "#444444"
BUTTON_ACTIVE_BG = "#666666"

# === Additional Fonts ===
ENTRY_FONT = ("Helvetica", 14)
LABEL_FONT = ("Helvetica", 16)


# === FONTS ===
TITLE_FONT = ("Courier New", 32, "bold")
SUBTITLE_FONT = ("Courier New", 24, "bold")
BUTTON_FONT = ("Helvetica", 18, "bold")
CARD_FONT = ("Helvetica", 14)

# === DIMENSIONS ===
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# === POPUP UTILITY ===
import tkinter as tk
from tkinter import messagebox

def show_popup(title, message):
    messagebox.showinfo(title, message)
