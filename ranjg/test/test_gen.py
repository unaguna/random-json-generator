import itertools
import json
import os
from contextlib import ExitStack
from os import path
import random
import shutil
import unittest
import jsonschema
import ranjg.options
from ranjg import gen
from ..error import InvalidSchemaError
from ..error.__schema_file_io_error import SchemaFileIOError


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
        # 確率的事象につき、何度か試す
        for _ in range(5):
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
        with self.assertRaisesRegex(InvalidSchemaError, r'\[\] is too short'):
            gen(schema)

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

    def test_gen_with_output_file_path_list(self):
        """ Normalized System Test
        """
        schema_file = "./test-resources/schema-legal-user_object.json"
        with open(schema_file) as fp:
            schema = json.load(fp)
        output_file_list = (path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_file_path_output_1.json"),
                            path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_file_path_output_2.json"),
                            path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_file_path_output_3.json"),)

        # output_file として list や tuple ではなくイテレータを受け取っても正しく動作することを確認
        generated = gen(schema_file=schema_file, output_file_list=iter(output_file_list))

        # validate return value
        self.assertIsInstance(generated, list)
        self.assertEqual(len(generated), len(output_file_list))
        for generated_elem in generated:
            jsonschema.validate(generated_elem, schema)

        # validate output
        for output_file, generated_elem in zip(output_file_list, generated):
            self.assertTrue(path.exists(output_file))
            with open(output_file) as fp:
                output = json.load(fp)
            jsonschema.validate(output, schema)
            self.assertDictEqual(generated_elem, output)

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

    def test_gen_with_output_fp_list(self):
        """ Normalized System Test
        """
        schema_file = "./test-resources/schema-legal-user_object.json"
        with open(schema_file) as fp:
            schema = json.load(fp)
        output_file_list = (path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_file_path_output_1.json"),
                            path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_file_path_output_2.json"),
                            path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_file_path_output_3.json"),)

        with ExitStack() as stack:
            fp_list = [stack.enter_context(open(output_file, "w")) for output_file in output_file_list]
            generated = gen(schema_file="./test-resources/schema-legal-user_object.json",
                            output_fp_list=fp_list)

        # validate return value
        self.assertIsInstance(generated, list)
        self.assertEqual(len(generated), len(output_file_list))
        for generated_elem in generated:
            jsonschema.validate(generated_elem, schema)

        # validate output
        for output_file, generated_elem in zip(output_file_list, generated):
            self.assertTrue(path.exists(output_file))
            with open(output_file) as fp:
                output = json.load(fp)
            jsonschema.validate(output, schema)
            self.assertDictEqual(generated_elem, output)

    def test_gen_with_schema_and_schema_file(self):
        """ Semi-normalized System Test
        """
        schema = {"type": "string"}
        schema_file = "./test-resources/schema-legal-type_str.json"

        with self.assertRaisesRegex(ValueError, 'schema and schema_file'):
            gen(schema, schema_file=schema_file)

    def test_gen_with_illegal_schema_file_path(self):
        """ Semi-normalized System Test
        """
        schema_file = "./test-resources/json-illegal.json"

        with self.assertRaisesRegex(SchemaFileIOError, f'This file cannot be parsed as schema: {schema_file}'):
            gen(schema_file=schema_file)

    def test_gen_without_schema(self):
        """ Semi-normalized System Test

        ``ranjg.gen`` required either argument ``schema`` or ``schema_file``. When neither is specified, it raises
        ``ValueError``.

        assert that:
            When calling ``gen`` with no arguments, ``ValueError`` is raised.

        """
        with self.assertRaisesRegex(ValueError, 'schema or schema_file must be specified'):
            gen()

    def test_gen_with_output_file_and_output_fp(self):
        """ Semi-normalized System Test

        ``ranjg.gen`` receive only one of arguments ``output_file``, ``output_fp``, ``output_file_list`` and
        ``output_fp_list``. When two of them are specified, ``ranjg.gen`` raises ``ValueError``.

        assert that:
            When calling ``gen`` with two arguments of ``output_file``, ``output_fp``, ``output_file_list`` and
        ``output_fp_list``, ``ValueError`` is raised.

        """
        schema = {}
        output_file_1 = path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_file_path_output_1.json")
        output_file_2 = path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_file_path_output_2.json")
        output_file_list = (output_file_1, output_file_2)

        with open(output_file_1, "w") as fp1:
            with open(output_file_2, "w") as fp2:
                output_fp_list = (fp1, fp2)

                with self.subTest('output_file, output_fp'):
                    with self.assertRaisesRegex(ValueError, r'Only one of \(output_file, output_fp, output_file_list, '
                                                            r'output_fp_list\) can be set.'):
                        gen(schema, output_file=output_file_1, output_fp=fp1)

                with self.subTest('output_file, output_file_list'):
                    with self.assertRaisesRegex(ValueError, r'Only one of \(output_file, output_fp, output_file_list, '
                                                            r'output_fp_list\) can be set.'):
                        gen(schema, output_file=output_file_1, output_file_list=output_file_list)

                with self.subTest('output_file, output_fp_list'):
                    with self.assertRaisesRegex(ValueError, r'Only one of \(output_file, output_fp, output_file_list, '
                                                            r'output_fp_list\) can be set.'):
                        gen(schema, output_file=output_file_1, output_fp_list=output_fp_list)

                with self.subTest('output_fp, output_file_list'):
                    with self.assertRaisesRegex(ValueError, r'Only one of \(output_file, output_fp, output_file_list, '
                                                            r'output_fp_list\) can be set.'):
                        gen(schema, output_fp=fp1, output_file_list=output_file_list)

                with self.subTest('output_fp, output_fp_list'):
                    with self.assertRaisesRegex(ValueError, r'Only one of \(output_file, output_fp, output_file_list, '
                                                            r'output_fp_list\) can be set.'):
                        gen(schema, output_fp=fp1, output_fp_list=output_fp_list)

                with self.subTest('output_file_list, output_fp_list'):
                    with self.assertRaisesRegex(ValueError, r'Only one of \(output_file, output_fp, output_file_list, '
                                                            r'output_fp_list\) can be set.'):
                        gen(schema, output_file_list=output_file_list, output_fp_list=output_fp_list)

    def test_gen_with_options_file(self):
        options_file = "./test-resources/options-legal.json"
        schema = {"type": "object", "required": ["p2"]}

        generated = gen(schema, options_file=options_file)

        self.assertEqual(generated["p2"], '1')

    def test_gen_with_options_and_options_file(self):
        options_file = "./test-resources/options-legal.json"
        schema = {"type": "object", "required": ["p1"]}

        with self.assertRaisesRegex(ValueError, 'options and options_file'):
            gen(schema, options=ranjg.options.Options(), options_file=options_file)

    def test_gen_with_multiplicity(self):
        schema_list = (
            {"type": "null"},
            {"type": "boolean"},
            {"type": "integer", "minimum": 10, "maximum": 20},
            {"type": "number", "minimum": 10, "maximum": 20},
            {"type": "string", "pattern": r"\d\d\dA"},
            {"type": "array", "minItems": 2, "maxItems": 5, "items": {"type": "boolean"}},
            {"type": "object", "required": ["p1"], "properties": {"p1": {"type": "boolean"}}},
        )

        for schema, multiplicity in itertools.product(schema_list, range(5)):
            with self.subTest(multiplicity=multiplicity, schema=schema):
                generated = gen(schema, multiplicity=multiplicity)

                self.assertIsInstance(generated, list)
                self.assertEqual(len(generated), multiplicity)
                for generated_elem in generated:
                    jsonschema.validate(generated_elem, schema)

    def test_gen_with_multiplicity_and_multi_type(self):
        schema = {"type": ["null", "boolean"]}

        generated_list = gen(schema, multiplicity=100)

        self.assertIsInstance(generated_list, list)
        # type が複数ある場合に、すべてが使用されることを確かめる
        self.assertSetEqual(set(generated_list), {None, True, False})

    def test_gen_with_illegal_multiplicity(self):
        multiplicity_list = (-1, -2, 1.5, '1', [], dict(), tuple())
        schema = {"type": "boolean"}

        for multiplicity in multiplicity_list:
            with self.subTest(multiplicity=multiplicity):
                with self.assertRaisesRegex(ValueError, f"Illegal argument 'multiplicity'"):
                    gen(schema, multiplicity=multiplicity)

    # TODO: multiplicity を指定し、かつ output_file や output_fp をリストにした場合の動作仕様を決定し試験を作成する。

    def test_gen_with_return_none(self):
        schema_file = "./test-resources/schema-legal-user_object.json"
        with open(schema_file) as fp:
            schema = json.load(fp)
        output_file = path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_fp_output.json")

        with open(output_file, "w") as fp:
            generated = gen(schema_file="./test-resources/schema-legal-user_object.json",
                            output_fp=fp,
                            return_none=True)

        self.assertIsNone(generated)

        # validate output
        with open(output_file) as fp:
            output = json.load(fp)
        jsonschema.validate(output, schema)
