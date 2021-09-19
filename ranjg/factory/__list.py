import collections
import random
from typing import Tuple, Optional, Sequence, Iterable, Union

import ranjg
from .__common import Factory
from .._context import GenerationContext, SchemaContext
from ..error import SchemaConflictError
from ..options import Options
from ..util.listutil import fix_length


def _schema_is_tuple_validation(schema: dict) -> bool:
    """Determines if the schema is for a tuple validation or not.

    Args:
        schema: JSON schema object for list values.

    Returns:
        True if the schema is for a tuple validation, otherwise False.
    """

    items = schema.get("items")
    return isinstance(items, collections.Sequence)


def _get_range_of_length(schema: dict, context: SchemaContext) -> Tuple[Optional[int], Optional[int]]:
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
        raise SchemaConflictError("There are no integers in the range of length specified by the schema.", context)

    # schema がタプル指定である場合
    if _schema_is_tuple_validation(schema):
        items = list(schema.get("items"))
        additional_items = schema.get("additionalItems")

        if additional_items is False:
            if min_items is not None and len(items) < min_items:
                raise SchemaConflictError(
                    "In tuple validation, when \"additionalItems\" is false, \"minItems\" must be less than or equal "
                    "to size of \"items\".", context)
            elif max_items is not None:
                return min_items, min(max_items, len(items))
            else:
                return min_items, len(items)

        else:
            return min_items, max_items

    # schema がリスト指定である場合
    else:
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


class ListFactory(Factory[list]):
    _tuple_items_factory: Sequence[Factory]
    _other_items_factory: Optional[Factory]

    def __init__(self, schema: Optional[dict], *,
                 schema_is_validated: bool = False, context: Optional[SchemaContext] = None):
        super(ListFactory, self).__init__(schema, schema_is_validated=schema_is_validated, context=context)

        if context is None:
            context = SchemaContext.root(self._schema)

        # 生成する list の大きさの範囲
        min_items, max_items = _get_range_of_length(self._schema, context)
        self._min_items, self._max_items = _apply_default_length(min_items, max_items)

        if _schema_is_tuple_validation(self._schema):
            self._tuple_items_factory = [ranjg.factory.create_factory(item_schema, schema_is_validated=True,
                                                                      context=context.resolve(i, item_schema))
                                         for i, item_schema in enumerate(self._schema["items"])]
            additional_items_schema: Union[bool, dict, None] = self._schema.get("additionalItems")
            if additional_items_schema is not None and not isinstance(additional_items_schema, bool):
                self._other_items_factory = \
                    ranjg.factory.create_factory(additional_items_schema,
                                                 schema_is_validated=True,
                                                 # TODO: additionalItems 用のパスを検討
                                                 context=context.resolve('additionalItems', additional_items_schema))
            else:
                self._other_items_factory = None
        else:
            self._tuple_items_factory = tuple()
            items_schema = self._schema.get("items")
            if items_schema is not None:
                self._other_items_factory = ranjg.factory.create_factory(items_schema,
                                                                         schema_is_validated=True,
                                                                         # TODO: items 用のパスを検討
                                                                         context=context.resolve('items', items_schema))
            else:
                self._other_items_factory = None

    def _get_other_items_factory(self, options: Options) -> Factory:
        if self._other_items_factory is not None:
            return self._other_items_factory
        else:
            # TODO: options 用の context を指定する
            return ranjg.factory.create_factory(options.default_schema_of_items)

    def _get_items_factory_list(self, item_count: int, options: Options) -> Iterable[Factory]:
        return fix_length(self._tuple_items_factory, item_count,
                          padding_item=self._get_other_items_factory(options))

    def gen(self,
            *,
            options: Optional[Options] = None,
            context: Optional[GenerationContext] = None) -> list:
        if options is None:
            options = Options.default()
        if context is None:
            context = GenerationContext.root(self._schema)

        # 生成するリスト
        result = []

        # 生成する list の大きさ
        item_count = random.randint(self._min_items, self._max_items)

        # 各要素のファクトリ
        item_factory_list = self._get_items_factory_list(item_count, options)

        # 要素を1つずつ生成
        for key, item_factory in enumerate(item_factory_list):
            generated_item = item_factory.gen(options=options, context=context.resolve(key, item_factory._schema))
            result.append(generated_item)

        return result
