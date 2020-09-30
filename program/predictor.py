# This is the file that implements a flask server to do following use cases :
# language detection, db updates, duplicate detection.

from __future__ import print_function
import json

import flask
import fasttext
import cld2
import psycopg2
import string

# The flask app for x5Db use cases
app = flask.Flask(__name__)
lid_model = fasttext.load_model("./lid.176.ftz")


def fasttext_detector(text):
    """
    fastText library functionality implementation for the language detection API
    this library is used for prominent language detection
    Args:
        text: (string) text value sent for language detection

    Returns: (dict) detected language with its confidence value or (boolean) if error returns false
    """
    try:
        sentence = text.split("\n")[0]
        result = lid_model.predict([sentence])
        return result[0][0][0].split("_label__")[1], result[1][0][0]
    except Exception as e:
        print(e)
        pass
    return False


def cld2_detector(text):
    """
    cld2 library functionality implementation for the language detection API
    this library is used for multiple language detection
    Args:
        text: (string) text value sent for language detection

    Returns: (dict) detected languages with its confidence values or (boolean) if error returns false

    """
    try:
        text = ''.join(x for x in text if x in string.printable)
        result = cld2.detect(text.strip())
        if result[2][1].language_code != "un":
            return [(result[2][0].language_code, result[2][0].percent),
                    (result[2][1].language_code, result[2][1].percent)]
        else:
            return [(result[2][0].language_code, result[2][0].percent)]

    except Exception as e:
        print(e)
        pass
    return False


@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy by sending 200 response"""

    return flask.Response(response="OK \n", status=200, mimetype='application/json')


@app.route('/language_detection', methods=['POST'])
def language_detect():
    """
    Detects language of the text sent. the text goes through two libraries : FastText and cld2. FastText is used to
    determine the prominent language, if there are multiple languages cld2 is used and both detected languages are
    returned with respective confidence values
    Args:
        flask.request.json: (json) json object with 'value' as key
    Returns: (json) Detected languages with confidence values.
    """
    content = flask.request.json
    text = content["value"]
    fastText_detection = fasttext_detector(text)
    cld2_detection = cld2_detector(text)

    if len(cld2_detection) > 1:
        response = {"detected_lang": [cld2_detection[0][0], cld2_detection[1][0]],
                    "confidence": [str(cld2_detection[0][1]),
                                   str(cld2_detection[1][1])]}
    else:
        if cld2_detection[0][1] > fastText_detection[1]:
            response = {"detected_lang": [fastText_detection[0]],
                        "confidence": [str(fastText_detection[1])]}
        else:
            response = {"detected_lang": [cld2_detection[0][0]],
                        "confidence": [str(cld2_detection[0][1])]}

    return flask.Response(response=json.dumps(response), status=200, mimetype='application/json')


@app.route('/duplicate_detection', methods=['POST'])
def duplicate_detect():
    """
      Detects whether this is a duplicate with any document in the db based on TF and WIKI similarity metrics

      Returns: material_id for the root of duplicate
      """
    content = flask.request.json
    value = content["value"]
    length = len(value.split(" "))
    """ Connect to the PostgreSQL database server and get all urls """
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost", database="x5db", user="postgres", password="hayleys")
        cur = conn.cursor()
        cur.execute(
            "select material_contents.value,oer_materials.id,material_contents.type,material_contents.language from "
            "material_contents,oer_materials where material_contents.type!='translation' and extension='plain' and "
            "oer_materials.word_count>" + str(length - 50) + " and oer_materials.word_count<" + str(length + 50) +
            "and oer_materials.id=material_contents.material_id")

        docs = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    print(len(docs))

app.run(host="0.0.0.0",debug=True)

