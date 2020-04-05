FROM python:3.6.9

COPY . /talos

WORKDIR /talos

RUN pip install -e .