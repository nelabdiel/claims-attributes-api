from flask import Flask, abort, jsonify, request
from sklearn.externals.joblib import load as pickle_loader
import os #Comment out if if at the bottom removed

APP = Flask(__name__)
print('starting vectorizer service...')

# Load the vectorizer
vectorizer = pickle_loader(filename='data/vectorizer.pkl')
print('vectorizer loaded')

@APP.route('/', methods=['GET', 'POST'])
def index():
    print('vectorizer service called')
    #print(request.get_json(force=True)['claim_text'])
    try:
        claim_text = request.get_json(force=True)['claim_text']
    except KeyError as e:
        abort(500, e)
        
        
    vectored_text_as_matrix = vectorizer.transform(claim_text)

    return jsonify(
        {'vectored_text': vectored_text_as_matrix.toarray().tolist() })

#Comment out everything below for CloudFoundry deployment
if __name__ == '__main__':
    # comment out port information only if deploying container
    port = int(os.environ.get("PORT", 5001))
    APP.run(host='0.0.0.0' , port=port)