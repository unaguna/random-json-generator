import itertools
import unittest

import ranjg
from ranjg.factories import *


class TestFactory(unittest.TestCase):
    """Test class of ``Factory``

    Test ``ranjg.Factory``
    """

    def test_create_factory(self):
        """ Normalized System Test
        """
        case_list = (
            (NoneFactory, {'type': 'null'}, (None,)),
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
             (dict(p1=None), None)),
            (EnumFactory, {'enum': ['value1', 1]}, ('value1', 1)),
        )

        for clz, schema, expected_list in case_list:
            with self.subTest(clz=clz.__name__):
                # 確率的事象につき、何度か試す
                for _ in range(10):
                    factory = ranjg.Factory(schema)
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
            ({"type": "number", "minimum": 10.25, "maximum": 11.25}, ),
            ({"type": "string", "pattern": "st"}, ),
            ({"type": "array", "minItems": 1, "maxItems": 1}, ),
            ({"type": "object", "required": ["p1"]}, ),
            ({'enum': ['value1', 1]}, ),
        )

        for (gen_type, clz), (schema,) in itertools.product(gen_type_list, schema_list):
            with self.subTest(gen_type=gen_type, schema=schema):
                factory = ranjg.Factory(schema, gen_type=gen_type)
                self.assertIsInstance(factory, clz)
