from nltk.tokenize import word_tokenize
import nltk
def filtercommand():
    numbcheck = []
    a = True

    while a == True:
        raw_check = input("Nach welchem Typ Wort möchtest du Filtern?\n Nomen (1)\n Eigennamen (2)\n Adjektiven (3)\n Verben (4)\n NICHT Filtern (5) BITTE ZAHLEN EINGEBEN: ")
        raw_check = raw_check.split()
        for i, number in enumerate(raw_check):
            if int(number):
                if len(number) < 2:
                    numbcheck.append(int(number))
                    a = False
                elif len(number) >= 2:
                    print(f"Die {i + 1}. Zahl ist zu groß")
            else:
                raise ValueError("Eingabe kontrollieren! (Zahl ohne Zeichen?)")

    check = ""
    for el in numbcheck:
        if el == 1:
            check += "NN NNS"
        if el == 2:
            check += " NNP NNPS"
        if el == 3:
            check += " "
        if el == 4:
            check += " NNP NNPS"
        if el == 5:
            break

    return check

def nlp(term):

    file = open("data/" + str(term) + ".txt", "r", encoding="utf-8")
    content = file.read()
    content_list = content.split()

    tags_content = nltk.pos_tag(content_list)
    print(tags_content)

    clas_words = dict(tags_content)

    for key,val in clas_words.items():
        if val == "NN":
            print(key)


def main():
    nlp("found")

main()
