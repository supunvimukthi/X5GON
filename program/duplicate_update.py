import psycopg2
import time
import argparse

start = time.perf_counter()
COLUMN_SEARCH_QUERY = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'oer_materials' \
                ORDER BY ORDINAL_POSITION;"

INSERT_QUERY = "ALTER TABLE oer_materials \
              ADD duplicate BOOLEAN NOT NULL DEFAULT(False)"

UPDATE_QUERY = "UPDATE oer_materials SET duplicate = true WHERE id IN \
        (SELECT material_id FROM material_contents WHERE value->>'value' IN \
        (SELECT DISTINCT (value->>'value') FROM material_contents WHERE type!='translation' AND extension='plain' \
        GROUP BY value HAVING count(id)>1)) AND id NOT IN \
        ( SELECT MAX(material_id) FROM material_contents WHERE type!='translation' AND extension='plain' \
        GROUP BY value HAVING COUNT(id)>1);"

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

        # check if the column already exists
        if "duplicate" not in [i[0] for i in columns]:
            cur = conn.cursor()
            cur.execute(INSERT_QUERY)
            conn.commit()
            cur.close()

        cur = conn.cursor()
        cur.execute(UPDATE_QUERY)
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    print("Time Elapsed : " + str(time.perf_counter() - start))
