import tkinter as tk
import ttkbootstrap as ttk
import random

point = random.randint(1, 12)

def box_clicked(box_number):
    """Run when a box is clicked."""
    if box_number == point:
        lbl_result.config(text=f"Congratulations! You clicked the correct Box {box_number}")
    else:
        lbl_result.config(text=f"You clicked Box {box_number}. Try again!")

# Create the main window
root = ttk.Window(themename="superhero")
root.title("12 Clickable Boxes")
root.geometry("500x550")


# Title
lbl_title = ttk.Label(
    root,
    text="Select a Box",
    font=("Arial", 24, "bold")
)
lbl_title.pack(pady=20)

# Frame containing the boxes
box_frame = ttk.Frame(root)
box_frame.pack(pady=10)

# Create 12 clickable boxes in 3 columns and 4 rows
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

# Result label
lbl_result = ttk.Label(
    root,
    text="Click one of the boxes",
    font=("Arial", 14)
)
lbl_result.pack(pady=20)

root.mainloop()