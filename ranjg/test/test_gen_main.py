import itertools
import json
import sys
import os
from os import path
import random
import shutil
from test.support import captured_stdout, captured_stderr
import unittest
from unittest.mock import patch
import jsonschema
from ranjg.__main__ import main as module_main


class TestGenMain(unittest.TestCase):
    """Test class of commandline execution

    Test commandline execution ``python -m ranjg``
    """

    #: str: The path of directory where tests output file.
    TEST_TMP_DIR = "./test-tmp/test_gen_main"
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

    def test_gen_main_with_schema_file(self):
        """ Normalized System Test

        Module execution received a argument as schema file. Without option ``-j``, the module execution outputs
        generated value to stdout in one line.

        assert that:
            With only one argument ``schema_file``, module execution output a value valid schema to stdout in one line.
        """
        schema_file_list = ("./test-resources/schema-legal-type_str.json",
                            "./test-resources/schema-legal-user_object.json",
                            "./test-resources/schema-legal-list.json",)

        for schema_file in schema_file_list:
            with self.subTest(schema_file=schema_file):
                with open(schema_file) as fp:
                    schema = json.load(fp)
                test_args = ["__main__.py", schema_file]

                with captured_stdout() as stdout:
                    with patch.object(sys, 'argv', test_args):
                        module_main()

                output_str = stdout.getvalue()
                output = json.loads(output_str)

                self.assertTrue("\n" not in output_str)
                jsonschema.validate(output, schema)

    def test_gen_main_with_schema_file_and_output_file(self):
        """ Normalized System Test

        Module execution received a argument as schema file. With option ``-j output_file``, the module execution
        outputs generated value to the ``output_file`` in one line.

        assert that:
            With only one argument ``schema_file``, module execution output a value valid schema to the ``output_file``
            in one line. Then nothing are output to stdout.
        """
        schema_file_list = ("./test-resources/schema-legal-type_str.json",
                            "./test-resources/schema-legal-user_object.json",
                            "./test-resources/schema-legal-list.json",)
        output_file = path.join(self.TEST_TMP_DIR_PRE, "test_gen_main_with_schema_file_and_output_file_output.json")

        for schema_file in schema_file_list:
            with self.subTest(schema_file=schema_file):
                with open(schema_file) as fp:
                    schema = json.load(fp)
                test_args = ["__main__.py", schema_file, "-j", output_file]

                with captured_stdout() as stdout:
                    with patch.object(sys, 'argv', test_args):
                        module_main()

                output = stdout.getvalue()

                with open(output_file) as fp:
                    generated = json.load(fp)

                self.assertEqual(output, "")
                self.assertTrue(path.exists(output_file))
                jsonschema.validate(generated, schema)

    def test_gen_main_with_options_file(self):
        """ Normalized System Test
        """
        schema_file = "./test-resources/schema-legal-list.json"
        options_file = "./test-resources/options-legal-list.json"

        with open(schema_file) as fp:
            schema = json.load(fp)
        test_args = ["__main__.py", schema_file, "--options", options_file]

        with captured_stdout() as stdout:
            with patch.object(sys, 'argv', test_args):
                module_main()

        output_str = stdout.getvalue()
        output = json.loads(output_str)

        self.assertEqual(output[0]["comment"], '2')
        jsonschema.validate(output, schema)

    def test_gen_main_with_multiplicity(self):
        """ Normalized System Test

        Module execution received an optional argument ``--line`` as multiplicity.
        If it's specified, it repeats the generation for the specified number of times and output the results as a list.

        ``-l`` is an abbreviation for ``--line``.

        assert that:
            With an argument ``-l``, module execution output a list whose element valid schema.
            With an argument ``--line``, perform the same action.
        """
        schema_file_list = ("./test-resources/schema-legal-type_str.json",
                            "./test-resources/schema-legal-user_object.json",
                            "./test-resources/schema-legal-list.json",)

        for schema_file, arg, multiplicity in itertools.product(schema_file_list, ('-l', '--list'), range(10)):
            test_args = ["__main__.py", schema_file, arg, str(multiplicity)]
            with self.subTest(args=test_args):
                with open(schema_file) as fp:
                    schema = json.load(fp)

                with captured_stdout() as stdout:
                    with patch.object(sys, 'argv', test_args):
                        module_main()

                output_str = stdout.getvalue()
                output = json.loads(output_str)

                self.assertIsInstance(output, list)
                self.assertEqual(len(output), multiplicity)
                for output_elem in output:
                    jsonschema.validate(output_elem, schema)

    def test_gen_main_with_num(self):
        """ Normalized System Test

        Module execution received an optional argument ``-n`` as the number of output files.
        If it's specified, it repeats the generation for the specified number of times and outputs to each file.

        As filenames, strings in which placeholders in the string specified by ``--json_output`` are replaced with
        sequential numbers will be used.

        assert that:
            With an argument ``-n``, module execution output to multiple files.
        """
        schema_file = "./test-resources/schema-legal-user_object.json"
        output_file = path.join(self.TEST_TMP_DIR_PRE, "test_gen_main_with_num_{}.json")
        num = 5

        test_args = ["__main__.py", schema_file, '-n', str(num), '--json_output', output_file]

        with open(schema_file) as fp:
            schema = json.load(fp)

        with captured_stdout() as stdout:
            with patch.object(sys, 'argv', test_args):
                module_main()

        # output nothing to stdout when --num is specified.
        output_str = stdout.getvalue()
        self.assertEqual(output_str, '')

        for i in range(num):
            with open(output_file.format(i)) as fp:
                generated = json.load(fp)
            jsonschema.validate(generated, schema)

        self.assertFalse(path.exists(output_file.format(num)))

    def test_gen_main_with_num_without_output_file(self):
        """ Normalized System Test

        When Module execution received an optional argument ``-n``, another option ``--json_output`` is required.

        assert that:
            With an argument ``-n`` and without an argument ``--json_output``, module execution raises exception.
        """
        schema_file = "./test-resources/schema-legal-user_object.json"
        num = 5

        test_args = ["__main__.py", schema_file, '-n', str(num)]

        with captured_stdout() as stdout, captured_stderr() as stderr:
            with patch.object(sys, 'argv', test_args):
                with self.assertRaises(SystemExit) as error_ctx:
                    module_main()
                self.assertEqual(error_ctx.exception.code, 2)

        output_str = stdout.getvalue()
        self.assertEqual(output_str, '')

        stderr_str = stderr.getvalue()
        self.assertIn("error: the following arguments are required when -n is specified: --json_output", stderr_str)

    def test_gen_main_with_illegal_file_num(self):
        """ Normalized System Test

        When Module execution received an optional argument ``-n``, it must be positive integer.

        assert that:
            With an argument ``-n`` and illegal value, module execution raises exception.
        """
        schema_file = "./test-resources/schema-legal-user_object.json"
        num_list = ('0', '-1', '1.1', 'e')

        for num in num_list:
            with self.subTest(num=num):
                test_args = ["__main__.py", schema_file, '-n', num]

                with captured_stdout() as stdout, captured_stderr() as stderr:
                    with patch.object(sys, 'argv', test_args):
                        with self.assertRaises(SystemExit) as error_ctx:
                            module_main()
                        self.assertEqual(error_ctx.exception.code, 2)

                output_str = stdout.getvalue()
                self.assertEqual(output_str, '')

                stderr_str = stderr.getvalue()
                self.assertIn("error: argument -n: invalid positive_integer value:", stderr_str)
