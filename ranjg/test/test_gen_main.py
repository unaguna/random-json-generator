import sys
import os
from os import path
import random
import shutil
from test.support import captured_stdout
import unittest
from unittest.mock import patch
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
        schema_file = "./test-resources/schema-legal-type_str.json"
        # TODO: 複数のスキーマで試す。

        test_args = ["__main__.py", schema_file]

        with captured_stdout() as stdout:
            with patch.object(sys, 'argv', test_args):
                module_main()

        output = stdout.getvalue()
        # TODO: 取得した値がスキーマに合致することを確かめる。

        self.assertTrue(output.startswith("\""))
        self.assertTrue(output.endswith("\""))
        self.assertTrue("\n" not in output)

    def test_gen_main_with_schema_file_and_output_file(self):
        """ Normalized System Test

        Module execution received a argument as schema file. With option ``-j output_file``, the module execution
        outputs generated value to the ``output_file`` in one line.

        assert that:
            With only one argument ``schema_file``, module execution output a value valid schema to the ``output_file``
            in one line. Then nothing are output to stdout.
        """
        schema_file = "./test-resources/schema-legal-type_str.json"
        # TODO: 複数のスキーマで試す。
        output_file = path.join(self.TEST_TMP_DIR_PRE, "test_gen_main_with_schema_file_and_output_file_output.json")

        test_args = ["__main__.py", schema_file, "-j", output_file]

        with captured_stdout() as stdout:
            with patch.object(sys, 'argv', test_args):
                module_main()

        output = stdout.getvalue()

        self.assertEqual(output, "")
        # TODO: 取得した値がスキーマに合致することを確かめる。
        self.assertTrue(path.exists(output_file))
