# This is the file that implements a flask server to do following use cases :
# language detection, db updates, duplicate detection.

from __future__ import print_function
import json
import flask
from x5gon_rest.controllers import detect_language
from x5gon_rest.fieldnames import VALUE


# The flask app for x5Db use cases
app = flask.Flask(__name__)


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
    text = content[VALUE]
    response = detect_language(text)

    return flask.Response(response=json.dumps(response), status=200, mimetype='application/json')


app.run(host="0.0.0.0", debug=True)

