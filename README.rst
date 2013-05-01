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

TestSession
~~~~~~~~~~~

In ``requests`` 1.2 and older, the order of mounted adapters is unpredictable.
To make sure you can mount arbitrary paths with their own respective adapters,
use ``TestSession`` which always matches the longest prefix::

  >>> from requests_testadapter import TestAdapter, TestSession
  >>> s = TestSession()
  >>> s.mount('http://git', TestAdapter(b'git'))
  >>> s.mount('http://github', TestAdapter(b'github'))
  >>> s.mount('http://github.com', TestAdapter(b'github.com'))
  >>> s.mount('http://github.com/about/', TestAdapter(b'github.com/about'))
  >>> r = s.get('http://github.com/about/')
  >>> r.text
  u'github.com/about'
  >>> r = s.get('http://github.com')
  >>> r.text
  u'github.com'
  >>> r = s.get('http://gittip.com')
  >>> r.text
  u'git'

``TestSession`` doesn't connect the default handlers for HTTP and HTTPS so you
will be notified if your requests unintentionally try to reach external
websites in your unit tests::

  >>> r = s.get('http://bitbucket.org')
  Traceback (most recent call last):
  ...
  requests.exceptions.InvalidSchema: No connection adapters were found for
  'http://bitbucket.org/'

How do I run the tests?
-----------------------

The easiest way would be to extract the source tarball and run::

  $ python test/test_testadapter.py

If you have all compatible Python implementations available on your system, you
can run tests on all of them by using tox::

  $ pip install tox
  $ tox
  GLOB sdist-make: setup.py
  py26 inst-nodeps: .tox/dist/requests-testadapter-0.1.0.zip
  py26 runtests: commands[0]
  ..
  ----------------------------------------------------------------------
  Ran 2 tests in 0.014s

  OK
  py27 inst-nodeps: .tox/dist/requests-testadapter-0.1.0.zip
  py27 runtests: commands[0]
  ..
  ----------------------------------------------------------------------
  Ran 2 tests in 0.014s

  OK
  py32 inst-nodeps: .tox/dist/requests-testadapter-0.1.0.zip
  py32 runtests: commands[0]
  ..
  ----------------------------------------------------------------------
  Ran 2 tests in 0.024s

  OK
  py33 inst-nodeps: .tox/dist/requests-testadapter-0.1.0.zip
  py33 runtests: commands[0]
  ..
  ----------------------------------------------------------------------
  Ran 2 tests in 0.017s

  OK
  _______________________________ summary ______________________________
    py26: commands succeeded
    py27: commands succeeded
    py32: commands succeeded
    py33: commands succeeded
    congratulations :)

Change Log
----------

0.2.0
~~~~~

* introduced ``TestSession`` to make adapter order predictable in ``requests``
  1.2 and older

0.1.0
~~~~~

* initial published version

Authors
-------

Glued together by `Łukasz Langa <mailto:lukasz@langa.pl>`_.
