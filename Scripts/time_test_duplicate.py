import collections
import time

import pandas as pd
import psycopg2
from nltk.corpus import stopwords
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def time_test(length):
    start = time.perf_counter()
    conn = None
    material_val_query = "SELECT material_contents.value,oer_materials.id,material_contents.type," \
                         "material_contents.language,record_id, features_public.value FROM material_contents," \
                         "oer_materials,features_public WHERE material_contents.type!='translation' AND " \
                         "extension='plain' AND oer_materials.word_count>" + str(length - 50) + " AND " \
                         "oer_materials.word_count<" + str(length + 50) + "AND oer_materials.id=material_contents" \
                         ".material_id AND features_public.record_id=oer_materials.id ORDER BY oer_materials.id "

    try:
        conn = psycopg2.connect(host="localhost", database="x5db", user="postgres", password="hayleys")
        cur = conn.cursor()
        cur.execute(material_val_query)
        docs = cur.fetchall()
        cur.close()
        corpus = [(i[0]['value'], i[1], i[2], i[3]) for i in docs]
        df1 = pd.DataFrame([[i[0], len(i[0].split(" ")), i[1], i[2], i[3]] for i in corpus])
        a = list(df1.sort_values(2)[1].values)  # lengths
        b = list(df1.sort_values(2)[0].values)  # values
        c = list(df1.sort_values(2)[2].values)  # material_ids
        data = [(i[4], i[5]) for i in docs]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    ids = []
    wiki = []
    for row in data:
        temp = []
        num = row[1]["value"]
        dicTemp = collections.defaultdict(float)
        # f = {}
        for i in range(len(num)):
            temp.append(num[i]["name"])
            temp.append(num[i]["cosine"])
        for k in range(0, len(temp), 2):
            dicTemp[temp[k]] = temp[k + 1]
        wiki.append(dicTemp)
        ids.append(row[0])
    sw = stopwords.words("english")

    wiki_vectorizer = DictVectorizer(sparse=True)
    wiki_transform = wiki_vectorizer.fit_transform(wiki)
    sim_wiki = cosine_similarity(wiki_transform[-1], wiki_transform, dense_output=True)

    tf_vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words=sw)
    tf_transform = tf_vectorizer.fit_transform(b)
    sim_tf = cosine_similarity(tf_transform[-1], tf_transform, dense_output=True)
    return length, len(docs), (time.perf_counter() - start)


print(" {:-<20}{:-<20}{:<20} ".format("word count", "documents count", "time taken"))
for i in range(0, 10000, 200):
    x = time_test(i)
    print(" {:-<20}{:-<20}{:.2f} ".format(str(x[0]), x[1], x[2]))
