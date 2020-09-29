import argparse
import psycopg2
import requests

VALUE_QUERY = "SELECT value,material_id FROM material_contents WHERE material_id IN (SELECT id FROM oer_materials) AND " \
              "type!='translation' AND extension='plain' AND detected_lang IS NOT null;"

COLUMN_SEARCH_QUERY = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'oer_materials' \
                ORDER BY ORDINAL_POSITION;"

INSERT_QUERY = "ALTER TABLE oer_materials \
              ADD detected_lang TEXT[]"

LANGUAGE_API_URL = "localhost:8000/language_detection"
conn = None


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


if __name__ == '__main__':
    args = parse_args()
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=args.host, database=args.database, user=args.user, password=args.password)
        cur = conn.cursor()
        cur.execute(COLUMN_SEARCH_QUERY)
        columns = cur.fetchall()
        cur.close()
        print("Searched for all the columns in 'oer_materials' table")

        # check if the column already exists
        if "detected_lang" not in [i[0] for i in columns]:
            cur = conn.cursor()
            cur.execute(INSERT_QUERY)
            conn.commit()
            cur.close()
            print("New column 'detected_lang' added")

        cur = conn.cursor()
        cur.execute(VALUE_QUERY)
        values = cur.fetchall()
        cur.close()

        cur = conn.cursor()
        for value in values:
            payload = {'value': value[0]}
            r = requests.post(LANGUAGE_API_URL, data=payload)
            UPDATE_QUERY = "UPDATE oer_materials SET language_detected="+r['detected_lang']+" WHERE id=ARRAY "+value[1]
            cur.execute(UPDATE_QUERY)
            conn.commit()
            cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

