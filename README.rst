django-reciprocity
==================

To make a long story short, read description of `django-nginx-push-stream`_ . This is
a bit higher level, than `django-nginx-push-stream`_ - it is an implementation of an
interactive web UI in JavaScript (based on jQuery and Foundation 6) and Python (Django).
It sits on top of ``nginx-push-stream``.

.. _django-nginx-push-stream: http://github.com/mpasternak/django-nginx-push-stream

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

