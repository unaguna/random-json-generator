from typing import Tuple, Union, Iterable


class Context:
    """Context of randomly construction.
    """
    _path: Tuple[Union[int, str]]
    _current_schema: dict

    def __init__(self, path: Iterable[Union[int, str]], current_schema: dict):
        self._path = tuple(path)
        self._current_schema = current_schema

    @property
    def path(self) -> Tuple[Union[int, str]]:
        return self._path
