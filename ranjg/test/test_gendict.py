import unittest
from unittest import mock

import jsonschema

from ranjg import gendict, Options
from .._context import Context
from ..factory import DictFactory
from ..factory.__dict import _schema_of


class TestGendict(unittest.TestCase):
    """Test class of ``gendict``

    Test ``ranjg.gendict``
    """

    def test_gendict(self):
        """ Normalized System Test

        ``gendict()`` is wrapper of ``DictFactory#gen()``.

        assert that:
            When ``gendict`` is called, then ``DictFactory#gen()`` runs.
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
            with mock.patch('ranjg.factory.DictFactory.gen') as mock_gen:
                gendict(schema, context=context, schema_is_validated=is_validated, options=options)
                mock_gen.assert_called_once_with(context=context, options=options)
            # TODO: schema, schema_is_validated についても assert する


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
                "aaa": {"type": "number"},
                "bbb": {"type": "object"},
                "ccc": {"type": "string"},
                "ddd": {"type": "boolean"},
                "eee": {"type": "array"},
                "xxx": {"type": "null"},
                "zzz": {},
            },
        }
        generated = DictFactory(schema).gen()
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
                      'p1': {'type': 'integer'},
                      'p2': {'type': 'boolean'},
                      'p3': {'type': 'string'},
                      'p4': {'type': 'number'},
                  },
                  'required': ['p1']}

        # x = 0.0
        # Since this is a test of probabilistic events, it should be performed multiple times.
        for _ in range(10):
            generated = DictFactory(schema).gen(options=options_0)

            # contains the required property
            assert 'p1' in generated
            # not contains the optional property
            assert 'p2' not in generated
            assert 'p3' not in generated
            assert 'p4' not in generated

        # x = 1.0
        # Since this is a test of probabilistic events, it should be performed multiple times.
        for _ in range(10):
            generated = DictFactory(schema).gen(options=options_1)

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
        generated = DictFactory(schema).gen(options=Options(default_schema_of_properties=default_schema,
                                                              default_schema_of_items=dummy_schema))
        self.assertDictEqual(generated, {"p1": -100})

    def test_priority_schema_of_properties_with_prior(self):
        """ Normalized System Test

        When ``options.priority_schema_of_properties`` contains a key, corresponding property in generated dict (include
        nested dicts) satisfies a schema ``options.priority_schema_of_properties[key]`` and not necessarily satisfies
        ``schema.properties[key]``.
        """
        key = "p1"
        schema_list = ({"type": "object", "required": [key]},
                       {"type": "object", "required": [key], "properties": {key: {"type": "boolean"}}},)
        priority_schema = {"type": "integer", "maximum": -100, "minimum": -100}
        options = Options(priority_schema_of_properties={key: priority_schema})

        for schema in schema_list:
            generated = DictFactory(schema).gen(options=options)
            self.assertEqual(generated, {key: -100})

            schema_nest = {"type": "object", "required": ["parent"], "properties": {"parent": schema}}
            generated = DictFactory(schema_nest).gen(options=options)
            self.assertEqual(generated["parent"], {key: -100})

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
            generated = DictFactory(schema).gen(options=options)
            self.assertIsInstance(generated[key], bool)

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
            generated = DictFactory(schema).gen(options=options)
            self.assertTrue(key not in generated)

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
            generated = DictFactory(schema).gen(options=options)
            self.assertEqual(generated[key], -100)

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
            generated = DictFactory(schema).gen(options=options)
            self.assertTrue(key not in generated)

            schema_nest = {"type": "object", "required": ["parent"], "properties": {"parent": schema}}
            generated = DictFactory(schema_nest).gen(options=options)
            self.assertTrue(key not in generated["parent"])

    def test_schema_of_uses_default(self):
        """ Normalized System Test

        ``_schema_of`` returns the default schema when ``key`` is not contained in neither ``properties`` or
        ``priority_properties``.

        assert that:
            When both of a property and a priority_property don't contain ``key``, ``_schema_of`` returns default.
        """
        properties = {"p1": {"type": "boolean"}}
        priority_properties = {"p2": {"type": "boolean"}}
        default_schema = {"type": "integer", "maximum": -100, "minimum": -100}

        schema = _schema_of("px", properties=properties, priority_properties=priority_properties,
                            default_schema=default_schema)

        self.assertDictEqual(schema, default_schema)

    def test_schema_of_uses_properties(self):
        """ Normalized System Test

        ``_schema_of`` returns the schema in ``properties`` when ``key`` is contained in ``properties`` and not in
        ``priority_properties``.

        assert that:
            When a property contains ``key`` and a priority_property doesn't contain ``key``, ``_schema_of`` returns
            ``property[key]``.
        """
        key = "p1"
        properties = {key: {"type": "string"}}
        priority_properties = {"p2": {"type": "boolean"}}
        default_schema = {"type": "integer", "maximum": -100, "minimum": -100}

        schema = _schema_of(key, properties=properties, priority_properties=priority_properties,
                            default_schema=default_schema)

        self.assertDictEqual(schema, properties[key])

    def test_schema_of_uses_priority_property(self):
        """ Normalized System Test

        ``_schema_of`` returns the schema in ``priority_property`` when ``key`` is contained in ``priority_property``.
        In this case, ``properties`` is ignored.

        assert that:
            When a priority_property contains ``key``, ``_schema_of`` returns ``priority_property[key]``.
        """
        key = "p2"
        properties_list = ({"p1": {"type": "boolean"}},
                           {"p1": {"type": "boolean"}, key: {"type": "boolean"}})
        priority_properties = {key: {"type": "number"}}
        default_schema = {"type": "integer", "maximum": -100, "minimum": -100}

        for properties in properties_list:
            schema = _schema_of(key, properties=properties, priority_properties=priority_properties,
                                default_schema=default_schema)

            self.assertDictEqual(schema, priority_properties[key])
