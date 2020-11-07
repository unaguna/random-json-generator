import collections
import random
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
    """スキーマに適合するリストを生成する。

    Args:
        schema (dict): array 型についての JsonSchema を表現するマップ
        schema_is_validated (bool): schema の不正判定がすでに行われているかどうか

    Returns:
        list: 生成されたリスト
    """

    # スキーマの不正判定
    if not schema_is_validated:
        validate_schema(schema)

    # 生成するリスト
    result = []

    # 生成する list の大きさの範囲
    [min_items, max_items] = __get_range_of_length(schema)

    # 生成する list の大きさ
    item_count = random.randint(min_items, max_items)

    # 各要素のスキーマ
    item_schema_list = __get_items_schema_list(schema, item_count)

    # 要素を1つずつ生成
    for item_schema in item_schema_list:
        result.append(ranjg.gen(item_schema))

    return result


def __schema_is_tuple_validation(schema: dict) -> bool:
    """スキーマがタプル指定かどうかを判定する。

    Args:
        schema (dict): array 型についての JsonSchema を表現するマップ

    Returns:
        bool: schema がタプル指定であれば True、リスト指定 (指定なしも含む) であれば False。
    """

    items = schema.get("items")
    return isinstance(items, collections.abc.Sequence)


def __get_range_of_length(schema: dict) -> [int, int]:
    """スキーマから、生成するlistの大きさの範囲を決定する。

    スキーマに指定がない場合でも、None は返さず2つの正整数値を返す。
    一方のみが None (null) である場合、もう一方に矛盾しない整数値を代わりに返す。
    両方が None (null) である場合、デフォルト値を返す。

    Args:
        schema (dict): array 型についての JsonSchema を表現するマップ

    Returns:
        [int, int]: 生成するリストの大きさの最小値と最大値
    """

    min_items: int = schema.get("minItems")
    max_items: int = schema.get("maxItems")

    # schema がタプル指定である場合
    if __schema_is_tuple_validation(schema):
        items = list(schema.get("items"))
        additional_items = schema.get("additionalItems")

        if additional_items is False and len(items) < dfor(min_items, len(items)):
            raise SchemaConflictError(
                "In tuple validation, when \"additionalItems\" is false, \"minItems\" must be less than or equal to "
                "size of \"items\".")
        if len(items) > dfor(max_items, len(items)):
            raise SchemaConflictError(
                "In tuple validation, \"maxItems\" must be greater than or equal to size of \"items\".")

        # タプル指定に合わせて、生成する list の大きさの最小値を設定
        if min_items is None or min_items < len(items):
            min_items = len(items)

        # タプル指定に合わせて、生成する list の大きさの最大値を設定
        # 追加の要素 (additionalItems) が許されないか指定がない場合は、最低限しか追加の要素を生成しない
        if additional_items is False or additional_items is None:
            max_items = min_items
        # 追加の要素を作る場合で、maxItem の指定がない場合は追加の要素を最大5個とする。
        # ただし、minItems がそれより大きい場合はそれに準ずる。
        elif max_items is None:
            max_items = max(min_items, len(items) + 5)

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

    return [min_items, max_items]


def __get_items_schema_list(schema: dict, item_count: int):
    """genlist で生成する list の各要素を生成する際のスキーマからなるリストを生成する。

    schema がタプル指定である場合、items リストと同様のリストを生成して返す。
    ただし、items の大きさが item_count に満たない場合、足りない部分には schema.additionalItems を使用する。

    schema がリスト指定である場合、items オブジェクトを item_count 個持つリストを返す。

    Args:
        schema (dict): array 型についての JsonSchema を表現するマップ
        item_count (int): genlist で生成する配列の大きさ

    Returns:
        List[dict]: 各要素の生成に用いるスキーマからなるリスト
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
