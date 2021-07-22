from typing import Optional

from ._context import Context
from ._generator import NumGenerator


def gennum(schema: dict, context: Optional[Context] = None) -> float:
    """Generate a random number according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.
        context: The context of construction.

    Returns:
        Generated number.
    """
    return NumGenerator().gen(schema, context=context)
