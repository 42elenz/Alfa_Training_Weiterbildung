import tkinter as tk
from tkinter import messagebox

root = tk.Tk()

result = messagebox.askyesno(
    title="Customize filter",
    message="Do you want to add customized filtered words?",
)

root.mainloop()