from typing import Optional

from ._context import Context
from .options import Options
from .factory import NoneFactory


def gennone(schema: Optional[dict] = None,
            *,
            schema_is_validated: bool = False,
            options: Optional[Options] = None,
            context: Optional[Context] = None) -> None:
    """Generate ``None``.

    Args:
        schema: JSON schema object.
        schema_is_validated: Whether the schema is already validated or not.
        options: Options for generation.
        context: The context of construction.

    Returns:
        Generated ``None``.
    """
    return NoneFactory(schema, schema_is_validated=schema_is_validated).gen(options=options, context=context)
