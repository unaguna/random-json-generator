Enum
====
``enum`` keyword prescribes the candidates of value to generate.

For example:

>>> import ranjg
>>> schema = {
>>>     'enum': [1, 'a'],
>>> }
>>> generated = ranjg.gen(schema)  # -> returns a random value
>>> assert generated == 1 or generated == 'a'


Filtering candidates by other keywords
--------------------------------------
Not every element in ``schema.enum`` is a candidate.
If keywords is set other than ``enum``, elements that violate them will be excluded from the candidate list.

:warning:
    One of the features of the ``jsonschema`` package is used to determine if a candidate satisfies the schema.
    That is, the genuine JSON schema is used for this determination, not ranjg-JSON-schema.

    It is unstable because it does not particularly specify which draft will be used.
    Whenever possible, try not to specify other keywords when specifying ``enum``.
