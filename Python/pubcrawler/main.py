import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import crawl as c
import filter_words as fw
import filter_values as fv
import filter_nlp as fn

'''HINWEIS -> DIE PFADE SIND ABSOLUTE PFADANGABEN; DESWEGEN KANN ES SEIN, DASS DAS PROGRAMM NICHT LÄUFT BITTE VORHER ÄNDERN.
UND BITTE DEN UNÜBERSICHTLICHEN CODE ENTSCHULDIGEN. SO SIEHT ES AUCH IN MEINEM KOPF AUS :D '''

def search():
    input = mystring.get()
    termp, termlist = c.term_processing(input) #macihine+leraning + machine learning
    txtpath = c.maketxtpath(termp) #path im Dateienordner der Datei
    textfound, o_z = c.iffile(txtpath) #o_z= ob file schon existiert, textfound = rückgabe text
    o_z = GUI_isfile_reload(textfound, o_z) #gibt zurück ob gesucht werden muss oder nicht
    text, page = c.pubsearch(o_z, txtpath, termp) #gibt zurück ob neue Suche gestartet wurde, gibt Seiten zurück
    GUI_print(text) #printet ob neue Datei erstellt wurde
    filecontent_string = c.file_content_reader(txtpath)
    sorterd_raw_list = c.filestring_to_sorted(termlist, filecontent_string) #gibt gecountete Lsite zurück sortiert, ohne Wörter < 2
    efw_trash, efw_dcit = c.english_fill_word_filter(sorterd_raw_list)
    GUI_see_efw_trash(efw_trash)
    c.writeinlist(efw_dcit)#ich habe jetzt hier einen txt file, auf den ich referenzieren kann
    weiter()
    listezeigen()
    beenden()



    #filt_trash, filt_dict = c.customized_filterd_words(y_n, efw_dcit)  # wenn gefilterte wurde Trash, sonst Trash leer (Liste); gefiltertet dict mit Values


def GUI_isfile_reload(textfound, o_z):
    if o_z == 1:
        result = messagebox.askyesno(
            title="Wurde schon mal durchsucht",
            message=textfound,
        )
        return result #True = Will suchen oder false = will nicht suchen
    elif o_z == 0:
        print(textfound)
        return True #Datei ist schon vorhanden

def GUI_print(text):
    text_box = tk.Text(root, width=40, height =10,)
    text_box.insert(tk.END, text)
    text_box.grid(columnspan=2, column=0, row=4)

def GUI_see_efw_trash(efw_trash):
        result = messagebox.askyesno(
            title="Standarfilterwörter",
            message="Wollen Sie die Standardfilterwörter sehen?"
        )
        if result == True:
            GUI_print(efw_trash)

def GUI_customized_words():
    result = messagebox.askyesno(
        title="Customize filter",
        message="Möchten Sie selber Wörter bennen nach denen gefiltert werden soll?",
    )
    return result

def weiter():
    get_text_button = Button(root, text="filter", command=nextwindow)
    get_text_button.grid(column=2, row=3, columnspan=1, rowspan=1)
    get_text_button.config(height=1, width=10)

def listezeigen():
    showlist_button = Button(root, text="Show list", command=showlist)
    showlist_button.grid(column=3, row=3, columnspan=1, rowspan=1)
    showlist_button.config(height=1, width=10)

def beenden():
    killer = Button(root, text="beenden", command= lambda: root.destroy())
    killer.grid(column=2, row=4, columnspan=2, rowspan=1)
    get_text_button.config(height=1, width=10)

def showlist():
    dict = c.filetodict()
    newWindow2 = tk.Toplevel(root)
    Label(newWindow2, text="Aktuelle Liste").grid(column=0, row=1)

    text_box = tk.Text(newWindow2, width=80, height=80, )
    text_box.insert(tk.END, dict)
    text_box.grid(column=1, row=1)

    killerbutton = Button(newWindow2, text="KILL", command=lambda: newWindow2.destroy())
    killerbutton.grid(column=1, row=2)

def nextwindow():
        def search():
            wordsy_n = var1.get()
            if wordsy_n == "ON":
                fw.newWindow_text(newWindow)
            valuesy_n = var2.get()
            if valuesy_n == "ON":
                fv.newWindow_value(newWindow)
            NLP = var3.get()
            if NLP == "ON":
                fn.newWindow_nlp(newWindow)

        def printer():
            c.printer()


        newWindow = tk.Toplevel(root)
        instructions = Label(newWindow, text="Wonach soll gefiltert werden", font="Raleway")
        instructions.pack()

        # textbox
        var1 = StringVar()
        var2 = StringVar()
        var3 = StringVar()

        # words
        f = Checkbutton(newWindow, text="Anklicken, wenn Wörter gefiltert werden sollen", variable=var1, onvalue="ON",offvalue="OFF")
        f.pack()
        # values
        d = Checkbutton(newWindow, text="Anklicken, wenn bestimmte Anzahl von Nennungen gefiltert werden sollen", variable=var2, onvalue="ON",offvalue="OFF")
        d.pack()
        # NLP
        e = Checkbutton(newWindow, text="Anklicken, wenn nach bestimmten Wortarten gefiltert werden soll", variable=var3, onvalue="ON",offvalue="OFF")
        e.pack()

        # Textbutton und aufruf de sgettext
        get_text_buttona = Button(newWindow, text="Abschicken", command=search)
        get_text_buttona.pack()

        print_buttonb = Button(newWindow, text="Print", command=printer)
        print_buttonb.pack()



root = tk.Tk()
#definiere Umgebung
canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=3)
#logo
logo = Image.open("logo.png")
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=0, row=0, columnspan=3)

#instructions
instructions = tk.Label(root, text="Use as word u want to crawl for", font="Raleway")
instructions.grid(columnspan=1, column=1, row=1, sticky=W)
#textbox
mystring = StringVar()
Label(root, text="Enter the word").grid(row=2, column=0, sticky=E)
Entry(root, textvariable=mystring).grid(columnspan=2, column=1, row=2, sticky=W)
#Textbutton und aufruf de sgettext
get_text_button = Button(root, text="CRAWL", command=search) # -> AUS HAUPTRAUS UND RUFT
get_text_button.grid(column=1, row=3, sticky=W)



#Gesamtlayout unten
canvas = tk.Canvas(root, width=50, height=50)
canvas.grid(columnspan=3, rowspan=3)

#Kommawarnung
messagebox.showinfo(title= "Info", message="KEINE KOMMATA UND BITTE ERFORDERLICHEN INPUT BEACHTEN")

root.mainloop()