ranjg-JSON-schema
=================
**ranjg** is a module to generate random string, JSON object, and so on.
The generated values will conform to a schema dictionary specified as argument.
For example:

>>> schema = {
>>>     'type': 'number',
>>>     'minimum': 0,
>>> }
>>> ranjg.gen(schema)  # -> returns a non-negative float value

But schema used in ranjg does not strictly conform to the `JSON schema`_.

The schema used in ranjg is called *ranjg-JSON-schema*, which adopts parts of the JSON schema draft 4 and draft 7.
In the future, we will increase corresponding keywords and may even adopt our own keywords.

:warning: In the future, partial support for draft 4 will be removed.

The following pages show keywords of ranjg-JSON-schema.

.. toctree::
   :maxdepth: 2
   :caption: References:

   ranjg-json-schema_enum
   ranjg-json-schema_type
   ranjg-json-schema_null
   ranjg-json-schema_string
   ranjg-json-schema_number
   ranjg-json-schema_boolean
   ranjg-json-schema_array
   ranjg-json-schema_object

.. _JSON schema: https://json-schema.org/
