Quick Start (Python Code)
=========================
Module ``ranjg`` can be used in python code.

If you haven't installed ranjg yet, install it with the following command:

.. code-block:: shell

    $ pip install ranjg

Then, you can generate values according to :doc:`ranjg-json-schema` with following code.

>>> import ranjg
>>> schema = {
...     'type': 'object',
...     'required': ['name'],
...     'properties': {
...         'name': { 'type': 'string', 'minLength': 1 },
...         'age': { 'type': 'integer', 'minimum': 0 },
...     }
... }
>>> generated = ranjg.gen(schema)

The ``schema`` specified in the above example is according to :doc:`ranjg-json-schema`.
Then ``generated`` satisfies the schema.
