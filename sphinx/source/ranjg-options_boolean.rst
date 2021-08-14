Options for Boolean Generation
==============================
When generating a boolean value, some options will be used.

Probability
-----------
If ``ranjg.gen`` generates a boolean value, it returns True with probability ``options.default_prob_of_true_given_bool``
and False with probability 1-``default_prob_of_true_given_bool``.

>>> import ranjg
>>> from ranjg.options import Options
>>> schema = {'type': 'boolean'}
>>> options = Options(default_prob_of_true_given_bool=1.0)  # 1.0 = 100%
>>> generated = ranjg.gen(schema, options=options)  # -> returns True with probability 100%
>>> assert generated is True


:note:
    The default value of ``default_prob_of_true_given_bool`` is 0.5.
