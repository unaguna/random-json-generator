import jsonschema
from ..error import InvalidSchemaError

# スキーマのスキーマ
__meta_schema = {
    "type": "object",
    "additionalProperties": True,
    "properties": {
        "type": {
            "anyOf": [
                {"$ref": "#/definitions/type_single"},
                {
                    "type": "array",
                    "items": {"$ref": "#/definitions/type_single"},
                },
            ],
        },
        "items": {
            "anyOf": [
                {"$ref": "#"},
                {
                    "type": "array",
                    "items": {"$ref": "#"},
                },
            ],
        },
        "minItems": {
            "type": "number",
            "multipleOf": 1,
            "minimum": 0,
        },
        "maxItems": {
            "type": "number",
            "multipleOf": 1,
            "minimum": 0,
        },
    },
    "definitions": {
        "type_single": {
            "enum": ["null", "boolean", "integer", "number", "string", "array", "object"],
        },
    },
}


def validate_schema(schema: dict):
    """スキーマのバリデーション

    スキーマに不正がないかどうかを判定する。

    Args:
        schema:
            判定するスキーマ
    Raises:
        InvalidSchemaError:
            schema が不正であるとき
    """
    validate_error_list = [*jsonschema.Draft7Validator(__meta_schema).iter_errors(schema)]

    # schema が不正でなければ終了
    if len(validate_error_list) <= 0:
        return

    raise InvalidSchemaError(validate_error_list)
