import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=3)


#logo
logo = Image.open("data/GUI/logo.png")
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=0, row=0, columnspan=3)


#instructions
instructions = tk.Label(root, text="Use as word u want to crawl for", font="Raleway")
instructions.grid(columnspan=1, column=1, row=1, sticky=W)

def destroy():
    root.destroy()

#gettext
def gettext():
    input = mystring.get()
    h.printer(input)


#textbox
mystring = StringVar()
Label(root, text="Enter the word").grid(row=2, column=0, sticky=E)
Entry(root, textvariable=mystring).grid(columnspan=2, column=1, row=2, sticky=W)

#Textbutton und aufruf de sgettext
get_text_button = Button(root, text="CRAWL", command=gettext)
get_text_button.grid(column=1, row=3, sticky=W)

#Gesamtlayout unten
canvas = tk.Canvas(root, width=50, height=50)
canvas.grid(columnspan=3, rowspan=3)

root.mainloop()

