import unittest
from unittest import mock

import jsonschema

from ranjg import gendict, Options
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
        _options_dummy = Options.default()
        params_list = (
            (None, None, False, None),
            (None, None, False, _options_dummy),
            ({"type": "object"}, None, False, None),
            ({"type": "object"}, None, True, None),
            (None, _context_dummy, False, None),
            (None, _context_dummy, False, _options_dummy),
        )

        for schema, context, is_validated, options in params_list:
            with mock.patch('ranjg._generator.DictGenerator.gen') as mock_gen:
                gendict(schema, context=context, schema_is_validated=is_validated, options=options)
                mock_gen.assert_called_once_with(schema, context=context, schema_is_validated=is_validated,
                                                 options=options)


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

    def test_gen_with_option_default_prob_of_optional_properties(self):
        """ Normalized System Test

        ``DictGenerator#gen(schema)`` uses a option ``default_prob_of_optional_properties`` (float, 0.0 <= x <= 1.0).

        If ``default_prob_of_optional_properties`` x is specified, every optional property in the schema is contained
        in the result dict with a x probability independently.

        assert that:
            When ``default_prob_of_optional_properties`` is 1.0 (or 0.0), optional properties are surely in the result
            (or not).
        """
        options_0 = Options(default_prob_of_optional_properties=0.0)
        options_1 = Options(default_prob_of_optional_properties=1.0)
        schema = {'type': 'object',
                  'properties': {
                      'p1': {'type': 'integer'},
                      'p2': {'type': 'boolean'},
                      'p3': {'type': 'string'},
                      'p4': {'type': 'number'},
                  },
                  'required': ['p1']}

        # x = 0.0
        # Since this is a test of probabilistic events, it should be performed multiple times.
        for _ in range(10):
            generated = DictGenerator().gen(schema, options=options_0)

            # contains the required property
            assert 'p1' in generated
            # not contains the optional property
            assert 'p2' not in generated
            assert 'p3' not in generated
            assert 'p4' not in generated

        # x = 1.0
        # Since this is a test of probabilistic events, it should be performed multiple times.
        for _ in range(10):
            generated = DictGenerator().gen(schema, options=options_1)

            # contains the required property
            assert 'p1' in generated
            # contains the optional property
            assert 'p2' in generated
            assert 'p3' in generated
            assert 'p4' in generated

    def test_default_schema_of_properties(self):
        """ Normalized System Test

        When a property in ``schema.required`` but its schema is not in ``schema.properties``, this property satisfies
        ``options.default_schema_of_properties``.

        assert that:
            When a property is in ``schema.required`` but its schema is not in ``schema.properties``,
            the property of the generated dict is satisfied ``options.default_schema_of_properties``.

            Make sure it don't accidentally use ``options.default_schema_of_items``.
        """
        schema = {"type": "object", "required": ["p1"]}
        dummy_schema = {"type": "string", "pattern": "dummy"}
        default_schema = {"type": "integer", "maximum": -100, "minimum": -100}
        generated = DictGenerator().gen(schema, options=Options(default_schema_of_properties=default_schema,
                                                                default_schema_of_items=dummy_schema))
        self.assertDictEqual(generated, {"p1": -100})
