import requests
from flask import Flask, request, abort, jsonify
from config import VECTORIZER_URI, CLASSIFIER_URI

APP = Flask(__name__)
print('starting api...')

@APP.route('/', methods=['GET'])
def index():
    print('called')
    claim_text = request.get_json(force=True)

    vectored_text = requests.post(
        VECTORIZER_URI, json=claim_text).json()
    print('vectorizer called')

    classified_text = requests.post(
        CLASSIFIER_URI, json=vectored_text)

    print(classified_text.content)
    return jsonify(classified_text.json())

# import os
# PORT = os.getenv('PORT', '5000')
# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=int(PORT))
