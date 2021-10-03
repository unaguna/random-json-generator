Options
=======
**ranjg** uses options during generation and you can specify some options.
For example:

>>> schema = {
>>>     'type': 'object',
>>>     'required': ['sent_flg'],  # generated must contains 'sent_flg'
>>>     'properties': {
>>>         'sent_flg': {'type': 'boolean'},  # generated[sent_flg] is boolean value
>>>     }
>>> }
>>> options = Options(default_prob_of_true_given_bool=0.2)  # 0.2 = 20%
>>> generated = ranjg.gen(schema, options=options)
>>> assert isinstance(generated['sent_flg'], bool)  # -> it's True with probability 20% or False with probability 80%

Options also apply to the generation of descendant elements, as described above, and allow you to specify
generation rules that are not specified in the schema.


The following pages show keywords of Options.

.. toctree::
   :maxdepth: 2
   :caption: References:

   ranjg-options_enum
   ranjg-options_string
   ranjg-options_boolean
   ranjg-options_array
   ranjg-options_object


Options file
------------

You can also use ``ranjg.gen`` with a file containing the options.
For example:

>>> schema = { 'type': 'boolean' }
>>> ranjg.gen(schema, options_file='./options.json')  # -> returns True or False

with options file ./options.json:

.. code-block:: json

    {
      "default_prob_of_true_given_bool": 0.2
    }

In addition, you can also specify options in command line execution.
For example:

.. code-block:: shell

    $ python -m ranjg ./schema.json --options ./options.json
