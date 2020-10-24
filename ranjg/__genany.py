import ranjg.__gen as __gen

# 使用するスキーマ
__default_schema = {
    "type": "null",
}

def genany(schema: dict):
    return __gen.gen(__default_schema)
