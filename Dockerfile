FROM python:3.7

COPY . /talosbot

WORKDIR /talosbot

RUN pip install -e .