.. random-json-generator documentation master file, created by
   sphinx-quickstart on Mon Nov 23 15:14:40 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

random-json-generator
=====================

random-json-generator (ranjg) is a python package providing functions to generate random JSON data according to
JSON-Schema-**LIKE** object. (It is similar to JSON schema, but does NOT support some keywords.
Also see :doc:`ranjg-json-schema`.)

For example:

>>> import ranjg
>>> schema = { 'type': 'string' }
>>> ranjg.gen(schema)  # <- returns a string value
>>> schema = { 'type': 'number', "minimum": 0 }
>>> ranjg.gen(schema)  # <- returns a non-negative float value

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   quick-start-code
   quick-start-command
   ranjg
   ranjg-json-schema
   ranjg-options




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
