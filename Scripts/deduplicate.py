from __future__ import division
import collections

import argparse
import pandas as pd
import psycopg2
from nltk.corpus import stopwords
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import ray


def load_data(val_query, args):
    try:
        print('Fetching all the Document values with material Ids from Db...')
        conn = psycopg2.connect(host=args.host, database=args.database, user=args.user, password=args.password)
        cur = conn.cursor()
        cur.execute(val_query)
        docsX = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return False
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Successfully fetched '+str(len(docsX))+' documents from the DB')
            return docsX


@ray.remote
def duplicate_detect(z):
    value = z[0]['value']
    length = len(value.split(" "))
    """ Connect to the PostgreSQL database server and get all urls """
    DATA_QUERY = "SELECT material_contents.value,oer_materials.id,material_contents.type," \
                 "material_contents.language,record_id, features_public.value FROM material_contents," \
                 "oer_materials,features_public WHERE material_contents.type!='translation' AND " \
                 "extension='plain' AND oer_materials.word_count>" + str(length - 50) + " AND " \
                                                                                        "oer_materials.word_count<" + str(
        length + 50) + "AND oer_materials.id=material_" \
                       "contents.material_id AND features_public.record_id=oer_materials.id AND " \
                       "oer_materials.duplicate=FALSE ORDER BY oer_materials.id;"

    try:
        conn = psycopg2.connect(host="localhost", database="x5db", user="postgres", password="hayleys")
        cur = conn.cursor()
        cur.execute(DATA_QUERY)
        docs = cur.fetchall()
        cur.close()

        corpus = [(i[0]['value'], i[1], i[2], i[3]) for i in docs]
        df1 = pd.DataFrame([[i[0], len(i[0].split(" ")), i[1], i[2], i[3]] for i in corpus])
        b = list(df1.sort_values(2)[0].values)  # values
        c = list(df1.sort_values(2)[2].values)  # material_ids
        data = [(j[4], j[5]) for j in docs]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')

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
    sim_wiki = cosine_similarity(wiki_transform[ids.index(z[1])], wiki_transform, dense_output=True)

    tf_vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words=sw)
    tf_transform = tf_vectorizer.fit_transform(b)
    sim_tf = cosine_similarity(tf_transform[b.index(z[0]['value'])], tf_transform, dense_output=True)

    assert c == ids, "invalid wiki and tf set"
    tf = [c[j] for j, k in enumerate(sim_tf[0]) if k > 0.85]
    wiki = [c[j] for j, k in enumerate(sim_wiki[0]) if k > 0.95]
    return z[1], len(list(set(tf) & set(wiki))), tf, wiki


def parse_args():
    """Parse input arguments. Refer to default values to set each argument."""
    parser = argparse.ArgumentParser(description='database update')
    parser.add_argument('--host', dest='host', help='database host',
                        default="localhost")
    parser.add_argument('--database', dest='database', help='database name',
                        default='x5db')
    parser.add_argument('--user', dest='user', help='database user',
                        default="postgres")
    parser.add_argument('--password', dest='password', help='database password',
                        default='hayleys')
    parser.add_argument('--procs', dest='procs', help='number of parallel processes',
                        default=10)
    parser.add_argument('--out', dest='out', help='output file name',
                        default="output")
    parser.add_argument('--tf_conf', dest='tf_conf', help='threshold for TF similarity',
                        default=0.85)
    parser.add_argument('--wiki_conf', dest='wiki_conf', help='threshold for WIKI similarity',
                        default=0.95)
    arguments = parser.parse_args()
    return arguments


if __name__ == '__main__':
    ray.init(num_gpus=1)
    sw = stopwords.words("english")
    VAL_QUERY = "SELECT value,material_id FROM material_contents,oer_materials WHERE " \
                "oer_materials.id=material_contents.material_id AND material_contents.type!='translation' AND " \
                "extension='plain' AND oer_materials.duplicate=FALSE "
    args = parse_args()
    documents = load_data(VAL_QUERY, args)
    print(len(documents))
    conn = None
    final = []
    print("Running Duplicate Detection .. ")
    print("{:-<40} {}".format("* Number of Parallel Multiple Processes ", args.procs))
    print("{:-<40} {}".format("* TF similarity Confidence Value ", args.tf_conf))
    print("{:-<40} {}".format("* WIKI similarity Confidence Value ", args.wiki_conf))
    print("{:-<40} {}_tf_{}_wiki_{}_procs_{}.txt".format("* Output File Name ", args.out, args.tf_conf, args.wiki_conf, args.procs))
    # using ray to run multiple duplicate detection jobs in parallel
    try:
        for i in tqdm(range(0, len(documents[50000:60000]), args.procs)):
            futures = [duplicate_detect.remote(i) for i in documents[i:i + args.procs]]
            final.append(ray.get(futures))
    except Exception as e:
        print(e)
    finally:
        file_name = "{}_tf_{}_wiki_{}_procs_{}.txt".format(args.out, args.tf_conf, args.wiki_conf, args.procs)
        f = open(file_name, "w")
        f.write(str(final))
        print('Successfully dumped results to the file {}', file_name)


