import os
import argparse
import psycopg2
import requests
from tqdm import tqdm


def parse_args():
    """Parse input arguments. Refer to default values to set each argument."""
    parser = argparse.ArgumentParser(description='database update')
    parser.add_argument('--host', dest='host', help='database host',
                        default="localhost")
    parser.add_argument('--database', dest='database', help='database name',
                        default='x5gon_dirty')
    parser.add_argument('--user', dest='user', help='database user',
                        default="postgres")
    parser.add_argument('--password', dest='password', help='database password',
                        default='hayleys')
    arguments = parser.parse_args()
    return arguments


def main(args):
    try:
        """ Get all column names in the oer material table to check whether 'language_detected' column exists"""
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=args.host, database=args.database, user=args.user, password=args.password)
        cur = conn.cursor()
        cur.execute(COLUMN_SEARCH_QUERY)
        columns = cur.fetchall()
        cur.close()
        print("Searched for all the columns in 'oer_materials' table")

        """ if 'language detected' column does not exist insert the column to the table """
        if "language_detected" not in [i[0] for i in columns]:
            cur = conn.cursor()
            cur.execute(COLUMN_INSERT_QUERY)
            conn.commit()
            cur.close()
            print("New column 'language_detected' added")

        """ get all the material contents for oer_materials which has NULL value for the 'language_detected' field"""
        cur = conn.cursor()
        cur.execute(VALUE_QUERY)
        values = cur.fetchall()
        cur.close()
        count = len(values)

        """ update all oer_materials with detected languages from the language API"""
        cur = conn.cursor()
        for value in tqdm(values):
            payload = {"value": str(value[0]['value'])}
            r = requests.post(LANGUAGE_API_URL, json=payload)
            UPDATE_QUERY = "UPDATE oer_materials SET language_detected=ARRAY " + str(
                r.json()['detected_lang']) + " WHERE id=" + str(value[1])
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
    VALUE_QUERY = "SELECT value,material_id FROM material_contents WHERE material_id IN (SELECT id FROM oer_materials " \
                  ") AND type!='translation' AND extension='plain';"

    COLUMN_SEARCH_QUERY = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'oer_materials' \
                    ORDER BY ORDINAL_POSITION;"

    COLUMN_INSERT_QUERY = "ALTER TABLE oer_materials \
                  ADD language_detected TEXT[]"

    LANGUAGE_API_URL = os.environ["LANGUAGE_API_URL"]
    conn = None
    count = 0
    args = parse_args()
    main(args)
