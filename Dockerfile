FROM python:3.6.9

COPY ./ai_bot/requirements.txt requirements.txt

RUN pip install -r requirements.txt