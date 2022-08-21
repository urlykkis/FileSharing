FROM python:3.10-slim-buster

COPY ./app /src/
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


WORKDIR /src/

EXPOSE 8000

CMD uvicorn app:app --reload