import random
import ranj.__gen as ranjg

# 配列の要素の値の生成に使用するスキーマのデフォルト値。
# items に指定がない場合に使用する。
__default_items_schema = {
    "type": "number",
    "minimum": 0,
    "maximum": 0,
}

def genlist(schema: dict) -> list:
    """スキーマに適合するリストを生成する。

    Args:
        schema (dict): array 型についての JsonSchema を表現するマップ

    Returns:
        list: 生成されたリスト
    """

    # 生成するリスト
    result = []

    # 生成する list の大きさの範囲
    [min_items, max_items] = __get_length(schema)

    # 生成する list の大きさ
    item_count = random.randint(min_items, max_items)

    # 要素のスキーマ
    items_schema = schema.get("items", __default_items_schema)

    # 要素を1つずつ生成
    for i in range(item_count):
        result.append(ranjg.gen(items_schema))

    return result

def __get_length(schema: dict) -> [int, int]:
    """スキーマから minLength, maxLength の値を読み取る。

    スキーマに指定がない場合でも、None は返さず2つの正整数値を返す。
    一方のみが None (null) である場合、もう一方に矛盾しない整数値を代わりに返す。
    両方が None (null) である場合、デフォルト値を返す。

    Args:
        schema (dict): array 型についての JsonSchema を表現するマップ

    Returns:
        [int, int]: 生成するリストの大きさの最小値と最大値
    """

    minItems: int = schema.get("minItems")
    maxItems: int = schema.get("maxItems")

    if minItems is None:
        if maxItems is None:
            minItems = 1
        else:
            minItems = min(1, maxItems)
    
    if maxItems is None:
        if minItems is None:
            maxItems = 5
        else:
            maxItems = max(5, minItems)
    
    return [minItems, maxItems]
