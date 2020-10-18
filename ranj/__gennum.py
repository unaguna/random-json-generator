import sys
import random

__default_schema = {
    "minimum": -sys.float_info.max / 2,
    "exclusiveMinimum": float('-inf'),
    "maximum": sys.float_info.max / 2,
    "exclusiveMaximum": float('inf'),
}

def gennum(schema: dict) -> float:
    """スキーマに適合する浮動小数点数を生成する。

    Args:
        schema (dict): number 型についての JsonSchema を表現するマップ

    Returns:
        float: 生成された浮動小数点数
    """

    schema = __normalize_schema(schema)

    # 生成する数値の最小値
    minimum = max(schema["minimum"], schema["exclusiveMinimum"])
    maximum = min(schema["maximum"], schema["exclusiveMaximum"])

    if(minimum > maximum):
        raise Exception("Minimum value must be lower than or equal to the maximum value.")

    if(maximum == schema["exclusiveMinimum"]):
        raise Exception("ExclusiveMinimum value must be lower than the maximum value.")

    if(minimum == schema["exclusiveMaximum"]):
        raise Exception("ExclusiveMaximum value must be greater than the minimum value.")

    # 境界値を許容しない Schema であっても、境界値を含む乱数生成を行うため、
    # Schema に合致する値を引くまで生成を繰り返す。
    generated = None
    while(not __validate(generated, schema)):
        generated = random.uniform(minimum, maximum)

        if generated == float("inf") or generated == float("-inf"):
            raise Exception("Error by too large maximum and too small minimum")

    return generated

def __normalize_schema(schema: dict) -> dict:
    """スキーマの正規化。乱数生成に使用しやすくするため、JsonSchema の未設定の項目を設定する。

    Args:
        schema (dict): number 型についての JsonSchema を表現するマップ

    Returns:
        dict: schema が持つ値とデフォルト値によって新たに作られた JsonSchema。
    """

    nSchema = __default_schema.copy()
    nSchema.update(schema)

    return nSchema

def __validate(value: float, schema: dict) -> bool:
    """値がスキーマに適合するかどうかチェックする。

    Args:
        value (float): チェック対象の値
        schema (dict): 正規化済みのJsonSchema

    Returns:
        bool: スキームに適合していれば True、そうでなければ False。　
    """

    if value is None:
        return False

    return schema["exclusiveMinimum"] < value < schema["exclusiveMaximum"] \
        and schema["minimum"] <= value <= schema["maximum"]

if __name__ == "__main__":
    schema1 = {
        "type": "number",
        "minimum": 0.0,
        "exclusiveMaximum": 1.0,
    }

    num1 = gennum(schema1)
    print(num1)
