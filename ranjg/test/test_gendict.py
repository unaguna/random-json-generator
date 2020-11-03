import unittest
from ranjg import gendict


class TestGendict(unittest.TestCase):
    """Test class of ``gendict``

    Test ``ranjg.gendict``
    """

    def test_gendict_with_empty_schema(self):
        """ Normalized System Test

        ``gendict(schema)`` returns dict. The result dict has only key in ``schema.required`` or ``schema.properties``.
        And ``schema.additionalProperties`` is ignored. As a consequence, when ``schema`` has no effective parameters,
        returns empty dict.

        assert that:
            When the schema is empty, ``gendict(schema)`` returns empty dict.
        """
        schema = {}
        generated = gendict(schema)
        # TODO: 取得した値がスキーマに合致することを確かめる。
        self.assertIsInstance(generated, dict)
        self.assertDictEqual(generated, {})

    def test_gendict_with_required(self):
        """ Normalized System Test

        ``gendict(schema)`` returns dict. When ``schema.required`` is specified, the result dict has all keys in
        ``schema.required`` even if the key is not in ``schema.properties``.

        Because of the result dict has only key in ``schema.required`` or ``schema.properties``, the result dict has
        keys equal to ``schema.required`` when ``schema.properties`` is not specified.

        assert that:
            When schema has required, ``gendict(schema)`` returns a dict and
            every key are in the dict iff the key is in ``schema.required``.
        """
        schema = {
            "required": ["aaa", "bbb"],
        }
        generated = gendict(schema)
        # TODO: 取得した値がスキーマに合致することを確かめる。
        self.assertIsInstance(generated, dict)
        self.assertSetEqual(set(generated.keys()), {"aaa", "bbb"})

    def test_gendict_with_required_and_properties(self):
        # TODO: properties 内のタイプについての試験は分解する。
        schema = {
            "required": ["aaa", "bbb", "ccc", "ddd", "eee", "xxx", "zzz"],
            "properties": {
                "aaa": {"type": "number"},
                "bbb": {"type": "object"},
                "ccc": {"type": "string"},
                "ddd": {"type": "boolean"},
                "eee": {"type": "array"},
                "xxx": {"type": "null"},
                "zzz": {},
            },
        }
        generated = gendict(schema)
        # TODO: 取得した値がスキーマに合致することを確かめる。
        self.assertIsInstance(generated, dict)
        self.assertSetEqual(set(generated.keys()),
                            {"aaa", "bbb", "ccc", "ddd", "eee", "xxx", "zzz"})
        self.assertIsInstance(generated["aaa"], float)
        self.assertIsInstance(generated["bbb"], dict)
        self.assertDictEqual(generated["bbb"], {})
        self.assertIsInstance(generated["ccc"], str)
        self.assertIsInstance(generated["ddd"], bool)
        self.assertIsInstance(generated["eee"], list)
        self.assertIsNone(generated["xxx"])
