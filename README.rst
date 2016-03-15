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

.. image:: https://www.versioneye.com/user/projects/5672d2a6107997003e00064d/badge.svg?style=flat
    :target: https://www.versioneye.com/user/projects/5672d2a6107997003e00064d/
    :alt: Dependencies

Web-based application written in Django with the following goals:

#) Improve tracking and discoverability of experimental samples and data, both process and characterization data
#) Allow data-driven experimentation by allowing programmable access to data via an embedded iPython notebook
#) Provide project management functionality to help organize experiments and samples
#) Have a clean, consistent user interface to encourage best-practices for use

Installation Instructions
=========================

Node.js
-------

Emergence uses Node.js for some server-side functionality. Install `Node.js <http://nodejs.org>`_ and then run ``npm install -g bower`` to install Bower.


Docker
------

The easiest way to get Emergence Lab up and running is to build a Docker container. Linux users can install Docker and docker-compose via their package manager. For OS X and Windows users, the `Docker Toolbox <https://docker.com/docker-toolbox/>`_ has everything you need to get started.

Setting up the Container
~~~~~~~~~~~~~~~~~~~~~~~~

After installing Docker and Bower, go to your command line (or Docker shell) and use the following commands:

.. code::

    $ git clone https://github.com/emergence-lab/emergence-lab.git
    $ cd emergence-lab
    $ bower install
    $ cp wbg/secrets.docker.json wbg/secrets.json
    $ docker-machine start default  ## OS X and Windows only
    $ docker-compose build
    $ docker-compose up &
    $ docker exec -it emergencelab_web_1 python manage.py migrate
    $ docker exec -it emergencelab_web_1 python manage.py collectstatic --noinput

Create an administrative user by entering:

.. code::

    $ docker exec -it emergencelab_web_1 python manage.py createsuperuser

Get your docker machine IP address:

.. code::

    $ docker-machine ip default

Then fire up your web browser and go to ``<IP Address>:8000`` or ``localhost:8000`` and login with the username and password you created. Enjoy!

Shutting down the container
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To shut down Emergence, run ``docker-compose stop``.

Additional Development Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To facilitate development, you can change the ``DEBUG`` and ``TEMPLATE_DEBUG`` settings in ``wbg/settings/docker.py`` to ``True``, and edit ``docker-compose.yml``, line 13 with the path to your git repository.

Manual Install
--------------

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

.. code::

    $ pip install -r requirements/development.txt
    $ bower install

Configure Application
~~~~~~~~~~~~~~~~~~~~~

Copy the template secrets file and edit with database and ldap (optional) configuration.

.. code::

    $ cp wbg/secrets.template.json wbg/secrets.json
    $ vim wbg/secrets.json

Running Tests
-------------

Tests are run using tox, environments configured are for python 2.7 and flake8. To run them, invoke ``tox`` from the command line. If you are using Docker, you can invoke it using:

.. code::

    $ docker exec -it emergencelab_web_1 tox

File Uploads
------------

File uploads use RQ in order to process files in the background. In order for uploaded files to be saved, an RQ worker on the queue ``default`` needs to be running. To start the worker, run

.. code::

    $ python manage.py rqworker default &

If you are using Docker, use the following command:

.. code::

    $ docker exec -it emergencelab_web_1 python manage.py rqworker default &
