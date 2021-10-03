import unittest
from unittest import mock

import ranjg
from ranjg.factories import NoneFactory, BoolFactory, IntFactory, NumFactory, StrFactory, ListFactory, DictFactory

from .res import sample_schema
from .._context import GenerationContext


class TestContext(unittest.TestCase):
    """Test class of ``GenerationContext``

    Test ``ranjg._context.GenerationContext``
    """

    def test_genlist_carry_context_over(self):
        case_list = (
            (sample_schema('null'), NoneFactory),
            (sample_schema('boolean'), BoolFactory),
            (sample_schema('integer'), IntFactory),
            (sample_schema('number'), NumFactory),
            (sample_schema('string'), StrFactory),
            (sample_schema('object'), DictFactory),
        )
        path = (1, '2', 3)

        for items, clz in case_list:
            with self.subTest(clz=clz):
                schema = {"type": "array", "minItems": 1, "maxItems": 1, "items": items}
                parent_context = GenerationContext(path, schema)
                with mock.patch(f'{clz}.gen') as mock_gen:
                    ranjg.gen(schema, context=parent_context)

                self.assertGreaterEqual(len(mock_gen.call_args_list), 1)
                for call in mock_gen.call_args_list:
                    self.assertIn('context', call[1])
                    self.assertTupleEqual((*path, 0), tuple(call[1]['context'].key_path))

    def test_gendict_carry_context_over(self):
        case_list = (
            (sample_schema('null'), NoneFactory),
            (sample_schema('boolean'), BoolFactory),
            (sample_schema('integer'), IntFactory),
            (sample_schema('number'), NumFactory),
            (sample_schema('string'), StrFactory),
            (sample_schema('array'), ListFactory),
        )
        path = (1, '2', 3)

        for items, clz in case_list:
            with self.subTest(clz=clz):
                schema = {"type": "object", "required": ["p1"], "properties": {"p1": items}}
                parent_context = GenerationContext(path, schema)
                with mock.patch(f'{clz}.gen') as mock_gen:
                    ranjg.gen(schema, context=parent_context)

                self.assertGreaterEqual(len(mock_gen.call_args_list), 1)
                for call in mock_gen.call_args_list:
                    self.assertIn('context', call[1])
                    self.assertTupleEqual((*path, "p1"), tuple(call[1]['context'].key_path))
