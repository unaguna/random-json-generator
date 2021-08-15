from typing import Optional

from ._context import Context
from .options import Options
from .factory import IntFactory


def genint(schema: Optional[dict] = None,
           *,
           schema_is_validated: bool = False,
           options: Optional[Options] = None,
           context: Optional[Context] = None) -> int:
    """Generate a random integer according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.
        schema_is_validated: Whether the schema is already validated or not.
        options: Options for generation.
        context: The context of construction.

    Returns:
        Generated integer value.
    """

    return IntFactory().gen(schema, schema_is_validated=schema_is_validated, options=options, context=context)
