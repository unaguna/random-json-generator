from typing import Optional

from ._context import Context
from ._generator import BoolGenerator


def genbool(schema: Optional[dict] = None, context: Optional[Context] = None) -> bool:
    """Generate a random boolean value according to the JSON schema.

    Returns:
        Generated boolean value.
    """
    return BoolGenerator().gen(schema, context=context)
