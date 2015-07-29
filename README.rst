=============
Emergence Lab
=============

.. image:: https://travis-ci.org/wbg-optronix-lab/emergence-lab.svg?branch=master
    :target: https://travis-ci.org/wbg-optronix-lab/emergence-lab
    :alt: Test Status

.. image:: https://coveralls.io/repos/wbg-optronix-lab/emergence-lab/badge.svg
    :target: https://coveralls.io/r/wbg-optronix-lab/emergence-lab
    :alt: Code Coverage

.. image:: https://landscape.io/github/wbg-optronix-lab/emergence-lab/master/landscape.svg?style=flat
    :target: https://landscape.io/github/wbg-optronix-lab/emergence-lab/master
    :alt: Code Health

Web-based application written in Django with the following goals:

#) Improve tracking and discoverability of experimental samples and data, both process and characterization data
#) Allow data-driven experimentation by allowing programmable access to data via an embedded iPython notebook
#) Provide project management functionality to help organize experiments and samples
#) Have a clean, consistent user interface to encourage best-practices for use

Development Setup
=================

Install Dependencies
--------------------

.. code::

    $ pip install -r requirements/development.txt
    $ bower install

Configure Application
---------------------

Copy the template secrets file and edit with database and ldap configuration.

.. code::

    $ cp wbg/secrets.template.json wbg/secrets.json
    $ vim wbg/secrets.json

Running Tests
-------------

Tests are run using tox, environments configured are for python 2.7 and flake8. To run them, invoke tox from the command line.

.. code::

    $ tox
