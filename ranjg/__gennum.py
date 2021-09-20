from typing import Optional

from ._context import GenerationContext
from .options import Options
from .factories import NumFactory


def gennum(schema: Optional[dict] = None,
           *,
           schema_is_validated: bool = False,
           options: Optional[Options] = None,
           context: Optional[GenerationContext] = None) -> float:
    """Generate a random number according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.
        schema_is_validated: Whether the schema is already validated or not.
        options: Options for generation.
        context: The context of construction.

    Returns:
        Generated number.
    """
    return NumFactory(schema, schema_is_validated=schema_is_validated).gen(options=options, context=context)
