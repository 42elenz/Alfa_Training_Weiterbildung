import string
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import numpy as np
import os.path as os
import urllib
import requests
import nltk
#vorname.nachname.zip
""" Was will ich:
- nach Stichwort suchen
- 
- definieren der tops, lows und der Middles
- auslass Wörter definieren falls gewollt
- falls gewollt die Liste der ausgelassenen Wörter
- falls gewollt die Lister der default ausgelassenen Wörter
- Plot ausgeben mit den TOps, Lows und middles + (Suchwort, Seitentiefe, extra-ausgelassene Wörter

TODO: 
1 Aufdröseln unterfunktionen
2 extra Main
3 GUI Verknüpfung (GUi ruft eine funktion auf (webcrawler) -> result (GUi) -> webcrawler
2 PORTABEL MACHen-> REALTIVE PFADE 


"""

def page_counter(term):
    """ Gibt die Anzahl der Pages auf Pubmed zurück"""

    page = 1
    url = "https://pubmed.ncbi.nlm.nih.gov/?term=" + str(term) + "&page=" + str(page)
    response = urllib.request.urlopen("https://pubmed.ncbi.nlm.nih.gov/?term=" + str(term) + "&page=" + str(page))
    status_code = response.getcode()
    print(status_code)

    while status_code == 200:
        response = urllib.request.urlopen("https://pubmed.ncbi.nlm.nih.gov/?term=" + str(term) + "&page=" + str(page))
        status_code = response.getcode()
        page += 1
        print(page)
    #Womit hier enden? Der loop geht ewig

    print(status_code)
    print(page)

def pub_spider(term):
    """ DER TERM WIRD IN DER ULR GESUCHT, EINE .txt REFERENZDATEI WIRD ERSTELLT, FALLS NOCH NICHT VORHANDEN. FALLS JA WIRD GEFRAGT OB
    ERSETZT WERDEN SOLL """

    page = 1
    term = term.replace(" ", "+").replace(",", "+")#cleanterm
    if os.isfile("data/found_txt/" + str(term) + ".txt"):
        print("Es wurde bereits eine Abfrage durchgeführt. Wollen Sie diese erneut duchführen?")
        a = input("Y/N: ")
        if a == "Y":
            f = open("data/found_txt/" + str(term) + ".txt", "w")
            print(f)
            while True:
                url = "https://pubmed.ncbi.nlm.nih.gov/?term=" + str(term) + "&page=" + str(page)
                source_code = requests.get(url)
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, features="html.parser")
                links = soup.findAll("a", {"class": "docsum-title"})

                if len(links) < 1:
                    break

                for link in links:
                    f.write(link.text)
                page += 1
            f.close()
        elif a == "N":
            print("Alter Datensatz wird genutzt")
    else:
        while True:
            f = open("data/found_txt/" + str(term) + ".txt", "w")
            url = "https://pubmed.ncbi.nlm.nih.gov/?term=" + str(term) + "&page=" + str(page)
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, features="html.parser")
            links = soup.findAll("a", {"class": "docsum-title"})

            if len(links) < 1:
                break

            for link in links:
                f.write(link.text)
            page += 1
        f.close()

def information(term):
    """Gibt die sortierte Rohliste aus und die Länge der Liste"""
    #HIER NOCH ERGÄNZEN, DASS TERM Teile ausgetauscht werden
    filter_term = term.split()
    term = term.replace(" ", "+").replace(",", "+")
    search_terms = term.split()
    print("INFORMATION", search_terms)
    file = open("data/found_txt/" + str(term) + ".txt", "r", encoding="utf-8")
    content = file.read()
    print(content)
    content = content.lower()
    content = content.translate(str.maketrans('', '', string.punctuation)) # säubert von punkten
    content = content.split()

    ergebnis_liste = {}
    for el in content:
        if el not in filter_term:
            if len(el) > 2: #das könnte man ggf. noch einstellen lassen
                if el in ergebnis_liste:
                    ergebnis_liste[el] += 1
                else:
                    ergebnis_liste[el] = 1

    sortiert = sorted(ergebnis_liste.items(), key=lambda e: e[1], reverse=True)
    file.close()
    return sortiert

def filter_list(rawliste):
    rawdict = dict(rawliste)
    print(rawdict)

    file = open("data/englishfillwords.txt", "r", encoding="utf-8")
    englishword = file.read().lower()
    englishword = englishword.split("\n")
    filtered_list = {}
    trash = {}
    for key, val in rawdict.items():
        if key not in englishword:
            filtered_list[key] = val
        if key in englishword:
            trash[key] = val

    return trash, filtered_list

