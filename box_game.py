import random
import tkinter as tk
from pathlib import Path

import ttkbootstrap as ttk
from PIL import Image, ImageTk


NUMBER_OF_BOXES = 12
MAX_ATTEMPTS = 5
STARTING_BALANCE = 100.00

secret_box = 0
attempts = 0
selected_numbers = []
buttons = []
balance = STARTING_BALANCE
active_wager = 0.0


def disable_buttons():
    """Disable every box button when the game ends."""
    for button in buttons:
        button.config(state=tk.DISABLED)


def box_clicked(box_number):
    """Check the chosen box and save its number."""
    global attempts, balance, active_wager

    if active_wager <= 0:
        lbl_result.config(
            text="Enter and submit a wager before selecting a box.",
            bootstyle="warning",
        )
        return

    if box_number in selected_numbers:
        lbl_result.config(
            text=f"You already selected Box {box_number}.",
            bootstyle="warning",
        )
        return

    selected_numbers.append(box_number)
    attempts += 1

    # Disable the selected box so it cannot be chosen again.
    buttons[box_number - 1].config(state=tk.DISABLED)
    lbl_selected.config(
        text="Selected boxes: "
        + ", ".join(str(number) for number in selected_numbers)
    )

    if box_number == secret_box:
        profit = active_wager
        payout = active_wager * 2
        balance += payout
        lbl_balance.config(text=f"Balance: ${balance:.2f}")
        lbl_result.config(
            text=(
                f"Congratulations! Box {box_number} is correct. "
                f"You won ${profit:.2f}!"
            ),
            bootstyle="success",
        )

        if spiderman_photo is not None:
            lbl_winner_image.pack(pady=8)

        active_wager = 0.0
        disable_buttons()
    elif attempts >= MAX_ATTEMPTS:
        lbl_winner_image.pack_forget()
        lbl_result.config(
            text=(
                f"Game over! The correct box was Box {secret_box}. "
                "Your wager was lost."
            ),
            bootstyle="danger",
        )
        active_wager = 0.0
        disable_buttons()
    else:
        remaining = MAX_ATTEMPTS - attempts
        lbl_result.config(
            text=(
                f"Box {box_number} is incorrect. "
                f"You have {remaining} attempts remaining."
            ),
            bootstyle="danger",
        )


def submit_wager():
    """Validate the wager and begin the current round."""
    global balance, active_wager

    if active_wager > 0:
        lbl_result.config(
            text="A wager has already been submitted.",
            bootstyle="warning",
        )
        return

    try:
        wager = float(txt_wager.get().strip())
    except ValueError:
        lbl_result.config(
            text="Enter a valid wager amount.",
            bootstyle="danger",
        )
        txt_wager.focus_set()
        return

    if wager <= 0:
        lbl_result.config(
            text="The wager must be greater than zero.",
            bootstyle="danger",
        )
        txt_wager.focus_set()
        return

    if wager > balance:
        lbl_result.config(
            text="Your wager cannot be greater than your balance.",
            bootstyle="danger",
        )
        txt_wager.focus_set()
        return

    active_wager = wager
    balance -= wager
    lbl_balance.config(text=f"Balance: ${balance:.2f}")
    lbl_result.config(
        text=f"Wager accepted: ${wager:.2f}. Select a box.",
        bootstyle="info",
    )

    txt_wager.config(state=tk.DISABLED)
    btn_submit_wager.config(state=tk.DISABLED)

    for button in buttons:
        button.config(state=tk.NORMAL)

    buttons[0].focus_set()


def new_game():
    """Reset all game information and start a new game."""
    global secret_box, attempts, balance, active_wager

    # Return an unfinished wager when the user starts a new game.
    if active_wager > 0:
        balance += active_wager
        active_wager = 0.0

    secret_box = random.randint(1, NUMBER_OF_BOXES)
    attempts = 0
    selected_numbers.clear()
    lbl_winner_image.pack_forget()

    lbl_result.config(
        text="Enter a wager and select Submit Wager to begin.",
        bootstyle="info",
    )
    lbl_selected.config(text="Selected boxes: None")
    lbl_balance.config(text=f"Balance: ${balance:.2f}")

    txt_wager.config(state=tk.NORMAL)
    txt_wager.delete(0, tk.END)
    btn_submit_wager.config(state=tk.NORMAL)

    for button in buttons:
        button.config(state=tk.DISABLED)

    txt_wager.focus_set()


