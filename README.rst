django-reciprocity
==================

.. image:: https://travis-ci.org/mpasternak/django-reciprocity.svg?branch=develop
   :target: https://travis-ci.org/mpasternak/django-reciprocity

To make a long story short, read description of `django-nginx-push-stream`_ . This is
a bit higher level, than `django-nginx-push-stream`_ - it is an implementation of an
interactive web UI in JavaScript (based on jQuery and Foundation 6) and Python (Django).
It sits on top of ``nginx-push-stream``.

.. _django-nginx-push-stream: http://github.com/mpasternak/django-nginx-push-stream

Running the demo
----------------

nginx and rabbitmq
~~~~~~~~~~~~~~~~~~

Run the nginx with http-push-stream module. You can run it locally (see `django-nginx-push-stream`_ docs),
you can run it using included image. In this repo's root dir:

.. code-block:: shell

    docker-compose up webserver rabbitmq

This will boot a container running nginx with HTTP-push-stream module and a RabbitMQ node.

This nginx server is a proxy to a service running on your local machine (it loops back to
``docker.host.internal`` port 8080). It listens by default on port 9080. If you ever need to
change this port, make sure to adjust variables ``NGINX_PUSH_STREAM_PUB_PORT`` and
``NGINX_PUSH_STREAM_SUB_PORT`` defined in ``test_project.settings``.

Celery container defined in that compose file listens by default on port 45672. If you want
to change it, please make sure to adjust variable ``CELERY_BROKER_URL`` in
``test_project.settings``.

There may be more containers defined in the ``docker-compose.yml`` file. They're utilized
for tests and may take more time to download, so that's why it is good to specify which
containers to start when running ``docker-compose``. 

Set-up test_project with requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the root directory of the repo, please:

.. code-block:: shell

    cd test_project
    yarn
    pip install -r requirements.txt
    export PYTHONPATH=..
    python manage.py migrate


celery
~~~~~~

It's time to launch our background worker, that will handle long-running tasks.

.. code-block:: shell

    celery worker -A test_project.celery -E -l INFO

Celery should say something about our transport being "amqp://guest:**@localhost:45672//". The port
should match the port used in docker-compose container.

Django
~~~~~~

Now, launch another terminal window and boot up your Django part of the deal.
It is IMPORTANT to run the sever listening on all interfaces of your host,
so Nginx from Docker image will be able to proxy requests to it:

.. code-block:: shell

    cd test_project
    export PYTHONPATH=..
    python manage.py runserver 0.0.0.0:8080

Testing
~~~~~~~

Go to http://localhost:9080/ to see your stack in action. Click the link,
as web page says, to launch long running task, as defined in ``test_app.tasks`` module. The
web page will pass its UUID to the long running task and in turn the task will be able
to notify the web page about its progress.

Where to go now?
~~~~~~~~~~~~~~~~

You can try the commands, described below in the "Command-line interface" section.


Command-line interface
----------------------

Different channels
~~~~~~~~~~~~~~~~~~

Send a message to all users:

.. code-block:: shell

  python manage.py publish_message -q __all__ -d '{"type": "callout", "header": "Nice optional title.", "body": "Just a message.", "class": "success"}'

Send a message to all authorised (logged-in) users:

.. code-block:: shell

  python manage.py publish_message -q __authorized__ -d '{"type": "callout", "header": "Nice optional title.", "body": "Just a message.", "class": "success"}'

Send a message to a specific session:

.. code-block:: shell

  python manage.py publish_message -q __session__SESSION-ID -d '{"type": "callout", "header": "Nice optional title.", "body": "Just a message.", "class": "success"}'

Send a message to a specific web page:

.. code-block:: shell

  python manage.py publish_message -q __uuid__WEB-PAGE-UUID4 -d '{"type": "callout", "header": "Nice optional title.", "body": "Just a message.", "class": "success"}'

Command-line interface
~~~~~~~~~~~~~~~~~~~~~~

Send a message (callout) to all web browsers:

.. code-block:: shell

  python manage.py publish_message -q __all__ -d '{"type": "callout", "header": "Nice optional title.", "body": "Just a message.", "class": "success"}'

Send a clickable message to all web browsers:

.. code-block:: shell

  python manage.py publish_message -q __all__ -d '{"type": "callout-with-link", "href": "http://www.onet.pl", "header": "", "body": "Processing has finished. Please click this link to access report. ", "class": "success"}'

Make all web browsers visit a different web page:

.. code-block:: shell

  python manage.py publish_message -q __all__ -d '{"type": "goto-page", "href": "http://www.onet.pl"}'

Show a modal dialog:

.. code-block:: shell

  python manage.py publish_message -q __all__ -d '{"type": "modal-dialog", "header": "http://www.onet.pl", "lead": "lead", "paragraph": "paragraphs"}'

Close a previously shown modal dialog:

.. code-block:: shell

  python manage.py publish_message -q __all__ -d '{"type":"close-modal-dialog"}'

Show a please-wait dialog:

.. code-block:: shell

  python manage.py publish_message -q __all__ -d '{"type": "please-wait-dialog", "header": "Please wait patiently...", "lead": "The server is working", "paragraph": "After the operation is complete, the page will refresh."}'


Close a please-wait dialog:

.. code-block:: shell

  python manage.py publish_message -q __all__ -d '{"type":"close-please-wait-dialog"}'


Replace HTML of a given jQuery selector:

.. code-block:: shell

  python manage.py publish_message -q __all__ -d '{"type": "html", "selector": "body", "value": "LOL"}'

Execute JavaScript via eval:

.. code-block:: shell

  python manage.py publish_message -q __all__ -d '{"type": "eval", "value": "console.log(123);"}'

