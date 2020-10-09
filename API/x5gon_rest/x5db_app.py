# This is the file that implements a flask server to do following use cases :
# language detection, TODO : db updates, duplicate detection.

from __future__ import print_function
from flask import Flask, request, Response, Blueprint
import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restplus import Api, Resource, fields, apidoc

from x5gon_rest._configs import LATEST_API_VERSION
from x5gon_rest.controllers import detect_language
from x5gon_rest.fieldnames import VALUE, CONFIDENCE, DETECTED_LANGUAGE, ERROR

# The flask app for x5Db use cases
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
blueprint = Blueprint('ld_api', __name__, url_prefix='/')

api = Api(blueprint, title='X5DB Language Detection API', version=LATEST_API_VERSION,
          description='A simple API to detect language of a given text',
          doc='/docs/')

app.register_blueprint(blueprint)

value_fields = api.model('Raw Document', {
    VALUE: fields.String(required=True,
                         description="raw text document to be sent for the language detection"),
})

response_fields = api.model('Language Detection', {
    DETECTED_LANGUAGE: fields.String(required=True,
                                     description="list of languages detected"),
    CONFIDENCE: fields.String(required=True,
                              description="list of corresponding confidence values for the languages detected"),
})

error_fields = api.model('Error Response', {
    ERROR: fields.String(description="error caused"),
})


@api.route('info')
class APIInfo(Resource):
    def get(self):
        """Information about the API endpoint"""
        return {'version': LATEST_API_VERSION,
                'currency': 'latest',
                'status': 'stable'}


@api.route('language_detection')
class LanguageDetect(Resource):
    @api.doc('language detect', )
    @api.expect(value_fields)
    @api.response(200, 'Success', response_fields)
    @api.response(501, 'Error', error_fields)
    def post(self):
        """
        Detects language of the text sent.
        The text goes through two libraries : FastText and cld2. FastText is used to
        determine the prominent language, if there are multiple languages cld2 is used
        and both detected languages are returned with respective confidence values
        """
        json_data = request.json
        detections = detect_language(json_data[VALUE])
        return detections
