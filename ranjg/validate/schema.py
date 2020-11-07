import jsonschema
from ..error import InvalidSchemaError

# スキーマのスキーマ
__meta_schema = {
    "type": "object",
    "additionalProperties": True,
    "properties": {
        "type": {
            "type": "string",
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
    try:
        jsonschema.validate(schema, __meta_schema)
    except jsonschema.exceptions.ValidationError as e:
        raise InvalidSchemaError from e
