import unittest

import ranjg
from ranjg.error import InvalidOptionsError


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

        with self.assertRaises(FileNotFoundError):
            ranjg.options.load(options_file)

    def test_load_invalid_as_options(self):
        options_file = "./test-resources/options-illegal-param.json"

        with self.assertRaises(InvalidOptionsError, msg=options_file):
            ranjg.options.load(options_file)

    def test_load_invalid_as_json(self):
        options_file = "./test-resources/options-illegal.json"

        with self.assertRaises(InvalidOptionsError, msg=options_file):
            ranjg.options.load(options_file)

