import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import crawl as c






def newWindow_value(newWindow):
    def submit_numbers():
        numbers = mystringa.get()
        customizednumberfiltered = c.customized_filterd_numbers(numbers)

        newWindow3 = tk.Toplevel(newWindow2)
        Label(newWindow3, text="Foundwords for value").grid(column=0, row=1)

        text_box = tk.Text(newWindow3, width=80, height=80, )
        text_box.insert(tk.END, customizednumberfiltered)
        text_box.grid(column=1, row=1)

        killerbutton = Button(newWindow3, text="KILL", command=lambda:([newWindow3.destroy(), newWindow2.destroy()]))
        killerbutton.grid(column=1 , row=2)



    newWindow2 = tk.Toplevel(newWindow)
    instructions2 = Label(newWindow2, text="Gib die Values ein, die rausgefiltert werden sollen", font="Raleway")
    instructions2.pack()

    mystringa = StringVar()

    Label(newWindow2, text="Enter the Numbers").pack()
    Entry(newWindow2, textvariable=mystringa).pack()

    get_text_button2 = Button(newWindow2, text="GET", command=submit_numbers)
    get_text_button2.pack()
