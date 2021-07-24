from typing import Optional

from ._context import Context
from ._generator import ListGenerator


def genlist(schema: dict, schema_is_validated: bool = False, context: Optional[Context] = None) -> list:
    """Generate a random list according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.
        schema_is_validated: Whether the schema is already validated or not.
        context: The context of construction.

    Returns:
        Generated list.
    """
    return ListGenerator().gen(schema, schema_is_validated=schema_is_validated, context=context)
