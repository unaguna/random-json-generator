import json
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
        output_fp=None,
        schema_is_validated: bool = False):
    """Generate something randomly according to the JSON schema.

    This function is not fully compliant with the JSON schema, and unsupported parameters in the schema are ignored.

    Args:
        schema: JSON schema object.
        schema_file: The path to JSON schema file. This JSON schema is used instead of ``schema``.
        output_file: The path to a file where the result will be output as JSON.
        output_fp: The writing object of a file where the result will be output as JSON.
        schema_is_validated: Whether the schema is already validated or not.

    Returns:
        Generated something. It is satisfies the JSON schema.
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

    # TODO: Type が複数の場合の処理
    gen_type = schema.get("type")

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
