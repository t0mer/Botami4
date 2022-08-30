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
    pip3 install Tami4EdgeAPI --no-cache-dir

#=========
# Firefox
#=========
ARG FIREFOX_VERSION=firefox-93.0
RUN FIREFOX_DOWNLOAD_URL=https://download-installer.cdn.mozilla.net/pub/firefox/releases/93.0/linux-x86_64/en-US/firefox-93.0.tar.bz2 \
  && apt-get update -qqy \
  && apt-get -qqy --no-install-recommends install firefox libavcodec-extra \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
  && wget --no-verbose -O /tmp/firefox.tar.bz2 $FIREFOX_DOWNLOAD_URL \
  && apt-get -y purge firefox \
  && rm -rf /opt/firefox \
  && tar -C /opt -xjf /tmp/firefox-93.0.tar.bz2 \
  && rm /tmp/firefox-93.0.tar.bz2 \
  && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
  && ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox

#============
# GeckoDriver
#============
ARG GECKODRIVER_VERSION=latest
RUN GK_VERSION=$(if [ ${GECKODRIVER_VERSION:-latest} = "latest" ]; then echo "0.31.0"; else echo $GECKODRIVER_VERSION; fi) \
  && echo "Using GeckoDriver version: "$GK_VERSION \
  && wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GK_VERSION/geckodriver-v$GK_VERSION-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-$GK_VERSION \
  && chmod 755 /opt/geckodriver-$GK_VERSION \
  && ln -fs /opt/geckodriver-$GK_VERSION /usr/bin/geckodriver

USER 1200

#============================================
# Dumping Browser name and version for config
#============================================
RUN echo "firefox" > /opt/selenium/browser_name




RUN mkdir -p /opt/botami

COPY botami /opt/botami

WORKDIR /opt/botami

CMD python botami.py
