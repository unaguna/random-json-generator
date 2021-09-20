import unittest
from unittest import mock

import jsonschema

from ranjg import gendict, Options
from .res import sample_schema
from .._context import GenerationContext
from ..factories import DictFactory


class TestGendict(unittest.TestCase):
    """Test class of ``gendict``

    Test ``ranjg.gendict``
    """

    def test_when_gendict_then_call_init(self):
        """ Normalized System Test

        ``gendict()`` is wrapper of ``DictFactory#gen()``.

        assert that:
            When ``gendict`` is called, then ``DictFactory()`` runs.
        """
        _context_dummy = GenerationContext.root({}).resolve('key', {})
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
            with self.subTest(schema=schema, is_validated=is_validated, options=(options is not None)), \
                    mock.patch('ranjg.factories.DictFactory.__init__', return_value=None) as mock_gen, \
                    mock.patch('ranjg.factories.DictFactory.gen'):
                gendict(schema, context=context, schema_is_validated=is_validated, options=options)
                mock_gen.assert_called_once_with(schema, schema_is_validated=is_validated)

    def test_when_gendict_then_call_gen(self):
        """ Normalized System Test

        ``gendict()`` is wrapper of ``DictFactory#gen()``.

        assert that:
            When ``gendict`` is called, then ``DictFactory#gen()`` runs.
        """
        _context_dummy = GenerationContext.root({}).resolve('key', {})
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
            with self.subTest(schema=schema, is_validated=is_validated, options=(options is not None)), \
                    mock.patch('ranjg.factories.DictFactory.gen') as mock_gen:
                gendict(schema, context=context, schema_is_validated=is_validated, options=options)
                mock_gen.assert_called_once_with(context=context, options=options)


