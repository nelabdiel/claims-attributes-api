FROM python:3.5

Maintainer Nel Abdiel "nel.abdiel@pif.gov" GH: nelabdiel
# tell the port number the container should expose
#EXPOSE 5002

# run the application
#command: gunicorn -w 4 -b 127.0.0.1:5002 classifier:app
#CMD ["python", "classifierAPI.py"]
#CMD ["gunicorn", , "-w" ,"4" , "-b", "0.0.0.0:5002", "classifierAPI:app"]

# make directories suited to your application 
RUN mkdir -p /home/project/app
RUN mkdir -p /home/project/app/data
WORKDIR /home/project/app

# copy and install packages for flask
COPY requirements.txt /home/project/app
RUN pip install --no-cache-dir -r requirements.txt

# copy contents from your local to your docker container
COPY . /home/project/app
COPY ./data /home/project/app/data
