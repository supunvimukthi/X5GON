# This is the file that implements a flask server to do following use cases :
# language detection, db updates, duplicate detection.

from __future__ import print_function

import base64
import json
import os
import sys
import warnings
from collections import namedtuple
from io import BytesIO

import flask
import numpy as np
import tensorflow as tf
from PIL import Image
import fasttext
import cld2

# The flask app for x5Db use cases
app = flask.Flask(__name__)
lid_model = fasttext.load_model("./lid.176.ftz")


# method : fasttext
def fastText_Detector(text, label):
    try:
        sentence = text.split("\n")[0]
        result = lid_model.predict([sentence])
        if result[0][0][0].split("_label__")[1] == label:
            return True
    except Exception as e:
        print(e)
        pass
    return False


# method : cld2
def cld2_Detector(text, label):
    try:
        result = cld2.detect(text.strip())
        if result[2][0].language_code == label:
            return True
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
    Detects language of the text sent. the text goes through two libraries : fasttext and cld2.
    Fasttext is used to determine the prominent language, if there are multiple languages cld2 is used.

    :return: Detected languages with confidence value.
    """


    # Returning the final final object as Flask response
    return flask.Response(response=json.dumps(outobject), status=200, mimetype='application/json')
