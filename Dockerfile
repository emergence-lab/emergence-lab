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
    libjpeg-dev \
    curl \
    apt-transport-https

RUN pip install --upgrade pip

# Install Node
RUN curl --silent https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add -
RUN echo "deb https://deb.nodesource.com/node_5.x trusty main" | tee /etc/apt/sources.list.d/nodesource.list
RUN echo "deb-src https://deb.nodesource.com/node_5.x trusty main" | tee -a /etc/apt/sources.list.d/nodesource.list
RUN apt-get update && apt-get install -y nodejs

# Install Python reqs now for caching
ADD ./requirements /opt/django/requirements
RUN pip3 install -r /opt/django/requirements/development.txt

# Install bower reqs now for caching
RUN npm install -g bower
ADD ./bower.json /opt/django/bower.json
RUN cd /opt/django && bower install --allow-root

ADD . /opt/django
WORKDIR /opt/django
