import ranjg.__gendict as __gendict
import ranjg.__genlist as __genlist
import ranjg.__genint as __genint
import ranjg.__gennum as __gennum
import ranjg.__gennone as __gennone
import ranjg.__genbool as __genbool
import ranjg.__genstr as __genstr
import ranjg.__genany as __genany

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
