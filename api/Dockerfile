FROM python:3.7

Maintainer Nel Abdiel "nel.abdiel@pif.gov"
# tell the port number the container should expose
#EXPOSE 5000

# run the application
#command: gunicorn -w 4 -b 127.0.0.1:5000 classificationAPI:app
#CMD ["python", "classificationAPI.py"]
#CMD ["gunicorn", , "-w" ,"4" , "-b", "0.0.0.0:5000", "classificationAPI:app"]

# make directories suited to your application 
RUN mkdir -p /home/project/app
RUN mkdir -p /home/project/app/tM
WORKDIR /home/project/app

# copy and install packages for flask
COPY requirements.txt /home/project/app
RUN pip install --no-cache-dir -r requirements.txt

# copy contents from your local to your docker container
COPY . /home/project/app
COPY ./tM /home/project/app/tM