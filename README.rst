=============
Emergence Lab
=============

.. image:: https://travis-ci.org/wbg-optronix-lab/emergence-lab.svg?branch=master
    :target: https://travis-ci.org/wbg-optronix-lab/emergence-lab

.. image:: https://coveralls.io/repos/wbg-optronix-lab/emergence-lab/badge.svg
    :target: https://coveralls.io/r/wbg-optronix-lab/emergence-lab

Web-based application written in Django with the following goals:

    #) Improve tracking of experimental samples and data, both process and characteriztion data
    #) Allow data-driven experimentation by allowing programmable access to data via an embedded iPython notebook
    #) Have a clean, consistent user interface to encourage best-practices for use

Development Setup
=================

Install Dependencies
--------------------

    $ pip install -r requirements/development.txt
    $ bower install

Configure Application
---------------------

Copy the template secrets file and edit with database and ldap configuration.

    $ cp wbg/secrets.template.json wbg/secrets.json
    $ vim wbg/secrets.json

Running Tests
-------------

Tests are run using tox, environments configured are for python 2.7 and flake8. To run them, invoke tox from the command line.

    $ tox
