import os
from flask import Flask, jsonify, request, render_template, abort
from sklearn.externals.joblib import load as pickle_loader
import csv

# Create the application instance
APP = Flask(__name__)

# Load classification codes and labels
with open('tM/classification_text.csv', mode='r', encoding='utf-8') as infile:
    dict_reader = csv.DictReader(infile)
    ids = { i['label'].lower():i['id'] for i in dict_reader }
print('codes and labels loaded')

# Load the vectorizer
vectorizer = pickle_loader(filename='tM/vectorizer.pkl')
print('vectorizer loaded')

# Load the classifier
classifier = pickle_loader(filename='tM/LRclf.pkl')
print('classifier loaded')

# Classification route
@APP.route('/api/v1.0/classification', methods=['GET'])
def index():

    request_data_as_json = request.get_json(force=True, silent=True)
    if not request_data_as_json:
        return abort(400)

    claim_text = request_data_as_json.get('claim_text', None)
    if not claim_text:
        return abort(400, 'Request JSON missing claim_text parameter.')

    vectored_text = vectorizer.transform([claim_text])

    classification_text = classifier.predict(vectored_text)[0]

    response = {
        'claim_text': claim_text,
        'classification_text': classification_text,
        'classification_code': ids[classification_text],
        'classification_confidence': classifier.predict_proba(
            vectored_text).max()
    }

    return jsonify(response)

# APP.debug = True
# PORT = os.getenv('PORT', '5000')
# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=int(PORT))
