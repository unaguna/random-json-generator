Type
====
``type`` keyword prescribes the type of value to generate.

For example:

>>> import ranjg
>>> schema = {
>>>     'type': 'string',
>>> }
>>> generated = ranjg.gen(schema)  # -> returns random string
>>> type(generated)
<class 'str'>


Values available for the type
-----------------------------

You can use following values.

=============================== =======================
value of ``type``               type of generated value
=============================== =======================
``'null'``                      ``None``
``'boolean'``                   ``bool``
``'integer'``                   ``int``
``'number'``                    ``float``
``'string'``                    ``str``
``'array'``                     ``list``
``'object'``                    ``dict``
a list with the above strings   Along one of the strings in the list.
(unset)                         Determined on its own (not necessarily random)
=============================== =======================

:note: In the regular JSON schema, ``"type": "number"`` also allows for integer values such as ``1``, but ranjg always generates a float value.

.. _multiple-type-specification:

Multiple Type Specification
---------------------------

``type`` can be specified not only as a string, but also as a list of strings. In this case, one of them is adopted to generate the value. For example:

>>> import ranjg
>>> schema = {
>>>     'type': ['string', 'number'],
>>>     'maximum': 1.0,
>>>     'minLength': 2,
>>> }
>>> generated = ranjg.gen(schema)  # -> returns random string or float value

In above case, the type of ``generated`` is ``str`` or ``float``.
If ``string`` is adopted, ``maximum`` is ignored because it is a parameter for numbers, and ``minLength`` is ignored if ``number`` is used, because it is a parameter for strings.

:warning: It is not allowed to specify an empty list as ``type``.