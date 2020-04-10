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
    texts = open("output/new_data/combined_text_"+str(percentage)+".txt", "r").readlines()
    labels = open("output/new_data/combined_labels_"+str(percentage)+".txt", "r").readlines()


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


#  creating combined dataset

texts=text_test+text_train
labels=label_test+label_train

combined_texts=[]
combined_labels=[]
combined_percentage=[]
percentage = 40
for i in range(0,8000,500):
    randoms=[random.randrange(0, 500) for i in range(4)]
    for j in randoms:
        for  k in range(0,8000,500):
            if i!=k:
                randoms_other = [random.randrange(0, 500) for i in range(10)]
                for m in randoms_other:
                    # percentage=random.randrange(25,42)
                    text1=texts[i+j].split("\n")[0]
                    text2=texts[k+m].split("\n")[0]
                    text1_words=text1.split(" ")
                    text2_words=text2.split(" ")
                    text1_perc=len(text1_words)/(len(text1_words)+len(text2_words))*100
                    leng = min(len(text1_words),len(text2_words))
                    combined_texts.append((" ".join(text1_words[0:leng*percentage//100]))+(" ".join(text2_words[0:leng*(100-percentage)//100])))
                    # combined_texts.append(text1+text2)
                    if(percentage>50):
                        combined_labels.append((labels[i+j],labels[k+m]))
                    else:
                        combined_labels.append(( labels[k + m],labels[i + j]))
                    combined_percentage.append({labels[i+j]:str(percentage),labels[k+m]:str(100-percentage)})

f=open("output/new_data/combined_text_"+str(percentage)+".txt","a")
for i in combined_texts[:8000]:
    f.write(i+"\n")
f=open("output/new_data/combined_labels_"+str(percentage)+".txt","a")
for i in combined_labels[:8000]:
    f.write(str(i)+"\n")
f=open("output/new_data/combined_percentage_"+str(percentage)+".txt","a")
for i in combined_percentage[:8000]:
    f.write(str(i)+"\n")
