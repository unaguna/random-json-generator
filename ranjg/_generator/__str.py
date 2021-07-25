import re
import string
from typing import Optional

import rstr

from .__common import Generator
from .._context import Context
from ..error import SchemaConflictError

__default_schema = {
    "pattern": None,
    "minLength": 1,
    "maxLength": 100,
}


def _normalize_schema(schema: dict, context: Context) -> dict:
    """Schema normalization.

    To make it easier to use for randomly generation, set items to ``schema`` object.

    Args:
        schema: JSON schema for randomly generation.

    Returns:
        New schema based on ``schema`` and the default values.
    """
    if schema.get("minLength", float("-inf")) > schema.get("maxLength", float("inf")):
        raise SchemaConflictError("\"minLength\" must be lower than or equal to the \"maxLength\" value.", context)

    n_schema = __default_schema.copy()
    n_schema.update(schema)

    # maxLength = 0 の場合、minLength は無視する。
    if n_schema["maxLength"] <= 0:
        n_schema["minLength"] = None

    return n_schema


class StrGenerator(Generator[str]):

    def gen_without_schema_check(self,
                                 schema: Optional[dict],
                                 *,
                                 context: Optional[Context] = None) -> str:
        if schema is None:
            schema = {}
        if context is None:
            context = Context.root(schema)

        schema = _normalize_schema(schema, context)

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
