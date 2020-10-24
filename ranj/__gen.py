import ranj.__gendict as __gendict
import ranj.__genlist as __genlist
import ranj.__genint as __genint
import ranj.__gennum as __gennum
import ranj.__gennone as __gennone
import ranj.__genbool as __genbool
import ranj.__genstr as __genstr
import ranj.__genany as __genany

def gen(schema: dict):

    # TODO: Type が複数の場合の処理

    if "type" not in schema:
        return __genany.genany(schema)
    if schema["type"] == "null":
        return __gennone.gennone(schema)
    if schema["type"] == "integer":
        return __genint.genint(schema)
    if schema["type"] == "number":
        return __gennum.gennum(schema)
    if schema["type"] == "boolean":
        return __genbool.genbool(schema)
    if schema["type"] == "string":
        return __genstr.genstr(schema)
    if schema["type"] == "object":
        return __gendict.gendict(schema)
    if schema["type"] == "array":
        return __genlist.genlist(schema)
    else:
        raise Exception("Unsuported type: {}".format(schema["type"]))
