import ranjg

# 使用するスキーマ
__default_schema = {
    "type": "null",
}


def genany(schema: dict):
    # TODO: schema もマージして使用する
    return ranjg.gen(__default_schema)
