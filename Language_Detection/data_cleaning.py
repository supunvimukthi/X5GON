# creating combined data-sets of two languages
import random
import pandas as pd

# reading the initial data-set
text_test = open("Dataset/x_new_test.txt", "r").readlines()
label_test = open("Dataset/y_new_test.txt", "r").readlines()
text_train = open("Dataset/x_new_train.txt", "r").readlines()
label_train = open("Dataset/y_new_train.txt", "r").readlines()

# label pre-processing according to one global code
lang_a = ['eng\n', 'nld\n', 'slk\n', 'spa\n', 'slv\n', 'ita\n', 'deu\n', 'fra\n']
lang_b = ['en', 'nl', 'sk', 'es', 'sl', 'it', 'de', 'fr']

label_test = [lang_b[lang_a.index(i)] for i in label_test]
label_train = [lang_b[lang_a.index(i)] for i in label_train]

# combining both datasets as one
texts = text_test + text_train
labels = label_test + label_train

combined_texts = []
combined_labels = []
combined_percentage = []
percentage = 40  # change this to change the document percentage when combining documents of two languages.

for i in range(0, 8000, 500):  # loop through each language, one language has 500 instances each
    randoms = [random.randrange(0, 500) for i in range(4)]  # select random documents
    for j in randoms:
        for k in range(0, 8000, 500):
            if i != k:
                randoms_other = [random.randrange(0, 500) for i in
                                 range(10)]  # select 10 random documents from the other language
                for m in randoms_other:
                    # percentage=random.randrange(25,42)
                    text1 = texts[i + j].split("\n")[0]  # document1
                    text2 = texts[k + m].split("\n")[0]  # document2
                    text1_words = text1.split(" ")
                    text2_words = text2.split(" ")

                    text1_perc = len(text1_words) / (len(text1_words) + len(text2_words)) * 100
                    leng = min(len(text1_words),
                               len(text2_words))  # divide the percentage based on the length of the smaller document
                    combined_texts.append((" ".join(text1_words[0:leng * percentage // 100])) + (
                        " ".join(text2_words[0:leng * (100 - percentage) // 100])))
                    # combined_texts.append(text1+text2)
                    if percentage > 50:
                        combined_labels.append((labels[i + j], labels[
                            k + m]))  # labels of the two documents in correct order of the percentage
                    else:
                        combined_labels.append((labels[k + m], labels[i + j]))
                    combined_percentage.append({labels[i + j]: str(percentage), labels[k + m]: str(100 - percentage)})

f = open("output/new_data/combined_text_" + str(percentage) + ".txt", "a")
for i in combined_texts[:8000]:
    f.write(i + "\n")
f = open("output/new_data/combined_labels_" + str(percentage) + ".txt", "a")
for i in combined_labels[:8000]:
    f.write(str(i) + "\n")
f = open("output/new_data/combined_percentage_" + str(percentage) + ".txt", "a")
for i in combined_percentage[:8000]:
    f.write(str(i) + "\n")

# 2nd method : do sorting on the length first before the above method
train_text = open('./Dataset/x_new_train.txt', "r").readlines()
train_text_dataframe = pd.DataFrame(train_text)
train_label = open('./Dataset/y_new_train.txt', "r").readlines()
train_label_dataframe = pd.DataFrame(train_label)
test_text = open('./Dataset/x_new_test.txt', "r").readlines()
test_text_dataframe = pd.DataFrame(test_text)
test_label = open('./Dataset/y_new_test.txt', "r").readlines()
test_label_dataframe = pd.DataFrame(test_label)
train_text_dataframe.rename(columns={0: 'text'}, inplace=True)
train_label_dataframe.rename(columns={0: 'label'}, inplace=True)
test_text_dataframe.rename(columns={0: 'text'}, inplace=True)
test_label_dataframe.rename(columns={0: 'label'}, inplace=True)
train_data = pd.concat([train_text_dataframe, train_label_dataframe], axis=1)
test_data = pd.concat([test_text_dataframe, test_label_dataframe], axis=1)
data = pd.concat([train_data, test_data], axis=0)
data.index = data['text'].str.len()
data = data.sort_index().reset_index(drop=True)
grouped_data = data.groupby(['label'], as_index=False)
# access text by row index
grouped_data.get_group('eng\n').iloc[0].text

lang_a = ['eng\n', 'nld\n', 'slk\n', 'spa\n', 'slv\n', 'ita\n', 'deu\n', 'fra\n']
lang_b = ['en', 'nl', 'sk', 'es', 'sl', 'it', 'de', 'fr']
combined_texts = []
combined_labels = []
combined_percentage = []
percentage = 20
for i in lang_a:
    randoms = [random.randrange(0, 999) for i in range(20)]
    for j in randoms:
        for m in lang_a:
            for n in range(j, j + 10):
                if n < 1000 and m != i:
                    text1 = grouped_data.get_group(i).iloc[j].text.split("\n")[0]
                    text2 = grouped_data.get_group(m).iloc[n].text.split("\n")[0]
                    text1_words = text1.split(" ")
                    text2_words = text2.split(" ")
                    text1_perc = len(text1_words) / (len(text1_words) + len(text2_words)) * 100
                    leng = min(len(text1_words), len(text2_words))
                    combined_texts.append((" ".join(text1_words[0:leng * percentage // 100])) + (
                        " ".join(text2_words[0:leng * (100 - percentage) // 100])))
                    # combined_texts.append(text1+text2)
                    if percentage > 50:
                        combined_labels.append((lang_b[lang_a.index(i)], lang_b[lang_a.index(m)]))
                    else:
                        combined_labels.append((lang_b[lang_a.index(m)], lang_b[lang_a.index(i)]))
                    combined_percentage.append(
                        {lang_b[lang_a.index(i)]: str(percentage), lang_b[lang_a.index(m)]: str(100 - percentage)})

f = open("output/combined_text_sorted_" + str(percentage) + ".txt", "a")
for i in combined_texts[:8000]:
    f.write(i + "\n")
f = open("output/combined_labels_sorted_" + str(percentage) + ".txt", "a")
for i in combined_labels[:8000]:
    f.write(str(i) + "\n")
f = open("output/combined_percentage_sorted_" + str(percentage) + ".txt", "a")
for i in combined_percentage[:8000]:
    f.write(str(i) + "\n")
