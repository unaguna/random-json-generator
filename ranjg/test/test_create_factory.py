import itertools
import unittest

from ranjg.factory import *
from ranjg.factory.__create_factory import _raffle_type


class TestCreateFactory(unittest.TestCase):
    """Test class of ``create_factory``

    Test ``ranjg.factory.create_factory``
    """

    def test_create_factory(self):
        """ Normalized System Test
        """
        case_list = ((NoneFactory, {'type': 'null'}, (None,)),
                     (BoolFactory, {'type': 'boolean'}, (True, False)),
                     (IntFactory, {'type': 'integer', 'minimum': 0, 'maximum': 0}, (0,)),
                     (NumFactory, {'type': 'number', 'minimum': 0, 'maximum': 0}, (0.0,)),
                     (StrFactory, {'type': 'string', 'pattern': 'test'}, ('test',)),
                     (ListFactory, {'type': 'array', 'maxItems': 0}, (list(),)),
                     (DictFactory,
                      {'type': 'object', 'required': ['p1'], 'properties': {'p1': {'type': 'null'}}},
                      (dict(p1=None),)),
                     (MultiFactory,
                      {'type': ['object', 'null'], 'required': ['p1'], 'properties': {'p1': {'type': 'null'}}},
                      (dict(p1=None), None)),)

        for clz, schema, expected_list in case_list:
            with self.subTest(clz=clz.__name__):
                # 確率的事象につき、何度か試す
                for _ in range(10):
                    factory = create_factory(schema)
                    generated = factory.gen()

                    self.assertIsInstance(factory, clz)
                    self.assertIn(generated, expected_list)

    def test_create_factory_with_gen_type(self):
        """ Normalized System Test
        """
        gen_type_list = (
            ('null', NoneFactory),
            ('boolean', BoolFactory),
            ('integer', IntFactory),
            ('number', NumFactory),
            ('string', StrFactory),
            ('array', ListFactory),
            ('object', DictFactory),
        )
        schema_list = (
            ({"type": "null"}, ),
            ({"type": "boolean"}, ),
            ({"type": "integer", "minimum": 100, "maximum": 100}, ),
            ({"type": "number", "minimum": 10.25, "maximum": 10.25}, ),
            ({"type": "string", "pattern": "st"}, ),
            ({"type": "array", "minItems": 1, "maxItems": 1}, ),
            ({"type": "object", "required": ["p1"]}, ),
        )

        for (gen_type, clz), (schema,) in itertools.product(gen_type_list, schema_list):
            with self.subTest(gen_type=gen_type, schema=schema):
                factory = create_factory(schema, gen_type=gen_type)
                self.assertIsInstance(factory, clz)


class TestRaffleType(unittest.TestCase):
    """Test class of ``_raffle_type``

    Test ``ranjg.factory.__function._raffle_type``
    """

    def test_raffle_type_with_none(self):
        """ Normalized System Test

        If argument ``schema_type`` is None, returns None.

        assert that:
            If ``schema_type`` is None, ``_raffle_type(schema_type)`` returns None.
        """
        choice = _raffle_type(None)
        self.assertIsNone(choice)

    def test_raffle_type_with_str(self):
        """ Normalized System Test

        If argument ``schema_type`` is string, returns it.

        assert that:
            If ``schema_type`` is string, ``_raffle_type(schema_type)`` returns string same to the argument.
        """
        schema_type_list = ("null", "boolean", "integer", "number", "string", "array", "object")

        for schema_type in schema_type_list:
            with self.subTest(type=schema_type):
                choice = _raffle_type(schema_type)
                self.assertEqual(choice, schema_type)

    def test_raffle_type_with_list(self):
        """ Normalized System Test

        If argument ``schema_type`` is non-empty list, returns a string in the argument.

        assert that:
            If ``schema_type`` is non-empty list, ``_raffle_type(schema_type)`` returns a string of the argument.
        """
        schema_type_list = (["null", "boolean", "integer", "number", "string", "array", "object"],
                            ["null", "number"],
                            ["string", "boolean"])

        for schema_type in schema_type_list:
            with self.subTest(type=schema_type):
                for i in range(5):
                    choice = _raffle_type(schema_type)
                    self.assertIn(choice, schema_type)

    def test_raffle_type_with_empty_list(self):
        """ Normalized System Test

        If argument ``schema_type`` is empty list, returns None.

        assert that:
            If ``schema_type`` is empty list, ``_raffle_type(schema_type)`` returns None.
        """
        self.assertRaises(ValueError, lambda: _raffle_type([]))
