=============
Emergence Lab
=============

Web-based application written in Django with the following goals:

    #) Improve tracking of experimental samples and data, both process and characteriztion data
    #) Allow data-driven experimentation by allowing programmable access to data via an embedded iPython notebook
    #) Have a clean, consistent user interface to encourage best-practices for use

Development Setup
=================

To get started for development install dependencies with pip install -r requirements/development.txt. Create a ``secrets.json`` file with database and ldap information. To run the tests, run ``tox`` in the command line to run tests and flake8. To only run tests, use ``tox -e py27``.
