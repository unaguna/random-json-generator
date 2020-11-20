import collections
import random
from typing import List, Optional, Tuple
import ranjg
from ranjg.util.listutil import fix_length
from ranjg.util.nonesafe import dfor
from .validate.schema import validate_schema
from .error import SchemaConflictError

# 配列の要素の値の生成に使用するスキーマのデフォルト値。
# items に指定がない場合に使用する。
__default_items_schema = {
    "type": "number",
    "minimum": 0,
    "maximum": 0,
}


def genlist(schema: dict, schema_is_validated: bool = False) -> list:
    """Generate a random list according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.
        schema_is_validated: Whether the schema is already validated or not.

    Returns:
        Generated list.
    """

    # スキーマの不正判定
    if not schema_is_validated:
        validate_schema(schema)

    # 生成するリスト
    result = []

    # 生成する list の大きさの範囲
    min_items, max_items = _get_range_of_length(schema)
    min_items, max_items = _apply_default_length(min_items, max_items)

    # 生成する list の大きさ
    item_count = random.randint(min_items, max_items)

    # 各要素のスキーマ
    item_schema_list = __get_items_schema_list(schema, item_count)

    # 要素を1つずつ生成
    for item_schema in item_schema_list:
        generated_item = ranjg.gen(item_schema, schema_is_validated=True)
        result.append(generated_item)

    return result


def __schema_is_tuple_validation(schema: dict) -> bool:
    """Determines if the schema is for a tuple validation or not.

    Args:
        schema: JSON schema object for list values.

    Returns:
        True if the schema is for a tuple validation, otherwise False.
    """

    items = schema.get("items")
    return isinstance(items, collections.abc.Sequence)


def _get_range_of_length(schema: dict) -> Tuple[Optional[int], Optional[int]]:
    """Determine the range of the size of the list to be generated with the schema.

    If each of them are not specified in the schema, returns None. This function checks for inconsistencies in the
    schema. If it doesn't raise Error, there are no inconsistencies in the schema.

    Args:
        schema: JSON schema object for list values.

    Returns:
        The minimum and maximum size of the list to be generated. Not specified parameter will be None.

    Raises:
        SchemaConflictError: If there are inconsistencies in the schema.
    """

    min_items: int = schema.get("minItems")
    max_items: int = schema.get("maxItems")

    if min_items is not None and max_items is not None and min_items > max_items:
        raise SchemaConflictError("There are no integers in the range of length specified by the schema.")

    # schema がタプル指定である場合
    if __schema_is_tuple_validation(schema):
        items = list(schema.get("items"))
        additional_items = schema.get("additionalItems")

        if additional_items is False and len(items) < dfor(min_items, len(items)):
            raise SchemaConflictError(
                "In tuple validation, when \"additionalItems\" is false, \"minItems\" must be less than or equal to "
                "size of \"items\".")

    return min_items, max_items


def _apply_default_length(min_items: Optional[int], max_items: Optional[int]) -> Tuple[int, int]:
    """Apply default minItems and maxItems.

    Args:
        min_items: None or minimum length of the list to generate
        max_items: None or maximum length of the list to generate

    Returns:
        The minimum and maximum size of the list to be generated.
    """
    if min_items is None:
        if max_items is None:
            min_items = 1
        else:
            min_items = min(1, max_items)

    if max_items is None:
        if min_items is None:
            max_items = 5
        else:
            max_items = max(5, min_items)

    return min_items, max_items


def __get_items_schema_list(schema: dict, item_count: int) -> List[dict]:
    """Returns a list of schemas for generating each element of the list generated by ``genlist``.

    If the schema is for tuple validation, this function returns a list similar to ``schema.items``.
    However, if the size of items is less than ``item_count``, ``schema.additionalItems`` is used for the missing part.

    If schema is for list validation, it returns a list containing ``item_count`` of ``items``.

    Args:
        schema: JSON schema object for list values.
        item_count: The length of the list to generate with ``genlist``.

    Returns:
        A list consisting of the schemas used to generate each element.
    """

    # タプル指定である場合
    if __schema_is_tuple_validation(schema):
        additional_items = schema.get('additionalItems')
        if additional_items is None or isinstance(additional_items, bool):
            additional_items = __default_items_schema

        return fix_length(schema["items"], item_count, padding_item=additional_items)
    # リスト指定である場合
    else:
        return item_count * [schema.get("items", __default_items_schema)]
