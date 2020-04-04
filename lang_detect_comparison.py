import csv
import time
import polyglot
import chardet
import langid
from textblob import TextBlob
from polyglot.text import Text, Word
from langdetect import detect, DetectorFactory, detect_langs
from guess_language import guess_language
import fasttext
import cld2
import spacy
from spacy_langdetect import LanguageDetector
from nltk.classify.textcat import TextCat
import nltk
from whatthelang import WhatTheLang
from langua import Predict

nltk.download('crubadan')
nltk.download('punkt')

from pycountry import languages


# method: textBlob
def textBlob(text, label):
    try:
        sentence = text.strip()
        blob = TextBlob(sentence)
        result = blob.detect_language()
        if result == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method: polyglot
def polyglot(text, label):
    try:
        sentence = text.strip()
        result = Text(sentence)
        if result.language.code == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method: chardet
def chardet(text, label):
    try:
        sentence = text.strip()
        result = chardet.detect(sentence.encode('cp1251'))
        print(sentence, result, file=open("./output/chardetResult.short.txt", "a"))
    except Exception as e:
        print(e)
        pass
    return False


# method: langDedect
def langDedect(text, label):
    try:
        sentence = text.strip()
        result = detect(sentence)
        if result == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method: guessLanguage
def guessLanguage(text, label):
    try:
        sentence = text.strip()
        result = guess_language(sentence)
        if result == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method: lanid
def langid(text, label):
    try:
        sentence = text.strip()
        result = langid.classify(sentence)
        if result[0] == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method : fasttext
def fasttext(text, label):
    try:
        sentence = text.split("\n")[0]
        result = lid_model.predict([sentence])
        if result[0][0][0].split("_label__")[1] == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method : cld2
def cld2(text, label):
    try:
        result = cld2.detect(text.strip())
        if result[2][0].language_code == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method : spacy
def spacy(text, label):
    try:
        nlp = spacy.load("en")
        nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
        doc = nlp(text.split("/n")[0])
        doc_lang = doc._.language
        if doc_lang['language'] == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method : nltk
def nltkDetect(text, label):
    try:
        result = TextCat().guess_language(text=text)
        if str(result).__contains__(label):
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method : whatlang
def whatlang(text, label):
    try:
        wtl = WhatTheLang()
        result = wtl.predict_lang(text)
        if result == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method : langua
def langua(text, label):
    try:
        p = Predict()
        result = p.get_lang(text)
        if result == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# language_name = languages.get(alpha_2='fr').name  // use this to print the language name using code
# print(language_name)

def updateResults(val, key):
    if (val):
        results[key]['true'] = results[key]['true'] + 1
    else:
        results[key]['false'] = results[key]['false'] + 1


def executeLibrary(key, libraryFunc, text, label):
    start = time.perf_counter()
    value = libraryFunc(text, label)
    updateResults(value, key)
    time_elapsed = time.perf_counter() - start
    return value, time_elapsed


if __name__ == '__main__':
    lid_model = fasttext.load_model("./lid.176.ftz")
    dataset = ""
    results = dict();

    # field names
    fields = ["textblob", "time", "polyglot", "time", "chardet", "time", "langDedect", "time", "guess_language", "time",
              "langid", "time", "fasttext", "time", "cld2", "time", "spacy", "time", "nltkDetect", "time", "whatlang",
              "time", "langua"]

    # name of csv file
    filename = "lang_detect_comparison.csv"
    function_list = [textBlob, polyglot, chardet, langDedect, guess_language, langid, fasttext, cld2, spacy,
                     nltkDetect, whatlang, langua]

    key_list = ["textblob", "polyglot", "chardet", "langDedect", "guess_language", "langid", "fasttext", "cld2",
                "spacy", "nltkDetect", "whatlang", "langua"]
    # writing to csv file
    with open(filename, 'a') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)

        for text, label in dataset:
            row=[]
            for index,libr in enumerate(function_list):
                value,time=executeLibrary(key_list[index],libr,text,label)
                row.append(value,time)
            csvwriter.writerow(row)
