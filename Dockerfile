FROM python:3.14.0a1-slim-bookworm

ENV API_KEY ""
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV ALLOWED_IDS ""
LABEL authors="tomer.klein@gmail.com"

RUN apt -yqq update && \
    apt -yqq install gnupg2 && \
    apt -yqq install curl unzip && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip3 install --upgrade pip --no-cache-dir && \
    pip3 install --upgrade setuptools --no-cache-dir

COPY requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt

RUN mkdir -p /opt/botami/tokens

COPY botami /opt/botami

WORKDIR /opt/botami

CMD python botami.py
