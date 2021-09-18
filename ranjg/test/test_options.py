import unittest
from unittest import mock

import ranjg
from ranjg import Options
from ranjg.error import OptionsFileIOError
from ranjg.factory import NoneFactory, BoolFactory, IntFactory, NumFactory, StrFactory, ListFactory, DictFactory

from .res import sample_schema


class TestOptions(unittest.TestCase):
    """Test class of ``Options``

    Test ``ranjg.options.Options``
    """

    def test_load(self):
        options_file = "./test-resources/options-legal.json"

        options = ranjg.options.load(options_file)

        self.assertIsInstance(options, ranjg.options.Options)
        self.assertEqual(options.regeneration_attempt_limit, 100)
        self.assertEqual(options.default_prob_of_true_given_bool, 0.2)
        self.assertEqual(options.default_length_range_of_genstr, 2)
        self.assertEqual(options.default_min_length_of_string, 10)
        self.assertEqual(options.default_max_length_of_string, 20)
        self.assertEqual(options.default_prob_of_optional_properties, 0.3)
        self.assertDictEqual(options.default_schema_of_properties, {"type": "string", "pattern": "1"})
        self.assertDictEqual(options.priority_schema_of_properties, {"p1": {"type": "string", "pattern": "2"}})
        self.assertDictEqual(options.default_schema_of_items, {"type": "string", "pattern": "3"})

    def test_load_raises_FileNotFoundError(self):
        # ファイルが存在しないパス
        options_file = "./test-resources/not-exists/options.json"

        with self.assertRaisesRegex(FileNotFoundError, options_file):
            ranjg.options.load(options_file)

    def test_load_invalid_as_options(self):
        options_file = "./test-resources/options-illegal-param.json"

        with self.assertRaisesRegex(OptionsFileIOError, options_file):
            ranjg.options.load(options_file)

    def test_load_invalid_as_json(self):
        options_file = "./test-resources/json-illegal.json"

        with self.assertRaisesRegex(OptionsFileIOError, options_file):
            ranjg.options.load(options_file)

    def test_genlist_carry_options_over(self):
        case_list = (
            (sample_schema('null'), NoneFactory),
            (sample_schema('boolean'), BoolFactory),
            (sample_schema('integer'), IntFactory),
            (sample_schema('number'), NumFactory),
            (sample_schema('string'), StrFactory),
            (sample_schema('object'), DictFactory),
        )

        for items, clz in case_list:
            with self.subTest(clz=clz):
                options = Options()
                schema = {"type": "array", "minItems": 1, "maxItems": 1, "items": items}
                with mock.patch(f'{clz}.gen') as mock_gen:
                    ranjg.gen(schema, options=options)

                self.assertGreaterEqual(len(mock_gen.call_args_list), 1)
                for call in mock_gen.call_args_list:
                    self.assertIn('options', call[1])
                    self.assertIs(options, call[1]['options'])

    def test_gendict_carry_options_over(self):
        case_list = (
            (sample_schema('null'), NoneFactory),
            (sample_schema('boolean'), BoolFactory),
            (sample_schema('integer'), IntFactory),
            (sample_schema('number'), NumFactory),
            (sample_schema('string'), StrFactory),
            (sample_schema('array'), ListFactory),
        )

        for items, clz in case_list:
            with self.subTest(clz=clz):
                options = Options()
                schema = {"type": "object", "required": ["p1"], "properties": {"p1": items}}
                with mock.patch(f'{clz}.gen') as mock_gen:
                    ranjg.gen(schema, options=options)

                self.assertGreaterEqual(len(mock_gen.call_args_list), 1)
                for call in mock_gen.call_args_list:
                    self.assertIn('options', call[1])
                    self.assertIs(options, call[1]['options'])
