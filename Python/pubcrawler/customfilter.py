import tkinter
from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import filter_words as fw

def start():
    root = tk.Tk()



    #instructions
    instructions = Label(root, text="Wonach soll gefiltert werden", font="Raleway")
    instructions.pack()

    #gettext
    def search():
        wordsy_n = var1.get()
        print(wordsy_n, type(wordsy_n))
        if wordsy_n == "ON":
            fw.main()
        valuesy_n = var2.get()
        NLP = var3.get()


    #textbox
    var1 = StringVar()
    var2 = IntVar()
    var3 = IntVar()

    #words
    c = Checkbutton(root, text="Anklicken, wenn Wörter gefiltert werden sollen", variable=var1, onvalue= "ON", offvalue="OFF" )
    c.pack()
    #values
    d = Checkbutton(root, text="Anklicken, wenn bestimmte Anzahl von Nennungen gefiltert werden sollen", variable=var2)
    d.pack()
    #NLP
    e = Checkbutton(root, text="Anklicken, wenn nach bestimmten Wortarten gefiltert werden soll", variable=var3)
    e.pack()

    #Textbutton und aufruf de sgettext
    get_text_button = Button(root, text="Abschicken", command=search)

    get_text_button.pack()


