#FROM python:latest

FROM selenium/standalone-firefox

ENV API_KEY ""
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV ALLOWED_IDS ""
ENV PHONE_NUMBER ""


    
RUN pip install --upgrade pip --no-cache-dir && \
    pip install --upgrade setuptools --no-cache-dir && \
    pip install pypasser --no-cache-dir && \
    pip install Tami4EdgeAPI --no-cache-dir

RUN mkdir -p /opt/botami

COPY botami /opt/botami

WORKDIR /opt/botami

CMD python botami.py
