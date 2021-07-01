"""Content classificatoin API application. Depends on classifier_service and
vectorizer_service."""

import requests
from flask import Flask, request, abort, jsonify
from config import VECTORIZER_URI, CLASSIFIER_URI, FLASHES_URI, SPECIAL_ISSUES_URI
import os #Comment out if if at the bottom removed

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
        classifications = requests.post(
            CLASSIFIER_URI, json=vectored_text).json()
    except ServiceConnectionError:
        abort(500, '{}Classifier connection error.'.format(base_error_message))
    if not classifications.get('classifications', None):
        abort(500, '{}Vectorized claim text classification error.')

    # Flashes claim text
    try:
        flashes_text = requests.post(
            FLASHES_URI, json=claim_text).json()
    except ServiceConnectionError:
        abort(500, '{}Flashes connection error.'.format(base_error_message))
    if not flashes_text.get('flashes_text', None):
        abort(500, '{}Flashes finding error.')
        
    # Flashes claim text
    try:
        special_issues_text = requests.post(
            SPECIAL_ISSUES_URI, json=claim_text).json()
    except ServiceConnectionError:
        abort(500, '{}Special Issues connection error.'.format(base_error_message))
    if not special_issues_text.get('special_issues_text', None):
        abort(500, '{}Special Issues finding error.')
        
    #Contentions Classifications Conflated 
    CCC = []
    
    #list of classifications
    listOfC = classifications['classifications']
    
    codes = []
    for i in len(listOfC):
        ClasI = listOfC[i]
        # if we haven't seen the classification code, create it
        Ccode = ClasI[code]
        if Ccode not in codes:
            CCC.append({'code': Ccode, 'classification': ClasI['text'], 'contention': claim_text[i]})
            codes.append(Ccode)
        else:
            # position to update
            ptu = codes.index(Ccode)
            newContention = '%s. %s' % (CCC[ptu]['contention'], claim_text[i])
            CCC[ptu] = {'code': CCC[ptu]['code'], 'classification': CCC[ptu]['classification'], 'contention': newContention}
            
    # create a dictionary to save the results         
    classifications = {'results': CCC}
    
    payload = {}
    payload.update(classifications)
    payload.update(flashes_text)
    payload.update(special_issues_text)
    #print(payload)
    # Return response.
    return jsonify(payload)

#Comment out everything below for CloudFoundry deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    APP.run(host='0.0.0.0' , port=port)