from flask import Flask, abort, jsonify, request
import re
import os #Comment out if if at the bottom removed


def CleanText(x):
    x = x.lower().strip()
    #remove periods from abbreviations first to make sure acronyms are collapsed together.
    x = x.replace('.', '')
    cleanString = re.sub('\W+',' ', x)
    return cleanString

spi = {'als': 'ALS','amyotrophic lateral sclerosis': 'ALS',
       'agent orange': 'AOOV','ao': 'AOOV','herbicide': 'AOOV',
       'asbestos': 'ASB',
       'asbestosis': 'ASB','gulf war': 'GW','burn pits': 'GW',
       'hepatitis c': 'HEPC','hep c': 'HEPC','hepatitus c': 'HEPC',
       'hiv': 'HIV','mustard': 'MG','mst': 'MST','sexual trauma': 'MST',
       'sexual assault': 'MST','prisoner': 'POW','pow': 'POW','ptsd': 'PTSD/1',
       'post traumatic stress': 'PTSD/1','p t s d': 'PTSD/1',
       'posttraumatic stress': 'PTSD/1','postraumatic stress': 'PTSD/1',
       'pts': 'PTSD/1','shell shock': 'PTSD/1',
       'stress post traumatic': 'PTSD/1','stress disorder': 'PTSD/1',
       'personal trauma': 'PTSD/3','acquired psychiatric': 'PTSD/3',
       'radiation': 'RDN','sarcoidosis': 'SARCO', 'tbi': 'TBI',
       't b i': 'TBI', 'traumatic brain injury': 'TBI',
       'c 123': 'C123','c123': 'C123'}

def findSI(x):
    issues = []
    for fl in spi.keys():
        if (fl in x) and (spi[fl] not in issues):
            issues.append(spi[fl])
    if ('AOOV' in issues) and ('vietnam' in x):
        issues.append('AOIV')
        issues.remove('AOOV')
    if ('PTSD/1' in issues) and ('non combat' in x):
        issues.append('PTSD/2')
        issues.remove('PTSD/1')
    return issues


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
    for el in spi.keys():
        if ((1. - (1.*minimumEditDistance(el, x)/max(len(el), len(x)))) >= .8) \
        and ((1. - (1.*minimumEditDistance(el, x)/max(len(el), len(x)))) \
             > (1. - (1.*minimumEditDistance(el, temp)/max(len(el), len(temp))))):
            temp = el

    if temp == '':
        results = []
    else:
        results = [spi[temp]]

    return results


APP = Flask(__name__)
print('starting special issues service...')


@APP.route('/', methods=['GET', 'POST'])
def index():
    print('special issues service called')
    #print(request.get_json(force=True)['claim_text'])
    try:
        claim_text = request.get_json(force=True)['claim_text']
    except KeyError as e:
        abort(500, e)
        
    SpecialIssues = []
    for el in claim_text:
        SpecialIssues = SpecialIssues + findSI(CleanText(el)) + findSimilar(CleanText(el))
    SpecialIssues = list(set(SpecialIssues))

    return jsonify(
        {'special_issues_text': SpecialIssues })

#Comment out everything below for CloudFoundry deployment
if __name__ == '__main__':
    # comment out port information only if deploying container
    port = int(os.environ.get("PORT", 5004))
    APP.run(host='0.0.0.0' , port=port)