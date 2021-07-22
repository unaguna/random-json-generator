from ._generator import IntGenerator


def genint(schema: dict) -> int:
    """Generate a random integer according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.

    Returns:
        Generated integer value.
    """

    return IntGenerator().gen(schema)
