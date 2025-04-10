import tkinter as tk
from tkinter import messagebox
from game_screen import launch_game_screen
from gui_units import (
    POKER_GREEN, TITLE_FONT, SUBTITLE_FONT, BUTTON_FONT,
    BUTTON_BG, BUTTON_ACTIVE_BG, WINDOW_WIDTH, WINDOW_HEIGHT,
    LABEL_FONT, ENTRY_FONT
)
from game_screen import launch_game_screen  # <-- Use your real game screen

# == Main Menu Window ==
root = tk.Tk()
root.title("Five Card Draw - Game Screen")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg=POKER_GREEN)

# === Title Placeholder ===
title_label = tk.Label(
    root,
    text="R  O  Y  A  L     F  L  U  S  H",
    font=TITLE_FONT,
    fg="white",
    bg=POKER_GREEN
)
title_label.pack(pady=(40, 10))

subtitle_label = tk.Label(
    root,
    text="Five Card Draw",
    font=SUBTITLE_FONT,
    fg="white",
    bg=POKER_GREEN
)
subtitle_label.pack(pady=(0, 30))

# === Button Frame ===
button_frame = tk.Frame(root, bg=POKER_GREEN)
button_frame.pack(side="bottom", pady=50)

# === Button Functions ===
def start_game():
    popup = tk.Toplevel(root)
    popup.title("Game Setup")
    popup.configure(bg=POKER_GREEN)
    popup.grab_set()

    # Center popup relative to the root window (same monitor)
    root.update_idletasks()
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    w, h = 400, 250
    x = root_x + (root_width // 2) - (w // 2)
    y = root_y + (root_height // 2) - (h // 2)
    popup.geometry(f"{w}x{h}+{x}+{y}")

    # === Name Entry ===
    name_label = tk.Label(popup, text="Enter your name:", font=LABEL_FONT, bg=POKER_GREEN, fg="white")
    name_label.pack(pady=(20, 5))

    name_entry = tk.Entry(popup, font=ENTRY_FONT, width=30)
    name_entry.pack(pady=(0, 15))

    # === Player Count ===
    count_label = tk.Label(popup, text="Number of Players (2–4):", font=LABEL_FONT, bg=POKER_GREEN, fg="white")
    count_label.pack(pady=(10, 5))

    player_count = tk.Spinbox(popup, from_=2, to=4, font=ENTRY_FONT, width=5)
    player_count.pack(pady=(0, 15))

    # === Start Button Logic ===
    def confirm_start():
        name = name_entry.get().strip()
        count = int(player_count.get())

        if not name:
            popup.grab_release()
            messagebox.showerror("Input Error", "Please enter your name.")
            popup.grab_set()
            return

        if not name.replace(" ", "").isalpha():
            popup.grab_release()
            messagebox.showerror("Input Error", "Name must only contain letters.")
            popup.grab_set()
            return

        if count < 2 or count > 4:
            popup.grab_release()
            messagebox.showerror("Input Error", "Invalid Table Size (2–4 players only).")
            popup.grab_set()
            return

        print(f"Name: {name}, Players: {count}")
        popup.grab_release()
        popup.destroy()

        # Launch game and hide menu
        root.withdraw()
        launch_game_screen(name, count)

    # === Confirm/Cancel Buttons ===
    bottom_buttons = tk.Frame(popup, bg=POKER_GREEN)
    bottom_buttons.pack(pady=(10, 0))

    start_btn = tk.Button(
        bottom_buttons,
        text="Start",
        font=BUTTON_FONT,
        bg=BUTTON_BG,
        activebackground=BUTTON_ACTIVE_BG,
        fg="white",
        command=confirm_start
    )
    start_btn.pack(side="left", padx=10)

    cancel_btn = tk.Button(
        bottom_buttons,
        text="Cancel",
        font=BUTTON_FONT,
        bg=BUTTON_BG,
        activebackground=BUTTON_ACTIVE_BG,
        fg="white",
        command=lambda: (popup.grab_release(), popup.destroy())
    )
    cancel_btn.pack(side="left", padx=10)

def show_rules():
    messagebox.showinfo("Rules", "Poker hand hierarchy will be displayed here.")

def exit_game():
    root.quit()

# === Buttons ===
start_button = tk.Button(
    button_frame,
    text="Start Game",
    font=BUTTON_FONT,
    bg=BUTTON_BG,
    activebackground=BUTTON_ACTIVE_BG,
    fg="white",
    width=20,
    command=start_game
)
start_button.pack(pady=10)

rules_button = tk.Button(
    button_frame,
    text="Rules",
    font=BUTTON_FONT,
    bg=BUTTON_BG,
    activebackground=BUTTON_ACTIVE_BG,
    fg="white",
    width=20,
    command=show_rules
)
rules_button.pack(pady=10)

exit_button = tk.Button(
    button_frame,
    text="Exit",
    font=BUTTON_FONT,
    bg=BUTTON_BG,
    activebackground=BUTTON_ACTIVE_BG,
    fg="white",
    width=20,
    command=exit_game
)
exit_button.pack(pady=10)

# === Run the App ===
root.mainloop()
