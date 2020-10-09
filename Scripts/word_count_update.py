import psycopg2
import pandas as pd
import time
import argparse

from tqdm import tqdm


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
    arguments = parser.parse_args()
    return arguments


def update_word_count():
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=args.host, database=args.database, user=args.user, password=args.password)

        cur = conn.cursor()
        cur.execute(COLUMN_SEARCH_QUERY)
        columns = cur.fetchall()
        cur.close()
        print("Searched for all the columns in 'oer_materials' table")

        # check if the column already exists
        if "word_count" not in [i[0] for i in columns]:
            cur = conn.cursor()
            cur.execute(INSERT_QUERY)
            conn.commit()
            cur.close()
            print("New column 'word_count' added")

            cur = conn.cursor()
            cur.execute(INDEX_QUERY)
            conn.commit()
            cur.close()
            print("created Index on 'word_count' column")

        cur = conn.cursor()
        cur.execute(SEARCH_QUERY)

        docs = cur.fetchall()
        cur.close()
        print("All documents retrieved for checking word count")

        corpus = [[i[0]['value'], len(i[0]['value'].split(" ")), i[1], i[2], i[3]] for i in docs]
        df = pd.DataFrame(corpus)

        lengths = list(df.sort_values(1)[1].values)  # lengths
        material_ids = list(df.sort_values(1)[2].values)  # material_ids
        cur = conn.cursor()
        print("updating word count for each oer material..")

        for i in tqdm(range(len(lengths))):
            UPDATE_QUERY = "UPDATE oer_materials SET word_count=" + str(lengths[i]) + " WHERE id=" + str(material_ids[i]) + ";"
            cur.execute(UPDATE_QUERY)
            conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    args = parse_args()
    start = time.perf_counter()
    COLUMN_SEARCH_QUERY = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'oer_materials' \
                    ORDER BY ORDINAL_POSITION;"

    INSERT_QUERY = "ALTER TABLE oer_materials \
                  ADD word_count INT NOT NULL DEFAULT(0)"

    INDEX_QUERY = "CREATE INDEX index_word_count_oer ON oer_materials(word_count);"

    SEARCH_QUERY = "SELECT material_contents.value,oer_materials.id,material_contents.type,material_contents.language FROM \
                material_contents,oer_materials WHERE material_contents.type!='translation' AND extension='plain' \
                 AND oer_materials.id=material_contents.material_id"
    conn = None
    update_word_count()
    print("Time Elapsed :{:.2f} s ".format(time.perf_counter() - start))
