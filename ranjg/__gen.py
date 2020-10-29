import json
from .__gennone import gennone
from .__genbool import genbool
from .__genint import genint
from .__gennum import gennum
from .__genstr import genstr
from .__gendict import gendict
from .__genlist import genlist
from .__genany import genany
from .util.nonesafe import dfor

def gen(schema: dict = None, schema_file: str = None):
    # TODO: schema と schema_file がともに None であるとき、エラー

    schema = dfor(schema, {})

    # スキーマファイルを読み込み
    if schema_file is not None:
        with open(schema_file) as fp:
            loaded_schema = json.load(fp)
            loaded_schema.update(schema)
            schema = loaded_schema

    # TODO: Type が複数の場合の処理

    if "type" not in schema:
        return genany(schema)
    if schema["type"] == "null":
        return gennone(schema)
    if schema["type"] == "integer":
        return genint(schema)
    if schema["type"] == "number":
        return gennum(schema)
    if schema["type"] == "boolean":
        return genbool(schema)
    if schema["type"] == "string":
        return genstr(schema)
    if schema["type"] == "object":
        return gendict(schema)
    if schema["type"] == "array":
        return genlist(schema)
    else:
        raise Exception("Unsuported type: {}".format(schema["type"]))
