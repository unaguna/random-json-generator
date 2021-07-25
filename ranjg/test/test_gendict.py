import unittest
from unittest import mock

import jsonschema

from ranjg import gendict
from .._context import Context
from .._generator import DictGenerator


class TestGendict(unittest.TestCase):
    """Test class of ``gendict``

    Test ``ranjg.gendict``
    """

    def test_gendict(self):
        """ Normalized System Test

        ``gendict()`` is wrapper of ``DictGenerator#gen()``.

        assert that:
            When ``gendict`` is called, then ``DictGenerator#gen()`` runs.
        """
        _context_dummy = Context.root({}).resolve('key', {})
        params_list = (
            (None, {}, None, None),
            ({"type": "object"}, {"type": "object"}, None, None),
            (None, {}, _context_dummy, _context_dummy),
        )

        for schema_arg, schema_used, context_arg, context_used in params_list:
            with mock.patch('ranjg._generator.DictGenerator.gen') as mock_gen:
                gendict(schema_arg, context=context_arg)
                mock_gen.assert_called_once_with(schema_used, context=context_used)


class TestDictGenerator(unittest.TestCase):
    """Test class of ``DictGenerator``

    Test ``DictGenerator``
    """

    def test_gen_with_empty_schema(self):
        """ Normalized System Test

        ``DictGenerator#gen(schema)`` returns dict. The result dict has only key in ``schema.required`` or
        ``schema.properties``.
        And ``schema.additionalProperties`` is ignored. As a consequence, when ``schema`` has no effective parameters,
        returns empty dict.

        assert that:
            When the schema is empty, ``DictGenerator#gen(schema)`` returns empty dict.
        """
        schema = {}
        generated = DictGenerator().gen(schema)
        self.assertIsInstance(generated, dict)
        self.assertDictEqual(generated, {})
        jsonschema.validate(generated, schema)

    def test_gen_with_required(self):
        """ Normalized System Test

        ``DictGenerator#gen(schema)`` returns dict. When ``schema.required`` is specified, the result dict has all keys
        in ``schema.required`` even if the key is not in ``schema.properties``.

        Because of the result dict has only key in ``schema.required`` or ``schema.properties``, the result dict has
        keys equal to ``schema.required`` when ``schema.properties`` is not specified.

        assert that:
            When schema has required, ``DictGenerator#gen(schema)`` returns a dict and
            every key are in the dict iff the key is in ``schema.required``.
        """
        schema = {
            "required": ["aaa", "bbb"],
        }
        generated = DictGenerator().gen(schema)
        self.assertIsInstance(generated, dict)
        self.assertSetEqual(set(generated.keys()), {"aaa", "bbb"})
        jsonschema.validate(generated, schema)

    def test_gen_with_required_and_properties(self):
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
        generated = DictGenerator().gen(schema)
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
        jsonschema.validate(generated, schema)
