Options for Array Generation
============================
When generating an array, some options will be used.

Default Schema of Items
-----------------------
If items' schema is not specified in the schema, ``options.default_schema_of_items`` will be used instead.
For example:

>>> import ranjg
>>> from ranjg.options import Options
>>> schema = {
>>>     'type': 'array',
>>>     # length of result array is at least 3
>>>     'minItems': 3,
>>>     # schema of [2] is not specified
>>>     'items': [
>>>         {'type': 'boolean'},
>>>         {'type': 'string'},
>>>     ]
>>> }
>>> default_schema = {'type': 'integer', 'minimum': 10, 'maximum': 10}  # the integer between 10 and 10
>>> options = Options(default_schema_of_items=default_schema)
>>> generated = ranjg.gen(schema, options=options)
>>> assert generated[2] == 10  # the integer between 10 and 10

>>> import ranjg
>>> from ranjg.options import Options
>>> schema = {
>>>     'type': 'array',
>>>     # length of result array is at least 1
>>>     'minItems': 1,
>>>     # schema of elements is not specified
>>> }
>>> default_schema = {'type': 'integer', 'minimum': 10, 'maximum': 10}  # the integer between 10 and 10
>>> options = Options(default_schema_of_items=default_schema)
>>> generated = ranjg.gen(schema, options=options)
>>> assert generated[0] == 10  # the integer between 10 and 10
