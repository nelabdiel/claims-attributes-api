import os
from flask import Flask, jsonify, request, render_template, redirect, abort
from bokeh.util.string import encode_utf8
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
#Index page
@app.route('/')
def main():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        html = render_template('index.html')
        return html

    else:
        if request.form:
            text = request.form['claim_text']
            vText = vectorizer.transform([text])
            classification = clf.predict(vText)[0]
            confidence = str(int(clf.predict_proba(vText).max()*100)) + '%'
            code = dLabels[classification]

            d = {'text': text, 'prediction': {
                 'classification': classification,
                 'code':code,
                 'probability': confidence}}
            #return jsonify(d)
        
            html = render_template('results.html', results=d)
            return encode_utf8(html)
        else:
            return abort(404)

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)