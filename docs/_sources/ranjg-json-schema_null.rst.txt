Null Generation
===============
When ``null`` is adopted as :doc:`type <ranjg-json-schema_type>`, ``ranjg.gen`` returns ``None``. Then the other keywords are ignored.

>>> import ranjg
>>> schema = { 'type': 'null' }
>>> generated = ranjg.gen(schema)  # -> returns None
>>> type(generated)
<class 'NoneType'>


Multiple type with null
-----------------------

Type ``null`` is especially useful when used in multiple type.

For non-required items, if you want to express the absence of a value as null, you can write the following:

>>> import ranjg
>>> schema = {
...     'type': 'object',
...     # ↓ age is required. So a result dict has always key ``age``.
...     'required': ['name', 'age'],
...     'properties': {
...         'name': { 'type': 'string', 'minLength': 1 },
...         # ↓ The value of age can be an non-negative integer or None.
...         'age': { 'type': ['integer', 'null'], 'minimum': 0 },
...     }
... }
>>> generated = ranjg.gen(schema)
>>> # Examples of ``generated``
>>> #     { 'name': 'Abc', 'age': 3 }
>>> #     { 'name': 'Exp', 'age': None }
