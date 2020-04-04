import polyglot
import chardet
import langid
from textblob import TextBlob
from polyglot.text import Text, Word
from langdetect import detect, DetectorFactory, detect_langs
from guess_language import guess_language
import fasttext
# import cld2
import spacy
from spacy_langdetect import LanguageDetector
from nltk.classify.textcat import TextCat
import nltk
nltk.download('crubadan')
nltk.download('punkt')

from pycountry import languages
import sys


# reload(sys)
# sys.setdefaultencoding('UTF8') # default encoding to utf-8


# method: textBlob
# Dedect which language used
# @return: True
# @completed
def textBlob():
    with open("./input_text.txt", "r") as sentences:
        try:
            for sentence in sentences:
                sentence = sentence.strip()
                blob = TextBlob(sentence)
                result = blob.detect_language()
                print(sentence, ":", result, file=open("./output/textBlobResult.short.txt", "a"))

        except:
            pass
    return True


# method: polyglot
# Dedect which language used
# @return: True
# @completed
def polyglot():
    #: Import dataset
    with open("./input_text.txt", "r") as sentences:
        try:
            for sentence in sentences:
                sentence = sentence.strip()
                result = Text(sentence)
                print(sentence, "Language Detected: Code={}, Name={}\n".format(result.language.code,
                                                                               result.language.name),
                      file=open("./output/polyglotResult.short.txt", "a"))
        except:
            pass
    return True


# method: chardetExport
# Dedect which language used
# @return: True
# @completed
def chardetExport():
    #: Import dataset
    with open("./input_text.txt", "r") as sentences:
        try:
            for sentence in sentences:
                sentence = sentence.strip()
                result = chardet.detect(sentence.encode('utf-8'))
                # print(result)
                print(sentence, result, file=open("./output/chardetResult.short.txt", "a"))
        except:
            pass
    return True


# method: langDedect
# Dedect which language used
# @return: True
# @completed
def langDedect():
    #: Import dataset
    with open("./input_text.txt", "r") as sentences:
        try:
            for sentence in sentences:
                sentence = sentence.strip()
                result = detect_langs(sentence)
                # print(result)
                print(sentence, ":", result, file=open("./output/langDedectResult.short.txt", "a"))
        except:
            pass
    return True


# method: guessLanguage
# Dedect which language used
# @return: True
# @completed
def guessLanguage():
    #: Import dataset
    with open("./input_text.txt", "r") as sentences:
        for sentence in sentences:
            try:
                sentence = sentence.strip()
                result = guess_language(sentence)
                # print(result)
                print(sentence, ":", result, file=open("./output/guessLanguageResult.short.txt", "a"))
            except:
                pass
    return True


# method: lanidExport
# Dedect which language used
# @return: True
# @completed
def langidExport():
    #: Import dataset
    with open("./input_text.txt", "r") as sentences:
        for sentence in sentences:
            try:
                sentence = sentence.strip()
                result = langid.classify(sentence)
                # print(result)
                print(sentence, ":", result, file=open("./output/langidResult.short.txt", "a"))
            except:
                pass
    return True


lid_model = fasttext.load_model("./lid.176.ftz")


def fasttextExport():
    #: Import dataset
    with open("./input_text.txt", "r") as sentences:
        for sentence in sentences:
            try:
                sentence = sentence.split("\n")[0]
                result = lid_model.predict([sentence])
                print(sentence, ":", result, file=open("./output/fastTextResult.short.txt", "a"))
            except Exception as e:
                print(e)
                pass
    return True


def cld2Export():
    #: Import dataset
    with open("./input_text.txt", "r") as sentences:
        for sentence in sentences:
            try:
                isReliable, textBytesFound, details = cld2.detect(sentence)
                print(sentence, ": [", isReliable, textBytesFound, details, " ]",
                      file=open("./output/cld2Result.short.txt", "a"))
            except Exception as e:
                print(e)
                pass
    return True


def spacyExport():
    #: Import dataset
    with open("./input_text.txt", "r") as sentences:
        try:
            nlp = spacy.load("en")
            nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)

            doc = nlp(sentences.read().split("/n")[0])
            # document level language detection. Think of it like average language of document!
            doc_lang=doc._.language
            # sentence level language detection
            for i, sent in enumerate(doc.sents):
                lang=sent._.language
                print(sent, lang,"doc_language",doc_lang,file=open("./output/spacyResult.short.txt", "a"))
        except Exception as e:
            print(e)
            pass
    return True

def nltkExport():
    #: Import dataset
    with open("./input_text.txt", "r") as sentences:
        for sentence in sentences:
            try:
                result=TextCat().guess_language(text=sentence)
                print(sentence, ": [", result ," ]",
                      file=open("./output/nltkResult.short.txt", "a"))
            except Exception as e:
                print(e)
                pass
    return True



# language_name = languages.get(alpha_2='fr').name  // use this to print the language name using code
# print(language_name)




if __name__ == '__main__':
    textBlob()
    polyglot()
    chardetExport()
    langDedect()
    guessLanguage()
    langidExport()
    fasttextExport()
    # cld2Export()
    spacyExport()
    nltkExport()