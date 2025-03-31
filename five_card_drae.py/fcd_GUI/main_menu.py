import tkinter as tk
from gui_units import (
    POKER_GREEN, TITLE_FONT,SUBTITLE_FONT, BUTTON_FONT, BUTTON_BG,
    BUTTON_ACTIVE_BG, show_popup, WINDOW_WIDTH, WINDOW_HEIGHT, LABEL_FONT, ENTRY_FONT
)

# ==Main Menu Window==
root = tk.Tk()
root.title("Five Card Draw") 
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg=POKER_GREEN)

# === Title Placeholder ===
title_label = tk.Label(
    root,
    text="R  O  Y  A  L     F  L  U  S  H",  # simulate arch spacing
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


# ==Button Frame==
button_frame = tk.Frame(root, bg=POKER_GREEN)
button_frame.pack(side="bottom", pady=50)

# ==Button Functions==
def start_game():
    
    popup = tk.Toplevel(root)
    popup.title("Game Setup")
    popup.geometry("400x250")
    popup.configure(bg=POKER_GREEN)
    popup.grab_set()  # Locks focus to this popup window

    # === Name Entry ===
    name_label = tk.Label(popup, text="Enter your name:", font=LABEL_FONT, bg=POKER_GREEN, fg="white")
    name_label.pack(pady=(20, 5))

    name_entry = tk.Entry(popup, font=ENTRY_FONT, width=30)
    name_entry.pack(pady=(0, 15))

    # === Player Count Selection ===
    count_label = tk.Label(popup, text="Number of Players (2–4):", font=LABEL_FONT, bg=POKER_GREEN, fg="white")
    count_label.pack(pady=(10, 5))

    player_count = tk.Spinbox(popup, from_=2, to=4, font=ENTRY_FONT, width=5)
    player_count.pack(pady=(0, 15))

    # === Start and Cancel Buttons ===
    def confirm_start():
        name = name_entry.get()
        count = int(player_count.get())
        print(f"Name: {name}, Players: {count}")
        popup.destroy()  # Close popup after confirmation

    button_frame = tk.Frame(popup, bg=POKER_GREEN)
    button_frame.pack(pady=(10, 0))

    start_btn = tk.Button(
        button_frame, text="Start", font=BUTTON_FONT,
        bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, fg="white",
        command=confirm_start
    )
    start_btn.pack(side="left", padx=10)

    cancel_btn = tk.Button(
        button_frame, text="Cancel", font=BUTTON_FONT,
        bg=BUTTON_BG, activebackground=BUTTON_ACTIVE_BG, fg="white",
        command=popup.destroy
    )
    cancel_btn.pack(side="left", padx=10)

    

def show_rules():
    show_popup("Rules", "Rules will appear here")

def exit_game():
    root.quit()

# ==Buttons==
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

# ==Pack Buttons Vertically==
start_button.pack(pady=10)
rules_button.pack(pady=10)
exit_button.pack(pady=10)

root.mainloop()
