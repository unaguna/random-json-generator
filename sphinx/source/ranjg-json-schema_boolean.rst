Boolean Generation
==================
When ``boolean`` is adopted as :doc:`type <ranjg-json-schema_type>`, ``ranjg.gen`` returns ``True`` or ``False`` randomly. Then the other keywords are ignored.

>>> import ranjg
>>> schema = { 'type': 'boolean' }
>>> generated = ranjg.gen(schema)  # -> returns True or False
>>> type(generated)
<class 'bool'>


:note:
    It returns True with a probability of ``options.default_prob_of_true_given_bool`` and False with the remaining probability. See also :doc:`ranjg-options_boolean`.