def filter_custom(rawdict):
    nogos = input("Bitte geben Sie an welche Wörte zustäzlich gefiltert werden sollen: ")
    filter_words = nogos.split()
    print(filter_words)
    print(rawdict)
    filtered_list = {}
    trash = {}
    for key, val in rawdict.items():
        if key not in filter_words:
            filtered_list[key] = val
        if key in filter_words:
            trash[key] = val

    return trash, filtered_list

def bereiche(string):
    x = True
    while x:
        liste = string.split()
        if len(liste) != 3:
            string = input("Bitte nochmal: Welche Tops, Lows und Mittelbereich (eine Zahl) wollen Sie darstellen?: ")
        else:
            x = False

    liste = tuple(liste)
    print(liste)
    return liste


def check_nlp():
    numbcheck = []
    a = True

    while a == True:
        trueorfalse = []
        raw_check = input(
            "Nach welchem Typ Wort möchtest du Filtern?\n Nomen (1)\n Eigennamen (2)\n Adjektiven (3)\n Verben (4)\n NICHT Filtern (5)\n BITTE ZAHLEN EINGEBEN: ")
        raw_check = raw_check.split()
        for i, number in enumerate(raw_check):
            if int(number):
                if len(number) < 2:
                    numbcheck.append(int(number))
                    trueorfalse.append(1)
                    print(trueorfalse)
                elif len(number) >= 2:
                    print(f"Die {i + 1}. Zahl ist zu groß")
                    trueorfalse.append(0)
        if all(trueorfalse):
            a = False

    check = ""
    for el in numbcheck:
        if el == 1:
            check += " NN NNS"
        if el == 2:
            check += " NNP NNPS"
        if el == 3:
            check += " JJ JJR JJS"
        if el == 4:
            check += " VB VBD VBG VBZ"
        if el == 5:
            print("Es wurde nicht gefiltert")
            break

    return check

def nlp(filterd_dict):
    #aus keys eine Liste
    print("FILTER_DICT_RAW:", filterd_dict)
    liste = []
    for key in filterd_dict:
        liste.append(key)
    print("Filtered_LISTE__RAW:", liste)
    tags_content = nltk.pos_tag(liste)
    print("LISTE MIT TAGS:", tags_content)
    clas_words = dict(tags_content)
    print("DICT MIT TAGS:", clas_words)

    check = check_nlp()
    print("CHEKC AUS NLP", check)
    check = check.split()
    print("CHECK ALS LISTE ", check)

   # key get
    to_del = [key for key, val in clas_words.items() if val not in check]

    print(to_del)
    # Delete keys
    for key in to_del: del clas_words[key]
    print("191", clas_words)

    # New Dictionary
    print("194", filterd_dict)

    to_del = [key for key, val in filterd_dict.items() if key not in clas_words]
    print("197", to_del)
    for key in to_del: del filterd_dict[key]

    print(filterd_dict)
    return filterd_dict

def specific_value_types(filtered_dict):
    nogov = input("Welche Values mochtest du aussschließen? ")
    #ggf. Kontrolle einbauen

    nogov = nogov.split()
    nogovz = []
    for zahl in nogov:
        nogovz.append(int(zahl))


    # value get
    to_del = [key for key, val in filtered_dict.items() if val in nogovz]

    print(to_del)
    # Delete keys
    for key in to_del: del filtered_dict[key]

    # New Dictionary
    print("NEW DICT", filtered_dict)

    return filtered_dict

