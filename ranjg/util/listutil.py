from typing import Iterable, TypeVar, Callable, Sequence

_T = TypeVar('_T')


def diff(base: Iterable, removed: Iterable) -> list:
    """Subtraction of the list.

    Args:
        base: A base list.
        removed: A list of elements to be stripped from the base.

    Returns:
        A list contains only elements in ``base`` and not in ``removed``.
    """
    result = list(base).copy()
    for value in removed:
        try:
            result.remove(value)
        except ValueError:
            # do nothing
            continue

    return result


def fix_length(base: Sequence, length: int, padding_item) -> Sequence:
    """Generating a list with a different length to the base list.

    If the length of ``base`` is equal to or greater than ``length``, it returns a list of ``length - 1`` elements from
    the top of ``base``.

    If the length of ``base`` is less than ``length``, it returns a list of size ``length`` created by adding one or
    more ``padding_item`` to the end of the copy of ``base``.

    Args:
        base: A base list.
        length: The length of the list to generate.
        padding_item: Elements to be added at the end if ``base`` has length shorter than ``length``.

    Returns:
        list: List of size ``length``, generated from base.
    """

    if len(base) >= length:
        return base[:length]
    else:
        return list(base) + [padding_item] * (length - len(base))


def count(function: Callable[[_T], bool], iterable: Iterable[_T]) -> int:
    """Count items in iterable.
    """
    return sum(1 for _ in filter(function, iterable))
