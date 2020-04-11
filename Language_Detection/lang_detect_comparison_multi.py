import csv
import time
import ast
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
import random
from whatthelang import WhatTheLang
from langua import Predict

nltk.download('crubadan')
nltk.download('punkt')

from pycountry import languages


# method: polyglot
def polyglot(text, label):
    score=0
    try:
        sentence = text.strip()
        result = Text(sentence)
        if result.detected_languages.languages[0].code in label:
            score+=1
        if result.detected_languages.languages[1].code in label:
            score += 1
        if result.detected_languages.languages[0].code == label[0]:
            score += 2
        if result.detected_languages.languages[0].code == label[0] and result.detected_languages.languages[1].code == label[1]:
            score += 3
    except Exception as e:
        print(e)
        pass
    return score



# method: langDedect
def langDedect(text, label):
    try:
        score=0
        sentence = text.strip()
        result = detect(sentence)
        result=detect_langs(sentence)
        if result.__getitem__(0).lang in label:
            score+=1
        if(len(result)==2):
            if result.__getitem__(1).lang in label:
                score += 1
            if result.__getitem__(0).lang == label[0] and result.__getitem__(1).lang == label[1]:
                score += 3
        if result.__getitem__(0).lang== label[0]:
            score += 2
    except Exception as e:
        print(e)
        pass
    return score



# method: lanid
def langid_(text, label):
    score=0
    try:
        sentence = text.strip()
        result=langid.rank(sentence)
        if result[0][0] in label:
            score += 1
        if result[1][0] in label:
            score += 1
        if result[0][0] == label[0]:
            score += 2
        if result[0][0] == label[0] and result[1][0] == label[1]:
            score += 3
    except Exception as e:
        print(e)
        pass
    return score


# method : fasttext
def fasttext_(text, label):
    score=0
    try:
        sentence = text.split("\n")[0]
        result = lid_model.predict([sentence],k=2)
        if result[0][0][0].split("_label__")[1] in label:
            score += 1
        if result[0][0][1].split("_label__")[1] in label:
            score += 1
        if result[0][0][0].split("_label__")[1]== label[0]:
            score += 2
        if result[0][0][0].split("_label__")[1] == label[0] and result[0][0][1].split("_label__")[1] == label[1]:
            score += 3

    except Exception as e:
        print(e)
        pass
    return score

# method : spacy
# def spacy_lib(text, label):
#     try:
#
#         doc = nlp(text.split("/n")[0])
#         doc_lang = doc._.language
#         print("spacy", doc_lang)
#         if doc_lang['language'] == label:
#             return True
#     except Exception as e:
#         print(e)
#         pass
#     return False





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
    percentage = 40
    # load text data set and label dataset
    texts = open("output/combined_text_"+str(percentage)+".txt", "r").readlines()
    labels = open("output/combined_labels_"+str(percentage)+".txt", "r").readlines()


    # label preprocessing according to one global code
    lang_a = ['eng\n', 'nld\n', 'slk\n', 'spa\n', 'slv\n', 'ita\n', 'deu\n', 'fra\n']
    lang_b = ['en', 'nl', 'sk', 'es', 'sl', 'it', 'de', 'fr']

    # label_test = [lang_b[lang_a.index(i)] for i in label_test]
    # label_train = [lang_b[lang_a.index(i)] for i in label_train]

    # dataset = zip(text_test[:3] + text_train[:3], label_test[:3] + label_train[:3])
    dataset = zip(texts,labels)
    # memory saving code
    text_test = None
    text_train = None
    results = dict();

    # field names for the csv
    fields = ["polyglot", "time", "langDedect", "time",
              "langid", "time", "fasttext", "time"]

    # name of csv file

    filename = "lang_detect_comparison_multi_"+str(percentage)+".csv"
    # language detection library list TODO : add additional libraries
    function_list = [polyglot, langDedect, langid_, fasttext_]

    key_list = [ "polyglot", "langDedect",  "langid", "fasttext"]

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
            label=ast.literal_eval(label.split("\n")[0])
            row = []
            for index, libr in enumerate(function_list):  # send text through all libraries
                value, time_taken = executeLibrary(key_list[index], libr, text, label)  # execute one library
                row.append(value)
                row.append(float("{:.4f}".format(time_taken)))
            csvwriter.writerow(row)  # write one instance result for each library - accuracy and time
            count = count + 1

        print(results)

        csvwriter.writerow([""] * 12)

        # csvwriter.writerow(final)
        print("Done")


# import json
# import csv
#
# f=open("final_sorted.txt","r")
# x=f.readlines()
# y=[i.split("-->")[1] for i in x]
# y=[json.loads(i.replace(" ","").replace("'",'"')) for i in y]
# scores=["7","3","2","1","0"]
# count=0
# with open("final_data_sorted.csv", 'a') as csvfile:
#     # creating a csv writer object
#     csvwriter = csv.writer(csvfile)
#     for b in y:
#
#         csvwriter.writerow(["x"]+[i for i in y[0]])
#         for i in scores:
#             csvwriter.writerow([i]+[y[count][j][i]/8000*100 for j in y[count]])
#         count+=1

# import numpy as np
# import matplotlib.pyplot as plt
#
# # set width of bar
# barWidth = 0.25
#
# # set height of bar
# bars1 = [12, 30, 1, 8, 22]
# bars2 = [28, 6, 16, 5, 10]
# bars3 = [29, 3, 24, 25, 17]
#
# # Set position of bar on X axis
# r1 = np.arange(len(bars1))
# r2 = [x + barWidth for x in r1]
# r3 = [x + barWidth for x in r2]
#
# # Make the plot
# plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='var1')
# plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='var2')
# plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='var3')
#
# # Add xticks on the middle of the group bars
# plt.xlabel('group', fontweight='bold')
# plt.xticks([r + barWidth for r in range(len(bars1))], ['A', 'B', 'C', 'D', 'E'])
#
# # Create legend & Show graphic
# plt.legend()
# plt.show()