def exit_program():
    """Close the application."""
    root.destroy()


# Main window
root = ttk.Window(themename="superhero")
root.title("Find the Correct Box")
root.geometry("620x750")
root.resizable(False, False)


# Load the winning image from the same folder as this program.
# The game will still run if spiderman.jpg is missing or unreadable.
spiderman_photo = None
image_path = Path(__file__).with_name("spiderman.jpg")

try:
    with Image.open(image_path) as spiderman_image:
        spiderman_image.thumbnail((160, 160), Image.Resampling.LANCZOS)
        spiderman_photo = ImageTk.PhotoImage(spiderman_image.copy())
except (FileNotFoundError, OSError):
    pass


# Menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New Game", command=new_game, accelerator="Ctrl+N")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_program, accelerator="Ctrl+Q")

root.bind("<Control-n>", lambda event: new_game())
root.bind("<Control-q>", lambda event: exit_program())


# Heading and directions
lbl_title = ttk.Label(
    root,
    text="Find the Correct Box",
    font=("Arial", 24, "bold"),
    bootstyle="primary",
)
lbl_title.pack(pady=(25, 10))

lbl_instructions = ttk.Label(
    root,
    text="One of the twelve boxes contains the winning number.",
    font=("Arial", 12),
)
lbl_instructions.pack(pady=(0, 20))


# Box-button grid
box_frame = ttk.Frame(root, padding=10)
box_frame.pack()

for number in range(1, NUMBER_OF_BOXES + 1):
    button = ttk.Button(
        box_frame,
        text=f"Box {number}",
        width=12,
        padding=12,
        bootstyle="primary-outline",
        command=lambda selected=number: box_clicked(selected),
    )

    row = (number - 1) // 4
    column = (number - 1) % 4
    button.grid(row=row, column=column, padx=8, pady=8)
    buttons.append(button)


# Game messages
lbl_result = ttk.Label(
    root,
    text="",
    font=("Arial", 12, "bold"),
    wraplength=560,
    justify=tk.CENTER,
)
lbl_result.pack(pady=(20, 8))

lbl_selected = ttk.Label(
    root,
    text="Selected boxes: None",
    font=("Arial", 11),
    bootstyle="secondary",
)
lbl_selected.pack()

lbl_winner_image = ttk.Label(root, image=spiderman_photo)


# Wager controls
wager_frame = ttk.Labelframe(
    root,
    text="Wager",
    padding=15,
    bootstyle="success",
)
wager_frame.pack(pady=(20, 0))

lbl_balance = ttk.Label(
    wager_frame,
    text=f"Balance: ${balance:.2f}",
    font=("Arial", 12, "bold"),
    bootstyle="success",
)
lbl_balance.grid(row=0, column=0, columnspan=3, pady=(0, 10))

lbl_wager = ttk.Label(
    wager_frame,
    text="Wager amount: $",
    font=("Arial", 11),
)
lbl_wager.grid(row=1, column=0, padx=(0, 5))

txt_wager = ttk.Entry(wager_frame, width=12, font=("Arial", 11))
txt_wager.grid(row=1, column=1, padx=5)

btn_submit_wager = ttk.Button(
    wager_frame,
    text="Submit Wager",
    command=submit_wager,
    bootstyle="success",
)
btn_submit_wager.grid(row=1, column=2, padx=(10, 0))

txt_wager.bind("<Return>", lambda event: submit_wager())

btnPlayAgain = ttk.Button(
    wager_frame,
    text="Play Again",
    command=new_game,
    bootstyle="success",
)
btnPlayAgain.grid(row=2, column=0, columnspan=3, pady=(10, 0))

new_game()
root.mainloop()
