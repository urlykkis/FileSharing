FROM python:3.10-slim-buster

COPY ./app /src/
COPY requirements.txt requirements.txt
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip3 install -r requirements.txt

WORKDIR /src/

EXPOSE 8000