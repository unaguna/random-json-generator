import abc
from typing import TypeVar, Generic

_T = TypeVar('_T')


class _Generator(abc.ABC, Generic[_T]):

    @abc.abstractmethod
    def gen(self,
            schema: dict,
            *,
            schema_is_validated: bool = False) -> _T:
        pass
