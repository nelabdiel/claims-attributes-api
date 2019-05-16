import sys
import numpy as np
import pandas as pd
from sklearn.externals import joblib


# get codes for prediction
dfLabels = pd.read_excel('./LinnaeusClassifier/data/Contention_Dictionary.xlsx')
dLabels = {}
for index, row in dfLabels.iterrows():
    dLabels[row['New Contention Classification Text'].lower().strip()] = row['IDs']

# load the vectorizer
vectorizer = joblib.load(filename='tM/vectorizer.pkl')
# load the classifier
clf = joblib.load(filename='tM/LRclf.pkl')

def main(arg=None):
    if len(arg) > 1:
        # Load string and clean it
        text = arg[1]
        text = [text.lower().strip()]

        #Vectorize data
        X = vectorizer.transform(text)
        # predict value
        y = clf.predict(X)[0]
        # predict code
        y_code = dLabels[clf.predict(X)[0]]
        d = {text :[y, y_code]}
        # print string and value
        print(d)
    else:
        print('please include the string that needs to be scored')

if __name__ == '__main__':
    main(sys.argv)