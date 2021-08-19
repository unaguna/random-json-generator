import random
from typing import Optional, Dict, Sequence

from .__function import _create_factory_by_type
from .__common import Factory
from .._context import Context
from ..options import Options


class MultiFactory(Factory[None]):
    _schema: dict
    _factories: Dict[str, Factory]
    _type_list: Sequence[str]

    def __init__(self, schema: Optional[dict], *, schema_is_validated: bool = False):
        super(MultiFactory, self).__init__(schema, schema_is_validated=schema_is_validated)

        # TODO: schema['type'] がリストでない場合 (strであるばあいを含む) 例外を生じる
        self._type_list = schema['type']

        self._factories = {}
        for schema_type in self._type_list:
            # 各 type の factory を生成
            # 親クラスの__init__でバリデーションチェックは済んでいるので schema_is_validated=True
            self._factories[schema_type] = _create_factory_by_type(schema_type, schema_is_validated=True,
                                                                   schema=schema)

    def gen(self,
            *,
            options: Optional[Options] = None,
            context: Optional[Context] = None) -> None:
        schema_type = random.choice(self._type_list)
        return self._factories[schema_type].gen(options=options, context=context)
