from ._generator import StrGenerator


def genstr(schema: dict, schema_is_validated: bool = False) -> str:
    """Generate a random string value according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.
        schema_is_validated: Whether the schema is already validated or not.

    Returns:
        Generated string value.
    """
    return StrGenerator().gen(schema, schema_is_validated=schema_is_validated)
