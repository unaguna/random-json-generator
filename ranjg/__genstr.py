import string
import re
import rstr

__default_schema = {
    "pattern": None,
    "minLength": 1,
    "maxLength": 100,
}


def genstr(schema: dict) -> str:
    """Generate a random string value according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.

    Returns:
        Generated string value.
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
    """Schema normalization.

    To make it easier to use for randomly generation, set items to ``schema`` object.

    Args:
        schema: JSON schema for randomly generation.

    Returns:
        New schema based on ``schema`` and the default values.
    """

    n_schema = __default_schema.copy()
    n_schema.update(schema)

    # maxLength = 0 の場合、minLength は無視する。
    if n_schema["maxLength"] <= 0:
        n_schema["minLength"] = None

    return n_schema
