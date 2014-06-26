WGB Django
==========

Migrations
----------
Migrations are tracked with git. Make any changes to models on the development db and later make the changes to production.

Workflow for adding apps to database:
    1. Make sure the database is synced::

        dev$ ./manage.py syncdb

    2. Create app and add models::

        dev$ ./manage.py startapp APPNAME
        dev$ gedit APPNAME/models.py

    3. Add to installed apps in settings.py
    4. Add app to south tracking::

        dev$ ./manage.py convert_to_south APPNAME

    5. Migrate app with south to add table to database::

        dev$ ./manage.py migrate APPNAME

    6. Add migrations to version control::

        dev$ git add APPNAME

    7. Push changes to gitlab::

        dev$ git push

    8. Pull in changes on production server::

        prod$ sudo -i
        prod$ cd /var/wsgi/
        prod$ git pull

    9. Migrate app to make changes to database::

        prod$ ./manage.py migrate APPNAME

    10. Your production environment is now in sync

Workflow for editing models:
    1. Make sure the database is synced::

        dev$ ./manage.py syncdb

    2. Make changes to models::

        dev$ gedit APPNAME/models.py

    3. Create migration and migrate app::

        dev$ ./manage.py schemamigration APPNAME --auto
        dev$ ./manage.py migrate APPNAME

    4. Add migrations to version control and push::

        dev$ git add APPNAME/models.py
        dev$ git add APPNAME/migrations
        dev$ git push

    5. Pull in changes on production server::

        prod$ git pull

    6. Migrate app to make changes to database::

        prod$ ./manage.py migrate APPNAME

    7. Your production environment is now in sync
