import sys
import pandas as pd
import numpy as np


# Open training dataset
dfL = pd.read_csv(sys.argv[1])
dfL.head()

print('Preview of our dataset')
print('\n')
print(dfL.head(2))

# clean up text
dfL['CLMANT_TXT'] = dfL.apply(lambda x: x['CLMANT_TXT'].lower().strip(), 1)
dfL['CNTNTN_CLSFCN_TXT'] = dfL.apply(lambda x: x['CNTNTN_CLSFCN_TXT'].lower().strip(), 1)

# open list of approved labels
dfC = pd.read_excel('../data/Contention_Dictionary.xlsx')

# Levenshtein Distance function.
def minimumEditDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]

print('\n')
print('Do not panic, this may take a while')
# Get a list of the new classes
Classifications = list(dfC.apply(lambda x: x['New Contention Classification Text'].lower().strip(), 1))

# Get a list of all unique entries for classes in our dataset.
oldC = dfL['CNTNTN_CLSFCN_TXT'].unique()

# Find the closest approved classification for each unique class in our dataset.
DoC = {}
for el in oldC:
    temp = ''
    for clas in Classifications:
        if ((1. - (1.*minimumEditDistance(el, clas)/max(len(el), len(clas)))) >= .8) \
        and ((1. - (1.*minimumEditDistance(el, clas)/max(len(el), len(clas)))) > \
             (1. - (1.*minimumEditDistance(el, temp)/max(len(el), len(temp))))):
            DoC[el] = clas
            temp = clas

# Create a table with every element with an approved label.
dflt = dfL[dfL['CNTNTN_CLSFCN_TXT'].isin(DoC.keys())]
    
# For every description, find the most common class assigned to it.
dNew = dflt.groupby('CLMANT_TXT').agg(lambda x:x['CNTNTN_CLSFCN_TXT'].value_counts().index[0]).reset_index()

# Dictionary of unique claims and the mode of their label.
dSC = {}
for index, row in dNew.iterrows():
    dSC[row['CLMANT_TXT']] = row['CNTNTN_CLSFCN_TXT']

# Creates a columns on our dataset that associates the results from the previous table to our entries.
dfL['modeClass'] = dfL.apply(lambda x: dSC[x['CLMANT_TXT']] if x['CLMANT_TXT'] in dSC.keys() else None, 1)

# Creates a column with the accepted label corresponding the the most common element.
dfL['newClass'] = dfL.apply(lambda x: DoC[x['modeClass']] if x['modeClass'] in DoC.keys() else None, 1)

print('Here are the first two rows of our dataset')
print(dfL.head(2))

path_to_data = '../data/' + sys.argv[2]
dfL.to_csv(path_to_data)
print('Done. The cleaned up version of your dataset has been save in: ' + path_to_data) 
