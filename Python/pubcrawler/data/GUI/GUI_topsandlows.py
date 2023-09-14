import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=2, rowspan=5)


#instructions
instructions = Label(root, text="Submit numbers", font="Raleway")
instructions.grid(columnspan=2, column=0, row=3)

#gettext
def gettext():
    top = mystring.get()
    middle = mystring2.get()
    low = mystring3.get()
    print(top, middle, low)
    root.destroy()
    return(input)

#Wie verarbeite ich den weiter?

#textbox
mystring = StringVar()
mystring2 = StringVar()
mystring3 = StringVar()
#Top
Label(root, text="Enter the number of tops").grid(row=0, column=0, sticky=E)
Entry(root, textvariable=mystring).grid(columnspan=1, column=1, row=0, sticky=W)
#Low
Label(root, text="Enter the number of lows").grid(row=1, column=0, sticky=E)
Entry(root, textvariable=mystring2).grid(columnspan=1, column=1, row=1, sticky=W)
#Middle
Label(root, text="Enter the number of middles").grid(row=2, column=0, sticky=E)
Entry(root, textvariable=mystring3).grid(columnspan=1, column=1, row=2, sticky=W)

#Textbutton und aufruf de sgettext
get_text_button = Button(root, text="SUBMIT", command=gettext)
get_text_button.grid(columnspan=2, row=4)

'''
#Gesamtlayout unten
canvas = tk.Canvas(root, width=50, height=50)
canvas.grid(columnspan=3, rowspan=3)
'''
root.mainloop()