class TestDictFactory(unittest.TestCase):
    """Test class of ``DictFactory``

    Test ``DictFactory``
    """

    def test_gen_with_empty_schema(self):
        """ Normalized System Test

        ``DictFactory#gen(schema)`` returns dict. The result dict has only key in ``schema.required`` or
        ``schema.properties``.
        And ``schema.additionalProperties`` is ignored. As a consequence, when ``schema`` has no effective parameters,
        returns empty dict.

        assert that:
            When the schema is empty, ``DictFactory#gen(schema)`` returns empty dict.
        """
        schema = {}
        generated = DictFactory(schema).gen()
        self.assertIsInstance(generated, dict)
        self.assertDictEqual(generated, {})
        jsonschema.validate(generated, schema)

    def test_gen_with_required(self):
        """ Normalized System Test

        ``DictFactory#gen(schema)`` returns dict. When ``schema.required`` is specified, the result dict has all keys
        in ``schema.required`` even if the key is not in ``schema.properties``.

        Because of the result dict has only key in ``schema.required`` or ``schema.properties``, the result dict has
        keys equal to ``schema.required`` when ``schema.properties`` is not specified.

        assert that:
            When schema has required, ``DictFactory#gen(schema)`` returns a dict and
            every key are in the dict iff the key is in ``schema.required``.
        """
        schema = {
            "required": ["aaa", "bbb"],
        }
        generated = DictFactory(schema).gen()
        self.assertIsInstance(generated, dict)
        self.assertSetEqual(set(generated.keys()), {"aaa", "bbb"})
        jsonschema.validate(generated, schema)

    def test_gen_with_required_and_properties(self):
        schema = {
            "required": ["aaa", "bbb", "ccc", "ddd", "eee", "xxx", "zzz"],
            "properties": {
                "aaa": sample_schema('number'),
                "bbb": sample_schema('object'),
                "ccc": sample_schema('string'),
                "ddd": sample_schema('boolean'),
                "eee": sample_schema('array'),
                "xxx": sample_schema('null'),
                "zzz": {},
            },
        }
        generated = DictFactory(schema).gen()
        self.assertIsInstance(generated, dict)
        self.assertSetEqual(set(generated.keys()),
                            {"aaa", "bbb", "ccc", "ddd", "eee", "xxx", "zzz"})
        self.assertIsInstance(generated["aaa"], float)
        self.assertIsInstance(generated["bbb"], dict)
        self.assertIsInstance(generated["ccc"], str)
        self.assertIsInstance(generated["ddd"], bool)
        self.assertIsInstance(generated["eee"], list)
        self.assertIsNone(generated["xxx"])
        jsonschema.validate(generated, schema)

    def test_gen_with_option_default_prob_of_optional_properties(self):
        """ Normalized System Test

        ``DictFactory#gen(schema)`` uses a option ``default_prob_of_optional_properties`` (float, 0.0 <= x <= 1.0).

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
                      'p1': sample_schema('integer'),
                      'p2': sample_schema('boolean'),
                      'p3': sample_schema('string'),
                      'p4': sample_schema('number'),
                  },
                  'required': ['p1']}

        # x = 0.0
        # Since this is a test of probabilistic events, it should be performed multiple times.
        with self.subTest(default_prob_of_optional_properties=0.0):
            for _ in range(10):
                generated = DictFactory(schema).gen(options=options_0)

                # contains the required property
                assert 'p1' in generated
                # not contains the optional property
                assert 'p2' not in generated
                assert 'p3' not in generated
                assert 'p4' not in generated

                jsonschema.validate(generated, schema)

        # x = 1.0
        # Since this is a test of probabilistic events, it should be performed multiple times.
        with self.subTest(default_prob_of_optional_properties=1.0):
            for _ in range(10):
                generated = DictFactory(schema).gen(options=options_1)

                # contains the required property
                assert 'p1' in generated
                # contains the optional property
                assert 'p2' in generated
                assert 'p3' in generated
                assert 'p4' in generated

                jsonschema.validate(generated, schema)

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
        default_schema_list = (
            sample_schema('null'),
            sample_schema('boolean'),
            sample_schema('integer'),
            sample_schema('number'),
            sample_schema('string'),
            sample_schema('array'),
            # sample_schema('object'),  # 仕様上、子要素再帰が無限に続く
        )

        for default_schema in default_schema_list:
            with self.subTest(default_schema=default_schema):
                generated = DictFactory(schema).gen(options=Options(default_schema_of_properties=default_schema,
                                                                    default_schema_of_items=dummy_schema))
                jsonschema.validate(generated['p1'], default_schema)
                jsonschema.validate(generated, schema)

    def test_priority_schema_of_properties_with_prior(self):
        """ Normalized System Test

        When ``options.priority_schema_of_properties`` contains a key, corresponding property in generated dict (include
        nested dicts) satisfies a schema ``options.priority_schema_of_properties[key]`` and not necessarily satisfies
        ``schema.properties[key]``.
        """
        key = "p1"
        schema_list = ({"type": "object", "required": [key]},
                       {"type": "object", "required": [key], "properties": {key: {"type": "boolean"}}},)
        priority_schema = sample_schema('integer')
        options = Options(priority_schema_of_properties={key: priority_schema})

        for schema in schema_list:
            with self.subTest(nested=False, schema=schema):
                generated = DictFactory(schema).gen(options=options)
                jsonschema.validate(generated[key], priority_schema)

            with self.subTest(nested=True, schema=schema):
                schema_nest = {"type": "object", "required": ["parent"], "properties": {"parent": schema}}
                generated = DictFactory(schema_nest).gen(options=options)
                jsonschema.validate(generated['parent'][key], priority_schema)

    def test_priority_schema_of_properties_with_not_prior(self):
        """ Normalized System Test

        When ``options.priority_schema_of_properties`` contains a key, corresponding property in generated dict (include
        nested dicts) satisfies a schema ``options.priority_schema_of_properties[key]`` and not necessarily satisfies
        ``schema.properties[key]``.
        """
        key = "p1"
        schema_list = ({"type": "object", "required": [key], "properties": {key: {"type": "boolean"}}},)
        priority_schema = {"type": "integer", "maximum": -100, "minimum": -100}
        options = Options(priority_schema_of_properties={"px": priority_schema})

        for schema in schema_list:
            with self.subTest(nested=False, schema=schema):
                generated = DictFactory(schema).gen(options=options)
                self.assertIsInstance(generated[key], bool)

            with self.subTest(nested=True, schema=schema):
                schema_nest = {"type": "object", "required": ["parent"], "properties": {"parent": schema}}
                generated = DictFactory(schema_nest).gen(options=options)
                self.assertIsInstance(generated["parent"][key], bool)

    def test_priority_schema_of_properties_with_not_required_key(self):
        """ Normalized System Test

        When ``options.priority_schema_of_properties`` contains a key, corresponding property in generated dict (include
        nested dicts) satisfies a schema ``options.priority_schema_of_properties[key]`` and not necessarily satisfies
        ``schema.properties[key]``.
        """
        key = "p1"
        schema_list = ({"type": "object", "required": ["p2"]},
                       {"type": "object", "required": ["p2"], "properties": {key: {"type": "boolean"}}},)
        priority_schema = {"type": "integer", "maximum": -100, "minimum": -100}
        options = Options(priority_schema_of_properties={key: priority_schema},
                          # required でない要素が required であるかのように処理されていないことを確かめるため
                          default_prob_of_optional_properties=0.0)

        for schema in schema_list:
            with self.subTest(nested=False, schema=schema):
                generated = DictFactory(schema).gen(options=options)
                self.assertTrue(key not in generated)

            with self.subTest(nested=True, schema=schema):
                schema_nest = {"type": "object", "required": ["parent"], "properties": {"parent": schema}}
                generated = DictFactory(schema_nest).gen(options=options)
                self.assertTrue(key not in generated["parent"])

    def test_priority_schema_of_properties_with_not_required_key_2(self):
        """ Normalized System Test

        When ``options.priority_schema_of_properties`` contains a key, corresponding property in generated dict (include
        nested dicts) satisfies a schema ``options.priority_schema_of_properties[key]`` and not necessarily satisfies
        ``schema.properties[key]``.
        """
        key = "p1"
        schema_list = ({"type": "object", "required": ["p2"], "properties": {key: {"type": "boolean"}}},)
        priority_schema = {"type": "integer", "maximum": -100, "minimum": -100}
        options = Options(priority_schema_of_properties={key: priority_schema},
                          # required でない場合も priority_schema_of_properties が使用されることを確かめるため
                          default_prob_of_optional_properties=1.0)

        for schema in schema_list:
            with self.subTest(nested=False, schema=schema):
                generated = DictFactory(schema).gen(options=options)
                self.assertEqual(generated[key], -100)

            with self.subTest(nested=True, schema=schema):
                schema_nest = {"type": "object", "required": ["parent"], "properties": {"parent": schema}}
                generated = DictFactory(schema_nest).gen(options=options)
                self.assertEqual(generated["parent"][key], -100)

    def test_priority_schema_of_properties_with_not_required_key_3(self):
        """ Normalized System Test

        When ``options.priority_schema_of_properties`` contains a key, corresponding property in generated dict (include
        nested dicts) satisfies a schema ``options.priority_schema_of_properties[key]`` and not necessarily satisfies
        ``schema.properties[key]``.
        """
        key = "p1"
        schema_list = ({"type": "object"}, {"type": "object", "required": ["p2"]},)
        priority_schema = {"type": "integer", "maximum": -100, "minimum": -100}
        options = Options(priority_schema_of_properties={key: priority_schema},
                          # schema に登場しないプロパティは priority_schema_of_properties に指定があっても生成されないことを確かめるため
                          default_prob_of_optional_properties=1.0)

        for schema in schema_list:
            with self.subTest(nested=False, schema=schema):
                generated = DictFactory(schema).gen(options=options)
                self.assertTrue(key not in generated)

            with self.subTest(nested=True, schema=schema):
                schema_nest = {"type": "object", "required": ["parent"], "properties": {"parent": schema}}
                generated = DictFactory(schema_nest).gen(options=options)
                self.assertTrue(key not in generated["parent"])
