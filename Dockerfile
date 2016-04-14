FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    python \
    python-dev \
    python-setuptools \
    python-pip \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    supervisor \
    libpq-dev \
    libffi-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libcairo2-dev \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libjpeg-dev

RUN pip install --upgrade pip

ADD . /opt/django
WORKDIR /opt/django
ENV DJANGO_SETTINGS_MODULE wbg.settings.docker
RUN pip3 install -r /opt/django/requirements/development.txt
