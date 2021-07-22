import abc
from typing import TypeVar, Generic

from ..validate.schema import validate_schema

_T = TypeVar('_T')


class Generator(abc.ABC, Generic[_T]):

    def gen(self,
            schema: dict,
            *,
            schema_is_validated: bool = False) -> _T:
        # スキーマの不正判定
        if not schema_is_validated:
            validate_schema(schema)

        return self.gen_without_schema_check(schema)

    @abc.abstractmethod
    def gen_without_schema_check(self,
                                 schema: dict) -> _T:
        pass
