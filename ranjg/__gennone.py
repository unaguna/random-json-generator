from typing import Optional

from ._context import Context
from ._generator import NoneGenerator


def gennone(schema: Optional[dict] = None, context: Optional[Context] = None) -> None:
    """Generate ``None``.

    Returns:
        Generated ``None``.
    """
    return NoneGenerator().gen(schema, context=context)
