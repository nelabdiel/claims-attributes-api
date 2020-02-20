import csv
from flask import Flask, request, abort, jsonify
from sklearn.externals.joblib import load as pickle_loader
from scipy.sparse.csr import csr_matrix

APP = Flask(__name__)
print('starting classifier_service...')

# Load classification codes and labels
with open('data/classification_text.csv', mode='r') as infile:
    dict_reader = csv.DictReader(infile)
    ids = { i['label'].lower().strip():i['id'] for i in dict_reader }
print('codes and labels loaded')

# Load the classifier
classifier = pickle_loader(filename='data/LRclf.pkl')
print('classifier loaded')

@APP.route('/', methods=['GET', 'POST'])
def index():
    print('classifier service called')

    raw_vectored_text = request.get_json(force=True)['vectored_text']
    vectored_text = csr_matrix(raw_vectored_text)

    output = []
    classifications = classifier.predict(vectored_text)

    for classification in classifications:
        output.append({
            'classification_text':classification.strip(),
            'classification_confidence': classifier.predict_proba(
                vectored_text).max(),
            # TODO: this line needs a fix - we're passing the array of vectors in there
            # so we'll return the same confidence for every classification
            'classification_code': ids[classification],
        })

    return jsonify(output)
