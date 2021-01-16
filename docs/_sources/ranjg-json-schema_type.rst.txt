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

=============================== ============================================== ===================================
value of ``type``               type of generated value                        detailed usage
=============================== ============================================== ===================================
``'null'``                      ``None``                                       :doc:`Here <ranjg-json-schema_null>`
``'boolean'``                   ``bool``                                       :doc:`Here <ranjg-json-schema_boolean>`
``'integer'``                   ``int``                                        :doc:`Here <ranjg-json-schema_number>`
``'number'``                    ``float``                                      :doc:`Here <ranjg-json-schema_number>`
``'string'``                    ``str``                                        :doc:`Here <ranjg-json-schema_string>`
``'array'``                     ``list``                                       :doc:`Here <ranjg-json-schema_array>`
``'object'``                    ``dict``                                       :doc:`Here <ranjg-json-schema_object>`
a list with the above strings   Along one of the strings in the list.          :ref:`below <Multiple-Type-Specification>`
(unset)                         Determined on its own (not necessarily random)
=============================== ============================================== ===================================

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