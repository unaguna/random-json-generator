import string
import re
import rstr

__default_schema = {
    "pattern": None,
    "minLength": 1,
    "maxLength": 100,
}


def genstr(schema: dict) -> str:
    """スキーマに適合する文字列を生成する。

    Args:
        schema (dict): string 型についての JsonSchema を表現するマップ

    Returns:
        str: 生成された文字列
    """

    schema = __normalize_schema(schema)

    pattern = re.compile(schema["pattern"]) if schema["pattern"] is not None else None
    min_length = schema["minLength"]
    max_length = schema["maxLength"]

    # pattern の指定がある場合、それを使用する
    if pattern is not None:
        generated = rstr.xeger(pattern)
    # maxLength が 0 の場合、空文字でよい
    elif max_length is not None and max_length <= 0:
        generated = ""
    # いずれにも当てはまらない場合、英字列を生成する。
    else:
        generated = rstr.rstr(string.ascii_letters, start_range=min_length, end_range=max_length)

    return generated


def __normalize_schema(schema: dict) -> dict:
    """スキーマの正規化。乱数生成に使用しやすくするため、JsonSchema の未設定の項目を設定する。

    Args:
        schema (dict): number 型についての JsonSchema を表現するマップ

    Returns:
        dict: schema が持つ値とデフォルト値によって新たに作られた JsonSchema。
    """

    n_schema = __default_schema.copy()
    n_schema.update(schema)

    # maxLength = 0 の場合、minLength は無視する。
    if n_schema["maxLength"] <= 0:
        n_schema["minLength"] = None

    return n_schema
