import abc
import json
import random
from typing import Union, List, Optional, TextIO, TypeVar, Generic

from .__gennone import gennone
from .__genbool import genbool
from .__genint import genint
from .__gennum import gennum
from .__genstr import genstr
from .__gendict import gendict
from .__genlist import genlist
from .__genany import genany
from .validate.schema import validate_schema
from .util.nonesafe import dfor


def gen(schema: dict = None,
        schema_file: str = None,
        output_file: str = None,
        output_fp: TextIO = None,
        schema_is_validated: bool = False):
    """Generate something randomly according to the JSON schema.

    This function is not fully compliant with the JSON schema, and unsupported parameters in the schema are ignored.

    Examples
        The following code is most simple usage.

        >>> import ranjg
        >>> schema_dict = { 'type': 'string' }
        >>> ranjg.gen(schema_dict)    # -> returns some string

        By replacing the contents of ``schema_dict``, you can change the value to be generated.

        If you want to specify a schema without a python dict but with JSON file, you can use argument ``schema_file``.

        >>> import ranjg
        >>> schema_path = './schema_file.json'
        >>> ranjg.gen(schema_file=schema_path)  # -> returns some value

        If you want to get the result as JSON file, you can use argument ``output_file`` or ``output_fp``. (Following
        two examples will run similarly.

        >>> import ranjg
        >>> schema_dict = { 'type': 'string' }
        >>> ranjg.gen(schema_dict, output_file='./output.json')
        >>> # -> returns the result value and writes the result to specified file

        >>> import ranjg
        >>> schema_dict = { 'type': 'string' }
        >>> with open('./output.json', 'w+') as out_fp:
        >>>     ranjg.gen(schema_dict, output_fp=out_fp)
        >>>     # -> returns the result value and writes the result to specified file

    Args:
        schema (dict, default={}): JSON schema object.
        schema_file (str, optional):
            The path to JSON schema file. This JSON schema is used instead of the argument ``schema``.
        output_file (str, optional): The path to a file where the result will be output as JSON.
        output_fp (TextIO, optional): The writing object of a file where the result will be output as JSON.
        schema_is_validated (bool, optional):
            Whether the schema is already validated or not.
            (In normal usage, this argument does not specify.)

    Returns:
        Generated something. It is satisfies the JSON schema.

    Raises:
        InvalidSchemaError:
            When the schema specified as arguments is invalid.
        SchemaConflictError:
            When the schema specified as arguments has confliction.
            In other words, when no value can satisfy the schema.
        GenerateError:
            If an unforeseen error arises.
    """
    if schema is None and schema_file is None:
        raise ValueError("schema or schema_file must be specified.")
    if output_file is not None and output_fp is not None:
        raise ValueError("Only one of output_file and output_fp can be set. (You don't have to set either one.)")

    schema = dfor(schema, {})

    # スキーマファイルを読み込み
    if schema_file is not None:
        with open(schema_file) as fp:
            loaded_schema = json.load(fp)
            loaded_schema.update(schema)
            schema = loaded_schema

    # スキーマの不正判定
    if not schema_is_validated:
        validate_schema(schema)

    gen_type = _raffle_type(schema.get("type"))

    if gen_type is None:
        generated = genany(schema)
    elif gen_type == "null":
        generated = gennone()
    elif gen_type == "integer":
        generated = genint(schema)
    elif gen_type == "number":
        generated = gennum(schema)
    elif gen_type == "boolean":
        generated = genbool()
    elif gen_type == "string":
        generated = genstr(schema, schema_is_validated=True)
    elif gen_type == "object":
        generated = gendict(schema)
    elif gen_type == "array":
        generated = genlist(schema, schema_is_validated=True)
    else:
        raise ValueError(f"Unsupported type: {gen_type}")

    # 出力先指定がある場合、JSONとして出力する
    if output_file is not None:
        with open(output_file, "w+") as fp:
            json.dump(generated, fp)
    if output_fp is not None:
        json.dump(generated, output_fp)

    return generated


def _raffle_type(schema_type: Union[str, List[str], None]) -> Optional[str]:
    """Returns a type string specified by the schema.

    Args:
        schema_type: The type(s) specified by the schema.

    Returns:
        A type string. If argument ``schema_type`` is None, it returns None.
    """
    if schema_type is None or type(schema_type) == str:
        return schema_type
    elif len(schema_type) <= 0:
        raise ValueError("type must not be an empty list.")
    else:
        return random.choice(schema_type)
