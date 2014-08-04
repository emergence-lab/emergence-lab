Deployment
==========

Deploying code to the server is done via git, with some extra manual commands that have to be run. Code should only ever be deployed from the git ``master`` branch, which should always build and pass tests. Any feature development that will fail these conditions should be done in a branch and merged in via pull request on gitlab.

A git repository is already set up on the server with a remote that points to the correct location. The steps to deploy are as follows.

    #) Activate the root user to deploy::

        prod$ sudo -i
        prod$ cd /var/wsgi/

    #) Pull in the latest changes via git::

        prod$ git pull

    #) Add any new apps to the settings.py::

        prod$ gedit wbg/settings.py

    #) Migrate all apps::

        prod$ ./manage.py migrate APPNAME

    #) Make the html documentation::

        prod$ cd docs/
        prod$ make clean
        prod$ make html

    #) Restart apache2::

        prod$ service apache2 restart

    #) Exit root user::

        prod$ exit
