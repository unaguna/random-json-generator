Null Generation
===============
When ``null`` is adopted as :doc:`type <ranjg-json-schema_type>`, ``ranjg.gen`` returns ``None``. Then the other keywords are ignored.

>>> import ranjg
>>> schema = { 'type': 'null' }
>>> generated = ranjg.gen(schema)  # -> returns None
>>> type(generated)
<class 'NoneType'>

.. TODO: null の活用方法として、オブジェクトの要素のスキーマに "type":["integer","null"] を指定する例へのリンクを張る

