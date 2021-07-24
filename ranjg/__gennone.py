from typing import Optional

from ._context import Context
from ._generator import NoneGenerator


def gennone(schema: dict = None, context: Optional[Context] = None) -> None:
    """Generate ``None``.

    Returns:
        Generated ``None``.
    """
    if schema is None:
        schema = {}

    return NoneGenerator().gen(schema, context=context)
