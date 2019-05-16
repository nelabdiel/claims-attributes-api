import sys
import numpy as np
import pandas as pd

from sklearn.externals import joblib


# get codes for prediction
dfLabels = pd.read_excel('./LinnauesClassifier/data/Contention_Dictionary.xlsx')
dLabels = {}
for index, row in dfLabels.iterrows():
    dLabels[row['New Contention Classification Text'].lower().strip()] = row['IDs']

# load the vectorizer
vectorizer = joblib.load(filename='./tM/vectorizer.pkl')
# load the classifier
clf = joblib.load(filename='./tM/LRclf.pkl')

# Load Dataset
df = pd.read_csv(sys.argv[1])
df['CLMANT_TXT'] = df.apply(lambda x: x['CLMANT_TXT'].lower().strip(), 1)

#Vectorize data
X = vectorizer.transform(df['CLMANT_TXT'])

# Predict Label
df['predictedLabel'] = clf.predict(X)

df['predictedID'] = df.apply(lambda x: dLabels[x['predictedLabel']], 1)

#Save file
file_name = './LinnaeusClassifier/data/predicted' + sys.argv[1].split('/')[-1]
df.to_csv(file_name)

print('Done. Results have been saved in: ' + file_name)
