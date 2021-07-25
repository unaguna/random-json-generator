from typing import Optional

from ._context import Context
from ._generator import NoneGenerator


def gennone(schema: Optional[dict] = None,
            *,
            schema_is_validated: bool = False,
            context: Optional[Context] = None) -> None:
    """Generate ``None``.

    Args:
        schema: JSON schema object.
        schema_is_validated: Whether the schema is already validated or not.
        context: The context of construction.

    Returns:
        Generated ``None``.
    """
    return NoneGenerator().gen(schema, schema_is_validated=schema_is_validated, context=context)
