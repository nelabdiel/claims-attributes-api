import csv
from flask import Flask, request, abort, jsonify
from sklearn.externals.joblib import load as pickle_loader
from scipy.sparse.csr import csr_matrix
import os #Comment out if if at the bottom removed

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

    classification_text = classifier.predict(vectored_text)
    #print(classification_text)
    classifications = []
    for el in classification_text:
        classifications.append({"code":ids[el], "text": el})
    #print(classifications)
    
    return jsonify(
        {#'classification_text':classification_text.tolist(),
            #'classification_confidence': classifier.predict_proba(
                #vectored_text).max(),
            #'classification_code': classification_codes,
            'classifications': classifications,
        }
    )

#Comment out everything below for CloudFoundry deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    APP.run(host='0.0.0.0' , port=port)