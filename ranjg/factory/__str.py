import re
import string
from typing import Optional

import rstr

from .__common import Factory
from .._context import GenerationContext
from ..error import SchemaConflictError
from ..options import Options


def _normalize_schema(schema: dict, options: Options, context: GenerationContext) -> dict:
    """Schema normalization.

    To make it easier to use for randomly generation, set items to ``schema`` object.

    Args:
        schema: JSON schema for randomly generation.

    Returns:
        New schema based on ``schema`` and the default values.
    """
    if schema.get("minLength", float("-inf")) > schema.get("maxLength", float("inf")):
        raise SchemaConflictError("\"minLength\" must be lower than or equal to the \"maxLength\" value.", context)

    n_schema = schema.copy()
    n_schema.setdefault("pattern", None)

    # minLength と maxLength がともに指定されていない場合、デフォルト設定を使う
    if "minLength" not in n_schema and "maxLength" not in n_schema:
        n_schema["minLength"] = max(0, options.default_min_length_of_string)
        n_schema["maxLength"] = options.default_max_length_of_string

        if n_schema["minLength"] > n_schema["maxLength"]:
            raise SchemaConflictError("\"options.default_min_length_of_string\" must be lower than or equal to the "
                                      "\"options.default_max_length_of_string\" value.", context)
    # minLength が設定されていて maxLength が指定されていない場合
    elif "maxLength" not in n_schema:
        length_range = max(0, options.default_length_range_of_genstr)
        n_schema["maxLength"] = n_schema["minLength"] + length_range
    # maxLength が設定されていて minLength が指定されていない場合
    elif "minLength" not in n_schema:
        length_range = max(0, options.default_length_range_of_genstr)
        n_schema["minLength"] = max(0, n_schema["maxLength"] - length_range)

    return n_schema


class StrFactory(Factory[str]):
    _schema: dict

    def __init__(self, schema: Optional[dict], *, schema_is_validated: bool = False):
        super(StrFactory, self).__init__(schema, schema_is_validated=schema_is_validated)

        self._schema = schema if schema is not None else {}

    def gen(self,
            *,
            options: Optional[Options] = None,
            context: Optional[GenerationContext] = None) -> str:
        if options is None:
            options = Options.default()
        if context is None:
            context = GenerationContext.root(self._schema)

        schema = _normalize_schema(self._schema, options, context)

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
