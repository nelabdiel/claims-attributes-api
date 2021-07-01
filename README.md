# Claims Attributes API

beta version
# Warning: this version is not backwards compatible as it groups together all the contentions with the same classification


# Updates: The current version now supports multiple contentions in the same request and returns additional information about flashes and special issues.

This API uses Natural Language Understading to infer 526 Benefit Claims Attributes, like classification, flashes and special issues,  from text and other features.


## Setup


Obtain the vectorier and predictive model files from someone on the team and add them to the following directories:
```
classifier_service/data/LRclf.pkl
vectorizer_service/data/vectorizer.pkl
```

### If deploying in container comment out the port assignment in each .py of /api and /*_service/

### Running locally (not containerized) 

Open three terminal tabs, one to `/api`, one to `/classifier_service`, one to `/vectorizer_service`, , one to `/flashes_service`, one to `/special_issues_service`.

Export the following vars in each respective tab:

```
export FLASK_APP=api.py 
export VECTORIZER_URI=http://127.0.0.1:5001/
export CLASSIFIER_URI=http://127.0.0.1:5002/
export FLASHES_URI=http://127.0.0.1:5003/
export SPECIAL_ISSUES_URI=http://127.0.0.1:5004/
python api.py
```

```
export FLASK_RUN_PORT=5001
export FLASK_APP=vectorizer.py
python vectorizer.py
```

```
export FLASK_RUN_PORT=5002
export FLASK_APP=classifier.py
python classifier.py
```

```
export FLASK_RUN_PORT=5003
export FLASK_APP=flashes.py
python flashes.py
```

```
export FLASK_RUN_PORT=5004
export FLASK_APP=special_issues.py
python special_issues.py
```


#### Example API call

```
curl -i -H "Content-Type: application/json" -X POST -d '{"claim_text":["Ringing in my ear", "trouble hearing", "cancer due to agent orange", "p.t.s.d from gulf war", "recurring nightmares", "skin condition because of homelessness"]}' http://127.0.0.1:5000/
```

The response should looks like this:

```
{"classifications":[{"code": "3140", "classification": "hearing loss", "contention": "Ringing in my ear. trouble hearing"}, {"code": "8935", "classification": "cancer - genitourinary", "contention": "cancer due to agent orange"}, {"code": "8977", "classification": "gulf war undiagnosed illness", "contention": "p.t.s.d from gulf war"}, {"code": "8989", "classification": "mental disorders", "contention": "recurring nightmares"}, {"code": "9016", "classification": "skin", "contention": "skin condition because of homelessness"}],"flashes_text":["Homeless"],"special_issues_text":["PTSD/1","AOOV","GW"]}
```


#### Python Version: 3.7


Created by: Nel Abdiel 

Based on the work done by: Bennett Gebken

Restructure by: Patrick Bateman, Alex Prokop
