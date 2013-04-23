====================
requests-testadapter
====================

.. image:: https://secure.travis-ci.org/ambv/requests-testadapter.png
  :target: https://secure.travis-ci.org/ambv/requests-testadapter

Currently a very basic module that provides an adapter for `requests
<http://pypi.python.org/pypi/requests>`_ that mocks network activity for unit
test purposes.

How to use
----------

This code assumes your HTTP client is written in a way that enables passing
a custom `Session
<http://www.python-requests.org/en/latest/user/advanced/#session-objects>`_
object. When that's the case, all you have to do is to mount the adapter to
answer for a specific prefix::

  >>> import requests
  >>> from requests_testadapter import TestAdapter
  >>> s = requests.Session()
  >>> s.mount('http://', TestAdapter(b'Mock!', status=404))
  >>> r = s.get('http://mocked.com')
  >>> r.status_code
  404
  >>> r.text
  'Mock!'

You can also specify a ``headers`` dictionary as a keyword argument to
``TestAdapter``.

How do I run the tests?
-----------------------

The easiest way would be to extract the source tarball and run::

  $ python test/test_testadapter.py

Change Log
----------

0.1.0
~~~~~

* initial published version

Authors
-------

Glued together by `Łukasz Langa <mailto:lukasz@langa.pl>`_.
