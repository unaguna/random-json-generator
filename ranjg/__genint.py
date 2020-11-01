import random
from .error import SchemaConflictError


def genint(schema: dict) -> int:
    """スキーマに適合する整数を生成する。

    Args:
        schema (dict): integer 型についての JsonSchema を表現するマップ

    Returns:
        int: 生成された整数
    """

    schema = __normalize_schema(schema)

    minimum: int = schema["minimum"]
    maximum: int = schema["maximum"]

    if minimum > maximum:
        raise SchemaConflictError("Minimum value must be lower than or equal to the maximum value.")

    return random.randint(minimum, maximum)


def __normalize_schema(schema: dict) -> dict:
    """スキーマの正規化。乱数生成に使用しやすくするため、JsonSchema の未設定の項目を設定する。

    Args:
        schema (dict): integer 型についての JsonSchema を表現するマップ

    Returns:
        dict: schema が持つ値とデフォルト値によって新たに作られた JsonSchema。
    """

    # 生成する数値の最小値
    inclusive_minimum = schema.get("minimum", None)
    exclusive_minimum = schema.get("exclusiveMinimum", None)
    if exclusive_minimum == True:
        exclusive_minimum = inclusive_minimum
        inclusive_minimum = None
    elif exclusive_minimum == False:
        exclusive_minimum = None
    minimum = 0
    if inclusive_minimum is not None and exclusive_minimum is not None:
        minimum = max(inclusive_minimum, exclusive_minimum + 1)
    elif exclusive_minimum is not None:
        minimum = exclusive_minimum + 1
    elif inclusive_minimum is not None:
        minimum = inclusive_minimum

    # 生成する数値の最大値
    inclusive_maximum = schema.get("maximum", None)
    exclusive_maximum = schema.get("exclusiveMaximum", None)
    if exclusive_maximum == True:
        exclusive_maximum = inclusive_maximum
        inclusive_maximum = None
    elif exclusive_maximum == False:
        exclusive_maximum = None
    maximum = 100
    if inclusive_maximum is not None and exclusive_maximum is not None:
        maximum = min(inclusive_maximum, exclusive_maximum - 1)
    elif exclusive_maximum is not None:
        maximum = exclusive_maximum - 1
    elif inclusive_maximum is not None:
        maximum = inclusive_maximum

    return {
        "minimum": minimum,
        "maximum": maximum,
    }
