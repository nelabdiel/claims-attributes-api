"""Content classificatoin API application. Depends on classifier_service and
vectorizer_service."""

import requests
from flask import Flask, request, abort, jsonify
from config import VECTORIZER_URI, CLASSIFIER_URI

APP = Flask(__name__)

@APP.route('/', methods=['GET', 'POST'])
def index():
    """Primary API route."""

    # Exception handling setup.
    base_error_message = 'Failed to process request: '
    ServiceConnectionError = requests.exceptions.ConnectionError

    # Get claim text JSON from request.
    claim_text = request.get_json(force=True)
    if not claim_text.get('claim_text', None):
        abort(400, '{}Supplied JSON missing claim_text key.'.format(
            base_error_message))

    # Vectorize claim text.
    try:
        vectored_text = requests.post(
            VECTORIZER_URI, json=claim_text).json()
    except ServiceConnectionError:
        abort(500, '{}Vectorizer connection error.'.format(base_error_message))
    if not vectored_text.get('vectored_text', None):
        abort(500, '{}Claim text vectorization error.'.format(
            base_error_message))

    # Classify claim text.
    try:
        classified_text = requests.post(
            CLASSIFIER_URI, json=vectored_text).json()
    except ServiceConnectionError:
        abort(500, '{}Classifier connection error.'.format(base_error_message))
    if not classified_text.get('classification_text', None):
        abort(500, '{}Vectorized claim text classification error.')

    # Return response.
    return jsonify(classified_text)
