Options for String Generation
=============================
When generating a string, some options will be used.

Length Range
------------
If **only one** of ``schema.minLength`` and ``schema.maxLength`` is specified,
the other is determined so that ``schema.maxLength`` - ``schema.minLength`` is equal to
``options.default_length_range_of_genstr``.

>>> import ranjg
>>> schema = {
>>>     'type': 'string',
>>>     'minLength': 8
>>> }
>>> options = Options(default_length_range_of_genstr=1)
>>> generated = ranjg.gen(schema)  # -> returns a string of 8 to 8+1 characters
>>> assert len(generated) in (8, 9)

>>> import ranjg
>>> schema = {
>>>     'type': 'string',
>>>     'maxLength': 8
>>> }
>>> options = Options(default_length_range_of_genstr=1)
>>> generated = ranjg.gen(schema)  # -> returns a string of 8-1 to 8 characters
>>> assert len(generated) in (7, 8)


:note:
    When ``schema.minLength`` is not specified and ``schema.maxLength`` - ``options.default_length_range_of_genstr``
    is negative, the result string is length of between 0 and ``schema.maxLength``.
    In other words, ``ranjg.gen`` doesN'T raise error even if ``schema.maxLength`` -
    ``options.default_length_range_of_genstr`` is negative.

:warning:
    If ``schema.pattern`` is specified, this options are ignored, as well as ``schema.minLength`` and
    ``schema.maxLength``. See also :doc:`ranjg-json-schema_string`.


Default minLength and maxLength
-------------------------------
If **neither** ``schema.minLength`` nor ``schema.maxLength`` is specified,
they are determined with ``options.default_min_length_of_string`` and ``options.default_max_length_of_string``.

>>> import ranjg
>>> schema = { 'type': 'string' }
>>> options = Options(default_min_length_of_string=1, default_max_length_of_string=3)
>>> generated = ranjg.gen(schema)  # -> returns a string of 1 to 3 characters
>>> assert len(generated) in (1, 2, 3)

:warning:
    If you specify one of ``options.default_min_length_of_string`` and ``options.default_max_length_of_string``,
    also specify the other.

    If not explicitly specified, the default value will be used, but if min is greater than max,
    ``ranjg.gen`` will raise an exception.

:warning:
    If ``schema.pattern`` is specified, these options are ignored, as well as ``schema.minLength`` and
    ``schema.maxLength``. See also :doc:`ranjg-json-schema_string`.