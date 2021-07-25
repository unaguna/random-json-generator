from typing import Optional

from ._context import Context
from ._generator import BoolGenerator


def genbool(schema: Optional[dict] = None,
            *,
            schema_is_validated: bool = False,
            context: Optional[Context] = None) -> bool:
    """Generate a random boolean value according to the JSON schema.

    Args:
        schema: JSON schema object.
        schema_is_validated: Whether the schema is already validated or not.
        context: The context of construction.

    Returns:
        Generated boolean value.
    """
    return BoolGenerator().gen(schema, schema_is_validated=schema_is_validated, context=context)
