from typing import Optional

from ._context import GenerationContext
from .options import Options
from .factory import BoolFactory


def genbool(schema: Optional[dict] = None,
            *,
            schema_is_validated: bool = False,
            options: Optional[Options] = None,
            context: Optional[GenerationContext] = None) -> bool:
    """Generate a random boolean value according to the JSON schema.

    Args:
        schema: JSON schema object.
        schema_is_validated: Whether the schema is already validated or not.
        options: Options for generation.
        context: The context of construction.

    Returns:
        Generated boolean value.
    """
    return BoolFactory(schema, schema_is_validated=schema_is_validated).gen(options=options, context=context)