def visu(dicto, top, low, middle):
    # Vorbereiten der Übergabewerte
    print(dicto)
    top = int(top)
    low = int(low)
    middle = int(middle)
    leng = len(dicto)

    print(top, low, middle)
    # Abklären, ob Länge passt, falls nicht, dann ändern
    if leng % 2 == 0:
        if leng / 2 + middle >= leng:
            print(
                "Das Mittel-Set kann mit diesem Mittelwertanzeige Fenster nicht angezeigt werden. Es wird der max. Mittelbereich angezeigt")
            middle = (leng / 2) - 1  # Das ist noch nicht perfekt, reviewen. Also ein Problem mit der Mitte
    if leng % 2 != 0:
        if leng / 2 + middle >= leng:
            print(
                "Das Mittel-Set kann mit diesem Mittelwertanzeige Fenster nicht angezeigt werden. Es wird der max. Mittelbereich angezeigt")
            middle = round(leng / 2) - 1
    if top > leng:
        top == leng / 2
    if low > leng:
        low == leng / 2

    middle1 = int(round(leng / 2) + middle)
    middle2 = int(round(leng / 2) - middle)

    # X und Y werte-definieren für postive liste
    x = list(dicto.keys())
    y = list(dicto.values())

    # tops
    xt = x[0:top]
    yt = y[0:top]

    # xr und yr werte-definieren für negativ liste
    xr = x[::-1]
    yr = y[::-1]

    # lows
    xl = xr[0:low]
    yl = yr[0:low]

    # xm und ym werte für Zwischenwerte definieren:
    xm = x[middle2:middle1]
    ym = y[middle2:middle1]
    y_pos = np.arange(len(yr[0:low]))

    # Abfrage ob Einzel oder Gesamtdarstellung
    eorz = input("Wollen Sie eine Zusammenfassung(Z) oder Einzeldarstellung(E): ")

    if eorz == "E":
        # TOPS
        plt.pie(yt, labels=xt, wedgeprops={"edgecolor": "black"}, shadow=True, startangle=90, autopct="%1.1f%%", )
        plt.title("TOP-Begriffe")
        plt.tight_layout()
        plt.show()
        # LOWS
        plt.style.use("fivethirtyeight")
        plt.barh(xl, yl)
        plt.xticks(np.arange(min(yl), max(yl) + 1, 1.0))
        plt.title("LOW-BEGRIFFE")
        plt.ylabel("Begriffe", fontsize=10)
        plt.xlabel("Anzahl der Nennungen", fontsize=10)
        plt.tight_layout()
        plt.show()
        # MIDDLES
        plt.bar(xm, ym, color="#444444", label="NENNUNGEN")
        plt.legend()
        plt.title("MITTEL-BEGRIFFE")
        plt.xlabel("Begriffe", fontsize=10)
        plt.xticks(rotation=90)
        plt.ylabel("Anzahl der Nennungen", fontsize=10)
        plt.yticks(np.arange(min(ym), max(ym) + 1, 1.0))
        plt.tight_layout()
        plt.show()


def main():
    run = True
    while run == True:
        #BEGINN --> SOLL EIGENTLICH GUI_WORD AUFRUFEN!
        print("Willkommen! Du bist auf der Suche nach neuen Ideen! Hier findest du die Top Ten Begriff-Assoziationen")
        term = input("Wonach willst du suchen?: ")
        #TERM SOLL ZU ZURÜCKKOMMEN aus GUI_word

        #SUCHT MAXIMALE SEITENANZAHL:
        #npages = page_counter(term)
        #Soll Max. Seitenanzahl zurückgeben

        #TIEFE AUSWÄHLEN ÜBER GUI_depths:
        #max_pages = int(input("Wie tief willst du suchen? "))

        #SCHAUT OB DATENSATZ VORHANDEN UND ERSTELLT NEUE ABFRAGE
        pub_spider(term)

        #GIBT DIE LISTE GEORDNET ZURÜCK UNGEFILTERT
        rawliste = information(term)

        #HIER WIRD DIE LISTE MIT DEN STANDARDFÜLLWÖRTERN GEMAPPT
        trash, filtered_dict = filter_list(rawliste)

        #ABFRAGE OB MAN EIGENE WÖRTER FILTERN WILL
        filterdec = input("Do you want to add customized filtered words Y/N: ")
        if filterdec == "Y":
            trash_custom, filtered_dict = filter_custom(filtered_dict)
            print(f"This are your filtered words and how often they were mentioned:{trash_custom}")

        #ALWAYSFILTERD WORDS
        trash_always = input("Do you want to see the always filtered words? Y/N: ")

        if trash_always == "Y":
            print(f"This are the words that were filtered by default and found:{trash}")
            #print(f"Do you want to change that list?")

        #NLP FILTER
        specific_word_types = input("Do you want to filter for specific word type? Y/N: ")
        if specific_word_types == "Y":
            filtered_dict = nlp(filtered_dict)

        #VALUES AUSSORTIEREN
        svp = input("Do you want to filter out for specific values (times mentioned? Y/N: ")
        if svp == "Y":
            filtered_dict = specific_value_types(filtered_dict)

        #DEFINITION DES MITTELBEREICHS UND DES TOPS UND LOWS
        user = input("Which Tops, lows and in which middle area you want to search?: ")
        top, low, middel = bereiche(user)
        print(top, low, middel)

        #VISUALISIERUNG
        visu(filtered_dict, top, low, middel)

        #Loop beenden?
        if answer == True:
            run = True
        elif answer == False:
            run = False
    print("Hope you got some ideas")
main()