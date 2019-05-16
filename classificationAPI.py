import os
from flask import Flask, jsonify, request, render_template, abort
from sklearn.externals import joblib
import pandas as pd
import numpy as np


# get codes for prediction
dfLabels = pd.read_excel('LinnaeusClassifier/data/Contention_Dictionary.xlsx')
dLabels = {}
for index, row in dfLabels.iterrows():
    dLabels[row['New Contention Classification Text'].lower().strip()] = row['IDs']

# load the vectorizer
vectorizer = joblib.load(filename='tM/vectorizer.pkl')
# load the classifier
clf = joblib.load(filename='tM/LRclf.pkl')


# Create the application instance
app = Flask(__name__)


# Create a URL route in our application for "/"

@app.route('/api/v1.0/classification', methods=['POST'])
def index():
    if request.json:
            text = request.json['claim_text']
            vText = vectorizer.transform([text])
            classification = clf.predict(vText)[0]
            confidence = str(int(clf.predict_proba(vText).max()*100)) + '%'
            code = dLabels[classification]
            print('yes')
            print('\n')
            
            d = {'text': text, 'prediction': {
                 'classification': classification,
                 'code':code,
                 'probability': confidence}}
            return jsonify(d)
    else:
        abort(404)

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)