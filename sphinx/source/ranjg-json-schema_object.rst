Object Generation
=================
When ``object`` is adopted as :doc:`type <ranjg-json-schema_type>`, ``ranjg.gen`` returns a dict randomly.

>>> import ranjg
>>> schema = { 'type': 'object' }
>>> generated = ranjg.gen(schema)  # -> returns a dict
>>> type(generated)
<class 'dict'>


Properties
----------
By specifying ``properties``, you can control each property of the generated dict. ``properties`` is a dictionary whose keys are strings and whose values are schemas. If a property name in the generated dict matches a key, the property satisfies the schema corresponding to the key.

>>> import ranjg
>>> schema = {
...     'type': 'object',
...     'properties': {
...         'pro1': { 'type': 'string' },
...         'pro2': { 'type': 'number' },
...     },
... }
>>> generated = ranjg.gen(schema)  # -> returns a dict
>>> if 'pro1' in generated:
...     assert isinstance(generated['pro1'], str)
>>> if 'pro2' in generated:
...     assert isinstance(generated['pro2'], float)

:note:
    If ``options.priority_schema_of_properties`` is specified and the generated property is included in the option,
    the option ``options.priority_schema_of_properties[key]`` takes precedence over ``schema.properties[key]``.
    See also :doc:`ranjg-options_object`.

:note:
    Even if a key is specified in ``properties``, it does not necessarily mean that the generated dict will contain
    that key. The keys that must be included in the generated dict are specified with the ``required`` keyword.

    If the key is in ``properties`` but not in ``required``, the generated dict has the key with probability
    ``options.default_prob_of_optional_properties``. See also :doc:`ranjg-options_object`.


Required Properties
-------------------
If ``required`` is a list of strings, those strings will always be included as keys in the generated dict.

>>> import ranjg
>>> schema = {
...     'type': 'object',
...     'required': ['pro1', 'pro2'],
... }
>>> generated = ranjg.gen(schema)  # -> returns a dict
>>> assert 'pro1' in generated
>>> assert 'pro2' in generated

:note: The ``required`` keyword specifies only the presence of a key. If you want to specify the contents of a property, use the ``properties`` keyword as well.
