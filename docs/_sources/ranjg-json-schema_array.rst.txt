Array Generation
================
When ``array`` is adopted as :doc:`type <ranjg-json-schema_type>`, ``ranjg.gen`` returns a list randomly.

>>> import ranjg
>>> schema = { 'type': 'array' }
>>> generated = ranjg.gen(schema)  # -> returns a list
>>> type(generated)
<class 'list'>


Length
------
When generating a list, you can limit the length of the list by specifying ``minItems`` or ``maxItems``.

>>> import ranjg
>>> schema = {
...     'type': 'array',
...     'minItems': 2,
...     'maxItems': 4,
... }
>>> generated = ranjg.gen(schema)  # -> returns a list
>>> assert len(generated) >= 2
>>> assert len(generated) <= 4


Items
-----
The keyword ``items`` can be a schema or an list of schemas, each of which specifies the elements of the generated array.

To All Elements
^^^^^^^^^^^^^^^

If ``items`` is a dict (it must be schema), each of element of the generated list satisfies the schema.

>>> import ranjg
>>> schema = {
...     'type': 'array',
...     'items': {
...         'type': 'string'
...     }
... }
>>> generated = ranjg.gen(schema)  # -> returns a list
>>> for element in generated:
...     assert isinstance(element, str)

To Each Element
^^^^^^^^^^^^^^^

On the other hand, if ``items`` is a list (its elements must be schema), each element of the generated list
satisfies the corresponding schema in the list.

>>> import ranjg
>>> schema = {
...     'type': 'array',
...     'items': [
...         { 'type': 'string' },
...         { 'type': 'boolean' },
...         { 'type': 'array' },
...     ]
... }
>>> generated = ranjg.gen(schema)  # -> returns a list
>>> if len(generated) >= 1:
...     assert isinstance(generated[0], str)
>>> if len(generated) >= 2:
...     assert isinstance(generated[1], bool)
>>> if len(generated) >= 3:
...     assert isinstance(generated[2], list)

:note: Even if ``items`` is a list of length 3, the length of the generated list is not necessarily 3, but may be longer or shorter than that.
    (However, if ``additionalItems`` is set to ``False`` as described below, the number of elements in the generated list will not exceed the number of elements in ``items``.)
    The length of the generated list can be specified with the keywords ``minItems`` and ``maxItems``.

If ``items`` is a list, it isn't limit overflowing elements. For example, if the length of ``items`` is 3, nothing is specified for the 4th and subsequent elements of the generated list.

>>> import ranjg
>>> schema = {
...     'type': 'array',
...     'items': [
...         { 'type': 'string' },
...         { 'type': 'boolean' },
...         { 'type': 'array' },
...     ]
... }
>>> generated = ranjg.gen(schema)  # -> returns a list
>>> # generated[3] was freely generated (if it exists).

You can avoid this by specifying a schema for ``additionalItems``. If ``additionalItems`` is a schema, the schema will be specified for elements that exceed the number of items elements.

>>> import ranjg
>>> schema = {
...     'type': 'array',
...     'items': [
...         { 'type': 'string' },
...         { 'type': 'boolean' },
...         { 'type': 'array' },
...     ],
...     'additionalItems': { 'type': 'integer' },
... }
>>> generated = ranjg.gen(schema)  # -> returns a list
>>> if len(generated) >= 1:
...     assert isinstance(generated[0], str)
>>> if len(generated) >= 2:
...     assert isinstance(generated[1], bool)
>>> if len(generated) >= 3:
...     assert isinstance(generated[2], list)
>>> for i in range(3, len(generated)):
...     assert isinstance(generated[i], int)

If you don't want to allow additional elements that are not specified in ``items``, set ``False`` to ``additionalItems``.

>>> import ranjg
>>> schema = {
...     'type': 'array',
...     'items': [
...         { 'type': 'string' },
...         { 'type': 'boolean' },
...         { 'type': 'array' },
...     ],
...     'additionalItems': False,
... }
>>> generated = ranjg.gen(schema)  # -> returns a list
>>> assert len(generated) <= len(schema['items'])


