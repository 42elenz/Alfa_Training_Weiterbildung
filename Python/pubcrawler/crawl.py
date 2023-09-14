import os.path as os
import string
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import numpy as np
import requests
import nltk
import re

#_____________________
def pubsearch_core(file, termp):
    page = 0
    print(file, termp)
    while True:
        url = "https://pubmed.ncbi.nlm.nih.gov/?term=" + str(termp) + "&page=" + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, features="html.parser")
        links = soup.findAll("a", {"class": "docsum-title"})

        if page > 3:
            break

        ''' NICHT SICHER OB DER BREAK FUNKTIONIERT LIEBER GELASSEN '''
        '''if len(links) < 1:
            break'''


        for link in links:
            file.write(link.text)
            print(link.text)

        page += 1

    return page
#_________________


def term_processing(string):
    termlist = string.split()
    termp = string.replace(" ", "+").replace(",", "+")
    return(termp, termlist)


def maketxtpath(termp):
    txtpath = "data/found_txt/" + str(termp) + ".txt"
    return(txtpath)


def iffile(textpath):
    if os.isfile(textpath):
        textfound = "Es wurde bereits eine Abfrage durchgeführt. Wollen Sie diese erneut duchführen?"
        return(textfound, 1)
    else:
        textfound = "Diese Abfrage wurde noch nicht durchgeführt. Prozess läuft"
        return(textfound, 0)


def pubsearch(o_z, txtpath, termp):
    page = 0
    if o_z == True: #entweder File gibt es nicht oder soll überschrieben werden
        file = open(txtpath, "w")
        print(file, txtpath)
        page = pubsearch_core(file, termp)
        file.close()
        text = "Eine neue Suche wurde angelegt"
        return text, page
    if o_z == False:
        text = "Die alten Suchergebnisse werden genutzt"
        return text, page


def file_content_reader(txtpath):
    file = open(txtpath, "r", encoding="utf-8")
    content = file.read()
    content = content.lower()
    content = content.translate(str.maketrans('', '', string.punctuation))  # säubert von punkten
    file.close()
    return content


def filestring_to_sorted(termlist, filecontent_string):
    content = filecontent_string.split()
    ergebnis_liste = {}
    for el in content:
        if el not in termlist:
            if len(el) > 2: #um ganz kurze Wörter rauszufiltern
                if el in ergebnis_liste:
                    ergebnis_liste[el] += 1
                else:
                    ergebnis_liste[el] = 1
    sortiert = sorted(ergebnis_liste.items(), key=lambda e: e[1], reverse=True)
    return sortiert

def english_fill_word_filter(sorterd_raw_list):
    rawdict = dict(sorterd_raw_list)
    englishwords = file_content_reader("data/englishfillwords.txt")
    englishwords = englishwords.split("\n")
    filtered_list = {}
    trash = {}
    for key, val in rawdict.items():
        if key not in englishwords:
            filtered_list[key] = val
        if key in englishwords:
            trash[key] = val

    return trash, filtered_list

def filter_list(rawliste):
    rawdict = dict(rawliste)
    print(rawdict)

    file = open("/Projects/pubcrawler/englishfillwords.txt", "r", encoding="utf-8")
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
def overwritedict(efw_dict):
    file = open("efw_dict.txt", "w")
    file.write(str(efw_dict))
    file.close()

def filetodict():
    file = open("efw_dict.txt", "r")
    efwstring = file.read()
    efwstring = efwstring.replace("'", "")
    efwstring = re.findall(r"[\w']+", efwstring)
    efw_dict = {efwstring[i]: efwstring[i + 1] for i in range(0, len(efwstring), 2)}
    file.close()
    return efw_dict

def customized_filterd_words(nogos):
    trash = {}
    filter_words = nogos.split()
    filtered_dict = {}

    efw_dict = filetodict()

    for key, val in efw_dict.items():
        if key not in filter_words:
            filtered_dict[key] = val
        if key in filter_words:
            trash[key] = val

    overwritedict(filtered_dict)

    return trash, filtered_dict


def customized_filterd_numbers(nogov):
    nogovz = nogov.split()

    filtered_dict = filetodict()

    # value get
    to_del = [key for key, val in filtered_dict.items() if val in nogovz]

    # Delete keys
    for key in to_del: del filtered_dict[key]

    # New Dictionary
    overwritedict(filtered_dict)
    return filtered_dict


def customized_nlp_filter(nlps):
    #aus keys eine Liste
    filterd_dict = filetodict()
    print("*"*40, nlps)
    liste = []
    for key in filterd_dict:
        liste.append(key)

    tags_content = nltk.pos_tag(liste)
    print("*" * 40, tags_content)
    clas_words = dict(tags_content)

    check = check_nlp(nlps)
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

    overwritedict(filterd_dict)
    return filterd_dict


def check_nlp(nlps):
    numbcheck = []
    a = True
    while a == True:
        trueorfalse = []
        raw_check = nlps.split()
        for i, number in enumerate(raw_check):
            if int(number):
                if len(number) < 2:
                    numbcheck.append(int(number))
                    trueorfalse.append(1)
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


def printer(top=7, low=5, middle=1):
    dicto = filetodict()
    print(dicto)
    top = int(top)
    low = int(low)
    middle = int(middle)
    leng = len(dicto)

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
    print("x:"*3,x )
    y = list(dicto.values())
    print("y:" * 3, y)

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

    # TOPS
    plt.pie(yt, labels=xt, wedgeprops={"edgecolor": "black"}, shadow=True, startangle=90, autopct="%1.1f%%", )
    plt.title("TOP-Begriffe")
    plt.tight_layout()
    plt.show()
    # LOWS
    plt.style.use("fivethirtyeight")
    plt.barh(xl, yl)
    #plt.xticks(np.arange(min(yl), max(yl) + 1, 1.0))
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
    #plt.yticks(np.arange(min(ym), max(ym) + 1, 1.0))
    plt.tight_layout()
    plt.show()


def writeinlist(efw_dict):
    with open("efw_dict.txt", "w") as file:
        file.write(str(efw_dict))
    '''
    file = open("efw_dict.txt", "r")
    efw_dict_txt = file.read()
    print(efw_dict_txt)
    '''




