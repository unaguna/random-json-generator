import json
import os
from os import path
import random
import shutil
import unittest
import jsonschema
import ranjg.options
from ranjg import gen
from ..__gen import _raffle_type
from ..error import InvalidSchemaError


class TestGen(unittest.TestCase):
    """Test class of ``gen``

    Test ``ranjg.gen``
    """

    #: str: The path of directory where tests output file.
    TEST_TMP_DIR = "./test-tmp/test_gen"
    #: str: The path of directory where tests output file.
    TEST_TMP_DIR_PRE = path.join(TEST_TMP_DIR, f"{random.randint(0, 2 ** 64):X}")

    @classmethod
    def setUpClass(cls):
        """preparation before tests

        It makes the directory for test output.
        """
        if path.exists(cls.TEST_TMP_DIR_PRE):
            shutil.rmtree(cls.TEST_TMP_DIR_PRE)
        os.makedirs(cls.TEST_TMP_DIR_PRE, exist_ok=True)

    def test_gen_with_empty_schema(self):
        """ Normalized System Test

        ``gen(schema)`` returns something even if schema is empty.

        assert that:
            When the schema is empty, ``gen(schema)`` returns without exception.
        """
        schema = {}
        generated = gen(schema)
        jsonschema.validate(generated, schema)

    def test_gen_with_multi_type(self):
        """ Normalized System Test

        If ``schema.type`` is a list, ``gen(schema)`` returns something.

        assert that:
            When ``schema.type`` is a list, ``gen(schema)`` returns a value type of a type in ``schema.type``.
        """
        for i in range(5):
            schema = {
                "type": ["string", "number"],
            }
            generated = gen(schema)
            self.assertTrue(type(generated) == str or type(generated) == float)
            jsonschema.validate(generated, schema)

    def test_gen_with_empty_multi_type(self):
        """ Semi-normalized System Test

        If ``schema.type`` is an empty list, ``gen(schema)`` raises InvalidSchemaError.

        assert that:
            When ``schema.type`` is an empty list, ``gen(schema)`` raises InvalidSchemaError.
        """
        schema = {
            "type": [],
        }
        self.assertRaises(InvalidSchemaError, lambda: gen(schema))

    def test_gen_with_schema_file_path(self):
        """ Normalized System Test

        ``gen(schema_file)`` returns something satisfying the schema defined by ``schema_file``.

        assert that:
            When the schema defined by ``schema_file`` has ``type: string``, ``gen(schema_file)`` returns a ``str``
            value.
        """
        schema_file = "./test-resources/schema-legal-type_str.json"
        with open(schema_file) as fp:
            schema = json.load(fp)

        generated = gen(schema_file=schema_file)
        jsonschema.validate(generated, schema)

    def test_gen_with_output_file_path(self):
        """ Normalized System Test

        ``gen(schema_file, output_file)`` returns a value satisfying the schema defined by ``schema_file`` and writes
        the generated value as JSON to file of path ``output_file``.

        assert that:
            ``gen(schema_file, output_file)`` returns a value satisfying the schema defined by ``schema_file``. And
            ``output_file`` is made and the generated value is written to the file as JSON.

        """
        schema_file = "./test-resources/schema-legal-user_object.json"
        with open(schema_file) as fp:
            schema = json.load(fp)
        output_file = path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_file_path_output.json")

        generated = gen(schema_file=schema_file, output_file=output_file)

        # validate return value
        jsonschema.validate(generated, schema)

        # validate output
        self.assertTrue(path.exists(output_file))
        with open(output_file) as fp:
            output = json.load(fp)
        jsonschema.validate(output, schema)
        self.assertDictEqual(generated, output)

    def test_gen_with_output_fp(self):
        """ Normalized System Test

        ``gen(schema_file, output_fp)`` returns a value satisfying the schema defined by ``schema_file`` and writes
        the generated value as JSON to file ``output_fp``.

        assert that:
            ``gen(schema_file, output_file)`` returns a value satisfying the schema defined by ``schema_file``. And
            the generated value is written as JSON to the file bound from ``output_fp``.

        """
        schema_file = "./test-resources/schema-legal-user_object.json"
        with open(schema_file) as fp:
            schema = json.load(fp)
        output_file = path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_fp_output.json")

        with open(output_file, "w") as fp:
            generated = gen(schema_file="./test-resources/schema-legal-user_object.json",
                            output_fp=fp)

        # validate return value
        jsonschema.validate(generated, schema)

        # validate output
        with open(output_file) as fp:
            output = json.load(fp)
        jsonschema.validate(output, schema)
        self.assertDictEqual(generated, output)

    # TODO: schema と schema_file をともに指定する場合のテスト

    # TODO: schema_file が JSON として解釈できない場合の挙動を定義して試験を作成する。

    def test_gen_without_schema(self):
        """ Semi-normalized System Test

        ``ranjg.gen`` required either argument ``schema`` or ``schema_file``. When neither is specified, it raises
        ``ValueError``.

        assert that:
            When calling ``gen`` with no arguments, ``ValueError`` is raised.

        """
        self.assertRaises(ValueError, lambda: gen())

    def test_gen_with_output_file_and_output_fp(self):
        """ Semi-normalized System Test

        ``ranjg.gen`` receive only one of arguments ``output_file`` and ``output_fp``. When both are specified,
        ``ranjg.gen`` raises ``ValueError``.

        assert that:
            When calling ``gen`` with arguments ``output_file`` and ``output_fp``, ``ValueError`` is raised.

        """
        schema = {}
        output_file = path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_file_path_output.json")

        with open(output_file, "w") as fp:
            self.assertRaises(ValueError,
                              lambda: gen(schema,
                                          output_file=output_file,
                                          output_fp=fp))

    def test_gen_with_options_file(self):
        options_file = "./test-resources/options-legal.json"
        schema = {"type": "object", "required": ["p2"]}

        generated = gen(schema, options_file=options_file)

        self.assertEqual(generated["p2"], '1')

    def test_gen_with_options_and_options_file(self):
        options_file = "./test-resources/options-legal.json"
        schema = {"type": "object", "required": ["p1"]}

        with self.assertRaises(ValueError, msg='options and options_file'):
            gen(schema, options=ranjg.options.Options(), options_file=options_file)


class TestRaffleType(unittest.TestCase):
    """Test class of ``_raffle_type``

    Test ``ranjg.__gen._raffle_type``
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
