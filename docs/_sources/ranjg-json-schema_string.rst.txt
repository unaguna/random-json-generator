String Generation
=================
When ``string`` is adopted as :doc:`type <ranjg-json-schema_type>`, ``ranjg.gen`` returns string randomly.

>>> import ranjg
>>> schema = { 'type': 'string' }
>>> generated = ranjg.gen(schema)  # -> returns a string
>>> type(generated)
<class 'str'>

:note: With a few exceptions, alphanumeric characters are used in string generation.


Length
------
When generating a string, you can limit the length of the string by specifying ``minLength`` or ``maxLength``.

>>> import ranjg
>>> schema = {
>>>     'type': 'string',
>>>     'minLength': 8,
>>>     'maxLength': 12,
>>> }
>>> generated = ranjg.gen(schema)  # -> returns a string of 8 to 12 characters

If you want a string of a certain length, specify the same value for ``minLength`` and ``maxLength``.

:warning: If ``pattern`` is specified in the schema, both ``minLength`` and ``maxLength`` are ignored.

:warning: ``minLength`` cannot be a negative number as well as ``maxLength``.

:note:
    If ``minLength`` or ``maxLength`` is not specified, it will be completed by options.
    See also :doc:`ranjg-options_string`.


Regular Expression
------------------
By using the ``pattern`` keyword, you can generate a string that matches the regular expression.

>>> import ranjg
>>> schema = {
>>>     'type': 'string',
>>>     'pattern': r'\d\d\d',
>>> }
>>> generated = ranjg.gen(schema)
# -> returns a string consisting of three numeric characters

:note: Internally ``ranjg.gen`` use the `rstr`_ package for generating string.

:warning: The pattern can only be a string. Regular expression objects, etc. cannot be specified.

.. _rstr: https://pypi.org/project/rstr/