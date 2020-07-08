# Contention Classification Model API

This model is designed to accept a string of text containing a disability description and return the proper VA approved classification.


## Setup


Obtain the two model files from someone on the team and add them to the following directories:
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
curl -i -H "Content-Type: application/json" -X POST -d '{"claim_text":["Ringing in my ear", "cancer due to agent orange", "p.t.s.d from gulf war", "recurring nightmares", "skin condition because of homelessness"]}' http://127.0.0.1:5000/
```

The response should look something like:

```
{"classification_code":["3140","8935","8977","8989","9016"],"classification_text":["hearing loss","cancer - genitourinary","gulf war undiagnosed illness","mental disorders","skin"],"flashes_text":["Homeless"],"special_issues_text":["PTSD/1","AOOV","GW"]}
```


#### Python Version: 3.7


Created by: Bennett Gebken

Retrained and packaged by: Nel Abdiel 