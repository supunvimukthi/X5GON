import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import csv
import time


def train_model(ngram_range, analyzer, training_data, training_labels):
    text_classifier= Pipeline([('vect', CountVectorizer(ngram_range, analyzer)), ('tfidf', TfidfTransformer(use_idf=False)), ('lrg', LogisticRegression(n_jobs=-1))])
    return text_classifier.fit(training_data[0], training_labels)

def predict(model,data,label):
    prediction = model.predict(data)
    if prediction[0]==label:
        return True
    return False
for i in fin:
    fin[i]['passage']=fin[i]['passage'].split('Passage')[1]
    fin[i]['question'] = fin[i]['question'].split('question')[1]
    fin[i]['answer'] = fin[i]['answer'].split('answer')[1]

def updateResults(val, key):
    if key not in results.keys():
        results[key] = {}

    if str(val).lower() not in results[key].keys():
        results[key][str(val).lower()] = 0
    results[key][str(val).lower()] = results[key][str(val).lower()] + 1

def executeLibrary(key, model, text, label):
    start = time.perf_counter()
    value = predict(model,text, label)
    # print(value)
    updateResults(value, key)
    
    time_elapsed = time.perf_counter() - start
    return value, time_elapsed

if __name__=='__main__':
    train_text = open( './Dataset/x_new_train.txt', "r").readlines()
    train_text_dataframe = pd.DataFrame(train_text)
    train_label= open( './Dataset/y_new_train.txt', "r").readlines()
    train_label_dataframe = pd.DataFrame(train_label)

    test_text = open( './Dataset/x_new_test.txt', "r").readlines()
    test_text_dataframe = pd.DataFrame(test_text)
    test_label= open( './Dataset/y_new_test.txt', "r").readlines()
    test_label_dataframe = pd.DataFrame(test_label)

    

    lang_a = ['eng\n', 'nld\n', 'slk\n', 'spa\n', 'slv\n', 'ita\n', 'deu\n', 'fra\n']
    lang_b = ['en', 'nl', 'sk', 'es', 'sl', 'it', 'de', 'fr']

    test_label_dataframe = [lang_b[lang_a.index(i)] for i in test_label_dataframe[0]]
    train_label_dataframe = [lang_b[lang_a.index(i)] for i in train_label_dataframe[0]]
    dataset = zip(test_text_dataframe[0], test_label_dataframe)

    hyperparameters = [((1,1),'char'),((1,1),'word'),((1,2),'char'),((1,4),'char'),((1,2),'word')]
    models = []
    fields = ['1-gram Character','time','2-gram Character','time','4-gram Character','time','1-gram Word','time', '2-gram Word','time']
    key_list = ['1-gram Character','2-gram Character','4-gram Character','1-gram Word', '2-gram Word']
    for ngram_range,analyzer in hyperparameters:
        models.append(train_model(ngram_range,analyzer,train_text_dataframe,train_label_dataframe))
    

    results = dict()

    # name of csv file
    filename = "lang_detect_trainable_comparison.csv"
    
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
            text= pd.DataFrame([[text]])

            row = []
            for index, model in enumerate(models):  # send text through all libraries
                value, time_taken = executeLibrary(key_list[index], model, text[0], label)  # execute one library
                row.append(value)
                row.append(float("{:.5f}".format(time_taken)))
            csvwriter.writerow(row)  # write one instance result for each library - accuracy and time
            count = count + 1

        final = []
        for key in results:
            final.append(results[key]['true'])
            final.append(results[key]['false'])

        csvwriter.writerow([""] * 12)

        csvwriter.writerow(final)
        print("Done")

    



