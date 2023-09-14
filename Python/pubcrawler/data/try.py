
import os.path as os
import string
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import numpy as np
import urllib
import requests
import nltk

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

def file_content_reader(txtpath):
    file = open(txtpath, "r", encoding="utf-8")
    content = file.read()
    content = content.lower()
    content = content.translate(str.maketrans('', '', string.punctuation))  # säubert von punkten
    file.close()
    return content

def english_fill_word_filter(sorterd_raw_list):
    rawdict = dict(sorterd_raw_list)
    englishwords = file_content_reader("englishfillwords.txt")
    englishwords = englishwords.split("\n")
    filtered_list = {}
    trash = {}
    for key, val in rawdict.items():
        if key not in englishwords:
            filtered_list[key] = val
        if key in englishwords:
            trash[key] = val

    return trash, filtered_list

def main():
    filecontent_string = file_content_reader("found_txt/boy.txt")
    sorterd_raw_list = filestring_to_sorted(["boy"], filecontent_string)
    trash, filtered_list = english_fill_word_filter(sorterd_raw_list)
    print(trash,filtered_list)

main()