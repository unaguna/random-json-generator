import itertools
import unittest

from ranjg.factory import *


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
