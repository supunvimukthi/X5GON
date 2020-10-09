from __future__ import division
import collections

import time
import pandas as pd
import psycopg2
from nltk.corpus import stopwords
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sw = stopwords.words("english")

val_query = "SELECT value,material_id FROM material_contents,oer_materials WHERE " \
            "oer_materials.id=material_contents.material_id AND material_contents.type!='translation' AND " \
            "extension='plain' AND oer_materials.duplicate=FALSE "
conn = None
try:
    conn = psycopg2.connect(host="localhost", database="x5db", user="postgres", password="hayleys")
    cur = conn.cursor()
    cur.execute(val_query)
    docsX = cur.fetchall()
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
        print('Database connection closed.')


def duplicate_detect(z):
    start = time.perf_counter()
    value = z[0]['value']
    length = len(value.split(" "))
    print("{:-<40} {}".format("* length of the material ", length))
    """ Connect to the PostgreSQL database server and get all urls """
    conn = None
    material_val_query = "SELECT material_contents.value,oer_materials.id,material_contents.type," \
                         "material_contents.language,record_id, features_public.value FROM material_contents," \
                         "oer_materials,features_public WHERE material_contents.type!='translation' AND " \
                         "extension='plain' AND oer_materials.word_count>" + str(length - 50) + " AND " \
                         "oer_materials.word_count<" +str(length + 50) + "AND oer_materials.id=material_contents" \
                         ".material_id AND features_public.record_id=oer_materials.id AND " \
                         "oer_materials.duplicate=FALSE ORDER BY oer_materials.id "

    material_wiki_query = "SELECT record_id, features_public.value, oer_materials.language FROM features_public, " \
                          "oer_materials WHERE features_public.record_id = oer_materials.id AND " \
                          "oer_materials.word_count>" + str(length - 50) + " AND oer_materials.word_count<" + str(
        length + 50) + "AND oer_materials.duplicate=FALSE ORDER BY oer_materials.id "
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost", database="x5db", user="postgres", password="hayleys")
        cur = conn.cursor()
        cur.execute(material_val_query)
        docs = cur.fetchall()
        cur.close()
        print("{:-<40} {:.2f} s".format("* Time elapsed - query 0 ", (time.perf_counter() - start)))

        corpus = [(i[0]['value'], i[1], i[2], i[3]) for i in docs]
        df1 = pd.DataFrame([[i[0], len(i[0].split(" ")), i[1], i[2], i[3]] for i in corpus])
        a = list(df1.sort_values(2)[1].values)  # lengths
        b = list(df1.sort_values(2)[0].values)  # values
        c = list(df1.sort_values(2)[2].values)  # material_ids
        data = [(i[4], i[5]) for i in docs]

        cur = conn.cursor()
        cur.execute(material_wiki_query)
        print("{:-<40} {:.2f} s".format("* Time elapsed - query 1 execute ", (time.perf_counter() - start)))
        data = cur.fetchall()
        print("{:-<40} {:.2f} s".format("* Time elapsed - query 1 fetch ", (time.perf_counter() - start)))
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

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

    wiki_vectorizer = DictVectorizer(sparse=True)
    wiki_transform = wiki_vectorizer.fit_transform(wiki)
    print("{:-<40} {:.2f} s".format("* Time Elapsed WIKI transform ", (time.perf_counter() - start)))
    sim_wiki = cosine_similarity(wiki_transform[ids.index(z[1])], wiki_transform, dense_output=True)
    print("{:-<40} {:.2f} s".format("* Time Elapsed WIKI similarity ", (time.perf_counter() - start)))
    tf_vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words=sw)
    tf_transform = tf_vectorizer.fit_transform(b)
    print("{:-<40} {:.2f} s".format("* Time Elapsed TF transform ", (time.perf_counter() - start)))
    sim_tf = cosine_similarity(tf_transform[b.index(z[0]['value'])], tf_transform, dense_output=True)
    tf = [c[j] for j, i in enumerate(sim_tf[0]) if i > 0.85]
    wiki = [c[j] for j, i in enumerate(sim_wiki[0]) if i > 0.95]
    print("{:-<40} {:.2f} s".format("* Time Elapsed TF similarity ", (time.perf_counter() - start)))
    print("{:-<40} {}".format("* TF transform shape ", tf_transform.shape))
    print("{:-<40} {}".format("* WIKI transform shape ", wiki_transform.shape))
    print("{:-<40} {}".format("* matching document count ", str(len(docs))))
    print("{:-<40} {}".format("* Validity (TF vs WIKI) ", c == ids))
    print("{:-<40} {:.2f} s".format("* Total time elapsed ", (time.perf_counter() - start)))
    print("{:-<40} {}".format("* Material ID ", z[1]))
    print("{:-<40} {}".format("* Duplicate Material ID Both ", list(set(tf) & set(wiki))))
    print("{:-<40} {}".format("* Duplicate Material ID TF ", tf))
    print("{:-<40} {}".format("* Duplicate Material ID WIKI ", wiki))
    print("{:-<40} {}".format("* Material ID ", z[1]))
