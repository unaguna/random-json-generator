import abc
from typing import TypeVar, Generic, Optional

from ..options import Options
from .._context import Context
from ..schema import validate as validate_schema

_T = TypeVar('_T')


class Factory(abc.ABC, Generic[_T]):

    def __init__(self, schema: Optional[dict], *, schema_is_validated: bool = False):
        # スキーマの不正判定
        if schema is not None and not schema_is_validated:
            validate_schema(schema)

    def gen(self,
            *,
            options: Optional[Options] = None,
            context: Optional[Context] = None) -> _T:

        return self.gen_without_schema_check(context=context, options=options)

    @abc.abstractmethod
    def gen_without_schema_check(self,
                                 *,
                                 options: Optional[Options] = None,
                                 context: Optional[Context] = None) -> _T:
        pass
