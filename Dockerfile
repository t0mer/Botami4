FROM python:latest

ENV API_KEY ""
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV ALLOWED_IDS ""
ENV PHONE_NUMBER ""
LABEL authors="tomer.klein@gmail.com"

RUN apt -yqq update && \
    apt -yqq install gnupg2 && \
    apt -yqq install curl unzip && \
    apt -yqq install iputils-ping && \
    apt -yqq install xvfb && \
    apt -yqq install fonts-ipafont-gothic xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip3 install --upgrade pip --no-cache-dir && \
    pip3 install --upgrade setuptools --no-cache-dir && \
    pip3 install pypasser --no-cache-dir && \
    pip3 install loguru --no-cache-dir && \
    pip3 install Tami4EdgeAPI --no-cache-dir






RUN mkdir -p /opt/botami

COPY botami /opt/botami

WORKDIR /opt/botami

CMD python botami.py
