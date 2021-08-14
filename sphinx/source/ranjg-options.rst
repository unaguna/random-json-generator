Options
=======
**ranjg** uses options during generation and you can specify some options.
For example:

>>> schema = { 'type': 'boolean' }
>>> options = Options(default_prob_of_true_given_bool=0.2)  # 0.2 = 20%
>>> ranjg.gen(schema, options=options)  # -> returns True with probability 20% or False with probability 80%

You can also generate it with a file containing the options.
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


The following pages show keywords of Options.

.. toctree::
   :maxdepth: 2
   :caption: References:

   ranjg-options_string
   ranjg-options_boolean
   ranjg-options_array

.. _JSON schema: https://json-schema.org/
