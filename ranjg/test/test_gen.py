import json
import os
from os import path
import random
import shutil
import unittest
import jsonschema
from ranjg import gen


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
