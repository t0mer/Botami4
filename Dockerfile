FROM python:latest

ENV API_KEY ""
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV ALLOWED_IDS ""

RUN apt -yqq update && \
    apt -yqq install gnupg2 && \
    apt -yqq install curl unzip && \
    apt -yqq install iputils-ping && \
    apt -yqq install xvfb && \
    apt -yqq install fonts-ipafont-gothic xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip3 install --upgrade pip --no-cache-dir && \
    pip3 install --upgrade setuptools --no-cache-dir && \
    pip3 install Tami4EdgeAPI --no-cache-dir