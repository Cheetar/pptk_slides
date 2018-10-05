FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
ADD . /code

RUN pip3 install -r /code/requirements.txt
