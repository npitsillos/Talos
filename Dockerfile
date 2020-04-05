FROM python:3.6.8

COPY . /talos

WORKDIR /talos

RUN pip install -e .