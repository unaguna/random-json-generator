from ._generator.__float import NumGenerator


def gennum(schema: dict) -> float:
    """Generate a random number according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.

    Returns:
        Generated number.
    """
    return NumGenerator().gen(schema)
