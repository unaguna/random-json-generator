import ranj.__gendict as __gendict
import ranj.__genint as __genint
import ranj.__gennum as __gennum
import ranj.__genstr as __genstr

def gen(schema: dict):

    # Type が複数の場合の処理

    if schema["type"] == "integer":
        return __genint.genint(schema)
    if schema["type"] == "number":
        return __gennum.gennum(schema)
    if schema["type"] == "string":
        return __genstr.genstr(schema)
    if schema["type"] == "object":
        return __gendict.gendict(schema)
    else:
        raise Exception("Unsuported type: {}".format(schema["type"]))
