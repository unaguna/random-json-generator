import random
from typing import Optional, List, Iterable

from .__function import _create_factory_by_type
from .__common import Factory
from .._context import Context
from ..options import Options


class MultiFactory(Factory[None]):
    _schema: dict
    _factories: List[Factory]

    def __init__(self, schema: Optional[dict], *, schema_is_validated: bool = False):
        super(MultiFactory, self).__init__(schema, schema_is_validated=schema_is_validated)

        # schema['type'] がリストでない場合 (strであるばあいを含む) やリストが空である場合例外を生じる
        schema_type = schema.get('type')
        if isinstance(schema_type, str) or not isinstance(schema_type, Iterable) or len(schema_type) <= 0:
            raise ValueError('For MultiFactory, schema.type must be iterable of at least 1 strings')

        # 各 type の factory を生成
        # 親クラスの__init__でバリデーションチェックは済んでいるので schema_is_validated=True
        self._factories = [_create_factory_by_type(typ, schema_is_validated=True, schema=schema)
                           for typ in schema_type]

    def gen(self,
            *,
            options: Optional[Options] = None,
            context: Optional[Context] = None) -> None:
        factory = random.choice(self._factories)
        return factory.gen(options=options, context=context)
