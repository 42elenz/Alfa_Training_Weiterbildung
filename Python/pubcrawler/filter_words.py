import tkinter as tk
from tkinter import *
import crawl as c






def newWindow_text(newWindow):
    def submit_words():
        words = mystringa.get()
        trash, customizedwordfiltered = c.customized_filterd_words(words)

        newWindow3 = tk.Toplevel(newWindow2)
        Label(newWindow3, text="Trashwords").grid(column=0, row=0)

        text_box = tk.Text(newWindow3, width=40, height=10,)
        text_box.insert(tk.END, trash)
        text_box.grid(column=1, row=0)

        Label(newWindow3, text="Foundwords").grid(column=0, row=1)

        text_box = tk.Text(newWindow3, width=80, height=80, )
        text_box.insert(tk.END, customizedwordfiltered)
        text_box.grid(column=1, row=1)

        killerbutton = Button(newWindow3, text="KILL", command=lambda:([newWindow3.destroy(),newWindow2.destroy()]))
        killerbutton.grid(column =1 , row =2)



    newWindow2 = tk.Toplevel(newWindow)
    instructions2 = Label(newWindow2, text="Gib die Wörter ein", font="Raleway")
    instructions2.pack()

    mystringa = StringVar()

    Label(newWindow2, text="Enter the word").pack()
    Entry(newWindow2, textvariable=mystringa).pack()

    get_text_button2 = Button(newWindow2, text="CRAWL", command=submit_words)
    get_text_button2.pack()
