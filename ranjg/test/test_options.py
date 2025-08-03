import unittest
from unittest import mock

import ranjg
from ranjg import Options
from ranjg.error import OptionsFileIOError
from ranjg.factories import NoneFactory, BoolFactory, IntFactory, NumFactory, StrFactory, ListFactory, DictFactory

from .res import sample_schema, class_path


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
                with mock.patch(f'{class_path(clz)}.gen') as mock_gen:
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
                with mock.patch(f'{class_path(clz)}.gen') as mock_gen:
                    ranjg.gen(schema, options=options)

                self.assertGreaterEqual(len(mock_gen.call_args_list), 1)
                for call in mock_gen.call_args_list:
                    self.assertIn('options', call[1])
                    self.assertIs(options, call[1]['options'])

    def test_factory_construction_from_default_schema_of_items(self):
        """ Normalized System Test

        When ``options.default_schema_of_items`` is used to construct a factory, argument ``context`` has ``key_path``.
        """
        case_list = (
            (sample_schema('string'), tuple()),
            ({"type": "array", "items": [sample_schema('string')]}, (0,)),
            ({"type": "object", "required": ["c1"], "properties": {"c1": sample_schema('string')}}, ('c1',)),
        )
        schema = {"type": "array", "minItems": 1, "maxItems": 1}

        for default_schema, path_suffix in case_list:
            with self.subTest(path_suffix=path_suffix):

                with mock.patch(f'{class_path(StrFactory)}.__init__') as mock_init:
                    # 試験は StrFactory.__init__ の引数について行うので、呼び出し後の動作は不要。
                    # 下手に先へ進むと本来の __init__ が行う処理が行われていないせいでバグるので、ここで例外を出す。
                    mock_init.side_effect = ValueError('I am mock.')

                    with self.assertRaisesRegex(ValueError, 'I am mock.'):
                        ListFactory(schema).gen(options=Options(default_schema_of_items=default_schema))

                self.assertGreaterEqual(len(mock_init.call_args_list), 1)
                for call_args in mock_init.call_args_list:
                    context = call_args[1]['context']
                    self.assertTupleEqual(tuple(context.key_path), ('default_schema_of_items', *path_suffix))
                    if len(path_suffix) == 0:
                        self.assertTrue(context._is_for_options)

    def test_factory_construction_from_default_schema_of_properties(self):
        """ Normalized System Test

        When ``options.default_schema_of_properties`` is used to construct a factory, argument ``context`` has
        ``key_path``.
        """
        case_list = (
            (sample_schema('string'), tuple()),
            ({"type": "array", "items": [sample_schema('string')]}, (0,)),
            ({"type": "object", "required": ["c1"], "properties": {"c1": sample_schema('string')}}, ('c1',)),
        )
        schema = {"type": "object", "required": ["p1"]}

        for default_schema, path_suffix in case_list:
            with self.subTest(path_suffix=path_suffix):

                with mock.patch(f'{class_path(StrFactory)}.__init__') as mock_init:
                    # 試験は StrFactory.__init__ の引数について行うので、呼び出し後の動作は不要。
                    # 下手に先へ進むと本来の __init__ が行う処理が行われていないせいでバグるので、ここで例外を出す。
                    mock_init.side_effect = ValueError('I am mock.')

                    with self.assertRaisesRegex(ValueError, 'I am mock.'):
                        DictFactory(schema).gen(options=Options(default_schema_of_properties=default_schema))

                self.assertGreaterEqual(len(mock_init.call_args_list), 1)
                for call_args in mock_init.call_args_list:
                    context = call_args[1]['context']
                    self.assertTupleEqual(tuple(context.key_path), ('default_schema_of_properties', *path_suffix))
                    if len(path_suffix) == 0:
                        self.assertTrue(context._is_for_options)

    def test_factory_construction_from_priority_schema_of_properties(self):
        """ Normalized System Test

        When ``options.priority_schema_of_properties`` is used to construct a factory, argument ``context`` has
        ``key_path``.
        """
        case_list = (
            (sample_schema('string'), tuple()),
            ({"type": "array", "items": [sample_schema('string')]}, (0,)),
            ({"type": "object", "required": ["c1"], "properties": {"c1": sample_schema('string')}}, ('c1',)),
        )
        schema = {"type": "object", "required": ["p1"]}

        for priority_schema_value, path_suffix in case_list:
            priority_schema = {'p1': priority_schema_value}

            with self.subTest(path_suffix=path_suffix):

                with mock.patch(f'{class_path(StrFactory)}.__init__') as mock_init:
                    # 試験は Factory.__init__ の引数について行うので、呼び出し後の動作は不要。
                    # 下手に先へ進むと本来の __init__ が行う処理が行われていないせいでバグるので、ここで例外を出す。
                    mock_init.side_effect = ValueError('I am mock.')

                    with self.assertRaisesRegex(ValueError, 'I am mock.'):
                        DictFactory(schema).gen(options=Options(priority_schema_of_properties=priority_schema))

                self.assertGreaterEqual(len(mock_init.call_args_list), 1)
                for call_args in mock_init.call_args_list:
                    context = call_args[1]['context']
                    self.assertTupleEqual(tuple(context.key_path),
                                          ('priority_schema_of_properties', 'p1', *path_suffix))
                    if len(path_suffix) == 0:
                        self.assertTrue(context._is_for_options)
