from typing import Optional

from ._context import Context
from ._generator import IntGenerator


def genint(schema: Optional[dict], context: Optional[Context] = None) -> int:
    """Generate a random integer according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.
        context: The context of construction.

    Returns:
        Generated integer value.
    """

    return IntGenerator().gen(schema, context=context)
