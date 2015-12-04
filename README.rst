=============
Emergence Lab
=============

.. image:: https://travis-ci.org/emergence-lab/emergence-lab.svg?branch=master
    :target: https://travis-ci.org/emergence-lab/emergence-lab
    :alt: Test Status

.. image:: https://coveralls.io/repos/emergence-lab/emergence-lab/badge.svg
    :target: https://coveralls.io/r/emergence-lab/emergence-lab
    :alt: Code Coverage

.. image:: https://landscape.io/github/emergence-lab/emergence-lab/master/landscape.svg?style=flat
    :target: https://landscape.io/github/emergence-lab/emergence-lab/master
    :alt: Code Health

Web-based application written in Django with the following goals:

#) Improve tracking and discoverability of experimental samples and data, both process and characterization data
#) Allow data-driven experimentation by allowing programmable access to data via an embedded iPython notebook
#) Provide project management functionality to help organize experiments and samples
#) Have a clean, consistent user interface to encourage best-practices for use

Installation Instructions
=========================

Docker
------

The easiest way to get Emergence Lab up and running is to build a Docker container.

You can get Docker by navigating `here <http://docs.docker.com/compose/install/>`_. Follow the instructions to install both Docker and docker-compose. Note that users of OS X only need to install the Docker toolkit. For dependencies, install `node.js <http://nodejs.org>`_ and then ```npm install -g bower```.

After installing Docker and Bower, go to your command line and use the following commands:

.. code::

    $ git clone https://github.com/emergence-lab/emergence-lab.git
    $ cd emergence-lab
    $ bower install
    $ cp wbg/settings.docker.json wbg/settings.json
    $ docker-machine start default
    $ docker-compose build
    $ docker-compose up &
    $ docker exec -it emergencelab_web_1 python /opt/django/manage.py migrate --settings=wbg.settings.docker
    $ docker exec -it emergencelab_web_1 python /opt/django/manage.py collectstatic --noinput --settings=wbg.settings.docker

Create an administrative user by entering:

.. code::

    $ docker exec -it emergencelab_web_1 python /opt/django/manage.py createsuperuser --settings=wbg.settings.docker

Get your docker machine IP address:

.. code::

    $ docker-machine ip default

Then fire up your web browser and go to ```<IP Address>:8000``` and login with the username and password you created. Enjoy!

Shutting down the container
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To shut down Emergence, run ```docker-compose stop```.

Additional Development Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To facilitate development, you can change the ```DEBUG``` and ```TEMPLATE_DEBUG``` settings in ```wbg/settings/docker.py``` to ```True```, and edit ```docker-compose.yml```, line 13 with the path to your git repository.

Manual Install
--------------

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

.. code::

    $ pip install -r requirements/development.txt
    $ bower install

Configure Application
~~~~~~~~~~~~~~~~~~~~~

Copy the template secrets file and edit with database and ldap configuration.

.. code::

    $ cp wbg/secrets.template.json wbg/secrets.json
    $ vim wbg/secrets.json

Running Tests
-------------

Tests are run using tox, environments configured are for python 2.7 and flake8. To run them, invoke tox from the command line.

.. code::

    $ tox
