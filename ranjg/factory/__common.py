import abc
from typing import TypeVar, Generic, Optional

from ..options import Options
from .._context import GenerationContext, SchemaContext
from ..schema import validate as validate_schema

_T = TypeVar('_T')


class Factory(abc.ABC, Generic[_T]):

    def __init__(self, schema: Optional[dict], *,
                 schema_is_validated: bool = False, context: Optional[SchemaContext]):
        # スキーマの不正判定
        if schema is not None and not schema_is_validated:
            validate_schema(schema)

    @abc.abstractmethod
    def gen(self,
            *,
            options: Optional[Options] = None,
            context: Optional[GenerationContext] = None) -> _T:
        pass
