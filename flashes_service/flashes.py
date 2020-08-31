from flask import Flask, abort, jsonify, request
import re
import os #Comment out if if at the bottom removed



def CleanText(x):
    x = x.lower().strip()
    #remove periods from abbreviations first to make sure acronyms are collapsed together.
    x = x.replace('.', '')
    cleanString = re.sub('\W+',' ', x)
    return cleanString

def FindFlashes(x):
    flashes = []
    if 'hardship' in x:
        flashes.append('Hardship')
    if 'seriously injured' in x:
        flashes.append('Seriously Injured/Very Seriously Injured')
    if 'terminally ill' in x:
        flashes.append('Terminally Ill')
    if 'homeless' in x:
        flashes.append('Homeless')
    if 'purple heart' in x:
        flashes.append('Purple Heart')
    if ('pow' in x) or ('prisoner of war' in x) or ('p o w' in x):
        flashes.append('POW')
    if 'medal of honor' in x:
        flashes.append('Medal of Honor')
    if ('amyotrophic lateral sclerosis' in x) or ('als' in x) or ('a l s' in x):
        flashes.append('Amyotrophic Lateral Sclerosis')
    if 'emergency care' in x:
        flashes.append('Emergency Care')
    return flashes

flashesD = {'hardship':'Hardship',
            'seriously injured':'Seriously Injured/Very Seriously Injured',
            'terminally ill':'Terminally Ill','homeless':'Homeless',
            'purple heart':'Purple Heart','pow':'POW','prisoner of war':'POW',
            'p o w':'POW', 'medal of honor':'Medal of Honor',
            'amyotrophic lateral sclerosis': 'Amyotrophic Lateral Sclerosis',
            'als':'Amyotrophic Lateral Sclerosis',
            'a l s':'Amyotrophic Lateral Sclerosis',
            'emergency care':'Emergency Care'}


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


# Find a similar special issue
def findSimilar(x):
    temp = ''
    for el in flashesD.keys():
        if ((1. - (1.*minimumEditDistance(el, x)/max(len(el), len(x)))) >= .8) \
        and ((1. - (1.*minimumEditDistance(el, x)/max(len(el), len(x)))) \
             > (1. - (1.*minimumEditDistance(el, temp)/max(len(el), len(temp))))):
            temp = el
    if temp == '':
        results = []
    else:
        results = [flashesD[temp]]

    return results


APP = Flask(__name__)
print('starting flashes service...')



@APP.route('/', methods=['GET', 'POST'])
def index():
    print('flashes service called')
    #print(request.get_json(force=True)['claim_text'])
    try:
        claim_text = request.get_json(force=True)['claim_text']
    except KeyError as e:
        abort(500, e)
        
    Flashes = []
    for el in claim_text:
        Flashes = Flashes + FindFlashes(CleanText(el)) + findSimilar(CleanText(el))
    Flashes = list(set(Flashes))

    return jsonify(
        {'flashes_text': Flashes})

#Comment out everything below for CloudFoundry deployment
if __name__ == '__main__':
    # comment out port information only if deploying container
    port = int(os.environ.get("PORT", 5003))
    APP.run(host='0.0.0.0' , port=port)