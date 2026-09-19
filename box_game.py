import random
import tkinter as tk

import ttkbootstrap as ttk


NUMBER_OF_BOXES = 12
MAX_ATTEMPTS = 5

secret_box = 0
attempts = 0
selected_numbers = []
buttons = []


def disable_buttons():
    """Disable every box button when the game ends."""
    for button in buttons:
        button.config(state=tk.DISABLED)


def box_clicked(box_number):
    """Check the chosen box and save its number."""
    global attempts

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
        lbl_result.config(
            text=f"Congratulations! Box {box_number} is correct.",
            bootstyle="success",
        )
        disable_buttons()
    elif attempts >= MAX_ATTEMPTS:
        lbl_result.config(
            text=f"Game over! The correct box was Box {secret_box}.",
            bootstyle="danger",
        )
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


def new_game():
    """Reset all game information and start a new game."""
    global secret_box, attempts

    secret_box = random.randint(1, NUMBER_OF_BOXES)
    attempts = 0
    selected_numbers.clear()

    lbl_result.config(
        text=f"Select the correct box. You have {MAX_ATTEMPTS} attempts.",
        bootstyle="info",
    )
    lbl_selected.config(text="Selected boxes: None")

    for button in buttons:
        button.config(state=tk.NORMAL)

    buttons[0].focus_set()


def exit_program():
    """Close the application."""
    root.destroy()


# Main window
root = ttk.Window(themename="superhero")
root.title("Find the Correct Box")
root.geometry("620x500")
root.resizable(False, False)


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


new_game()
root.mainloop()
