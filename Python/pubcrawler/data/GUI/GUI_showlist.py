import tkinter as tk
from tkinter import *
from tkinter import ttk

win = Tk()
dictionarie= {"hallo": 2, "tschüss": 3, "Auto": 4}
tv = ttk.Treeview(columns=(1, 2), show="headings", height="20")


tv.pack()

tv.heading(1, text="Word")
tv.heading(2, text="Mentioned")



win.title("Resultlist")
win.geometry("650x500")
win.resizable(False, False)
win.mainloop()