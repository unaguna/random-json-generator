Options for Object Generation
=============================
When generating an object, some options will be used.

Schema of Properties
--------------------
When generating each property, the following steps will determine the schema to be used.

#. If ``options.priority_schema_of_properties`` contains the key, the corresponding value will be used as the schema.
#. If ``schema.properties`` contains the key, the corresponding value will be used as the schema.
#. ``options.default_schema_of_properties`` will be used as the schema.

The following is an explanation in order.

Priority Schema of Each Property
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If ``options.priority_schema_of_properties`` contains the key, the corresponding value will be used as the schema,
and ``schema.properties`` will be ignored.

>>> import ranjg
>>> from ranjg.options import Options
>>> schema = {
>>>     'type': 'object',
>>>     'required': ['id', 'code'],
>>>     'properties': {
>>>         'id': {'type': 'integer'},
>>>         'code': {'type': ['string', 'null']},  # type contains 'null'
>>>     }
>>> }
>>> priority_schema_of_properties = {
>>>     'code': {'type': 'string', 'pattern': r'OBJ\d\d\d'}  # type doesn't contain 'null'
>>> }
>>> options = Options(priority_schema_of_properties=priority_schema_of_properties)
>>> generated = ranjg.gen(schema, options=options)
>>> assert isinstance(generated['code'], str)   # str beginning with 'OBJ', cannot be null

schema.properties
^^^^^^^^^^^^^^^^^
With the exceptions mentioned above, ``schema.properties`` is used.
See also :doc:`ranjg-json-schema_object`.

Default Schema
^^^^^^^^^^^^^^
If the schema used cannot be determined according to the above, ``options.default_schema_of_properties`` will be used
instead.

>>> import ranjg
>>> from ranjg.options import Options
>>> schema = {
>>>     'type': 'object',
>>>     # property 'code' is required
>>>     'required': ['id', 'code'],
>>>     'properties': {
>>>         'id': {'type': 'integer'},
>>>         # schema of 'code' is not specified
>>>     }
>>> }
>>> default_schema = {'type': 'integer', 'minimum': 0, 'maximum': 0}
>>> options = Options(default_schema_of_properties=default_schema)
>>> generated = ranjg.gen(schema, options=options)
>>> assert 'code' in generated  # because property 'code' is required
>>> assert generated['code'] == 0  # default_schema_of_properties is used because schema.properties doesn't have 'code'


Probability of Non-Required Properties
--------------------------------------
When generating a dict, properties in ``schema.required`` are always generated, but properties in ``schema.properties``
and not in ``schema.required`` are also generated with probability ``options.default_prob_of_optional_properties``.
For example:

>>> import ranjg
>>> from ranjg.options import Options
>>> schema = {
>>>     'type': 'object',
>>>     # 'age' is not required
>>>     'required': ['id'],
>>>     'properties': {
>>>         'id': {'type': 'integer'},
>>>         'age': {'type': 'integer', 'minimum': 0},
>>>     }
>>> }
>>> options = Options(default_prob_of_optional_properties=1.0)  # 1.0 = 100%
>>> generated = ranjg.gen(schema, options=options)
>>> assert 'age' in generated  # generated contains 'age' with probability 100%