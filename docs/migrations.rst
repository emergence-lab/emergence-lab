Migrations
==========

Migrations are tracked with git. Make any changes to models on the development db and later make the changes to production.

Workflow for adding apps to database:
-------------------------------------

    #) Make sure the database is synced and git is up to date::

        dev$ git pull
        dev$ ./manage.py syncdb

    #) Create app and add models::

        dev$ ./manage.py startapp APPNAME
        dev$ gedit APPNAME/models.py

    #) Add to installed apps in settings.py::

        dev$ gedit wbg/settings.py

    #) Create initital migrations::

        dev$ ./manage.py makemigrations APPNAME

    #) Migrate app to add table to database::

        dev$ ./manage.py migrate APPNAME

    #) Add app and migrations to version control::

        dev$ git add APPNAME

    #) Push changes to gitlab (assuming master branch)::

        dev$ git push origin master

    #) Pull in changes on production server::

        prod$ sudo -i
        prod$ cd /var/wsgi/
        prod$ git pull

    #) Migrate app to make changes to database::

        prod$ ./manage.py migrate APPNAME

    #) Your production environment is now in sync

Workflow for editing models:
----------------------------

    #) Make sure the database is synced and git is up to date::

        dev$ git pull
        dev$ ./manage.py migrate

    #) Make changes to models::

        dev$ gedit APPNAME/models.py

    #) Create migration and migrate app::

        dev$ ./manage.py makemigrations APPNAME
        dev$ ./manage.py migrate APPNAME

    #) Add migrations to version control and push (assuming master branch)::

        dev$ git add APPNAME/models.py
        dev$ git add APPNAME/migrations
        dev$ git push origin master

    #) Pull in changes on production server::

        prod$ sudo -i
        prod$ cd /var/wsgi/
        prod$ git pull

    #) Migrate app to make changes to database::

        prod$ ./manage.py migrate APPNAME

    #) Your production environment is now in sync
