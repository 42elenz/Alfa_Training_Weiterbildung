import tkinter as tk
from tkinter import *
import crawl as c


def newWindow_nlp(newWindow):
    def submit_nlp():
        nlps = mystringa.get()
        customizenlpfiltered = c.customized_nlp_filter(nlps)

        newWindow3 = tk.Toplevel(newWindow2)
        Label(newWindow3, text="Gefunden nach Wortart").grid(column=0, row=1)

        text_box = tk.Text(newWindow3, width=80, height=80, )
        text_box.insert(tk.END, customizenlpfiltered)
        text_box.grid(column=1, row=1)

        killerbutton = Button(newWindow3, text="KILL", command=lambda:([newWindow3.destroy(), newWindow2.destroy()]))
        killerbutton.grid(column=1 , row=2)



    newWindow2 = tk.Toplevel(newWindow)
    instructions2 = Label(newWindow2, text="Nach welchem Typ Wort möchtest du Filtern?\n Nomen (1)\n Eigennamen (2)\n Adjektiven (3)\n Verben (4)\n NICHT Filtern (5)\n BITTE ZAHLEN EINGEBEN: ", font="Raleway")
    instructions2.pack()

    mystringa = StringVar()

    Label(newWindow2, text="Enter the Numbers").pack()
    Entry(newWindow2, textvariable=mystringa).pack()

    get_text_button = Button(newWindow2, text="Start", command=submit_nlp)
    get_text_button.pack()
