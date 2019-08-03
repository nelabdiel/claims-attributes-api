FROM python:3.7

MAINTAINER Nel Abdiel "nel.abdiel@pif.gov"

RUN mkdir -p /home/project/app
RUN mkdir -p /home/project/app/tM
WORKDIR /home/project/app

COPY requirements.txt /home/project/app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/project/app
COPY ./tM /home/project/app/tM
