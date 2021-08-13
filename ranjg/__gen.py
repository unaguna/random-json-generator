import json
import random
from typing import Union, List, Optional, TextIO

from ._context import Context
from .options import Options
from .options import load as load_options
from ._generator import get_generator
from .schema import load as load_schema
from .schema import validate as validate_schema


def gen(schema: dict = None,
        schema_file: str = None,
        output_file: str = None,
        output_fp: TextIO = None,
        schema_is_validated: bool = False,
        options: Optional[Options] = None,
        options_file: str = None,
        context: Optional[Context] = None):
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
        options (Options, optional):
            The options for generation.
        options_file (str, optional):
            The path to options file. This is parsed as JSON to an Options instance.
        context (Context):
            The context of construction.

    Returns:
        Generated something. It is satisfies the JSON schema.

    Raises:
        SchemaFileIOError:
            When loading schema_file is failed
        OptionsFileIOError:
            When loading options_file is failed
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
    if schema is not None and schema_file is not None:
        raise ValueError("Only one of schema and schema_file can be set.")
    if output_file is not None and output_fp is not None:
        raise ValueError("Only one of output_file and output_fp can be set. (You don't have to set either one.)")
    if options is not None and options_file is not None:
        raise ValueError("Only one of options and options_file can be set. (You don't have to set either one.)")

    # スキーマファイルを読み込み
    if schema_file is not None:
        schema = load_schema(schema_file)

    # スキーマの不正判定
    if not schema_is_validated:
        validate_schema(schema)

    # オプションファイルを読み込み
    if options_file is not None:
        options = load_options(options_file)

    gen_type = _raffle_type(schema.get("type"))
    generator = get_generator(gen_type)

    # ランダムに値を生成
    generated = generator.gen(schema, schema_is_validated=True, options=options, context=context)

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
