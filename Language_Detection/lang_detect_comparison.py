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
        print("textBlob",result)
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
        print("polygot",result.detected_languages)
        if result.language.code == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method: chardet
def chardet_(text, label):
    try:
        sentence = text.strip()
        result = chardet.detect(sentence.encode('cp1251'))
        print(result)
        print("chardet", result)
        # print(sentence, result, file=open("./output/chardetResult.short.txt", "a"))
    except Exception as e:
        print(e)
        pass
    return False


# method: langDedect
def langDedect(text, label):
    try:
        sentence = text.strip()
        result = detect(sentence)
        r=detect_langs(sentence)
        print("langdetect", result,r)
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
        print("guess", result)
        if result == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method: lanid
def langid_(text, label):
    try:
        sentence = text.strip()
        result = langid.classify(sentence)
        print("langid", result)
        if result[0] == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method : fasttext
def fasttext_(text, label):
    try:
        sentence = text.split("\n")[0]
        result = lid_model.predict([sentence])
        print("fasttext", result)
        if result[0][0][0].split("_label__")[1] == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method : cld2
def cld2_(text, label):
    try:
        result = cld2.detect(text.strip())
        print("cld2", result)
        if result[2][0].language_code == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method : spacy
def spacy_lib(text, label):
    try:

        doc = nlp(text.split("/n")[0])

        doc_lang = doc._.language
        print("spacy", doc_lang)
        if doc_lang['language'] == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method : nltk
def nltkDetect(text, label):
    try:
        result = nltkO.guess_language(text=text)
        if str(result) == lang_a[lang_b.index(label)].split("\n")[0]:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method : whatlang
def whatlang(text, label):
    try:
        wtl = WhatTheLang()
        r=wtl.predict_lang(text)
        result = wtl.predict_lang(text)
        print("whatlang",r, result)
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
        print("langua", result)
        if result == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# language_name = languages.get(alpha_2='fr').name  // use this to print the language name using code
# print(language_name)

def updateResults(val, key):
    if key not in results.keys():
        results[key] = {}

    if str(val).lower() not in results[key].keys():
        results[key][str(val).lower()] = 0
    results[key][str(val).lower()] = results[key][str(val).lower()] + 1


# execute one of the above library
#  key --> key for the library in key_list array
# librayFunc --> method for the library (in function_list array)
# text --> text to detect the language
# label --> language of the specific text


def executeLibrary(key, libraryFunc, text, label):
    start = time.perf_counter()
    value = libraryFunc(text, label)
    updateResults(value, key)
    time_elapsed = time.perf_counter() - start
    return value, time_elapsed


# TODO : parallel processing implementation
def oneProcess(text, label):
    row = []
    for index, libr in enumerate(function_list):
        value, time_taken = executeLibrary(key_list[index], libr, text, label)
        row.append(value)
        row.append(float("{:.2f}".format(time_taken)))
    csvwriter.writerow(row)


if __name__ == '__main__':
    # loading model files and objects for libraries
    nltkO = TextCat()
    nlp = spacy.load("en")
    nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
    lid_model = fasttext.load_model("./lid.176.ftz")

    # load text data set and label dataset
    text_test = open("Dataset/x_new_test.txt", "r").readlines()
    label_test = open("Dataset/y_new_test.txt", "r").readlines()
    text_train = open("Dataset/x_new_train.txt", "r").readlines()
    label_train = open("Dataset/y_new_train.txt", "r").readlines()

    # label preprocessing according to one global code
    lang_a = ['eng\n', 'nld\n', 'slk\n', 'spa\n', 'slv\n', 'ita\n', 'deu\n', 'fra\n']
    lang_b = ['en', 'nl', 'sk', 'es', 'sl', 'it', 'de', 'fr']

    label_test = [lang_b[lang_a.index(i)] for i in label_test]
    label_train = [lang_b[lang_a.index(i)] for i in label_train]

    # dataset = zip(text_test[:3] + text_train[:3], label_test[:3] + label_train[:3])
    dataset = zip(text_test[:2], label_test[:2])
    # memory saving code
    text_test = None
    text_train = None
    results = dict();

    # field names for the csv
    fields = ["textblob", "time", "polyglot", "time", "langDedect", "time", "guess_language", "time",
              "langid", "time", "fasttext", "time", "cld2", "time", "nltkDetect", "time", "whatlang",
              "time", "langua", "time"]

    # name of csv file
    filename = "lang_detect_comparison.csv"
    # language detection library list TODO : add additional libraries
    function_list = [textBlob, polyglot, langDedect, guessLanguage, langid_, fasttext_, cld2_,
                     nltkDetect, whatlang, langua,spacy_lib]

    key_list = ["textblob", "polyglot", "langDedect", "guess_language", "langid", "fasttext", "cld2", "nltkDetect",
                "whatlang", "langua"]

    # writing to csv file
    with open(filename, 'a') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)

        count = 0
        for text, label in dataset:  # looping through each instance of the dataset
            if count % 100 == 0:
                print("Completed instances : ", count)
            text = text.split("\n")[0]
            row = []
            for index, libr in enumerate(function_list):  # send text through all libraries
                value, time_taken = executeLibrary(key_list[index], libr, text, label)  # execute one library
                row.append(value)
                row.append(float("{:.2f}".format(time_taken)))
            csvwriter.writerow(row)  # write one instance result for each library - accuracy and time
            count = count + 1

        final = []
        for key in results:
            final.append(results[key]['true'])
            final.append(results[key]['false'])

        csvwriter.writerow([""] * 12)

        csvwriter.writerow(final)
        print("Done")


#  creating combined dataset

texts=text_test+text_train
labels=label_test+label_train
import random
combined_texts=[]
combined_labels=[]
combined_percentage=[]
for i in range(0,8000,500):
    randoms=[random.randrange(0, 500) for i in range(4)]
    for j in randoms:
        for  k in range(0,8000,500):
            if i!=k:
                randoms_other = [random.randrange(0, 500) for i in range(10)]
                for m in randoms_other:
                    percentage=random.randrange(25,42)
                    text1=texts[i+j].split("\n")[0]
                    text2=texts[k+m].split("\n")[0]
                    text1_words=text1.split(" ")
                    text2_words=text2.split(" ")
                    combined_texts.append((" ".join(text1_words[0:len(text1_words)*percentage//100]))+(" ".join(text2_words[0:len(text2_words)*(100-percentage)//100])))
                    if(percentage>50):
                        combined_labels.append((labels[i+j],labels[k+m]))
                    else:
                        combined_labels.append(( labels[k + m],labels[i + j]))
                    combined_percentage.append({labels[i+j]:percentage,labels[k+m]:str(100-percentage)})

f=open("output/combined_text.txt","a")
for i in combined_texts[:8000]:
    f.write(i+"\n")
f=open("output/combined_labels.txt","a")
for i in combined_labels[:8000]:
    f.write(str(i)+"\n")
f=open("output/combined_percentage.txt","a")
for i in combined_percentage[:8000]:
    f.write(str(i)+"\n")
