Number Generation
=================
When ``number`` or ``integer`` is adopted as :doc:`type <ranjg-json-schema_type>`, ``ranjg.gen`` returns a numerical value.

>>> import ranjg
>>> schema = { 'type': 'number' }
>>> generated = ranjg.gen(schema)  # -> returns a float number
>>> type(generated)
<class 'float'>

>>> import ranjg
>>> schema = { 'type': 'integer' }
>>> generated = ranjg.gen(schema)  # -> returns an integer
>>> type(generated)
<class 'int'>

:note: If ``type`` is ``'number'``, the type of the result is always ``float``, but it can also be an integer, as in ``1.0``.

:note: If you want to randomly determine whether the type is ``int`` or ``float``, you can use ``'type':['integer','number']`` to do so. (see :ref:`multiple-type-specification`)


Range
-----

Ranges of numbers are specified using a combination of the ``minimum`` and ``maximum`` keywords, (or ``exclusiveMinimum`` and ``exclusiveMaximum`` for expressing exclusive range).

Generated value *x* satisfies the following:

.. code-block::

    x ≧ minimum
    x ≦ maximum
    x ＞ exclusiveMinimum
    x ＜ exclusiveMaximum

:warning: For now, if ``exclusiveMinimum`` is set to true, the number *x* generated will satisfy *x* ＜ ``minimum``, but this will be deprecated in the future. Similarly for ``exclusiveMaximum``.

For example:

>>> import ranjg
>>> schema = {
>>>     'type': 'number',
>>>     'minimum': 0,
>>> }
>>> generated = ranjg.gen(schema)
>>> 0 <= generated
True

>>> import ranjg
>>> schema = {
>>>     'type': 'integer',
>>>     'exclusiveMinimum': 74,
>>>     'maximum': 77,
>>> }
>>> generated = ranjg.gen(schema)
>>> generated in (75, 76, 77)
True

