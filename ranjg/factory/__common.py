import abc
from typing import TypeVar, Generic, Optional

from ..options import Options
from .._context import Context
from ..schema import validate as validate_schema

_T = TypeVar('_T')


class Factory(abc.ABC, Generic[_T]):

    def gen(self,
            schema: Optional[dict],
            *,
            options: Optional[Options] = None,
            context: Optional[Context] = None,
            schema_is_validated: bool = False) -> _T:
        # スキーマの不正判定
        if not schema_is_validated:
            validate_schema(schema)

        return self.gen_without_schema_check(schema, context=context, options=options)

    @abc.abstractmethod
    def gen_without_schema_check(self,
                                 schema: Optional[dict],
                                 *,
                                 options: Optional[Options] = None,
                                 context: Optional[Context] = None) -> _T:
        pass
