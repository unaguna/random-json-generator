Options for Enum Generation
===========================
When generating with ``schema.enum``, some options will be used.

Copy Candidates
---------------
If ``schema.enum`` contains a mutable object such as list, the question is whether to copy it or not.
``options.enum_copy_style`` can be used to specify whether or not to copy.

If ``enum_copy_style`` is NO_COPY, the returned value is same instance to one of candidate.
For example:

>>> import ranjg
>>> from ranjg import options
>>> from ranjg.options import Options
>>> schema = {'enum': [[1, 2]]}    # only one candidate: [1, 2]
>>> generated = ranjg.gen(schema, options=Options(enum_copy_style=options.NO_COPY))
>>> assert generated == [1, 2]
>>>
>>> # Rewrite schema indirectly using the fact that it is NO_COPY.
>>> generated.append(3)
>>> assert schema['enum'][0] == [1, 2, 3]

If ``enum_copy_style`` is SHALLOW_COPY or DEEP_COPY, the returned value is copy of one of candidate.
For example:

>>> import ranjg
>>> from ranjg import options
>>> from ranjg.options import Options
>>> schema = {'enum': [[1, 2]]}    # only one candidate: [1, 2]
>>> generated = ranjg.gen(schema, options=Options(enum_copy_style=options.DEEP_COPY))
>>> assert generated == [1, 2]
>>>
>>> # Since generated is a copy, editing it will not affect the schema.
>>> generated.append(3)
>>> assert schema['enum'][0] == [1, 2]

:note:
    To copy, it uses package `copy`_.
    The respective behavior of shallow copy and deep copy is also the same as ``copy.copy()`` and ``copy.deepcopy()``.

.. _copy: https://docs.python.org/ja/3/library/copy.html
