# This is the file that implements a flask server to do following use cases :
# language detection, db updates, duplicate detection.

from __future__ import print_function
import json

import flask
import numpy as np
import fasttext
import cld2

# The flask app for x5Db use cases
app = flask.Flask(__name__)
lid_model = fasttext.load_model("./lid.176.ftz")


# method : fastText
def fasttext_detector(text):
    try:
        sentence = text.split("\n")[0]
        result = lid_model.predict([sentence])
        return result[0][0][0].split("_label__")[1], result[1][0][0]
    except Exception as e:
        print(e)
        pass
    return False


# method : cld2
def cld2_detector(text):
    try:
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

    # Return status = 200
    return flask.Response(response="OK \n", status=200, mimetype='application/json')


@app.route('/language_detection', methods=['POST'])
def receive():
    """
    Detects language of the text sent. the text goes through two libraries : FastText and cld2. FastText is used to
    determine the prominent language, if there are multiple languages cld2 is used and both detected languages are
    returned with respective confidence values

    :return: Detected languages with confidence values.
    """
    content = flask.request.json
    text = content["text"]
    fastText_detection = fasttext_detector(text)
    cld2_detection = cld2_detector(text)

    if len(cld2_detection) > 1:
        response = {"detected_lang": [cld2_detection[0][0], cld2_detection[1][0]],
                    "confidence": [str(cld2_detection[0][1]),
                                   str(cld2_detection[1][1])]}
    else:
        response = {"detected_lang": [fastText_detection[0]],
                    "confidence": [str(fastText_detection[1])]}

    return flask.Response(response=json.dumps(response), status=200, mimetype='application/json')


app.run(host="0.0.0.0", debug=True)
