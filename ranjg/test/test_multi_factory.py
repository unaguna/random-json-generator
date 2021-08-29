import unittest
from unittest import mock

from ranjg.factory import *


class TestMultiFactory(unittest.TestCase):
    """Test class of ``MultiFactory``

    Test ``MultiFactory``
    """

    def test_gen(self):
        """ Normalized System Test

        ``MultiFactory(schema).gen()`` returns value according the schema regardless of schema.type.
        """
        case_list = (
            ({"type": ["null"]}, (None,)),
            ({"type": ["boolean"]}, (True, False)),
            ({"type": ["integer"], "minimum": 100, "maximum": 100}, (100,)),
            ({"type": ["number"], "minimum": 10.25, "maximum": 10.25}, (10.25,)),
            ({"type": ["string"], "pattern": "st"}, ("st",)),
            ({"type": ["array"], "minItems": 1, "maxItems": 1, "items": {"type": "string", "pattern": "st"}}, (["st"],)),
            ({"type": ["object"], "required": ["p1"], "properties": {"p1": {"type": "string", "pattern": "st"}}},
             ({"p1": "st"},)),
            ({"type": ["null", "boolean"]}, (None, True, False)),
            ({"type": ["integer", "boolean"], "minimum": 100, "maximum": 100}, (100, True, False)),
            ({"type": ["integer", "string"], "minimum": 100, "maximum": 100, "pattern": "100"}, (100, "100")),
        )

        for schema, expected_list in case_list:
            with self.subTest(schema=schema):
                for i in range(10):
                    generated = MultiFactory(schema).gen()

                    self.assertIn(generated, expected_list)

    def test_gen_through_each_single_factory(self):
        """ Normalized System Test

        ``MultiFactory(schema).gen()`` uses factories to generate value.
        """
        case_list = (
            ({"type": ["null"]}, NoneFactory),
            ({"type": ["boolean"]}, BoolFactory),
            ({"type": ["integer"], "minimum": 100, "maximum": 100}, IntFactory),
            ({"type": ["number"], "minimum": 10.25, "maximum": 10.25}, NumFactory),
            ({"type": ["string"], "pattern": "st"}, StrFactory),
            ({"type": ["array"], "minItems": 1, "maxItems": 1}, ListFactory),
            ({"type": ["object"], "required": ["p1"]}, DictFactory),
        )

        for schema, clz in case_list:
            with self.subTest(clz=clz.__name__):
                with mock.patch(f'{clz}.gen') as mock_gen:
                    MultiFactory(schema).gen()
                    mock_gen.assert_called()

    def test_gen_with_illegal_type(self):
        """ Semi-normalized System Test

        ``MultiFactory(schema)`` raises error if schema.type is not Iterable[str].
        """
        schema_list = (
            {"type": "string"},
            {},
        )

        for schema in schema_list:
            with self.subTest(type=schema.get("type")):
                with self.assertRaises(ValueError,
                                       msg="For MultiFactory, schema.type must be iterable of at least 1 strings"):
                    MultiFactory(schema)
