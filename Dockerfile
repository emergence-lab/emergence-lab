FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    python \
    python-dev \
    python-setuptools \
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
    libgdk-pixbuf2.0-0
RUN (easy_install pip)

ADD . /opt/django
RUN pip install -r /opt/django/requirements/development.txt
