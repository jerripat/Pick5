import random
import tkinter as tk
import ttkbootstrap as ttk


MAX_ATTEMPTS = 5

secret_box = random.randint(1, 12)
attempts = 0
buttons = []


def box_clicked(box_number):
    """Check the selected box."""
    global attempts

    attempts += 1

    if box_number == secret_box:
        lbl_result.config(
            text=f"Congratulations! Box {box_number} is correct.",
            bootstyle="success"
        )
        disable_buttons()

    elif attempts >= MAX_ATTEMPTS:
        lbl_result.config(
            text=f"Game over! The correct box was Box {secret_box}.",
            bootstyle="danger"
        )
        disable_buttons()

    else:
        remaining = MAX_ATTEMPTS - attempts

        lbl_result.config(
            text=(
                f"Box {box_number} is incorrect. "
                f"You have {remaining} attempts remaining."
            ),
            bootstyle="warning"
        )


def disable_buttons():
    """Disable every box button."""
    for button in buttons:
        button.config(state=tk.DISABLED)


def new_game():
    """Reset the game."""
    global secret_box, attempts

    secret_box = random.randint(1, 12)
    attempts = 0

    lbl_result.config(
        text="Click one of the boxes",
        bootstyle="light"
    )

    for button in buttons:
        button.config(state=tk.NORMAL)


# Create one main window
root = ttk.Window(themename="superhero")
root.title("12 Clickable Boxes")
root.geometry("500x600")
root.resizable(False, False)

# Title
lbl_title = ttk.Label(
    root,
    text="Select a Box",
    font=("Arial", 24, "bold")
)
lbl_title.pack(pady=20)

# Frame containing the buttons
box_frame = ttk.Frame(root)
box_frame.pack(pady=10)

# Create 12 buttons in three columns and four rows
for number in range(1, 13):
    row = (number - 1) // 3
    column = (number - 1) % 3

    button = ttk.Button(
        box_frame,
        text=f"Box {number}",
        width=12,
        bootstyle="primary",
        command=lambda n=number: box_clicked(n)
    )

    button.grid(
        row=row,
        column=column,
        padx=10,
        pady=10,
        ipady=15
    )

    buttons.append(button)

# Result label
lbl_result = ttk.Label(
    root,
    text="Click one of the boxes",
    font=("Arial", 13),
    bootstyle="light",
    wraplength=450
)
lbl_result.pack(pady=20)

# New-game button
btn_new_game = ttk.Button(
    root,
    text="New Game",
    bootstyle="success",
    command=new_game
)
btn_new_game.pack(pady=10)

# Run the application once
root.mainloop()